#!/bin/bash
# Quick Setup Guide for Blink
# Copy and paste these commands to get started

echo "=========================================="
echo "Blink - Quick Setup"
echo "=========================================="
echo ""
echo "Step 1: Create virtual environment"
python -m venv venv

echo ""
echo "Step 2: Activate virtual environment"
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    # Windows
    source venv/Scripts/activate
else
    # macOS/Linux
    source venv/bin/activate
fi

echo ""
echo "Step 3: Install dependencies"
pip install -r requirements.txt

echo ""
echo "Step 4: Configure API token"
echo "Run the setup helper:"
python setup.py

echo ""
echo "Step 5: Launch Blink"
echo "Run:"
echo "  python main.py"
echo ""
echo "=========================================="
