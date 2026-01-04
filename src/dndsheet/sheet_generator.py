"""
Character sheet LaTeX generator using Jinja2 templates.

This module converts Character objects into D&D-styled LaTeX documents.
"""

from pathlib import Path
from typing import Optional

from jinja2 import Environment, FileSystemLoader, select_autoescape

try:
    from .character import Character, Ability, Skill, SKILL_ABILITIES
except ImportError:
    # Running as script, not as module
    from character import Character, Ability, Skill, SKILL_ABILITIES


def get_template_env() -> Environment:
    """Create and configure Jinja2 environment for LaTeX templates."""
    # Get templates directory relative to this file
    templates_dir = Path(__file__).parent / "templates"

    env = Environment(
        loader=FileSystemLoader(str(templates_dir)),
        autoescape=False,  # Don't autoescape for LaTeX
        trim_blocks=True,
        lstrip_blocks=True, # Set to True for better control over whitespace
    )
    return env


def render_template(template_name: str, **context) -> str:
    """
    Renders a Jinja2 template with the given context.

    Args:
        template_name: The filename of the template to render.
        **context: The data to pass to the template.

    Returns:
        The rendered template as a string.
    """
    env = get_template_env()
    template = env.get_template(template_name)
    return template.render(**context)


def generate_character_sheet_latex(character: Character) -> str:
    """
    Generate LaTeX source for a character sheet.

    Args:
        character: Character object to generate sheet for

    Returns:
        LaTeX source code as a string
    """
    # Prepare context with all necessary data
    all_skills = list(Skill)

    return render_template(
        "character_sheet.tex.j2",
        character=character,
        Ability=Ability,
        Skill=Skill,
        SKILL_ABILITIES=SKILL_ABILITIES,
        ALL_SKILLS=all_skills,
    )


def generate_character_sheet_qmd(character: Character) -> str:
    """
    Generate Quarto Markdown (QMD) source for a character sheet.

    Args:
        character: Character object to generate QMD for

    Returns:
        QMD source code as a string
    """
    all_skills = list(Skill)

    # The 'now()' function is not available in standard Jinja2
    # but could be passed in the context if needed.
    # For simplicity, we'll assume a 'now' context variable if needed,
    # or handle date generation externally. For now, rely on template's `date: "{{ now().strftime('%Y-%m-%d') }}"`
    # and hope Quarto handles it, or Quarto has its own mechanism.
    
    # Passing `datetime` for `now()` in the QMD template.
    from datetime import datetime
    
    return render_template(
        "character_sheet.qmd.j2",
        character=character,
        Ability=Ability,
        Skill=Skill,
        SKILL_ABILITIES=SKILL_ABILITIES,
        ALL_SKILLS=all_skills,
        now=datetime.now
    )


def generate_and_compile_character_sheet(
    character: Character,
    output_dir: Optional[Path] = None,
    template_path: Optional[Path] = None,
    cleanup: bool = True,
) -> tuple[bool, str, Optional[Path], Optional[Path]]: # Added Optional[Path] for qmd_path
    """
    Generate LaTeX source, compile to PDF, and generate Quarto Markdown (QMD) for a character sheet.

    Args:
        character: Character object to generate sheet for
        output_dir: Directory for output files. If None, uses 'output/'.
        template_path: Path to DND-5e-LaTeX-Template. If None, auto-detects.
        cleanup: Whether to clean up auxiliary files

    Returns:
        Tuple of (success: bool, message: str, pdf_path: Optional[Path], qmd_path: Optional[Path])
    """
    try:
        from .latex_generator import generate_tex_file, compile_to_pdf
    except ImportError:
        from latex_generator import generate_tex_file, compile_to_pdf

    if output_dir is None:
        output_dir = Path("output")

    output_dir.mkdir(parents=True, exist_ok=True)

    # Create safe filename from character name
    safe_name = "".join(c if c.isalnum() or c in (' ', '-', '_') else '_' for c in character.name)
    safe_name = safe_name.replace(' ', '_').lower()
    
    # --- Generate LaTeX and PDF ---
    latex_success, latex_message, pdf_path = False, "", None
    try:
        latex_source = generate_character_sheet_latex(character)
        tex_filename = f"{safe_name}_sheet.tex"
        tex_path = output_dir / tex_filename
        tex_file = generate_tex_file(latex_source, tex_path, template_path)
        latex_success, latex_message, pdf_path = compile_to_pdf(
            tex_file,
            output_dir=output_dir,
            template_path=template_path,
            cleanup=cleanup,
        )
    except Exception as e:
        latex_message = f"Failed to generate or compile LaTeX: {str(e)}"

    # --- Generate QMD ---
    qmd_path = None
    qmd_success, qmd_message = False, ""
    try:
        qmd_source = generate_character_sheet_qmd(character)
        qmd_filename = f"{safe_name}_sheet.qmd"
        qmd_path = output_dir / qmd_filename
        qmd_path.write_text(qmd_source, encoding='utf-8')
        qmd_success = True
        qmd_message = f"Generated {qmd_filename}"
    except Exception as e:
        qmd_message = f"Failed to generate QMD: {str(e)}"
    
    overall_success = latex_success and qmd_success
    overall_message = f"PDF: {latex_message}. QMD: {qmd_message}"

    return overall_success, overall_message, pdf_path, qmd_path


# Example usage and testing
if __name__ == "__main__":
    try:
        from .character import AbilityScores
    except ImportError:
        from character import AbilityScores

    print("Testing character sheet generation...\n")

    # Create test character (Grimnar Ironforge)
    grimnar = Character(
        name="Grimnar Ironforge",
        player_name="Test Player",
        race="Mountain Dwarf",
        character_class="Fighter",
        level=5,
        background="Soldier",
        alignment="Lawful Good",
        ability_scores=AbilityScores(
            strength=16,
            dexterity=14,
            constitution=15,
            intelligence=10,
            wisdom=12,
            charisma=8,
        ),
        skill_proficiencies=[
            Skill.ATHLETICS,
            Skill.INTIMIDATION,
            Skill.PERCEPTION,
            Skill.SURVIVAL,
        ],
        saving_throw_proficiencies=[
            Ability.STRENGTH,
            Ability.CONSTITUTION,
        ],
        armor_class=18,
        max_hit_points=42,
        speed=25,
        hit_dice="5d10",
        experience_points=6500,
    )

    print("1. Generating LaTeX source...")
    try:
        latex_source = generate_character_sheet_latex(grimnar)
        print(f"   ✓ Generated {len(latex_source)} characters of LaTeX")
        print()
        print("   Preview (first 500 chars):")
        print("   " + "\n   ".join(latex_source[:500].split('\n')))
        print("   ...")
    except Exception as e:
        print(f"   ✗ Error: {e}")
        exit(1)

    print()
    print("2. Compiling to PDF and generating QMD...")
    success, message, pdf_path, qmd_path = generate_and_compile_character_sheet(
        grimnar,
        output_dir=Path("output"),
    )

    if success:
        print(f"   ✓ {message}")
        if pdf_path and pdf_path.exists():
            print(f"   PDF size: {pdf_path.stat().st_size:,} bytes")
        if qmd_path and qmd_path.exists():
            print(f"   QMD size: {qmd_path.stat().st_size:,} bytes")
        print()
        print("✓ Character sheet generation successful!")
    else:
        print(f"   ✗ {message}")
        print()
        print("✗ Character sheet generation failed")
        exit(1)
