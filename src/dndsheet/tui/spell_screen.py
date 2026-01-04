"""
TUI screen for managing a character's spells and spell slots.
"""

from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Vertical, Horizontal, Grid
from textual.screen import Screen
from textual.widgets import Header, Footer, Static, DataTable, Button

from ..character import Character
from ..enums import Ability
from ..spells import Spell


class SpellScreen(Screen[None]):
    """A screen for viewing and managing spells."""

    DEFAULT_CSS_FILE = "spell_screen.css"

    BINDINGS = [
        Binding("p", "toggle_prepare", "Prepare/Unprepare Spell"),
        Binding("u", "use_slot", "Use Spell Slot"),
        Binding("r", "recover_slot", "Recover Spell Slot"),
        Binding("q", "quit", "Back to Character"),
    ]

    def __init__(self, character: Character, name: str | None = None, id: str | None = None, classes: str | None = None):
        super().__init__(name, id, classes)
        self.character = character
        self.spell_table = DataTable(id="spell-table")

    def compose(self) -> ComposeResult:
        """Compose the spell screen UI."""
        with Vertical(id="spell-screen-container"):
            yield Header()
            yield self.make_spell_header()
            yield self.make_spell_slots_display()
            with Vertical(id="spell-list-box"):
                yield Static("[b]Spell List[/b] (Navigate with arrows, 'p' to prepare)")
                yield self.spell_table
            yield Footer()

    def on_mount(self) -> None:
        """Set up the spell table when the screen is mounted."""
        self.spell_table.cursor_type = "row"
        self.spell_table.add_columns("Prep", "Name", "Lvl", "School", "Time", "Concentration")
        self.update_spell_list()

    def make_spell_header(self) -> Static:
        """Creates the header display with spellcasting stats."""
        if not self.character.spellcasting_ability:
            return Static("This character is not a spellcaster.")

        ability_name = self.character.spellcasting_ability.name.capitalize()
        save_dc = self.character.spell_save_dc
        attack_bonus = f"+{self.character.spell_attack_bonus}"

        return Static(
            f"[b]Ability:[/b] {ability_name} | [b]Save DC:[/b] {save_dc} | [b]Attack Bonus:[/b] {attack_bonus}",
            id="spell-header-box"
        )

    def make_spell_slots_display(self) -> Static:
        """Creates the interactive spell slots display."""
        if not self.character.spellbook.spell_slots:
            return Static(id="spell-slots-box")
        
        slots_grid = Grid(id="spell-slots-grid")
        
        sorted_slots = sorted(self.character.spellbook.spell_slots.items())

        for level, slots in sorted_slots:
            slots_grid.add_column(f"lvl-{level}", repeat=1)
            
        for level, slots in sorted_slots:
            slots_grid.add_row(f"row-{level}", repeat=1)
            
        for level, slots in sorted_slots:
            slots_grid.add_widget(Static(f"[b]Level {level}[/b]", classes="slot-level"), column=f"lvl-{level}", row=f"row-{level}")
            
        for level, slots in sorted_slots:
            slots_grid.add_widget(Static(f"{slots.remaining}/{slots.max}", classes="slot-count", id=f"slot-count-{level}"), column=f"lvl-{level}", row=f"row-{level}")
            
        # This part seems to have an issue in the original thought process. Let's simplify.
        # We will create a new display that is easier to manage.
        
        container = Vertical()
        for level, slots in sorted_slots:
            container.mount(
                Horizontal(
                    Static(f"Level {level}:", classes="slot-level"),
                    Static(f"{slots.remaining}/{slots.max}", classes="slot-count", id=f"slot-count-{level}"),
                    Button("-", id=f"use-slot-{level}", classes="slot-buttons"),
                    Button("+", id=f"recover-slot-{level}", classes="slot-buttons"),
                )
            )

        return Static(container, id="spell-slots-box")


    def update_spell_list(self):
        """Clears and repopulates the spell list table."""
        self.spell_table.clear()
        all_spells = sorted(self.character.spellbook.spells, key=lambda s: (s.level, s.name))
        for spell in all_spells:
            is_prepared = self.character.spellbook.is_prepared(spell.name)
            prep_marker = "[b green]✓[/]" if is_prepared else "[dim red]✗[/]"
            concentration_marker = "C" if spell.concentration else ""
            self.spell_table.add_row(
                prep_marker,
                spell.name,
                str(spell.level),
                spell.school.value,
                spell.casting_time,
                concentration_marker,
                key=spell.name,
            )

    def action_toggle_prepare(self) -> None:
        """Toggles the prepared status of the selected spell."""
        row_key = self.spell_table.cursor_row
        if row_key is None:
            return
        
        spell_name = self.spell_table.get_row(row_key)[1]
        spell = self.character.spellbook.get_spell(spell_name)
        if not spell or spell.level == 0: # Cantrips cannot be unprepared
            return

        if self.character.spellbook.is_prepared(spell_name):
            self.character.spellbook.unprepare_spell(spell_name)
        else:
            self.character.spellbook.prepare_spell(spell_name)
        
        self.update_spell_list()
        self.spell_table.cursor_row = row_key

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses for spell slots."""
        if event.button.id and event.button.id.startswith("use-slot-"):
            level = int(event.button.id.split("-")[-1])
            self.use_slot_for_level(level)
        elif event.button.id and event.button.id.startswith("recover-slot-"):
            level = int(event.button.id.split("-")[-1])
            self.recover_slot_for_level(level)

    def use_slot_for_level(self, level: int):
        """Uses a spell slot for the given level."""
        try:
            self.character.spellbook.spell_slots[level].use_slot()
            self.update_slot_display(level)
        except (KeyError, ValueError):
            # Ignore if no slots of that level or no slots remaining
            pass

    def recover_slot_for_level(self, level: int):
        """Recovers a spell slot for the given level."""
        try:
            self.character.spellbook.spell_slots[level].recover_slot()
            self.update_slot_display(level)
        except KeyError:
            # Ignore if no slots of that level
            pass

    def update_slot_display(self, level: int) -> None:
        """Updates the text of a single spell slot counter."""
        slots = self.character.spellbook.spell_slots.get(level)
        if slots:
            slot_counter = self.query_one(f"#slot-count-{level}", Static)
            slot_counter.update(f"{slots.remaining}/{slots.max}")

    def action_quit(self) -> None:
        """Go back to the previous screen."""
        self.app.pop_screen()

if __name__ == '__main__':
    from textual.app import App
    from ..character import Character, AbilityScores
    from ..enums import Ability, MagicSchool, SpellComponent

    class SpellScreenTestApp(App):
        def on_mount(self):
            # Create a test character
            spells = [
                Spell("Fire Bolt", 0, MagicSchool.EVOCATION, "1 Action", "120 ft", "Instantaneous", "...", components={SpellComponent.VERBAL, SpellComponent.SOMATIC}),
                Spell("Mage Armor", 1, MagicSchool.ABJURATION, "1 Action", "Touch", "8 hours", "...", components={SpellComponent.VERBAL, SpellComponent.SOMATIC, SpellComponent.MATERIAL}, material_component="leather"),
                Spell("Magic Missile", 1, MagicSchool.EVOCATION, "1 Action", "120 ft", "Instantaneous", "...", components={SpellComponent.VERBAL, SpellComponent.SOMATIC}),
                Spell("Misty Step", 2, MagicSchool.CONJURATION, "1 Bonus Action", "Self", "Instantaneous", "...", components={SpellComponent.VERBAL})
            ]
            char = Character(
                name="Elara",
                character_class="Wizard",
                level=3,
                spellcasting_ability=Ability.INTELLIGENCE,
                ability_scores=AbilityScores(intelligence=17),
                spellbook=Spellbook(spells=spells)
            )
            char.spellbook.prepare_spell("Mage Armor")
            self.push_screen(SpellScreen(character=char))
    
    app = SpellScreenTestApp()
    app.run()