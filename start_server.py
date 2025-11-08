#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Startup script to ensure the server starts with proper error handling.
"""
import sys
import os

# CRITICAL: Force output immediately
sys.stdout.flush()
sys.stderr.flush()

# Print immediately - this MUST appear in logs
print("", flush=True)
print("=" * 50, flush=True)
print("STARTING SERVER STARTUP SCRIPT", flush=True)
print("=" * 50, flush=True)
print("", flush=True)

# Get port from environment or use default
port = os.getenv("PORT", "8000")
print(f"Port: {port}", flush=True)

# Change to backend directory
backend_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(backend_dir)
print(f"Working directory: {os.getcwd()}", flush=True)

print("=" * 50, flush=True)
print("Importing modules...", flush=True)

try:
    print("Importing uvicorn...", flush=True)
    import uvicorn
    print("✅ Uvicorn imported", flush=True)
    
    print("Importing main...", flush=True)
    from main import app
    print("✅ FastAPI app imported", flush=True)
    
    print("=" * 50, flush=True)
    print(f"🚀 Starting Uvicorn server on 0.0.0.0:{port}", flush=True)
    print("=" * 50, flush=True)
    
    # Start server
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=int(port),
        log_level="info"
    )
except ImportError as e:
    print(f"❌ Import error: {e}", flush=True)
    import traceback
    traceback.print_exc()
    sys.exit(1)
except Exception as e:
    print(f"❌ Error starting server: {e}", flush=True)
    import traceback
    traceback.print_exc()
    sys.exit(1)

