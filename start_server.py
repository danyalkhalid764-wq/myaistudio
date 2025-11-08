#!/usr/bin/env python3
"""
Startup script to ensure the server starts with proper error handling.
"""
import sys
import os
import subprocess

print("=" * 50)
print("🚀 Starting server startup script...")
print("=" * 50)

# Get port from environment or use default
port = os.getenv("PORT", "8000")
print(f"Port: {port}")

# Change to backend directory
backend_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(backend_dir)
print(f"Working directory: {os.getcwd()}")

print("=" * 50)
print("Starting Uvicorn server...")
print("=" * 50)

try:
    # Start uvicorn server
    import uvicorn
    from main import app
    
    print("✅ Uvicorn imported successfully")
    print("✅ FastAPI app imported successfully")
    print(f"🚀 Starting server on 0.0.0.0:{port}")
    print("=" * 50)
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=int(port),
        log_level="info"
    )
except Exception as e:
    print(f"❌ Error starting server: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

