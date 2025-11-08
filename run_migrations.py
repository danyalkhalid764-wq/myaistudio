#!/usr/bin/env python3
"""
Wrapper script to run Alembic migrations with error handling.
This ensures we see any errors that occur during migrations.
"""
import sys
import subprocess
import os

print("=" * 50)
print("Starting migration wrapper script...")
print("=" * 50)

# Change to backend directory if needed
backend_dir = os.path.dirname(os.path.abspath(__file__))
print(f"Working directory: {backend_dir}")
os.chdir(backend_dir)
print(f"Changed to: {os.getcwd()}")

# Check if alembic is available
print("Checking if alembic is available...")
try:
    result = subprocess.run(
        ["alembic", "--version"],
        cwd=backend_dir,
        capture_output=True,
        text=True,
        timeout=10
    )
    print(f"Alembic version check: {result.stdout}")
except Exception as e:
    print(f"❌ Error checking alembic: {e}")
    print("Continuing anyway...")

print("=" * 50)
print("Running Alembic migrations...")
print("=" * 50)

try:
    # Run alembic upgrade head with explicit output
    print("Executing: alembic upgrade head")
    result = subprocess.run(
        ["alembic", "upgrade", "head"],
        cwd=backend_dir,
        capture_output=False,  # Show output in real-time
        text=True,
        check=False,  # Don't raise exception, we'll handle it
        timeout=60  # 60 second timeout
    )
    
    print("=" * 50)
    if result.returncode != 0:
        print(f"❌ Alembic migrations failed with exit code {result.returncode}")
        print("=" * 50)
        # Don't exit - let server start anyway
        print("⚠️  Continuing with server startup despite migration failure...")
    else:
        print("✅ Alembic migrations completed successfully!")
        print("=" * 50)
        
except subprocess.TimeoutExpired:
    print("❌ Alembic migrations timed out after 60 seconds")
    print("⚠️  Continuing with server startup...")
except Exception as e:
    print(f"❌ Error running Alembic migrations: {e}")
    import traceback
    traceback.print_exc()
    print("=" * 50)
    print("⚠️  Continuing with server startup...")

print("=" * 50)
print("Migration wrapper script complete.")
print("=" * 50)

