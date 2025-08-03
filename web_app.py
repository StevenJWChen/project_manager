#!/usr/bin/env python3
"""
Web interface for Project Management System
With automatic data reloading for real-time updates
"""
from flask import Flask, render_template, jsonify, request, redirect, url_for, send_file
from project_manager import ProjectManager, Task, TaskStatus, StageStatus
from notification_system import get_notification_system
import json
import logging
import os
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)

# Global variables for data management
_pm_instance = None
_last_file_mtime = 0
_data_file = "projects.json"

def get_project_manager():
    """Get ProjectManager instance with automatic data reloading"""
    global _pm_instance, _last_file_mtime, _data_file
    
    try:
        # Check if file exists and get modification time
        if os.path.exists(_data_file):
            current_mtime = os.path.getmtime(_data_file)
        else:
            current_mtime = 0
        
        # Create new instance or reload if file changed
        if _pm_instance is None or current_mtime > _last_file_mtime:
            logging.info(f"Reloading project data from {_data_file}")
            _pm_instance = ProjectManager(_data_file)
            _last_file_mtime = current_mtime
            
    except Exception as e:
        logging.error(f"Error loading project manager: {e}")
        if _pm_instance is None:
            _pm_instance = ProjectManager(_data_file)
    
    return _pm_instance

@app.route('/')
def dashboard():
    try:
        pm = get_project_manager()  # Get fresh data
        projects = pm.list_projects()
        categories = pm.list_categories()
        summary = pm.get_global_summary()
        
        # Add project count to categories
        for category in categories:
            category.project_count = len([p for p in projects if p.category_id == category.id])
        
        logging.info(f"Dashboard: {len(projects)} projects, {len(categories)} categories")
        return render_template('dashboard.html', projects=projects, categories=categories, summary=summary)
    except Exception as e:
        logging.error(f"Error rendering dashboard: {e}")
        return "Error loading dashboard", 500

@app.route('/projects')
def index():
    try:
        pm = get_project_manager()  # Get fresh data
        projects = pm.list_projects()
        categories = pm.list_categories()
        logging.info(f"Projects page: {len(projects)} projects, {len(categories)} categories")
        return render_template('index.html', projects=projects, categories=categories)
    except Exception as e:
        logging.error(f"Error rendering projects page: {e}")
        return "Error loading page", 500

@app.route('/summary')
def summary():
    try:
        pm = get_project_manager()  # Get fresh data
        global_summary = pm.get_global_summary()
        projects = pm.list_projects()
        projects_summary = []
        
        for p in projects:
            summary_data = p.get_project_summary()
            summary_data['id'] = p.id
            summary_data['name'] = p.name
            summary_data['description'] = p.description
            
            # Add category information
            if p.category_id:
                category = pm.get_category(p.category_id)
                summary_data['category_name'] = category.name if category else 'Unknown'
            else:
                summary_data['category_name'] = None
                
            projects_summary.append(summary_data)
        
        logging.info(f"Summary page: {global_summary['total_projects']} total projects")
        logging.info(f"Projects Summary: {len(projects_summary)} projects")
        return render_template('summary.html', summary=global_summary, projects=projects_summary)
    except Exception as e:
        logging.error(f"Error rendering summary page: {e}")
        return "Error loading summary page", 500

@app.route('/categories')
def categories():
    try:
        pm = get_project_manager()  # Get fresh data
        categories = pm.list_categories()
        default_category = pm.get_default_category()
        projects = pm.list_projects()
        logging.info(f"Categories page: {len(categories)} categories")
        return render_template('categories.html', categories=categories, default_category=default_category, projects=projects)
    except Exception as e:
        logging.error(f"Error rendering categories page: {e}")
        return "Error loading categories page", 500

@app.route('/category/<category_id>')
def category_detail(category_id):
    try:
        pm = get_project_manager()  # Get fresh data
        category = pm.get_category(category_id)
        if not category:
            return "Category not found", 404
        projects = pm.get_projects_by_category(category_id)
        logging.info(f"Category detail: {category.name}")
        return render_template('category_detail.html', category=category, projects=projects)
    except Exception as e:
        logging.error(f"Error rendering category detail page: {e}")
        return "Error loading category detail page", 500

@app.route('/project/<project_id>')
def project_detail(project_id):
    try:
        pm = get_project_manager()  # Get fresh data
        project = pm.get_project(project_id)
        if not project:
            return "Project not found", 404
        categories = pm.list_categories()
        logging.info(f"Project detail: {project.name}")
        return render_template('project_detail.html', project=project, categories=categories)
    except Exception as e:
        logging.error(f"Error rendering project detail page: {e}")
        return "Error loading project detail page", 500

# API Endpoints
@app.route('/api/projects')
def api_projects():
    try:
        pm = get_project_manager()  # Get fresh data
        projects = pm.list_projects()
        return jsonify([p.to_dict() for p in projects])
    except Exception as e:
        logging.error(f"Error in API /api/projects: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500

@app.route('/api/project/<project_id>')
def api_project_detail(project_id):
    try:
        pm = get_project_manager()  # Get fresh data
        project = pm.get_project(project_id)
        if not project:
            return jsonify({'error': 'Project not found'}), 404
        return jsonify(project.to_dict())
    except Exception as e:
        logging.error(f"Error in API /api/project/{project_id}: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500

@app.route('/api/create_project', methods=['POST'])
def api_create_project():
    try:
        pm = get_project_manager()  # Get fresh data
        data = request.json
        name = data.get('name')
        if not name:
            return jsonify({'error': 'Project name is required'}), 400
        
        # Check if using a template
        template_id = data.get('template_id')
        if template_id:
            project = pm.create_project_from_template(
                name,
                data.get('description', ''),
                data.get('deadline'),
                data.get('category_id'),
                template_id
            )
        else:
            project = pm.create_project(
                name,
                data.get('description', ''),
                data.get('stages', []),
                data.get('deadline'),
                data.get('category_id')
            )
        return jsonify(project.to_dict()), 201
    except Exception as e:
        logging.error(f"Error in API /api/create_project: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500

@app.route('/api/project/<project_id>/add_task', methods=['POST'])
def api_add_task(project_id):
    try:
        pm = get_project_manager()  # Get fresh data
        project = pm.get_project(project_id)
        if not project: return jsonify({'error': 'Project not found'}), 404
        
        current_stage = project.get_current_stage()
        if not current_stage: return jsonify({'error': 'No active stage found'}), 400

        data = request.json
        if not data.get('name'): return jsonify({'error': 'Task name is required'}), 400

        task = Task(data['name'], data.get('description', ''), data.get('assignee', ''))
        current_stage.add_task(task)
        pm.save_data()
        return jsonify(task.to_dict()), 201
    except Exception as e:
        logging.error(f"Error in API /api/project/{project_id}/add_task: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500

@app.route('/api/task/<task_id>/complete', methods=['POST'])
def api_complete_task(task_id):
    try:
        pm = get_project_manager()  # Get fresh data
        for p in pm.projects.values():
            for stage in p.stages:
                for task in stage.tasks:
                    if task.id == task_id:
                        task.status = TaskStatus.COMPLETED
                        task.complete()
                        
                        # Check if all tasks in this stage are completed
                        stage_tasks = stage.tasks
                        completed_tasks = [t for t in stage_tasks if t.status == TaskStatus.COMPLETED]
                        
                        if len(completed_tasks) == len(stage_tasks) and len(stage_tasks) > 0:
                            # All tasks completed, mark stage as complete
                            stage.status = StageStatus.COMPLETED
                            stage.completed_at = datetime.now().isoformat()
                            
                            # Check if we should advance to next stage
                            project_stages = p.stages
                            current_stage_index = project_stages.index(stage)
                            
                            if current_stage_index + 1 < len(project_stages):
                                # There's a next stage, start it
                                next_stage = project_stages[current_stage_index + 1]
                                if next_stage.status == StageStatus.NOT_STARTED:
                                    next_stage.start()
                        
                        pm.save_data()
                        return jsonify(task.to_dict())
        
        return jsonify({'error': 'Task not found'}), 404
    except Exception as e:
        logging.error(f"Error in API /api/task/{task_id}/complete: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500

@app.route('/api/task/<task_id>/update', methods=['POST'])
def api_update_task_status(task_id):
    try:
        pm = get_project_manager()  # Get fresh data
        data = request.json
        new_status = data.get('status')
        if not new_status:
            return jsonify({'error': 'Status is required'}), 400
        
        try:
            status_enum = TaskStatus(new_status)
        except ValueError:
            return jsonify({'error': 'Invalid status value'}), 400

        for p in pm.projects.values():
            for stage in p.stages:
                for task in stage.tasks:
                    if task.id == task_id:
                        task.status = status_enum
                        if status_enum == TaskStatus.COMPLETED:
                            task.complete()
                        pm.save_data()
                        return jsonify(task.to_dict())
        
        return jsonify({'error': 'Task not found'}), 404
    except Exception as e:
        logging.error(f"Error in API /api/task/{task_id}/update: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500

@app.route('/api/project/<project_id>/next_stage', methods=['POST'])
def api_next_stage(project_id):
    try:
        pm = get_project_manager()  # Get fresh data
        project = pm.get_project(project_id)
        if not project: return jsonify({'error': 'Project not found'}), 404
        
        success, message = project.advance_to_next_stage()
        pm.save_data()
        return jsonify({'success': success, 'message': message, 'project': project.to_dict()})
    except Exception as e:
        logging.error(f"Error in API /api/project/{project_id}/next_stage: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500

@app.route('/api/project/<project_id>/previous_stage', methods=['POST'])
def api_previous_stage(project_id):
    try:
        pm = get_project_manager()  # Get fresh data
        project = pm.get_project(project_id)
        if not project: return jsonify({'error': 'Project not found'}), 404

        success, message = project.go_back_to_previous_stage()
        pm.save_data()
        return jsonify({'success': success, 'message': message, 'project': project.to_dict()})
    except Exception as e:
        logging.error(f"Error in API /api/project/{project_id}/previous_stage: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500

@app.route('/api/summary')
def api_summary():
    try:
        pm = get_project_manager()  # Get fresh data
        return jsonify(pm.get_global_summary())
    except Exception as e:
        logging.error(f"Error in API /api/summary: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500

@app.route('/api/categories', methods=['GET', 'POST'])
def api_categories():
    try:
        pm = get_project_manager()  # Get fresh data
        if request.method == 'POST':
            data = request.json
            if not data.get('name'):
                return jsonify({'error': 'Category name is required'}), 400
            category = pm.create_category(data['name'], data.get('description', ''), data.get('color', '#007bff'))
            return jsonify(category.to_dict()), 201
        
        categories = pm.list_categories()
        return jsonify([c.to_dict() for c in categories])
    except Exception as e:
        logging.error(f"Error in API /api/categories: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500

@app.route('/api/category/<category_id>', methods=['DELETE'])
def api_delete_category(category_id):
    try:
        pm = get_project_manager()  # Get fresh data
        if pm.delete_category(category_id):
            return jsonify({'message': 'Category deleted successfully'})
        return jsonify({'error': 'Category not found'}), 404
    except Exception as e:
        logging.error(f"Error in API /api/category/{category_id}: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500

@app.route('/api/project/<project_id>/assign_category', methods=['POST'])
def api_assign_category(project_id):
    try:
        pm = get_project_manager()  # Get fresh data
        category_id = request.json.get('category_id')
        if pm.assign_project_to_category(project_id, category_id):
            return jsonify({'message': 'Category assigned successfully'})
        return jsonify({'error': 'Failed to assign category'}), 400
    except Exception as e:
        logging.error(f"Error in API /api/project/{project_id}/assign_category: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500

@app.route('/api/project/<project_id>/update', methods=['POST'])
def api_update_project(project_id):
    try:
        pm = get_project_manager()  # Get fresh data
        project = pm.get_project(project_id)
        if not project: return jsonify({'error': 'Project not found'}), 404
        
        data = request.json
        if 'deadline' in data: project.deadline = data['deadline']
        if 'category_id' in data: project.category_id = data['category_id']
        if 'name' in data: project.name = data['name']
        if 'description' in data: project.description = data['description']
        
        pm.save_data()
        return jsonify(project.to_dict())
    except Exception as e:
        logging.error(f"Error in API /api/project/{project_id}/update: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500

@app.route('/api/project/<project_id>/delete', methods=['DELETE'])
def api_delete_project(project_id):
    try:
        pm = get_project_manager()  # Get fresh data
        if pm.delete_project(project_id):
            return jsonify({'message': 'Project deleted successfully'})
        return jsonify({'error': 'Project not found'}), 404
    except Exception as e:
        logging.error(f"Error in API /api/project/{project_id}/delete: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500

@app.route('/api/default_category', methods=['GET', 'POST'])
def api_default_category():
    try:
        pm = get_project_manager()  # Get fresh data
        if request.method == 'POST':
            category_id = request.json.get('category_id')
            if pm.set_default_category(category_id):
                return jsonify({'message': 'Default category updated'})
            return jsonify({'error': 'Invalid category ID'}), 400
        
        default_category = pm.get_default_category()
        return jsonify(default_category.to_dict() if default_category else {'default_category': None})
    except Exception as e:
        logging.error(f"Error in API /api/default_category: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500

# Template Management Routes
@app.route('/templates')
def templates():
    try:
        pm = get_project_manager()  # Get fresh data
        templates = pm.list_templates()
        return render_template('templates.html', templates=templates)
    except Exception as e:
        logging.error(f"Error rendering templates page: {e}")
        return "Error loading templates page", 500

@app.route('/api/templates', methods=['GET', 'POST'])
def api_templates():
    try:
        pm = get_project_manager()  # Get fresh data
        if request.method == 'GET':
            templates = pm.list_templates()
            return jsonify(templates)
        else:  # POST - Create new template
            data = request.json
            name = data.get('name')
            description = data.get('description', '')
            stages = data.get('stages', [])
            
            if not name or not stages:
                return jsonify({'error': 'Name and stages are required'}), 400
            
            template_id = pm.create_template(name, description, stages)
            return jsonify({'id': template_id, 'success': True}), 201
    except Exception as e:
        logging.error(f"Error in API /api/templates: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500

@app.route('/api/template/<template_id>', methods=['GET', 'PUT', 'DELETE'])
def api_template(template_id):
    try:
        pm = get_project_manager()  # Get fresh data
        if request.method == 'GET':
            template = pm.get_template(template_id)
            if template:
                return jsonify(template)
            else:
                return jsonify({'error': 'Template not found'}), 404
        elif request.method == 'PUT':
            data = request.json
            name = data.get('name')
            description = data.get('description', '')
            stages = data.get('stages', [])
            
            if not name or not stages:
                return jsonify({'error': 'Name and stages are required'}), 400
            
            success = pm.update_template(template_id, name, description, stages)
            if success:
                return jsonify({'success': True})
            else:
                return jsonify({'error': 'Template not found or cannot be updated'}), 404
        else:  # DELETE
            success = pm.delete_template(template_id)
            if success:
                return jsonify({'success': True})
            else:
                return jsonify({'error': 'Template not found or cannot be deleted'}), 404
    except Exception as e:
        logging.error(f"Error in API /api/template/{template_id}: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500

# Import/Export Routes
@app.route('/api/export/projects')
def api_export_projects():
    try:
        pm = get_project_manager()  # Get fresh data
        projects = pm.list_projects()
        projects_data = [p.to_dict() for p in projects]
        return jsonify({
            'projects': projects_data,
            'exported_at': datetime.now().isoformat(),
            'count': len(projects_data)
        })
    except Exception as e:
        logging.error(f"Error in API /api/export/projects: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500

@app.route('/api/export/templates')
def api_export_templates():
    try:
        pm = get_project_manager()  # Get fresh data
        templates = pm.list_templates()
        return jsonify({
            'templates': templates,
            'exported_at': datetime.now().isoformat(),
            'count': len(templates)
        })
    except Exception as e:
        logging.error(f"Error in API /api/export/templates: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500

@app.route('/api/export/all')
def api_export_all():
    try:
        pm = get_project_manager()  # Get fresh data
        projects = pm.list_projects()
        templates = pm.list_templates()
        categories = pm.list_categories()
        
        return jsonify({
            'projects': [p.to_dict() for p in projects],
            'templates': templates,
            'categories': [c.to_dict() for c in categories],
            'exported_at': datetime.now().isoformat(),
            'counts': {
                'projects': len(projects),
                'templates': len(templates),
                'categories': len(categories)
            }
        })
    except Exception as e:
        logging.error(f"Error in API /api/export/all: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500

@app.route('/api/import/projects', methods=['POST'])
def api_import_projects():
    try:
        pm = get_project_manager()  # Get fresh data
        data = request.json
        if 'projects' not in data:
            return jsonify({'error': 'No projects data found'}), 400
        
        from project_manager import Project
        imported_count = 0
        for project_data in data['projects']:
            # Create project from imported data
            project = Project.from_dict(project_data)
            pm.projects[project.id] = project
            imported_count += 1
        
        pm.save_data()
        return jsonify({
            'message': f'Successfully imported {imported_count} projects',
            'imported_count': imported_count
        })
    except Exception as e:
        logging.error(f"Error in API /api/import/projects: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500

@app.route('/api/import/templates', methods=['POST'])
def api_import_templates():
    try:
        pm = get_project_manager()  # Get fresh data
        data = request.json
        if 'templates' not in data:
            return jsonify({'error': 'No templates data found'}), 400
        
        imported_count = 0
        for template in data['templates']:
            pm.templates[template['id']] = template
            imported_count += 1
        
        pm.save_data()
        return jsonify({
            'message': f'Successfully imported {imported_count} templates',
            'imported_count': imported_count
        })
    except Exception as e:
        logging.error(f"Error in API /api/import/templates: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500

@app.route('/api/import/all', methods=['POST'])
def api_import_all():
    try:
        pm = get_project_manager()  # Get fresh data
        data = request.json
        imported_counts = {'projects': 0, 'templates': 0, 'categories': 0}
        
        from project_manager import Project, Category
        
        # Import categories first
        if 'categories' in data:
            for category_data in data['categories']:
                category = Category.from_dict(category_data)
                pm.categories[category.id] = category
                imported_counts['categories'] += 1
        
        # Import templates
        if 'templates' in data:
            for template in data['templates']:
                pm.templates[template['id']] = template
                imported_counts['templates'] += 1
        
        # Import projects
        if 'projects' in data:
            for project_data in data['projects']:
                project = Project.from_dict(project_data)
                pm.projects[project.id] = project
                imported_counts['projects'] += 1
        
        pm.save_data()
        return jsonify({
            'message': f'Successfully imported {sum(imported_counts.values())} items',
            'imported_counts': imported_counts
        })
    except Exception as e:
        logging.error(f"Error in API /api/import/all: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500

# Batch Operations APIs
@app.route('/api/projects/batch_delete', methods=['POST'])
def api_batch_delete_projects():
    try:
        pm = get_project_manager()  # Get fresh data
        data = request.json
        project_ids = data.get('project_ids', [])
        
        if not project_ids:
            return jsonify({'error': 'No project IDs provided'}), 400
        
        deleted_count = 0
        failed_deletions = []
        
        for project_id in project_ids:
            if pm.delete_project(project_id):
                deleted_count += 1
            else:
                failed_deletions.append(project_id)
        
        if failed_deletions:
            return jsonify({
                'deleted_count': deleted_count,
                'failed_deletions': failed_deletions,
                'message': f'Deleted {deleted_count} projects. Failed to delete {len(failed_deletions)} projects.'
            }), 206  # Partial success
        
        return jsonify({
            'deleted_count': deleted_count,
            'message': f'Successfully deleted {deleted_count} projects'
        })
        
    except Exception as e:
        logging.error(f"Error in batch delete: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500

@app.route('/api/projects/batch_move_category', methods=['POST'])
def api_batch_move_category():
    try:
        pm = get_project_manager()  # Get fresh data
        data = request.json
        project_ids = data.get('project_ids', [])
        category_id = data.get('category_id')  # Can be None to remove category
        
        if not project_ids:
            return jsonify({'error': 'No project IDs provided'}), 400
        
        # Validate category exists if category_id is provided
        if category_id and not pm.get_category(category_id):
            return jsonify({'error': 'Category not found'}), 404
        
        updated_count = 0
        failed_updates = []
        
        for project_id in project_ids:
            if pm.assign_project_to_category(project_id, category_id):
                updated_count += 1
            else:
                failed_updates.append(project_id)
        
        if failed_updates:
            return jsonify({
                'updated_count': updated_count,
                'failed_updates': failed_updates,
                'message': f'Updated {updated_count} projects. Failed to update {len(failed_updates)} projects.'
            }), 206  # Partial success
        
        category_name = pm.get_category(category_id).name if category_id else 'Uncategorized'
        return jsonify({
            'updated_count': updated_count,
            'message': f'Successfully moved {updated_count} projects to {category_name}'
        })
        
    except Exception as e:
        logging.error(f"Error in batch move category: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500

# Notification System APIs
@app.route('/api/notification-settings', methods=['GET', 'POST'])
def api_notification_settings():
    try:
        notification_system = get_notification_system()
        
        if request.method == 'POST':
            settings = request.json
            success = notification_system.update_settings(settings)
            return jsonify({'success': success})
        else:
            # Return current settings
            config = notification_system.config
            return jsonify({
                'email': config['email']['address'],
                'phone': config['sms']['phone'],
                'emailEnabled': config['email']['enabled'],
                'smsEnabled': config['sms']['enabled'],
                'notifyDeadlines': config['preferences']['notify_deadlines'],
                'notifyCompletion': config['preferences']['notify_completion'],
                'notifyErrors': config['preferences']['notify_errors']
            })
    except Exception as e:
        logging.error(f"Error in notification settings API: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500

@app.route('/api/test-notifications', methods=['POST'])
def api_test_notifications():
    try:
        notification_system = get_notification_system()
        results = notification_system.test_notifications()
        return jsonify(results)
    except Exception as e:
        logging.error(f"Error testing notifications: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500

@app.route('/api/system-status')
def api_system_status():
    try:
        notification_system = get_notification_system()
        pm = get_project_manager()
        
        # Check system health
        status = {
            'web_interface': True,
            'data_persistence': os.path.exists(_data_file),
            'auto_reload': True,
            'notifications_configured': (
                notification_system.config['email']['enabled'] or 
                notification_system.config['sms']['enabled']
            ),
            'total_projects': len(pm.list_projects()),
            'timestamp': datetime.now().isoformat()
        }
        return jsonify(status)
    except Exception as e:
        logging.error(f"Error checking system status: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500

@app.route('/api/recent-activity')
def api_recent_activity():
    try:
        pm = get_project_manager()
        projects = pm.list_projects()
        
        activities = []
        
        # Get recent project activities
        for project in projects[-5:]:  # Last 5 projects
            activities.append({
                'title': f'Project Created: {project.name}',
                'description': f'New project added to {project.category_id or "Uncategorized"}',
                'time': project.created_at if hasattr(project, 'created_at') else 'Recently',
                'icon': 'fas fa-plus',
                'color': '#10b981'
            })
        
        # Add some system activities
        activities.insert(0, {
            'title': 'Dashboard Loaded',
            'description': f'Viewing {len(projects)} projects across {len(pm.list_categories())} categories',
            'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'icon': 'fas fa-tachometer-alt',
            'color': '#4f46e5'
        })
        
        return jsonify({'activities': activities[-10:]})  # Return last 10 activities
    except Exception as e:
        logging.error(f"Error getting recent activity: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500

@app.route('/USER_GUIDE.md')
def user_guide():
    try:
        return send_file('USER_GUIDE.md', as_attachment=False, mimetype='text/plain')
    except Exception as e:
        logging.error(f"Error serving user guide: {e}")
        return "User guide not found", 404

# Background deadline checker (runs periodically)
def check_deadlines_background():
    try:
        pm = get_project_manager()
        notification_system = get_notification_system()
        projects = pm.list_projects()
        notification_system.check_deadlines(projects)
    except Exception as e:
        logging.error(f"Error checking deadlines: {e}")
        # Send error notification
        try:
            notification_system = get_notification_system()
            notification_system.notify_system_error(
                "Deadline Check Error",
                str(e),
                datetime.now().isoformat()
            )
        except:
            pass

if __name__ == '__main__':
    print("🌐 Starting Project Management Web Interface with Auto-Reload")
    print("📊 Real-time data updates enabled!")
    print("🔄 The interface will automatically reload data when projects.json changes")
    print("🌍 Access at: http://localhost:8083")
    app.run(debug=True, host='0.0.0.0', port=8083)
