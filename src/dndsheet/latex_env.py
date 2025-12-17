"""
LaTeX environment validation and helper functions.

This module provides functions to check if the required LaTeX environment is properly set up.
"""

import shutil
import subprocess
from pathlib import Path
from typing import Optional, Tuple


def verify_lualatex() -> Tuple[bool, str]:
    """
    Check if LuaLaTeX is installed and accessible.

    Returns:
        Tuple of (is_installed: bool, version_or_error: str)
    """
    lualatex_path = shutil.which("lualatex")

    if not lualatex_path:
        return False, "LuaLaTeX not found in PATH. Please install TeX Live."

    try:
        result = subprocess.run(
            ["lualatex", "--version"],
            capture_output=True,
            text=True,
            timeout=5,
        )

        if result.returncode == 0:
            # Extract first line with version info
            version_line = result.stdout.split('\n')[0]
            return True, version_line
        else:
            return False, f"LuaLaTeX found but failed to run: {result.stderr}"

    except subprocess.TimeoutExpired:
        return False, "LuaLaTeX command timed out"
    except Exception as e:
        return False, f"Error checking LuaLaTeX: {str(e)}"


def check_dnd_template(search_paths: Optional[list[Path]] = None) -> Tuple[bool, str]:
    """
    Check if the DND-5e-LaTeX-Template is available.

    Args:
        search_paths: Optional list of paths to search. If None, uses default locations.

    Returns:
        Tuple of (is_found: bool, location_or_error: str)
    """
    if search_paths is None:
        search_paths = []

        # Check local project directory first
        project_root = Path(__file__).parent.parent.parent
        local_template = project_root / "DND-5e-LaTeX-Template"
        search_paths.append(local_template)

        # Check TEXMFHOME
        try:
            result = subprocess.run(
                ["kpsewhich", "-var-value", "TEXMFHOME"],
                capture_output=True,
                text=True,
                timeout=5,
            )
            if result.returncode == 0:
                texmfhome = Path(result.stdout.strip())
                search_paths.append(texmfhome / "tex" / "latex" / "dnd")
                search_paths.append(texmfhome / "tex" / "latex" / "DND-5e-LaTeX-Template")
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass  # kpsewhich not available, skip TEXMFHOME

    # Search for dndbook.cls in each path
    for path in search_paths:
        cls_file = path / "dndbook.cls"
        if cls_file.exists():
            return True, str(path.absolute())

    # Try using kpsewhich to find it
    try:
        result = subprocess.run(
            ["kpsewhich", "dndbook.cls"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        if result.returncode == 0 and result.stdout.strip():
            found_path = Path(result.stdout.strip()).parent
            return True, str(found_path)
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass

    return False, "DND-5e-LaTeX-Template not found. Please install or clone to project root."


def get_installation_instructions() -> dict[str, str]:
    """
    Get installation instructions for missing dependencies.

    Returns:
        Dictionary with keys 'lualatex' and 'dnd_template' containing installation instructions.
    """
    return {
        "lualatex": """
LuaLaTeX Installation:

Debian/Ubuntu:
    sudo apt update
    sudo apt install texlive-full

Arch Linux:
    sudo pacman -S texlive-bin texlive-core texlive-latexextra

macOS (Homebrew):
    brew install --cask mactex

After installation, verify with:
    lualatex --version
""",
        "dnd_template": """
DND-5e-LaTeX-Template Installation:

Option 1 - Local (Recommended for development):
    cd /path/to/Latex-DnDSheet
    git clone https://github.com/rpgtex/DND-5e-LaTeX-Template.git

Option 2 - System-wide:
    mkdir -p "$(kpsewhich -var-value TEXMFHOME)/tex/latex/"
    cd "$(kpsewhich -var-value TEXMFHOME)/tex/latex/"
    git clone https://github.com/rpgtex/DND-5e-LaTeX-Template.git dnd

Verify installation:
    kpsewhich dndbook.cls
""",
    }


def check_environment() -> dict:
    """
    Check the complete LaTeX environment setup.

    Returns:
        Dictionary with status of all components:
        {
            'lualatex': {'installed': bool, 'info': str},
            'dnd_template': {'found': bool, 'location': str},
            'ready': bool  # True if everything is ready
        }
    """
    lualatex_ok, lualatex_info = verify_lualatex()
    template_ok, template_info = check_dnd_template()

    return {
        'lualatex': {
            'installed': lualatex_ok,
            'info': lualatex_info,
        },
        'dnd_template': {
            'found': template_ok,
            'location': template_info,
        },
        'ready': lualatex_ok and template_ok,
    }


if __name__ == "__main__":
    """Quick test of environment check."""
    print("Checking LaTeX environment...\n")

    status = check_environment()

    print(f"LuaLaTeX: {'✓' if status['lualatex']['installed'] else '✗'}")
    print(f"  {status['lualatex']['info']}\n")

    print(f"DND Template: {'✓' if status['dnd_template']['found'] else '✗'}")
    print(f"  {status['dnd_template']['location']}\n")

    if status['ready']:
        print("✓ Environment is ready!")
    else:
        print("✗ Environment setup incomplete.")
        print("\nInstallation instructions:")
        instructions = get_installation_instructions()

        if not status['lualatex']['installed']:
            print(instructions['lualatex'])

        if not status['dnd_template']['found']:
            print(instructions['dnd_template'])
