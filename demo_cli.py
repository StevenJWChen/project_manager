#!/usr/bin/env python3
"""
Demo script that simulates CLI interactions for demonstration
"""
from project_manager import ProjectManager, Task, TaskStatus

def demo_cli():
    print("🚀 Project Management System - CLI Demo")
    print("=" * 50)
    
    # Create project manager
    pm = ProjectManager()
    
    # Create a demo project
    print("\n📋 Creating new project: 'Mobile App Development'")
    project = pm.create_project(
        "Mobile App Development", 
        "Complete mobile app for iOS and Android",
        ["Research", "Design", "Development", "Testing", "Launch"]
    )
    print(f"✅ Project created with ID: {project.id[:8]}...")
    
    # Show initial project status
    print(f"\n📊 Initial project progress: {project.get_overall_progress():.1%}")
    print(f"📋 Stages: {len(project.stages)}")
    print(f"🎯 Current stage: {project.get_current_stage().name}")
    
    # Add tasks to Research stage
    print(f"\n➕ Adding tasks to '{project.get_current_stage().name}' stage...")
    research_stage = project.get_current_stage()
    
    tasks = [
        Task("Market analysis", "Research competitor apps and market trends", "Alice"),
        Task("User interviews", "Conduct user research and interviews", "Bob"),
        Task("Technical requirements", "Define technical specifications", "Carol"),
        Task("Platform decision", "Choose development platforms", "Alice")
    ]
    
    for task in tasks:
        research_stage.add_task(task)
        print(f"  ✅ Added: {task.name} (assigned to {task.assignee})")
    
    print(f"\n📈 Progress after adding tasks: {project.get_overall_progress():.1%}")
    
    # Complete some tasks
    print(f"\n⏳ Completing tasks...")
    tasks[0].complete()  # Market analysis
    print(f"  ✅ Completed: {tasks[0].name}")
    
    tasks[1].complete()  # User interviews  
    print(f"  ✅ Completed: {tasks[1].name}")
    
    print(f"📈 Progress after completing 2 tasks: {project.get_overall_progress():.1%}")
    print(f"📊 Research stage progress: {research_stage.get_progress():.1%}")
    
    # Complete remaining tasks and advance
    print(f"\n⏳ Completing remaining tasks...")
    tasks[2].complete()  # Technical requirements
    tasks[3].complete()  # Platform decision
    print(f"  ✅ All tasks completed in Research stage")
    
    # Advance to next stage
    print(f"\n➡️  Advancing to next stage...")
    success, message = project.advance_to_next_stage()
    print(f"  {message}")
    
    current_stage = project.get_current_stage()
    print(f"🎯 New current stage: {current_stage.name}")
    
    # Add task to new stage
    design_task = Task("Create wireframes", "Design app wireframes and user flow", "Carol")
    current_stage.add_task(design_task)
    print(f"  ✅ Added task to {current_stage.name}: {design_task.name}")
    
    # Show final status
    print(f"\n📊 Final Project Status:")
    print(f"  📈 Overall progress: {project.get_overall_progress():.1%}")
    print(f"  📋 Completed stages: {len([s for s in project.stages if s.status.value == 'completed'])}")
    print(f"  🎯 Current stage: {current_stage.name}")
    print(f"  ✅ Project completed: {project.is_completed()}")
    
    # Show all stages and their status
    print(f"\n📋 All Stages Status:")
    status_icons = {
        'not_started': '⏸️',
        'in_progress': '🔄', 
        'completed': '✅'
    }
    
    for i, stage in enumerate(project.stages, 1):
        icon = status_icons.get(stage.status.value, '❓')
        progress = stage.get_progress()
        task_count = len(stage.tasks)
        completed_count = len([t for t in stage.tasks if t.status == TaskStatus.COMPLETED])
        
        print(f"  {i}. {icon} {stage.name}: {progress:.1%} ({completed_count}/{task_count} tasks)")
    
    # Save project
    pm.save_projects()
    print(f"\n💾 Project data saved to projects.json")
    
    print(f"\n🌐 Web Interface Available:")
    print(f"  Open your browser to: http://localhost:8080")
    print(f"  Or run: python3 start_web.py")
    
    print(f"\n🖥️  CLI Interface Available:")
    print(f"  Run: python3 cli.py")
    
    print(f"\n✨ Demo completed successfully!")

if __name__ == "__main__":
    demo_cli()