# Fix Python 3.13 Installation Issues

## Problem
You're using Python 3.13 which is very new. Some packages (like pydantic-core) don't have pre-built wheels for Python 3.13 yet, so they try to compile from source, which requires Rust.

## Solution: Updated Requirements

I've updated `requirements.txt` to use newer versions that have better Python 3.13 support.

## Commands to Run in PyCharm

### Step 1: Uninstall old packages (if needed)
```bash
pip uninstall pydantic pydantic-core -y
```

### Step 2: Install updated requirements
```bash
pip install -r requirements.txt
```

### Step 3: If it still fails, install Rust properly

**Option A: Install Rust system-wide**
1. Download from: https://rustup.rs/
2. Run the installer
3. Restart PyCharm terminal
4. Run: `pip install -r requirements.txt`

**Option B: Use Python 3.11 or 3.12 (Recommended)**
Python 3.11 or 3.12 have better package support:

1. Create a new virtual environment with Python 3.11 or 3.12
2. Activate it
3. Run: `pip install -r requirements.txt`

## Quick Fix Commands

```bash
# In PyCharm terminal (you're already in backend folder)
pip uninstall pydantic pydantic-core -y
pip install -r requirements.txt
```

If that doesn't work:
```bash
# Install Rust first
# Download from: https://rustup.rs/
# Then restart terminal and:
pip install -r requirements.txt
```

