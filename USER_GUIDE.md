# Project Manager - Complete User Guide

A comprehensive guide to using the Project Management System with both CLI and Web interfaces.

## Table of Contents

1. [Getting Started](#getting-started)
2. [Web Interface Guide](#web-interface-guide)
3. [CLI Interface Guide](#cli-interface-guide)
4. [Project Management](#project-management)
5. [Stage & Task Management](#stage--task-management)
6. [Categories & Organization](#categories--organization)
7. [Templates](#templates)
8. [Batch Operations](#batch-operations)
9. [Data Management](#data-management)
10. [Automation & Scripts](#automation--scripts)
11. [Troubleshooting](#troubleshooting)

---

## Getting Started

### System Requirements
- Python 3.6 or higher
- Flask (for web interface)
- Modern web browser (for web interface)

### Quick Start
```bash
# Start the web interface (recommended)
python3 web_app.py

# Or use the CLI interface
python3 cli.py

# Run example demo
python3 example_usage.py
```

### First Time Setup
1. Clone or download the project files
2. Navigate to the project directory
3. Run `python3 web_app.py` to start the web interface
4. Open http://localhost:8083 in your browser
5. Start creating your first project!

---

## Web Interface Guide

### Accessing the Web Interface
1. Start the web server: `python3 web_app.py`
2. Open your browser to: http://localhost:8083
3. The interface loads with your project dashboard

### Main Dashboard
- **Project Cards**: Visual overview of all projects
- **Progress Bars**: Visual progress for each project
- **Category Filters**: Filter projects by category
- **Quick Actions**: Create, edit, delete projects
- **Batch Selection**: Select multiple projects for bulk operations

### Navigation Menu
- **Projects**: Main project listing (home page)
- **Categories**: Manage project categories
- **Templates**: Create and manage project templates
- **Summary**: Global statistics and project summaries

### Real-time Updates
- Changes save automatically
- No page refresh needed
- Updates appear instantly across all open browser windows
- File modification tracking ensures data consistency

---

## CLI Interface Guide

### Starting the CLI
```bash
python3 cli.py
```

### Basic Command Structure
```
pm> [command] [subcommand] [arguments]
```

### Essential Commands

#### Project Commands
```bash
# Create a new project
pm> create project "Website Redesign" "Complete company website overhaul"

# List all projects
pm> list projects

# Select a project to work with
pm> select project <project_id>

# Show current project details
pm> show project

# Delete a project
pm> delete project <project_id>

# Show detailed project progress
pm> project progress
```

#### Stage Commands
```bash
# Add a stage to current project
pm> add stage "Development" "Core development phase"

# List stages in current project
pm> list stages

# Show specific stage details
pm> show stage <stage_id>

# Advance to next stage
pm> next stage

# Complete current stage
pm> complete stage
```

#### Task Commands
```bash
# Add task to current stage
pm> add task "Design homepage" "Create responsive homepage design" "Alice"

# List tasks in current stage
pm> list tasks

# Complete a task
pm> complete task <task_id>

# Update task status
pm> update task <task_id> in_progress

# Show task details
pm> show task <task_id>
```

#### Navigation Commands
```bash
# Show current project and stage
pm> current

# Get help
pm> help

# Exit the program
pm> quit
```

---

## Project Management

### Creating Projects

#### Web Interface
1. Click "Create New Project" button
2. Fill in project details:
   - **Name**: Project title
   - **Description**: Detailed description
   - **Deadline**: Optional due date
   - **Category**: Select from existing categories
   - **Template**: Optional template to use
3. Click "Create Project"

#### CLI Interface
```bash
pm> create project "Project Name" "Project Description"
```

### Project Lifecycle

#### Default Stages
Every new project gets these stages automatically:
1. **Planning** - Define requirements and scope
2. **Development** - Core implementation work
3. **Testing** - Quality assurance and validation
4. **Deployment** - Release and launch activities
5. **Completion** - Final review and closure

#### Stage Progression
- Stages advance automatically when all tasks are completed
- Manual stage advancement available
- Can go back to previous stages if needed
- Visual progress tracking throughout

### Project Details
- **Progress**: Percentage completion based on completed tasks
- **Current Stage**: Which stage is currently active
- **Tasks**: Number of completed vs total tasks
- **Deadline**: Optional due date with countdown
- **Category**: Organization grouping
- **Creation Date**: When project was created

---

## Stage & Task Management

### Understanding Stages
Stages represent major phases of your project:
- Only one stage is active at a time
- Must complete all tasks in a stage to advance
- Can add custom stages beyond the defaults
- Each stage tracks its own progress

### Task Management

#### Task Statuses
- **todo**: Not started (default)
- **in_progress**: Currently being worked on
- **completed**: Finished successfully
- **blocked**: Cannot proceed due to dependencies

#### Adding Tasks
**Web Interface:**
1. Go to project detail page
2. Navigate to current stage
3. Click "Add Task"
4. Fill in task details
5. Assign to team member (optional)

**CLI Interface:**
```bash
pm> add task "Task Name" "Task Description" "Assignee"
```

#### Completing Tasks
**Web Interface:**
- Click the checkbox next to the task
- Or use the task dropdown menu

**CLI Interface:**
```bash
pm> complete task <task_id>
```

### Stage Advancement
When all tasks in a stage are completed:
1. Current stage is marked as completed
2. Next stage automatically begins
3. Team members can start working on new stage tasks
4. Progress bars update to reflect advancement

---

## Categories & Organization

### Purpose of Categories
- Group related projects together
- Visual organization with custom colors
- Filter projects by type or department
- Better project discovery and management

### Creating Categories

#### Web Interface
1. Go to "Categories" page
2. Click "Create New Category"
3. Enter details:
   - **Name**: Category title
   - **Description**: What this category contains
   - **Color**: Visual identifier (hex color)
4. Click "Create Category"

#### Available Category Colors
- Development: Green (#28a745)
- Design: Blue (#007bff)
- Marketing: Purple (#6f42c1)
- Research: Orange (#fd7e14)
- Custom: Any hex color

### Assigning Projects to Categories

#### Web Interface
1. Go to project detail page
2. Select category from dropdown
3. Changes save automatically

#### CLI Interface
Categories are managed through the web interface for better visual organization.

### Category Management
- **Edit Categories**: Update name, description, or color
- **Delete Categories**: Remove unused categories
- **Default Category**: Set a default for new projects
- **Project Count**: See how many projects are in each category

---

## Templates

### What are Templates?
Templates are pre-defined project structures with:
- Standard stages for specific project types
- Common tasks within each stage
- Best practices for different workflows
- Time-saving project creation

### Default Templates
The system includes several built-in templates:
1. **Software Development**: Full development lifecycle
2. **Marketing Campaign**: Campaign planning and execution
3. **Research Project**: Academic or business research
4. **Product Launch**: Product development and release
5. **Event Planning**: Event organization and management

### Creating Custom Templates

#### Web Interface
1. Go to "Templates" page
2. Click "Create New Template"
3. Define template structure:
   - **Name**: Template title
   - **Description**: When to use this template
   - **Stages**: Define each stage and its tasks
4. Save template for future use

### Using Templates
When creating a new project:
1. Select "Use Template" option
2. Choose from available templates
3. Project is created with pre-defined stages and tasks
4. Customize as needed for specific project

### Template Benefits
- **Consistency**: Standardized project structures
- **Speed**: Faster project creation
- **Best Practices**: Proven workflows
- **Team Alignment**: Everyone follows same process

---

## Batch Operations

### What are Batch Operations?
Batch operations allow you to:
- Select multiple projects at once
- Perform actions on all selected projects
- Save time with bulk operations
- Maintain consistency across projects

### Available Batch Operations

#### Batch Delete
1. Select projects using checkboxes
2. Click "Delete Selected" button
3. Confirm deletion in dialog
4. All selected projects are removed

#### Batch Move to Category
1. Select projects using checkboxes
2. Choose "Move to Category" action
3. Select target category from dropdown
4. All projects are moved to the category

#### Batch Remove from Category
1. Select projects with categories assigned
2. Choose "Remove Category" action
3. Projects are moved to "Uncategorized"

### Using Batch Operations

#### Web Interface
1. **Individual Selection**: Click checkboxes next to project names
2. **Select All**: Use the master checkbox to select all visible projects
3. **Action Bar**: Appears when projects are selected
4. **Confirmation**: All batch operations require confirmation

#### Selection Features
- **Visual Feedback**: Selected projects are highlighted
- **Counter**: Shows number of selected projects
- **Clear Selection**: Button to deselect all projects
- **Persistent Selection**: Selection maintained during page interactions

### Batch Operation Safety
- **Confirmation Dialogs**: Prevent accidental operations
- **Reversible Operations**: Category moves can be undone
- **Error Handling**: Partial failures are reported
- **Audit Trail**: Operations are logged for tracking

---

## Data Management

### Data Storage
- **File Format**: JSON for human-readable data
- **Location**: `projects.json` in project directory
- **Backup**: Automatic backup on each save
- **Portability**: Easy to copy and transfer

### Automatic Saving
- **Real-time**: Changes save immediately
- **No Data Loss**: Automatic persistence
- **Conflict Resolution**: Handles multiple access gracefully
- **File Monitoring**: Detects external changes

### Import/Export

#### Export Options
**Web Interface API Endpoints:**
```bash
# Export all projects
curl http://localhost:8083/api/export/projects

# Export all templates
curl http://localhost:8083/api/export/templates

# Export everything
curl http://localhost:8083/api/export/all
```

#### Import Process
1. Prepare JSON data in correct format
2. Use API endpoints to import data
3. System validates and merges data
4. Conflicts are resolved automatically

### Data Backup Strategy
1. **Regular Exports**: Use API to export data regularly
2. **File Backups**: Copy `projects.json` file
3. **Version Control**: Use git to track changes
4. **Cloud Storage**: Store backups in cloud services

---

## Automation & Scripts

### Automation Demo
```bash
python3 automation_demo.py
```
Demonstrates:
- Programmatic project creation
- Automatic task completion
- Stage advancement
- Real-time web updates

### Batch Operations Demo
```bash
python3 batch_operations_demo.py
```
Shows:
- Bulk project creation
- Category assignment
- Batch deletion
- Web interface integration

### Auto-Commit Script
```bash
./auto_commit.sh
```
Features:
- Automatic git commits
- Timestamped messages
- Secure SSH authentication
- Push to GitHub

### Custom Automation
Create your own automation scripts:

```python
from project_manager import ProjectManager

# Initialize
pm = ProjectManager()

# Create projects programmatically
project = pm.create_project("Automated Project", "Created by script")

# Complete tasks automatically
current_stage = project.get_current_stage()
for task in current_stage.tasks:
    task.complete()

# Save changes
pm.save_data()
```

---

## API Reference

### Project Management API

#### Get All Projects
```bash
GET /api/projects
```

#### Create Project
```bash
POST /api/create_project
{
  "name": "Project Name",
  "description": "Project Description",
  "deadline": "2024-12-31",
  "category_id": "category-uuid"
}
```

#### Update Project
```bash
POST /api/project/<project_id>/update
{
  "name": "New Name",
  "description": "New Description"
}
```

#### Delete Project
```bash
DELETE /api/project/<project_id>/delete
```

### Task Management API

#### Add Task
```bash
POST /api/project/<project_id>/add_task
{
  "name": "Task Name",
  "description": "Task Description",
  "assignee": "Person Name"
}
```

#### Complete Task
```bash
POST /api/task/<task_id>/complete
```

#### Update Task Status
```bash
POST /api/task/<task_id>/update
{
  "status": "in_progress"
}
```

### Category Management API

#### Get All Categories
```bash
GET /api/categories
```

#### Create Category
```bash
POST /api/categories
{
  "name": "Category Name",
  "description": "Category Description",
  "color": "#007bff"
}
```

#### Assign Project to Category
```bash
POST /api/project/<project_id>/assign_category
{
  "category_id": "category-uuid"
}
```

### Batch Operations API

#### Batch Delete Projects
```bash
POST /api/projects/batch_delete
{
  "project_ids": ["id1", "id2", "id3"]
}
```

#### Batch Move to Category
```bash
POST /api/projects/batch_move_category
{
  "project_ids": ["id1", "id2", "id3"],
  "category_id": "category-uuid"
}
```

---

## Troubleshooting

### Common Issues

#### Web Interface Won't Start
**Problem**: Error when running `python3 web_app.py`
**Solution**:
1. Check Python version: `python3 --version`
2. Install Flask: `pip3 install flask`
3. Check port availability: `lsof -i :8083`

#### Data Not Saving
**Problem**: Changes don't persist after restart
**Solution**:
1. Check file permissions on `projects.json`
2. Ensure directory is writable
3. Look for error messages in console

#### Browser Shows "Error Loading Page"
**Problem**: Web interface displays error
**Solution**:
1. Check web server is running
2. Verify URL: http://localhost:8083
3. Check console for error messages
4. Restart web server

#### CLI Commands Not Working
**Problem**: Commands not recognized in CLI
**Solution**:
1. Check command syntax: `help`
2. Ensure project is selected: `current`
3. Use exact command format from help

### Performance Issues

#### Slow Web Interface
**Causes & Solutions**:
- **Too many projects**: Use category filters
- **Large project files**: Consider archiving completed projects
- **Browser cache**: Clear cache and reload

#### Memory Usage
**Optimization**:
- Archive old projects
- Use templates instead of duplicating projects
- Regular cleanup of completed projects

### Data Recovery

#### Corrupted Data File
1. Check for backup files (`projects.json.bak`)
2. Restore from version control if available
3. Use API export from working instance
4. Manually recreate critical projects

#### Lost Projects
1. Check if projects are filtered by category
2. Look in different project statuses
3. Check browser cache for unsaved changes
4. Restore from recent backup

---

## Best Practices

### Project Organization
1. **Use Categories**: Group related projects
2. **Descriptive Names**: Clear, searchable project names
3. **Regular Updates**: Keep project status current
4. **Archive Completed**: Move finished projects to archive

### Task Management
1. **Specific Tasks**: Break down work into actionable items
2. **Clear Assignments**: Assign tasks to specific people
3. **Regular Reviews**: Check task status frequently
4. **Update Status**: Keep task statuses current

### Data Management
1. **Regular Backups**: Export data regularly
2. **Version Control**: Use git for change tracking
3. **Clean Data**: Remove unnecessary test projects
4. **Document Changes**: Use meaningful commit messages

### Team Collaboration
1. **Shared Categories**: Use consistent category structure
2. **Template Standards**: Create organization-specific templates
3. **Status Updates**: Regular project status meetings
4. **Access Control**: Manage who can modify projects

---

## Advanced Features

### Custom Stage Workflows
Create specialized workflows for different project types:
- **Agile Development**: Sprint-based stages
- **Research Projects**: Hypothesis, experiment, analysis stages
- **Marketing Campaigns**: Planning, execution, analysis stages

### Integration Possibilities
The system can be extended to integrate with:
- **Slack**: Task completion notifications
- **Email**: Deadline reminders
- **Calendar**: Project milestone tracking
- **Time Tracking**: Work hour logging

### Automation Scripts
Develop custom scripts for:
- **Automatic Status Updates**: Based on external triggers
- **Report Generation**: Weekly progress reports
- **Data Synchronization**: With other project management tools
- **Deadline Monitoring**: Automated alerts for overdue projects

---

## Support and Resources

### Getting Help
1. **Built-in Help**: Use `help` command in CLI
2. **Documentation**: Refer to this guide
3. **Demo Scripts**: Run example demonstrations
4. **Code Comments**: Check source code for details

### Extending the System
- **Custom Fields**: Add project-specific data fields
- **New Task Types**: Extend task status options
- **Integration APIs**: Connect with external services
- **Custom Reports**: Generate specific analytics

### Community
- **GitHub Repository**: Source code and issues
- **Feature Requests**: Suggest improvements
- **Bug Reports**: Report problems encountered
- **Contributions**: Submit code improvements

---

This comprehensive guide covers all aspects of using the Project Management System. For specific questions or advanced use cases, refer to the source code or create custom automation scripts using the provided APIs and examples.