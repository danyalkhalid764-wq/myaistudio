# Fix Rust/Pydantic-Core Installation Error

## Problem
`pydantic-core` requires Rust to compile from source. This happens when pre-built wheels aren't available for your Python version.

## Solutions (Try in Order)

### Solution 1: Update pip, setuptools, and wheel (Recommended)

```bash
python -m pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

### Solution 2: Install Rust (If Solution 1 doesn't work)

**Windows:**
1. Download Rust installer: https://rustup.rs/
2. Run the installer
3. Restart your terminal/PyCharm
4. Then run: `pip install -r requirements.txt`

**Or via PowerShell:**
```powershell
# Install Rust via winget (Windows 11)
winget install Rustlang.Rustup

# Or download and run: https://win.rustup.rs/x86_64
```

### Solution 3: Use Pre-built Wheels (Easiest)

```bash
# Upgrade pip first
python -m pip install --upgrade pip

# Install pydantic-core separately with pre-built wheel
pip install pydantic-core --only-binary :all:

# Then install requirements
pip install -r requirements.txt
```

### Solution 4: Install Specific Python Version

If you're using Python 3.13 (very new), try Python 3.11 or 3.12 which have better wheel support:

```bash
# Check your Python version
python --version

# If it's 3.13, consider using 3.11 or 3.12
```

### Solution 5: Install Requirements One by One

```bash
# Install core dependencies first
pip install fastapi uvicorn sqlalchemy alembic python-dotenv

# Then install the rest
pip install -r requirements.txt
```

## Quick Fix Commands (Copy-Paste)

```bash
# Step 1: Upgrade pip
python -m pip install --upgrade pip setuptools wheel

# Step 2: Try installing again
pip install -r requirements.txt

# If that fails, try Solution 3:
pip install pydantic-core --only-binary :all:
pip install -r requirements.txt
```

