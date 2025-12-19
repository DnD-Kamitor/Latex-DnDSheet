"""
TUI screens for character loading and generation.

This module contains the actual functional screens for the TUI.
"""

from pathlib import Path

try:
    from textual.app import ComposeResult
    from textual.containers import Container, Vertical, Horizontal, ScrollableContainer
    from textual.widgets import Static, Button, DirectoryTree, Label, Footer
    from textual.screen import Screen
    from textual import on
    TEXTUAL_AVAILABLE = True
except ImportError:
    TEXTUAL_AVAILABLE = False
    # Dummy classes for when textual isn't installed
    from typing import Any
    ComposeResult = Any
    Screen = type('Screen', (), {})
    Container = type('Container', (), {})
    DirectoryTree = type('DirectoryTree', (), {})
    Static = type('Static', (), {})
    Button = type('Button', (), {})


if TEXTUAL_AVAILABLE:
    class CharacterFileLoadScreen(Screen):
        """Screen for browsing and loading character JSON files."""

        CSS = """
        CharacterFileLoadScreen {
            align: center middle;
        }

        #load-container {
            width: 90;
            height: 85%;
            border: solid $primary;
            background: $surface;
            padding: 1;
        }

        #title {
            text-align: center;
            color: $accent;
            text-style: bold;
            margin-bottom: 1;
        }

        #instructions {
            text-align: center;
            color: $text-muted;
            margin-bottom: 1;
        }

        DirectoryTree {
            height: 1fr;
            margin: 1;
            border: solid $primary;
        }

        #button-bar {
            height: auto;
            margin-top: 1;
        }

        #selected-file {
            color: $accent;
            margin: 1;
        }

        Button {
            margin: 0 1;
        }
        """

        def __init__(self):
            super().__init__()
            self.selected_file = None

        def compose(self) -> ComposeResult:
            """Create widgets for the file browser."""
            with Container(id="load-container"):
                yield Static("📂 Load Character from File", id="title")
                yield Static("Browse and select a character JSON file", id="instructions")

                # Start from examples/characters directory if it exists
                start_path = Path("examples/characters")
                if not start_path.exists():
                    start_path = Path(".")

                yield DirectoryTree(start_path, id="file-tree")
                yield Label("No file selected", id="selected-file")

                with Horizontal(id="button-bar"):
                    yield Button("Generate PDF", id="btn-generate", variant="primary", disabled=True)
                    yield Button("← Back", id="btn-back", variant="default")

        @on(DirectoryTree.FileSelected)
        def on_file_selected(self, event: DirectoryTree.FileSelected) -> None:
            """Handle file selection."""
            file_path = event.path

            # Only enable generate button for .json files
            if file_path.suffix == '.json':
                self.selected_file = file_path
                self.query_one("#selected-file", Label).update(f"Selected: {file_path.name}")
                self.query_one("#btn-generate", Button).disabled = False
            else:
                self.selected_file = None
                self.query_one("#selected-file", Label).update("Please select a .json file")
                self.query_one("#btn-generate", Button).disabled = True

        def on_button_pressed(self, event: Button.Pressed) -> None:
            """Handle button presses."""
            button_id = event.button.id

            if button_id == "btn-back":
                self.app.pop_screen()
            elif button_id == "btn-generate" and self.selected_file:
                # Import here to avoid circular imports
                from ..character import Character
                from ..sheet_generator import generate_and_compile_character_sheet

                try:
                    # Load character
                    self.app.notify(f"Loading {self.selected_file.name}...")
                    character = Character.from_json(self.selected_file)

                    # Generate PDF
                    self.app.notify(f"Generating PDF for {character.name}...")
                    success, message, pdf_path = generate_and_compile_character_sheet(
                        character,
                        output_dir=Path("output"),
                    )

                    if success:
                        self.app.notify(
                            f"✓ Success! Created {pdf_path.name}",
                            severity="information",
                            timeout=5
                        )
                    else:
                        self.app.notify(
                            f"✗ Error: {message}",
                            severity="error",
                            timeout=10
                        )

                except Exception as e:
                    self.app.notify(
                        f"✗ Error: {str(e)}",
                        severity="error",
                        timeout=10
                    )
