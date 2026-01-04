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
    from .character_creator import CharacterBasicInfoScreen

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
                yield Button("Create Empty Character Sheet", id="btn-character-empty", variant="default")
                yield Button("Create Character and Fill It In", id="btn-character-new", variant="primary")
                yield Button("Load Character from File", id="btn-character-load")

                yield Static("📚 In-World Documents", classes="section-title")
                yield Button("Create Empty Book (Placeholders)", id="btn-book-empty", variant="default")
                yield Button("Create Spell Book", id="btn-spellbook", variant="default")
                yield Button("Create Crafting Guide", id="btn-crafting", variant="default")

                yield Static("🎭 DM Tools", classes="section-title")
                yield Button("Create NPC and Fill It In", id="btn-npc", variant="default")
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
            elif button_id == "btn-character-empty":
                self.create_empty_character_sheet()
            elif button_id == "btn-book-empty":
                self.create_empty_book()
            elif button_id == "btn-npc":
                self.create_npc()
            elif button_id == "btn-settings":
                self.app.push_screen("settings")
            else:
                # Placeholder for other features
                self.app.notify(f"Feature not yet implemented: {button_id}", severity="warning")

        def create_empty_character_sheet(self) -> None:
            """Create an empty character sheet with placeholders."""
            try:
                from ..latex_generator import generate_tex_file, compile_to_pdf
                from ..latex_env import check_dnd_template

                # Check if DND template is available
                found, location = check_dnd_template()
                if not found:
                    self.app.notify("DND template not found. Cannot create empty character sheet.", severity="error")
                    return

                # Generate empty character sheet template
                empty_content = r"""\documentclass[letterpaper,twocolumn,openany]{dndbook}

\usepackage[english]{babel}
\usepackage[utf8]{inputenc}
\usepackage{graphicx}

\title{Character Sheet}
\author{D&D Sheet Generator}
\date{\today}

\begin{document}

\maketitle

\begin{DndComment}{Character Information}
    \textbf{Name:} \underline{\hspace{6cm}} \\
    \textbf{Player:} \underline{\hspace{6cm}} \\
    \textbf{Race:} \underline{\hspace{6cm}} \\
    \textbf{Class:} \underline{\hspace{6cm}} \\
    \textbf{Level:} \underline{\hspace{6cm}} \\
    \textbf{Background:} \underline{\hspace{6cm}} \\
    \textbf{Alignment:} \underline{\hspace{6cm}}
\end{DndComment}

\section*{Ability Scores}
\begin{DndTable}[header=Ability Scores]{lcccccc}
    \textbf{Ability} & \textbf{Score} & \textbf{Modifier} & \textbf{Save} & \textbf{Prof?} & \textbf{Total} \\
    Strength & \underline{\hspace{1cm}} & \underline{\hspace{1cm}} & \underline{\hspace{1cm}} & \square & \underline{\hspace{1cm}} \\
    Dexterity & \underline{\hspace{1cm}} & \underline{\hspace{1cm}} & \underline{\hspace{1cm}} & \square & \underline{\hspace{1cm}} \\
    Constitution & \underline{\hspace{1cm}} & \underline{\hspace{1cm}} & \underline{\hspace{1cm}} & \square & \underline{\hspace{1cm}} \\
    Intelligence & \underline{\hspace{1cm}} & \underline{\hspace{1cm}} & \underline{\hspace{1cm}} & \square & \underline{\hspace{1cm}} \\
    Wisdom & \underline{\hspace{1cm}} & \underline{\hspace{1cm}} & \underline{\hspace{1cm}} & \square & \underline{\hspace{1cm}} \\
    Charisma & \underline{\hspace{1cm}} & \underline{\hspace{1cm}} & \underline{\hspace{1cm}} & \square & \underline{\hspace{1cm}} \\
\end{DndTable}

\section*{Skills}
\begin{DndTable}[header=Skills]{lcc}
    \textbf{Skill} & \textbf{Ability} & \textbf{Prof?} \\
    Acrobatics & Dex & \square \\
    Animal Handling & Wis & \square \\
    Arcana & Int & \square \\
    Athletics & Str & \square \\
    Deception & Cha & \square \\
    History & Int & \square \\
    Insight & Wis & \square \\
    Intimidation & Cha & \square \\
    Investigation & Int & \square \\
    Medicine & Wis & \square \\
    Nature & Int & \square \\
    Perception & Wis & \square \\
    Performance & Cha & \square \\
    Persuasion & Cha & \square \\
    Religion & Int & \square \\
    Sleight of Hand & Dex & \square \\
    Stealth & Dex & \square \\
    Survival & Wis & \square \\
\end{DndTable}

\section*{Combat Statistics}
\begin{DndTable}[header=Combat]{lcc}
    \textbf{Statistic} & \textbf{Value} & \textbf{Notes} \\
    Armor Class & \underline{\hspace{2cm}} & \\
    Initiative & \underline{\hspace{2cm}} & \\
    Speed & \underline{\hspace{2cm}} & \\
    Hit Points (Max) & \underline{\hspace{2cm}} & \\
    Hit Dice & \underline{\hspace{2cm}} & \\
    Death Saves & \square \square \square & \\
\end{DndTable}

\section*{Equipment}
\begin{DndTable}[header=Equipment]{lp{10cm}}
    \textbf{Item} & \textbf{Description} \\
    \underline{\hspace{3cm}} & \underline{\hspace{10cm}} \\
    \underline{\hspace{3cm}} & \underline{\hspace{10cm}} \\
    \underline{\hspace{3cm}} & \underline{\hspace{10cm}} \\
    \underline{\hspace{3cm}} & \underline{\hspace{10cm}} \\
    \underline{\hspace{3cm}} & \underline{\hspace{10cm}} \\
\end{DndTable}

\section*{Notes and Ledgers}
\begin{DndComment}{Adventure Notes}
    \vspace{5cm}
\end{DndComment}

\begin{DndComment}{Quest Log}
    \vspace{5cm}
\end{DndComment}

\begin{DndComment}{Character Development}
    \vspace{5cm}
\end{DndComment}

\end{document}
"""

                # Generate and compile
                self.app.notify("Creating empty character sheet...")
                tex_file = generate_tex_file(empty_content, Path("output/empty_character_sheet.tex"))
                success, message, pdf_path = compile_to_pdf(tex_file, Path("output"))

                if success:
                    self.app.notify(f"✓ Created empty character sheet: {pdf_path.name}", severity="information")
                else:
                    self.app.notify(f"✗ Error: {message}", severity="error")

            except Exception as e:
                self.app.notify(f"✗ Error creating empty character sheet: {str(e)}", severity="error")

        def create_empty_book(self) -> None:
            """Create an empty book with placeholders."""
            try:
                from ..latex_generator import generate_tex_file, compile_to_pdf
                from ..latex_env import check_dnd_template

                # Check if DND template is available
                found, location = check_dnd_template()
                if not found:
                    self.app.notify("DND template not found. Cannot create empty book.", severity="error")
                    return

                # Generate empty book template
                empty_content = r"""\documentclass[letterpaper,twocolumn,openany]{dndbook}

\usepackage[english]{babel}
\usepackage[utf8]{inputenc}
\usepackage{graphicx}

\title{Adventurer's Journal}
\author{D&D Sheet Generator}
\date{\today}

\begin{document}

\maketitle

\chapter*{Introduction}
This journal contains the adventures, discoveries, and wisdom gathered during your travels.

\section*{Character Information}
\begin{DndComment}{Character Details}
    \textbf{Name:} \underline{\hspace{6cm}} \\
    \textbf{Class:} \underline{\hspace{6cm}} \\
    \textbf{Level:} \underline{\hspace{6cm}} \\
    \textbf{Campaign:} \underline{\hspace{6cm}} \\
    \textbf{DM:} \underline{\hspace{6cm}}
\end{DndComment}

\chapter{Adventure Log}

\section*{Session 1}
\begin{DndComment}{Session Notes}
    \vspace{5cm}
\end{DndComment}

\subsection*{Key Events}
\begin{itemize}
    \item \underline{\hspace{12cm}}
    \item \underline{\hspace{12cm}}
    \item \underline{\hspace{12cm}}
\end{itemize}

\subsection*{Treasure Acquired}
\begin{DndTable}[header=Treasure]{lcc}
    \textbf{Item} & \textbf{Value} & \textbf{Notes} \\
    \underline{\hspace{4cm}} & \underline{\hspace{2cm}} & \underline{\hspace{4cm}} \\
    \underline{\hspace{4cm}} & \underline{\hspace{2cm}} & \underline{\hspace{4cm}} \\
    \underline{\hspace{4cm}} & \underline{\hspace{2cm}} & \underline{\hspace{4cm}} \\
\end{DndTable}

\section*{Session 2}
\begin{DndComment}{Session Notes}
    \vspace{5cm}
\end{DndComment}

\subsection*{Key Events}
\begin{itemize}
    \item \underline{\hspace{12cm}}
    \item \underline{\hspace{12cm}}
    \item \underline{\hspace{12cm}}
\end{itemize}

\subsection*{Treasure Acquired}
\begin{DndTable}[header=Treasure]{lcc}
    \textbf{Item} & \textbf{Value} & \textbf{Notes} \\
    \underline{\hspace{4cm}} & \underline{\hspace{2cm}} & \underline{\hspace{4cm}} \\
    \underline{\hspace{4cm}} & \underline{\hspace{2cm}} & \underline{\hspace{4cm}} \\
    \underline{\hspace{4cm}} & \underline{\hspace{2cm}} & \underline{\hspace{4cm}} \\
\end{DndTable}

\chapter{Spells and Magic}

\section*{Cantrips Known}
\begin{DndTable}[header=Cantrips]{lp{8cm}}
    \textbf{Spell} & \textbf{Description} \\
    \underline{\hspace{3cm}} & \underline{\hspace{8cm}} \\
    \underline{\hspace{3cm}} & \underline{\hspace{8cm}} \\
    \underline{\hspace{3cm}} & \underline{\hspace{8cm}} \\
\end{DndTable}

\section*{1st Level Spells}
\begin{DndTable}[header=1st Level]{lp{8cm}}
    \textbf{Spell} & \textbf{Description} \\
    \underline{\hspace{3cm}} & \underline{\hspace{8cm}} \\
    \underline{\hspace{3cm}} & \underline{\hspace{8cm}} \\
    \underline{\hspace{3cm}} & \underline{\hspace{8cm}} \\
\end{DndTable}

\section*{2nd Level Spells}
\begin{DndTable}[header=2nd Level]{lp{8cm}}
    \textbf{Spell} & \textbf{Description} \\
    \underline{\hspace{3cm}} & \underline{\hspace{8cm}} \\
    \underline{\hspace{3cm}} & \underline{\hspace{8cm}} \\
    \underline{\hspace{3cm}} & \underline{\hspace{8cm}} \\
\end{DndTable}

\chapter{NPCs and Allies}

\section*{Important NPCs}
\begin{DndTable}[header=Important NPCs]{lp{8cm}}
    \textbf{Name} & \textbf{Description} \\
    \underline{\hspace{3cm}} & \underline{\hspace{8cm}} \\
    \underline{\hspace{3cm}} & \underline{\hspace{8cm}} \\
    \underline{\hspace{3cm}} & \underline{\hspace{8cm}} \\
\end{DndTable}

\section*{Party Members}
\begin{DndTable}[header=Party]{lp{8cm}}
    \textbf{Name} & \textbf{Class/Race} \\
    \underline{\hspace{3cm}} & \underline{\hspace{8cm}} \\
    \underline{\hspace{3cm}} & \underline{\hspace{8cm}} \\
    \underline{\hspace{3cm}} & \underline{\hspace{8cm}} \\
\end{DndTable}

\chapter{Locations and Maps}

\section*{Important Locations}
\begin{DndTable}[header=Locations]{lp{8cm}}
    \textbf{Location} & \textbf{Description} \\
    \underline{\hspace{3cm}} & \underline{\hspace{8cm}} \\
    \underline{\hspace{3cm}} & \underline{\hspace{8cm}} \\
    \underline{\hspace{3cm}} & \underline{\hspace{8cm}} \\
\end{DndTable}

\section*{Maps}
\begin{DndComment}{Map Section}
    \vspace{8cm}
    \begin{center}
        \textit{Insert maps here}
    \end{center}
\end{DndComment}

\chapter{Lore and Knowledge}

\section*{World Lore}
\begin{DndComment}{Lore Notes}
    \vspace{10cm}
\end{DndComment}

\section*{Quests and Goals}
\begin{DndTable}[header=Quests]{lp{8cm}}
    \textbf{Quest} & \textbf{Status} \\
    \underline{\hspace{3cm}} & \underline{\hspace{8cm}} \\
    \underline{\hspace{3cm}} & \underline{\hspace{8cm}} \\
    \underline{\hspace{3cm}} & \underline{\hspace{8cm}} \\
\end{DndTable}

\end{document}
"""

                # Generate and compile
                self.app.notify("Creating empty book...")
                tex_file = generate_tex_file(empty_content, Path("output/empty_adventurers_journal.tex"))
                success, message, pdf_path = compile_to_pdf(tex_file, Path("output"))

                if success:
                    self.app.notify(f"✓ Created empty book: {pdf_path.name}", severity="information")
                else:
                    self.app.notify(f"✗ Error: {message}", severity="error")

            except Exception as e:
                self.app.notify(f"✗ Error creating empty book: {str(e)}", severity="error")

        def create_npc(self) -> None:
            """Create an NPC character."""
            try:
                from ..latex_generator import generate_tex_file, compile_to_pdf
                from ..latex_env import check_dnd_template

                # Check if DND template is available
                found, location = check_dnd_template()
                if not found:
                    self.app.notify("DND template not found. Cannot create NPC.", severity="error")
                    return

                # Generate NPC template
                npc_content = r"""\documentclass[letterpaper,twocolumn,openany]{dndbook}

\usepackage[english]{babel}
\usepackage[utf8]{inputenc}
\usepackage{graphicx}

\title{NPC Character Sheet}
\author{D&D Sheet Generator}
\date{\today}

\begin{document}

\maketitle

\begin{DndComment}{NPC Information}
    \textbf{Name:} \underline{\hspace{6cm}} \\
    \textbf{Race:} \underline{\hspace{6cm}} \\
    \textbf{Class/Role:} \underline{\hspace{6cm}} \\
    \textbf{Alignment:} \underline{\hspace{6cm}} \\
    \textbf{Location:} \underline{\hspace{6cm}} \\
    \textbf{Relationship:} \underline{\hspace{6cm}}
\end{DndComment}

\section*{Statistics}
\begin{DndTable}[header=Statistics]{lcccccc}
    \textbf{Ability} & \textbf{Score} & \textbf{Modifier} & \textbf{Save} & \textbf{Prof?} & \textbf{Total} \\
    Strength & \underline{\hspace{1cm}} & \underline{\hspace{1cm}} & \underline{\hspace{1cm}} & \square & \underline{\hspace{1cm}} \\
    Dexterity & \underline{\hspace{1cm}} & \underline{\hspace{1cm}} & \underline{\hspace{1cm}} & \square & \underline{\hspace{1cm}} \\
    Constitution & \underline{\hspace{1cm}} & \underline{\hspace{1cm}} & \underline{\hspace{1cm}} & \square & \underline{\hspace{1cm}} \\
    Intelligence & \underline{\hspace{1cm}} & \underline{\hspace{1cm}} & \underline{\hspace{1cm}} & \square & \underline{\hspace{1cm}} \\
    Wisdom & \underline{\hspace{1cm}} & \underline{\hspace{1cm}} & \underline{\hspace{1cm}} & \square & \underline{\hspace{1cm}} \\
    Charisma & \underline{\hspace{1cm}} & \underline{\hspace{1cm}} & \underline{\hspace{1cm}} & \square & \underline{\hspace{1cm}} \\
\end{DndTable}

\section*{Combat}
\begin{DndTable}[header=Combat]{lcc}
    \textbf{Statistic} & \textbf{Value} & \textbf{Notes} \\
    Armor Class & \underline{\hspace{2cm}} & \\
    Hit Points & \underline{\hspace{2cm}} & \\
    Speed & \underline{\hspace{2cm}} & \\
    Challenge Rating & \underline{\hspace{2cm}} & \\
    Proficiency Bonus & \underline{\hspace{2cm}} & \\
\end{DndTable}

\section*{Skills}
\begin{DndTable}[header=Skills]{lcc}
    \textbf{Skill} & \textbf{Ability} & \textbf{Prof?} \\
    Acrobatics & Dex & \square \\
    Animal Handling & Wis & \square \\
    Arcana & Int & \square \\
    Athletics & Str & \square \\
    Deception & Cha & \square \\
    History & Int & \square \\
    Insight & Wis & \square \\
    Intimidation & Cha & \square \\
    Investigation & Int & \square \\
    Medicine & Wis & \square \\
    Nature & Int & \square \\
    Perception & Wis & \square \\
    Performance & Cha & \square \\
    Persuasion & Cha & \square \\
    Religion & Int & \square \\
    Sleight of Hand & Dex & \square \\
    Stealth & Dex & \square \\
    Survival & Wis & \square \\
\end{DndTable}

\section*{Equipment}
\begin{DndTable}[header=Equipment]{lp{10cm}}
    \textbf{Item} & \textbf{Description} \\
    \underline{\hspace{3cm}} & \underline{\hspace{10cm}} \\
    \underline{\hspace{3cm}} & \underline{\hspace{10cm}} \\
    \underline{\hspace{3cm}} & \underline{\hspace{10cm}} \\
    \underline{\hspace{3cm}} & \underline{\hspace{10cm}} \\
    \underline{\hspace{3cm}} & \underline{\hspace{10cm}} \\
\end{DndTable}

\section*{Personality}
\begin{DndComment}{Personality Traits}
    \vspace{3cm}
\end{DndComment}

\begin{DndComment}{Ideals}
    \vspace{3cm}
\end{DndComment}

\begin{DndComment}{Bonds}
    \vspace{3cm}
\end{DndComment}

\begin{DndComment}{Flaws}
    \vspace{3cm}
\end{DndComment}

\section*{Background}
\begin{DndComment}{NPC Background}
    \vspace{5cm}
\end{DndComment}

\section*{Adventure Hooks}
\begin{DndComment}{Adventure Hooks}
    \vspace{5cm}
\end{DndComment}

\end{document}
"""

                # Generate and compile
                self.app.notify("Creating NPC sheet...")
                tex_file = generate_tex_file(npc_content, Path("output/npc_sheet.tex"))
                success, message, pdf_path = compile_to_pdf(tex_file, Path("output"))

                if success:
                    self.app.notify(f"✓ Created NPC sheet: {pdf_path.name}", severity="information")
                else:
                    self.app.notify(f"✗ Error: {message}", severity="error")

            except Exception as e:
                self.app.notify(f"✗ Error creating NPC: {str(e)}", severity="error")

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
            "character_create": CharacterBasicInfoScreen,
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
