import csv
import os
from spritopia.players.players import Player
from spritopia.common.logger import log
from spritopia.common.paths import paths
from spritopia.utilities import misc
from spritopia.data_storage import stats_processing
import sqlite3 as sql
from datetime import date
import random
import json

# This dictionary stores relevant values for each possible Jersey that can be selected.
_JERSEYS_PATH = paths["misc"] / "jerseys.json"
with open (_JERSEYS_PATH, "r", encoding="utf-8") as f:
    JERSEY_DICT = json.load(f)

# This class handles all communications with Databases and CSV sets.
class DataStorage:

    # Init method defaults to opening the players, stats, and all roster files. Options exist
    # to manually disable these, as well as manually set the paths to databases.
    def __init__(self, openCSVFiles=True, openPlayers=True, openStats = True,
                 playersPathOverride: str = None, statsPathOverride: str = None):

        if(playersPathOverride is None):
            self.__playersDBPath = paths["saveDBs"] / "Players.db" # Default PlayersDB path
        else:
            self.__playersDBPath = playersPathOverride

        if(statsPathOverride is None):
            self.__statsDBPath = paths["saveDBs"] / "Stats.db" # Default StatsDB path
        else:
            self.__statsDBPath = statsPathOverride

        self.rosters = {}
        self.__csvDBDict = {}
        self.__csvCursorDict = {}
        if (openCSVFiles):
            savedRosters = self.csv_GetSavedRosterList()
            for roster in savedRosters:
                self.csv_ImportCSVs(roster)

        self.players = {}
        self.__playersDB = None
        self.__playersCursor = None
        if (openPlayers):
            self.playersDB_Open()
            self.playersDB_DownloadPlayers()

        self.stats = {}
        self.__statsDB = None
        self.__statsCursor = None
        if(openStats):
            self.statsDB_Open()
            self.statsDB_DownloadRaw()

        log.info("Finished initializing DataStorage object.")

    # region === CSV/Roster Management ===

    # This method simply returns an array of all managed and saved roster directories.
    @staticmethod
    def csv_GetSavedRosterList():
        returnArray = []
        for item in os.listdir(paths["rosterCSVs"]):
            if (os.path.isdir(paths["rosterCSVs"] / item)):
                returnArray.append(item)
        return returnArray

    # This method updates a single RosterID's SpriteID in the RosterVals.db database.
    def __csv_UpdateSpriteID(self, rosterName, rosterID, spriteID):
        query = f'UPDATE SpriteIDs SET SpriteID = {spriteID} WHERE RosterID = {rosterID};'
        self.__csvCursorDict[rosterName].execute(query)
        self.__csvDBDict[rosterName].commit()
    # This method adds a valid height adjustment (between 0.00 and 2.53) for the given RosterID, applies it,
    # stores it in RosterVals.db, and returns True if the Roster isn't yet full. realHeight should be in inches.
    def __csv_AdjustHeight(self, rosterName, rosterID, realHeight):
        if (realHeight == -1):
            query = f"UPDATE HeightMap SET RealHeight = {realHeight}, HeightAdjustment = 0 WHERE RosterID = {rosterID}"
            self.__csvCursorDict[rosterName].execute(query)
            self.__csvDBDict[rosterName].commit()
        else:
            query = f"SELECT HeightAdjustment FROM HeightMap WHERE RealHeight = {realHeight} AND RosterID != {rosterID}"
            self.__csvCursorDict[rosterName].execute(query)
            records = self.__csvCursorDict[rosterName].fetchall()
            allCurrentAdjustments = set(record[0] for record in records)

            validAdjustments = [i for i in range(254) if i not in allCurrentAdjustments]

            if (len(validAdjustments) == 0):
                error = ValueError(f"Out of space to add more players to roster with this height: {realHeight}. Quite sad.")
                log.exception(error)
                raise error
            # Deterministic pick — smallest available adjustment.
            thisAdjustment = validAdjustments[0]

            query = f"UPDATE HeightMap SET RealHeight = {realHeight}, HeightAdjustment = {thisAdjustment} WHERE RosterID = {rosterID}"
            self.__csvCursorDict[rosterName].execute(query)
            self.__csvDBDict[rosterName].commit()

            self.rosters[rosterName]["Players"][rosterID]["Height"] = str(
                round((realHeight * 2.54) + (thisAdjustment * 0.01), 2))
    # This method uses the RosterVals.db database present alongside each exported Roster csv set to generate
    # a dictionary that matches each ID of the Players tab of the rosterName roster to a SpriteID.
    def csv_GenSpriteIDDict(self, rosterName):
        allUsedPlayerIDs = self.csv_FindAllUsedPlayerIDs(rosterName)
        query = f'SELECT SpriteID FROM SpriteIDs WHERE RosterID IN ({str(allUsedPlayerIDs).strip("[]")})'

        self.__csvCursorDict[rosterName].execute(query)
        spriteIDList = self.__csvCursorDict[rosterName].fetchall()

        spriteIDDict = {}
        for i in range(len(allUsedPlayerIDs)):
            spriteIDDict[allUsedPlayerIDs[i]] = spriteIDList[i][0]

        self.rosters[rosterName]["SpriteIDs"] = spriteIDDict
    # This method uses the RosterVals.db database present alongside each exported Roster csv set to generate
    # a dictionary that matches each RosterID with the player's height adjustment.
    def csv_GenHeightAdjustmentDict(self,rosterName):
        allUsedPlayerIDs = self.csv_FindAllUsedPlayerIDs(rosterName)
        query = f'SELECT * FROM HeightMap WHERE RosterID IN ({str(allUsedPlayerIDs).strip("[]")})'

        self.__csvCursorDict[rosterName].execute(query)
        heightAdjustmentRows = self.__csvCursorDict[rosterName].fetchall()

        heightMap = {}
        for row in heightAdjustmentRows:
            heightMap[row[0]] = {"RealHeight" : row[1], "HeightAdjustment" : row[2]}

        self.rosters[rosterName]["HeightMap"] = heightMap
    # This method uses the RosterVals.db database present alongside each exported Roster csv set to generate
    # a dictionary of Jersey config values.
    def csv_GenJerseyConfigDict(self,rosterName):
        query = f'SELECT * FROM JerseyConfig'

        self.__csvCursorDict[rosterName].execute(query)
        jerseyConfigRows = self.__csvCursorDict[rosterName].fetchall()

        jerseyConfig = {}
        for row in jerseyConfigRows:
            jerseyConfig[row[0]] = row[1]

        self.rosters[rosterName]["JerseyConfig"] = jerseyConfig
    # This method simply returns the SpriteID of a player on a roster, given RosterID.
    def csv_GetSpriteIDFromRosterID(self, rosterName, rosterID):
        return self.rosters[rosterName]["SpriteIDs"].get(rosterID,None)
    # This method simply returns the RosterID if a player exists on a roster with given SpriteID.
    def csv_GetRosterIDFromSpriteID(self, rosterName, spriteID):
        for rosterID in self.rosters[rosterName]["SpriteIDs"]:
            if (str(self.rosters[rosterName]["SpriteIDs"][rosterID]) == str(spriteID)):
                return rosterID

    # This helper method loads all aspects of CSV and SpriteID.db information into this local DataStorage
    # object for use.
    def csv_ImportCSVs(self, rosterName):
        # This method looks for the associated rosterName folder in paths rosterCSVs path to read (import) the 4
        # exported CSV files into self.rosters = {}, overwriting whatever was there under
        # rosterName previously.
        def readBaseCSVs():
            def readCSVFileToDict(filePath):
                with open(filePath, "r", encoding="utf16") as f:
                    reader = csv.DictReader(f, delimiter=",")
                    return [row for row in reader]

            self.rosters[rosterName] = {
                "Players": readCSVFileToDict(paths["rosterCSVs"] / f"{rosterName}/Players.csv"),
                "Headshapes": readCSVFileToDict(paths["rosterCSVs"] / f"{rosterName}/Headshapes.csv"),
                "Teams": readCSVFileToDict(paths["rosterCSVs"] / f"{rosterName}/Teams.csv"),
                "Jerseys": readCSVFileToDict(paths["rosterCSVs"] / f"{rosterName}/Jerseys.csv"),
            }
        readBaseCSVs()

        log.debug(f"Read CSV files for roster '{rosterName}'")

        # This simply generates necessary db connection and cursor objects to hook into this rosterName's
        # RosterVals.db data file. If the db doesn't exist for this roster yet, it creates it.
        def genRosterValsDBConnection():
            rosterValsDBPath = paths["rosterCSVs"] / f"{rosterName}/RosterVals.db"
            if (not os.path.exists(rosterValsDBPath)):
                needsTableBuilt = True
            else:
                needsTableBuilt = False
            if (rosterName not in self.__csvDBDict):
                self.__csvDBDict[rosterName] = sql.connect(rosterValsDBPath)
                self.__csvCursorDict[rosterName] = self.__csvDBDict[rosterName].cursor()
                if (needsTableBuilt):
                    spriteIDTableQuery = '''CREATE TABLE "SpriteIDs" ("RosterID" INTEGER UNIQUE, "SpriteID" INTEGER, PRIMARY KEY("RosterID"));'''
                    self.__csvCursorDict[rosterName].execute(spriteIDTableQuery)
                    # Insert 1000 entries with a SpriteID of -1
                    for i in range(1, 1001):
                        self.__csvCursorDict[rosterName].execute(
                            '''INSERT INTO "SpriteIDs" ("RosterID", "SpriteID") VALUES (?, -1);''', (i,))

                    heightMapTableQuery = '''CREATE TABLE "HeightMap" ("RosterID" INTEGER,"RealHeight" INTEGER,"HeightAdjustment" INTEGER,PRIMARY KEY("RosterID"));'''
                    self.__csvCursorDict[rosterName].execute(heightMapTableQuery)
                    for i in range(1, 1001):
                        self.__csvCursorDict[rosterName].execute(
                            '''INSERT INTO "HeightMap" ("RosterID","RealHeight","HeightAdjustment") VALUES (?,-1,0);''',
                            (i,))

                    jerseyConfigTableQuery = '''CREATE TABLE "JerseyConfig" ("JerseyOption" TEXT UNIQUE, "JerseyValue"	TEXT, PRIMARY KEY("JerseyOption"));'''
                    self.__csvCursorDict[rosterName].execute(jerseyConfigTableQuery)
                    jerseyConfigQuery = '''INSERT INTO JerseyConfig (JerseyOption, JerseyValue) VALUES (?,?)'''
                    jerseyConfigOptions = ["BallerzSlayer","BallerzVigilante","BallerzMedic","BallerzGuardian","BallerzEngineer","BallerzDirector","RingersSlayer","RingersVigilante","RingersMedic","RingersGuardian","RingersEngineer","RingersDirector",]
                    for jerseyConfigOption in jerseyConfigOptions:
                        self.__csvCursorDict[rosterName].execute(jerseyConfigQuery,(jerseyConfigOption,"GrizzliesHome"))

                    self.__csvDBDict[rosterName].commit()

        genRosterValsDBConnection()

        self.csv_GenSpriteIDDict(rosterName)
        self.csv_GenHeightAdjustmentDict(rosterName)
        self.csv_GenJerseyConfigDict(rosterName)
        log.debug(f"Imported roster '{rosterName}'")
    # This method turns a CSV dictionary into four files, saves them to the rosterName csv folder for
    # RedMC import, and overwrites any existing files there.
    def csv_ExportCSVs(self, rosterName):
        if (not os.path.exists(paths["rosterCSVs"] / rosterName)):
            os.mkdir(paths["rosterCSVs"] / rosterName)

        # Helper function to write a single CSV file from a csvData set.
        def writeCSVDictToFile(filePath: str, csvData: list):
            with open(filePath, "w", newline="", encoding="UTF-16") as f:
                writer = csv.DictWriter(f, fieldnames=csvData[0].keys(), quoting=csv.QUOTE_NONNUMERIC)
                writer.writeheader()
                writer.writerows(csvData)

        # WriteCSVDictToFile for all 4 relevant files.
        writeCSVDictToFile(filePath=paths["rosterCSVs"] / f"{rosterName}\\Players.csv",
                           csvData=self.rosters[rosterName]["Players"])
        writeCSVDictToFile(filePath=paths["rosterCSVs"] / f"{rosterName}\\Headshapes.csv",
                           csvData=self.rosters[rosterName]["Headshapes"])
        writeCSVDictToFile(filePath=paths["rosterCSVs"] / f"{rosterName}\\Teams.csv",
                           csvData=self.rosters[rosterName]["Teams"])
        writeCSVDictToFile(filePath=paths["rosterCSVs"] / f"{rosterName}\\Jerseys.csv",
                           csvData=self.rosters[rosterName]["Jerseys"])
        log.debug(f"Exported CSV files for roster '{rosterName}'")

    # This method overwrites the given RosterID in the Players tab of rosterName with the given
    # Player object. If no Player is given, the player will instead be 'removed', which
    # essentially means the RosterID is set to inactive and their name is reset.
    def csv_UpdatePlayer(self, rosterName, rosterID, player: Player = None):
        rosterID = int(rosterID)
        if(rosterID > 999):
            error = ValueError(f"ERROR: RosterID must be <= 999, given value is {rosterID}")
            log.exception(error)
            raise error
        if (player is None):
            self.rosters[rosterName]["Players"][rosterID]["IsRegNBA"] = "0"
            self.rosters[rosterName]["Players"][rosterID]["First_Name"] = f"*{misc.alphaBase26(decimalNumber=rosterID,maxPlaces=15)}"
            self.rosters[rosterName]["Players"][rosterID]["Last_Name"] = f"*{misc.alphaBase26(decimalNumber=-1 * rosterID - 1,maxPlaces=15)}"
            self.rosters[rosterName]["Players"][rosterID]["NickName"] = "**************"
            self.__csv_UpdateSpriteID(rosterName, rosterID, -1)
            self.csv_GenSpriteIDDict(rosterName)
            self.__csv_AdjustHeight(rosterName=rosterName, rosterID=rosterID, realHeight=-1)
            self.csv_GenHeightAdjustmentDict(rosterName)
            self.csv_GenJerseyConfigDict(rosterName)
            log.debug(f"Updated roster '{rosterName}' rosterID {rosterID} with blank player.")
        else:
            player["HS_ID"] = rosterID
            player["PortrID"] = str(rosterID + 9999)
            player["NickName"] = ""
            player["ASA_ID"] = "0"
            # Check if this player is not a normal archetype
            if (player["Archetype"] is None):
                player["TeamID1"] = "7"
                player["TeamID2"] = "7"

            # Update all Players tab values
            for key in self.rosters[rosterName]["Players"][0].keys():
                if (key == "Height"):  # Skip height for now, as we need to set it specially later
                    finalVal = "0"
                elif (key in ["ID"] or key == ""):  # Skip bad keys
                    continue
                else:
                    finalVal = str(player[key])
                self.rosters[rosterName]["Players"][rosterID][key] = finalVal

            # Update all Headshapes tab values
            for key in self.rosters[rosterName]["Headshapes"][0].keys():
                if (key in ["HS_ID", "ID"] or key == ""):
                    continue
                else:
                    self.rosters[rosterName]["Headshapes"][rosterID][key] = str(player[key])

            # Final clean up, adjusting height properly and updating SpriteID db
            self.__csv_AdjustHeight(rosterName=rosterName, rosterID=rosterID, realHeight=player["HeightIn"])
            self.__csv_UpdateSpriteID(rosterName, rosterID, player["SpriteID"])
            self.csv_GenSpriteIDDict(rosterName)
            self.csv_GenHeightAdjustmentDict(rosterName)
            self.csv_GenJerseyConfigDict(rosterName)
            log.debug(f"Updated roster '{rosterName}' rosterID {rosterID} with new player: {player}")
    # This method uses exported CSVs (specifically, headshapes and players csvs) to generate a Player object.
    # Assumes rosterName CSVs are already exported and up to date. It uses rosterID to target a single player.
    def csv_ExtractPlayer(self, rosterName, rosterID):
        player = Player()
        for key, value in self.rosters[rosterName]['Players'][rosterID].items():
            if (key not in ["ID", "HS_ID", "Height"] and key != ""):
                player[key] = value

        # True height needs to be extracted from RosterVals.db
        query = f"SELECT RealHeight FROM HeightMap WHERE RosterID = {rosterID}"
        self.__csvCursorDict[rosterName].execute(query)
        realHeight = self.__csvCursorDict[rosterName].fetchone()[0]
        player["Height"] = realHeight

        # Grab HS_ID for future use
        HS_ID = int(self.rosters[rosterName]["Players"][rosterID]["HS_ID"])

        for key, value in self.rosters[rosterName]['Headshapes'][HS_ID].items():
            if (key != "HS_ID"):
                player[key] = value
        return player

    # This method simply returns the first unused RosterID on the "Players" tab of a CSV dict
    # TODO Max rosterID error handling
    def csv_FindFirstUnusedRosterID(self, rosterName):
        for singlePlayer in self.rosters[rosterName]["Players"][1:]:
            if (singlePlayer["IsRegNBA"] == "1"):
                continue
            else:
                log.debug(f"Found first unused RosterID: {singlePlayer['ID']}")
                return singlePlayer["ID"]
        error = ValueError(f"No unused RosterIDs present on roster '{rosterName}'")
        log.exception(error)
        raise error
    # This method simply returns a list of all used RosterIDs on the "Players" tab of a CSV dict
    def csv_FindAllUsedPlayerIDs(self, rosterName):
        returnList = []
        for singlePlayer in self.rosters[rosterName]["Players"][1:]:
            if (singlePlayer["IsRegNBA"] == "1"):
                returnList.append(int(singlePlayer["ID"]))
        log.debug(f"Found {len(returnList)} used RosterIDs in roster '{rosterName}'")
        return returnList
    # This method uses the HeightMap table of RosterVals.db to determine, given a list of SpriteIDs,
    # the mapped Ball Handling IDs for that team.
    def csv_FindBallHandlingMap(self, rosterName, rosterIDs: list):
        query = f"SELECT * FROM HeightMap WHERE RosterID IN {tuple(rosterIDs)} ORDER BY RealHeight DESC,HeightAdjustment DESC"
        self.__csvCursorDict[rosterName].execute(query)
        results = self.__csvCursorDict[rosterName].fetchall()

        resultList = []
        for row in results:
            resultList.append(row[0])
        return resultList

    # This function updates the given rosterName with Jersey information as defined in this roster's
    # JerseyConfig.
    def csv_UpdateAllJerseys(self, rosterName):
        # This dict stores the constant values we will be editing, based on what config value
        # we're updating.
        translationDict = {"BallerzSlayer": 61,
                           "BallerzVigilante": 74,
                           "BallerzMedic": 82,
                           "BallerzGuardian": 91,
                           "BallerzEngineer": 100,
                           "BallerzDirector": 116,
                           "RingersSlayer": 60,
                           "RingersVigilante": 73,
                           "RingersMedic": 81,
                           "RingersGuardian": 90,
                           "RingersEngineer": 99,
                           "RingersDirector": 115}

        for configVal, jerseyPosition in translationDict.items():
            thisJerseyVal = self.rosters[rosterName]["JerseyConfig"][configVal]
            jerseyContent = JERSEY_DICT[thisJerseyVal]

            # Now we loop through each value in the Jerseys tab of RedMC.
            counter = 0

            for elementName in jerseyContent.keys():
                self.rosters[rosterName]["Jerseys"][jerseyPosition][elementName] = jerseyContent[elementName]
                counter += 1

        self.csv_ExportCSVs(rosterName)

        # Finally, we ensure that the Jersey configurations are now saved in the actually RosterVals.db.
        updateJerseyConfigQuery = "UPDATE JerseyConfig SET JerseyValue = ? WHERE JerseyOption = ?"
        for jerseyOption,jerseyValue in self.rosters[rosterName]["JerseyConfig"].items():
            self.__csvCursorDict[rosterName].execute(updateJerseyConfigQuery,(jerseyValue,jerseyOption))
        self.__csvDBDict[rosterName].commit()

        log.info("Updated all Jersey information")

    # endregion === CSV/Roster Management ===

    # region === Players Table Management ===

    # Simple open function forms connection to Players.db
    def playersDB_Open(self):
        self.__playersDB = sql.connect(self.__playersDBPath)
        self.__playersDB.row_factory = sql.Row
        self.__playersCursor = self.__playersDB.cursor()
        log.debug(f"Opened PlayerDB connection with '{self.__playersDBPath}'")

    # This method simply returns the count of Players currently in the players table.
    def playersDB_GetPlayerCount(self):
        countQuery = "SELECT COUNT(*) FROM Players;"
        self.__playersCursor.execute(countQuery)
        rowCount = self.__playersCursor.fetchone()[0]
        log.debug(f"Counted {rowCount} players in player table")
        return rowCount
    # This function simply returns the first unused SpriteID from the players table.
    def playersDB_GetFirstUnusedSpriteID(self):
        if(self.playersDB_GetPlayerCount() == 0):
            log.debug("Found first unused SpriteID to be 0, since there are currently no players in database.")
            return 0
        else:
            spriteQuery = "SELECT MAX(SpriteID) FROM Players;"
            self.__playersCursor.execute(spriteQuery)
            maxSpriteID = self.__playersCursor.fetchone()[0]
            log.debug(f"Found first unused SpriteID to be {maxSpriteID + 1}")
            return maxSpriteID + 1

    # This method downloads the full Players.db into this object's self.players member.
    def playersDB_DownloadPlayers(self):
        query = "SELECT * FROM Players;"
        self.__playersCursor.execute(query)
        results = self.__playersCursor.fetchall()

        allPlayers = {}
        for row in results:
            thisPlayer = Player()
            thisPlayer["SpriteID"] = row["SpriteID"]
            for key in thisPlayer.all_keys:
                thisPlayer[key] = row[key]
            if(row["PMods"] is not None):
                thisPlayer.pmods = json.loads(row["PMods"])
            allPlayers[thisPlayer["SpriteID"]] = thisPlayer

        self.players = allPlayers
        log.debug(f"Downloaded full players DB from '{self.__playersDBPath}'")
    # This method uploads any changed Players in the self.players dict to the Players.db file.
    # It also handles insertion of new Players as well as SpriteID assignment.
    def playersDB_UploadPlayers(self):
        nextNewSpriteID = self.playersDB_GetFirstUnusedSpriteID()

        pendingQueries = []
        for spriteID,thisPlayer in self.players.items():
            # We only want to update/insert this Player if its marked as updated.
            if(thisPlayer.hasPendingUpdates):
                # Declare initial values for queries/value tuple
                columnNameQuery = "INSERT OR REPLACE INTO Players ("
                valuesQuery = "VALUES ("
                values = []

                # First we build the info part of the query
                for key in thisPlayer.all_keys:
                    columnNameQuery += f"{key}, "
                    valuesQuery += "?, "
                    if (key == "Archetype"):
                        finalVal = thisPlayer["Archetype_Name"]
                    else:
                        finalVal = thisPlayer[key]
                    values.append(finalVal)
                # We also handle serializing potential PMods for this Player.
                columnNameQuery += "PMods, "
                valuesQuery += "?, "
                if(len(thisPlayer.pmods) > 0):
                    values.append(json.dumps(thisPlayer.pmods))
                else:
                    values.append(None)
                # Now, we append the SpriteID to actually replace/insert into the
                # correct SpriteID.
                columnNameQuery += "SpriteID)"
                valuesQuery += "?)"
                # A negative SpriteID means this Player object hasn't yet been assigned
                # an actual SpriteID, and needs one.
                if(spriteID < 0):
                    thisPlayer["SpriteID"] = nextNewSpriteID
                    values.append(nextNewSpriteID)
                    nextNewSpriteID += 1
                else:
                    values.append(spriteID)
                # Now we append the actual query for eventual execution.
                pendingQueries.append((f"{columnNameQuery} {valuesQuery}",values))

                # We finally mark this Player object as no longer having pending updates.
                thisPlayer.hasPendingUpdates = False

        for query in pendingQueries:
            self.__playersCursor.execute(query[0], query[1])
        self.__playersDB.commit()
        log.info(f"Uploaded full Players DB to '{self.__playersDBPath}'")

    # Helper method for adding a new player to the self.players dict. To save this player,
    # UploadPlayers MUST BE RUN or the player will be lost after program closes.
    def playersDB_AddPlayer(self, player : Player):
        tempSpriteID = min(self.players.keys()) - 1 if len(self.players.keys()) > 0 else -1
        player["SpriteID"] = tempSpriteID
        self.players[tempSpriteID] = player
        log.info(f"Added '{player}' to players")

    # endregion === Players Table Management ===

    # region === Stats Table Management ===

    # Simply opens a single, maintained connection with the Stats.db database.
    def statsDB_Open(self):
        self.__statsDB = sql.connect(self.__statsDBPath)
        self.__statsDB.row_factory = sql.Row
        self.__statsCursor = self.__statsDB.cursor()
        log.debug(f"Opened StatsDB connection with '{self.__playersDBPath}'")

    # Downloads the full Stats database into the stats member of this object.
    def statsDB_DownloadRaw(self):
        # Fetch all games
        self.__statsCursor.execute("SELECT * FROM Games")
        games = self.__statsCursor.fetchall()

        gamesDict = {}
        for game in games:
            gameId = game['GameID']
            gameDict = dict(game)

            # Fetch player slots for this game
            self.__statsCursor.execute("SELECT * FROM PlayerSlots WHERE GameID = ?", (gameId,))
            playerSlots = self.__statsCursor.fetchall()

            gameDict["DataState"] = "Committed"
            gameDict["PlayerSlots"] = {}
            for playerSlot in playerSlots:
                playerSlotDict = dict(playerSlot)
                playerSlotDict["DataState"] = "Committed"
                slotID = playerSlotDict["PlayerSlot"]
                gameDict["PlayerSlots"][slotID] = playerSlotDict

            # Add this game's dictionary to the main dictionary
            gamesDict[gameId] = gameDict

        self.stats["Raw"] = gamesDict
        log.debug(f"Downloaded full StatsDB from '{self.__statsDBPath}'")
    # Uploads all changes made to the Stats dict to the actual stats database.
    def statsDB_UploadRaw(self):
        updateQueries = []
        insertQueries = []
        # Iterate through each game in the dictionary
        for gameId, gameInfo in self.stats["Raw"].items():
            # Check if the game is marked as updated.
            if(gameInfo["DataState"] == "Updated"):
                # Prepare an UPDATE statement for the Games table
                updateGameQuery = """
                    UPDATE Games SET
                    LoadedRoster = ?,
                    Mode = ?,
                    PlayDate = ?,
                    GameDuration = ?,
                    BallerzScore = ?,
                    RingersScore = ?,
                    ExtraValue1 = ?, ExtraValue2 = ?, ExtraValue3 = ?,
                    ExtraValue4 = ?, ExtraValue5 = ?, ExtraValue6 = ?,
                    ExtraValue7 = ?, ExtraValue8 = ?, ExtraValue9 = ?,
                    ExtraValue10 = ?
                    WHERE GameID = ?
                """
                gameVals = (
                    gameInfo["LoadedRoster"],
                    gameInfo["Mode"],
                    gameInfo["PlayDate"],
                    gameInfo["GameDuration"],
                    gameInfo["BallerzScore"],
                    gameInfo["RingersScore"],
                    gameInfo["ExtraValue1"],
                    gameInfo["ExtraValue2"],
                    gameInfo["ExtraValue3"],
                    gameInfo["ExtraValue4"],
                    gameInfo["ExtraValue5"],
                    gameInfo["ExtraValue6"],
                    gameInfo["ExtraValue7"],
                    gameInfo["ExtraValue8"],
                    gameInfo["ExtraValue9"],
                    gameInfo["ExtraValue10"],
                    gameId
                )
                updateQueries.append((updateGameQuery,gameVals))
            # Check if the game is marked as new.
            elif(gameInfo["DataState"] == "New"):
                # Prepare an INSERT statement for the Games table
                insertGameQuery = """
                    INSERT INTO Games (
                        GameID, LoadedRoster, Mode, PlayDate, GameDuration, BallerzScore, RingersScore,
                        ExtraValue1, ExtraValue2, ExtraValue3, ExtraValue4, ExtraValue5,
                        ExtraValue6, ExtraValue7, ExtraValue8, ExtraValue9, ExtraValue10
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """
                gameVals = (
                    gameId,
                    gameInfo["LoadedRoster"],
                    gameInfo["Mode"],
                    gameInfo["PlayDate"],
                    gameInfo["GameDuration"],
                    gameInfo["BallerzScore"],
                    gameInfo["RingersScore"],
                    gameInfo["ExtraValue1"],
                    gameInfo["ExtraValue2"],
                    gameInfo["ExtraValue3"],
                    gameInfo["ExtraValue4"],
                    gameInfo["ExtraValue5"],
                    gameInfo["ExtraValue6"],
                    gameInfo["ExtraValue7"],
                    gameInfo["ExtraValue8"],
                    gameInfo["ExtraValue9"],
                    gameInfo["ExtraValue10"]
                )
                insertQueries.append((insertGameQuery, gameVals))

            # Iterate through each player slot in the game
            for slotId, slotInfo in gameInfo["PlayerSlots"].items():
                # Check if the player slot is marked as "Dirty"
                if(gameInfo["DataState"] == "Updated"):
                    # Prepare an UPDATE statement for the PlayerSlots table
                    updateSlotQuery = """
                        UPDATE PlayerSlots SET
                        IsActive = ?, SpriteID = ?, RosterID = ?, Points = ?,
                        DefensiveRebounds = ?, OffensiveRebounds = ?, PointsPerAssist = ?,
                        AssistCount = ?, Steals = ?, Blocks = ?, Turnovers = ?,
                        InsidesMade = ?, InsidesAttempted = ?, ThreesMade = ?,
                        ThreesAttempted = ?, Fouls = ?, Dunks = ?, Layups = ?,
                        Unknown1 = ?, Unknown2 = ?, BallHolding_InPlay = ?, BallHolding_OutOfPlay = ?
                        WHERE GameID = ? AND PlayerSlot = ?
                    """
                    slotVals = (
                        slotInfo["IsActive"],
                        slotInfo["SpriteID"],
                        slotInfo["RosterID"],
                        slotInfo["Points"],
                        slotInfo["DefensiveRebounds"],
                        slotInfo["OffensiveRebounds"],
                        slotInfo["PointsPerAssist"],
                        slotInfo["AssistCount"],
                        slotInfo["Steals"],
                        slotInfo["Blocks"],
                        slotInfo["Turnovers"],
                        slotInfo["InsidesMade"],
                        slotInfo["InsidesAttempted"],
                        slotInfo["ThreesMade"],
                        slotInfo["ThreesAttempted"],
                        slotInfo["Fouls"],
                        slotInfo["Dunks"],
                        slotInfo["Layups"],
                        slotInfo["Unknown1"],
                        slotInfo["Unknown2"],
                        slotInfo["BallHolding_InPlay"],
                        slotInfo["BallHolding_OutOfPlay"],
                        gameId,
                        slotId
                    )
                    updateQueries.append((updateSlotQuery,slotVals))
                elif(gameInfo["DataState"] == "New"):
                    # Prepare an INSERT statement for the PlayerSlots table
                    insertSlotQuery = """
                        INSERT INTO PlayerSlots (
                            GameID, PlayerSlot, IsActive, SpriteID, RosterID, Points,
                            DefensiveRebounds, OffensiveRebounds, PointsPerAssist, AssistCount, Steals,
                            Blocks, Turnovers, InsidesMade, InsidesAttempted, ThreesMade,
                            ThreesAttempted, Fouls, Dunks, Layups, Unknown1, Unknown2, BallHolding_InPlay, 
                            BallHolding_OutOfPlay
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """
                    slotVals = (
                        gameId,
                        slotInfo["PlayerSlot"],
                        slotInfo["IsActive"],
                        slotInfo["SpriteID"],
                        slotInfo["RosterID"],
                        slotInfo["Points"],
                        slotInfo["DefensiveRebounds"],
                        slotInfo["OffensiveRebounds"],
                        slotInfo["PointsPerAssist"],
                        slotInfo["AssistCount"],
                        slotInfo["Steals"],
                        slotInfo["Blocks"],
                        slotInfo["Turnovers"],
                        slotInfo["InsidesMade"],
                        slotInfo["InsidesAttempted"],
                        slotInfo["ThreesMade"],
                        slotInfo["ThreesAttempted"],
                        slotInfo["Fouls"],
                        slotInfo["Dunks"],
                        slotInfo["Layups"],
                        slotInfo["Unknown1"],
                        slotInfo["Unknown2"],
                        slotInfo["BallHolding_InPlay"],
                        slotInfo["BallHolding_OutOfPlay"]
                    )
                    insertQueries.append((insertSlotQuery, slotVals))

        # Finally, we actually execute all statements.
        for query, vals in updateQueries:
            self.__statsCursor.execute(query, vals)
        for query, vals in insertQueries:
            self.__statsCursor.execute(query, vals)

        # Commit the changes
        self.__statsDB.commit()
        log.info(f"Uploaded StatsDB to '{self.__statsDBPath}'")

        self.statsDB_DownloadRaw()

    # This method uses a stats object, which is assumed to have a full ripped game in it, and adds it as a new game row
    # to the stats.db. It also returns the GameID of the saved game.
    def statsDB_AddRippedGame(self, statsObject, extraValues=None):
        newGameID = max(self.stats["Raw"].keys()) + 1
        newGame = {"DataState" : "New",
                   "GameID" : newGameID,
                   "LoadedRoster" : statsObject.loadedRoster,
                   "Mode" : statsObject.gameMode,
                   "PlayDate" : date.today().strftime("%Y-%m-%d"),
                   "GameDuration" : None, #TODO
                   "BallerzScore" : statsObject.ballerzScore,
                   "RingersScore" : statsObject.ringersScore}
        if(type(extraValues) is not list): # TODO maybe make these kwargs instead?
            extraValues = []

        for i in range(1,11):
            if(len(extraValues) >= i):
                newGame[f"ExtraValue{i}"] = extraValues[i-1]
            else:
                newGame[f"ExtraValue{i}"] = None


        playerSlots = {}
        for slotName,slotInfo in statsObject.slotStats["slotStats"].items():
            slotId = int(slotName.split("Slot")[1])
            if not slotInfo.get("IsActive"):
                # Inactive slots have only IsActive=0 from the tracker rip. The DB
                # convention (preserved across all 237 historic games) is one row
                # per slot per game, with stat columns NULL on inactive rows.
                playerSlots[slotId] = {
                    "DataState"             : "New",
                    "GameID"                : newGameID,
                    "PlayerSlot"            : slotId,
                    "IsActive"              : 0,
                    "SpriteID"              : None,
                    "RosterID"              : None,
                    "Points"                : None,
                    "DefensiveRebounds"     : None,
                    "OffensiveRebounds"     : None,
                    "PointsPerAssist"       : None,
                    "AssistCount"           : None,
                    "Steals"                : None,
                    "Blocks"                : None,
                    "Turnovers"             : None,
                    "InsidesMade"           : None,
                    "InsidesAttempted"      : None,
                    "ThreesMade"            : None,
                    "ThreesAttempted"       : None,
                    "Fouls"                 : None,
                    "Dunks"                 : None,
                    "Layups"                : None,
                    "Unknown1"              : None,
                    "Unknown2"              : None,
                    "BallHolding_InPlay"    : None,
                    "BallHolding_OutOfPlay" : None,
                }
                continue
            thisPlayerSlot = {"DataState" : "New",
                              "GameID" : newGameID,
                              "PlayerSlot" : slotId,
                              "IsActive" : slotInfo["IsActive"],
                              "SpriteID" : self.csv_GetSpriteIDFromRosterID(statsObject.loadedRoster.split(".ROS")[0], slotInfo.get('RosterID')),
                              "RosterID" : slotInfo['RosterID'],
                              "Points" : slotInfo["Points"],
                              "DefensiveRebounds" : slotInfo["DefensiveRebounds"],
                              "OffensiveRebounds" : slotInfo["OffensiveRebounds"],
                              "PointsPerAssist" : slotInfo["PointsPerAssist"],
                              "AssistCount" : slotInfo["AssistCount"],
                              "Steals" : slotInfo["Steals"],
                              "Blocks" : slotInfo["Blocks"],
                              "Turnovers" : slotInfo["Turnovers"],
                              "InsidesMade" : slotInfo["InsidesMade"],
                              "InsidesAttempted" : slotInfo["InsidesAttempted"],
                              "ThreesMade" : slotInfo["ThreesMade"],
                              "ThreesAttempted" : slotInfo["ThreesAttempted"],
                              "Fouls" : slotInfo["Fouls"],
                              "Dunks" : slotInfo["Dunks"],
                              "Layups" : slotInfo["Layups"],
                              "Unknown1" : slotInfo["Unknown1"],
                              "Unknown2" : slotInfo["Unknown2"],
                              "BallHolding_InPlay" : slotInfo.get("BallHolding_InPlay"),
                              "BallHolding_OutOfPlay" : slotInfo.get("BallHolding_OutOfPlay")
                              }
            playerSlots[slotId] = thisPlayerSlot
        newGame["PlayerSlots"] = playerSlots

        self.stats["Raw"][newGameID] = newGame

        log.debug(f"Added new ripped game ({newGameID}, {newGame['PlayDate']}) to stats dictionary")
        return newGameID

    # endregion === Stats Table Management ===

    #region === Helpers ===

    # This method uses CAP information from a Roster CSV set to overwrite the given Player with.
    # with. This method assumes that the roster set is already exported and up to date. Should
    # be used after we make changes to Player's faces in game to save them permanently on Players.db.
    def updatePlayerCAPInfoFromRoster(self,rosterName,spriteID):
        rosterID = self.csv_GetRosterIDFromSpriteID(rosterName, spriteID)

        capVals = ["CAP_FaceT",
                     "CAP_Hstl",
                     "CAP_Hcol",
                     "CAP_Hlen",
                     "CAP_BStyle",
                     "CAP_Moust",
                     "CAP_Goatee",
                     "CAP_Fhcol",
                     "CAP_Eyebr",
                     "CAP_T_LftN",
                     "CAP_T_LftS",
                     "CAP_T_RgtS",
                     "CAP_T_LftB",
                     "CAP_T_RgtB",
                     "CAP_T_LftF",
                     "CAP_T_RgtF",
                     "GHeadband",
                    "GHdbndLg",
                    "GUndrshrt",
                    "GUndrsCol",
                    "GLeftArm",
                    "GLArmCol",
                    "GLeftElb",
                    "GLElbCol",
                    "GLeftWrst",
                    "GLWrstC1",
                    "GLWrstC2",
                    "GLeftFngr",
                    "GLFngrCol",
                    "GRghtArm",
                    "GRArmCol",
                    "GRghtElb",
                    "GRElbCol",
                    "GRghtWrst",
                    "GRWrstC1",
                    "GRWrstC2",
                    "GRghtFngr",
                    "GRFngrCol",
                    "GPresShrt",
                    "GPrsShCol",
                    "GLeftLeg",
                    "GLLegCol",
                    "GLeftKnee",
                    "GLKneeCol",
                    "GLeftAnkl",
                    "GLAnklCol",
                    "GRghtLeg",
                    "GRLegCol",
                    "GRghtKnee",
                    "GRKneeCol",
                    "GRghtAnkl",
                    "GRAnklCol",
                    "GSockLngh",
                    "GShsBrLck",
                    "GShsBrand",
                    "GShsModel",
                    "GShsUCusC",
                    "GShsTHC1",
                    "GShsTHC2",
                    "GShsTAC1",
                    "GShsTAC2",
                    "GShsHCol1",
                    "GShsHCol2",
                    "GShsHCol3",
                    "GShsACol1",
                    "GShsACol2",
                    "GShsACol3",
                    "Weight",
                    "SkinTone",
                    "Muscles",
                    "EyeColor",
                    "Bodytype",
                    "Clothes",
                    "Number"]
        headshapeVals = ["HParam1",
                         "HParam2",
                         "HdBrwHght",
                         "HdBrwWdth",
                         "HdBrwSlpd",
                         "HdNkThck",
                         "HdNkFat",
                         "HdChnLen",
                         "HdChnWdth",
                         "HdChnProt",
                         "HdJawSqr",
                         "HdJawWdth",
                         "HdChkHght",
                         "HdChkWdth",
                         "HdChkFull",
                         "HdDefinit",
                         "MtULCurve",
                         "MtULThick",
                         "MtULProtr",
                         "MtLLCurve",
                         "MtLLThick",
                         "MtLLProtr",
                         "MtSzHght",
                         "MtSzWdth",
                         "MtCrvCorn",
                         "ErHeight",
                         "ErWidth",
                         "ErEarLobe",
                         "ErTilt",
                         "NsNsHght",
                         "NsNsWdth",
                         "NsNsProtr",
                         "NsBnBridge",
                         "NsBnDefin",
                         "NsBnWdth",
                         "NsTipHght",
                         "NsTipWdth",
                         "NsTipTip",
                         "NsTipBnd",
                         "NsNtHght",
                         "NsNtWdth",
                         "EsFrmOpen",
                         "EsFrmSpac",
                         "EsFrmLwEl",
                         "EsFrmUpEl",
                         "EsPlcHght",
                         "EsPlcWdth",
                         "EsPlcRot",
                         "EsPlcProt",
                         "EsShpOtEl",
                         "EsShpInEl"]

        for capVal in capVals:
            self.players[spriteID][capVal] = self.rosters[rosterName]["Players"][rosterID][capVal]
        for headshapeVal in headshapeVals:
            self.players[spriteID][headshapeVal] = self.rosters[rosterName]["Headshapes"][rosterID][headshapeVal]

        log.debug(f"Updated CAP Info from roster '{rosterName}' for player '{self.players[spriteID]}'")

    #endregion === Helpers ===

# The actual, global DataStorage object used.
d = DataStorage()
stats_processing.generatePlayerGamesDict(d)
stats_processing.calculatePlayerAverages(d)
stats_processing.calculateExtraPlayerValues(d)



'''
# Use this code to test the size of each important part of a dataStorageObject, as
# well as the general size of non-data members.

print(f"Players Size: {b.getMemorySizeOf(d.players)}")
print(f"Stats Size: {b.getMemorySizeOf(d.stats)}")
print(f"Rosters Size: {b.getMemorySizeOf(d.rosters)}")
d.players,d.stats,d.rosters = {},{},{}
print(f"(Other) Size: {b.getMemorySizeOf(d)}")
'''