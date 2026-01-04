"""
Tests for spellcasting logic, particularly spell slot calculation.
"""

import pytest
from dndsheet.character import Character
from dndsheet.spells import Spell, MagicSchool, SpellComponent, Spellbook

# Test cases: (character_class, level, expected_slots_dict)
SPELL_SLOT_TEST_CASES = [
    # Full Casters (Wizard)
    ("Wizard", 1, {1: 2}),
    ("Wizard", 3, {1: 4, 2: 2}),
    ("Wizard", 5, {1: 4, 2: 3, 3: 2}),
    ("Wizard", 20, {1: 4, 2: 3, 3: 3, 4: 3, 5: 3, 6: 2, 7: 2, 8: 1, 9: 1}),
    # Half Casters (Paladin)
    ("Paladin", 1, {}),
    ("Paladin", 2, {1: 2}),
    ("Paladin", 5, {1: 4, 2: 2}),
    ("Paladin", 17, {1: 4, 2: 3, 3: 3, 4: 3, 5: 1}),
    # Third Casters (Arcane Trickster)
    ("Arcane Trickster", 2, {}),
    ("Arcane Trickster", 3, {1: 2}),
    ("Arcane Trickster", 7, {1: 4, 2: 2}),
    ("Arcane Trickster", 19, {1: 4, 2: 3, 3: 3, 4: 1}),
    # Pact Magic (Warlock)
    # Pact slots are different: only one level of slot
    ("Warlock", 1, {1: 1}),
    ("Warlock", 2, {1: 2}),
    ("Warlock", 5, {3: 2}),
    ("Warlock", 17, {5: 4}),
    # Non-Caster (Fighter)
    ("Fighter", 5, {}),
]

@pytest.mark.parametrize("character_class, level, expected_slots", SPELL_SLOT_TEST_CASES)
def test_update_spell_slots(character_class, level, expected_slots):
    """
    Tests that spell slots are correctly calculated for different classes and levels.
    """
    char = Character(
        name="Test Caster",
        race="Human",
        character_class=character_class,
        level=level,
    )
    
    # The __post_init__ of Character should have already called update_spell_slots
    calculated_slots = {
        level: slots.max for level, slots in char.spellbook.spell_slots.items()
    }
    
    assert calculated_slots == expected_slots, \
        f"Failed for {character_class} Lvl {level}. Expected {expected_slots}, got {calculated_slots}"


def test_get_prepared_spells():
    """
    Tests the get_prepared_spells method to ensure it returns a correctly
    sorted flat list of cantrips and prepared spells.
    """
    spells = [
        Spell("C", 1, MagicSchool.EVOCATION, "1 Action", "120 ft", "Instantaneous", "..."),
        Spell("B", 0, MagicSchool.EVOCATION, "1 Action", "120 ft", "Instantaneous", "..."),
        Spell("A", 2, MagicSchool.CONJURATION, "1 Bonus Action", "Self", "Instantaneous", "..."),
        Spell("D", 1, MagicSchool.ABJURATION, "1 Action", "Touch", "8 hours", "..."),
    ]
    char = Character(
        name="Sorter",
        race="Elf",
        character_class="Wizard",
        level=3,
        spellbook=Spellbook(spells=spells)
    )
    
    # Prepare A and C, B is a cantrip (always prepared), D is not prepared
    char.spellbook.prepare_spell("A")
    char.spellbook.prepare_spell("C")
    
    prepared_list = char.spellbook.get_prepared_spells()
    
    # Expected order: B (Lvl 0), C (Lvl 1), A (Lvl 2)
    expected_names = ["B", "C", "A"]
    actual_names = [spell.name for spell in prepared_list]
    
    assert actual_names == expected_names, "Prepared spells are not sorted correctly by level then name."
    assert len(prepared_list) == 3, "Should only include cantrips and prepared spells."
    assert "D" not in actual_names, "Unprepared spell should not be in the list."
