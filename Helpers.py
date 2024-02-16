import BaseFunctions as b
import DataStorage
import RedMC
import StatsRipper
import time
import random
import Factions
import Player

# =========================================================================================
# ==============================INTERNAL DATA MANAGEMENT===================================
# =========================================================================================

# Given a spriteID, this method simply returns a Player's full name.
def getFullPlayerName(spriteID,dataStorageObject=None):
    if(dataStorageObject is not None):
        d = dataStorageObject
    else:
        d = DataStorage.DataStorage()

    fullNameArray = d.playersDB_ReadElement(spriteID,["First_Name","Last_Name"])
    return f"{fullNameArray[0]} {fullNameArray[1]}"

# TODO THIS FUNCTION NEEDNT EXIST, I DONT THINK. BUH BUYE BITHC
# This method adds a Player from the Players.db to a specific Roster CSV set.
def addPlayerToRoster(spriteID,rosterName,dataStorageObject = None,saveFile=True):
    if(dataStorageObject is None):
        d = DataStorage.DataStorage()
    else:
        d = dataStorageObject
    playerDict = d.playersDB_GetPlayer(spriteID)
    newRosterID = d.csv_FindFirstUnusedRosterID(rosterName)
    d.csv_UpdatePlayer(rosterName,newRosterID,playerDict)

    if(saveFile):
        d.csv_ExportCSVs(rosterName)

# This method adds a Player from the Players.db to a specific Roster CSV set.
def addPlayerObjectToRoster(rosterName,playerObject,dataStorageObject = None):
    if(dataStorageObject is None):
        dataStorageObject = DataStorage.DataStorage()
    newRosterID = dataStorageObject.csv_FindFirstUnusedRosterID(rosterName)
    dataStorageObject.csv_UpdatePlayer(rosterName,newRosterID,playerObject)

# This method uses a Player object, as defined in Players.py, to add a single new player
# to the Players.xml file.
# TODO AGAIN, THIS JUST WRAPS OTHER FUNCTIONS. BE A MAN.
def savePlayerObjectToPlayersFile(playerObject,dataStorageObject=None,saveFile=True):
    if(dataStorageObject is None):
        d = DataStorage.DataStorage()
    else:
        d = dataStorageObject
    playerDict = playerObject.convertToPlayerDict()
    newSpriteID = d.playersDB_AddBlankPlayer()
    d.playersDB_UpdatePlayer(spriteID=newSpriteID,playerDictionary=playerDict)
    if(saveFile):
        d.playersDB_Execute()
    return newSpriteID

# This simple helper method returns an array of dicts, containing all player names in the Players.xml file and
# their associated spriteIDs. If a roster is specified, it will only pull players which exist on the given
# roster.
def getDictOfPlayerNames(rosterName=None,dataStorageObject=None):
    if (dataStorageObject is None):
        d = DataStorage.DataStorage()
    else:
        d = dataStorageObject


    if(rosterName is None):
        returnDict = {}
        for i in range(d.playersDB_GetPlayerCount()):
            returnDict[i] = getFullPlayerName(i,d)
    else:
        returnDict = {}
        for spriteID in d.csvRosterDict[rosterName]["SpriteIDs"].values():
            if(spriteID >= 0):
                returnDict[spriteID] = getFullPlayerName(spriteID,d)

    return returnDict

# This method rips all CAP information from a Roster CSV set, to overwrite the Players.db
# with. This method assumes that the roster set is already exported and up to date. Should
# be used after we make changes to Player's faces in game to save them permanently on Players.db.
def updateCAPInfoFromRosterSet(rosterName,spriteID,dataStorageObject=None,saveData=True):
    if(dataStorageObject is None):
        d = DataStorage.DataStorage()
    else:
        d = dataStorageObject

    rosterID = d.csv_GetRosterIDFromSpriteID(rosterName,spriteID)
    rosterPDict = d.csv_GetSinglePlayerDict(rosterName,rosterID)
    playersPDict = d.playersDB_GetPlayer(spriteID)
    finalPDict = playersPDict

    capValues = ["CAP_FaceT",
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
                      "CAP_T_RgtF"]
    gearValues = ["GHeadband",
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
                      "GShsACol3"]
    missingVals = ["Weight",
                   "SkinTone",
                   "Muscles",
                   "EyeColor",
                   "Bodytype",
                   "Clothes",
                   "Number"]
    allCAPVals = capValues + gearValues + missingVals

    for elementName in rosterPDict:
        if(elementName in allCAPVals):
            finalPDict[elementName] = rosterPDict[elementName]

    d.playersDB_UpdatePlayer(spriteID,finalPDict)
    if(saveData):
        d.playersDB_Execute()


# This function simply returns a list of all SpriteIDs associated with a certain archetype. If a
# rosterName is specified, it only returns SpriteIDs that exist on that roster.
#def getListOfArchetypeSpriteIDs()

# =========================================================================================
# ============================RED MC <-> PROGRAM FUNCTIONS=================================
# =========================================================================================

# RedMC -> PROGRAM
# This method imports all CSVs from the given %rosterName%.ROS file into the local program CSV
# data folder and dataStorageObject.
def importRosterData(rosterName,dataStorageObject):
    r = RedMC.RedMC()
    r.openRedMC()
    r.loadRoster(rosterName)
    r.exportCSVs(rosterName)
    r.closeRedMC()
    time.sleep(2)
    dataStorageObject.csv_ImportCSVs(rosterName)
    return r.testIfRedMCClosed()

# PROGRAM -> RedMC
# exportRosterData then exports internal program CSV data into actual CSV files, then exports
# those 4 CSV files into the actual %rosterName%.ROS file using RedMC.
def exportRosterData(rosterName,dataStorageObject):
    dataStorageObject.csv_ExportCSVs(rosterName)
    r = RedMC.RedMC()
    r.openRedMC()
    r.loadRoster(rosterName)
    r.importCSVs(rosterName)
    r.saveRoster()
    r.closeRedMC()
    return r.testIfRedMCClosed()

# PROGRAM (CAP info) -> Players.db
# This method rips all CAP information from a Roster CSV set, to overwrite the Players.db
# with. This method assumes that the roster set is already exported and up to date. Should
# be used after we make changes to Player's faces in game to save them permanently on Players.db.
def saveCAPInfo(rosterName,spriteID,dataStorageObject=None,saveData=True):
    if(dataStorageObject is None):
        d = DataStorage.DataStorage()
    else:
        d = dataStorageObject

    rosterID = d.csv_GetRosterIDFromSpriteID(rosterName,spriteID)
    rosterPlayer = d.csv_ExtractPlayer(rosterName,rosterID)
    playersPlayer = d.playersDB_GetPlayer(spriteID)
    finalPDict = playersPlayer

    capValues = ["CAP_FaceT",
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
                      "CAP_T_RgtF"]
    gearValues = ["GHeadband",
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
                      "GShsACol3"]
    missingVals = ["Weight",
                   "SkinTone",
                   "Muscles",
                   "EyeColor",
                   "Bodytype",
                   "Clothes",
                   "Number"]
    allCAPVals = capValues + gearValues + missingVals

    for elementName in rosterPlayer:
        if(elementName in allCAPVals):
            finalPDict[elementName] = rosterPlayer[elementName]

    d.playersDB_UpdatePlayer(spriteID,finalPDict)
    if(saveData):
        d.playersDB_Execute()

# =========================================================================================
# ====================================MISCELLANEOUS========================================
# =========================================================================================


'''
# Sets the Jerseys to their defaults for the given roster.

thisRoster = "Premier"
d = DataStorage.DataStorage()
importRosterData(rosterName=thisRoster,dataStorageObject=d)
d.rosters[thisRoster]["JerseyConfig"]["BallerzSlayer"] = "TimberwolvesAlternate"
d.rosters[thisRoster]["JerseyConfig"]["BallerzVigilante"] = "RaptorsMilitaryNight"
d.rosters[thisRoster]["JerseyConfig"]["BallerzMedic"] = "RocketsClassicAwayI"
d.rosters[thisRoster]["JerseyConfig"]["BallerzGuardian"] = "WizardsClassicAwayIVAlt"
d.rosters[thisRoster]["JerseyConfig"]["BallerzEngineer"] = "WarriorsClassicAwayIVAlt"
d.rosters[thisRoster]["JerseyConfig"]["BallerzDirector"] = "KingsClassicAwayV"
d.rosters[thisRoster]["JerseyConfig"]["RingersSlayer"] = "TrailblazersClassicAwayI"
d.rosters[thisRoster]["JerseyConfig"]["RingersVigilante"] = "CelticsAlternate"
d.rosters[thisRoster]["JerseyConfig"]["RingersMedic"] = "HeatAlternate"
d.rosters[thisRoster]["JerseyConfig"]["RingersGuardian"] = "WizardsClassicHomeIII"
d.rosters[thisRoster]["JerseyConfig"]["RingersEngineer"] = "SunsLatinNights"
d.rosters[thisRoster]["JerseyConfig"]["RingersDirector"] = "HornetsClassicAwayIAlt"
d.csv_UpdateAllJerseys(rosterName=thisRoster)
exportRosterData(rosterName=thisRoster,dataStorageObject=d)
'''


'''
d = DataStorage.DataStorage()
importRosterData(rosterName="Premier",dataStorageObject=d)

for i in range(291,355):
    thisPlayer = d.playersDB_DownloadPlayer(spriteID=i)
    addPlayerObjectToRoster(playerObject=thisPlayer,rosterName="Premier",dataStorageObject=d)
    print(f"Added '{thisPlayer['First_Name']} {thisPlayer['Last_Name']}' to roster.")
exportRosterData(rosterName="Premier",dataStorageObject=d)
'''


'''
# Code for generating faction test rosters. Just copy a template named "FactionTest" to 2k
# directory beforehand

d = DataStorage.DataStorage()
importRosterData(rosterName="FactionTest",dataStorageObject=d)

newPlayers = []
for i in range(200):
    newPlayer = Player.Player()
    thisFaction = Factions.getRandomFaction()
    newPlayer = Factions.genFaction(thisFaction,newPlayer)
    newPlayer.genArchetype()
    newPlayer.genRarity()
    newPlayer.genAttributes()
    newPlayer.genAnimations()
    newPlayer.genTendencies()
    newPlayer.genHotspots()
    newPlayer.genHeight()
    newPlayer.genPlayStyle()
    newPlayer.genPlayTypes()
    #newPlayer.generateArtifact()
    newPlayer.genMisc()
    print(f"{newPlayer['First_Name']} {newPlayer['Last_Name']} | {newPlayer['Faction']}")
    newPlayers.append(newPlayer)

for newPlayer in newPlayers:
    newPlayer["SpriteID"] = d.playersDB_UploadPlayer(player=newPlayer,newPlayer=True)
    addPlayerObjectToRoster("FactionTest",newPlayer,dataStorageObject=d)

d.csv_ExportCSVs("FactionTest")
exportRosterData(rosterName="FactionTest",dataStorageObject=d)
'''


'''
d = DataStorage.DataStorage()
exportRedMCCSVs(rosterName="HeightsTest",dataStorageObject=d)


for i in range(5):
    p = Player.Player()
    p.genArchetype()
    p.genRarity()
    p.genAttributes()
    p.genTendencies()
    p.genPlayTypes()
    p.genPlayStyle()
    p.genHotspots()
    p.genAnimations()
    p.genMisc()
    p["Height"] = 66
    p["First_Name"] = "Jungle"
    p["Last_Name"] = "Fucker"
    p["SpriteID"] = 1612

    newRosterID = d.csv_FindFirstUnusedRosterID(rosterName="HeightsTest")
    d.csv_UpdatePlayer(rosterName="HeightsTest",rosterID=newRosterID,player=p)

d.csv_ExportCSVs(rosterName="HeightsTest")
importRedMCCSVs(rosterName="HeightsTest")
'''