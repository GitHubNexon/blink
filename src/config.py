"""Configuration module for AI Agent"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Try to load from .env if it exists (for development)
env_path = Path(__file__).parent.parent / ".env"
if env_path.exists():
    load_dotenv(dotenv_path=env_path)

# Try to get token from environment (for development/raw Python)
REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")
MODEL = os.getenv("MODEL", "anthropic/claude-4.5-sonnet")

# If no token in .env or env vars, we'll prompt at startup (for EXE)
# This is handled by token_manager.py when the app starts
if not REPLICATE_API_TOKEN:
    # For EXE version: token will be prompted via token_manager
    # For raw Python: provide helpful error message
    REPLICATE_API_TOKEN = None  # Will be set by token_manager at startup

# Project root
PROJECT_ROOT = Path(__file__).parent.parent
SRC_DIR = PROJECT_ROOT / "src"
WORKSPACE_ROOT = PROJECT_ROOT / "workspace"

# Ensure workspace directory exists
WORKSPACE_ROOT.mkdir(exist_ok=True)

