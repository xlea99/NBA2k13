from spritopia.common.paths import paths
import tomlkit

with open(paths["config"] / "backstories/profiles.toml", "r") as f:
    PROFILES_CFG = tomlkit.parse(f.read())

name = "John Fuckemup"
age = "30"
morality = None # (good, evil, neutral)
mannerisms = None # Semi-Rare
disposition = None
hobbies = None # Rare
fears = None # Rare
personal_goals = None
personal_events = None
faction = "Associated with the Peaky Blinders."
faction_status = None
faction_role = None
faction_goals = None
faction_events = None
secrets = None # Rare
regrets = None # Rare
religion = None # Rare
politics = None # Rare


def generateFullProfile(_name,_age,_morality,
                        _mannerisms,_disposition,_hobbies,_fears,
                        _personal_goals,_personal_events,
                        _faction,_faction_status,_faction_role,_faction_goals,_faction_events,
                        _secrets,_regrets,_religion,_politics,
                        _significant_figures : dict):
    pass
