#!/usr/bin/env python3
"""
Wrapper script to run Alembic migrations with error handling.
This ensures we see any errors that occur during migrations.
"""
import sys
import subprocess
import os

print("=" * 50)
print("Running Alembic migrations...")
print("=" * 50)

# Change to backend directory if needed
backend_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(backend_dir)

try:
    # Run alembic upgrade head
    result = subprocess.run(
        ["alembic", "upgrade", "head"],
        cwd=backend_dir,
        capture_output=False,  # Show output in real-time
        text=True,
        check=False  # Don't raise exception, we'll handle it
    )
    
    if result.returncode != 0:
        print(f"❌ Alembic migrations failed with exit code {result.returncode}")
        print("=" * 50)
        sys.exit(result.returncode)
    else:
        print("=" * 50)
        print("✅ Alembic migrations completed successfully!")
        print("=" * 50)
        
except Exception as e:
    print(f"❌ Error running Alembic migrations: {e}")
    import traceback
    traceback.print_exc()
    print("=" * 50)
    sys.exit(1)

