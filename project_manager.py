#!/usr/bin/env python3
import json
import os
from datetime import datetime
from enum import Enum
from typing import List, Dict, Optional
import uuid


class TaskStatus(Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    BLOCKED = "blocked"


class StageStatus(Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class Category:
    def __init__(self, name: str, description: str = "", color: str = "#007bff"):
        self.id = str(uuid.uuid4())
        self.name = name
        self.description = description
        self.color = color
        self.created_at = datetime.now().isoformat()

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'color': self.color,
            'created_at': self.created_at
        }

    @classmethod
    def from_dict(cls, data):
        category = cls(data['name'], data.get('description', ''), data.get('color', '#007bff'))
        category.id = data['id']
        category.created_at = data['created_at']
        return category


class Task:
    def __init__(self, name: str, description: str = "", assignee: str = ""):
        self.id = str(uuid.uuid4())
        self.name = name
        self.description = description
        self.assignee = assignee
        self.status = TaskStatus.TODO
        self.created_at = datetime.now().isoformat()
        self.completed_at = None

    def complete(self):
        self.status = TaskStatus.COMPLETED
        self.completed_at = datetime.now().isoformat()

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'assignee': self.assignee,
            'status': self.status.value,
            'created_at': self.created_at,
            'completed_at': self.completed_at
        }

    @classmethod
    def from_dict(cls, data):
        task = cls(data['name'], data['description'], data['assignee'])
        task.id = data['id']
        task.status = TaskStatus(data['status'])
        task.created_at = data['created_at']
        task.completed_at = data['completed_at']
        return task


class Stage:
    def __init__(self, name: str, description: str = "", default_tasks: List[str] = None):
        self.id = str(uuid.uuid4())
        self.name = name
        self.description = description
        self.status = StageStatus.NOT_STARTED
        self.tasks: List[Task] = []
        self.created_at = datetime.now().isoformat()
        self.started_at = None
        self.completed_at = None
        
        if default_tasks:
            for task_name in default_tasks:
                default_task = Task(task_name, f"Default task for {name} stage")
                self.tasks.append(default_task)

    def add_task(self, task: Task):
        self.tasks.append(task)
        if self.status == StageStatus.NOT_STARTED:
            self.start()

    def start(self):
        if self.status == StageStatus.NOT_STARTED:
            self.status = StageStatus.IN_PROGRESS
            self.started_at = datetime.now().isoformat()

    def complete(self):
        incomplete_tasks = [t for t in self.tasks if t.status != TaskStatus.COMPLETED]
        if incomplete_tasks:
            return False, f"Cannot complete stage: {len(incomplete_tasks)} tasks incomplete"
        
        self.status = StageStatus.COMPLETED
        self.completed_at = datetime.now().isoformat()
        return True, "Stage completed successfully"

    def get_progress(self):
        if not self.tasks:
            return 1.0 if self.status == StageStatus.COMPLETED else 0.0
        completed = sum(1 for task in self.tasks if task.status == TaskStatus.COMPLETED)
        return completed / len(self.tasks)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'status': self.status.value,
            'tasks': [task.to_dict() for task in self.tasks],
            'created_at': self.created_at,
            'started_at': self.started_at,
            'completed_at': self.completed_at
        }

    @classmethod
    def from_dict(cls, data):
        stage = cls(data['name'], data['description'])
        stage.id = data['id']
        stage.status = StageStatus(data['status'])
        stage.tasks = [Task.from_dict(task_data) for task_data in data['tasks']]
        stage.created_at = data['created_at']
        stage.started_at = data['started_at']
        stage.completed_at = data['completed_at']
        return stage


class Project:
    def __init__(self, name: str, description: str = "", deadline: str = None, category_id: str = None):
        self.id = str(uuid.uuid4())
        self.name = name
        self.description = description
        self.deadline = deadline
        self.category_id = category_id
        self.stages: List[Stage] = []
        self.created_at = datetime.now().isoformat()
        self.completed_at = None

    def add_stage(self, stage: Stage):
        self.stages.append(stage)

    def get_current_stage(self) -> Optional[Stage]:
        for stage in self.stages:
            if stage.status == StageStatus.IN_PROGRESS:
                return stage
        for stage in self.stages:
            if stage.status == StageStatus.NOT_STARTED:
                return stage
        return None

    def advance_to_next_stage(self) -> tuple[bool, str]:
        current_stage = self.get_current_stage()
        if not current_stage:
            return False, "No active stage to advance from."

        success, message = current_stage.complete()
        if not success:
            return False, message

        current_index = self.stages.index(current_stage)
        if current_index + 1 < len(self.stages):
            next_stage = self.stages[current_index + 1]
            next_stage.start()
            return True, f"Advanced to stage: {next_stage.name}"
        else:
            self.completed_at = datetime.now().isoformat()
            return True, "Project completed!"

    def go_back_to_previous_stage(self) -> tuple[bool, str]:
        current_stage = self.get_current_stage()
        if not current_stage:
            if all(s.status == StageStatus.COMPLETED for s in self.stages):
                last_stage = self.stages[-1]
                last_stage.status = StageStatus.IN_PROGRESS
                last_stage.completed_at = None
                self.completed_at = None
                return True, f"Moved back to stage: {last_stage.name}"
            return False, "No active stage to go back from."

        current_index = self.stages.index(current_stage)
        if current_index == 0:
            return False, "Already at the first stage."

        current_stage.status = StageStatus.NOT_STARTED
        current_stage.started_at = None
        
        previous_stage = self.stages[current_index - 1]
        previous_stage.status = StageStatus.IN_PROGRESS
        previous_stage.completed_at = None
        
        if self.completed_at:
            self.completed_at = None
        
        return True, f"Moved back to stage: {previous_stage.name}"

    def is_overdue(self) -> bool:
        if not self.deadline:
            return False
        try:
            deadline_date = datetime.fromisoformat(self.deadline.replace('Z', '+00:00'))
            return datetime.now(deadline_date.tzinfo) > deadline_date and not self.is_completed()
        except (ValueError, TypeError):
            return False

    def days_until_deadline(self) -> Optional[int]:
        if not self.deadline:
            return None
        try:
            deadline_date = datetime.fromisoformat(self.deadline.replace('Z', '+00:00'))
            delta = deadline_date - datetime.now(deadline_date.tzinfo)
            return delta.days
        except (ValueError, TypeError):
            return None

    def get_project_summary(self) -> Dict:
        total_tasks = sum(len(stage.tasks) for stage in self.stages)
        completed_tasks = sum(1 for stage in self.stages for t in stage.tasks if t.status == TaskStatus.COMPLETED)
        
        current_stage_obj = self.get_current_stage()
        current_stage_name = current_stage_obj.name if current_stage_obj else ("Completed" if self.is_completed() else "Not Started")

        return {
            'total_stages': len(self.stages),
            'completed_stages': len([s for s in self.stages if s.status == StageStatus.COMPLETED]),
            'total_tasks': total_tasks,
            'completed_tasks': completed_tasks,
            'overall_progress': self.get_overall_progress(),
            'is_completed': self.is_completed(),
            'current_stage': current_stage_name,
            'deadline': self.deadline,
            'is_overdue': self.is_overdue(),
            'days_until_deadline': self.days_until_deadline(),
            'category_id': self.category_id
        }

    def get_overall_progress(self):
        if not self.stages:
            return 1.0 if self.is_completed() else 0.0
        
        total_progress = sum(stage.get_progress() for stage in self.stages)
        return total_progress / len(self.stages)

    def is_completed(self):
        stages_completed = all(stage.status == StageStatus.COMPLETED for stage in self.stages)
        if stages_completed and not self.completed_at:
            self.completed_at = datetime.now().isoformat()
        elif not stages_completed and self.completed_at:
            self.completed_at = None
        return stages_completed

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'deadline': self.deadline,
            'category_id': self.category_id,
            'stages': [stage.to_dict() for stage in self.stages],
            'created_at': self.created_at,
            'completed_at': self.completed_at
        }

    @classmethod
    def from_dict(cls, data):
        project = cls(
            data['name'], 
            data.get('description', ''), 
            data.get('deadline'), 
            data.get('category_id')
        )
        project.id = data['id']
        project.stages = [Stage.from_dict(stage_data) for stage_data in data.get('stages', [])]
        project.created_at = data.get('created_at')
        project.completed_at = data.get('completed_at')
        return project


class ProjectManager:
    def __init__(self, data_file: str = "projects.json"):
        self.data_file = data_file
        self.projects: Dict[str, Project] = {}
        self.categories: Dict[str, Category] = {}
        self.templates: Dict[str, Dict] = {}
        self.default_category_id: Optional[str] = None
        self.metadata: Dict = {}
        self.default_stage_tasks = {
            "Planning": ["Define requirements", "Create timeline", "Assign resources"],
            "Design": ["Create wireframes", "Design mockups", "Review design"],
            "Development": ["Set up environment", "Implement features", "Code review"],
            "Testing": ["Write test cases", "Execute tests", "Fix bugs"],
            "Deployment": ["Deploy to staging", "User acceptance testing", "Deploy to production"],
            "Launch": ["Monitor launch", "Gather feedback", "Create documentation"]
        }
        self.load_data()
        self._ensure_default_category()

    def create_project(self, name: str, description: str = "", stage_names: List[str] = None, 
                      deadline: str = None, category_id: str = None) -> Project:
        category_id = category_id if category_id is not None else self.default_category_id
        project = Project(name, description, deadline, category_id)
        
        stages_to_create = stage_names if stage_names else list(self.default_stage_tasks.keys())
        for stage_name in stages_to_create:
            default_tasks = self.default_stage_tasks.get(stage_name, [])
            stage = Stage(stage_name, f"Stage for {stage_name}", default_tasks=default_tasks)
            project.add_stage(stage)
        
        # Start the first stage automatically
        if project.stages:
            project.stages[0].start()

        self.projects[project.id] = project
        self.save_data()
        return project

    def get_project(self, project_id: str) -> Optional[Project]:
        return self.projects.get(project_id)

    def list_projects(self) -> List[Project]:
        return sorted(list(self.projects.values()), key=lambda p: p.created_at, reverse=True)
    
    def delete_project(self, project_id: str) -> bool:
        if project_id in self.projects:
            del self.projects[project_id]
            self.save_data()
            return True
        return False

    def create_category(self, name: str, description: str = "", color: str = "#007bff") -> Category:
        category = Category(name, description, color)
        self.categories[category.id] = category
        self.save_data()
        return category

    def get_category(self, category_id: str) -> Optional[Category]:
        return self.categories.get(category_id)

    def list_categories(self) -> List[Category]:
        return sorted(list(self.categories.values()), key=lambda c: c.name)

    def delete_category(self, category_id: str) -> bool:
        if category_id in self.categories:
            for project in self.projects.values():
                if project.category_id == category_id:
                    project.category_id = self.default_category_id if self.default_category_id != category_id else None
            
            del self.categories[category_id]
            
            if self.default_category_id == category_id:
                self.default_category_id = None
                self._ensure_default_category()

            self.save_data()
            return True
        return False

    def assign_project_to_category(self, project_id: str, category_id: Optional[str]) -> bool:
        project = self.get_project(project_id)
        if project and (category_id is None or self.get_category(category_id)):
            project.category_id = category_id
            self.save_data()
            return True
        return False

    def set_default_category(self, category_id: Optional[str]) -> bool:
        if category_id is None or self.get_category(category_id):
            self.default_category_id = category_id
            self.save_data()
            return True
        return False

    def get_default_category(self) -> Optional[Category]:
        return self.get_category(self.default_category_id) if self.default_category_id else None

    def _ensure_default_category(self):
        needs_save = False
        if not self.categories:
            default_cat = self.create_category("General", "Default category", "#6c757d")
            self.default_category_id = default_cat.id
            needs_save = True
        elif not self.default_category_id or not self.get_category(self.default_category_id):
            self.default_category_id = next(iter(self.categories.keys()), None)
            needs_save = True
        
        if needs_save:
            self.save_data()

    def get_projects_by_category(self, category_id: str) -> List[Project]:
        return [p for p in self.list_projects() if p.category_id == category_id]

    def get_global_summary(self) -> Dict:
        if not self.projects:
            return {'total_projects': 0, 'active_projects': 0, 'completed_projects': 0, 'total_tasks': 0, 'completed_tasks': 0, 'total_stages': 0, 'completed_stages': 0, 'overall_progress': 0.0}
        
        total_projects = len(self.projects)
        completed_projects = sum(1 for p in self.projects.values() if p.is_completed())
        
        total_tasks = sum(len(s.tasks) for p in self.projects.values() for s in p.stages)
        completed_tasks = sum(1 for p in self.projects.values() for s in p.stages for t in s.tasks if t.status == TaskStatus.COMPLETED)
        
        total_stages = sum(len(p.stages) for p in self.projects.values())
        completed_stages = sum(1 for p in self.projects.values() for s in p.stages if s.status == StageStatus.COMPLETED)
        
        overall_progress = sum(p.get_overall_progress() for p in self.projects.values()) / total_projects if total_projects > 0 else 0.0
        
        return {
            'total_projects': total_projects,
            'active_projects': total_projects - completed_projects,
            'completed_projects': completed_projects,
            'total_tasks': total_tasks,
            'completed_tasks': completed_tasks,
            'total_stages': total_stages,
            'completed_stages': completed_stages,
            'overall_progress': overall_progress
        }

    def save_data(self):
        data = {
            'projects': {pid: p.to_dict() for pid, p in self.projects.items()},
            'categories': {cid: c.to_dict() for cid, c in self.categories.items()},
            'templates': self.templates,
            'default_category_id': self.default_category_id,
            'metadata': self.metadata
        }
        try:
            with open(self.data_file, 'w') as f:
                json.dump(data, f, indent=2, default=str)
        except IOError as e:
            print(f"Error saving data to {self.data_file}: {e}")

    def load_data(self):
        if not os.path.exists(self.data_file):
            self.projects, self.categories, self.templates, self.default_category_id = {}, {}, {}, None
            self.metadata = self._get_default_metadata()
            self._create_default_templates()
            return

        try:
            with open(self.data_file, 'r') as f:
                content = f.read().strip()
                if not content:
                    # File exists but is empty - don't overwrite, just initialize
                    print(f"Warning: {self.data_file} is empty. Initializing with defaults but not saving.")
                    self.projects, self.categories, self.templates, self.default_category_id = {}, {}, {}, None
                    self.metadata = self._get_default_metadata()
                    self._create_default_templates()
                    return
                
                data = json.loads(content)
                self.projects = {pid: Project.from_dict(p_data) for pid, p_data in data.get('projects', {}).items()}
                self.categories = {cid: Category.from_dict(c_data) for cid, c_data in data.get('categories', {}).items()}
                self.templates = data.get('templates', {})
                self.default_category_id = data.get('default_category_id')
                self.metadata = data.get('metadata', self._get_default_metadata())
                
                # Ensure metadata has all required fields
                default_metadata = self._get_default_metadata()
                for key, value in default_metadata.items():
                    if key not in self.metadata:
                        self.metadata[key] = value
                
                if not self.templates:
                    self._create_default_templates()
        except (json.JSONDecodeError, KeyError, TypeError) as e:
            print(f"Warning: Could not load or parse {self.data_file}. Error: {e}")
            # Don't automatically overwrite - preserve existing instance data if we have it
            if not hasattr(self, 'projects') or self.projects is None:
                print(f"Initializing fresh data for {self.data_file}")
                self.projects, self.categories, self.templates, self.default_category_id = {}, {}, {}, None
                self.metadata = self._get_default_metadata()
                self._create_default_templates()

    def _get_default_metadata(self):
        """Get default metadata structure"""
        return {
            'subtitle': 'Comprehensive Project Management System with Real-time Updates',
            'description': '',
            'created_at': datetime.now().isoformat(),
            'last_modified': datetime.now().isoformat()
        }

    def update_metadata(self, **kwargs):
        """Update metadata fields"""
        for key, value in kwargs.items():
            if key in ['subtitle', 'description']:
                self.metadata[key] = value
        self.metadata['last_modified'] = datetime.now().isoformat()
        self.save_data()

    def get_subtitle(self):
        """Get the current subtitle"""
        return self.metadata.get('subtitle', 'Comprehensive Project Management System with Real-time Updates')

    def set_subtitle(self, subtitle: str):
        """Set a new subtitle"""
        self.update_metadata(subtitle=subtitle)

    def _create_default_templates(self):
        """Create default project templates"""
        import uuid
        
        # Standard Software Development Template
        self.templates["standard"] = {
            "id": "standard",
            "name": "Standard Software Development",
            "description": "Traditional software development lifecycle",
            "stages": [
                {
                    "name": "Planning",
                    "description": "Project planning and requirement gathering",
                    "tasks": ["Define requirements", "Create timeline", "Assign resources"]
                },
                {
                    "name": "Design",
                    "description": "System and UI design",
                    "tasks": ["Create wireframes", "Design mockups", "Review design"]
                },
                {
                    "name": "Development",
                    "description": "Code implementation",
                    "tasks": ["Set up environment", "Implement features", "Code review"]
                },
                {
                    "name": "Testing",
                    "description": "Quality assurance and testing",
                    "tasks": ["Write test cases", "Execute tests", "Fix bugs"]
                },
                {
                    "name": "Deployment",
                    "description": "Production deployment",
                    "tasks": ["Deploy to staging", "User acceptance testing", "Deploy to production"]
                },
                {
                    "name": "Launch",
                    "description": "Project launch and monitoring",
                    "tasks": ["Monitor launch", "Gather feedback", "Create documentation"]
                }
            ],
            "created_at": datetime.now().isoformat(),
            "is_default": True
        }
        
        # Agile Sprint Template
        self.templates["agile"] = {
            "id": "agile",
            "name": "Agile Sprint",
            "description": "Single sprint in agile development",
            "stages": [
                {
                    "name": "Sprint Planning",
                    "description": "Plan sprint goals and tasks",
                    "tasks": ["Define sprint goals", "Estimate story points", "Create sprint backlog"]
                },
                {
                    "name": "Development",
                    "description": "Sprint development work",
                    "tasks": ["Daily standups", "Develop features", "Update task board"]
                },
                {
                    "name": "Review & Retrospective",
                    "description": "Sprint review and retrospective",
                    "tasks": ["Sprint demo", "Gather feedback", "Retrospective meeting"]
                }
            ],
            "created_at": datetime.now().isoformat(),
            "is_default": True
        }
        
        # Simple Task Template
        self.templates["simple"] = {
            "id": "simple",
            "name": "Simple Task",
            "description": "Basic task template with minimal stages",
            "stages": [
                {
                    "name": "To Do",
                    "description": "Tasks to be completed",
                    "tasks": ["Complete main task"]
                },
                {
                    "name": "In Progress",
                    "description": "Tasks currently being worked on",
                    "tasks": ["Work on task"]
                },
                {
                    "name": "Done",
                    "description": "Completed tasks",
                    "tasks": ["Review completion"]
                }
            ],
            "created_at": datetime.now().isoformat(),
            "is_default": True
        }

    def list_templates(self):
        """Get all project templates"""
        return list(self.templates.values())

    def get_template(self, template_id: str):
        """Get a specific template by ID"""
        return self.templates.get(template_id)

    def create_template(self, name: str, description: str, stages: List[Dict]) -> str:
        """Create a new project template"""
        import uuid
        template_id = str(uuid.uuid4())
        
        self.templates[template_id] = {
            "id": template_id,
            "name": name,
            "description": description,
            "stages": stages,
            "created_at": datetime.now().isoformat(),
            "is_default": False
        }
        
        self.save_data()
        return template_id

    def update_template(self, template_id: str, name: str, description: str, stages: List[Dict]) -> bool:
        """Update an existing template"""
        if template_id not in self.templates:
            return False
        
        # Don't allow updating default templates
        if self.templates[template_id].get("is_default", False):
            return False
            
        self.templates[template_id].update({
            "name": name,
            "description": description,
            "stages": stages
        })
        
        self.save_data()
        return True

    def delete_template(self, template_id: str) -> bool:
        """Delete a template"""
        if template_id not in self.templates:
            return False
        
        # Don't allow deleting default templates
        if self.templates[template_id].get("is_default", False):
            return False
            
        del self.templates[template_id]
        self.save_data()
        return True

    def create_project_from_template(self, name: str, description: str = "", deadline: str = None, category_id: str = None, template_id: str = "standard") -> Project:
        """Create a new project using a template"""
        import uuid
        
        template = self.get_template(template_id)
        if not template:
            template = self.get_template("standard")  # Fallback to standard template
        
        project = Project(name, description, deadline, category_id)
        
        # Create stages and tasks from template
        for stage_template in template["stages"]:
            stage = Stage(
                stage_template["name"],
                stage_template.get("description", "")
            )
            
            # Add tasks from template
            for task_name in stage_template.get("tasks", []):
                task = Task(
                    task_name,
                    f"Default task for {stage_template['name']} stage"
                )
                stage.tasks.append(task)
            
            project.stages.append(stage)
        
        # Start the first stage automatically
        if project.stages:
            project.stages[0].start()
        
        self.projects[project.id] = project
        self.save_data()
        return project
