#!/usr/bin/env python3
"""
Virtual Environment Setup Script for MyAIStudio Backend
Run this script to set up the virtual environment and install dependencies
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error in {description}: {e}")
        print(f"Error output: {e.stderr}")
        return False

def main():
    """Main setup function"""
    print("🚀 Setting up MyAIStudio Backend Virtual Environment")
    print("=" * 50)
    
    # Check if Python is available
    if not run_command("python --version", "Checking Python version"):
        print("❌ Python is not installed or not in PATH")
        print("Please install Python 3.10+ from https://python.org")
        return False
    
    # Create virtual environment
    venv_path = Path("venv")
    if venv_path.exists():
        print("📁 Virtual environment already exists")
    else:
        if not run_command("python -m venv venv", "Creating virtual environment"):
            return False
    
    # Determine activation script path
    if os.name == 'nt':  # Windows
        activate_script = "venv\\Scripts\\activate"
        pip_path = "venv\\Scripts\\pip"
    else:  # Unix/Linux/Mac
        activate_script = "venv/bin/activate"
        pip_path = "venv/bin/pip"
    
    # Install dependencies
    if not run_command(f"{pip_path} install --upgrade pip", "Upgrading pip"):
        return False
    
    if not run_command(f"{pip_path} install -r requirements.txt", "Installing dependencies"):
        return False
    
    print("\n" + "=" * 50)
    print("✅ Virtual environment setup completed!")
    print("\n📋 Next steps:")
    print("1. Activate the virtual environment:")
    if os.name == 'nt':
        print("   venv\\Scripts\\activate")
    else:
        print("   source venv/bin/activate")
    print("\n2. Create .env file from env.example:")
    print("   copy env.example .env")
    print("\n3. Edit .env with your API keys")
    print("\n4. Run database migrations:")
    print("   alembic upgrade head")
    print("\n5. Start the server:")
    print("   uvicorn main:app --reload")
    print("\n🌐 Server will be available at: http://localhost:8000")
    print("📚 API Documentation: http://localhost:8000/docs")

if __name__ == "__main__":
    main()
























