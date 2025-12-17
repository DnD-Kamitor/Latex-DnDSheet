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
        print("Check command not yet implemented.")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
