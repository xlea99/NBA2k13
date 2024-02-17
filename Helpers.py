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

# This method adds a Player from the Players.db to a specific Roster CSV set.
def addPlayerToRoster(rosterName,playerObject,dataStorageObject = None):
    if(dataStorageObject is None):
        dataStorageObject = DataStorage.DataStorage()
    newRosterID = dataStorageObject.csv_FindFirstUnusedRosterID(rosterName)
    dataStorageObject.csv_UpdatePlayer(rosterName,newRosterID,playerObject)

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

# =========================================================================================
# ====================================MISCELLANEOUS========================================
# =========================================================================================


d = DataStorage.DataStorage(playersPathOverride=f"{b.paths.databases}\\PlayersTest.db")
fuckeryRoster = "PremierFuckery"
#for i in range(100):
#    d.csv_UpdatePlayer(rosterName=fuckeryRoster,rosterID=i)
#for i in range(291,355):
#    addPlayerObjectToRoster(rosterName=fuckeryRoster,playerObject=d.players[i],dataStorageObject=d)
#d.csv_ExportCSVs(rosterName=fuckeryRoster)

importRosterData(rosterName=fuckeryRoster,dataStorageObject=d)
d.updatePlayerCAPInfoFromRoster(rosterName=fuckeryRoster,spriteID=297)
d.playersDB_UploadPlayers()

for i in range(5):
    addPlayerToRoster(rosterName=fuckeryRoster,playerObject=d.players[297],dataStorageObject=d)
exportRosterData(rosterName=fuckeryRoster,dataStorageObject=d)

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