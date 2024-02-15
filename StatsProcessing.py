import BaseFunctions as b
import DataStorage


# This method, given a DataStorage object with a Raw stats dictionary, generates the Player history dictionary,
# which simply lists all games that the player has played in along with their stats.
def generatePlayerGamesList(dataStorageObject):
    playerGamesList = {}
    for gameId,gameInfo in dataStorageObject.stats["Raw"].items():
        for slotId,slotInfo in gameInfo["PlayerSlots"].items():
            if(slotInfo["IsActive"] == 1):
                if(slotInfo["SpriteID"] not in playerGamesList.keys()):
                    playerGamesList[slotInfo["SpriteID"]] = {"Games" : [],
                                                             "Totals" : {"GamesPlayed" : 0,
                                                                         "Wins" : 0,
                                                                         "Losses" : 0,
                                                                         "Points" : 0,
                                                                         "DefensiveRebounds" : 0,
                                                                         "OffensiveRebounds" : 0,
                                                                         "PointsPerAssist" : 0,
                                                                         "AssistCount" : 0,
                                                                         "Steals" : 0,
                                                                         "Blocks" : 0,
                                                                         "Turnovers" : 0,
                                                                         "InsidesMade" : 0,
                                                                         "InsidesAttempted" : 0,
                                                                         "ThreesMade" : 0,
                                                                         "ThreesAttempted" : 0,
                                                                         "Fouls" : 0,
                                                                         "Dunks" : 0,
                                                                         "Layups" : 0,
                                                                         "Unknown1" : 0,
                                                                         "Unknown2" : 0}}

                thisGame = slotInfo.copy()
                thisGame["LoadedRoster"] = gameInfo["LoadedRoster"]
                thisGame["PlayDate"] = gameInfo["PlayDate"]
                thisGame["BallerzScore"] = gameInfo["BallerzScore"]
                thisGame["RingersScore"] = gameInfo["RingersScore"]
                thisGame["GameDuration"] = gameInfo["GameDuration"]
                if((slotInfo["PlayerSlot"] <= 5 and thisGame["BallerzScore"] > thisGame["RingersScore"]) or (slotInfo["PlayerSlot"] >= 6 and thisGame["BallerzScore"] < thisGame["RingersScore"])):
                    thisGame["Win"] = True
                    playerGamesList[slotInfo["SpriteID"]]["Totals"]["Wins"] += 1
                else:
                    playerGamesList[slotInfo["SpriteID"]]["Totals"]["Losses"] += 1
                    thisGame["Win"] = False
                playerGamesList[slotInfo["SpriteID"]]["Totals"]["GamesPlayed"] += 1

                playerGamesList[slotInfo["SpriteID"]]["Games"].append(thisGame)
                for statToTotal in playerGamesList[slotInfo["SpriteID"]]["Totals"].keys():
                    if(statToTotal not in ["Wins","Losses","GamesPlayed"]):
                        playerGamesList[slotInfo["SpriteID"]]["Totals"][statToTotal] += slotInfo[statToTotal]

    dataStorageObject.stats["Players"] = playerGamesList


d = DataStorage.DataStorage()
generatePlayerGamesList(d)

