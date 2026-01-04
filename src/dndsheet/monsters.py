"""
Monster data models for D&D 5e.
"""

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional, List, Dict, Any

from .enums import Ability, Skill


@dataclass
class MonsterAction:
    """Represents a monster's action, trait, or legendary action."""
    name: str
    desc: str


@dataclass
class Monster:
    """Represents a D&D 5e monster."""
    name: str
    size: str = "Medium"
    type: str = "humanoid"
    alignment: str = "unaligned"
    ac: int = 10
    hp: int = 1
    hit_dice: str = "1d8"
    speed: str = "30 ft."
    
    # Abilities
    strength: int = 10
    dexterity: int = 10
    constitution: int = 10
    intelligence: int = 10
    wisdom: int = 10
    charisma: int = 10

    # Derived stats
    cr: float = 0.0 # Challenge Rating (e.g., 0.25 for 1/4, 0.5 for 1/2)
    xp: int = 0
    proficiency_bonus: int = 2 # Most monsters use proficiency bonus based on CR/level (often CR/4 rounded up)

    # Proficiencies
    saving_throws: Dict[Ability, int] = field(default_factory=dict) # e.g., {Ability.DEXTERITY: 2}
    skills: Dict[Skill, int] = field(default_factory=dict) # e.g., {Skill.PERCEPTION: 4}
    damage_vulnerabilities: List[str] = field(default_factory=list)
    damage_resistances: List[str] = field(default_factory=list)
    damage_immunities: List[str] = field(default_factory=list)
    condition_immunities: List[str] = field(default_factory=list)
    senses: str = "passive Perception 10"
    languages: str = "—"

    # Abilities, actions, etc.
    traits: List[MonsterAction] = field(default_factory=list)
    actions: List[MonsterAction] = field(default_factory=list)
    legendary_actions: List[MonsterAction] = field(default_factory=list)
    description: Optional[str] = None
    
    # Custom post-init for XP based on CR
    def __post_init__(self):
        if self.xp == 0: # Auto-calculate XP if not provided
            self.xp = self._calculate_xp_from_cr(self.cr)

    def _calculate_xp_from_cr(self, cr: float) -> int:
        # Based on DMG p. 82 - Encounter Building
        xp_table = {
            0: 10, 0.125: 25, 0.25: 50, 0.5: 100, 1: 200, 2: 450, 3: 700,
            4: 1100, 5: 1800, 6: 2300, 7: 2900, 8: 3900, 9: 5000, 10: 5900,
            11: 7200, 12: 8400, 13: 10000, 14: 11500, 15: 13000, 16: 15000,
            17: 18000, 18: 20000, 19: 22000, 20: 25000, 21: 33000, 22: 41000,
            23: 50000, 24: 62000, 25: 75000, 26: 90000, 27: 105000, 28: 120000,
            29: 135000, 30: 155000
        }
        return xp_table.get(cr, 0) # Return 0 for unknown CRs
        
    def get_ability_modifier(self, ability: Ability) -> int:
        score = getattr(self, ability.value)
        return (score - 10) // 2
        
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Monster":
        """
        Creates a Monster instance from a dictionary, handling nested objects.
        """
        # Convert ability strings to Ability enums if present
        if 'saving_throws' in data:
            data['saving_throws'] = {Ability(k): v for k, v in data['saving_throws'].items()}
        if 'skills' in data:
            data['skills'] = {Skill(k): v for k, v in data['skills'].items()}
        
        # Convert action dicts to MonsterAction instances
        for list_attr in ['traits', 'actions', 'legendary_actions']:
            if list_attr in data:
                data[list_attr] = [MonsterAction(**a_data) for a_data in data[list_attr]]
                
        return cls(**data)


def load_monster_data(filepath: Path) -> Monster:
    """Loads monster data from a JSON file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return Monster.from_dict(data)

def load_all_monsters_from_dir(dir_path: Path) -> List[Monster]:
    """Loads all monster data from JSON files in a given directory."""
    monsters = []
    if dir_path.is_dir():
        for file in dir_path.glob("*.json"):
            try:
                monsters.append(load_monster_data(file))
            except Exception as e:
                print(f"Warning: Could not load monster from {file}: {e}")
    return monsters


if __name__ == "__main__":
    # Example usage:
    goblin_data = {
        "name": "Goblin",
        "size": "Small",
        "type": "humanoid (goblinoid)",
        "alignment": "neutral evil",
        "ac": 15,
        "hp": 7,
        "hit_dice": "2d6",
        "speed": "30 ft.",
        "strength": 8, "dexterity": 14, "constitution": 10,
        "intelligence": 10, "wisdom": 8, "charisma": 8,
        "cr": 0.25,
        "skills": {"stealth": 6},
        "senses": "darkvision 60 ft., passive Perception 9",
        "languages": "Common, Goblin",
        "traits": [
            {"name": "Nimble Escape", "desc": "The goblin can take the Disengage or Hide action as a bonus action on each of its turns."}
        ],
        "actions": [
            {"name": "Scimitar", "desc": "Melee Weapon Attack: +4 to hit, reach 5 ft., one target. Hit: 5 (1d6 + 2) slashing damage."},
            {"name": "Shortbow", "desc": "Ranged Weapon Attack: +4 to hit, range 80/320 ft., one target. Hit: 5 (1d6 + 2) piercing damage."}
        ]
    }
    
    goblin = Monster.from_dict(goblin_data)
    print(f"Loaded Monster: {goblin.name}, CR: {goblin.cr}, XP: {goblin.xp}")
    print(f"Goblin Dex Mod: {goblin.get_ability_modifier(Ability.DEXTERITY)}")
    if goblin.traits:
        print(f"First Trait: {goblin.traits[0].name}")

    # Create a dummy monsters directory and save sample
    monsters_dir = Path("output/monsters_test")
    monsters_dir.mkdir(parents=True, exist_ok=True)
    with open(monsters_dir / "goblin.json", "w") as f:
        json.dump(goblin_data, f, indent=2)

    loaded_monsters = load_all_monsters_from_dir(monsters_dir)
    print(f"\nLoaded {len(loaded_monsters)} monsters from directory.")
    if loaded_monsters:
        print(f"First loaded: {loaded_monsters[0].name}")
    
    # Cleanup
    # for file in monsters_dir.glob("*.json"):
    #     file.unlink()
    # monsters_dir.rmdir()
