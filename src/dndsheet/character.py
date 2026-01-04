"""
Character data models for D&D 5e.

This module defines the core character data structure using dataclasses.
"""

import json
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Optional, List, Set

from .enums import Ability, Skill, SKILL_ABILITIES, MagicSchool, SpellComponent
from .spells import Spellbook, Spell


# Helper to load rulebook data
def _load_rulebook_data(filename: str) -> dict:
    # This is a simplification. In a real app, you might have a dedicated asset loader.
    # It assumes the script is run from the project root or tests/.
    path = Path(__file__).parent.parent.parent / "rulebooks" / "reference" / "calculations" / filename
    if not path.exists():
        # Fallback for different execution contexts
        path = Path("rulebooks/reference/calculations") / filename
    if not path.exists():
        raise FileNotFoundError(f"Could not find rulebook file: {filename} at path {path.resolve()}")
    with open(path, 'r') as f:
        return json.load(f)


PROFICIENCY_BONUS_DATA = _load_rulebook_data("proficiency-bonus.json")["proficiency_by_level"]
ABILITY_MODIFIER_DATA = _load_rulebook_data("ability-modifiers.json")["modifier_table"]


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
        for ability in ['strength', 'dexterity', 'constitution', 'intelligence', 'wisdom', 'charisma']:
            value = getattr(self, ability)
            if not (1 <= value <= 30):
                raise ValueError(f"{ability} must be between 1 and 30, got {value}")

    def get_score(self, ability: Ability) -> int:
        return getattr(self, ability.value)

    def get_modifier(self, ability: Ability) -> int:
        score = self.get_score(ability)
        return ABILITY_MODIFIER_DATA.get(str(score), (score - 10) // 2)

    @property
    def strength_modifier(self) -> int: return self.get_modifier(Ability.STRENGTH)
    @property
    def dexterity_modifier(self) -> int: return self.get_modifier(Ability.DEXTERITY)
    @property
    def constitution_modifier(self) -> int: return self.get_modifier(Ability.CONSTITUTION)
    @property
    def intelligence_modifier(self) -> int: return self.get_modifier(Ability.INTELLIGENCE)
    @property
    def wisdom_modifier(self) -> int: return self.get_modifier(Ability.WISDOM)
    @property
    def charisma_modifier(self) -> int: return self.get_modifier(Ability.CHARISMA)


@dataclass
class Character:
    """D&D 5e character sheet data model."""

    name: str
    race: str
    character_class: str
    level: int = 1
    player_name: Optional[str] = None
    background: Optional[str] = None
    alignment: Optional[str] = None
    ability_scores: AbilityScores = field(default_factory=AbilityScores)
    skill_proficiencies: List[Skill] = field(default_factory=list)
    saving_throw_proficiencies: List[Ability] = field(default_factory=list)
    armor_class: int = 10
    initiative_bonus: Optional[int] = None
    speed: int = 30
    max_hit_points: int = 10
    current_hit_points: Optional[int] = None
    temporary_hit_points: int = 0
    hit_dice: str = "1d8"
    inspiration: bool = False
    experience_points: int = 0
    spellcasting_ability: Optional[Ability] = None
    spellbook: Spellbook = field(default_factory=Spellbook)

    def __post_init__(self):
        if not (1 <= self.level <= 20):
            raise ValueError(f"Level must be between 1 and 20, got {self.level}")
        if not self.name or len(self.name) > 100:
            raise ValueError("Name must be 1-100 characters")
        if self.current_hit_points is None:
            self.current_hit_points = self.max_hit_points
        if self.max_hit_points < 1:
            raise ValueError("Max hit points must be at least 1")
        if self.current_hit_points < 0:
            raise ValueError("Current hit points cannot be negative")
        if not (1 <= self.armor_class <= 30):
            raise ValueError("Armor class must be between 1 and 30")
        
        # Automatically update spell slots based on class and level
        self.spellbook.update_spell_slots(self.level, self.character_class)

    @property
    def proficiency_bonus(self) -> int:
        return PROFICIENCY_BONUS_DATA.get(str(self.level), 0)

    @property
    def initiative(self) -> int:
        initiative = self.ability_scores.dexterity_modifier
        if self.initiative_bonus is not None:
            initiative += self.initiative_bonus
        return initiative

    @property
    def spell_save_dc(self) -> Optional[int]:
        if not self.spellcasting_ability:
            return None
        mod = self.ability_scores.get_modifier(self.spellcasting_ability)
        return 8 + self.proficiency_bonus + mod

    @property
    def spell_attack_bonus(self) -> Optional[int]:
        if not self.spellcasting_ability:
            return None
        mod = self.ability_scores.get_modifier(self.spellcasting_ability)
        return self.proficiency_bonus + mod

    def get_skill_modifier(self, skill: Skill) -> int:
        ability = SKILL_ABILITIES[skill]
        modifier = self.ability_scores.get_modifier(ability)
        if skill in self.skill_proficiencies:
            modifier += self.proficiency_bonus
        return modifier

    def get_saving_throw(self, ability: Ability) -> int:
        modifier = self.ability_scores.get_modifier(ability)
        if ability in self.saving_throw_proficiencies:
            modifier += self.proficiency_bonus
        return modifier

    @classmethod
    def from_json(cls, json_path: Path) -> "Character":
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        if 'class' in data:
            data['character_class'] = data.pop('class')
        if 'ability_scores' in data and isinstance(data['ability_scores'], dict):
            data['ability_scores'] = AbilityScores(**data['ability_scores'])
        if 'skill_proficiencies' in data:
            data['skill_proficiencies'] = [Skill(s) for s in data['skill_proficiencies']]
        if 'saving_throw_proficiencies' in data:
            data['saving_throw_proficiencies'] = [Ability(a) for a in data['saving_throw_proficiencies']]
        if 'spellcasting_ability' in data and data['spellcasting_ability']:
            data['spellcasting_ability'] = Ability(data['spellcasting_ability'])
        
        # Deserialize spellbook
        if 'spellbook' in data:
            spellbook_data = data['spellbook']
            spells_data = spellbook_data.get('spells', [])
            spells = []
            for s_data in spells_data:
                # Convert component strings back to enums
                s_data['components'] = {SpellComponent(c) for c in s_data.get('components', [])}
                # Convert school string back to enum
                s_data['school'] = MagicSchool(s_data['school'])
                spells.append(Spell(**s_data))

            data['spellbook'] = Spellbook(
                spells=spells,
                prepared_spells=spellbook_data.get('prepared_spells', [])
            )
        
        return cls(**data)

    def to_json(self, json_path: Path, indent: int = 2) -> None:
        json_path.parent.mkdir(parents=True, exist_ok=True)
        data = asdict(self)
        
        # Basic field conversions
        data['class'] = data.pop('character_class')
        if data.get('skill_proficiencies'):
            data['skill_proficiencies'] = [s.value for s in data['skill_proficiencies']]
        if data.get('saving_throw_proficiencies'):
            data['saving_throw_proficiencies'] = [a.value for a in data['saving_throw_proficiencies']]
        if data.get('spellcasting_ability'):
            data['spellcasting_ability'] = data['spellcasting_ability'].value
        
        # Custom serialization for spellbook
        spellbook_dict = asdict(self.spellbook)
        serialized_spells = []
        for spell in self.spellbook.spells:
            spell_data = asdict(spell)
            # Convert enums to their string values for JSON
            spell_data['school'] = spell.school.value
            spell_data['components'] = [c.value for c in spell.components]
            serialized_spells.append(spell_data)
        
        spellbook_dict['spells'] = serialized_spells
        data['spellbook'] = spellbook_dict
        
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=indent)


if __name__ == "__main__":
    # Create a test character with spellcasting
    elara_spells = [
        Spell("Fire Bolt", 0, MagicSchool.EVOCATION, "1 Action", "120 feet", "Instantaneous", "You hurl a mote of fire...", components={SpellComponent.VERBAL, SpellComponent.SOMATIC}),
        Spell("Mage Armor", 1, MagicSchool.ABJURATION, "1 Action", "Touch", "8 hours", "You touch a willing creature...", components={SpellComponent.VERBAL, SpellComponent.SOMATIC, SpellComponent.MATERIAL}, material_component="a piece of cured leather"),
        Spell("Magic Missile", 1, MagicSchool.EVOCATION, "1 Action", "120 feet", "Instantaneous", "You create three glowing darts...", components={SpellComponent.VERBAL, SpellComponent.SOMATIC}),
        Spell("Misty Step", 2, MagicSchool.CONJURATION, "1 Bonus Action", "Self", "Instantaneous", "Briefly surrounded by silvery mist...", components={SpellComponent.VERBAL})
    ]

    elara = Character(
        name="Elara Moonwhisper",
        player_name="Test Player",
        race="High Elf",
        character_class="Wizard",
        level=3,
        background="Sage",
        alignment="Neutral Good",
        ability_scores=AbilityScores(
            strength=8, dexterity=14, constitution=12,
            intelligence=17, wisdom=13, charisma=10
        ),
        skill_proficiencies=[Skill.ARCANA, Skill.HISTORY],
        saving_throw_proficiencies=[Ability.INTELLIGENCE, Ability.WISDOM],
        armor_class=12,
        max_hit_points=18,
        speed=30,
        hit_dice="3d6",
        spellcasting_ability=Ability.INTELLIGENCE,
        spellbook=Spellbook(spells=elara_spells)
    )
    elara.spellbook.prepare_spell("Mage Armor")
    elara.spellbook.prepare_spell("Magic Missile")

    print("Character Created:")
    print(f"  Name: {elara.name}")
    print(f"  Class: {elara.character_class} {elara.level}")
    print(f"  Proficiency Bonus: +{elara.proficiency_bonus}")
    print(f"  Spellcasting Ability: {elara.spellcasting_ability.value}")
    print(f"  Spell Save DC: {elara.spell_save_dc}")
    print(f"  Spell Attack Bonus: +{elara.spell_attack_bonus}")
    print("\nSpell Slots:")
    for level, slots in sorted(elara.spellbook.spell_slots.items()):
        print(f"  Level {level}: {slots.remaining}/{slots.max}")
    
    print("\nPrepared Spells:")
    for level, spells in sorted(elara.spellbook.get_prepared_spells_by_level().items()):
        print(f"  Level {level}: {', '.join(s.name for s in spells)}")

    # Test JSON export/import
    print("\nTesting JSON serialization...")
    test_path = Path("test_character_spells.json")
    elara.to_json(test_path)
    print(f"  ✓ Saved to {test_path}")

    loaded = Character.from_json(test_path)
    print(f"  ✓ Loaded: {loaded.name} (Level {loaded.level} {loaded.character_class})")
    assert loaded.spell_save_dc == elara.spell_save_dc
    assert loaded.spellbook.get_spell("Fire Bolt") is not None
    assert loaded.spellbook.is_prepared("Mage Armor")
    assert loaded.spellbook.spell_slots[1].max == 4
    print("  ✓ All spell data verified")

    test_path.unlink()
    print("  ✓ Cleanup complete")
    print("\n✓ Character data model with spells is working correctly!")
