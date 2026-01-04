"""
TUI screens for character loading and generation.

This module contains the actual functional screens for the TUI.
"""

from pathlib import Path

try:
    from textual.app import ComposeResult
    from textual.containers import Container, Vertical, Horizontal
    from textual.widgets import Static, Button, DirectoryTree, Label, Footer
    from textual.screen import Screen
    from textual import on, log

    from ..character import Character
    from .spell_screen import SpellScreen
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
    Character = Any
    SpellScreen = Any


if TEXTUAL_AVAILABLE:
    class CharacterFileLoadScreen(Screen):
        """Screen for browsing and loading character JSON files."""

        CSS_PATH = "character_creator.css" # Re-use some styles

        def __init__(self):
            super().__init__()
            self.selected_file: Path | None = None

        def compose(self) -> ComposeResult:
            """Create widgets for the file browser."""
            with Container(id="creator-container"):
                yield Static("📂 Load Character from File", id="creator-title")
                yield Static("Browse and select a character JSON file", id="creator-subtitle")

                start_path = Path("examples/characters")
                if not start_path.is_dir():
                    start_path = Path(".")

                yield DirectoryTree(start_path, id="file-tree")
                yield Label("No file selected", id="selected-file")

                with Horizontal(classes="button-bar"):
                    yield Button("Load Character", id="btn-load", variant="primary", disabled=True)
                    yield Button("← Back", id="btn-back")

        @on(DirectoryTree.FileSelected)
        def on_file_selected(self, event: DirectoryTree.FileSelected) -> None:
            """Handle file selection."""
            file_path = event.path
            if file_path.suffix == '.json':
                self.selected_file = file_path
                self.query_one("#selected-file", Label).update(f"Selected: {file_path.name}")
                self.query_one("#btn-load", Button).disabled = False
            else:
                self.selected_file = None
                self.query_one("#selected-file", Label).update("Please select a .json file")
                self.query_one("#btn-load", Button).disabled = True

        def on_button_pressed(self, event: Button.Pressed) -> None:
            """Handle button presses."""
            if event.button.id == "btn-back":
                self.app.pop_screen()
            elif event.button.id == "btn-load" and self.selected_file:
                try:
                    self.app.notify(f"Loading {self.selected_file.name}...")
                    character = Character.from_json(self.selected_file)
                    # Store character in app context and switch to view screen
                    self.app.character = character
                    self.app.push_screen(CharacterViewScreen(character))
                except Exception as e:
                    log.error(f"Failed to load character: {e}")
                    self.app.notify(f"✗ Error: {e}", severity="error", timeout=10)


    class CharacterViewScreen(Screen):
        """Displays a loaded character and provides actions."""

        CSS_PATH = "character_creator.css"

        def __init__(self, character: Character):
            super().__init__()
            self.character = character

        def compose(self) -> ComposeResult:
            with Container(id="creator-container"):
                yield Static(f"Character: {self.character.name}", id="creator-title")
                
                info = (
                    f"[b]Class:[/b] {self.character.character_class} | "
                    f"[b]Level:[/b] {self.character.level} | "
                    f"[b]Race:[/b] {self.character.race}"
                )
                yield Static(info, id="creator-subtitle")

                with Vertical(classes="button-bar"):
                    if self.character.spellcasting_ability:
                        yield Button("View Spells", id="btn-spells", variant="success")
                    yield Button("Generate PDF", id="btn-generate", variant="primary")
                    yield Button("← Back", id="btn-back")

        def on_button_pressed(self, event: Button.Pressed) -> None:
            if event.button.id == "btn-back":
                self.app.pop_screen()
            elif event.button.id == "btn-spells":
                self.app.push_screen(SpellScreen(self.character))
            elif event.button.id == "btn-generate":
                self.generate_pdf()

        def generate_pdf(self) -> None:
            """Generates the character sheet PDF and QMD."""
            from ..sheet_generator import generate_and_compile_character_sheet
            try:
                self.app.notify(f"Generating documents for {self.character.name}...")
                success, message, pdf_path, qmd_path = generate_and_compile_character_sheet(
                    self.character,
                    output_dir=Path("output"),
                )
                if success:
                    output_message = f"✓ Success! Created "
                    if pdf_path:
                        output_message += f"PDF: {pdf_path.name}"
                    if qmd_path:
                        output_message += f", QMD: {qmd_path.name}"
                    self.app.notify(output_message, timeout=7)
                else:
                    self.app.notify(f"✗ Generation Error: {message}", severity="error", timeout=10)
            except Exception as e:
                log.error(f"Failed to generate documents: {e}")
                self.app.notify(f"✗ App Error: {e}", severity="error", timeout=10)
