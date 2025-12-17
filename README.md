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
- [ ] Implement main menu screen with document type selection
  - Character Sheets
  - In-World Books (Spellbooks, Guides)
  - DM Tools (NPCs, Sessions)
  - Props & Handouts
  - Custom Templates
- [ ] Add keyboard shortcuts (q=quit, h=help, arrows=navigation)
- [ ] Create CSS styling with D&D theme colors (PHB green, parchment)
- [ ] Write test: TUI launches without errors
- [ ] Write test: Main menu navigation works

### Phase 8: Template Selection System
- [ ] Design template metadata structure (JSON schema)
- [ ] Create template registry/catalog
- [ ] Implement template browser UI (list/grid view)
- [ ] Add template preview functionality (show description, example)
- [ ] Add template categories and filtering
- [ ] Write test: Template registry loads correctly
- [ ] Write test: Filter templates by category

### Phase 9: Character Creation TUI Screens
- [ ] Create character creation wizard (multi-screen)
- [ ] Implement form inputs with validation feedback
- [ ] Add ability score input screen (with point buy calculator option)
- [ ] Add class/race selection screens (dropdown/list)
- [ ] Create equipment/inventory input screen
- [ ] Add preview screen showing final character
- [ ] Wire up "Generate PDF" button to existing core functions
- [ ] Write test: Complete character creation flow in TUI

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
