"""
Character data models for D&D 5e.

This module defines the core character data structure using dataclasses.
"""

import json
from dataclasses import dataclass, field, asdict
from enum import Enum
from pathlib import Path
from typing import Optional


class Ability(str, Enum):
    """D&D 5e ability scores."""
    STRENGTH = "strength"
    DEXTERITY = "dexterity"
    CONSTITUTION = "constitution"
    INTELLIGENCE = "intelligence"
    WISDOM = "wisdom"
    CHARISMA = "charisma"


class Skill(str, Enum):
    """D&D 5e skills and their governing abilities."""
    ACROBATICS = "acrobatics"  # DEX
    ANIMAL_HANDLING = "animal_handling"  # WIS
    ARCANA = "arcana"  # INT
    ATHLETICS = "athletics"  # STR
    DECEPTION = "deception"  # CHA
    HISTORY = "history"  # INT
    INSIGHT = "insight"  # WIS
    INTIMIDATION = "intimidation"  # CHA
    INVESTIGATION = "investigation"  # INT
    MEDICINE = "medicine"  # WIS
    NATURE = "nature"  # INT
    PERCEPTION = "perception"  # WIS
    PERFORMANCE = "performance"  # CHA
    PERSUASION = "persuasion"  # CHA
    RELIGION = "religion"  # INT
    SLEIGHT_OF_HAND = "sleight_of_hand"  # DEX
    STEALTH = "stealth"  # DEX
    SURVIVAL = "survival"  # WIS


# Skill to ability mapping
SKILL_ABILITIES: dict[Skill, Ability] = {
    Skill.ACROBATICS: Ability.DEXTERITY,
    Skill.ANIMAL_HANDLING: Ability.WISDOM,
    Skill.ARCANA: Ability.INTELLIGENCE,
    Skill.ATHLETICS: Ability.STRENGTH,
    Skill.DECEPTION: Ability.CHARISMA,
    Skill.HISTORY: Ability.INTELLIGENCE,
    Skill.INSIGHT: Ability.WISDOM,
    Skill.INTIMIDATION: Ability.CHARISMA,
    Skill.INVESTIGATION: Ability.INTELLIGENCE,
    Skill.MEDICINE: Ability.WISDOM,
    Skill.NATURE: Ability.INTELLIGENCE,
    Skill.PERCEPTION: Ability.WISDOM,
    Skill.PERFORMANCE: Ability.CHARISMA,
    Skill.PERSUASION: Ability.CHARISMA,
    Skill.RELIGION: Ability.INTELLIGENCE,
    Skill.SLEIGHT_OF_HAND: Ability.DEXTERITY,
    Skill.STEALTH: Ability.DEXTERITY,
    Skill.SURVIVAL: Ability.WISDOM,
}


@dataclass
class AbilityScores:
    """Character ability scores (STR, DEX, CON, INT, WIS, CHA)."""

    strength: int = 10
    dexterity: int = 10
    constitution: int = 10
    intelligence: int = 10
    wisdom: int = 10
    charisma: int = 10

    def __post_init__(self):
        """Validate ability scores are in valid range (1-30)."""
        for ability in ['strength', 'dexterity', 'constitution', 'intelligence', 'wisdom', 'charisma']:
            value = getattr(self, ability)
            if not (1 <= value <= 30):
                raise ValueError(f"{ability} must be between 1 and 30, got {value}")

    def get_score(self, ability: Ability) -> int:
        """Get ability score by ability type."""
        return getattr(self, ability.value)

    def get_modifier(self, ability: Ability) -> int:
        """Calculate ability modifier using the formula: (score - 10) // 2."""
        score = self.get_score(ability)
        return (score - 10) // 2

    @property
    def strength_modifier(self) -> int:
        return self.get_modifier(Ability.STRENGTH)

    @property
    def dexterity_modifier(self) -> int:
        return self.get_modifier(Ability.DEXTERITY)

    @property
    def constitution_modifier(self) -> int:
        return self.get_modifier(Ability.CONSTITUTION)

    @property
    def intelligence_modifier(self) -> int:
        return self.get_modifier(Ability.INTELLIGENCE)

    @property
    def wisdom_modifier(self) -> int:
        return self.get_modifier(Ability.WISDOM)

    @property
    def charisma_modifier(self) -> int:
        return self.get_modifier(Ability.CHARISMA)


@dataclass
class Character:
    """D&D 5e character sheet data model."""

    # Basic information
    name: str
    race: str
    character_class: str
    level: int = 1
    player_name: Optional[str] = None
    background: Optional[str] = None
    alignment: Optional[str] = None

    # Ability scores
    ability_scores: AbilityScores = field(default_factory=AbilityScores)

    # Proficiencies
    skill_proficiencies: list[Skill] = field(default_factory=list)
    saving_throw_proficiencies: list[Ability] = field(default_factory=list)

    # Combat stats
    armor_class: int = 10
    initiative_bonus: Optional[int] = None  # If None, uses DEX modifier
    speed: int = 30
    max_hit_points: int = 10
    current_hit_points: Optional[int] = None  # If None, equals max_hit_points
    temporary_hit_points: int = 0
    hit_dice: str = "1d8"  # e.g., "3d10"

    # Additional stats
    inspiration: bool = False
    experience_points: int = 0

    def __post_init__(self):
        """Validate character data and set defaults."""
        # Validate level
        if not (1 <= self.level <= 20):
            raise ValueError(f"Level must be between 1 and 20, got {self.level}")

        # Validate name
        if not self.name or len(self.name) > 100:
            raise ValueError("Name must be 1-100 characters")

        # Set current HP to max if not specified
        if self.current_hit_points is None:
            self.current_hit_points = self.max_hit_points

        # Validate HP
        if self.max_hit_points < 1:
            raise ValueError("Max hit points must be at least 1")
        if self.current_hit_points < 0:
            raise ValueError("Current hit points cannot be negative")

        # Validate AC
        if not (1 <= self.armor_class <= 30):
            raise ValueError("Armor class must be between 1 and 30")

    @property
    def proficiency_bonus(self) -> int:
        """Calculate proficiency bonus based on character level."""
        # Standard D&D 5e proficiency progression
        if self.level < 5:
            return 2
        elif self.level < 9:
            return 3
        elif self.level < 13:
            return 4
        elif self.level < 17:
            return 5
        else:
            return 6

    @property
    def initiative(self) -> int:
        """Calculate initiative (DEX modifier + initiative bonus if any)."""
        initiative = self.ability_scores.dexterity_modifier
        if self.initiative_bonus is not None:
            initiative += self.initiative_bonus
        return initiative

    def get_skill_modifier(self, skill: Skill) -> int:
        """
        Calculate skill modifier.

        Formula: ability_modifier + (proficiency_bonus if proficient else 0)
        """
        # Get governing ability for this skill
        ability = SKILL_ABILITIES[skill]
        modifier = self.ability_scores.get_modifier(ability)

        # Add proficiency bonus if proficient
        if skill in self.skill_proficiencies:
            modifier += self.proficiency_bonus

        return modifier

    def get_saving_throw(self, ability: Ability) -> int:
        """
        Calculate saving throw modifier.

        Formula: ability_modifier + (proficiency_bonus if proficient else 0)
        """
        modifier = self.ability_scores.get_modifier(ability)

        # Add proficiency bonus if proficient
        if ability in self.saving_throw_proficiencies:
            modifier += self.proficiency_bonus

        return modifier

    @classmethod
    def from_json(cls, json_path: Path) -> "Character":
        """Load character from JSON file."""
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Rename 'class' to 'character_class' for Python
        if 'class' in data:
            data['character_class'] = data.pop('class')

        # Convert ability_scores dict to AbilityScores object
        if 'ability_scores' in data and isinstance(data['ability_scores'], dict):
            data['ability_scores'] = AbilityScores(**data['ability_scores'])

        # Convert skill/ability proficiency strings to enums
        if 'skill_proficiencies' in data:
            data['skill_proficiencies'] = [Skill(s) for s in data['skill_proficiencies']]
        if 'saving_throw_proficiencies' in data:
            data['saving_throw_proficiencies'] = [Ability(a) for a in data['saving_throw_proficiencies']]

        return cls(**data)

    def to_json(self, json_path: Path, indent: int = 2) -> None:
        """Save character to JSON file."""
        json_path.parent.mkdir(parents=True, exist_ok=True)

        # Convert to dict
        data = asdict(self)

        # Rename character_class to class for JSON
        data['class'] = data.pop('character_class')

        # Convert enum values to strings
        if 'skill_proficiencies' in data:
            data['skill_proficiencies'] = [s.value if isinstance(s, Skill) else s for s in data['skill_proficiencies']]
        if 'saving_throw_proficiencies' in data:
            data['saving_throw_proficiencies'] = [a.value if isinstance(a, Ability) else a for a in data['saving_throw_proficiencies']]

        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=indent)


# Example usage and testing
if __name__ == "__main__":
    # Create a test character
    grimnar = Character(
        name="Grimnar Ironforge",
        player_name="Test Player",
        race="Mountain Dwarf",
        character_class="Fighter",
        level=5,
        background="Soldier",
        alignment="Lawful Good",
        ability_scores=AbilityScores(
            strength=16,  # +3 modifier
            dexterity=14,  # +2 modifier
            constitution=15,  # +2 modifier
            intelligence=10,  # +0 modifier
            wisdom=12,  # +1 modifier
            charisma=8,  # -1 modifier
        ),
        skill_proficiencies=[
            Skill.ATHLETICS,
            Skill.INTIMIDATION,
            Skill.PERCEPTION,
            Skill.SURVIVAL,
        ],
        saving_throw_proficiencies=[
            Ability.STRENGTH,
            Ability.CONSTITUTION,
        ],
        armor_class=18,
        max_hit_points=42,
        speed=25,
        hit_dice="5d10",
        experience_points=6500,
    )

    print("Character Created:")
    print(f"  Name: {grimnar.name}")
    print(f"  Class: {grimnar.character_class} {grimnar.level}")
    print(f"  Proficiency Bonus: +{grimnar.proficiency_bonus}")
    print()
    print("Ability Scores:")
    print(f"  STR: {grimnar.ability_scores.strength} ({grimnar.ability_scores.strength_modifier:+d})")
    print(f"  DEX: {grimnar.ability_scores.dexterity} ({grimnar.ability_scores.dexterity_modifier:+d})")
    print(f"  CON: {grimnar.ability_scores.constitution} ({grimnar.ability_scores.constitution_modifier:+d})")
    print(f"  INT: {grimnar.ability_scores.intelligence} ({grimnar.ability_scores.intelligence_modifier:+d})")
    print(f"  WIS: {grimnar.ability_scores.wisdom} ({grimnar.ability_scores.wisdom_modifier:+d})")
    print(f"  CHA: {grimnar.ability_scores.charisma} ({grimnar.ability_scores.charisma_modifier:+d})")
    print()
    print("Skills:")
    print(f"  Athletics: {grimnar.get_skill_modifier(Skill.ATHLETICS):+d} (proficient)")
    print(f"  Perception: {grimnar.get_skill_modifier(Skill.PERCEPTION):+d} (proficient)")
    print(f"  Stealth: {grimnar.get_skill_modifier(Skill.STEALTH):+d}")
    print()
    print("Saving Throws:")
    print(f"  STR: {grimnar.get_saving_throw(Ability.STRENGTH):+d} (proficient)")
    print(f"  DEX: {grimnar.get_saving_throw(Ability.DEXTERITY):+d}")
    print(f"  CON: {grimnar.get_saving_throw(Ability.CONSTITUTION):+d} (proficient)")
    print()
    print("Combat:")
    print(f"  AC: {grimnar.armor_class}")
    print(f"  Initiative: {grimnar.initiative:+d}")
    print(f"  HP: {grimnar.current_hit_points}/{grimnar.max_hit_points}")
    print(f"  Hit Dice: {grimnar.hit_dice}")
    print()

    # Test JSON export/import
    print("Testing JSON serialization...")
    test_path = Path("test_character.json")
    grimnar.to_json(test_path)
    print(f"  ✓ Saved to {test_path}")

    loaded = Character.from_json(test_path)
    print(f"  ✓ Loaded: {loaded.name} (Level {loaded.level} {loaded.character_class})")

    # Verify calculations match
    assert loaded.proficiency_bonus == grimnar.proficiency_bonus, "Proficiency bonus mismatch"
    assert loaded.get_skill_modifier(Skill.ATHLETICS) == grimnar.get_skill_modifier(Skill.ATHLETICS), "Skill modifier mismatch"
    assert loaded.ability_scores.strength_modifier == grimnar.ability_scores.strength_modifier, "Ability modifier mismatch"
    print("  ✓ All calculations verified")

    # Cleanup
    test_path.unlink()
    print("  ✓ Cleanup complete")
    print()
    print("✓ Character data model is working correctly!")
