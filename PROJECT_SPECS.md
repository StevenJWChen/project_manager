# Project Management System - Complete Specifications

## Overview
A comprehensive web-based project management system built with Flask and Bootstrap, featuring project templates, categories, stage management, task tracking, and comprehensive reporting.

## Architecture

### Backend (Python/Flask)
- **Framework**: Flask with Jinja2 templating
- **Data Storage**: JSON files for persistence
- **Structure**: MVC pattern with separate business logic layer

### Frontend
- **Framework**: Bootstrap 5.1.3 for responsive UI
- **Icons**: Font Awesome 6.0.0
- **JavaScript**: Vanilla JS for dynamic functionality
- **Styling**: Custom CSS with Bootstrap theming

## Core Data Models

### Project
```python
class Project:
    id: str (UUID)
    name: str
    description: str
    stages: List[Stage]
    deadline: str (ISO date)
    created_at: str (ISO datetime)
    category_id: str (optional)
    current_stage_index: int
    
    Methods:
    - get_overall_progress() -> float
    - get_current_stage() -> Stage
    - advance_to_next_stage() -> (bool, str)
    - go_back_to_previous_stage() -> (bool, str)
    - is_completed() -> bool
    - is_overdue() -> bool
    - days_until_deadline() -> int
```

### Stage
```python
class Stage:
    id: str (UUID)
    name: str
    description: str
    tasks: List[Task]
    status: StageStatus (PENDING, IN_PROGRESS, COMPLETED)
    
    Methods:
    - get_progress() -> float
    - add_task(task: Task)
    - remove_task(task_id: str) -> bool
    - is_completed() -> bool
```

### Task
```python
class Task:
    id: str (UUID)
    name: str
    description: str
    assignee: str
    status: TaskStatus (PENDING, IN_PROGRESS, COMPLETED)
    created_at: str (ISO datetime)
    completed_at: str (ISO datetime, optional)
    
    Methods:
    - complete()
    - is_completed() -> bool
```

### Category
```python
class Category:
    id: str (UUID)
    name: str
    description: str
    color: str (hex color)
    
    Methods:
    - to_dict() -> dict
```

### Template
```python
class Template:
    id: str (UUID)
    name: str
    description: str
    stages: List[dict] (stage definitions with tasks)
    is_default: bool
    
    Structure:
    {
        "id": "template_id",
        "name": "Template Name",
        "description": "Template description",
        "stages": [
            {
                "name": "Stage Name",
                "description": "Stage description",
                "tasks": [
                    {
                        "name": "Task Name",
                        "description": "Task description"
                    }
                ]
            }
        ]
    }
```

## File Structure
```
/
├── web_app.py                 # Flask application and routes
├── project_manager.py         # Core business logic and data models
├── projects.json             # Project data persistence
├── categories.json           # Category data persistence
├── templates.json            # Template data persistence
├── static/
│   ├── css/
│   │   └── style.css         # Custom styles
│   └── js/
│       └── app.js            # Shared JavaScript utilities
└── templates/
    ├── base.html             # Base template with navigation
    ├── index.html            # Dashboard/project listing
    ├── summary.html          # Project summary and statistics
    ├── categories.html       # Category management
    ├── category_detail.html  # Category detail view
    ├── templates.html        # Template management
    └── project_detail.html   # Project detail and task management
```

## Web Routes

### Page Routes
- `GET /` - Dashboard with project cards and filters
- `GET /summary` - Summary page with statistics and sortable project table
- `GET /categories` - Category management page
- `GET /category/<category_id>` - Category detail with projects
- `GET /templates` - Template management page
- `GET /project/<project_id>` - Project detail page

### API Routes

#### Projects
- `GET /api/projects` - List all projects
- `GET /api/project/<project_id>` - Get project details
- `POST /api/create_project` - Create new project (with optional template)
- `POST /api/project/<project_id>/update` - Update project details
- `POST /api/project/<project_id>/add_task` - Add task to current stage
- `POST /api/project/<project_id>/next_stage` - Advance to next stage
- `POST /api/project/<project_id>/previous_stage` - Go back to previous stage
- `POST /api/project/<project_id>/assign_category` - Assign project to category

#### Tasks
- `POST /api/task/<task_id>/complete` - Mark task as completed
- `POST /api/task/<task_id>/update` - Update task status

#### Categories
- `GET /api/categories` - List all categories
- `POST /api/categories` - Create new category
- `DELETE /api/category/<category_id>` - Delete category
- `GET /api/default_category` - Get default category
- `POST /api/default_category` - Set default category

#### Templates
- `GET /api/templates` - List all templates
- `POST /api/templates` - Create new template
- `GET /api/template/<template_id>` - Get template details  
- `PUT /api/template/<template_id>` - Update template
- `DELETE /api/template/<template_id>` - Delete template

#### Statistics
- `GET /api/summary` - Get global project statistics

## Features

### Dashboard (index.html)
- **Project Cards**: Visual cards showing project progress, status, deadlines
- **Search & Filtering**: Real-time search by name/description
- **Status Filtering**: Filter by active, completed, overdue
- **Category Filtering**: Filter by project category
- **Sorting**: Sort by name, progress, deadline, creation date
- **Project Creation Modal**: Create projects with template selection

### Summary Page (summary.html)
- **Global Statistics**: Total projects, active/completed counts, overall progress
- **Progress Overview**: Visual progress bars for stages and tasks
- **Project Breakdown Table**: Sortable table with all project details
- **Clickable Column Headers**: Sort by clicking column headers
- **Sort Options**: Name, Category, Progress, Stages, Tasks, Status, Deadline, Creation Date
- **Auto-refresh**: Statistics update every 30 seconds

### Category Management (categories.html)
- **Category CRUD**: Create, read, update, delete categories
- **Color Coding**: Assign colors to categories
- **Default Category**: Set and manage default category
- **Project Assignment**: Assign projects to categories

### Template Management (templates.html)
- **Template Creation**: Create reusable project templates
- **Stage & Task Definition**: Define stages with associated tasks
- **Template Preview**: View template structure before use
- **Default Templates**: Built-in templates (Standard, Agile, Simple)
- **Template Usage**: Select templates when creating projects

### Project Detail (project_detail.html)
- **Stage Management**: View and navigate between project stages
- **Task Management**: Add, complete, update tasks within stages
- **Progress Tracking**: Visual progress indicators
- **Stage Navigation**: Move forward/backward between stages
- **Real-time Updates**: Dynamic UI updates without page refresh

## Default Templates

### Standard Software Development
```json
{
    "stages": [
        {
            "name": "Planning",
            "tasks": ["Define requirements", "Create project plan", "Set up development environment"]
        },
        {
            "name": "Design",
            "tasks": ["Create system architecture", "Design user interface", "Database design"]
        },
        {
            "name": "Development",
            "tasks": ["Implement core features", "Write unit tests", "Code review"]
        },
        {
            "name": "Testing",
            "tasks": ["Integration testing", "User acceptance testing", "Bug fixes"]
        },
        {
            "name": "Deployment",
            "tasks": ["Production deployment", "Documentation", "User training"]
        }
    ]
}
```

### Agile Development
```json
{
    "stages": [
        {
            "name": "Sprint Planning",
            "tasks": ["Define user stories", "Estimate story points", "Sprint backlog creation"]
        },
        {
            "name": "Development Sprint",
            "tasks": ["Daily standups", "Feature development", "Code reviews"]
        },
        {
            "name": "Sprint Review",
            "tasks": ["Demo to stakeholders", "Gather feedback", "Update product backlog"]
        },
        {
            "name": "Sprint Retrospective",
            "tasks": ["Identify improvements", "Action items", "Process refinement"]
        }
    ]
}
```

### Simple Project
```json
{
    "stages": [
        {
            "name": "Start",
            "tasks": ["Project kickoff", "Initial setup"]
        },
        {
            "name": "Work",
            "tasks": ["Main work", "Progress review"]
        },
        {
            "name": "Finish",
            "tasks": ["Final review", "Project completion"]
        }
    ]
}
```

## UI Components

### Sorting & Filtering
- **Real-time Search**: Instant filtering as user types
- **Multi-criteria Filtering**: Combine search, status, and category filters
- **Clickable Headers**: Sort by clicking table column headers
- **Sort Direction Indicators**: Visual icons showing sort direction
- **Dropdown Sorting**: Alternative sorting via dropdown menus

### Visual Indicators
- **Progress Bars**: Show completion percentage
- **Status Badges**: Color-coded status indicators
- **Deadline Warnings**: Visual alerts for overdue/due soon projects
- **Category Tags**: Colored badges for project categories

### Responsive Design
- **Mobile-friendly**: Bootstrap responsive grid system
- **Touch-friendly**: Appropriate touch targets
- **Adaptive Layout**: Adjusts to different screen sizes

## Data Persistence
- **JSON Storage**: All data stored in JSON files
- **Atomic Updates**: Data consistency during updates
- **Backup Strategy**: Manual backup of JSON files
- **Data Validation**: Input validation before persistence

## Error Handling
- **User-friendly Messages**: Clear error messages for users
- **Logging**: Comprehensive server-side logging
- **Graceful Degradation**: Fallback behavior for failed operations
- **Input Validation**: Both client and server-side validation

## Performance Features
- **Client-side Filtering**: Instant search and filter responses
- **Minimal API Calls**: Efficient data loading strategies
- **Progressive Enhancement**: Core functionality works without JavaScript
- **Caching**: Browser caching for static assets

## Security Considerations
- **Input Sanitization**: Prevent XSS attacks
- **Data Validation**: Server-side validation of all inputs
- **No Authentication**: Simple single-user system (can be extended)

## Browser Compatibility
- **Modern Browsers**: Chrome, Firefox, Safari, Edge
- **ES6+ Features**: Modern JavaScript features
- **CSS3**: Advanced styling features
- **Progressive Enhancement**: Graceful degradation for older browsers

## Deployment
- **Development Server**: Flask built-in development server
- **Port**: Default port 8084
- **Host**: 0.0.0.0 (accessible from network)
- **Debug Mode**: Enabled for development

## Extension Points
- **Authentication**: Can add user management
- **Database**: Can migrate from JSON to SQL database
- **Real-time Updates**: Can add WebSocket support  
- **File Attachments**: Can add file upload capabilities
- **Notifications**: Can add email/push notifications
- **API Documentation**: Can add Swagger/OpenAPI docs
- **Testing**: Can add comprehensive test suite

## Key Implementation Details

### Template-based Project Creation
- Templates define reusable project structures
- Projects created from templates inherit all stages and tasks
- Template system supports custom and default templates

### Advanced Sorting System
- Multiple sort criteria supported
- Clickable column headers with visual feedback
- Persistent sort state during user interactions
- Handles mixed data types (strings, numbers, dates)

### Real-time Progress Calculation
- Progress calculated dynamically based on task completion
- Stage completion triggers automatic stage advancement
- Overall project progress aggregates all stage progress

### Category System
- Flexible categorization with color coding
- Default category support for uncategorized projects
- Category-based filtering and organization

This specification provides a complete blueprint for recreating the entire project management system, including all features, data models, API endpoints, and UI components implemented during development.