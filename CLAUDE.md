# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a comprehensive project management system built in Python with both CLI and web interfaces. It manages projects through stages with tasks, includes category organization, deadline tracking, and progress monitoring.

## Common Development Commands

### Running the Application
```bash
# CLI interface
python3 cli.py

# Web interface (Flask app on port 8083)
python3 web_app.py

# Alternative web interface (port 8082)  
python3 start_web.py

# Demo/example usage
python3 example_usage.py
```

### Testing
```bash
# Test core enhancements
python3 test_enhancements.py

# Test all enhanced features
python3 test_all_enhancements.py

# Test completion logic specifically
python3 fix_completion_test.py
```

### Data Storage
- All project data is stored in `projects.json` in the root directory
- Data is automatically saved when changes are made through the ProjectManager class

## Architecture Overview

### Core Classes (project_manager.py)

1. **ProjectManager**: Main controller class that manages all projects, categories, and data persistence
   - Handles CRUD operations for projects and categories
   - Manages data loading/saving from JSON
   - Provides global summary statistics

2. **Project**: Represents a complete project with multiple stages
   - Contains stages, metadata (name, description, deadline, category)
   - Handles stage advancement and completion logic
   - Tracks overall project progress

3. **Stage**: Represents a phase within a project
   - Contains tasks and manages stage-level completion
   - Default stages: Planning, Design, Development, Testing, Deployment, Launch
   - Each stage can have default tasks automatically created

4. **Task**: Individual work items within stages
   - Has status (todo, in_progress, completed, blocked)
   - Includes assignee and description fields

5. **Category**: Organizational grouping for projects
   - Includes name, description, and color coding
   - Projects can be assigned to categories

### Default Stage Configuration
The system creates 6 default stages with pre-defined tasks:
- **Planning**: Define requirements, Create timeline, Assign resources
- **Design**: Create wireframes, Design mockups, Review design  
- **Development**: Set up environment, Implement features, Code review
- **Testing**: Write test cases, Execute tests, Fix bugs
- **Deployment**: Deploy to staging, User acceptance testing, Deploy to production
- **Launch**: Monitor launch, Gather feedback, Create documentation

### Interfaces

1. **CLI Interface** (cli.py): Interactive command-line interface with colored output
2. **Web Interface** (web_app.py): Flask-based web application with HTML templates
3. **Demo Scripts**: Various test and example scripts

### Key Features

- Multi-stage project workflow with automatic progression
- Task management within stages
- Category-based project organization
- Deadline tracking with overdue detection
- Progress monitoring at task, stage, and project levels
- Data persistence with automatic JSON serialization
- Web dashboard with project details and summary views

### Template System
- HTML templates stored in `templates/` directory
- Static assets (CSS/JS) in `static/` directory
- Responsive web interface with Bootstrap styling

### Status Management
- **TaskStatus**: todo, in_progress, completed, blocked
- **StageStatus**: not_started, in_progress, completed
- Projects are considered complete when all stages are completed

## Development Notes

- The system uses UUID4 for all entity IDs
- All timestamps use ISO format strings
- The web interface supports both basic dashboard view and detailed project management
- Stage advancement is automatic when all tasks in current stage are completed
- Projects can be assigned to categories for better organization
- Deadline functionality includes overdue detection and days-until-deadline calculation