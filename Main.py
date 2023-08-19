import BaseFunctions as b
import DataStorage
import GUI
import GUINew

# 1. Create a player (or players) in the GUI. Player is now stored in Players.xml, with a blank face.
#    Player is also stored in Premier Roster.xml, and exported as CSV.
# 2. GUI now shows one pending outgoing change to the Premier Roster (or however many players were created). To save these changes,
#    you click on the "save all Roster changes" button. This opens and automatically imports the processed CSVs into RedMC.
#    while there are outgoing changes pending, 2k can not be opened.
# 3. Open 2k, play with the players, move around teams, change faces, whatever the fuck you want to do. Each time you load a Roster
#    in 2k, it flags that roster as "potentially out of date", meaning the program would like you to re-export the Roster's CSVs from
#    RedMC to ensure up-to-date files. This can be overridden, if the user is POSITIVE no changes were made while player 2k. Either way,
#    while there is a Roster flagged as potentially out of date, actions can not be taken on that roster until it is either overridden
#    or reexported.
#
# ALL actions involving RedMC must be 100% automated, so that there is never, ever any confusion on what we're meant to be doing.

print("hi")

myGUI = GUI.GUI()
myGUI.startupScreen()
myGUI.runMainLoop()


#g = GUINew.GUI()
#g.buildHeader()
#g.runMainLoop()

# RUN THIS TO MANUALLY SAVE A GAME
#s = StatsRipper.StatsRipper()
#s.attachTo2K()
#s.ripAllStats()
#d = DataStorage.DataStorage()
#newGameID = d.statsTable_AddBlankGame()
#d.statsTable_Save()
#d.statsTable_UpdateGameStatsFromObject(newGameID, s)
#d.statsTable_Save()


#d = DataStorage.DataStorage()
#d.rosterTable_GenerateNewRosterFile("Wild")
#
#h.exportRedMCCSVs("Wild")
#h.readCSVsFromRedMC("Wild")
#h.generateCSVsFromRosterFile("Wild")
#h.importRedMCCSVs("Wild")

#for i in range(327):
#    print("ADDING PLAYER: " + str(i))
#    h.addPlayerToRoster(spriteID=i,rosterName="Wild",dataStorageObject=None,saveFile=True,assignToTeam=False)


'''
d = DataStorage.DataStorage()
h.exportRedMCCSVs("Premier")
h.readCSVsFromRedMC("Premier")
for i in range(333,339):
    h.updateCAPInfoFromRosterFile("Premier",i,d,True)
'''



