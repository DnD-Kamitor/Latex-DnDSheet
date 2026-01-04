"""
Spell data models for D&D 5e.
"""
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional, List, Dict, Set

from .enums import MagicSchool, SpellComponent


# Helper to load rulebook data
def _load_rulebook_data(filename: str) -> dict:
    path = Path(__file__).parent.parent.parent / "rulebooks" / "reference" / "calculations" / filename
    if not path.exists():
        path = Path("rulebooks/reference/calculations") / filename
    if not path.exists():
        raise FileNotFoundError(f"Could not find rulebook file: {filename} at path {path.resolve()}")
    with open(path, 'r') as f:
        return json.load(f)

SPELL_SLOT_DATA = _load_rulebook_data("spell-slots-by-level.json")


@dataclass
class Spell:
    """Represents a single spell."""
    name: str
    level: int
    school: MagicSchool
    casting_time: str
    range: str
    duration: str
    description: str
    components: Set[SpellComponent] = field(default_factory=set)
    material_component: Optional[str] = None
    higher_levels: Optional[str] = None
    ritual: bool = False
    concentration: bool = False

    @property
    def components_str(self) -> str:
        comp_list = [c.value for c in sorted(list(self.components))]
        if self.material_component:
            comp_list.append(f"M ({self.material_component})")
        return ", ".join(comp_list)


@dataclass
class SpellSlots:
    """Tracks spell slots for a character for a single spell level."""
    level: int
    max: int
    used: int = 0

    @property
    def remaining(self) -> int:
        return self.max - self.used

    def use_slot(self):
        if self.remaining <= 0:
            raise ValueError(f"No remaining spell slots for level {self.level}")
        self.used += 1

    def recover_slot(self):
        if self.used > 0:
            self.used -= 1

    def recover_all(self):
        self.used = 0


@dataclass
class Spellbook:
    """Manages all spells and spell slots for a character."""
    spells: List[Spell] = field(default_factory=list)
    prepared_spells: List[str] = field(default_factory=list)  # List of spell names
    spell_slots: Dict[int, SpellSlots] = field(default_factory=dict)  # Keyed by spell level

    def add_spell(self, spell: Spell):
        if spell.name not in [s.name for s in self.spells]:
            self.spells.append(spell)
            self.spells.sort(key=lambda s: (s.level, s.name))

    def get_spell(self, name: str) -> Optional[Spell]:
        for spell in self.spells:
            if spell.name == name:
                return spell
        return None

    def prepare_spell(self, spell_name: str):
        spell = self.get_spell(spell_name)
        if spell and spell.name not in self.prepared_spells:
            self.prepared_spells.append(spell.name)
            self.prepared_spells.sort()

    def unprepare_spell(self, spell_name: str):
        if spell_name in self.prepared_spells:
            self.prepared_spells.remove(spell_name)

    def is_prepared(self, spell_name: str) -> bool:
        spell = self.get_spell(spell_name)
        if not spell:
            return False
        # Cantrips are always considered prepared
        if spell.level == 0:
            return True
        return spell.name in self.prepared_spells

    def get_prepared_spells_by_level(self) -> Dict[int, List[Spell]]:
        by_level: Dict[int, List[Spell]] = {}
        
        # Add all cantrips
        cantrips = [s for s in self.spells if s.level == 0]
        if cantrips:
            by_level[0] = sorted(cantrips, key=lambda s: s.name)

        # Add all prepared spells
        for spell_name in self.prepared_spells:
            spell = self.get_spell(spell_name)
            if spell and spell.level > 0:
                if spell.level not in by_level:
                    by_level[spell.level] = []
                by_level[spell.level].append(spell)
        
        # Sort prepared spells within each level
        for level in by_level:
            if level > 0:
                by_level[level].sort(key=lambda s: s.name)
                
        return by_level

    def get_prepared_spells(self) -> List[Spell]:
        """Returns a single, sorted list of all prepared spells (including cantrips)."""
        prepared_list = []
        spells_by_level = self.get_prepared_spells_by_level()
        for level in sorted(spells_by_level.keys()):
            prepared_list.extend(spells_by_level[level])
        return prepared_list

    def update_spell_slots(self, character_level: int, character_class: str):
        """Calculates and sets the spell slots based on character level and class."""
        self.spell_slots.clear()
        caster_type = None
        for type_name, type_data in SPELL_SLOT_DATA["caster_types"].items():
            if character_class in type_data["classes"]:
                caster_type = type_name
                break
        
        if caster_type is None:
            return # Not a spellcasting class

        level_str = str(character_level)

        if caster_type == "pact":
            pact_data = SPELL_SLOT_DATA["caster_types"]["pact"]["slots_by_level"].get(level_str)
            if pact_data:
                slot_level = pact_data["level"]
                num_slots = pact_data["slots"]
                self.spell_slots[slot_level] = SpellSlots(level=slot_level, max=num_slots)
        else:
            slots_for_level = SPELL_SLOT_DATA["caster_types"][caster_type]["slots_by_level"].get(level_str)
            if slots_for_level:
                for slot_level_str, num_slots in slots_for_level.items():
                    slot_level = int(slot_level_str)
                    self.spell_slots[slot_level] = SpellSlots(level=slot_level, max=num_slots)
