# Quick Start Guide

## One Command to Install and Run

**First time? Run this:**

```bash
./INSTALL.sh
```

This will:
- Install python3-venv (asks for sudo once)
- Create a virtual environment
- Install all dependencies
- Offer to launch the TUI

**Already installed? Just run:**

```bash
./RUN.sh
```

## Manual Setup (Alternative)

If you prefer to do it manually:

### Install Python venv (one time only)
```bash
sudo apt install python3.11-venv
```

### Create and activate virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
pip install -e .
```

### Run the TUI
```bash
dndsheet tui
```

## Alternative: CLI Usage

### Generate PDF from existing character
```bash
dndsheet generate examples/characters/grimnar_ironforge.json
```

### Check LaTeX installation
```bash
dndsheet check
```

## What Can You Do?

### TUI Features (Interactive)
- **Create Character Sheet**: 4-step wizard to create a new character
  - Step 1: Basic info (name, race, class, level)
  - Step 2: Skills and proficiencies
  - Step 3: Ability scores
  - Step 4: Combat stats (AC, HP, speed)
- **Load Character from File**: Browse and generate PDFs from JSON files
- **Settings**: Configure paths (coming soon)

### CLI Features (Command Line)
- Generate PDFs from JSON character files
- Check if LaTeX is properly installed
- Launch the TUI

## Example Workflow

```bash
# 1. Run the tool
./RUN.sh

# 2. In the TUI:
#    - Press Enter on "Create Character Sheet"
#    - Fill in character details through the wizard
#    - Click "Generate PDF"
#
# OR
#    - Press Enter on "Load Character from File"
#    - Navigate to examples/characters/
#    - Select grimnar_ironforge.json
#    - Click "Generate PDF"

# 3. Find your PDF in the output/ directory
ls -lh output/

# 4. Exit the TUI with 'Q' or the Exit button
```

## Keyboard Shortcuts

- **Q**: Quit application
- **Escape**: Go back to previous screen
- **Arrow Keys**: Navigate menus
- **Enter**: Select/activate
- **Tab**: Move between form fields

## Troubleshooting

### "ensurepip is not available"
Install python3-venv:
```bash
sudo apt install python3.11-venv
```

### "textual is not installed"
Install in a virtual environment (recommended):
```bash
python3 -m venv venv
source venv/bin/activate
pip install -e .
```

Or install system-wide (not recommended):
```bash
pip install --user --break-system-packages textual rich jinja2 pyyaml
```

### "LaTeX not found" or PDF generation fails
Install LaTeX:
```bash
sudo apt install texlive-luatex texlive-fonts-extra
```

Check installation:
```bash
dndsheet check
```

### Can't find dndsheet command
Make sure you've installed the package:
```bash
pip install -e .
```

Or use PYTHONPATH mode:
```bash
PYTHONPATH=src python3 -m dndsheet tui
```

## Example Characters

Try these pre-made characters in `examples/characters/`:
- `grimnar_ironforge.json` - Dwarf Fighter
- `elara_moonwhisper.json` - Elf Wizard
- `thorin_stonehelm.json` - Dwarf Cleric

## What's Next?

See [README.md](README.md) for full documentation and development roadmap.
