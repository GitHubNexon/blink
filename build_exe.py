#!/usr/bin/env python3
"""
Build Blink AI Agent as a standalone executable (.exe)

This script uses PyInstaller to package the entire Blink project
into a single executable that doesn't require Python or venv to run.

Usage:
    python build_exe.py
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path


def main():
    """Build the executable"""
    
    print("=" * 70)
    print("[BLINK] Building Executable")
    print("=" * 70 + "\n")
    
    # Get project root
    project_root = Path(__file__).parent.absolute()
    dist_dir = project_root / "dist"
    build_dir = project_root / "build"
    spec_file = project_root / "blink.spec"
    
    # Check if PyInstaller is installed
    print("[CHECK] Verifying PyInstaller installation...")
    try:
        import PyInstaller
        print("[OK] PyInstaller is installed\n")
    except ImportError:
        print("[ERROR] PyInstaller not found!")
        print("[INSTALL] Installing PyInstaller...\n")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller>=6.0.0"])
    
    # Clean old builds
    print("[CLEAN] Removing old build artifacts...")
    for dir_to_clean in [dist_dir, build_dir]:
        if dir_to_clean.exists():
            shutil.rmtree(dir_to_clean)
            print(f"[OK] Removed {dir_to_clean.name}/")
    
    if spec_file.exists():
        spec_file.unlink()
        print(f"[OK] Removed {spec_file.name}")
    
    print()
    
    # Build command
    print("[BUILD] Creating executable with PyInstaller...\n")
    
    build_cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name", "Blink",
        "--onefile",
        "--console",  # Keep console for token input
        "--icon=blink.ico" if (project_root / "blink.ico").exists() else None,
        "--add-data", f"src:src",
        "--hidden-import=pathvalidate",
        "--hidden-import=requests",
        "--hidden-import=dotenv",
        "--hidden-import=token_manager",
        "--collect-all=pathvalidate",
        "--collect-all=requests",
        "--collect-all=dotenv",
        "--clean",
        "main.py"
    ]
    
    # Remove None values from command
    build_cmd = [x for x in build_cmd if x is not None]
    
    try:
        subprocess.check_call(build_cmd, cwd=project_root)
    except subprocess.CalledProcessError as e:
        print(f"\n[ERROR] Build failed: {e}")
        return False
    
    print("\n" + "=" * 70)
    print("[OK] Build Complete!")
    print("=" * 70 + "\n")
    
    # Show results
    exe_path = dist_dir / "Blink.exe"
    if exe_path.exists():
        file_size = exe_path.stat().st_size / (1024 * 1024)  # Convert to MB
        print(f"[LOCATION] Executable created at:")
        print(f"           {exe_path}\n")
        print(f"[SIZE]     {file_size:.2f} MB\n")
        print("[READY] You can now:")
        print(f"        1. Run the exe: {exe_path.name}")
        print(f"        2. Share the 'dist' folder with others")
        print(f"        3. Or move {exe_path.name} anywhere on your system\n")
        return True
    else:
        print("[ERROR] Build failed - executable not found")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
