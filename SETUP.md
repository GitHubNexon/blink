# Blink - Setup & Configuration Guide

## Problem You're Seeing

```
ValueError: REPLICATE_API_TOKEN is not set in .env file
```

This error means Blink needs your Replicate API token to work. Follow the steps below to fix it.

---

## Solution: 3 Easy Ways to Set Up

### Method 1: Automatic Setup (RECOMMENDED) ⭐

The easiest way - our setup script will guide you through everything:

**Windows:**

```bash
python setup.py
```

**macOS/Linux:**

```bash
python setup.py
```

This script will:

1. Ask for your API token
2. Ask which AI model to use
3. Create the `.env` file automatically
4. You're done!

---

### Method 2: Manual Setup (Copy-Paste)

Create a file named `.env` in the project root folder with:

```env
REPLICATE_API_TOKEN=your_actual_token_here
MODEL=anthropic/claude-4.5-sonnet
```

Replace `your_actual_token_here` with your real token.

---

### Method 3: Environment Variable

If you prefer not to create a `.env` file, set an environment variable:

**Windows (Command Prompt):**

```cmd
set REPLICATE_API_TOKEN=your_token_here
python main.py
```

**Windows (PowerShell):**

```powershell
$env:REPLICATE_API_TOKEN="your_token_here"
python main.py
```

**macOS/Linux:**

```bash
export REPLICATE_API_TOKEN=your_token_here
python main.py
```

---

## Get Your Free API Token

1. Go to: **https://replicate.com/signin**
2. Sign up for a free account (takes 1 minute)
3. Go to your account page and copy your API token
4. Paste it into the setup script or `.env` file

**No credit card required!** Free tier is generous enough for testing.

---

## Quick Start Commands

### If using Raw Version (Python):

```bash
# 1. Create virtual environment
python -m venv venv

# 2. Activate it
# Windows:
venv\Scripts\activate.bat
# macOS/Linux:
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up API token (choose one method above)
python setup.py

# 5. Run Blink
python main.py
```

### If using EXE Version:

```bash
# 1. Build the executable
python build_exe.py

# 2. The EXE will be at: dist/Blink.exe

# 3. Create .env in the same folder as Blink.exe
# Add: REPLICATE_API_TOKEN=your_token_here

# 4. Double-click Blink.exe to run
```

---

## Verification Checklist

After setup, verify everything works:

```bash
✓ .env file exists in project root
✓ REPLICATE_API_TOKEN is in the .env file
✓ Token is from https://replicate.com
✓ Python dependencies installed (pip install -r requirements.txt)
✓ Virtual environment activated (if using raw version)
```

Run: `python main.py`

You should see:

```
=======================================
[AI AGENT] - Code Generation & Analysis Platform
=======================================

Workspace: C:\...\blink\workspace

Type 'help::' for commands or 'exit::' to quit.

blink>
```

---

## Troubleshooting

### Still getting "REPLICATE_API_TOKEN is not set"

1. Check `.env` file exists in project root
2. Verify it contains: `REPLICATE_API_TOKEN=...` (not empty)
3. Make sure token is from https://replicate.com
4. Try restarting your terminal/command prompt

### "ModuleNotFoundError: No module named 'requests'"

Run: `pip install -r requirements.txt`

Then activate venv if you haven't already.

### Python not found

Install Python from: https://www.python.org/downloads/

Make sure to check "Add Python to PATH" during installation.

---

## Getting Help

1. Use `setup.py` script - it's interactive and will guide you
2. Check `.env.example` for template
3. Run `python main.py` to see detailed error messages
4. Use `help::` command inside Blink for command reference

---

Good luck! You're almost there! 🚀
