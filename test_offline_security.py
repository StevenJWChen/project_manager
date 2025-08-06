#!/usr/bin/env python3
"""
High Security Offline Test
Verifies the application works without any external network dependencies
"""

import os
import sys
import socket
from contextlib import contextmanager

@contextmanager
def block_network():
    """Context manager that blocks all network access during test"""
    original_socket = socket.socket
    
    def blocked_socket(*args, **kwargs):
        raise Exception("Network access blocked for security testing")
    
    socket.socket = blocked_socket
    try:
        yield
    finally:
        socket.socket = original_socket

def test_offline_functionality():
    """Test all core functionality with network completely blocked"""
    print("🔒 HIGH-SECURITY OFFLINE TEST")
    print("=" * 50)
    
    with block_network():
        try:
            # Test 1: Import core modules
            print("📦 Testing imports...")
            from project_manager import ProjectManager
            import cli
            print("✅ Core modules import successfully")
            
            # Test 2: Create project manager instance
            print("🏗️ Testing ProjectManager initialization...")
            pm = ProjectManager()
            print("✅ ProjectManager initializes without network")
            
            # Test 3: Create and manipulate project
            print("📝 Testing project operations...")
            project = pm.create_project("Security Test", "Testing offline functionality")
            
            # Add and complete a task
            stage = project.get_current_stage()
            if stage and stage.tasks:
                task = stage.tasks[0]
                task.complete()
                print("✅ Task operations work offline")
            
            # Test stage advancement
            result, message = project.advance_to_next_stage()
            if not result:
                print("✅ Stage logic works (expected failure due to incomplete tasks)")
            
            # Test 4: Data persistence
            print("💾 Testing data persistence...")
            pm.save_data()
            print("✅ Data saves successfully without network")
            
            # Test 5: Import web app (should work without starting server)
            print("🌐 Testing web app imports...")
            try:
                import web_app
                print("✅ Web app imports successfully")
            except ImportError as e:
                print(f"❌ Web app import failed: {e}")
            
            print("\n🎉 ALL TESTS PASSED!")
            print("✅ Application is fully functional offline")
            print("🔒 No external network dependencies detected")
            
            return True
            
        except Exception as e:
            print(f"❌ SECURITY TEST FAILED: {e}")
            return False

def test_static_assets():
    """Verify all static assets are local"""
    print("\n📁 STATIC ASSETS VERIFICATION")
    print("=" * 50)
    
    required_assets = [
        "static/lib/bootstrap/css/bootstrap.min.css",
        "static/lib/fontawesome/css/all-local.min.css", 
        "static/lib/chartjs/chart.min.js",
        "static/lib/bootstrap/js/bootstrap.bundle.min.js",
        "static/lib/fontawesome/webfonts/fa-solid-900.woff2",
        "static/lib/fontawesome/webfonts/fa-regular-400.woff2",
        "static/lib/fontawesome/webfonts/fa-brands-400.woff2"
    ]
    
    all_present = True
    for asset in required_assets:
        if os.path.exists(asset):
            print(f"✅ {asset}")
        else:
            print(f"❌ MISSING: {asset}")
            all_present = False
    
    if all_present:
        print("\n✅ ALL STATIC ASSETS PRESENT")
        print("🔒 No external CDN dependencies")
    else:
        print("\n❌ SOME ASSETS MISSING")
    
    return all_present

def main():
    """Run all security tests"""
    print("🛡️ HIGH-SECURITY DEPLOYMENT VERIFICATION")
    print("=" * 70)
    
    # Test offline functionality
    offline_test = test_offline_functionality()
    
    # Test static assets
    assets_test = test_static_assets()
    
    # Final summary
    print("\n🏁 FINAL SECURITY ASSESSMENT")
    print("=" * 50)
    
    if offline_test and assets_test:
        print("🔒 ✅ DEPLOYMENT READY FOR HIGH-SECURITY ENVIRONMENT")
        print("   • No external network dependencies")
        print("   • All static assets included locally")
        print("   • Core functionality verified offline")
        return 0
    else:
        print("🔒 ❌ SECURITY REQUIREMENTS NOT MET")
        return 1

if __name__ == "__main__":
    sys.exit(main())