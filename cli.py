#!/usr/bin/env python3
import sys
from project_manager import ProjectManager, Task, TaskStatus, StageStatus

# ANSI escape codes for colors
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class ProjectCLI:
    def __init__(self):
        self.manager = ProjectManager()
        self.current_project = None

    def run(self):
        print(f"{Colors.HEADER}🚀 Welcome to the Enhanced Project Management System{Colors.ENDC}")
        print(f"Type '{Colors.BOLD}help{Colors.ENDC}' for commands or '{Colors.BOLD}quit{Colors.ENDC}' to exit.\n")
        
        while True:
            try:
                command = input(f"{Colors.BOLD}pm> {Colors.ENDC}").strip().lower()
                if not command:
                    continue
                if command in ['quit', 'exit']:
                    print(f"{Colors.WARNING}Goodbye!{Colors.ENDC}")
                    break
                elif command == 'help':
                    self.show_help()
                else:
                    self.execute_command(command)
            except KeyboardInterrupt:
                print(f"\n{Colors.WARNING}Goodbye!{Colors.ENDC}")
                break
            except Exception as e:
                print(f"{Colors.FAIL}An unexpected error occurred: {e}{Colors.ENDC}")

    def show_help(self):
        help_text = f"""
{Colors.BOLD}Available Commands:{Colors.ENDC}

{Colors.CYAN}Project Management:{Colors.ENDC}
  {Colors.GREEN}create project <name> [desc]{Colors.ENDC}   - Create a new project
  {Colors.GREEN}list projects{Colors.ENDC}                    - List all projects
  {Colors.GREEN}select project <id>{Colors.ENDC}              - Select a project
  {Colors.GREEN}show project{Colors.ENDC}                     - Show current project details
  {Colors.GREEN}delete project <id>{Colors.ENDC}              - Delete a project
  {Colors.GREEN}project progress{Colors.ENDC}                 - Show project progress

{Colors.CYAN}Stage Management:{Colors.ENDC}
  {Colors.GREEN}add stage <name> [desc]{Colors.ENDC}          - Add a stage to current project
  {Colors.GREEN}list stages{Colors.ENDC}                     - List stages in current project
  {Colors.GREEN}show stage <id>{Colors.ENDC}                   - Show stage details
  {Colors.GREEN}next stage{Colors.ENDC}                      - Advance to the next stage
  {Colors.GREEN}back stage{Colors.ENDC}                      - Go back to the previous stage
  {Colors.GREEN}complete stage{Colors.ENDC}                  - Complete current stage

{Colors.CYAN}Task Management:{Colors.ENDC}
  {Colors.GREEN}add task <name> [desc] [assignee]{Colors.ENDC} - Add a task to current stage
  {Colors.GREEN}list tasks{Colors.ENDC}                      - List tasks in current stage
  {Colors.GREEN}complete task <id>{Colors.ENDC}               - Mark a task as completed
  {Colors.GREEN}update task <id> <status>{Colors.ENDC}        - Update task status (todo/in_progress/completed/blocked)
  {Colors.GREEN}show task <id>{Colors.ENDC}                    - Show task details

{Colors.CYAN}Other:{Colors.ENDC}
  {Colors.GREEN}current{Colors.ENDC}                         - Show current project and stage
  {Colors.GREEN}help{Colors.ENDC}                            - Show this help message
  {Colors.GREEN}quit/exit{Colors.ENDC}                       - Exit the program
        """
        print(help_text)

    def execute_command(self, command):
        parts = command.split()
        cmd, args = parts[0], parts[1:]

        if cmd == "create" and args and args[0] == "project":
            self.create_project(args[1:])
        elif cmd == "list" and args:
            if args[0] == "projects": self.list_projects()
            elif args[0] == "stages": self.list_stages()
            elif args[0] == "tasks": self.list_tasks()
        elif cmd == "select" and args and args[0] == "project":
            self.select_project(args[1])
        elif cmd == "show" and args:
            if args[0] == "project": self.show_project()
            elif args[0] == "stage" and len(args) > 1: self.show_stage(args[1])
            elif args[0] == "task" and len(args) > 1: self.show_task(args[1])
        elif cmd == "add" and args:
            if args[0] == "stage": self.add_stage(args[1:])
            elif args[0] == "task": self.add_task(args[1:])
        elif cmd == "complete" and args:
            if args[0] == "stage": self.complete_stage()
            elif args[0] == "task" and len(args) > 1: self.complete_task(args[1])
        elif cmd == "next" and args and args[0] == "stage":
            self.next_stage()
        elif cmd == "back" and args and args[0] == "stage":
            self.previous_stage()
        elif cmd == "update" and args and args[0] == "task" and len(args) > 2:
            self.update_task(args[1], args[2])
        elif cmd == "delete" and args and args[0] == "project":
            self.delete_project(args[1])
        elif cmd == "project" and args and args[0] == "progress":
            self.show_project_progress()
        elif cmd == "current":
            self.show_current()
        else:
            print(f"{Colors.FAIL}Unknown command. Type 'help' for assistance.{Colors.ENDC}")

    def create_project(self, args):
        if not args:
            print(f"{Colors.FAIL}Error: Project name is required.{Colors.ENDC}")
            return
        name = args[0]
        description = " ".join(args[1:]) if len(args) > 1 else ""
        project = self.manager.create_project(name, description)
        self.current_project = project
        print(f"{Colors.GREEN}✅ Created project '{name}' with ID: {project.id[:8]}...{Colors.ENDC}")
        print(f"📝 Default stages created: {Colors.CYAN}{', '.join([s.name for s in project.stages])}{Colors.ENDC}")

    def list_projects(self):
        projects = self.manager.list_projects()
        if not projects:
            print(f"{Colors.WARNING}No projects found. Use 'create project' to start.{Colors.ENDC}")
            return
        print(f"\n{Colors.HEADER}{Colors.BOLD}📋 All Projects:{Colors.ENDC}")
        for p in projects:
            progress = p.get_overall_progress()
            status_color = Colors.GREEN if p.is_completed() else (Colors.WARNING if p.is_overdue() else Colors.CYAN)
            status_text = "✅ Completed" if p.is_completed() else f"🔄 {progress:.1%} complete"
            current_marker = f"{Colors.BOLD} (current){Colors.ENDC}" if self.current_project and p.id == self.current_project.id else ""
            overdue_marker = f"{Colors.FAIL} (Overdue){Colors.ENDC}" if p.is_overdue() else ""
            print(f"  {p.id[:8]}... - {Colors.BOLD}{p.name}{Colors.ENDC} - {status_color}{status_text}{Colors.ENDC}{overdue_marker}{current_marker}")

    def select_project(self, project_id):
        matching = [p for p in self.manager.projects.values() if p.id.startswith(project_id)]
        if not matching:
            print(f"{Colors.FAIL}Project with ID starting with '{project_id}' not found.{Colors.ENDC}")
            return
        if len(matching) > 1:
            print(f"{Colors.FAIL}Multiple projects match '{project_id}'. Please be more specific.{Colors.ENDC}")
            return
        self.current_project = matching[0]
        print(f"{Colors.GREEN}✅ Selected project: {self.current_project.name}{Colors.ENDC}")

    def show_project(self):
        if not self.current_project:
            print(f"{Colors.FAIL}No project selected. Use 'select project <id>'.{Colors.ENDC}")
            return
        p = self.current_project
        print(f"\n{Colors.HEADER}{Colors.BOLD}📊 Project: {p.name}{Colors.ENDC}")
        print(f"  {Colors.CYAN}Description:{Colors.ENDC} {p.description}")
        print(f"  {Colors.CYAN}Progress:{Colors.ENDC} {p.get_overall_progress():.1%}")
        print(f"  {Colors.CYAN}Status:{Colors.ENDC} {'✅ Completed' if p.is_completed() else '🔄 In Progress'}")
        current_stage = p.get_current_stage()
        if current_stage:
            print(f"  {Colors.CYAN}Current Stage:{Colors.ENDC} {current_stage.name}")

    def show_project_progress(self):
        if not self.current_project:
            print(f"{Colors.FAIL}No project selected.{Colors.ENDC}")
            return
        p = self.current_project
        print(f"\n{Colors.HEADER}{Colors.BOLD}📈 Progress for '{p.name}':{Colors.ENDC}")
        for i, stage in enumerate(p.stages, 1):
            icon = {
                StageStatus.NOT_STARTED: "⏸️",
                StageStatus.IN_PROGRESS: "🔄",
                StageStatus.COMPLETED: "✅"
            }.get(stage.status, "❓")
            print(f"  {i}. {icon} {stage.name}: {stage.get_progress():.1%} ({len([t for t in stage.tasks if t.status == TaskStatus.COMPLETED])}/{len(stage.tasks)} tasks)")

    def add_stage(self, args):
        if not self.current_project:
            print(f"{Colors.FAIL}No project selected.{Colors.ENDC}")
            return
        if not args:
            print(f"{Colors.FAIL}Error: Stage name required.{Colors.ENDC}")
            return
        name = args[0]
        description = " ".join(args[1:]) if len(args) > 1 else ""
        from project_manager import Stage
        self.current_project.add_stage(Stage(name, description))
        self.manager.save_data()
        print(f"{Colors.GREEN}✅ Added stage '{name}' to project.{Colors.ENDC}")

    def list_stages(self):
        if not self.current_project:
            print(f"{Colors.FAIL}No project selected.{Colors.ENDC}")
            return
        stages = self.current_project.stages
        if not stages:
            print(f"{Colors.WARNING}No stages in current project.{Colors.ENDC}")
            return
        print(f"\n{Colors.HEADER}{Colors.BOLD}📋 Stages in '{self.current_project.name}':{Colors.ENDC}")
        for i, stage in enumerate(stages, 1):
            icon = {
                StageStatus.NOT_STARTED: "⏸️",
                StageStatus.IN_PROGRESS: "🔄",
                StageStatus.COMPLETED: "✅"
            }.get(stage.status, "❓")
            print(f"  {i}. {icon} {stage.name} - {stage.get_progress():.1%} ({len(stage.tasks)} tasks)")

    def show_stage(self, stage_id):
        if not self.current_project:
            print(f"{Colors.FAIL}No project selected.{Colors.ENDC}")
            return
        matching = [s for s in self.current_project.stages if s.id.startswith(stage_id)]
        if not matching:
            print(f"{Colors.FAIL}Stage with ID starting with '{stage_id}' not found.{Colors.ENDC}")
            return
        stage = matching[0]
        print(f"\n{Colors.HEADER}{Colors.BOLD}📋 Stage: {stage.name}{Colors.ENDC}")
        print(f"  {Colors.CYAN}Description:{Colors.ENDC} {stage.description}")
        print(f"  {Colors.CYAN}Status:{Colors.ENDC} {stage.status.value}")
        print(f"  {Colors.CYAN}Progress:{Colors.ENDC} {stage.get_progress():.1%}")
        print(f"  {Colors.CYAN}Tasks:{Colors.ENDC} {len(stage.tasks)}")

    def add_task(self, args):
        if not self.current_project:
            print(f"{Colors.FAIL}No project selected.{Colors.ENDC}")
            return
        current_stage = self.current_project.get_current_stage()
        if not current_stage:
            print(f"{Colors.FAIL}No active stage to add tasks to.{Colors.ENDC}")
            return
        if not args:
            print(f"{Colors.FAIL}Error: Task name required.{Colors.ENDC}")
            return
        name, desc, assignee = args[0], (args[1] if len(args) > 1 else ""), (args[2] if len(args) > 2 else "")
        current_stage.add_task(Task(name, desc, assignee))
        self.manager.save_data()
        print(f"{Colors.GREEN}✅ Added task '{name}' to stage '{current_stage.name}'.{Colors.ENDC}")

    def list_tasks(self):
        if not self.current_project:
            print(f"{Colors.FAIL}No project selected.{Colors.ENDC}")
            return
        current_stage = self.current_project.get_current_stage()
        if not current_stage:
            print(f"{Colors.FAIL}No active stage found.{Colors.ENDC}")
            return
        if not current_stage.tasks:
            print(f"{Colors.WARNING}No tasks in stage '{current_stage.name}'.{Colors.ENDC}")
            return
        print(f"\n{Colors.HEADER}{Colors.BOLD}📋 Tasks in '{current_stage.name}':{Colors.ENDC}")
        icons = {TaskStatus.TODO: "📋", TaskStatus.IN_PROGRESS: "🔄", TaskStatus.COMPLETED: "✅", TaskStatus.BLOCKED: "🚫"}
        for task in current_stage.tasks:
            assignee_info = f" ({task.assignee})" if task.assignee else ""
            print(f"  {icons.get(task.status, '❓')} {task.name}{assignee_info} - {task.status.value}")

    def complete_task(self, task_id):
        if not self.current_project:
            print(f"{Colors.FAIL}No project selected.{Colors.ENDC}")
            return
        current_stage = self.current_project.get_current_stage()
        if not current_stage:
            print(f"{Colors.FAIL}No active stage found.{Colors.ENDC}")
            return
        matching = [t for t in current_stage.tasks if t.id.startswith(task_id)]
        if not matching:
            print(f"{Colors.FAIL}Task with ID starting with '{task_id}' not found.{Colors.ENDC}")
            return
        task = matching[0]
        task.complete()
        self.manager.save_data()
        print(f"{Colors.GREEN}✅ Completed task '{task.name}'.{Colors.ENDC}")

    def update_task(self, task_id, status_str):
        if not self.current_project:
            print(f"{Colors.FAIL}No project selected.{Colors.ENDC}")
            return
        current_stage = self.current_project.get_current_stage()
        if not current_stage:
            print(f"{Colors.FAIL}No active stage found.{Colors.ENDC}")
            return
        try:
            status = TaskStatus(status_str.lower())
        except ValueError:
            print(f"{Colors.FAIL}Invalid status. Use: todo, in_progress, completed, blocked.{Colors.ENDC}")
            return
        matching = [t for t in current_stage.tasks if t.id.startswith(task_id)]
        if not matching:
            print(f"{Colors.FAIL}Task with ID starting with '{task_id}' not found.{Colors.ENDC}")
            return
        task = matching[0]
        task.status = status
        if status == TaskStatus.COMPLETED:
            task.completed_at = datetime.now().isoformat()
        self.manager.save_data()
        print(f"{Colors.GREEN}✅ Updated task '{task.name}' to {status.value}.{Colors.ENDC}")

    def show_task(self, task_id):
        if not self.current_project:
            print(f"{Colors.FAIL}No project selected.{Colors.ENDC}")
            return
        task, _ = self._find_task(task_id)
        if not task:
            print(f"{Colors.FAIL}Task with ID starting with '{task_id}' not found in any stage.{Colors.ENDC}")
            return
        print(f"\n{Colors.HEADER}{Colors.BOLD}📋 Task: {task.name}{Colors.ENDC}")
        print(f"  {Colors.CYAN}Description:{Colors.ENDC} {task.description}")
        print(f"  {Colors.CYAN}Assignee:{Colors.ENDC} {task.assignee}")
        print(f"  {Colors.CYAN}Status:{Colors.ENDC} {task.status.value}")
        print(f"  {Colors.CYAN}Created:{Colors.ENDC} {task.created_at}")
        if task.completed_at:
            print(f"  {Colors.CYAN}Completed:{Colors.ENDC} {task.completed_at}")

    def complete_stage(self):
        if not self.current_project:
            print(f"{Colors.FAIL}No project selected.{Colors.ENDC}")
            return
        current_stage = self.current_project.get_current_stage()
        if not current_stage:
            print(f"{Colors.FAIL}No active stage to complete.{Colors.ENDC}")
            return
        success, message = current_stage.complete()
        if success:
            print(f"{Colors.GREEN}✅ {message}{Colors.ENDC}")
        else:
            print(f"{Colors.FAIL}❌ {message}{Colors.ENDC}")
        self.manager.save_data()

    def next_stage(self):
        if not self.current_project:
            print(f"{Colors.FAIL}No project selected.{Colors.ENDC}")
            return
        success, message = self.current_project.advance_to_next_stage()
        if success:
            print(f"{Colors.GREEN}✅ {message}{Colors.ENDC}")
        else:
            print(f"{Colors.FAIL}❌ {message}{Colors.ENDC}")
        self.manager.save_data()

    def previous_stage(self):
        if not self.current_project:
            print(f"{Colors.FAIL}No project selected.{Colors.ENDC}")
            return
        success, message = self.current_project.go_back_to_previous_stage()
        if success:
            print(f"{Colors.GREEN}✅ {message}{Colors.ENDC}")
        else:
            print(f"{Colors.FAIL}❌ {message}{Colors.ENDC}")
        self.manager.save_data()

    def delete_project(self, project_id):
        matching = [p for p in self.manager.projects.values() if p.id.startswith(project_id)]
        if not matching:
            print(f"{Colors.FAIL}Project with ID starting with '{project_id}' not found.{Colors.ENDC}")
            return
        project = matching[0]
        confirm = input(f"{Colors.WARNING}Are you sure you want to delete project '{project.name}'? This is irreversible. (y/N): {Colors.ENDC}")
        if confirm.lower() == 'y':
            self.manager.delete_project(project.id)
            if self.current_project and self.current_project.id == project.id:
                self.current_project = None
            print(f"{Colors.GREEN}✅ Deleted project '{project.name}'.{Colors.ENDC}")
        else:
            print("Deletion cancelled.")

    def show_current(self):
        if not self.current_project:
            print(f"{Colors.FAIL}No project selected.{Colors.ENDC}")
            return
        print(f"{Colors.HEADER}{Colors.BOLD}📊 Current Project: {self.current_project.name}{Colors.ENDC}")
        current_stage = self.current_project.get_current_stage()
        if current_stage:
            print(f"  {Colors.CYAN}Current Stage:{Colors.ENDC} {current_stage.name}")
            print(f"  {Colors.CYAN}Stage Progress:{Colors.ENDC} {current_stage.get_progress():.1%}")
        else:
            print(f"  {Colors.WARNING}No active stage (project might be completed).{Colors.ENDC}")

    def _find_task(self, task_id):
        if not self.current_project:
            return None, None
        for stage in self.current_project.stages:
            for task in stage.tasks:
                if task.id.startswith(task_id):
                    return task, stage
        return None, None

if __name__ == "__main__":
    cli = ProjectCLI()
    cli.run()
