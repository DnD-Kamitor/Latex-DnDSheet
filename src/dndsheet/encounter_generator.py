"""
Encounter building logic for D&D 5e.
"""

from typing import List, Dict
from dataclasses import dataclass, field

from .monsters import Monster


# XP Thresholds by Character Level (DMG p. 82)
XP_THRESHOLDS = {
    1: {"easy": 25, "medium": 50, "hard": 75, "deadly": 100},
    2: {"easy": 50, "medium": 100, "hard": 150, "deadly": 200},
    3: {"easy": 75, "medium": 150, "hard": 225, "deadly": 400},
    4: {"easy": 125, "medium": 250, "hard": 375, "deadly": 500},
    5: {"easy": 250, "medium": 500, "hard": 750, "deadly": 1100},
    6: {"easy": 300, "medium": 600, "hard": 900, "deadly": 1400},
    7: {"easy": 350, "medium": 750, "hard": 1100, "deadly": 1700},
    8: {"easy": 450, "medium": 900, "hard": 1400, "deadly": 2100},
    9: {"easy": 550, "medium": 1100, "hard": 1600, "deadly": 2400},
    10: {"easy": 600, "medium": 1200, "hard": 1900, "deadly": 2800},
    11: {"easy": 800, "medium": 1600, "hard": 2400, "deadly": 3600},
    12: {"easy": 1000, "medium": 2000, "hard": 3000, "deadly": 4500},
    13: {"easy": 1100, "medium": 2200, "hard": 3300, "deadly": 5000},
    14: {"easy": 1250, "medium": 2500, "hard": 3800, "deadly": 5700},
    15: {"easy": 1400, "medium": 2800, "hard": 4300, "deadly": 6400},
    16: {"easy": 1600, "medium": 3200, "hard": 4800, "deadly": 7200},
    17: {"easy": 2000, "medium": 3900, "hard": 5900, "deadly": 8800},
    18: {"easy": 2100, "medium": 4200, "hard": 6300, "deadly": 9500},
    19: {"easy": 2400, "medium": 4900, "hard": 7300, "deadly": 10900},
    20: {"easy": 2800, "medium": 5700, "hard": 8500, "deadly": 12700},
}

# Adjusted XP Multipliers by Number of Monsters (DMG p. 82)
ADJUSTED_XP_MULTIPLIERS = {
    1: 1.0,
    2: 1.5,
    3: 2.0,
    4: 2.0,
    5: 2.0,
    6: 2.0,
    7: 2.5,
    8: 2.5,
    9: 2.5,
    10: 2.5,
    11: 3.0,
    12: 3.0,
    13: 3.0,
    14: 3.0,
    15: 3.0,
}


@dataclass
class Encounter:
    """Represents a combat encounter with monsters."""
    monsters: List[Monster] = field(default_factory=list)
    party_size: int = 4
    average_party_level: int = 1

    def add_monster(self, monster: Monster):
        self.monsters.append(monster)

    def remove_monster(self, monster: Monster):
        if monster in self.monsters:
            self.monsters.remove(monster)

    @property
    def total_raw_xp(self) -> int:
        """Calculates the sum of raw XP for all monsters in the encounter."""
        return sum(m.xp for m in self.monsters)

    @property
    def adjusted_xp(self) -> int:
        """
        Calculates the adjusted XP for the encounter, applying both monster count
        and party size multipliers.
        """
        num_monsters = len(self.monsters)
        if num_monsters == 0:
            return 0

        # Monster count multiplier (DMG p. 82)
        monster_count_multiplier = 1.0
        if num_monsters >= len(ADJUSTED_XP_MULTIPLIERS):
            monster_count_multiplier = ADJUSTED_XP_MULTIPLIERS[max(ADJUSTED_XP_MULTIPLIERS.keys())]
        else:
            monster_count_multiplier = ADJUSTED_XP_MULTIPLIERS[num_monsters]

        raw_xp = self.total_raw_xp
        adjusted_by_monster_count = raw_xp * monster_count_multiplier

        # Party size multiplier (DMG p. 82)
        party_size_multiplier = 1.0
        if self.party_size < 3: # For parties of 1-2 characters
            # "If the party contains three or fewer characters, multiply the final XP total by 1.5."
            # The DMG implies this applies to the *total XP of the monsters*,
            # which is what `adjusted_by_monster_count` is at this point.
            party_size_multiplier = 1.5
        elif self.party_size > 5: # For parties of 6 or more characters
            # "If the party contains six or more characters, multiply the final XP total by 0.5."
            party_size_multiplier = 0.5

        return int(adjusted_by_monster_count * party_size_multiplier)

    @property
    def difficulty(self) -> str:
        """Determines the encounter difficulty (Easy, Medium, Hard, Deadly)."""
        if self.party_size < 1 or self.average_party_level < 1:
            return "Undefined (invalid party info)"
        if not self.monsters:
            return "None (no monsters)"

        party_thresholds_per_char = XP_THRESHOLDS.get(self.average_party_level)
        if not party_thresholds_per_char:
            return "Undefined (invalid party level)"

        # Calculate total party XP thresholds
        easy_threshold = party_thresholds_per_char["easy"] * self.party_size
        medium_threshold = party_thresholds_per_char["medium"] * self.party_size
        hard_threshold = party_thresholds_per_char["hard"] * self.party_size
        deadly_threshold = party_thresholds_per_char["deadly"] * self.party_size

        adj_xp = self.adjusted_xp

        if adj_xp >= deadly_threshold:
            return "Deadly"
        elif adj_xp >= hard_threshold:
            return "Hard"
        elif adj_xp >= medium_threshold:
            return "Medium"
        elif adj_xp >= easy_threshold:
            return "Easy"
        else:
            return "Trivial"

