#!/usr/bin/env python3
"""
Test script to verify completion logic is working correctly
"""
from project_manager import ProjectManager, Task

def test_completion_logic():
    print("🔧 Testing Project Completion Logic Fix")
    print("=" * 50)
    
    pm = ProjectManager()
    
    # Clean up duplicate projects first
    print("\n🧹 Cleaning up duplicate projects...")
    projects_to_remove = []
    project_names = {}
    
    for project_id, project in pm.projects.items():
        if project.name in project_names:
            # This is a duplicate, mark for removal
            projects_to_remove.append(project_id)
            print(f"   Removing duplicate: {project.name} ({project_id[:8]}...)")
        else:
            project_names[project.name] = project_id
    
    for project_id in projects_to_remove:
        pm.delete_project(project_id)
    
    print(f"   Removed {len(projects_to_remove)} duplicate projects")
    
    # Create a test project to verify completion logic
    print("\n📋 Creating test project for completion verification...")
    test_project = pm.create_project(
        "Completion Test",
        "Testing project completion logic",
        ["Stage1", "Stage2", "Stage3"]  # Simple 3-stage project
    )
    
    print(f"   Created project: {test_project.name}")
    print(f"   Initial completion status: {test_project.is_completed()}")
    print(f"   Initial completed_at: {test_project.completed_at}")
    
    # Add and complete tasks in Stage1
    stage1 = test_project.stages[0]
    task1 = Task("Task 1", "First task", "Alice")
    stage1.add_task(task1)
    task1.complete()
    
    print(f"\n✅ Completed task in Stage1")
    print(f"   Project completion status: {test_project.is_completed()}")
    
    # Advance to Stage2
    success, message = test_project.advance_to_next_stage()
    print(f"\n➡️  Advanced to Stage2: {message}")
    print(f"   Project completion status: {test_project.is_completed()}")
    
    # Add and complete tasks in Stage2
    stage2 = test_project.get_current_stage()
    task2 = Task("Task 2", "Second task", "Bob")
    stage2.add_task(task2)
    task2.complete()
    
    # Advance to Stage3
    success, message = test_project.advance_to_next_stage()
    print(f"\n➡️  Advanced to Stage3: {message}")
    print(f"   Project completion status: {test_project.is_completed()}")
    
    # Add and complete tasks in Stage3
    stage3 = test_project.get_current_stage()
    task3 = Task("Task 3", "Final task", "Carol")
    stage3.add_task(task3)
    task3.complete()
    
    # Complete the project
    success, message = test_project.advance_to_next_stage()
    print(f"\n🎉 Final advancement: {message}")
    print(f"   Project completion status: {test_project.is_completed()}")
    print(f"   Project completed_at: {test_project.completed_at}")
    
    # Test going back from completed state
    print(f"\n⬅️  Testing go back from completed state...")
    success, message = test_project.go_back_to_previous_stage()
    print(f"   Go back result: {message}")
    print(f"   Project completion status after going back: {test_project.is_completed()}")
    print(f"   Project completed_at after going back: {test_project.completed_at}")
    print(f"   Current stage: {test_project.get_current_stage().name}")
    
    # Advance to complete again
    print(f"\n➡️  Advancing to complete again...")
    success, message = test_project.advance_to_next_stage()
    print(f"   Final advancement: {message}")
    print(f"   Project completion status: {test_project.is_completed()}")
    print(f"   Project completed_at: {test_project.completed_at}")
    
    # Save and show final project summary
    pm.save_projects()
    
    print(f"\n📊 Final Summary:")
    global_summary = pm.get_global_summary()
    print(f"   Total projects: {global_summary['total_projects']}")
    print(f"   Active projects: {global_summary['active_projects']}")
    print(f"   Completed projects: {global_summary['completed_projects']}")
    
    print(f"\n✅ All projects status:")
    for project in pm.list_projects():
        stages_completed = len([s for s in project.stages if s.status.value == 'completed'])
        total_stages = len(project.stages)
        print(f"   {project.name}: {project.is_completed()} ({stages_completed}/{total_stages} stages)")
    
    print(f"\n✨ Completion logic testing complete!")
    print(f"   Web interface updated at: http://localhost:8082")

if __name__ == "__main__":
    test_completion_logic()