#!/bin/bash
# Quick run script for D&D Sheet Generator
# This script tries multiple installation methods

set -e

echo "🎲 D&D Sheet Generator"
echo "======================"
echo ""

# Method 1: Try with virtual environment (cleanest)
if [ -f "venv/bin/activate" ]; then
    echo "✓ Using existing virtual environment"
    source venv/bin/activate
    dndsheet tui
    exit 0
fi

# Method 2: Try creating venv
if command -v python3 &> /dev/null; then
    echo "Attempting to create virtual environment..."
    if python3 -m venv venv 2>/dev/null; then
        source venv/bin/activate
        echo "Installing dependencies..."
        pip install --upgrade pip -q
        pip install -e . -q
        echo ""
        echo "✅ Setup complete! Launching TUI..."
        echo ""
        dndsheet tui
        exit 0
    fi
fi

# Method 3: Use PYTHONPATH (development mode)
echo "⚠️  Virtual environment not available"
echo "Running in development mode with PYTHONPATH..."
echo ""

# Check if dependencies are available
python3 -c "import textual" 2>/dev/null || {
    echo "❌ Error: textual is not installed"
    echo ""
    echo "Please install dependencies first:"
    echo "  sudo apt install python3.11-venv"
    echo "  python3 -m venv venv"
    echo "  source venv/bin/activate"
    echo "  pip install -e ."
    echo ""
    echo "Or install system-wide (not recommended):"
    echo "  pip install --user --break-system-packages textual rich jinja2 pyyaml"
    echo ""
    exit 1
}

PYTHONPATH=src python3 -m dndsheet tui
