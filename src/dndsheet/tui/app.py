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

    # Import functional screens
    from .screens import CharacterFileLoadScreen

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
                yield Button("Create Character Sheet", id="btn-character-new", variant="primary")
                yield Button("Load Character from File", id="btn-character-load")

                yield Static("📚 In-World Documents", classes="section-title")
                yield Button("Create Spell Book", id="btn-spellbook", variant="default")
                yield Button("Create Crafting Guide", id="btn-crafting", variant="default")
                yield Button("Create Custom Book", id="btn-custom-book", variant="default")

                yield Static("🎭 DM Tools", classes="section-title")
                yield Button("Create NPC Sheet", id="btn-npc", variant="default")
                yield Button("Create Session Notes", id="btn-session", variant="default")

                yield Static("🎪 Props & Handouts", classes="section-title")
                yield Button("Create Wanted Poster", id="btn-poster", variant="default")
                yield Button("Create Letter/Document", id="btn-letter", variant="default")

                yield Static("", classes="menu-section")
                yield Button("⚙️  Settings", id="btn-settings", variant="default")
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
            elif button_id == "btn-settings":
                self.app.push_screen("settings")
            else:
                # Placeholder for other features
                self.app.notify(f"Feature not yet implemented: {button_id}", severity="warning")

    class CharacterCreateScreen(Screen):
        """Screen for creating a new character."""

        CSS = """
        CharacterCreateScreen {
            align: center middle;
        }

        #create-container {
            width: 80;
            height: auto;
            border: solid $primary;
            background: $surface;
            padding: 2;
        }
        """

        def compose(self) -> ComposeResult:
            """Create widgets for the character creation screen."""
            with Container(id="create-container"):
                yield Static("✨ Create New Character", id="title")
                yield Static("This feature will be implemented in Phase 8", classes="subtitle")
                yield Button("← Back to Main Menu", id="btn-back", variant="primary")

        def on_button_pressed(self, event: Button.Pressed) -> None:
            """Handle button press."""
            if event.button.id == "btn-back":
                self.app.pop_screen()

    class SettingsScreen(Screen):
        """Settings screen."""

        CSS = """
        SettingsScreen {
            align: center middle;
        }

        #settings-container {
            width: 80;
            height: auto;
            border: solid $primary;
            background: $surface;
            padding: 2;
        }
        """

        def compose(self) -> ComposeResult:
            """Create widgets for settings screen."""
            with Container(id="settings-container"):
                yield Static("⚙️  Settings", id="title")
                yield Static("LaTeX template path, output directory, etc.", classes="subtitle")
                yield Static("This feature will be implemented in Phase 8", classes="subtitle")
                yield Button("← Back to Main Menu", id="btn-back", variant="primary")

        def on_button_pressed(self, event: Button.Pressed) -> None:
            """Handle button press."""
            if event.button.id == "btn-back":
                self.app.pop_screen()

    class DnDSheetApp(App):
        """Main Textual application for D&D Sheet Generator."""

        CSS = """
        Screen {
            background: $background;
        }

        #title {
            text-style: bold;
            color: $accent;
            text-align: center;
            margin: 1;
        }

        .subtitle {
            color: $text-muted;
            text-align: center;
            margin: 1;
        }
        """

        TITLE = "D&D Sheet Generator"
        SUB_TITLE = "Create beautiful D&D documents with LaTeX"

        SCREENS = {
            "main": MainMenuScreen,
            "character_load": CharacterFileLoadScreen,
            "character_create": CharacterCreateScreen,
            "settings": SettingsScreen,
        }

        BINDINGS = [
            ("q", "quit", "Quit"),
            ("escape", "back", "Back"),
        ]

        def on_mount(self) -> None:
            """Called when app is mounted."""
            self.push_screen("main")

        def action_quit(self) -> None:
            """Quit the application."""
            self.exit()

        def action_back(self) -> None:
            """Go back to previous screen."""
            if len(self.screen_stack) > 1:
                self.pop_screen()

    # Run the app
    app = DnDSheetApp()
    app.run()
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
