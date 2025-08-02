#!/usr/bin/env python3
"""
Complete Project Lifecycle Automation Demo
This script demonstrates the complete project lifecycle from template creation to project completion.
The demo consistently updates the web interface so you can see changes in real-time.
"""
import time
import webbrowser
import threading
from project_manager import ProjectManager, Task, TaskStatus, StageStatus
from datetime import datetime, timedelta

class ProjectLifecycleDemo:
    def __init__(self):
        self.pm = ProjectManager()
        self.demo_project = None
        self.web_base_url = "http://localhost:8083"
        self.auto_open_browser = True
    
    def save_and_notify_web(self, action_description=""):
        """Save data and notify about web interface updates"""
        self.pm.save_data()
        if action_description:
            print(f"💾 {action_description} - Data saved to {self.pm.data_file}")
            print(f"🌐 Web interface auto-updated! Just refresh your browser to see changes.")
        time.sleep(0.5)  # Small delay to ensure data is written
    
    def show_web_links(self, project_id=None):
        """Display relevant web interface links"""
        print(f"\n🔗 View in Web Interface:")
        print(f"  📊 Dashboard: {self.web_base_url}")
        print(f"  📈 Summary: {self.web_base_url}/summary")
        print(f"  📁 Categories: {self.web_base_url}/categories")
        if project_id:
            print(f"  📋 Project Details: {self.web_base_url}/project/{project_id}")
    
    def prompt_web_check(self, message="Check the web interface"):
        """Prompt user to check web interface"""
        print(f"\n👀 {message}")
        choice = input("   Press Enter to continue (or 'o' to open browser): ").lower().strip()
        if choice == 'o' and self.auto_open_browser:
            try:
                webbrowser.open(self.web_base_url)
                print("   🌐 Browser opened!")
            except:
                print("   ⚠️  Could not open browser automatically")
        return choice
    
    def step_1_setup_environment(self):
        """Step 1: Setup environment with categories and templates"""
        print("🏗️  STEP 1: Environment Setup")
        print("=" * 60)
        
        # Create project categories
        print("Creating project categories...")
        web_category = self.pm.create_category(
            "Web Development", 
            "Frontend and backend web projects", 
            "#28a745"
        )
        self.save_and_notify_web("Created Web Development category")
        
        mobile_category = self.pm.create_category(
            "Mobile Apps", 
            "iOS and Android applications", 
            "#17a2b8"
        )
        self.save_and_notify_web("Created Mobile Apps category")
        
        print(f"✅ Created category: {web_category.name}")
        print(f"✅ Created category: {mobile_category.name}")
        
        # Show default stage templates
        print(f"\nDefault stage templates available:")
        for i, (stage_name, tasks) in enumerate(self.pm.default_stage_tasks.items(), 1):
            print(f"  {i}. {stage_name}: {len(tasks)} default tasks")
            for task in tasks:
                print(f"     - {task}")
        
        self.show_web_links()
        self.prompt_web_check("Categories have been created! Check the Categories page.")
        
        return web_category, mobile_category
    
    def step_2_create_project(self, category):
        """Step 2: Create new project with deadline"""
        print(f"\n🚀 STEP 2: Project Creation")
        print("=" * 60)
        
        # Set deadline (30 days from now)
        deadline = (datetime.now() + timedelta(days=30)).isoformat()
        
        # Create project
        project = self.pm.create_project(
            name="E-commerce Platform",
            description="Complete online shopping platform with payment integration",
            deadline=deadline,
            category_id=category.id
        )
        
        print(f"✅ Created project: {project.name}")
        print(f"📅 Deadline: {project.deadline}")
        print(f"🏷️  Category: {category.name}")
        print(f"📊 Days until deadline: {project.days_until_deadline()}")
        print(f"🔢 Total stages: {len(project.stages)}")
        
        # Show all stages and their default tasks
        print(f"\nProject stages and default tasks:")
        for i, stage in enumerate(project.stages, 1):
            print(f"  {i}. {stage.name} ({stage.status.value})")
            print(f"     Default tasks: {len(stage.tasks)}")
            for task in stage.tasks:
                print(f"       - {task.name} ({task.status.value})")
        
        # Project is automatically saved during creation, but notify about web update
        self.save_and_notify_web(f"Created project '{project.name}' with {len(project.stages)} stages")
        
        self.demo_project = project
        self.show_web_links(project.id)
        self.prompt_web_check(f"Project '{project.name}' created! Check the Dashboard and Project Details.")
        
        return project
    
    def step_3_complete_planning_stage(self, project):
        """Step 3: Complete Planning stage with custom tasks"""
        print(f"\n📋 STEP 3: Planning Stage Execution")
        print("=" * 60)
        
        current_stage = project.get_current_stage()
        print(f"Current stage: {current_stage.name}")
        print(f"Stage status: {current_stage.status.value}")
        
        # Add some custom tasks to planning
        custom_tasks = [
            Task("Market research", "Analyze competitors and market", "Research Team"),
            Task("Technical architecture", "Design system architecture", "Tech Lead"),
            Task("Budget planning", "Calculate project costs", "Project Manager")
        ]
        
        print(f"\nAdding {len(custom_tasks)} custom tasks to planning stage...")
        for task in custom_tasks:
            current_stage.add_task(task)
            print(f"  ➕ Added: {task.name}")
        
        # Save after adding custom tasks
        self.save_and_notify_web(f"Added {len(custom_tasks)} custom tasks to Planning stage")
        self.show_web_links(project.id)
        self.prompt_web_check("Custom tasks added! Check the Project Details page.")
        
        # Complete all tasks (default + custom)
        print(f"\nCompleting all tasks in {current_stage.name} stage...")
        for i, task in enumerate(current_stage.tasks, 1):
            print(f"  🔄 Completing task {i}/{len(current_stage.tasks)}: {task.name}")
            task.complete()
            
            # Save after every few tasks to show real-time progress
            if i % 2 == 0 or i == len(current_stage.tasks):
                self.save_and_notify_web(f"Completed {i}/{len(current_stage.tasks)} tasks in Planning")
            
            time.sleep(0.5)  # Simulate work time
        
        print(f"✅ All tasks completed in {current_stage.name}")
        print(f"📊 Stage progress: {current_stage.get_progress():.1%}")
        
        # Advance to next stage
        success, message = project.advance_to_next_stage()
        print(f"🚀 Stage advancement: {message}")
        
        # Save after stage advancement
        self.save_and_notify_web(f"Completed Planning stage and advanced to {project.get_current_stage().name}")
        self.show_web_links(project.id)
        self.prompt_web_check("Planning stage completed! Check the progress on Project Details.")
        
        return project
    
    def step_4_complete_remaining_stages(self, project):
        """Step 4: Complete all remaining stages automatically"""
        print(f"\n⚡ STEP 4: Complete All Remaining Stages")
        print("=" * 60)
        
        stage_count = 1
        while True:
            current_stage = project.get_current_stage()
            if not current_stage:
                print("🎉 All stages completed! Project is finished.")
                break
            
            print(f"\n--- Processing Stage {stage_count}: {current_stage.name} ---")
            print(f"Stage status: {current_stage.status.value}")
            print(f"Tasks in stage: {len(current_stage.tasks)}")
            
            # Add stage-specific custom tasks based on stage type
            custom_tasks = self._get_stage_specific_tasks(current_stage.name)
            if custom_tasks:
                print(f"Adding {len(custom_tasks)} stage-specific tasks...")
                for task in custom_tasks:
                    current_stage.add_task(task)
                    print(f"  ➕ {task.name}")
                
                # Save after adding stage-specific tasks
                self.save_and_notify_web(f"Added {len(custom_tasks)} tasks to {current_stage.name} stage")
            
            # Show web interface before starting task completion
            self.show_web_links(project.id)
            self.prompt_web_check(f"Starting {current_stage.name} stage. Check current status in web interface.")
            
            # Complete all tasks in current stage
            incomplete_tasks = [t for t in current_stage.tasks if t.status != TaskStatus.COMPLETED]
            print(f"\nCompleting {len(incomplete_tasks)} tasks...")
            
            for i, task in enumerate(incomplete_tasks, 1):
                print(f"  🔄 [{i}/{len(incomplete_tasks)}] {task.name}")
                task.complete()
                
                # Save progress every 2 tasks or at the end
                if i % 2 == 0 or i == len(incomplete_tasks):
                    self.save_and_notify_web(f"{current_stage.name}: {i}/{len(incomplete_tasks)} tasks completed")
                
                time.sleep(0.3)  # Simulate work
            
            print(f"✅ Stage {current_stage.name} completed ({current_stage.get_progress():.1%})")
            
            # Advance to next stage
            success, message = project.advance_to_next_stage()
            print(f"🚀 {message}")
            
            # Save after stage advancement
            if success:
                next_stage = project.get_current_stage()
                next_stage_name = next_stage.name if next_stage else "PROJECT COMPLETED"
                self.save_and_notify_web(f"Completed {current_stage.name} stage, advanced to {next_stage_name}")
                
                # Show progress after each stage
                self.show_web_links(project.id)
                self.prompt_web_check(f"Stage {current_stage.name} completed! Check the updated progress.")
            else:
                self.save_and_notify_web(f"Project completed after {current_stage.name} stage")
                break
                
            stage_count += 1
        
        return project
    
    def _get_stage_specific_tasks(self, stage_name):
        """Get custom tasks specific to each stage type"""
        stage_tasks = {
            "Design": [
                Task("User experience design", "Create user journey maps", "UX Designer"),
                Task("Database design", "Design database schema", "Database Architect")
            ],
            "Development": [
                Task("Frontend development", "Build React components", "Frontend Dev"),
                Task("Backend API", "Develop REST API endpoints", "Backend Dev"),
                Task("Database setup", "Configure production database", "DevOps")
            ],
            "Testing": [
                Task("Integration testing", "Test API integrations", "QA Engineer"),
                Task("Performance testing", "Load testing with 1000 users", "QA Engineer")
            ],
            "Deployment": [
                Task("CI/CD setup", "Configure deployment pipeline", "DevOps"),
                Task("Security audit", "Penetration testing", "Security Team")
            ],
            "Launch": [
                Task("Marketing campaign", "Launch product marketing", "Marketing Team"),
                Task("Customer support setup", "Train support team", "Support Manager")
            ]
        }
        return stage_tasks.get(stage_name, [])
    
    def step_5_project_completion_verification(self, project):
        """Step 5: Verify project completion and generate final report"""
        print(f"\n🏆 STEP 5: Project Completion Verification")
        print("=" * 60)
        
        # Final save to ensure all data is persisted
        self.save_and_notify_web("Final project data saved")
        
        # Check if project is truly completed
        print(f"Project: {project.name}")
        print(f"Completion status: {project.is_completed()}")
        print(f"Completed at: {project.completed_at}")
        
        if project.is_completed():
            print("✅ PROJECT SUCCESSFULLY COMPLETED!")
        else:
            print("⚠️  Project not yet completed")
        
        # Generate detailed completion report
        print(f"\n📊 FINAL PROJECT REPORT:")
        print("-" * 40)
        
        summary = project.get_project_summary()
        print(f"Overall Progress: {summary['overall_progress']:.1%}")
        print(f"Total Stages: {summary['total_stages']}")
        print(f"Completed Stages: {summary['completed_stages']}")
        print(f"Total Tasks: {summary['total_tasks']}")
        print(f"Completed Tasks: {summary['completed_tasks']}")
        
        # Show stage-by-stage breakdown
        print(f"\n📋 STAGE-BY-STAGE BREAKDOWN:")
        for i, stage in enumerate(project.stages, 1):
            completed_tasks = len([t for t in stage.tasks if t.status == TaskStatus.COMPLETED])
            total_tasks = len(stage.tasks)
            status_icon = "✅" if stage.status == StageStatus.COMPLETED else "🔄" if stage.status == StageStatus.IN_PROGRESS else "⏸️"
            
            print(f"  {status_icon} Stage {i}: {stage.name}")
            print(f"    Status: {stage.status.value}")
            print(f"    Tasks: {completed_tasks}/{total_tasks} completed")
            print(f"    Progress: {stage.get_progress():.1%}")
        
        # Project timeline
        print(f"\n📅 PROJECT TIMELINE:")
        print(f"  Created: {project.created_at}")
        print(f"  Deadline: {project.deadline}")
        print(f"  Completed: {project.completed_at}")
        
        if project.deadline and project.completed_at:
            # Calculate if completed on time
            try:
                deadline_dt = datetime.fromisoformat(project.deadline.replace('Z', '+00:00'))
                completed_dt = datetime.fromisoformat(project.completed_at.replace('Z', '+00:00'))
                if completed_dt <= deadline_dt:
                    print(f"  ✅ Completed ON TIME!")
                else:
                    print(f"  ⚠️  Completed LATE")
            except:
                print(f"  📅 Timeline comparison unavailable")
        
        # Show final web interface links
        self.show_web_links(project.id)
        self.prompt_web_check("Project completed! Check the final status in web interface.")
        
        return project
    
    def step_6_global_summary_and_cleanup(self):
        """Step 6: Generate global summary and save data"""
        print(f"\n🌍 STEP 6: Global Summary and Data Persistence")
        print("=" * 60)
        
        # Final save to ensure everything is persisted
        self.save_and_notify_web("Final system data saved")
        
        # Get global summary
        global_summary = self.pm.get_global_summary()
        
        print(f"SYSTEM-WIDE SUMMARY:")
        print(f"  Total Projects: {global_summary['total_projects']}")
        print(f"  Active Projects: {global_summary['active_projects']}")
        print(f"  Completed Projects: {global_summary['completed_projects']}")
        print(f"  Total Stages: {global_summary['total_stages']}")
        print(f"  Completed Stages: {global_summary['completed_stages']}")
        print(f"  Total Tasks: {global_summary['total_tasks']}")
        print(f"  Completed Tasks: {global_summary['completed_tasks']}")
        print(f"  Overall Progress: {global_summary['overall_progress']:.1%}")
        
        # List all projects and their status
        print(f"\n📋 ALL PROJECTS STATUS:")
        all_projects = self.pm.list_projects()
        for i, project in enumerate(all_projects, 1):
            status_icon = "✅" if project.is_completed() else "🔄"
            current_stage = project.get_current_stage()
            current_stage_name = current_stage.name if current_stage else "COMPLETED"
            
            print(f"  {status_icon} {i}. {project.name}")
            print(f"     Current stage: {current_stage_name}")
            print(f"     Progress: {project.get_project_summary()['overall_progress']:.1%}")
            
            # Show category if assigned
            if project.category_id:
                category = self.pm.get_category(project.category_id)
                if category:
                    print(f"     Category: {category.name}")
        
        # Show categories
        print(f"\n📁 PROJECT CATEGORIES:")
        categories = self.pm.list_categories()
        for category in categories:
            projects_in_category = [p for p in all_projects if p.category_id == category.id]
            print(f"  🏷️  {category.name}: {len(projects_in_category)} projects")
        
        # Final web interface summary
        self.show_web_links()
        print(f"\n🎉 DEMO COMPLETE! All data has been saved and is available in the web interface.")
        self.prompt_web_check("Check the Summary page to see the complete system overview!")
        
        return global_summary
    
    def run_complete_lifecycle_demo(self):
        """Run the complete project lifecycle demo from start to finish"""
        print("🎆 COMPLETE PROJECT LIFECYCLE AUTOMATION DEMO")
        print("=" * 80)
        print("This demo shows the entire project lifecycle with real-time web updates.\n")
        
        print("🌐 Web Interface: http://localhost:8083")
        print("🔄 Tip: Keep your browser open and refresh to see real-time updates!\n")
        
        try:
            # Step 1: Environment setup
            web_category, mobile_category = self.step_1_setup_environment()
            
            # Step 2: Project creation
            project = self.step_2_create_project(web_category)
            
            # Step 3: Complete planning stage
            project = self.step_3_complete_planning_stage(project)
            
            # Step 4: Complete all remaining stages
            project = self.step_4_complete_remaining_stages(project)
            
            # Step 5: Project completion verification
            project = self.step_5_project_completion_verification(project)
            
            # Step 6: Global summary and cleanup
            global_summary = self.step_6_global_summary_and_cleanup()
            
            # Final success message
            print(f"\n🎉 LIFECYCLE DEMO COMPLETED SUCCESSFULLY!")
            print(f"\n🔗 Final Results - View in Web Interface:")
            print(f"  • Dashboard: {self.web_base_url}")
            print(f"  • Project Details: {self.web_base_url}/project/{project.id}")
            print(f"  • Summary: {self.web_base_url}/summary")
            print(f"  • Categories: {self.web_base_url}/categories")
            
            print(f"\n💾 All data has been saved to: {self.pm.data_file}")
            print(f"🌐 The web interface shows the complete project lifecycle results!")
            
            # Optional: open browser to final results
            final_choice = input("\n🌐 Open browser to view final results? (y/n): ").lower().strip()
            if final_choice in ['y', 'yes']:
                try:
                    webbrowser.open(f"{self.web_base_url}/summary")
                    print("🌐 Browser opened to Summary page!")
                except:
                    print("⚠️  Could not open browser automatically")
            
            return project
            
        except KeyboardInterrupt:
            print(f"\n\n🚨 Demo interrupted by user")
            print(f"Saving any changes made so far...")
            self.pm.save_data()
            return None
        except Exception as e:
            print(f"\n\n❌ Error during demo: {e}")
            print(f"Saving any changes made so far...")
            self.pm.save_data()
            return None
    

def start_web_server_instruction():
    """Show instructions for starting the web server"""
    print("🌐 WEB INTERFACE SETUP REQUIRED")
    print("=" * 50)
    print("For the best experience, start the web interface in a separate terminal:")
    print("")
    print("1. Open a new terminal window/tab")
    print("2. Navigate to this directory")
    print("3. Run: python3 web_app.py")
    print("4. Open http://localhost:8083 in your browser")
    print("5. Return to this terminal to continue the demo")
    print("")
    print("📝 The automation will save data after each action,")
    print("   so you can refresh the browser to see real-time updates!")
    print("")
    
    choice = input("🚀 Ready to continue? (y/n): ").lower().strip()
    return choice in ['y', 'yes']

def main():
    """Main entry point for the complete project lifecycle demo"""
    print("🚀 Welcome to the Complete Project Lifecycle Demo!")
    print("\nThis demo demonstrates real-time web interface updates during automation.")
    print("\nDemo steps:")
    print("  1. 🏢 Environment setup (categories, templates)")
    print("  2. 🎆 Project creation with deadlines")
    print("  3. 📋 Planning stage completion")
    print("  4. ⚡ All remaining stages completion")
    print("  5. 🏆 Project completion verification")
    print("  6. 🌍 Global summary and data persistence")
    print("\n💾 The demo saves data after each action for real-time web updates.")
    print("🔄 You can refresh your browser at any time to see the latest changes.")
    
    # Check if user wants to start web server
    if not start_web_server_instruction():
        print("👋 Demo cancelled. Goodbye!")
        return
    
    demo = ProjectLifecycleDemo()
    demo.run_complete_lifecycle_demo()

if __name__ == "__main__":
    main()