"""
Core enumerations for D&D 5e data models.
"""
from enum import Enum


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


class MagicSchool(str, Enum):
    """Schools of magic in D&D 5e."""
    ABJURATION = "Abjuration"
    CONJURATION = "Conjuration"
    DIVINATION = "Divination"
    ENCHANTMENT = "Enchantment"
    EVOCATION = "Evocation"
    ILLUSION = "Illusion"
    NECROMANCY = "Necromancy"
    TRANSMUTATION = "Transmutation"


class SpellComponent(str, Enum):
    """Spell components (V, S, M)."""
    VERBAL = "V"
    SOMATIC = "S"
    MATERIAL = "M"


class CastingTimeCategory(str, Enum):
    """Broad categories for spell casting times."""
    ACTION = "Action"
    BONUS_ACTION = "Bonus Action"
    REACTION = "Reaction"
    LONGER = "Longer"
