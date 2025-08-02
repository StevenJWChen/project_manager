#!/usr/bin/env python3
"""
Test script for the enhanced project management features
"""
from project_manager import ProjectManager, Task

def test_enhancements():
    print("🚀 Testing Enhanced Project Management Features")
    print("=" * 60)
    
    pm = ProjectManager()
    
    # Create a test project
    print("\n📋 Creating test project...")
    project = pm.create_project(
        "Feature Enhancement Test",
        "Testing new navigation and summary features"
    )
    
    # Add tasks to first stage
    planning_stage = project.stages[0]  # Planning stage
    tasks = [
        Task("Define requirements", "List all requirements", "Alice"),
        Task("Create timeline", "Set project milestones", "Bob")
    ]
    
    for task in tasks:
        planning_stage.add_task(task)
        task.complete()  # Complete all tasks
    
    print(f"✅ Added and completed {len(tasks)} tasks in Planning stage")
    
    # Test stage advancement
    print(f"\n➡️  Current stage: {project.get_current_stage().name}")
    success, message = project.advance_to_next_stage()
    print(f"   {message}")
    print(f"   New current stage: {project.get_current_stage().name}")
    
    # Test going back to previous stage
    print(f"\n⬅️  Testing go back feature...")
    success, message = project.go_back_to_previous_stage()
    print(f"   {message}")
    print(f"   Current stage after going back: {project.get_current_stage().name}")
    
    # Test going forward again
    print(f"\n➡️  Advancing again...")
    success, message = project.advance_to_next_stage()
    print(f"   {message}")
    
    # Add task to current stage
    current_stage = project.get_current_stage()
    design_task = Task("Create mockups", "Design UI mockups", "Carol")
    current_stage.add_task(design_task)
    print(f"   Added task to {current_stage.name}: {design_task.name}")
    
    # Test project summary
    print(f"\n📊 Testing project summary...")
    summary = project.get_project_summary()
    print(f"   Total stages: {summary['total_stages']}")
    print(f"   Completed stages: {summary['completed_stages']}")
    print(f"   Total tasks: {summary['total_tasks']}")
    print(f"   Completed tasks: {summary['completed_tasks']}")
    print(f"   Overall progress: {summary['overall_progress']:.1%}")
    print(f"   Current stage: {summary['current_stage']}")
    
    # Test global summary
    print(f"\n🌐 Testing global summary...")
    global_summary = pm.get_global_summary()
    print(f"   Total projects: {global_summary['total_projects']}")
    print(f"   Active projects: {global_summary['active_projects']}")
    print(f"   Completed projects: {global_summary['completed_projects']}")
    print(f"   Total stages: {global_summary['total_stages']}")
    print(f"   Completed stages: {global_summary['completed_stages']}")
    print(f"   Total tasks: {global_summary['total_tasks']}")
    print(f"   Completed tasks: {global_summary['completed_tasks']}")
    print(f"   Overall progress: {global_summary['overall_progress']:.1%}")
    
    # Save the updated data
    pm.save_projects()
    print(f"\n💾 All data saved to projects.json")
    
    print(f"\n✨ Enhancement Testing Complete!")
    print(f"\n🌐 Web Interface Features:")
    print(f"   • Dashboard: http://localhost:8082")
    print(f"   • Summary Page: http://localhost:8082/summary")
    print(f"   • Project Details: Click 'View Details' on any project")
    print(f"\n🔧 New Features Available:")
    print(f"   ✅ Go back to previous stage (Previous Stage button)")
    print(f"   ✅ Summary page with global statistics")
    print(f"   ✅ Progress tracking across all projects")
    print(f"   ✅ Detailed project breakdown table")

if __name__ == "__main__":
    test_enhancements()