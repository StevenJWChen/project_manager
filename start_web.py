#!/usr/bin/env python3
"""
Startup script for the Project Management Web Interface
"""
import subprocess
import sys
import webbrowser
import time

def main():
    print("🚀 Starting Project Management System Web Interface...")
    
    try:
        # Start the Flask app
        print("📱 Starting web server on http://localhost:8080")
        
        # Open browser after a short delay
        def open_browser():
            time.sleep(2)
            webbrowser.open('http://localhost:8080')
        
        import threading
        browser_thread = threading.Thread(target=open_browser)
        browser_thread.daemon = True
        browser_thread.start()
        
        # Import and run the Flask app
        from web_app import app
        app.run(debug=False, host='0.0.0.0', port=8080)
        
    except KeyboardInterrupt:
        print("\n👋 Shutting down web server...")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Error starting web server: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()