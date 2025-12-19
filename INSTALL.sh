#!/bin/bash
# One-command installation script for D&D Sheet Generator
# This will install everything you need and launch the TUI

set -e

echo "🎲 D&D Sheet Generator - Installation"
echo "======================================"
echo ""

# Check if running as root
if [ "$EUID" -eq 0 ]; then
    echo "❌ Please don't run this script as root (no sudo)"
    exit 1
fi

# Step 1: Install python3-venv if not available
# Check if we can actually create a venv (not just import the module)
if ! python3 -c "import ensurepip" 2>/dev/null; then
    echo "📦 Installing python3-venv (requires sudo)..."
    echo "You will be asked for your password to install system packages."
    echo ""
    sudo apt update
    sudo apt install -y python3.11-venv
    echo "✓ python3-venv installed"
    echo ""
fi

# Step 2: Create virtual environment
if [ ! -f "venv/bin/activate" ]; then
    echo "🔨 Creating virtual environment..."
    rm -rf venv  # Remove any incomplete venv
    python3 -m venv venv
    echo "✓ Virtual environment created"
    echo ""
else
    echo "✓ Virtual environment already exists"
    echo ""
fi

# Step 3: Install dependencies
echo "📥 Installing Python dependencies..."
source venv/bin/activate
pip install --upgrade pip -q
pip install -e . -q
echo "✓ Dependencies installed"
echo ""

# Step 4: Check LaTeX
echo "🔍 Checking LaTeX installation..."
if command -v lualatex &> /dev/null; then
    echo "✓ LaTeX is installed"
else
    echo "⚠️  LaTeX not found"
    echo ""
    echo "To generate PDFs, install LaTeX:"
    echo "  sudo apt install texlive-luatex texlive-fonts-extra"
    echo ""
    echo "You can still use the TUI without LaTeX (for creating character data)."
    echo ""
fi

echo ""
echo "✅ Installation complete!"
echo ""
echo "To run the TUI:"
echo "  ./RUN.sh"
echo ""
echo "Or:"
echo "  source venv/bin/activate"
echo "  dndsheet tui"
echo ""

# Offer to launch now
read -p "Launch the TUI now? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo ""
    echo "🚀 Launching TUI..."
    echo ""
    dndsheet tui
fi
