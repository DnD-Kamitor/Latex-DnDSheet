# TUI Usage Guide

## Installing Textual

To use the TUI, you need to install Textual first:

### Option 1: Virtual Environment (Recommended)

```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Linux/Mac
# venv\Scripts\activate  # On Windows

# Install dependencies
pip install textual>=0.47.0 rich>=13.0.0
```

### Option 2: User Installation

```bash
pip install --user textual>=0.47.0 rich>=13.0.0
```

### Option 3: System Package (May be older version)

```bash
sudo apt install python3-textual python3-rich
```

## Launching the TUI

From the repository root:

```bash
# If using virtual environment
source venv/bin/activate
python -m dndsheet tui

# Or with PYTHONPATH
PYTHONPATH=src python3 -m dndsheet tui
```

## Main Menu

The TUI main menu provides several options:

### 📋 Character Management
- **Create Character Sheet**: Interactive character creation (Phase 9)
- **Load Character from File**: ✅ Browse and load existing JSON characters

### 📚 In-World Documents
- **Create Spell Book**: Generate spell grimoires (Future)
- **Create Crafting Guide**: Herbalism, alchemy guides (Future)
- **Create Custom Book**: Custom in-world documents (Future)

### 🎭 DM Tools
- **Create NPC Sheet**: NPC stat blocks (Future)
- **Create Session Notes**: Session planning tools (Future)

### 🎪 Props & Handouts
- **Create Wanted Poster**: Wanted posters, bounties (Future)
- **Create Letter/Document**: Letters, scrolls, documents (Future)

### ⚙️ Settings
- Configure LaTeX template path, output directory (Future)

## Using the File Browser (Currently Working!)

1. Launch the TUI
2. Select **"Load Character from File"**
3. Browse to `examples/characters/`
4. Select a `.json` file (e.g., `grimnar_ironforge.json`)
5. Click **"Generate PDF"**
6. The PDF will be created in the `output/` directory
7. You'll see a notification when it's complete

## Keyboard Shortcuts

- **Q**: Quit the application
- **Escape**: Go back to previous screen
- **Arrow Keys**: Navigate menus and file browser
- **Enter**: Select/activate button or file

## Example Workflow

```bash
# 1. Install textual
python3 -m venv venv
source venv/bin/activate
pip install textual rich

# 2. Launch TUI
python -m dndsheet tui

# 3. In the TUI:
#    - Press Enter on "Load Character from File"
#    - Navigate to examples/characters/
#    - Select grimnar_ironforge.json
#    - Press Enter on "Generate PDF"
#    - Check output/grimnar_ironforge_sheet.pdf

# 4. Exit with Q
```

## Troubleshooting

### "Textual is not installed"
Install textual as shown above.

### "No module named 'dndsheet'"
Make sure you're running from the repository root and using `PYTHONPATH=src`.

### File browser shows wrong directory
The file browser starts in `examples/characters/` if it exists, otherwise current directory. Use arrow keys to navigate.

### PDF generation fails
1. Check that LaTeX is installed: `python -m dndsheet check`
2. Verify the JSON file is valid
3. Check `output/` directory for error messages

## Current Status

### ✅ Working Features:
- Main menu navigation
- File browser for .json files
- Character loading from JSON
- PDF generation from TUI
- Notifications and error handling

### 🚧 Coming Soon (Phase 9+):
- Interactive character creation forms
- Character editing
- Settings screen
- In-world document creators
- DM tools

## Notes

- All generated PDFs go to the `output/` directory
- The TUI uses the same backend as the CLI, so all features work identically
- You can use the CLI for more control: `python -m dndsheet generate file.json -o custom.pdf`
