"""
Character creation wizard for the TUI.

Multi-screen wizard for creating D&D characters interactively.
"""

from pathlib import Path

try:
    from textual.app import ComposeResult
    from textual.containers import Container, Horizontal, Vertical, Grid
    from textual.widgets import (
        Static, Button, Input, Label, Select,
        SelectionList, RadioSet, RadioButton
    )
    from textual.screen import Screen
    from textual.validation import Number, Length
    from textual import on
    TEXTUAL_AVAILABLE = True
except ImportError:
    TEXTUAL_AVAILABLE = False
    from typing import Any
    ComposeResult = Any
    Screen = type('Screen', (), {})
    Container = type('Container', (), {})
    Static = type('Static', (), {})
    Button = type('Button', (), {})
    Input = type('Input', (), {})
    Select = type('Select', (), {})


if TEXTUAL_AVAILABLE:
    class CharacterBasicInfoScreen(Screen):
        """First step: Basic character information."""

        CSS = """
        CharacterBasicInfoScreen {
            align: center middle;
        }

        #create-container {
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

        .form-row {
            height: auto;
            margin: 1;
        }

        .form-label {
            width: 20;
            content-align: left middle;
        }

        Input {
            width: 1fr;
        }

        Select {
            width: 1fr;
        }

        #button-bar {
            margin-top: 2;
            height: auto;
        }

        Button {
            margin: 0 1;
        }
        """

        def __init__(self):
            super().__init__()
            self.character_data = {}

        def compose(self) -> ComposeResult:
            """Create the basic info form."""
            with Container(id="create-container"):
                yield Static("✨ Create New Character - Step 1: Basic Info", id="title")

                with Horizontal(classes="form-row"):
                    yield Label("Character Name:", classes="form-label")
                    yield Input(
                        placeholder="Enter character name",
                        id="input-name",
                        validators=[Length(minimum=1, maximum=100)]
                    )

                with Horizontal(classes="form-row"):
                    yield Label("Player Name:", classes="form-label")
                    yield Input(
                        placeholder="Enter player name (optional)",
                        id="input-player"
                    )

                with Horizontal(classes="form-row"):
                    yield Label("Race:", classes="form-label")
                    yield Select(
                        options=[
                            ("Human", "human"),
                            ("Elf", "elf"),
                            ("Dwarf", "dwarf"),
                            ("Halfling", "halfling"),
                            ("Dragonborn", "dragonborn"),
                            ("Gnome", "gnome"),
                            ("Half-Elf", "half-elf"),
                            ("Half-Orc", "half-orc"),
                            ("Tiefling", "tiefling"),
                        ],
                        prompt="Select race",
                        id="select-race"
                    )

                with Horizontal(classes="form-row"):
                    yield Label("Class:", classes="form-label")
                    yield Select(
                        options=[
                            ("Barbarian", "barbarian"),
                            ("Bard", "bard"),
                            ("Cleric", "cleric"),
                            ("Druid", "druid"),
                            ("Fighter", "fighter"),
                            ("Monk", "monk"),
                            ("Paladin", "paladin"),
                            ("Ranger", "ranger"),
                            ("Rogue", "rogue"),
                            ("Sorcerer", "sorcerer"),
                            ("Warlock", "warlock"),
                            ("Wizard", "wizard"),
                        ],
                        prompt="Select class",
                        id="select-class"
                    )

                with Horizontal(classes="form-row"):
                    yield Label("Level:", classes="form-label")
                    yield Input(
                        placeholder="1-20",
                        id="input-level",
                        value="1",
                        validators=[Number(minimum=1, maximum=20)]
                    )

                with Horizontal(classes="form-row"):
                    yield Label("Background:", classes="form-label")
                    yield Input(
                        placeholder="Soldier, Noble, etc. (optional)",
                        id="input-background"
                    )

                with Horizontal(classes="form-row"):
                    yield Label("Alignment:", classes="form-label")
                    yield Select(
                        options=[
                            ("Lawful Good", "lawful_good"),
                            ("Neutral Good", "neutral_good"),
                            ("Chaotic Good", "chaotic_good"),
                            ("Lawful Neutral", "lawful_neutral"),
                            ("True Neutral", "true_neutral"),
                            ("Chaotic Neutral", "chaotic_neutral"),
                            ("Lawful Evil", "lawful_evil"),
                            ("Neutral Evil", "neutral_evil"),
                            ("Chaotic Evil", "chaotic_evil"),
                        ],
                        prompt="Select alignment",
                        id="select-alignment"
                    )

                with Horizontal(id="button-bar"):
                    yield Button("Next: Ability Scores →", id="btn-next", variant="primary")
                    yield Button("← Back to Menu", id="btn-back", variant="default")

        def on_button_pressed(self, event: Button.Pressed) -> None:
            """Handle button presses."""
            button_id = event.button.id

            if button_id == "btn-back":
                self.app.pop_screen()
            elif button_id == "btn-next":
                # Validate and collect data
                name = self.query_one("#input-name", Input).value
                if not name:
                    self.app.notify("Character name is required!", severity="error")
                    return

                # Collect all form data
                self.character_data = {
                    "name": name,
                    "player_name": self.query_one("#input-player", Input).value or None,
                    "race": self.query_one("#select-race", Select).value or "Human",
                    "class": self.query_one("#select-class", Select).value or "Fighter",
                    "level": int(self.query_one("#input-level", Input).value or 1),
                    "background": self.query_one("#input-background", Input).value or None,
                    "alignment": self.query_one("#select-alignment", Select).value or None,
                }

                # Move to skills selection screen
                self.app.push_screen(CharacterSkillsScreen(self.character_data))


    class CharacterSkillsScreen(Screen):
        """Skills and proficiency selection."""

        CSS = """
        CharacterSkillsScreen {
            align: center middle;
        }

        #create-container {
            width: 80;
            height: 85%;
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

        SelectionList {
            height: 1fr;
            border: solid $primary;
            margin: 1;
        }

        #button-bar {
            margin-top: 1;
            height: auto;
        }

        Button {
            margin: 0 1;
        }
        """

        def __init__(self, character_data: dict):
            super().__init__()
            self.character_data = character_data

        def compose(self) -> ComposeResult:
            """Create the skills selection screen."""
            with Container(id="create-container"):
                yield Static("✨ Create New Character - Step 2: Skills & Proficiencies", id="title")
                yield Static("Select skills your character is proficient in:", classes="form-label")

                # Skills selection list
                skills_options = [
                    ("Acrobatics (DEX)", "acrobatics"),
                    ("Animal Handling (WIS)", "animal_handling"),
                    ("Arcana (INT)", "arcana"),
                    ("Athletics (STR)", "athletics"),
                    ("Deception (CHA)", "deception"),
                    ("History (INT)", "history"),
                    ("Insight (WIS)", "insight"),
                    ("Intimidation (CHA)", "intimidation"),
                    ("Investigation (INT)", "investigation"),
                    ("Medicine (WIS)", "medicine"),
                    ("Nature (INT)", "nature"),
                    ("Perception (WIS)", "perception"),
                    ("Performance (CHA)", "performance"),
                    ("Persuasion (CHA)", "persuasion"),
                    ("Religion (INT)", "religion"),
                    ("Sleight of Hand (DEX)", "sleight_of_hand"),
                    ("Stealth (DEX)", "stealth"),
                    ("Survival (WIS)", "survival"),
                ]

                yield SelectionList(*skills_options, id="skills-list")

                yield Static("Select saving throw proficiencies:", classes="form-label")

                saving_throws = [
                    ("Strength", "strength"),
                    ("Dexterity", "dexterity"),
                    ("Constitution", "constitution"),
                    ("Intelligence", "intelligence"),
                    ("Wisdom", "wisdom"),
                    ("Charisma", "charisma"),
                ]

                yield SelectionList(*saving_throws, id="saves-list")

                with Horizontal(id="button-bar"):
                    yield Button("Next: Ability Scores →", id="btn-next", variant="primary")
                    yield Button("← Back", id="btn-back", variant="default")

        def on_button_pressed(self, event: Button.Pressed) -> None:
            """Handle button presses."""
            button_id = event.button.id

            if button_id == "btn-back":
                self.app.pop_screen()
            elif button_id == "btn-next":
                # Get selected skills
                skills_list = self.query_one("#skills-list", SelectionList)
                self.character_data["skill_proficiencies"] = list(skills_list.selected)

                # Get selected saving throws
                saves_list = self.query_one("#saves-list", SelectionList)
                self.character_data["saving_throw_proficiencies"] = list(saves_list.selected)

                # Move to ability scores screen
                self.app.push_screen(CharacterAbilityScoresScreen(self.character_data))


    class CharacterAbilityScoresScreen(Screen):
        """Second step: Ability scores."""

        CSS = """
        CharacterAbilityScoresScreen {
            align: center middle;
        }

        #create-container {
            width: 70;
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

        .ability-row {
            height: auto;
            margin: 1;
        }

        .ability-label {
            width: 15;
            content-align: left middle;
        }

        Input {
            width: 10;
        }

        .modifier {
            width: 10;
            content-align: center middle;
            color: $accent;
        }

        #button-bar {
            margin-top: 2;
            height: auto;
        }

        Button {
            margin: 0 1;
        }
        """

        def __init__(self, character_data: dict):
            super().__init__()
            self.character_data = character_data

        def compose(self) -> ComposeResult:
            """Create the ability scores form."""
            with Container(id="create-container"):
                yield Static("✨ Create New Character - Step 3: Ability Scores", id="title")
                yield Static("Enter scores (1-30). Modifier is calculated automatically.", classes="form-label")

                for ability in ["Strength", "Dexterity", "Constitution", "Intelligence", "Wisdom", "Charisma"]:
                    with Horizontal(classes="ability-row"):
                        yield Label(f"{ability}:", classes="ability-label")
                        yield Input(
                            placeholder="10",
                            value="10",
                            id=f"input-{ability.lower()}",
                            validators=[Number(minimum=1, maximum=30)]
                        )
                        yield Label("(+0)", id=f"mod-{ability.lower()}", classes="modifier")

                with Horizontal(id="button-bar"):
                    yield Button("Next: Combat Stats →", id="btn-next", variant="primary")
                    yield Button("← Back", id="btn-back", variant="default")

        def on_mount(self) -> None:
            """Set up watchers when screen mounts."""
            for ability in ["strength", "dexterity", "constitution", "intelligence", "wisdom", "charisma"]:
                self.watch_ability_input(ability)

        def watch_ability_input(self, ability: str) -> None:
            """Watch for changes to ability score inputs."""
            input_widget = self.query_one(f"#input-{ability}", Input)

            def update_modifier(value: str):
                try:
                    score = int(value) if value else 10
                    modifier = (score - 10) // 2
                    mod_widget = self.query_one(f"#mod-{ability}", Label)
                    mod_widget.update(f"({modifier:+d})")
                except ValueError:
                    pass

            input_widget.watch(input_widget, "value", lambda v: update_modifier(v), init=True)

        def on_button_pressed(self, event: Button.Pressed) -> None:
            """Handle button presses."""
            button_id = event.button.id

            if button_id == "btn-back":
                self.app.pop_screen()
            elif button_id == "btn-next":
                # Collect ability scores
                self.character_data["ability_scores"] = {
                    "strength": int(self.query_one("#input-strength", Input).value or 10),
                    "dexterity": int(self.query_one("#input-dexterity", Input).value or 10),
                    "constitution": int(self.query_one("#input-constitution", Input).value or 10),
                    "intelligence": int(self.query_one("#input-intelligence", Input).value or 10),
                    "wisdom": int(self.query_one("#input-wisdom", Input).value or 10),
                    "charisma": int(self.query_one("#input-charisma", Input).value or 10),
                }

                # Move to combat stats screen
                self.app.push_screen(CharacterCombatStatsScreen(self.character_data))


    class CharacterCombatStatsScreen(Screen):
        """Third step: Combat stats and completion."""

        CSS = """
        CharacterCombatStatsScreen {
            align: center middle;
        }

        #create-container {
            width: 60;
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

        .form-row {
            height: auto;
            margin: 1;
        }

        .form-label {
            width: 20;
            content-align: left middle;
        }

        Input {
            width: 1fr;
        }

        #button-bar {
            margin-top: 2;
            height: auto;
        }

        Button {
            margin: 0 1;
        }
        """

        def __init__(self, character_data: dict):
            super().__init__()
            self.character_data = character_data

        def compose(self) -> ComposeResult:
            """Create the combat stats form."""
            with Container(id="create-container"):
                yield Static("✨ Create New Character - Step 4: Combat Stats", id="title")

                with Horizontal(classes="form-row"):
                    yield Label("Armor Class:", classes="form-label")
                    yield Input(placeholder="10", value="10", id="input-ac", validators=[Number(minimum=1, maximum=30)])

                with Horizontal(classes="form-row"):
                    yield Label("Max Hit Points:", classes="form-label")
                    yield Input(placeholder="10", value="10", id="input-hp", validators=[Number(minimum=1)])

                with Horizontal(classes="form-row"):
                    yield Label("Speed (ft):", classes="form-label")
                    yield Input(placeholder="30", value="30", id="input-speed", validators=[Number(minimum=0, maximum=120)])

                with Horizontal(classes="form-row"):
                    yield Label("Hit Dice:", classes="form-label")
                    yield Input(placeholder="1d8", value="1d8", id="input-hit-dice")

                with Horizontal(id="button-bar"):
                    yield Button("✓ Create & Generate PDF", id="btn-create", variant="success")
                    yield Button("← Back", id="btn-back", variant="default")
                    yield Button("✗ Cancel", id="btn-cancel", variant="error")

        def on_button_pressed(self, event: Button.Pressed) -> None:
            """Handle button presses."""
            button_id = event.button.id

            if button_id == "btn-back":
                self.app.pop_screen()
            elif button_id == "btn-cancel":
                # Go back to main menu
                while len(self.app.screen_stack) > 1:
                    self.app.pop_screen()
            elif button_id == "btn-create":
                # Collect final data
                self.character_data["armor_class"] = int(self.query_one("#input-ac", Input).value or 10)
                self.character_data["max_hit_points"] = int(self.query_one("#input-hp", Input).value or 10)
                self.character_data["speed"] = int(self.query_one("#input-speed", Input).value or 30)
                self.character_data["hit_dice"] = self.query_one("#input-hit-dice", Input).value or "1d8"

                # Create character and generate PDF
                self.create_character()

        def create_character(self) -> None:
            """Create the character and generate PDF."""
            try:
                from ..character import Character, AbilityScores, Skill, Ability
                from ..sheet_generator import generate_and_compile_character_sheet

                # Create character object
                self.app.notify(f"Creating character: {self.character_data['name']}...")

                # Convert skill strings to Skill enums
                skill_profs = [Skill(s) for s in self.character_data.get("skill_proficiencies", [])]
                save_profs = [Ability(s) for s in self.character_data.get("saving_throw_proficiencies", [])]

                character = Character(
                    name=self.character_data["name"],
                    player_name=self.character_data.get("player_name"),
                    race=self.character_data["race"],
                    character_class=self.character_data["class"],
                    level=self.character_data["level"],
                    background=self.character_data.get("background"),
                    alignment=self.character_data.get("alignment"),
                    ability_scores=AbilityScores(**self.character_data["ability_scores"]),
                    skill_proficiencies=skill_profs,
                    saving_throw_proficiencies=save_profs,
                    armor_class=self.character_data["armor_class"],
                    max_hit_points=self.character_data["max_hit_points"],
                    speed=self.character_data["speed"],
                    hit_dice=self.character_data["hit_dice"],
                )

                # Save to JSON
                output_dir = Path("output")
                output_dir.mkdir(exist_ok=True)

                json_filename = f"{character.name.lower().replace(' ', '_')}.json"
                json_path = output_dir / json_filename
                character.to_json(json_path)
                self.app.notify(f"Saved character to {json_path}")

                # Generate PDF
                self.app.notify(f"Generating PDF for {character.name}...")
                success, message, pdf_path = generate_and_compile_character_sheet(
                    character,
                    output_dir=output_dir,
                )

                if success:
                    self.app.notify(
                        f"✓ Success! Created {pdf_path.name}",
                        severity="information",
                        timeout=10
                    )
                    # Go back to main menu
                    while len(self.app.screen_stack) > 1:
                        self.app.pop_screen()
                else:
                    self.app.notify(f"✗ Error: {message}", severity="error", timeout=10)

            except Exception as e:
                self.app.notify(f"✗ Error creating character: {str(e)}", severity="error", timeout=10)
