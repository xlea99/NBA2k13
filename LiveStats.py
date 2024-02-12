import profiler
import sys
import BaseFunctions as b
import DataStorage
import StatsRipper
import sqlite3




class LiveStats:

    def __init__(self):
        pass


    # This method simply converts the Stats.db file into a neatly formatted Python dictionary
    # for further processing.
    def getRawStats(self):
        # Connect to the SQLite database
        conn = sqlite3.connect(f"{b.paths.databases}\\Stats.db")
        cursor = conn.cursor()

        # Fetch all games
        cursor.execute("SELECT * FROM Games")
        games = cursor.fetchall()

        # Initialize the main dictionary to store game data
        games_dict = {}

        # Iterate over each game to fetch its details and related player slots
        for game in games:
            game_id = game[0]  # Assuming GameID is the first column
            game_dict = {
                "GameID": game[0],
                "LoadedRoster": game[1],
                "Mode": game[2],
                "PlayDate": game[3],
                "GameDuration": game[4],
                "BallerzScore": game[5],
                "RingersScore": game[6],
                "ExtraValues": game[7:17]  # Assuming ExtraValue1 to ExtraValue10 are the last columns
            }

            # Fetch player slots for this game
            cursor.execute("SELECT * FROM PlayerSlots WHERE GameID = ?", (game_id,))
            player_slots = cursor.fetchall()

            # Convert player slots to dictionaries
            player_slots_dicts = []
            for slot in player_slots:
                slot_dict = {
                    "PlayerSlot": slot[1],
                    "IsActive": slot[2],
                    "SpriteID": slot[3],
                    # Add all other PlayerSlots fields here
                    "Unknown2": slot[-1],  # Assuming Unknown2 is the last column
                }
                player_slots_dicts.append(slot_dict)

            # Add the player slots list to the game dictionary
            game_dict["PlayerSlots"] = player_slots_dicts

            # Add this game's dictionary to the main dictionary
            games_dict[game_id] = game_dict

        # Close the database connection
        conn.close()

        return games_dict


k = LiveStats()
flounder = k.getRawStats()
