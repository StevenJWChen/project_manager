#!/usr/bin/env python3
"""
Complete automation setup that starts both web interface and automation demo
This script helps you run the complete lifecycle demo with real-time web updates.
"""
import subprocess
import sys
import time
import webbrowser
from threading import Thread
import signal
import os

class AutomationWithWebDemo:
    def __init__(self):
        self.web_process = None
        self.web_started = False
    
    def start_web_server(self):
        """Start the web server in background"""
        try:
            print("🌐 Starting web server...")
            self.web_process = subprocess.Popen(
                [sys.executable, "web_app.py"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            # Wait a moment for server to start
            time.sleep(3)
            
            # Check if process is still running
            if self.web_process.poll() is None:
                self.web_started = True
                print("✅ Web server started successfully!")
                print("🌐 Web interface available at: http://localhost:8083")
                return True
            else:
                print("❌ Failed to start web server")
                return False
                
        except Exception as e:
            print(f"❌ Error starting web server: {e}")
            return False
    
    def open_browser(self):
        """Open browser to web interface"""
        try:
            print("🌐 Opening browser...")
            webbrowser.open("http://localhost:8083")
            time.sleep(1)
            print("✅ Browser opened!")
        except Exception as e:
            print(f"⚠️  Could not open browser: {e}")
    
    def run_automation_demo(self):
        """Run the automation demo"""
        try:
            print("\n🤖 Starting automation demo...")
            print("=" * 50)
            
            # Import and run the demo
            from automation_demo import ProjectLifecycleDemo
            
            demo = ProjectLifecycleDemo()
            demo.auto_open_browser = False  # We'll handle browser opening
            
            print("🚀 Running complete project lifecycle automation...")
            print("🔄 The web interface will update automatically as the demo progresses.")
            print("\nNote: You can refresh your browser at any time to see the latest updates!")
            
            # Run the demo
            project = demo.run_complete_lifecycle_demo()
            
            if project:
                print("\n🎉 AUTOMATION DEMO COMPLETED SUCCESSFULLY!")
                print(f"✅ Project '{project.name}' completed through full lifecycle")
                print("🌐 Check the web interface for complete results!")
            else:
                print("\n⚠️  Demo ended early or encountered issues")
                
        except Exception as e:
            print(f"\n❌ Error during automation demo: {e}")
    
    def cleanup(self):
        """Clean up background processes"""
        if self.web_process and self.web_process.poll() is None:
            print("\n🛑 Stopping web server...")
            self.web_process.terminate()
            try:
                self.web_process.wait(timeout=5)
                print("✅ Web server stopped")
            except subprocess.TimeoutExpired:
                print("⚠️  Force killing web server...")
                self.web_process.kill()
    
    def signal_handler(self, signum, frame):
        """Handle Ctrl+C gracefully"""
        print(f"\n\n🛑 Received interrupt signal")
        self.cleanup()
        sys.exit(0)
    
    def run_complete_setup(self):
        """Run the complete setup with web server and automation"""
        print("🚀 COMPLETE PROJECT LIFECYCLE AUTOMATION WITH WEB INTERFACE")
        print("=" * 70)
        print("This will:")
        print("  1. 🌐 Start the web server (http://localhost:8083)")
        print("  2. 🌐 Open your browser to the dashboard")
        print("  3. 🤖 Run the complete automation demo")
        print("  4. 🔄 Update the web interface in real-time")
        print("  5. 🛑 Clean up when finished")
        
        choice = input("\n🚀 Ready to start the complete demo? (y/n): ").lower().strip()
        if choice not in ['y', 'yes']:
            print("👋 Demo cancelled. Goodbye!")
            return
        
        # Set up signal handler for graceful shutdown
        signal.signal(signal.SIGINT, self.signal_handler)
        
        try:
            # Step 1: Start web server
            if not self.start_web_server():
                print("❌ Cannot continue without web server")
                return
            
            # Step 2: Open browser
            time.sleep(1)
            self.open_browser()
            
            # Step 3: Wait for user to check browser
            input("\n📍 Press Enter when you can see the web interface in your browser...")
            
            # Step 4: Run automation demo
            self.run_automation_demo()
            
            # Step 5: Keep web server running for final review
            print(f"\n🌐 Web server is still running at: http://localhost:8083")
            print("📊 You can continue exploring the web interface.")
            input("Press Enter to stop the web server and exit...")
            
        except KeyboardInterrupt:
            print(f"\n🛑 Demo interrupted")
        except Exception as e:
            print(f"\n❌ Unexpected error: {e}")
        finally:
            self.cleanup()

def main():
    """Main entry point"""
    demo = AutomationWithWebDemo()
    demo.run_complete_setup()

if __name__ == "__main__":
    main()