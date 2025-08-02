# Project Management System

A comprehensive command-line project management tool that helps you organize projects into stages and track tasks through completion.

## Features

- **Multi-stage Project Management**: Organize projects into customizable stages
- **Task Tracking**: Add, update, and complete tasks within each stage
- **Progress Monitoring**: Track progress at both task and project levels
- **Data Persistence**: Automatically saves and loads projects from JSON
- **Interactive CLI**: Easy-to-use command-line interface
- **Stage Advancement**: Automatic progression through project stages

## Quick Start

### Run the CLI Interface
```bash
python3 cli.py
```

### Run the Example Demo
```bash
python3 example_usage.py
```

## CLI Commands

### Project Management
- `create project <name> [description]` - Create a new project
- `list projects` - List all projects
- `select project <id>` - Select a project to work with
- `show project` - Show current project details
- `delete project <id>` - Delete a project
- `project progress` - Show detailed project progress

### Stage Management
- `add stage <name> [description]` - Add a stage to current project
- `list stages` - List stages in current project
- `show stage <stage_id>` - Show stage details
- `next stage` - Advance to next stage
- `complete stage` - Complete current stage

### Task Management
- `add task <name> [description] [assignee]` - Add task to current stage
- `list tasks` - List tasks in current stage
- `complete task <task_id>` - Mark task as completed
- `update task <task_id> <status>` - Update task status
- `show task <task_id>` - Show task details

### Other Commands
- `current` - Show current project and stage
- `help` - Show help message
- `quit` - Exit the program

## Usage Example

1. **Create a project**:
   ```
   pm> create project "Website Redesign" "Complete company website overhaul"
   ```

2. **Add tasks to current stage**:
   ```
   pm> add task "Research competitors" "Analyze competitor sites" "Alice"
   pm> add task "Define requirements" "List feature requirements" "Bob"
   ```

3. **Complete tasks and advance**:
   ```
   pm> complete task abc123
   pm> next stage
   ```

4. **Monitor progress**:
   ```
   pm> project progress
   pm> current
   ```

## Project Structure

- **Project**: Top-level container with multiple stages
- **Stage**: Project phases (Planning, Development, Testing, etc.)
- **Task**: Individual work items within stages

## Default Stages

New projects automatically get these stages:
1. Planning
2. Development  
3. Testing
4. Deployment
5. Completion

## Data Storage

Projects are automatically saved to `projects.json` in the current directory. All changes are persisted immediately.

## Task Statuses

- `todo` - Not started
- `in_progress` - Currently being worked on
- `completed` - Finished
- `blocked` - Cannot proceed

## Stage Statuses

- `not_started` - Stage hasn't begun
- `in_progress` - Stage is active
- `completed` - All tasks in stage are done

## Requirements

- Python 3.6+
- No external dependencies required