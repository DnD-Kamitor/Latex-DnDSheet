# D&D LaTeX Examples

This directory contains example D&D documents that you can edit and compile manually.

## Directory Structure

```
examples/
├── latex/                  # LaTeX source files (.tex)
│   ├── character_example.tex   # Full character sheet example
│   └── npc_example.tex         # NPC stat block examples
├── output/                 # Compiled PDFs go here (gitignored)
└── README.md              # This file
```

## Prerequisites

Before compiling, make sure you have:

1. **LuaLaTeX** installed
   ```bash
   # Check if installed
   which lualatex

   # If not installed (Debian/Ubuntu)
   sudo apt install texlive-full
   ```

2. **DND-5e-LaTeX-Template** cloned in the repository root
   ```bash
   # Should already exist at:
   # /home/chris/Documents/github/Latex-DnDSheet/DND-5e-LaTeX-Template/
   ```

## How to Compile Manually

### Method 1: Using the Helper Script (Recommended)

From the repository root:

```bash
# Compile character example
./examples/compile.sh character_example

# Compile NPC example
./examples/compile.sh npc_example

# Compile any .tex file in examples/latex/
./examples/compile.sh your_file_name
```

The compiled PDF will be in `examples/output/`

### Method 2: Manual Compilation

From the repository root directory:

```bash
cd examples/latex

# Set TEXINPUTS to find the DND template
export TEXINPUTS=../../DND-5e-LaTeX-Template//:

# Compile the document (run twice for proper references)
lualatex -output-directory=../output character_example.tex
lualatex -output-directory=../output character_example.tex

# View the PDF
xdg-open ../output/character_example.pdf
```

### Method 3: One-Line Compilation

From the repository root:

```bash
TEXINPUTS=./DND-5e-LaTeX-Template//: lualatex -output-directory=examples/output examples/latex/character_example.tex
```

## Cleaning Up Auxiliary Files

LaTeX generates several auxiliary files (.aux, .log, .out, etc.). To clean them up:

```bash
# From the examples directory
cd output
rm -f *.aux *.log *.out *.toc
```

Or use the helper script:

```bash
./examples/compile.sh clean
```

## Editing the Examples

### Character Example ([character_example.tex](latex/character_example.tex))

This is a complete character sheet for **Grimnar Ironforge**, a level 5 Mountain Dwarf Fighter (Battle Master).

**What you can edit:**
- Character name, class, level, race
- Ability scores and modifiers
- Skills, features, equipment
- Personality traits
- Any section you want!

**Sections included:**
- Basic character information
- Ability scores and saves
- Combat stats (AC, HP, Initiative)
- Skills
- Racial traits
- Class features
- Equipment and weapons
- Personality traits
- Wealth

### NPC Example ([npc_example.tex](latex/npc_example.tex))

This file contains three example NPCs with full stat blocks:

1. **Elara Moonwhisper** - Friendly wizard NPC (CR 3)
2. **Captain Blackthorn** - Hostile fighter NPC (CR 5)
3. **Grimble Tinkertop** - Neutral merchant gnome (CR 1/8)
4. **Goblin Scout** - Common enemy (CR 1/4)

**What you can edit:**
- NPC names and descriptions
- Ability scores
- Spells and attacks
- Challenge ratings
- Any stat you need to adjust

## Tips for Editing

1. **Start small**: Make one change at a time and recompile to see the effect

2. **Common edits**:
   ```latex
   % Change character name
   \chapter*{Your Character Name}

   % Change an ability score
   Strength & 18 & +4 & +7 & Yes \\

   % Add a new skill
   Acrobatics (DEX) & +5 \\

   % Change equipment
   \item Longsword instead of battleaxe
   ```

3. **Use D&D template features**:
   - `\begin{DndTable}` - For stat tables
   - `\begin{DndComment}` - For highlighted notes
   - `\begin{DndReadAloud}` - For flavor text
   - `\begin{DndSidebar}` - For side notes
   - `\begin{DndMonster}` - For stat blocks

4. **Compile frequently**: Catch LaTeX errors early by compiling after each change

## Troubleshooting

### Error: "File 'dndbook.cls' not found"

**Solution**: Make sure you're using `TEXINPUTS` to point to the DND template:
```bash
TEXINPUTS=./DND-5e-LaTeX-Template//: lualatex yourfile.tex
```

### Error: "Undefined control sequence"

**Solution**: You might be using a command that doesn't exist. Check:
- Typos in command names (e.g., `\DndTabel` instead of `\DndTable`)
- Missing packages
- Syntax errors in your LaTeX

### PDF has wrong references or "??" marks

**Solution**: Compile twice to resolve cross-references:
```bash
lualatex yourfile.tex
lualatex yourfile.tex  # Second pass
```

### Fonts look wrong

**Solution**: Make sure you're using LuaLaTeX, not pdflatex:
```bash
lualatex yourfile.tex  # Correct
pdflatex yourfile.tex  # Wrong - will have font issues
```

## Learning More

- **DND Template Documentation**: See `DND-5e-LaTeX-Template/README.md`
- **Example File**: Check `DND-5e-LaTeX-Template/example.tex` for more features
- **LaTeX Basics**: https://www.overleaf.com/learn/latex/Learn_LaTeX_in_30_minutes

## Next Steps

Once you're comfortable editing and compiling manually:
1. The Python application will automate this process
2. The TUI will provide a visual interface for creating characters
3. You'll be able to save character data as JSON and auto-generate PDFs

For now, enjoy manually crafting your D&D documents!
