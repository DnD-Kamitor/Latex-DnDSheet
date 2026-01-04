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

echo "🔧 Installing TUI dependencies..."
pip install textual>=0.47.0 rich>=13.0.0 > /dev/null 2>&1

echo "🔧 Checking LaTeX environment..."
if command -v lualatex &> /dev/null; then
    echo "✓ LaTeX is installed"
else
    echo "⚠️  LaTeX not found"
    echo "Installing LaTeX packages..."
    sudo apt update
    sudo apt install -y texlive-luatex texlive-fonts-extra texlive-latex-extra
    echo "✓ LaTeX packages installed"
fi

echo "🔧 Checking DND-5e-LaTeX-Template..."
if [ -f "DND-5e-LaTeX-Template/dndbook.cls" ]; then
    echo "✓ DND template found"
else
    echo "⚠️  DND template not found"
    echo "Cloning DND-5e-LaTeX-Template..."
    git clone https://github.com/rpgtex/DND-5e-LaTeX-Template.git
    echo "✓ DND template cloned"
fi

echo "✅ Setup complete!"
echo ""
echo "🚀 Launching TUI..."
echo ""

# Run the TUI
dndsheet tui
