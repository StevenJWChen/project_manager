#!/usr/bin/env python3
"""
Example usage of the Project Management System
"""
from project_manager import ProjectManager, Task

def demo():
    # Initialize the project manager
    pm = ProjectManager()
    
    # Create a new project
    project = pm.create_project(
        "Website Redesign", 
        "Complete redesign of company website",
        ["Planning", "Design", "Development", "Testing", "Launch"]
    )
    
    print(f"Created project: {project.name}")
    print(f"Project ID: {project.id}")
    
    # Get the first stage (Planning)
    planning_stage = project.stages[0]
    
    # Add tasks to the planning stage
    tasks = [
        Task("Research competitors", "Analyze competitor websites", "Alice"),
        Task("Define requirements", "List all feature requirements", "Bob"),
        Task("Create wireframes", "Design basic page layouts", "Carol")
    ]
    
    for task in tasks:
        planning_stage.add_task(task)
    
    print(f"\nAdded {len(tasks)} tasks to {planning_stage.name} stage")
    
    # Show project progress
    print(f"Initial progress: {project.get_overall_progress():.1%}")
    
    # Complete some tasks
    tasks[0].complete()  # Research competitors
    tasks[1].complete()  # Define requirements
    
    print(f"Progress after completing 2 tasks: {project.get_overall_progress():.1%}")
    
    # Complete the remaining task and advance to next stage
    tasks[2].complete()
    success, message = project.advance_to_next_stage()
    print(f"Stage advancement: {message}")
    
    # Show current stage
    current_stage = project.get_current_stage()
    print(f"Current stage: {current_stage.name if current_stage else 'None'}")
    
    # Add a task to the new stage
    if current_stage:
        design_task = Task("Create mockups", "Design high-fidelity mockups", "Carol")
        current_stage.add_task(design_task)
        print(f"Added task to {current_stage.name}: {design_task.name}")
    
    # Show final project status
    print(f"\nFinal project progress: {project.get_overall_progress():.1%}")
    print(f"Project completed: {project.is_completed()}")
    
    # Save the project
    pm.save_projects()
    print("Project saved to file")

if __name__ == "__main__":
    demo()