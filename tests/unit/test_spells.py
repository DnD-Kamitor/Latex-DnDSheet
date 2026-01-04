"""
Tests for spellcasting data models and logic.
"""

import pytest
from pathlib import Path
import json

from dndsheet.character import Character, AbilityScores
from dndsheet.enums import Ability, Skill, SpellComponent
from dndsheet.spells import Spell, Spellbook, MagicSchool, SpellSlots

@pytest.fixture
def sample_wizard():
    """Returns a sample wizard character for testing."""
    return Character(
        name="Elara",
        race="High Elf",
        character_class="Wizard",
        level=5,
        ability_scores=AbilityScores(intelligence=18), # +4 modifier
        spellcasting_ability=Ability.INTELLIGENCE,
        saving_throw_proficiencies=[Ability.INTELLIGENCE]
    )

@pytest.fixture
def sample_spells():
    """Returns a list of sample spells."""
    return [
        Spell("Fire Bolt", 0, MagicSchool.EVOCATION, "1 Action", "120 feet", "Instantaneous", "Hurl a mote of fire.", components={SpellComponent.VERBAL, SpellComponent.SOMATIC}),
        Spell("Magic Missile", 1, MagicSchool.EVOCATION, "1 Action", "120 feet", "Instantaneous", "Create three glowing darts.", components={SpellComponent.VERBAL, SpellComponent.SOMATIC}),
        Spell("Misty Step", 2, MagicSchool.CONJURATION, "1 Bonus Action", "Self", "Instantaneous", "Teleport up to 30 feet.", components={SpellComponent.VERBAL}),
    ]

def test_spell_creation():
    spell = Spell("Test Spell", 1, MagicSchool.ABJURATION, "1 Action", "Self", "1 round", "Test description.", components={SpellComponent.VERBAL})
    assert spell.name == "Test Spell"
    assert spell.level == 1
    assert spell.school == MagicSchool.ABJURATION
    assert spell.components == {SpellComponent.VERBAL}

def test_spellbook_add_spell(sample_spells):
    book = Spellbook()
    book.add_spell(sample_spells[0])
    assert len(book.spells) == 1
    assert book.spells[0].name == "Fire Bolt"
    # Test that adding the same spell doesn't duplicate it
    book.add_spell(sample_spells[0])
    assert len(book.spells) == 1

def test_spellbook_prepare_unprepare(sample_spells):
    book = Spellbook(spells=sample_spells)
    # Cantrips (level 0) are always prepared
    assert book.is_prepared("Fire Bolt")

    # Level 1+ spells must be prepared
    assert not book.is_prepared("Magic Missile")
    book.prepare_spell("Magic Missile")
    assert book.is_prepared("Magic Missile")
    book.unprepare_spell("Magic Missile")
    assert not book.is_prepared("Magic Missile")

def test_spell_dc_and_attack_bonus(sample_wizard):
    # Level 5, proficiency bonus is +3
    # INT modifier is +4
    # DC = 8 + prof + mod = 8 + 3 + 4 = 15
    assert sample_wizard.spell_save_dc == 15
    # Attack = prof + mod = 3 + 4 = 7
    assert sample_wizard.spell_attack_bonus == 7

def test_spell_dc_no_ability():
    char = Character("Test", "Human", "Fighter", 1)
    assert char.spell_save_dc is None
    assert char.spell_attack_bonus is None

def test_spell_slots():
    slots = SpellSlots(level=1, max=4, used=1)
    assert slots.remaining == 3
    slots.use_slot()
    assert slots.remaining == 2
    assert slots.used == 2
    slots.recover_slot()
    assert slots.remaining == 3
    slots.recover_all()
    assert slots.remaining == 4
    assert slots.used == 0

def test_use_empty_spell_slots():
    slots = SpellSlots(level=1, max=2, used=2)
    with pytest.raises(ValueError):
        slots.use_slot()

def test_character_json_serialization_with_spells(sample_wizard, sample_spells, tmp_path):
    """Test saving and loading a character with a spellbook to JSON."""
    sample_wizard.spellbook = Spellbook(spells=sample_spells)
    sample_wizard.spellbook.prepare_spell("Magic Missile")

    json_path = tmp_path / "character.json"
    sample_wizard.to_json(json_path)

    assert json_path.exists()

    # Load and verify
    loaded_char = Character.from_json(json_path)
    assert loaded_char.name == sample_wizard.name
    assert loaded_char.spellcasting_ability == Ability.INTELLIGENCE
    assert len(loaded_char.spellbook.spells) == 3
    assert loaded_char.spellbook.get_spell("Fire Bolt") is not None
    assert loaded_char.spellbook.is_prepared("Magic Missile")
    assert not loaded_char.spellbook.is_prepared("Misty Step")
    assert loaded_char.spell_save_dc == 15
