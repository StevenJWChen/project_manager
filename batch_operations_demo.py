#!/usr/bin/env python3
"""
Batch Operations Demo
This script demonstrates the batch operations functionality for deleting projects and moving them to categories.
"""
from project_manager import ProjectManager, Task

def demo_batch_operations():
    print("🚀 BATCH OPERATIONS DEMO")
    print("=" * 60)
    print("This demo shows the enhanced batch operations functionality.\n")
    
    pm = ProjectManager()
    
    # Create sample projects for demonstration
    print("📋 Creating sample projects for batch operations demo...")
    sample_projects = []
    
    project_data = [
        ("Demo Project A", "First demo project for batch operations"),
        ("Demo Project B", "Second demo project for batch operations"),
        ("Demo Project C", "Third demo project for batch operations"),
        ("Demo Project D", "Fourth demo project for batch operations"),
        ("Demo Project E", "Fifth demo project for batch operations")
    ]
    
    for name, desc in project_data:
        project = pm.create_project(name, desc)
        sample_projects.append(project)
        print(f"  ✅ Created: {name}")
    
    # Create sample categories
    print(f"\n📁 Creating sample categories...")
    category1 = pm.create_category("Development", "Software development projects", "#28a745")
    category2 = pm.create_category("Marketing", "Marketing and promotion projects", "#007bff")
    
    print(f"  ✅ Created: {category1.name}")
    print(f"  ✅ Created: {category2.name}")
    
    print(f"\n📊 Current state:")
    print(f"  Total projects: {len(pm.list_projects())}")
    print(f"  Total categories: {len(pm.list_categories())}")
    
    # Demonstrate batch move to category
    print(f"\n📦 BATCH MOVE TO CATEGORY DEMO")
    print("-" * 40)
    
    # Move first 3 projects to Development category
    projects_to_move = sample_projects[:3]
    print(f"Moving {len(projects_to_move)} projects to '{category1.name}' category:")
    
    for project in projects_to_move:
        success = pm.assign_project_to_category(project.id, category1.id)
        print(f"  📁 {project.name} → {category1.name}: {'✅' if success else '❌'}")
    
    # Move remaining projects to Marketing category
    projects_to_move = sample_projects[3:]
    print(f"\nMoving {len(projects_to_move)} projects to '{category2.name}' category:")
    
    for project in projects_to_move:
        success = pm.assign_project_to_category(project.id, category2.id)
        print(f"  📁 {project.name} → {category2.name}: {'✅' if success else '❌'}")
    
    # Show projects by category
    print(f"\n📊 PROJECTS BY CATEGORY:")
    print("-" * 40)
    
    for category in [category1, category2]:
        category_projects = [p for p in pm.list_projects() if p.category_id == category.id]
        print(f"\n{category.name} ({len(category_projects)} projects):")
        for p in category_projects:
            if p in sample_projects:  # Only show our demo projects
                print(f"  📋 {p.name}")
    
    # Demonstrate batch delete
    print(f"\n🗑️  BATCH DELETE DEMO")
    print("-" * 40)
    
    # Delete the first 2 demo projects
    projects_to_delete = sample_projects[:2]
    print(f"Deleting {len(projects_to_delete)} projects:")
    
    deleted_count = 0
    for project in projects_to_delete:
        success = pm.delete_project(project.id)
        if success:
            deleted_count += 1
            print(f"  🗑️  Deleted: {project.name} ✅")
        else:
            print(f"  🗑️  Failed to delete: {project.name} ❌")
    
    print(f"\n📊 FINAL STATE:")
    print("-" * 40)
    print(f"  Deleted {deleted_count} projects")
    print(f"  Remaining demo projects: {len(sample_projects) - deleted_count}")
    print(f"  Total projects in system: {len(pm.list_projects())}")
    
    # Show how to use in web interface
    print(f"\n🌐 WEB INTERFACE BATCH OPERATIONS:")
    print("-" * 40)
    print(f"1. Start the web interface: python3 web_app.py")
    print(f"2. Go to: http://localhost:8083")
    print(f"3. Select projects using checkboxes:")
    print(f"   • Individual checkboxes on each project card/row")
    print(f"   • 'Select All' checkbox to select all projects")
    print(f"4. Batch operations bar appears when projects are selected")
    print(f"5. Available actions:")
    print(f"   • 🗑️  'Delete Selected' - Delete multiple projects")
    print(f"   • 📁 'Move to Category' - Move projects to a category")
    print(f"   • ❌ 'Clear Selection' - Unselect all projects")
    
    print(f"\n✨ FEATURES:")
    print("-" * 40)
    print(f"✅ Select individual projects or all at once")
    print(f"✅ Visual feedback with selection counter")
    print(f"✅ Confirmation dialogs for safety")
    print(f"✅ Works in both card and list view")
    print(f"✅ Real-time updates - no page reload needed")
    print(f"✅ Batch delete multiple projects")
    print(f"✅ Batch move projects to categories")
    print(f"✅ Remove category assignments")
    
    # Cleanup remaining demo projects
    print(f"\n🧹 CLEANUP:")
    print("-" * 40)
    
    remaining_demo_projects = [p for p in sample_projects if pm.get_project(p.id)]
    for project in remaining_demo_projects:
        pm.delete_project(project.id)
        print(f"  🗑️  Cleaned up: {project.name}")
    
    # Cleanup demo categories
    pm.delete_category(category1.id)
    pm.delete_category(category2.id)
    print(f"  📁 Cleaned up demo categories")
    
    print(f"\n🎉 BATCH OPERATIONS DEMO COMPLETE!")
    print(f"\nThe batch operations are now available in the web interface!")
    print(f"Start the web server and try selecting multiple projects.")

if __name__ == "__main__":
    demo_batch_operations()