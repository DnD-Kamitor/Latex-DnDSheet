# Installation Guide

## System Requirements

- Python 3.10 or higher
- LuaLaTeX (part of TeX Live)
- Linux operating system

## LaTeX Installation

### Install TeX Live (includes LuaLaTeX)

```bash
sudo apt update
sudo apt install texlive-full
```

Or for a minimal installation:

```bash
sudo apt install texlive-luatex texlive-latex-extra
```

### Install DND-5e-LaTeX-Template

The template is included in this repository at `DND-5e-LaTeX-Template/`. No additional installation needed.

## Python Dependencies

### Option 1: Using Virtual Environment (Recommended)

```bash
# Install venv package
sudo apt install python3.11-venv

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Option 2: Using System Packages

```bash
sudo apt install python3-jinja2
```

For the TUI (Phase 7+):
```bash
sudo apt install python3-textual python3-rich
```

**Note**: System packages may be older versions. For best experience, use a virtual environment.

### Option 3: User Installation (Without sudo)

If you don't have sudo access:

```bash
pip3 install --user -r requirements.txt
```

## Verification

Check that everything is installed correctly:

```bash
# Check LaTeX environment
PYTHONPATH=src python3 -m dndsheet check

# Expected output:
# ✓ LuaLaTeX: <version info>
# ✓ DND Template: <path>
# ✓ Environment is ready!
```

## Testing the CLI

Generate a test character sheet:

```bash
PYTHONPATH=src python3 -m dndsheet generate examples/characters/grimnar_ironforge.json
```

This should create `output/grimnar_ironforge_sheet.pdf`.

## Running the TUI (Phase 7+)

Once textual is installed:

```bash
PYTHONPATH=src python3 -m dndsheet tui
```

## Troubleshooting

### "No module named 'dndsheet'"

Make sure you're running from the repository root and using `PYTHONPATH=src`:

```bash
cd /path/to/Latex-DnDSheet
PYTHONPATH=src python3 -m dndsheet check
```

### "LuaLaTeX not found"

Install TeX Live:

```bash
sudo apt install texlive-luatex
```

### "DND-5e-LaTeX-Template not found"

Make sure the `DND-5e-LaTeX-Template/` directory exists in the repository root.

### Virtual environment activation issues

If `python3-venv` is not installed:

```bash
sudo apt install python3.11-venv
```

Then create the venv again:

```bash
python3 -m venv venv
source venv/bin/activate
```
