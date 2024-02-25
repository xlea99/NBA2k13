import BaseFunctions as b


# This method, given a DataStorage object with a Raw stats dictionary, generates the Player history dictionary,
# which simply lists all games that the player has played in along with their stats.
def generatePlayerGamesDict(dataStorageObject):
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

# Given a dataStorageObject with a PlayerGamesDict, this method simply calculates a set of averages.
def calculatePlayerAverages(dataStorageObject):
    for spriteID,playerStats in dataStorageObject.stats["Players"].items():
        playerStats["Averages"] = {"Points" : 0,
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
                                   "Unknown2" : 0}
        for statName in playerStats["Averages"].keys():
            playerStats["Averages"][statName] = round(playerStats["Totals"][statName] / playerStats["Totals"]["GamesPlayed"] if playerStats["Totals"]["GamesPlayed"] != 0 else 0,3)

# Given a dataStorageObject with a PlayerGamesDict in which both Totals and Averages are calculated, this calculates
# extra player-specific values such as Three Point %, FG %, etc
def calculateExtraPlayerValues(dataStorageObject):
    for playerStats in dataStorageObject.stats["Players"].values():
        playerStats["Other"] = {}
        playerStats["Other"]["InsidePercentage"] = round(playerStats["Totals"]["InsidesMade"] / playerStats["Totals"]["InsidesAttempted"],3) if playerStats["Totals"]["InsidesAttempted"] != 0 else 0
        playerStats["Other"]["ThreePercentage"] = round(playerStats["Totals"]["ThreesMade"] / playerStats["Totals"]["ThreesAttempted"],3) if playerStats["Totals"]["ThreesAttempted"] != 0 else 0
        playerStats["Other"]["ReboundBias"] = round(playerStats["Averages"]["OffensiveRebounds"] - playerStats["Averages"]["DefensiveRebounds"],3)
        playerStats["Other"]["AssistWorth"] = round(playerStats["Averages"]["PointsPerAssist"] / playerStats["Averages"]["AssistCount"],3) if playerStats["Averages"]["AssistCount"] != 0 else 0





# This function calculates the amount of games where the team with the most of the stat "statName" won, and
# how many that team lost. If multiple stats are provided, it calculates based on a total of all supplied stats.
def calculateStatGameImportance(dataStorageObject, statName : (str,list)):
    if(type(statName) is not list):
        statName = [statName]

    returnDict = {"Win" : 0, "Loss" : 0, "Tie" : 0}
    for gameID,gameInfo in dataStorageObject.stats["Raw"].items():
        runningCounterBallerz = 0
        runningCounterRingers = 0
        for slotID,slotInfo in gameInfo["PlayerSlots"].items():
            if(slotInfo["IsActive"]):
                if(slotID <= 5):
                    for entry in statName:
                        runningCounterBallerz += slotInfo[entry]
                else:
                    for entry in statName:
                        runningCounterRingers += slotInfo[entry]

        ballerzWon = gameInfo["BallerzScore"] > gameInfo["RingersScore"]

        if(runningCounterBallerz > runningCounterRingers):
            if(ballerzWon):
                returnDict["Win"] += 1
            else:
                returnDict["Loss"] += 1
        elif(runningCounterBallerz < runningCounterRingers):
            if(ballerzWon):
                returnDict["Loss"] += 1
            else:
                returnDict["Win"] += 1
        else:
            returnDict["Tie"] += 1



    return returnDict






