#!/usr/bin/env python3
"""
Startup script for the Media Monitoring Knowledge Assistant API
"""

import uvicorn
import sys
import os
from pathlib import Path

# Add the src directory to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

def main():
    """Start the API server"""
    print("=" * 60)
    print("Media Monitoring Knowledge Assistant API")
    print("=" * 60)
    print()
    
    # Check if required environment variables are set
    required_env_vars = [
        "ASTRA_DB_APPLICATION_TOKEN",
        "ASTRA_DB_API_ENDPOINT", 
        "ASTRA_DB_COLLECTION_NAME",
        "GEMINI_API_KEY"
    ]
    
    missing_vars = []
    for var in required_env_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print("⚠️  Warning: The following environment variables are not set:")
        for var in missing_vars:
            print(f"   - {var}")
        print()
        print("The API may not function properly without these variables.")
        print("Please check your .env file or environment configuration.")
        print()
    
    # Server configuration
    host = os.getenv("API_HOST", "0.0.0.0")
    port = int(os.getenv("API_PORT", "8000"))
    reload = os.getenv("API_RELOAD", "true").lower() == "true"
    log_level = os.getenv("API_LOG_LEVEL", "info")
    
    print(f"🚀 Starting API server...")
    print(f"   Host: {host}")
    print(f"   Port: {port}")
    print(f"   Reload: {reload}")
    print(f"   Log Level: {log_level}")
    print()
    print("📚 API Documentation will be available at:")
    print(f"   Swagger UI: http://{host}:{port}/docs")
    print(f"   ReDoc: http://{host}:{port}/redoc")
    print(f"   OpenAPI JSON: http://{host}:{port}/openapi.json")
    print()
    print("🔄 Press Ctrl+C to stop the server")
    print("=" * 60)
    print()
    
    try:
        # Start the server
        uvicorn.run(
            "main.main:app",
            host=host,
            port=port,
            reload=reload,
            log_level=log_level,
            access_log=True
        )
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"\n❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
