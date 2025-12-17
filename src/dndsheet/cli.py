"""
Command-line interface for dndsheet.

This is a basic CLI for testing core functionality before the TUI is implemented.
"""

import argparse
import sys
from pathlib import Path

from . import __version__


def main() -> int:
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        prog="dndsheet",
        description="D&D Character Sheet Generator using LaTeX",
        epilog="For more information, see: https://github.com/yourusername/Latex-DnDSheet",
    )

    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )

    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose output",
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Generate command (placeholder for Phase 5)
    generate_parser = subparsers.add_parser(
        "generate",
        help="Generate a character sheet from a JSON/YAML file",
    )
    generate_parser.add_argument(
        "input_file",
        type=Path,
        help="Path to character data file (JSON or YAML)",
    )
    generate_parser.add_argument(
        "-o", "--output",
        type=Path,
        help="Output PDF file path (default: character_name.pdf)",
    )

    # Check command for Phase 2
    check_parser = subparsers.add_parser(
        "check",
        help="Check LaTeX environment and dependencies",
    )

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        return 0

    if args.command == "generate":
        print(f"Generate command not yet implemented. Input: {args.input_file}")
        return 1

    if args.command == "check":
        from .latex_env import check_environment, get_installation_instructions

        print("Checking LaTeX environment...\n")
        status = check_environment()

        # LuaLaTeX status
        if status['lualatex']['installed']:
            print(f"✓ LuaLaTeX: {status['lualatex']['info']}")
        else:
            print(f"✗ LuaLaTeX: {status['lualatex']['info']}")

        # DND Template status
        if status['dnd_template']['found']:
            print(f"✓ DND Template: {status['dnd_template']['location']}")
        else:
            print(f"✗ DND Template: {status['dnd_template']['location']}")

        print()

        if status['ready']:
            print("✓ Environment is ready! You can start generating documents.")
            return 0
        else:
            print("✗ Environment setup incomplete. See instructions below:\n")
            instructions = get_installation_instructions()

            if not status['lualatex']['installed']:
                print(instructions['lualatex'])

            if not status['dnd_template']['found']:
                print(instructions['dnd_template'])

            return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
