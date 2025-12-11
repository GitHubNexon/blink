#!/usr/bin/env python3
"""
Test script to verify AI Agent setup
Run: source venv/Scripts/activate && python test_setup.py
"""

import sys
from pathlib import Path

print("=" * 60)
print("AI AGENT SETUP VERIFICATION")
print("=" * 60)

# Test 1: Check Python version
print("\n[1/5] Checking Python version...")
python_version = sys.version_info
if python_version.major >= 3 and python_version.minor >= 8:
    print(f"✅ Python {python_version.major}.{python_version.minor}.{python_version.micro}")
else:
    print(f"❌ Python {python_version.major}.{python_version.minor} (need 3.8+)")
    sys.exit(1)

# Test 2: Check virtual environment
print("\n[2/5] Checking virtual environment...")
if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
    print("✅ Virtual environment is active")
else:
    print("⚠️  Virtual environment may not be active")
    print("   Run: source venv/Scripts/activate")

# Test 3: Check dependencies
print("\n[3/5] Checking dependencies...")
dependencies = {
    'requests': 'requests',
    'dotenv': 'python-dotenv',
}

all_installed = True
for module_name, package_name in dependencies.items():
    try:
        __import__(module_name)
        print(f"✅ {package_name}")
    except ImportError:
        print(f"❌ {package_name}")
        all_installed = False

if not all_installed:
    print("\n   Run: pip install -r requirements.txt")
    sys.exit(1)

# Test 4: Check configuration
print("\n[4/5] Checking configuration...")
try:
    from src.config import REPLICATE_API_TOKEN, MODEL, WORKSPACE_ROOT
    
    if REPLICATE_API_TOKEN and REPLICATE_API_TOKEN != "xxxxxxxxxxxxxxxxxxxxxxxx":
        print("✅ REPLICATE_API_TOKEN is set")
    else:
        print("⚠️  REPLICATE_API_TOKEN not configured")
        print("   Edit .env file with your actual token")
    
    print(f"✅ MODEL: {MODEL}")
    print(f"✅ WORKSPACE: {WORKSPACE_ROOT}")
except Exception as e:
    print(f"❌ Configuration error: {e}")
    sys.exit(1)

# Test 5: Check agent imports
print("\n[5/5] Checking agent imports...")
try:
    from src.agent import CodeAgent
    from src.file_handler import FileHandler
    from src.replicate_api import ReplicateClient
    from src.cli import main
    
    print("✅ CodeAgent imported")
    print("✅ FileHandler imported")
    print("✅ ReplicateClient imported")
    print("✅ CLI imported")
except Exception as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)

# Summary
print("\n" + "=" * 60)
print("✅ ALL TESTS PASSED!")
print("=" * 60)
print("\nYour AI Agent is ready to use!")
print("\nNext steps:")
print("1. python main.py          # Start interactive CLI")
print("2. Type 'help'             # See available commands")
print("3. Try: plan Build a web scraper")
print("\nFor more info, read:")
print("- README.md               # Full documentation")
print("- QUICKSTART.md           # Quick reference")
print("- SETUP_COMPLETE.txt      # Setup details")
print("\n" + "=" * 60)
