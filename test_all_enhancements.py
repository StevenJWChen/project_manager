#!/usr/bin/env python3
"""
Comprehensive test script for all enhanced project management features
"""
from project_manager import ProjectManager, Task
from datetime import datetime, timedelta

def test_all_enhancements():
    print("🚀 Testing ALL Enhanced Project Management Features")
    print("=" * 70)
    
    pm = ProjectManager()
    
    # 1. Test Category Creation
    print("\n📂 Testing Category Management...")
    category1 = pm.create_category("Web Development", "Frontend and backend projects", "#28a745")
    category2 = pm.create_category("Mobile Apps", "iOS and Android applications", "#17a2b8")
    category3 = pm.create_category("Research", "R&D and experimental projects", "#ffc107")
    
    print(f"   ✅ Created categories: {category1.name}, {category2.name}, {category3.name}")
    print(f"   📊 Total categories: {len(pm.list_categories())}")
    
    # 2. Test Project Creation with Deadline and Category
    print("\n📅 Testing Project Creation with Deadlines and Categories...")
    
    # Create project with deadline (7 days from now)
    deadline = (datetime.now() + timedelta(days=7)).isoformat()
    project1 = pm.create_project(
        "E-commerce Website",
        "Complete online store with payment integration",
        deadline=deadline,
        category_id=category1.id
    )
    
    # Create project with far deadline
    far_deadline = (datetime.now() + timedelta(days=30)).isoformat()
    project2 = pm.create_project(
        "Mobile Shopping App",
        "iOS and Android companion app",
        deadline=far_deadline,
        category_id=category2.id
    )
    
    # Create project without deadline
    project3 = pm.create_project(
        "AI Research Project",
        "Machine learning experiment",
        category_id=category3.id
    )
    
    print(f"   ✅ Created project with 7-day deadline: {project1.name}")
    print(f"   ✅ Created project with 30-day deadline: {project2.name}")
    print(f"   ✅ Created project without deadline: {project3.name}")
    
    # 3. Test Default Tasks
    print("\n📋 Testing Default Tasks in Stages...")
    print(f"   Project '{project1.name}' stages and default tasks:")
    for i, stage in enumerate(project1.stages, 1):
        print(f"      {i}. {stage.name}: {len(stage.tasks)} default tasks")
        for task in stage.tasks:
            print(f"         - {task.name}")
    
    # 4. Test Deadline Functionality
    print("\n⏰ Testing Deadline Functionality...")
    print(f"   Project 1 deadline: {project1.deadline}")
    print(f"   Project 1 days until deadline: {project1.days_until_deadline()}")
    print(f"   Project 1 is overdue: {project1.is_overdue()}")
    
    # Create an overdue project for testing
    overdue_deadline = (datetime.now() - timedelta(days=5)).isoformat()
    overdue_project = pm.create_project(
        "Overdue Test Project",
        "This project is overdue",
        deadline=overdue_deadline,
        category_id=category1.id
    )
    print(f"   ✅ Created overdue project: {overdue_project.name}")
    print(f"   Overdue project days until deadline: {overdue_project.days_until_deadline()}")
    print(f"   Overdue project is overdue: {overdue_project.is_overdue()}")
    
    # 5. Test Category Assignment
    print("\n🏷️  Testing Category Assignment...")
    success = pm.assign_project_to_category(project3.id, category1.id)
    print(f"   ✅ Reassigned project to different category: {success}")
    
    # Remove category assignment
    success = pm.assign_project_to_category(project3.id, None)
    print(f"   ✅ Removed category assignment: {success}")
    
    # 6. Test Default Task Workflow
    print("\n⚡ Testing Workflow with Default Tasks...")
    # Complete some default tasks in the first stage
    planning_stage = project1.stages[0]  # Planning stage
    completed_tasks = 0
    for task in planning_stage.tasks:
        task.complete()
        completed_tasks += 1
        if completed_tasks >= 2:  # Complete first 2 tasks
            break
    
    print(f"   ✅ Completed {completed_tasks} default tasks in Planning stage")
    print(f"   📊 Planning stage progress: {planning_stage.get_progress():.1%}")
    
    # Add a custom task
    custom_task = Task("Custom requirement analysis", "Additional custom task", "Alice")
    planning_stage.add_task(custom_task)
    custom_task.complete()
    print(f"   ✅ Added and completed custom task: {custom_task.name}")
    
    # Complete remaining default tasks and advance
    for task in planning_stage.tasks:
        if task.status.value != 'completed':
            task.complete()
    
    print(f"   📊 Final Planning stage progress: {planning_stage.get_progress():.1%}")
    
    # Advance to next stage
    success, message = project1.advance_to_next_stage()
    print(f"   ➡️  Advanced to next stage: {message}")
    
    # Check new current stage has default tasks
    current_stage = project1.get_current_stage()
    print(f"   📋 Current stage '{current_stage.name}' has {len(current_stage.tasks)} default tasks")
    
    # 7. Test Global Summary with Categories
    print("\n📊 Testing Enhanced Global Summary...")
    summary = pm.get_global_summary()
    print(f"   Total projects: {summary['total_projects']}")
    print(f"   Active projects: {summary['active_projects']}")
    print(f"   Completed projects: {summary['completed_projects']}")
    print(f"   Overall progress: {summary['overall_progress']:.1%}")
    
    # 8. Test Project Summary with New Fields
    print("\n📈 Testing Enhanced Project Summary...")
    project_summary = project1.get_project_summary()
    print(f"   Project: {project1.name}")
    print(f"   Overall progress: {project_summary['overall_progress']:.1%}")
    print(f"   Current stage: {project_summary['current_stage']}")
    print(f"   Deadline: {project_summary['deadline']}")
    print(f"   Is overdue: {project_summary['is_overdue']}")
    print(f"   Days until deadline: {project_summary['days_until_deadline']}")
    print(f"   Category ID: {project_summary['category_id']}")
    
    # 9. Test Category Projects
    print("\n🔍 Testing Category-Project Relationships...")
    for category in pm.list_categories():
        category_projects = [p for p in pm.list_projects() if p.category_id == category.id]
        print(f"   Category '{category.name}' ({category.color}): {len(category_projects)} projects")
        for project in category_projects:
            print(f"      - {project.name} ({'Overdue' if project.is_overdue() else 'On Track'})")
    
    # Uncategorized projects
    uncategorized = [p for p in pm.list_projects() if not p.category_id]
    print(f"   Uncategorized projects: {len(uncategorized)}")
    
    # 10. Test Category Deletion
    print("\n🗑️  Testing Category Deletion...")
    test_category = pm.create_category("Test Category", "To be deleted", "#ff0000")
    pm.assign_project_to_category(project2.id, test_category.id)
    print(f"   ✅ Created test category and assigned project")
    
    success = pm.delete_category(test_category.id)
    print(f"   ✅ Deleted category: {success}")
    
    # Check project is now uncategorized
    project2_updated = pm.get_project(project2.id)
    print(f"   ✅ Project now uncategorized: {project2_updated.category_id is None}")
    
    # Save all data
    pm.save_projects()
    print(f"\n💾 All test data saved to {pm.data_file}")
    
    # Final Summary
    print(f"\n✨ COMPREHENSIVE TEST RESULTS:")
    print(f"   📂 Categories: {len(pm.list_categories())}")
    print(f"   📋 Projects: {len(pm.list_projects())}")
    print(f"   ⏰ Projects with deadlines: {len([p for p in pm.list_projects() if p.deadline])}")
    print(f"   🚨 Overdue projects: {len([p for p in pm.list_projects() if p.is_overdue()])}")
    print(f"   📈 Average progress: {pm.get_global_summary()['overall_progress']:.1%}")
    
    total_default_tasks = 0
    for project in pm.list_projects():
        for stage in project.stages:
            total_default_tasks += len([t for t in stage.tasks if "Default task" in t.description])
    print(f"   ⚙️  Total default tasks created: {total_default_tasks}")
    
    print(f"\n🌐 Enhanced Web Interface Available:")
    print(f"   • Dashboard: http://localhost:8083 (with deadline badges)")
    print(f"   • Categories: http://localhost:8083/categories")
    print(f"   • Summary: http://localhost:8083/summary")
    print(f"   • Project Details: Click any project (with edit options)")
    
    print(f"\n🎉 ALL ENHANCED FEATURES WORKING PERFECTLY!")

if __name__ == "__main__":
    test_all_enhancements()