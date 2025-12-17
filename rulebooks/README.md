# D&D Rulebooks Reference Library

This directory contains reference materials for implementing accurate D&D rules in the sheet generator.

## Directory Structure

```
rulebooks/
├── 5e-2014/          # D&D 5th Edition (2014) reference materials
│   ├── classes/      # Class features, spell lists, etc.
│   ├── races/        # Racial traits and abilities
│   ├── spells/       # Spell descriptions and stats
│   └── equipment/    # Items, weapons, armor
├── 2024/             # D&D 2024 (One D&D) reference materials
│   ├── classes/
│   ├── species/      # New term for races in 2024 rules
│   ├── spells/
│   └── equipment/
└── reference/        # General reference materials
    ├── rules/        # Core mechanics, conditions, etc.
    └── calculations/ # Proficiency bonuses, XP tables, CR calculations

```

## Usage

These reference files are used by the application to:
- Validate character data (e.g., valid class features at each level)
- Provide autocomplete/suggestions in the TUI
- Calculate derived stats accurately
- Generate accurate LaTeX output

## File Formats

Reference data should be in structured formats:
- **JSON** - For data that needs to be parsed by the application
- **YAML** - For more human-readable reference files
- **Markdown** - For documentation and rule explanations

## Contributing

When adding reference materials:
1. **DO NOT** include copyrighted text from official books
2. **DO** include mechanical data (stats, numbers, formulas)
3. **DO** cite which sourcebook the information comes from
4. Use a consistent naming scheme: `kebab-case.json`

## Legal Note

This project uses only mechanical data from the D&D 5e SRD (System Reference Document), which is available under the Open Gaming License (OGL). No copyrighted descriptive text or artwork from official books is included.
