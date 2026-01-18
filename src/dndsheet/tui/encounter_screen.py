"""
TUI screen for creating and managing combat encounters.
"""

from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Vertical, Horizontal
from textual.screen import Screen
from textual.widgets import Header, Footer, Static, DataTable, Button, Input, Label
from textual.message import Message
from textual import log

from ..monsters import load_all_monsters_from_dir, Monster
from ..encounter_generator import Encounter
from pathlib import Path


class EncounterScreen(Screen[None]):
    """A screen for building and viewing combat encounters."""

    DEFAULT_CSS_FILE = "encounter_screen.css" # We'll create this CSS file

    BINDINGS = [
        Binding("a", "add_selected_monster", "Add Monster"),
        Binding("r", "remove_encounter_monster", "Remove Monster"),
        Binding("q", "quit", "Back to Main Menu"),
    ]

    def __init__(self, name: str | None = None, id: str | None = None, classes: str | None = None):
        super().__init__(name, id, classes)
        self.all_monsters: List[Monster] = []
        self.current_encounter = Encounter()

        self.available_monsters_table = DataTable(id="available-monsters-table")
        self.encounter_monsters_table = DataTable(id="encounter-monsters-table")

        self.party_size_input = Input(value="4", placeholder="Party Size", id="party-size-input")
        self.avg_level_input = Input(value="1", placeholder="Average Level", id="avg-level-input")

        self.xp_display = Static("", id="xp-display")
        self.difficulty_display = Static("", id="difficulty-display")

    def compose(self) -> ComposeResult:
        """Compose the encounter screen UI."""
        with Vertical(id="encounter-screen-container"):
            yield Header()
            yield Static("[b]Encounter Builder[/b]", id="encounter-title")

            with Horizontal(id="party-info"):
                yield Label("Party Size:")
                yield self.party_size_input
                yield Label("Avg. Level:")
                yield self.avg_level_input

            with Horizontal(id="monster-tables-container"):
                with Vertical(id="available-monsters-panel"):
                    yield Static("[b]Available Monsters[/b]")
                    yield self.available_monsters_table
                    yield Button("Add Monster", id="btn-add-monster", classes="action-button")
                
                with Vertical(id="encounter-monsters-panel"):
                    yield Static("[b]Current Encounter[/b]")
                    yield self.encounter_monsters_table
                    yield Button("Remove Monster", id="btn-remove-monster", classes="action-button")

            with Horizontal(id="encounter-stats"):
                yield self.xp_display
                yield self.difficulty_display
            
            yield Button("Generate Encounter Document", id="btn-generate-encounter", variant="primary")
            yield Footer()

    def on_mount(self) -> None:
        """Load monsters and set up tables when the screen is mounted."""
        self.all_monsters = load_all_monsters_from_dir(Path("rulebooks/monsters"))
        self.all_monsters.sort(key=lambda m: (m.cr, m.name))

        self.available_monsters_table.cursor_type = "row"
        self.available_monsters_table.zebra_stripes = True
        self.available_monsters_table.add_columns("Name", "CR", "XP", "HP", "AC")
        self.update_available_monsters_table()

        self.encounter_monsters_table.cursor_type = "row"
        self.encounter_monsters_table.zebra_stripes = True
        self.encounter_monsters_table.add_columns("Name", "CR", "XP")
        self.update_encounter_monsters_table()

        # Initial calculation update
        self.update_encounter_stats()
        
        self.party_size_input.action_focus() # Focus on first input

    def on_input_changed(self, event: Input.Changed) -> None:
        """Update encounter stats when party info changes."""
        if event.input.id in ["party-size-input", "avg-level-input"]:
            try:
                self.current_encounter.party_size = int(self.party_size_input.value)
                self.current_encounter.average_party_level = int(self.avg_level_input.value)
            except ValueError:
                pass # Ignore invalid input for now, will be handled by update_encounter_stats
            self.update_encounter_stats()

    def update_available_monsters_table(self) -> None:
        """Populate the available monsters table."""
        self.available_monsters_table.clear()
        for monster in self.all_monsters:
            self.available_monsters_table.add_row(
                monster.name, str(monster.cr), str(monster.xp), str(monster.hp), str(monster.ac),
                key=monster.name
            )

    def update_encounter_monsters_table(self) -> None:
        """Populate the encounter monsters table."""
        self.encounter_monsters_table.clear()
        for monster in self.current_encounter.monsters:
            self.encounter_monsters_table.add_row(
                monster.name, str(monster.cr), str(monster.xp),
                key=id(monster) # Use object ID to differentiate multiple of same monster
            )
        self.update_encounter_stats() # Update stats after table refresh

    def update_encounter_stats(self) -> None:
        """Update the displayed XP and difficulty."""
        self.xp_display.update(
            f"Raw XP: [b]{self.current_encounter.total_raw_xp}[/b] | "
            f"Adjusted XP: [b]{self.current_encounter.adjusted_xp}[/b]"
        )
        self.difficulty_display.update(
            f"Difficulty: [b]{self.current_encounter.difficulty}[/b]"
        )

    def action_add_selected_monster(self) -> None:
        """Adds the currently selected monster from the available table to the encounter."""
        row_key = self.available_monsters_table.cursor_row
        if row_key is None:
            return
        
        monster_name = self.available_monsters_table.get_row_from_key(row_key)[0]
        monster_to_add = next((m for m in self.all_monsters if m.name == monster_name), None)
        
        if monster_to_add:
            self.current_encounter.add_monster(monster_to_add)
            self.update_encounter_monsters_table()

    def action_remove_encounter_monster(self) -> None:
        """Removes the currently selected monster from the encounter table."""
        row_key = self.encounter_monsters_table.cursor_row
        if row_key is None:
            return
        
        # We stored object ID as key, so we need to find the object
        monster_id = row_key
        monster_to_remove = next((m for m in self.current_encounter.monsters if id(m) == monster_id), None)

        if monster_to_remove:
            self.current_encounter.remove_monster(monster_to_remove)
            self.update_encounter_monsters_table()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        if event.button.id == "btn-add-monster":
            self.action_add_selected_monster()
        elif event.button.id == "btn-remove-monster":
            self.action_remove_encounter_monster()
        elif event.button.id == "btn-generate-encounter":
            self.generate_encounter_document()

    def generate_encounter_document(self) -> None:
        """Generates the encounter sheet PDF and QMD."""
        from ..latex_generator import generate_tex_file, compile_to_pdf
        from ..sheet_generator import render_template
        from ..latex_env import check_dnd_template
        from datetime import datetime

        if not self.current_encounter.monsters:
            self.app.notify("No monsters in encounter to generate.", severity="warning")
            return

        try:
            found, location = check_dnd_template()
            if not found:
                self.app.notify("DND template not found. Cannot create.", severity="error")
                return

            self.app.notify("Generating encounter document...")
            
            # Context for templates
            context = {
                "encounter": self.current_encounter,
                "party_size": self.current_encounter.party_size,
                "average_party_level": self.current_encounter.average_party_level,
                "now": datetime.now
            }

            safe_name = "encounter" # A generic name for now
            if self.current_encounter.monsters:
                first_monster_name = self.current_encounter.monsters[0].name.replace(" ", "_").lower()
                safe_name = f"{first_monster_name}_encounter"
            
            # --- Generate LaTeX and PDF ---
            latex_source = render_template("encounter_sheet.tex.j2", **context)
            tex_filename = f"{safe_name}.tex"
            tex_file = generate_tex_file(latex_source, Path(f"output/{tex_filename}"))
            success_pdf, message_pdf, pdf_path = compile_to_pdf(tex_file, Path("output"))

            # --- Generate QMD ---
            qmd_source = render_template("encounter_sheet.qmd.j2", **context)
            qmd_filename = f"{safe_name}.qmd"
            qmd_path = Path(f"output/{qmd_filename}")
            qmd_path.write_text(qmd_source, encoding='utf-8')
            success_qmd = True # Assuming write_text doesn't fail silently

            output_message = f"Created encounter: "
            if success_pdf:
                output_message += f"PDF ({pdf_path.name})"
            if success_qmd:
                output_message += f", QMD ({qmd_path.name})"
            
            self.app.notify(f"✓ {output_message}", severity="information", timeout=7)

        except Exception as e:
            log.error(f"Failed to generate encounter documents: {e}")
            self.app.notify(f"✗ Error: {str(e)}", severity="error", timeout=10)

    def action_quit(self) -> None:
        """Go back to the previous screen."""
        self.app.pop_screen()


if __name__ == "__main__":
    from textual.app import App

    class EncounterTestApp(App):
        def on_mount(self):
            self.push_screen(EncounterScreen())

    EncounterTestApp().run()
