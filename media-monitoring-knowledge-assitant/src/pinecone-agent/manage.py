#!/usr/bin/env python3
"""
Management script for the Media Monitoring Knowledge Assistant
This script sets up the Python environment and provides commands to run the application
"""

import os
import sys
import subprocess
from pathlib import Path

# Get the project root directory
PROJECT_ROOT = Path(__file__).parent.absolute()
SRC_DIR = PROJECT_ROOT / "src"

def setup_environment():
    """Set up the Python environment by adding src to Python path"""
    if str(SRC_DIR) not in sys.path:
        sys.path.insert(0, str(SRC_DIR))
        print(f"✅ Added {SRC_DIR} to Python path")
    
    # Set environment variables
    os.environ['PYTHONPATH'] = str(SRC_DIR)
    print(f"✅ Set PYTHONPATH to {SRC_DIR}")

def run_server():
    """Run the FastAPI server"""
    setup_environment()
    
    print("🚀 Starting FastAPI server...")
    print(f"📁 Working directory: {SRC_DIR}")
    print(f"🐍 Python path: {sys.path[0]}")
    
    try:
        # Change to src directory and run the FastAPI app
        os.chdir(SRC_DIR)
        
        # Import and run the FastAPI app
        from main.main import app
        import uvicorn
        
        print("✅ FastAPI app imported successfully")
        print("🌐 Starting server on http://localhost:8000")
        
        # Use import string for reload to work properly
        uvicorn.run(
            "main.main:app", 
            host="0.0.0.0", 
            port=8000, 
            reload=True,
            log_level="info"
        )
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Make sure you're in the project root directory")
        return 1
    except Exception as e:
        print(f"❌ Error running server: {e}")
        return 1
    
    return 0

def run_tests():
    """Run tests"""
    setup_environment()
    print("🧪 Running tests...")
    
    try:
        result = subprocess.run([
            sys.executable, "-m", "pytest", 
            str(SRC_DIR), "-v"
        ], cwd=SRC_DIR)
        return result.returncode
    except Exception as e:
        print(f"❌ Error running tests: {e}")
        return 1

def install_dependencies():
    """Install dependencies using uv"""
    print("📦 Installing dependencies...")
    
    try:
        result = subprocess.run([
            "uv", "sync"
        ], cwd=PROJECT_ROOT)
        return result.returncode
    except Exception as e:
        print(f"❌ Error installing dependencies: {e}")
        return 1

def show_help():
    """Show help information"""
    print("""
🔧 Media Monitoring Knowledge Assistant - Management Script

Usage:
    uv run manage.py <command>

Commands:
    runserver      - Start the FastAPI server
    test           - Run tests
    install        - Install dependencies
    help           - Show this help message

Examples:
    uv run manage.py runserver
    uv run manage.py test
    uv run manage.py install
    """)

def main():
    """Main entry point"""
    if len(sys.argv) < 2:
        show_help()
        return 1
    
    command = sys.argv[1].lower()
    
    if command == "runserver":
        return run_server()
    elif command == "test":
        return run_tests()
    elif command == "install":
        return install_dependencies()
    elif command == "help":
        show_help()
        return 0
    else:
        print(f"❌ Unknown command: {command}")
        show_help()
        return 1

if __name__ == "__main__":
    exit(main())
