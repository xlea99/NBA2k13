import json
from spritopia.common.paths import paths

# Localization of all values contained within a single "player" object.
with open(paths["localization"] / "player_vals.json","r",encoding="utf-8") as f:
    LOCALIZATION_PLAYERS = json.load(f)

# Localization of all values contained within a single "player" object.
with open(paths["localization"] / "stat_vals.json","r",encoding="utf-8") as f:
    LOCALIZATION_STATS = json.load(f)