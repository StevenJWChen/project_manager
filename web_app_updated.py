#!/usr/bin/env python3
"""
Web interface for Project Management System
With automatic data reloading for real-time updates
"""
from flask import Flask, render_template, jsonify, request, redirect, url_for
from project_manager import ProjectManager, Task, TaskStatus, StageStatus
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
def index():
    try:
        pm = get_project_manager()  # Get fresh data
        projects = pm.list_projects()
        categories = pm.list_categories()
        logging.info(f"Index page: {len(projects)} projects, {len(categories)} categories")
        return render_template('index.html', projects=projects, categories=categories)
    except Exception as e:
        logging.error(f"Error rendering index page: {e}")
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
        projects = [p for p in pm.list_projects() if p.category_id == category_id]
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

@app.route('/api/global_summary')
def api_global_summary():
    try:
        pm = get_project_manager()  # Get fresh data
        return jsonify(pm.get_global_summary())
    except Exception as e:
        logging.error(f"Error in API /api/global_summary: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500

@app.route('/api/categories')
def api_categories():
    try:
        pm = get_project_manager()  # Get fresh data
        categories = pm.list_categories()
        return jsonify([c.to_dict() for c in categories])
    except Exception as e:
        logging.error(f"Error in API /api/categories: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500

# Add a simple health check endpoint
@app.route('/api/health')
def api_health():
    try:
        pm = get_project_manager()
        return jsonify({
            'status': 'healthy',
            'data_file': _data_file,
            'last_reload': _last_file_mtime,
            'projects_count': len(pm.list_projects()),
            'categories_count': len(pm.list_categories())
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    print("🌐 Starting Project Management Web Interface with Auto-Reload")
    print("📊 Real-time data updates enabled!")
    print("🔄 The interface will automatically reload data when projects.json changes")
    print("🌍 Access at: http://localhost:8083")
    
    app.run(debug=True, host='0.0.0.0', port=8083)