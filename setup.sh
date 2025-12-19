#!/bin/bash
# One-command setup and run script for D&D Sheet Generator

set -e  # Exit on error

echo "🎲 D&D Sheet Generator - Quick Setup"
echo "======================================"
echo ""

# Check if venv exists and is valid
if [ ! -f "venv/bin/activate" ]; then
    echo "📦 Creating virtual environment..."
    rm -rf venv  # Remove any incomplete venv
    python3 -m venv venv
fi

echo "🔧 Activating virtual environment..."
source venv/bin/activate

echo "📥 Installing dependencies..."
pip install --upgrade pip > /dev/null 2>&1
pip install -e . > /dev/null 2>&1

echo "✅ Setup complete!"
echo ""
echo "🚀 Launching TUI..."
echo ""

# Run the TUI
dndsheet tui
