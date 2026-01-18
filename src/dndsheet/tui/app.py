"""
Main TUI application for dndsheet.

This module defines the primary Textual App class and main screen.
"""

# Check if textual is available before doing anything else
try:
    import textual
    TEXTUAL_AVAILABLE = True
except ImportError:
    TEXTUAL_AVAILABLE = False


def main() -> int:
    """Run the TUI application."""
    if not TEXTUAL_AVAILABLE:
        print("❌ Error: Textual is not installed.")
        print()
        print("To use the TUI, you need to install textual:")
        print("  pip install textual>=0.47.0 rich>=13.0.0")
        print()
        print("Or with a virtual environment:")
        print("  python3 -m venv venv")
        print("  source venv/bin/activate")
        print("  pip install -r requirements.txt")
        print()
        print("For more information, see docs/INSTALLATION.md")
        return 1

    # Only import textual components if available
    from textual.app import App, ComposeResult
    from textual.containers import Container
    from textual.widgets import Static, Button
    from textual.screen import Screen
    from pathlib import Path

    # Import functional screens
    from .screens import CharacterFileLoadScreen, CharacterViewScreen
    from .character_creator import CharacterBasicInfoScreen
    from .spell_screen import SpellScreen
    from .encounter_screen import EncounterScreen # New import

    # Import data models
    from ..character import Character

    class MainMenuScreen(Screen):
        """Main menu screen for document type selection."""

        CSS = """
        MainMenuScreen {
            align: center middle;
        }

        #menu-container {
            width: 80;
            height: auto;
            border: solid $primary;
            background: $surface;
            padding: 2;
        }

        #title {
            text-align: center;
            color: $accent;
            text-style: bold;
            margin-bottom: 1;
        }

        #subtitle {
            text-align: center;
            color: $text-muted;
            margin-bottom: 2;
        }

        Button {
            width: 100%;
            margin: 1;
        }

        .menu-section {
            margin-top: 1;
            margin-bottom: 1;
        }

        .section-title {
            text-style: bold;
            color: $accent;
            margin-top: 1;
        }
        """

        def compose(self) -> ComposeResult:
            """Create child widgets for the main menu."""
            with Container(id="menu-container"):
                yield Static("⚔️  D&D Sheet Generator  ⚔️", id="title")
                yield Static("Create beautiful D&D documents using LaTeX", id="subtitle")

                yield Static("📋 Character Management", classes="section-title")
                yield Button("Create New Character", id="btn-character-new", variant="primary")
                yield Button("Load Character from File", id="btn-character-load")
                yield Button("Create Empty Character Sheet", id="btn-character-empty", variant="default")

                yield Static("📚 In-World Documents", classes="section-title")
                yield Button("Create Empty Book", id="btn-book-empty", variant="default")

                yield Static("🎪 Props & Handouts", classes="section-title")
                yield Button("Create Wanted Poster", id="btn-poster", variant="default")

                yield Static("👹 DM Tools", classes="section-title")
                yield Button("Create Encounter", id="btn-encounter", variant="default") # New button

                yield Static("", classes="menu-section")
                yield Button("❌ Exit", id="btn-exit", variant="error")

        def on_button_pressed(self, event: Button.Pressed) -> None:
            """Handle button press events."""
            button_id = event.button.id

            if button_id == "btn-exit":
                self.app.exit()
            elif button_id == "btn-character-new":
                self.app.push_screen("character_create")
            elif button_id == "btn-character-load":
                self.app.push_screen("character_load")
            elif button_id == "btn-character-empty":
                self.create_empty_character_sheet()
            elif button_id == "btn-book-empty":
                self.create_empty_book()
            elif button_id == "btn-poster":
                self.create_wanted_poster()
            elif button_id == "btn-encounter": # New button handler
                self.app.push_screen("encounter_screen")
            else:
                self.app.notify(f"Feature not yet implemented: {button_id}", severity="warning")

        def create_wanted_poster(self) -> None:
            """Creates a sample wanted poster PDF and QMD."""
            try:
                from ..latex_generator import generate_tex_file, compile_to_pdf
                from ..sheet_generator import render_template
                from ..latex_env import check_dnd_template
                from datetime import datetime

                found, location = check_dnd_template()
                if not found:
                    self.app.notify("DND template not found. Cannot create.", severity="error")
                    return

                self.app.notify("Creating wanted poster...")
                
                image_path = Path("DND-5e-LaTeX-Template/scrot.jpg")
                
                # --- Generate LaTeX and PDF ---
                latex_source = render_template(
                    "wanted_poster.tex.j2",
                    name="The Shadow Viper",
                    crimes="Treason, Horse Thievery, and Unsavory Appetizers",
                    reward_amount="5,000",
                    last_seen_location="The Rusty Flagon Inn",
                    image_path=str(image_path) if image_path.exists() else None,
                    now=datetime.now
                )

                tex_filename = "wanted_poster.tex"
                tex_file = generate_tex_file(latex_source, Path(f"output/{tex_filename}"))
                success_pdf, message_pdf, pdf_path = compile_to_pdf(tex_file, Path("output"), template_path=None)

                # --- Generate QMD ---
                qmd_source = render_template(
                    "wanted_poster.qmd.j2",
                    name="The Shadow Viper",
                    crimes="Treason, Horse Thievery, and Unsavory Appetizers",
                    reward_amount="5,000",
                    last_seen_location="The Rusty Flagon Inn",
                    image_path=str(image_path) if image_path.exists() else None,
                    now=datetime.now
                )
                qmd_filename = "wanted_poster.qmd"
                qmd_path = Path(f"output/{qmd_filename}")
                qmd_path.write_text(qmd_source, encoding='utf-8')
                success_qmd = True # Assuming write_text doesn't fail silently
                
                output_message = f"Created wanted poster: "
                if success_pdf:
                    output_message += f"PDF ({pdf_path.name})"
                if success_qmd:
                    output_message += f", QMD ({qmd_path.name})"
                
                self.app.notify(f"✓ {output_message}", severity="information")

            except Exception as e:
                self.app.notify(f"✗ Error creating wanted poster: {str(e)}", severity="error")

        def create_empty_book(self) -> None:
            """Creates a generic book with a title page and empty chapters (PDF and QMD)."""
            try:
                from ..latex_generator import generate_tex_file, compile_to_pdf
                from ..sheet_generator import render_template
                from ..latex_env import check_dnd_template
                from datetime import datetime

                found, location = check_dnd_template()
                if not found:
                    self.app.notify("DND template not found. Cannot create.", severity="error")
                    return

                self.app.notify("Creating empty book...")
                
                # --- Generate LaTeX and PDF ---
                latex_source = render_template(
                    "generic_book.tex.j2",
                    title="My Grand Adventure",
                    author="A Humble Scribe",
                    num_chapters=5,
                    now=datetime.now
                )
                tex_filename = "empty_book.tex"
                tex_file = generate_tex_file(latex_source, Path(f"output/{tex_filename}"))
                success_pdf, message_pdf, pdf_path = compile_to_pdf(tex_file, Path("output"))

                # --- Generate QMD ---
                qmd_source = render_template(
                    "generic_book.qmd.j2",
                    title="My Grand Adventure",
                    author="A Humble Scribe",
                    num_chapters=5,
                    now=datetime.now
                )
                qmd_filename = "empty_book.qmd"
                qmd_path = Path(f"output/{qmd_filename}")
                qmd_path.write_text(qmd_source, encoding='utf-8')
                success_qmd = True # Assuming write_text doesn't fail silently

                output_message = f"Created empty book: "
                if success_pdf:
                    output_message += f"PDF ({pdf_path.name})"
                if success_qmd:
                    output_message += f", QMD ({qmd_path.name})"
                
                self.app.notify(f"✓ {output_message}", severity="information")

            except Exception as e:
                self.app.notify(f"✗ Error creating empty book: {str(e)}", severity="error")

        def create_empty_character_sheet(self) -> None:
            """Create an empty character sheet with placeholders and notes pages (PDF and QMD)."""
            try:
                from ..latex_generator import generate_tex_file, compile_to_pdf
                from ..sheet_generator import render_template
                from ..latex_env import check_dnd_template
                from datetime import datetime

                found, location = check_dnd_template()
                if not found:
                    self.app.notify("DND template not found. Cannot create.", severity="error")
                    return

                self.app.notify("Creating empty character sheet...")
                
                # --- Generate LaTeX and PDF ---
                latex_source = render_template(
                    "empty_character_sheet.tex.j2",
                    title="Empty Character Sheet",
                    author="D&D Sheet Generator",
                    now=datetime.now
                )
                tex_filename = "empty_character_sheet.tex"
                tex_file = generate_tex_file(latex_source, Path(f"output/{tex_filename}"))
                success_pdf, message_pdf, pdf_path = compile_to_pdf(tex_file, Path("output"))

                # --- Generate QMD ---
                qmd_source = render_template(
                    "empty_character_sheet.qmd.j2",
                    title="Empty Character Sheet",
                    author="D&D Sheet Generator",
                    now=datetime.now
                )
                qmd_filename = "empty_character_sheet.qmd"
                qmd_path = Path(f"output/{qmd_filename}")
                qmd_path.write_text(qmd_source, encoding='utf-8')
                success_qmd = True # Assuming write_text doesn't fail silently

                output_message = f"Created empty character sheet: "
                if success_pdf:
                    output_message += f"PDF ({pdf_path.name})"
                if success_qmd:
                    output_message += f", QMD ({qmd_path.name})"
                
                self.app.notify(f"✓ {output_message}", severity="information")

            except Exception as e:
                self.app.notify(f"✗ Error creating empty character sheet: {str(e)}", severity="error")


    class DnDSheetApp(App[None]):
        """Main Textual application for D&D Sheet Generator."""

        CSS = """
        Screen {
            background: $background;
        }
        """

        TITLE = "D&D Sheet Generator"
        SUB_TITLE = "Create beautiful D&D documents with LaTeX"

        SCREENS = {
            "main": MainMenuScreen,
            "character_load": CharacterFileLoadScreen,
            "character_create": CharacterBasicInfoScreen,
            "character_view": CharacterViewScreen,
            "spell_screen": SpellScreen,
            "encounter_screen": EncounterScreen, # New screen
        }

        BINDINGS = [
            ("q", "quit", "Quit"),
            ("escape", "back", "Back"),
        ]
        
        def __init__(self):
            super().__init__()
            # This holds the currently loaded character state
            self.character: Character | None = None

        def on_mount(self) -> None:
            self.push_screen("main")

        def action_quit(self) -> None:
            self.exit()

        def action_back(self) -> None:
            # Don't pop the main screen
            if len(self.screen_stack) > 1:
                # When going back from view, clear the character
                if isinstance(self.screen, CharacterViewScreen):
                    self.character = None
                self.pop_screen()

    app = DnDSheetApp()
    app.run()
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
