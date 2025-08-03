#!/usr/bin/env python3
"""
Test script for the notification system
Demonstrates email and SMS notification features
"""

from notification_system import get_notification_system
from project_manager import ProjectManager
from datetime import datetime, timedelta
import json

def main():
    print("🔔 NOTIFICATION SYSTEM TEST")
    print("=" * 50)
    
    # Get notification system
    ns = get_notification_system()
    
    print("📋 Current Configuration:")
    config = ns.config
    print(f"  Email: {config['email']['address']} ({'Enabled' if config['email']['enabled'] else 'Disabled'})")
    print(f"  SMS: {config['sms']['phone']} ({'Enabled' if config['sms']['enabled'] else 'Disabled'})")
    print()
    
    # Demo configuration (you can modify these)
    demo_settings = {
        'email': 'your-email@example.com',  # Replace with your email
        'phone': '+1234567890',             # Replace with your phone number
        'emailEnabled': True,
        'smsEnabled': False,  # Set to True to test SMS (uses free TextBelt service)
        'notifyDeadlines': True,
        'notifyCompletion': True,
        'notifyErrors': True
    }
    
    print("🛠️  CONFIGURATION SETUP")
    print("-" * 30)
    print("To test notifications, you need to configure:")
    print("1. Email settings (Gmail recommended)")
    print("2. SMTP credentials in notification_config.json")
    print("3. Optionally, phone number for SMS")
    print()
    
    # Show example configuration
    print("📄 Example configuration file (notification_config.json):")
    example_config = {
        "email": {
            "address": "your-email@example.com",
            "enabled": True
        },
        "sms": {
            "phone": "+1234567890",
            "enabled": False
        },
        "preferences": {
            "notify_deadlines": True,
            "notify_completion": True,
            "notify_errors": True,
            "deadline_warning_days": 3
        },
        "smtp": {
            "server": "smtp.gmail.com",
            "port": 587,
            "username": "your-email@gmail.com",
            "password": "your-app-specific-password",
            "use_tls": True
        }
    }
    
    print(json.dumps(example_config, indent=2))
    print()
    
    print("📧 GMAIL SETUP INSTRUCTIONS:")
    print("-" * 30)
    print("1. Enable 2-factor authentication on your Gmail account")
    print("2. Generate an app-specific password:")
    print("   - Go to: https://myaccount.google.com/apppasswords")
    print("   - Select 'Mail' and 'Other (custom name)'")
    print("   - Enter 'Project Manager' as the name")
    print("   - Use the generated password in the config file")
    print("3. Update notification_config.json with your credentials")
    print()
    
    # Test different notification types
    print("🧪 NOTIFICATION EXAMPLES")
    print("-" * 30)
    
    # Update settings for demo
    choice = input("Would you like to configure notifications for testing? (y/N): ").lower().strip()
    if choice == 'y':
        email = input("Enter your email address: ").strip()
        if email:
            demo_settings['email'] = email
            print("✅ Email configured")
        
        phone = input("Enter your phone number (optional, +1234567890): ").strip()
        if phone:
            demo_settings['phone'] = phone
            demo_settings['smsEnabled'] = True
            print("✅ SMS configured")
        
        # Update settings
        ns.update_settings(demo_settings)
        print("💾 Settings saved!")
        print()
    
    # Test notifications
    print("🔔 TESTING NOTIFICATIONS")
    print("-" * 30)
    
    # Test 1: System test
    print("1. Running system test...")
    test_results = ns.test_notifications()
    print(f"   Email test: {'✅ PASS' if test_results['email'] else '❌ FAIL'}")
    print(f"   SMS test: {'✅ PASS' if test_results['sms'] else '❌ FAIL'}")
    if test_results['errors']:
        print(f"   Errors: {', '.join(test_results['errors'])}")
    print()
    
    # Test 2: Deadline notification
    print("2. Testing deadline notification...")
    ns.notify_deadline_approaching(
        "Demo Project",
        (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d"),
        2
    )
    print("   ✅ Deadline notification sent")
    print()
    
    # Test 3: Completion notification
    print("3. Testing completion notification...")
    ns.notify_project_completed(
        "Demo Project",
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )
    print("   ✅ Completion notification sent")
    print()
    
    # Test 4: Error notification
    print("4. Testing error notification...")
    ns.notify_system_error(
        "Test Error",
        "This is a test error notification from the Project Manager system",
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )
    print("   ✅ Error notification sent")
    print()
    
    # Test 5: Deadline checking
    print("5. Testing deadline checking with real projects...")
    pm = ProjectManager()
    projects = pm.list_projects()
    
    # Add deadlines to some projects for testing
    test_projects = projects[:3] if projects else []
    for i, project in enumerate(test_projects):
        # Set deadline in 1-5 days
        project.deadline = (datetime.now() + timedelta(days=i+1)).isoformat()
    
    if test_projects:
        pm.save_data()
        ns.check_deadlines(projects)
        print(f"   ✅ Checked {len(projects)} projects for deadlines")
    else:
        print("   ℹ️  No projects found to check")
    print()
    
    print("🎉 NOTIFICATION TESTING COMPLETE!")
    print()
    print("📱 NEXT STEPS:")
    print("- Check your email for test notifications")
    print("- Check your phone for SMS (if enabled)")
    print("- Configure SMTP settings for production use")
    print("- Set up deadline monitoring in your projects")
    print()
    print("🌐 Access the web interface notification settings at:")
    print("   http://localhost:8083 → Click 'Notifications' button")

if __name__ == "__main__":
    main()