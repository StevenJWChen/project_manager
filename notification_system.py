#!/usr/bin/env python3
"""
Email and SMS Notification System for Project Manager
Handles notifications for deadlines, completions, and system issues
"""

import json
import os
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional

# Import email modules with fallback
try:
    import smtplib
    from email.mime.text import MimeText
    from email.mime.multipart import MimeMultipart
    EMAIL_AVAILABLE = True
except ImportError:
    EMAIL_AVAILABLE = False
    print("Email functionality not available - install email dependencies")

# Import requests with fallback
try:
    import requests
    SMS_AVAILABLE = True
except ImportError:
    SMS_AVAILABLE = False
    print("SMS functionality not available - install requests library")

class NotificationSystem:
    def __init__(self, config_file="notification_config.json"):
        self.config_file = config_file
        self.config = self.load_config()
        self.logger = logging.getLogger(__name__)
        
    def load_config(self) -> Dict:
        """Load notification configuration from file"""
        default_config = {
            "email": {
                "address": "",
                "enabled": False
            },
            "sms": {
                "phone": "",
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
                "username": "",
                "password": "",  # Use app-specific password for Gmail
                "use_tls": True
            },
            "sms_service": {
                "provider": "textbelt",  # Free SMS service
                "api_key": "textbelt"    # Default free key
            }
        }
        
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    loaded_config = json.load(f)
                    # Merge with defaults
                    default_config.update(loaded_config)
            except Exception as e:
                self.logger.error(f"Error loading config: {e}")
        
        return default_config
    
    def save_config(self):
        """Save configuration to file"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
        except Exception as e:
            self.logger.error(f"Error saving config: {e}")
    
    def update_settings(self, settings: Dict):
        """Update notification settings"""
        try:
            if 'email' in settings:
                self.config['email']['address'] = settings['email']
                self.config['email']['enabled'] = bool(settings.get('emailEnabled', False))
            
            if 'phone' in settings:
                self.config['sms']['phone'] = settings['phone']
                self.config['sms']['enabled'] = bool(settings.get('smsEnabled', False))
            
            # Update preferences
            prefs = self.config['preferences']
            prefs['notify_deadlines'] = settings.get('notifyDeadlines', True)
            prefs['notify_completion'] = settings.get('notifyCompletion', True)
            prefs['notify_errors'] = settings.get('notifyErrors', True)
            
            self.save_config()
            return True
        except Exception as e:
            self.logger.error(f"Error updating settings: {e}")
            return False
    
    def send_email(self, subject: str, body: str, html_body: str = None) -> bool:
        """Send email notification"""
        if not EMAIL_AVAILABLE:
            self.logger.warning("Email not available - skipping email notification")
            return False
            
        if not self.config['email']['enabled'] or not self.config['email']['address']:
            return False
        
        try:
            # Create message
            msg = MimeMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = self.config['smtp']['username']
            msg['To'] = self.config['email']['address']
            
            # Add plain text part
            text_part = MimeText(body, 'plain')
            msg.attach(text_part)
            
            # Add HTML part if provided
            if html_body:
                html_part = MimeText(html_body, 'html')
                msg.attach(html_part)
            
            # Send email
            with smtplib.SMTP(self.config['smtp']['server'], self.config['smtp']['port']) as server:
                if self.config['smtp']['use_tls']:
                    server.starttls()
                
                if self.config['smtp']['username'] and self.config['smtp']['password']:
                    server.login(self.config['smtp']['username'], self.config['smtp']['password'])
                
                server.send_message(msg)
            
            self.logger.info(f"Email sent successfully: {subject}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error sending email: {e}")
            return False
    
    def send_sms(self, message: str) -> bool:
        """Send SMS notification using TextBelt service"""
        if not SMS_AVAILABLE:
            self.logger.warning("SMS not available - skipping SMS notification")
            return False
            
        if not self.config['sms']['enabled'] or not self.config['sms']['phone']:
            return False
        
        try:
            # Use TextBelt free SMS service
            url = "https://textbelt.com/text"
            data = {
                'phone': self.config['sms']['phone'],
                'message': message,
                'key': self.config['sms_service']['api_key']
            }
            
            response = requests.post(url, data=data, timeout=10)
            result = response.json()
            
            if result.get('success'):
                self.logger.info("SMS sent successfully")
                return True
            else:
                self.logger.error(f"SMS failed: {result.get('error', 'Unknown error')}")
                return False
                
        except Exception as e:
            self.logger.error(f"Error sending SMS: {e}")
            return False
    
    def notify_deadline_approaching(self, project_name: str, deadline: str, days_left: int):
        """Send notification for approaching deadline"""
        if not self.config['preferences']['notify_deadlines']:
            return
        
        subject = f"⏰ Project Deadline Approaching: {project_name}"
        
        body = f"""
Project Manager Notification

Project: {project_name}
Deadline: {deadline}
Days remaining: {days_left}

Please ensure all tasks are completed on time.

---
Project Manager System
"""
        
        html_body = f"""
<html>
<body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
    <div style="background: linear-gradient(135deg, #f59e0b, #d97706); color: white; padding: 20px; text-align: center;">
        <h2>⏰ Deadline Approaching</h2>
    </div>
    <div style="padding: 20px; background: #f8f9fa;">
        <h3>Project: {project_name}</h3>
        <p><strong>Deadline:</strong> {deadline}</p>
        <p><strong>Days remaining:</strong> <span style="color: #f59e0b; font-weight: bold;">{days_left}</span></p>
        <p>Please ensure all tasks are completed on time.</p>
        <div style="text-align: center; margin-top: 20px;">
            <a href="http://localhost:8083" style="background: #4f46e5; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">View Project</a>
        </div>
    </div>
    <div style="text-align: center; padding: 10px; color: #6b7280; font-size: 12px;">
        Project Manager System
    </div>
</body>
</html>
"""
        
        sms_message = f"Project Manager Alert: {project_name} deadline in {days_left} days ({deadline})"
        
        self.send_email(subject, body, html_body)
        self.send_sms(sms_message)
    
    def notify_project_completed(self, project_name: str, completion_date: str):
        """Send notification for project completion"""
        if not self.config['preferences']['notify_completion']:
            return
        
        subject = f"🎉 Project Completed: {project_name}"
        
        body = f"""
Project Manager Notification

Congratulations! The following project has been completed:

Project: {project_name}
Completed: {completion_date}

Great work on finishing this project!

---
Project Manager System
"""
        
        html_body = f"""
<html>
<body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
    <div style="background: linear-gradient(135deg, #10b981, #059669); color: white; padding: 20px; text-align: center;">
        <h2>🎉 Project Completed!</h2>
    </div>
    <div style="padding: 20px; background: #f8f9fa;">
        <h3>Congratulations!</h3>
        <p>The following project has been completed:</p>
        <p><strong>Project:</strong> {project_name}</p>
        <p><strong>Completed:</strong> {completion_date}</p>
        <p>Great work on finishing this project!</p>
        <div style="text-align: center; margin-top: 20px;">
            <a href="http://localhost:8083/summary" style="background: #10b981; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">View Summary</a>
        </div>
    </div>
    <div style="text-align: center; padding: 10px; color: #6b7280; font-size: 12px;">
        Project Manager System
    </div>
</body>
</html>
"""
        
        sms_message = f"Project Manager: {project_name} completed successfully! 🎉"
        
        self.send_email(subject, body, html_body)
        self.send_sms(sms_message)
    
    def notify_system_error(self, error_type: str, error_message: str, timestamp: str):
        """Send notification for system errors"""
        if not self.config['preferences']['notify_errors']:
            return
        
        subject = f"🚨 System Error: {error_type}"
        
        body = f"""
Project Manager System Error

Error Type: {error_type}
Time: {timestamp}
Message: {error_message}

Please check the system and resolve any issues.

---
Project Manager System
"""
        
        html_body = f"""
<html>
<body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
    <div style="background: linear-gradient(135deg, #ef4444, #dc2626); color: white; padding: 20px; text-align: center;">
        <h2>🚨 System Error</h2>
    </div>
    <div style="padding: 20px; background: #f8f9fa;">
        <h3>Error Details</h3>
        <p><strong>Type:</strong> {error_type}</p>
        <p><strong>Time:</strong> {timestamp}</p>
        <p><strong>Message:</strong> {error_message}</p>
        <p style="color: #ef4444;">Please check the system and resolve any issues.</p>
        <div style="text-align: center; margin-top: 20px;">
            <a href="http://localhost:8083" style="background: #ef4444; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">Check System</a>
        </div>
    </div>
    <div style="text-align: center; padding: 10px; color: #6b7280; font-size: 12px;">
        Project Manager System
    </div>
</body>
</html>
"""
        
        sms_message = f"Project Manager Error: {error_type} at {timestamp}"
        
        self.send_email(subject, body, html_body)
        self.send_sms(sms_message)
    
    def check_deadlines(self, projects: List):
        """Check for approaching deadlines and send notifications"""
        if not self.config['preferences']['notify_deadlines']:
            return
        
        warning_days = self.config['preferences'].get('deadline_warning_days', 3)
        today = datetime.now()
        
        for project in projects:
            if not project.deadline:
                continue
            
            try:
                deadline_date = datetime.fromisoformat(project.deadline.replace('Z', '+00:00'))
                days_left = (deadline_date - today).days
                
                if 0 <= days_left <= warning_days:
                    self.notify_deadline_approaching(
                        project.name,
                        project.deadline,
                        days_left
                    )
            except Exception as e:
                self.logger.error(f"Error checking deadline for {project.name}: {e}")
    
    def test_notifications(self) -> Dict:
        """Test notification system"""
        results = {
            'email': False,
            'sms': False,
            'errors': []
        }
        
        # Test email
        if self.config['email']['enabled']:
            try:
                email_success = self.send_email(
                    "Test Email from Project Manager",
                    "This is a test email to verify your notification settings are working correctly.",
                    """
<html>
<body style="font-family: Arial, sans-serif;">
    <h3>🧪 Test Email</h3>
    <p>This is a test email to verify your notification settings are working correctly.</p>
    <p style="color: #10b981;">✅ Email notifications are working!</p>
</body>
</html>
"""
                )
                results['email'] = email_success
                if not email_success:
                    results['errors'].append("Email test failed")
            except Exception as e:
                results['errors'].append(f"Email error: {str(e)}")
        
        # Test SMS
        if self.config['sms']['enabled']:
            try:
                sms_success = self.send_sms("Test message from Project Manager. SMS notifications are working!")
                results['sms'] = sms_success
                if not sms_success:
                    results['errors'].append("SMS test failed")
            except Exception as e:
                results['errors'].append(f"SMS error: {str(e)}")
        
        return results

# Singleton instance
notification_system = NotificationSystem()

def get_notification_system():
    """Get the global notification system instance"""
    return notification_system