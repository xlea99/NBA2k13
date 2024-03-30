import os
import tomlkit
from spritopia.common.paths import paths


# Sets up the main.toml file, which is assumed to exist at root/config
with open(os.path.join(paths.get("config"),"main.toml"), "r") as f:
    config = tomlkit.parse(f.read())


# Registers the data folder given in the config in global paths
paths["saveFolder"] = config["paths"]["saveFolder"]
paths["logs"] = paths["saveFolder"] / "logs"
paths["backups"] = paths["saveFolder"] / "backups"
paths["rosterCSVs"] = paths["saveFolder"] / "roster_csvs"
paths["saveDBs"] = paths["saveFolder"] / "db"

# Registers the NBA2K13 game data and roaming folder in the config in global paths.
paths["gameInstall"] = config["paths"]["gameInstall"]
paths["gameRoaming"] = paths["appdata"] / "2K Sports/NBA 2K13"
paths["gameRosters"] = paths["gameRoaming"] / "Saves"