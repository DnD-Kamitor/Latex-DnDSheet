# Latex-DnDSheet

A Linux terminal application for creating D&D character sheets, NPC sheets, and DM session materials using LaTeX and the [DND-5e-LaTeX-Template](https://github.com/rpgtex/DND-5e-LaTeX-Template).

## Project Goals

Create a terminal-based tool that generates professional-quality D&D materials in LaTeX format with offline capability.

### Features

- **Character Sheet Creator**
  - D&D 2024 rules support
  - D&D 5e (2014) rules support
  - Traditional ledger sheets (items, gold tracking, spells)
  - Extended notes variant

- **Dungeon Master Tools**
  - NPC creator with stat blocks
  - Session planning and note templates

- **Output Format**
  - Professional D&D-styled PDFs using LaTeX
  - Fully offline workflow
  - Compatible with VSCodium/VSCode and Overleaf

## Technology Stack

- **LaTeX Template**: [rpgtex/DND-5e-LaTeX-Template](https://github.com/rpgtex/DND-5e-LaTeX-Template)
- **Compilation**: LuaLaTeX (recommended)
- **Platform**: Linux

## Status

Early planning and development phase.

## Development Roadmap

> **Strategy**: Build and validate core functionality first (Phases 1-6), then add TUI (Phases 7+)

### Phase 1: Project Setup & Foundation
- [x] Set up Python project structure (src/dndsheet/, tests/, templates/, docs/)
- [x] Create rulebooks/ directory with reference data (proficiency, modifiers)
- [ ] Create pyproject.toml with dependencies (Python 3.10+, jinja2, pydantic, pyyaml)
- [ ] Set up pytest for testing
- [ ] Create basic CLI entry point (argparse/click) for testing
- [ ] Add .gitignore for Python projects (*.pyc, __pycache__, *.pdf, *.aux, *.log)
- [ ] Write test: Python package imports correctly
- [ ] Add CI/CD workflow (GitHub Actions) for automated testing

### Phase 2: LaTeX Environment Validation
- [ ] Write function to verify LuaLaTeX installation (subprocess check)
- [ ] Write function to check for DND-5e-LaTeX-Template in TEXMFHOME
- [ ] Create installation helper script for DND template
- [ ] Write test: Detect LuaLaTeX correctly
- [ ] Write test: Detect DND template availability
- [ ] Add error handling with helpful messages for missing dependencies

### Phase 3: Minimal LaTeX Generation (Proof of Concept)
- [ ] Study DND-5e-LaTeX-Template example.tex structure
- [ ] Create minimal .tex file generator (hardcoded test data)
- [ ] Write function to compile .tex to PDF (subprocess lualatex)
- [ ] Write test: Generate minimal DnD document
- [ ] Write test: Verify PDF output file exists and is valid
- [ ] Add cleanup of auxiliary LaTeX files (.aux, .log, etc.)

### Phase 4: Character Data Model
- [ ] Design character data structure (Python dataclass or Pydantic)
- [ ] Create JSON schema for character data
- [ ] Implement basic character attributes (name, class, race, level)
- [ ] Implement ability scores with modifiers (STR, DEX, CON, INT, WIS, CHA)
- [ ] Add proficiency bonus calculator by level
- [ ] Implement skill modifiers and proficiencies
- [ ] Add saving throws
- [ ] Write test: Character data validation
- [ ] Write test: Ability score modifier calculation (-1 for 8-9, +0 for 10-11, etc.)
- [ ] Write test: Proficiency bonus by level (+2 at 1-4, +3 at 5-8, etc.)

### Phase 5: Character Sheet LaTeX Generator (5e 2014)
- [ ] Create LaTeX Jinja2 template for 5e 2014 character sheet
- [ ] Implement character-to-LaTeX converter using template
- [ ] Add hit points and hit dice rendering
- [ ] Add AC and initiative
- [ ] Add equipment and inventory section
- [ ] Add spells section (if applicable)
- [ ] Create test character JSON file (example fighter)
- [ ] Write test: Generate complete character sheet from test data
- [ ] Write test: Compile character sheet to PDF successfully
- [ ] Add CLI command for testing: `python -m dndsheet generate character.json`

### Phase 6: JSON/YAML File Import & CLI Testing
- [ ] Implement JSON file loader with validation
- [ ] Implement YAML file loader with validation
- [ ] Add multiple example character files (wizard, rogue, cleric)
- [ ] Write test: Load character from JSON file
- [ ] Write test: Load character from YAML file
- [ ] Write test: Validate and reject malformed files
- [ ] Test end-to-end: Load JSON → Generate LaTeX → Compile PDF

---

## 🎯 MILESTONE: Core functionality validated - Ready to build TUI

---

### Phase 7: Textual TUI Foundation
- [ ] Add textual and rich to dependencies
- [ ] Create basic TUI app structure (App class)
- [ ] Implement main menu screen with navigation
- [ ] Add keyboard shortcuts (q=quit, h=help)
- [ ] Create CSS styling with D&D theme colors
- [ ] Write test: TUI launches without errors
- [ ] Write test: Main menu navigation works

### Phase 8: Character Creation TUI Screens
- [ ] Create character creation wizard (multi-screen)
- [ ] Implement form inputs with validation feedback
- [ ] Add ability score input screen (with point buy calculator option)
- [ ] Add class/race selection screens (dropdown/list)
- [ ] Create equipment/inventory input screen
- [ ] Add preview screen showing final character
- [ ] Wire up "Generate PDF" button to existing core functions
- [ ] Write test: Complete character creation flow in TUI

### Phase 9: File Management UI
- [ ] Add "Load Character" screen with file browser widget
- [ ] Add "Save Character" dialog
- [ ] Add "Recent Files" list on main screen
- [ ] Implement drag-and-drop file loading (if supported)
- [ ] Write test: Save and load character through TUI

### Phase 10: Extended Features - Ledgers & Notes
- [ ] Design ledger data structure (items, gold, spells)
- [ ] Create LaTeX template for inventory ledger
- [ ] Create LaTeX template for spell tracking ledger
- [ ] Add ledger management screens to TUI
- [ ] Design notes data structure
- [ ] Create LaTeX template for extended notes pages
- [ ] Add multi-line text input widget for notes
- [ ] Add checkbox in TUI: "Include extended notes"
- [ ] Write test: Generate character sheet with ledgers and notes

### Phase 11: NPC Creator
- [ ] Design NPC data structure (simplified from PC)
- [ ] Create simplified NPC stat block LaTeX template
- [ ] Implement NPC-to-LaTeX converter
- [ ] Add challenge rating calculator with XP lookup
- [ ] Create NPC creation screen in TUI
- [ ] Write test: Generate NPC stat block PDF

### Phase 12: DM Session Tools
- [ ] Design session data structure
- [ ] Create session notes LaTeX template
- [ ] Create encounter planning LaTeX template
- [ ] Add initiative tracker template
- [ ] Add "Session Planner" section to TUI main menu
- [ ] Write test: Generate session notes document

### Phase 13: 2024 Rules Support
- [ ] Research differences between 5e 2014 and 2024 rules
- [ ] Create LaTeX template for 2024 character sheet
- [ ] Implement 2024-specific rule adjustments
- [ ] Add edition selector in TUI (radio button on character creation)
- [ ] Write test: Generate 2024 character sheet
- [ ] Write test: Verify 2024-specific fields are correct

### Phase 14: TUI Polish & User Experience
- [ ] Add comprehensive keyboard shortcuts (F1=help screen)
- [ ] Implement multiple color themes (PHB green, DMG coral, etc.)
- [ ] Add tooltips/help text for all form fields
- [ ] Implement undo/redo for form inputs
- [ ] Create settings screen (default edition, output path, theme)
- [ ] Add progress bars for PDF generation
- [ ] Implement error display with helpful troubleshooting
- [ ] Write test: Keyboard shortcuts work correctly
- [ ] Write test: Settings persist between sessions

### Phase 15: Documentation & Polish
- [ ] Write installation guide (INSTALL.md)
- [ ] Create example usage documentation with TUI screenshots
- [ ] Add man page for TUI application
- [ ] Create comprehensive example character/NPC files library
- [ ] Add troubleshooting guide (common LaTeX errors, etc.)
- [ ] Create video/GIF demo of TUI for README
- [ ] Write integration tests for end-to-end workflows
- [ ] Add contributing guide for new character sheet templates

### Phase 16: Distribution
- [ ] Create installation script
- [ ] Package for distribution (pip/cargo/apt)
- [ ] Add version checking
- [ ] Create release workflow
- [ ] Write test: Installation script works on clean system

## Contributing

This project is currently in initial development. Contributions and ideas welcome.
