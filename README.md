# Latex-DnDSheet

A Linux TUI (Terminal User Interface) application for creating beautiful D&D-themed documents using LaTeX. Generate character sheets, spell books, ledgers, NPC stat blocks, and immersive in-world documents with the authentic look and feel of official D&D materials.

## Project Vision

**More than just character sheets** - this tool empowers DMs and players to create any D&D-themed document:

- 📜 Character sheets with multiple layout options
- 📖 In-world spell books ("The Art of Evocation", "Herbalism Compendium")
- 📋 Ledgers and inventory trackers
- 👤 NPC stat blocks and villain profiles
- 🗺️ Adventure modules and session notes
- 📚 Custom rule books and homebrew content
- 🎭 Props like tavern menus, wanted posters, guild charters

All using professional LaTeX typesetting with the D&D aesthetic.

## Core Philosophy

1. **Template-Based Workflow**: Choose from pre-built templates or customize existing ones
2. **Offline-First**: No internet required - complete creative control
3. **TUI Interface**: Fast, keyboard-driven terminal interface for power users
4. **File-Based**: Save your work as JSON/YAML for version control and collaboration

## Features

### 📄 Document Templates

- **Character Sheets**
  - D&D 2024 rules support
  - D&D 5e (2014) rules support
  - Traditional ledger variants (items, gold, spell tracking)
  - Extended notes and backstory pages

- **In-World Books & Documents**
  - Spell grimoires ("Fireball: Theory and Practice")
  - Crafting guides (Herbalism, Alchemy, Smithing)
  - Lore books and historical texts
  - Guild manuals and organization handbooks
  - Religious texts and prayer books

- **DM Resources**
  - NPC creator with stat blocks
  - Villain profiles with motivations and tactics
  - Session planning and encounter notes
  - Adventure module templates
  - Campaign world-building documents

- **Props & Handouts**
  - Tavern menus and price lists
  - Wanted posters and bounty notices
  - Maps and location descriptions
  - Letters, scrolls, and documents
  - Item cards and treasure descriptions

### 🎨 Template System

- **Choose**: Select from a library of pre-built templates
- **Customize**: Adjust colors, fonts, layout options through TUI
- **Create**: Advanced users can add custom LaTeX templates
- **Share**: Export and share your favorite template configurations

### 💾 Output Options

- Professional D&D-styled PDFs using LaTeX
- Fully offline workflow
- Compatible with VSCodium/VSCode and Overleaf
- Export data as JSON/YAML for backup and sharing

## Technology Stack

- **LaTeX Template**: [rpgtex/DND-5e-LaTeX-Template](https://github.com/rpgtex/DND-5e-LaTeX-Template)
- **Compilation**: LuaLaTeX (recommended)
- **Platform**: Linux

## Status

Early planning and development phase.

## Development Roadmap

> **Strategy**: Build and validate core functionality first (Phases 1-6), then add TUI (Phases 7+)

### Phase 1: Project Setup & Foundation ✅ COMPLETE
- [x] Set up Python project structure (src/dndsheet/, tests/, templates/, docs/)
- [x] Create rulebooks/ directory with reference data (proficiency, modifiers)
- [x] Create pyproject.toml with dependencies (Python 3.10+, jinja2, pydantic, pyyaml)
- [x] Set up pytest for testing
- [x] Create basic CLI entry point (argparse) for testing
- [x] Add .gitignore for Python projects (*.pyc, __pycache__, *.pdf, *.aux, *.log)
- [x] Write test: Python package imports correctly
- [ ] Add CI/CD workflow (GitHub Actions) - DEFERRED to Phase 19

### Phase 2: LaTeX Environment Validation ✅ COMPLETE
- [x] Write function to verify LuaLaTeX installation (subprocess check)
- [x] Write function to check for DND-5e-LaTeX-Template in TEXMFHOME
- [x] Create installation helper (get_installation_instructions function)
- [x] Implement `dndsheet check` CLI command
- [x] Add error handling with helpful messages for missing dependencies
- [ ] Write automated tests (deferred - manual testing confirmed working)

### Phase 3: Minimal LaTeX Generation ✅ COMPLETE
- [x] Study DND-5e-LaTeX-Template example.tex structure
- [x] Create minimal .tex file generator (generate_tex_file function)
- [x] Write function to compile .tex to PDF (compile_to_pdf with two-pass compilation)
- [x] Implement automatic template path detection with TEXINPUTS
- [x] Write test: Generate minimal DnD document
- [x] Write test: Verify PDF output file exists and is valid
- [x] Add cleanup of auxiliary LaTeX files (.aux, .log, etc.)

### Phase 4: Character Data Model ✅ COMPLETE
- [x] Design character data structure (Python dataclass with validation)
- [x] Create JSON schema for character data (to_json/from_json methods)
- [x] Implement basic character attributes (name, class, race, level, background, alignment)
- [x] Implement ability scores with modifiers (STR, DEX, CON, INT, WIS, CHA)
- [x] Add proficiency bonus calculator by level (automated @property)
- [x] Implement skill modifiers and proficiencies (18 skills with ability mapping)
- [x] Add saving throws with proficiency support
- [x] Add combat stats (AC, initiative, HP, hit dice, speed)
- [x] Built-in validation (ability scores 1-30, level 1-20, etc.)
- [x] Tested: Character creation, JSON serialization, calculations verified
- [x] Created example character: examples/characters/grimnar_ironforge.json

### Phase 5: Character Sheet LaTeX Generator ✅ COMPLETE
- [x] Create LaTeX Jinja2 template for character sheets (character_sheet.tex.j2)
- [x] Implement character-to-LaTeX converter using Jinja2 templates
- [x] Add complete ability scores table with modifiers and saves
- [x] Add combat stats (HP, hit dice, AC, initiative, speed)
- [x] Add proficiency bonus display and calculation
- [x] Add skills table (both proficient and all skills)
- [x] Add saving throws with proficiency indicators
- [x] Add character summary sidebar with quick reference
- [x] Tested: Generated Grimnar's character sheet (1.6MB PDF)
- [x] Tested: LaTeX compilation successful with all D&D styling

### Phase 6: JSON/YAML File Import & CLI Testing ✅ COMPLETE
- [x] Implement JSON file loader (Character.from_json method)
- [x] Implement CLI `generate` command with file path and output options
- [x] Add multiple example character files:
  - examples/characters/grimnar_ironforge.json (Fighter)
  - examples/characters/elara_moonwhisper.json (Wizard)
  - examples/characters/shadow_quickblade.json (Rogue)
- [x] Tested: Load character from JSON file (all 3 examples)
- [x] Tested: CLI command `python -m dndsheet generate <file.json>`
- [x] Tested: End-to-end workflow (JSON → LaTeX → PDF)
- [x] All three character sheets generated successfully (~1.6MB each)
- [ ] YAML support - Deferred (JSON is sufficient for Phase 1-6)

---

## 🎯 MILESTONE: Core functionality validated - Ready to build TUI

---

### Phase 7: Textual TUI Foundation ✅ COMPLETE
- [x] Add textual and rich to dependencies (requirements.txt)
- [x] Create docs/INSTALLATION.md with setup instructions
- [x] Create basic TUI app structure (DnDSheetApp class)
- [x] Implement main menu screen with document type selection:
  - ✓ Character Sheets (Create New, Load from File)
  - ✓ In-World Books (Spell Books, Crafting Guides, Custom Books)
  - ✓ DM Tools (NPC Sheets, Session Notes)
  - ✓ Props & Handouts (Wanted Posters, Letters/Documents)
  - ✓ Settings screen
- [x] Add keyboard shortcuts (q=quit, escape=back)
- [x] Create CSS styling with Textual theme system
- [x] Implement screen navigation (push/pop screen stack)
- [x] Add CLI `tui` command
- [x] Graceful error handling when textual not installed
- [x] Created placeholder screens for Phase 8+ features
- [x] Tested: TUI command shows helpful installation message

**Note**: To actually run the TUI, install textual:
```bash
pip install textual>=0.47.0 rich>=13.0.0
```

### Phase 8: File Browser & Character Loading (TUI) ✅ COMPLETE
- [x] Create file browser widget using DirectoryTree
- [x] Implement CharacterFileLoadScreen with file selection
- [x] Connect file browser to character loading
- [x] Integrate with PDF generation backend
- [x] Add notification system for success/error feedback
- [x] Filter to show only .json files as selectable
- [x] Create docs/TUI_USAGE.md with instructions
- [x] Test workflow: Browse → Select → Generate PDF

**Working Features**:
- ✓ Browse file system in TUI
- ✓ Select character JSON files
- ✓ Generate PDFs directly from TUI
- ✓ Visual feedback with notifications
- ✓ Fully integrated with existing backend

### Phase 9: Character Creation TUI Screens ✅ COMPLETE
- [x] Create character creation wizard (3-step multi-screen flow)
- [x] Step 1: Basic info form (name, player, race, class, level, background, alignment)
- [x] Step 2: Ability scores with live modifier calculation
- [x] Step 3: Combat stats (AC, HP, speed, hit dice)
- [x] Implement form validation (required fields, number ranges)
- [x] Add class/race selection with dropdown Select widgets
- [x] Wire up "Create & Generate PDF" to backend
- [x] Save character to JSON automatically
- [x] Generate PDF directly from wizard
- [x] Navigation: Next/Back buttons between steps
- [x] Cancel button to return to main menu

**Working Features**:
- ✓ 3-step wizard for creating characters from scratch
- ✓ Dropdowns for race (9 options), class (12 options), alignment (9 options)
- ✓ Real-time ability modifier calculation as you type
- ✓ Validation on all numeric inputs (level 1-20, abilities 1-30, etc.)
- ✓ Automatically saves to output/{character_name}.json
- ✓ Generates PDF immediately after creation
- ✓ Full error handling with notifications

### Phase 10: File Management UI
- [ ] Add "Load Document" screen with file browser widget
- [ ] Add "Save Document" dialog with format selection (JSON/YAML)
- [ ] Add "Recent Files" list on main screen
- [ ] Implement drag-and-drop file loading (if supported)
- [ ] Add "Export PDF" and "Export LaTeX" options
- [ ] Write test: Save and load documents through TUI

### Phase 11: In-World Book Creator (Spellbooks, Guides)
- [ ] Design book data structure (title, author, chapters, content)
- [ ] Create LaTeX templates for different book types:
  - Spell grimoire (e.g., "The Art of Fireball")
  - Crafting guide (Herbalism, Alchemy, Smithing)
  - Lore book (History, Religion, Arcana)
  - Guild manual
- [ ] Implement rich text editor for book content (markdown-like)
- [ ] Add chapter/section management UI
- [ ] Add spell/recipe/item insertion helpers
- [ ] Create book cover generator with custom titles
- [ ] Write test: Generate spell book PDF
- [ ] Write test: Generate crafting guide PDF

### Phase 12: Props & Handouts Creator
- [ ] Design prop templates:
  - Wanted poster
  - Tavern menu
  - Letter/scroll
  - Bounty notice
  - Guild charter
  - Item card
- [ ] Create simple form-based UI for props
- [ ] Add image insertion for prop backgrounds
- [ ] Implement text formatting (fonts, sizes, styles)
- [ ] Add border/decoration options
- [ ] Write test: Generate wanted poster PDF
- [ ] Write test: Generate tavern menu PDF

### Phase 13: Extended Features - Ledgers & Notes
- [ ] Design ledger data structure (items, gold, spells)
- [ ] Create LaTeX template for inventory ledger
- [ ] Create LaTeX template for spell tracking ledger
- [ ] Add ledger management screens to TUI
- [ ] Design notes data structure
- [ ] Create LaTeX template for extended notes pages
- [ ] Add multi-line text input widget for notes
- [ ] Add checkbox in TUI: "Include extended notes"
- [ ] Write test: Generate character sheet with ledgers and notes

### Phase 14: NPC Creator
- [ ] Design NPC data structure (simplified from PC)
- [ ] Create simplified NPC stat block LaTeX template
- [ ] Implement NPC-to-LaTeX converter
- [ ] Add challenge rating calculator with XP lookup
- [ ] Create NPC creation screen in TUI
- [ ] Add NPC personality/motivation generators
- [ ] Write test: Generate NPC stat block PDF

### Phase 15: DM Session Tools
- [ ] Design session data structure
- [ ] Create session notes LaTeX template
- [ ] Create encounter planning LaTeX template
- [ ] Add initiative tracker template
- [ ] Add "Session Planner" section to TUI main menu
- [ ] Create session recap generator
- [ ] Write test: Generate session notes document

### Phase 16: 2024 Rules Support
- [ ] Research differences between 5e 2014 and 2024 rules
- [ ] Create LaTeX template for 2024 character sheet
- [ ] Implement 2024-specific rule adjustments
- [ ] Add edition selector in TUI (radio button on character creation)
- [ ] Update in-world books for 2024 rules compatibility
- [ ] Write test: Generate 2024 character sheet
- [ ] Write test: Verify 2024-specific fields are correct

### Phase 17: Template Marketplace & Sharing
- [ ] Design template package format (.dndtemplate files)
- [ ] Create template import/export functionality
- [ ] Add template metadata editor (description, author, preview image)
- [ ] Implement template validation and safety checks
- [ ] Add "Browse Community Templates" screen
- [ ] Write test: Import/export custom template
- [ ] Create documentation for template creators

### Phase 18: TUI Polish & User Experience
- [ ] Add comprehensive keyboard shortcuts (F1=help screen)
- [ ] Implement multiple color themes (PHB green, DMG coral, etc.)
- [ ] Add tooltips/help text for all form fields
- [ ] Implement undo/redo for form inputs
- [ ] Create settings screen (default edition, output path, theme)
- [ ] Add progress bars for PDF generation
- [ ] Implement error display with helpful troubleshooting
- [ ] Write test: Keyboard shortcuts work correctly
- [ ] Write test: Settings persist between sessions

### Phase 19: Documentation & Polish
- [ ] Write installation guide (INSTALL.md)
- [ ] Create example usage documentation with TUI screenshots
- [ ] Add man page for TUI application
- [ ] Create comprehensive example files library:
  - Character sheets
  - Spell books
  - Props and handouts
  - NPC stat blocks
- [ ] Add troubleshooting guide (common LaTeX errors, etc.)
- [ ] Create video/GIF demos of TUI for README
- [ ] Write integration tests for end-to-end workflows
- [ ] Add contributing guide for template creators
- [ ] Create template development tutorial

### Phase 20: Distribution
- [ ] Create installation script
- [ ] Package for distribution (pip/cargo/apt)
- [ ] Add version checking
- [ ] Create release workflow
- [ ] Write test: Installation script works on clean system

## Contributing

This project is currently in initial development. Contributions and ideas welcome.
