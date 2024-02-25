from pymem import *
from pymem.process import *
import BaseFunctions as b
import time
import threading



class Tracker:

    #region === Setup and Tools ===

    # Basic init method to initialize member variables.
    def __init__(self,dataStorageObject):
        # Members for actually connecting to 2K
        self.mem = None
        self.module = None

        # Tracking and thread operation.
        self.lock = threading.Lock()
        self.trackingThread = None
        self.trackerRunning = False
        self.tick = 0

        # Built in dataStorageObject.
        self.dataStorage = dataStorageObject

        # Stores the current location of the app.
        self.location = "Disconnected"

        # Values to track games.
        self.gameCount = 0
        self.gameStatus = "OutOfGame"
        self.haveFinalStatsBeenRipped = False
        self.needsCoin = None
        self.coinHasBeenAdded = None
        self.ballHolding = {"InPlay" : {},"OutOfPlay" : {}}
        self.lastTime = 0
        self.canCalcBallHolding = False

        # When a game ends, all ripped stats are temporarily stored here for use elsewhere.
        self.rippedGames = {}

    # This helper method extracts the actual address of an address set by applying offsets
    def getPointerAddress(self,addressSet):
        address = self.mem.read_int(self.module + addressSet[0])
        for offset in addressSet:
            if (offset != addressSet[-1] and offset != addressSet[0]):
                address = self.mem.read_int(address + offset)
        address = address + addressSet[-1]
        return address
    # Extracts the actual value at a given addressSet.
    def getAddressValue(self,addressSet,_type = 'i',stringLength = 50):
        if(addressSet is not None):
            try:
                finalAddress = self.getPointerAddress(addressSet)
                if(_type == 'i'):
                    return self.mem.read_int(finalAddress)
                elif(_type == 's'):
                    returnString = ""
                    for i in range(stringLength):
                        try:
                            returnString += self.mem.read_string(finalAddress + (i*2))
                        except:
                            break
                    returnString = returnString.split(".ROS",1)[0]
                    return returnString + ".ROS"
            except pymem.exception.MemoryReadError:
                return "ERROR"
        else:
            return "None"
    # This method uses a valueType (RosterID, Rebounds, Dunks) to extract a value directly
    # from 2K. It also uses getSecondaryValue for values that have two values baked into them.
    # Read each value for further details.
    def getStatValue(self,slot,valueType,getSecondaryValue = False):
        try:
            if(valueType == "RosterID"):
                return self.getAddressValue(self.boxScoreSlots[slot].get("RosterID")[0])
            elif(valueType == "Steals" or valueType == "Blocks"): # Steals and Blocks are stored on the same value.
                if(getSecondaryValue):
                    return int(self.getAddressValue(self.boxScoreSlots[slot].get("Steals")[0]) / 65536)
                else:
                    return int(self.getAddressValue(self.boxScoreSlots[slot].get("Steals")[0]) % 65536)
            elif(valueType == "Turnovers"):
                if(self.boxScoreSlots[slot].get("Turnovers") == []):
                    return "None"
                else:
                    return int(self.getAddressValue(self.boxScoreSlots[slot].get("Turnovers")[0]) % 65536)
            elif(valueType == "Rebounds"): # Primary is Offensive, secondary is Defensive
                if(getSecondaryValue):
                    return int(self.getAddressValue(self.boxScoreSlots[slot].get("Rebounds")[0]) / 65536)
                else:
                    return int(self.getAddressValue(self.boxScoreSlots[slot].get("Rebounds")[0]) % 65536)
            elif (valueType == "Fouls"):
                if (self.boxScoreSlots[slot].get("Fouls") == []):
                    return "None"
                else:
                    return int(self.getAddressValue(self.boxScoreSlots[slot].get("Fouls")[0]) % 65536)
            elif(valueType == "Assists"):
                if (self.boxScoreSlots[slot].get("Assists") == []):
                    return "None"
                else:
                    if(getSecondaryValue):
                        return int(self.getAddressValue(self.boxScoreSlots[slot].get("Assists")[0]) / 65536)
                    else:
                        return int(self.getAddressValue(self.boxScoreSlots[slot].get("Assists")[0]) % 65536)
            elif(valueType == "Dunks"):
                if (self.boxScoreSlots[slot].get("Dunks") == []):
                    return "None"
                else:
                    if(getSecondaryValue):
                        return int(self.getAddressValue(self.boxScoreSlots[slot].get("Dunks")[0]) / 65536)
                    else:
                        return int(self.getAddressValue(self.boxScoreSlots[slot].get("Dunks")[0]) % 65536)
            elif(valueType == "FG" or valueType == "3PT"): # FG
                if(getSecondaryValue):
                    return int(self.getAddressValue(self.boxScoreSlots[slot].get(valueType)[0]) / 65536)
                else:
                    return int(self.getAddressValue(self.boxScoreSlots[slot].get(valueType)[0]) % 65536)
            else:
                if(len(self.boxScoreSlots[slot].get(valueType)) != 0):
                    return self.getAddressValue(self.boxScoreSlots[slot].get(valueType)[0])
                else:
                    return "None"
        except Exception as e:
            raise e

    #endregion === Setup and Tools ===

    #region === Tracking and Operation ===

    # Method using all Location Tracking methods to find the true location of the app.
    def updateLocationTracking(self):
        with self.lock:
            self.location = self.testCurrentScreen()

    # Method that tracks the current status of the running game.
    def updateGameStatus(self):
        with self.lock:
            if(self.location == "InGame"):
                if (self.gameStatus != "Won"):
                    if(self.testIsGameUnpaused()):
                        if (self.testIfGameIsWon()):
                            self.gameStatus = "Won"
                            #TODO COIN MANAGEMENT CLEAN UP GOES HERE?
                        else:
                            self.gameStatus = "Running"
                    else:
                        self.gameStatus = "Paused"
            else:
                if(self.gameStatus != "OutOfGame"):
                    self.gameCount += 1
                    self.gameStatus = "OutOfGame"
                    self.needsCoin = None
                    self.coinHasBeenAdded = None
                    self.haveFinalStatsBeenRipped = False
                    self.ballHolding = {}
                    self.canCalcBallHolding = False

    # Method that tracks the current ball holder of the game.
    def updateBallHolding(self):
        with self.lock:
            if(self.location == "InGame"):
                # Do this if game is actively running.
                if(self.gameStatus == "Running"):
                    currentIValue = self.getBallHolder()
                    isBallInPlay = self.testIfBallIsInPlay()

                    now = time.perf_counter()
                    timeDif = now - self.lastTime
                    self.lastTime = now

                    if(isBallInPlay):
                        self.ballHolding["InPlay"][currentIValue] = self.ballHolding["InPlay"].get(currentIValue,0.0) + timeDif
                    else:
                        self.ballHolding["OutOfPlay"][currentIValue] = self.ballHolding["OutOfPlay"].get(currentIValue,0.0) + timeDif
                # Do this if game is paused or ended/won.
                else:
                    self.lastTime = time.perf_counter()

    # This update method handles ripping stats from an active game and flagging it as finished or unfinished.
    def updateStatsRip(self):
        with self.lock:
            if(self.location == "InGame" and not self.haveFinalStatsBeenRipped):
                if(self.tick % 20 == 0 or self.gameStatus == "Won"):
                    thisStatRip = self.ripAllStats()
                    # Calculate ball holding times here
                    if(self.canCalcBallHolding or thisStatRip["GameStats"]["LoadedRoster"].split(".ROS")[0] in self.dataStorage.rosters.keys()):
                        ballHoldingTimes = self.convertIValueTimesToRosterIDs(rosterName=thisStatRip["GameStats"]["LoadedRoster"].split(".ROS")[0],
                                                       rippedStats=thisStatRip,iValueTimes=self.ballHolding)
                        if(ballHoldingTimes is not None):
                            self.canCalcBallHolding = True
                            thisStatRip["BallHolding"] = ballHoldingTimes
                    if(self.gameStatus == "Won"):
                        self.haveFinalStatsBeenRipped = True
                        thisStatRip["Final"] = True
                    else:
                        thisStatRip["Final"] = False
                    self.rippedGames[self.gameCount] = thisStatRip

    # Runs the loop to facilitate all 2k app tracking and modification.
    def run(self):
        self.trackerRunning = True
        while self.trackerRunning:
            self.updateLocationTracking()
            self.updateGameStatus()
            self.updateBallHolding()
            self.updateStatsRip()

            self.tick += 1
            time.sleep(0.1)

            print(self.location)
    # This method starts the tracking process.
    def startTracker(self,runAsDaemon = True):
        if(not self.trackerRunning):
            self.trackingThread = threading.Thread(target=self.run)
            if(runAsDaemon):
                self.trackingThread.daemon = True  # This makes sure the thread will not prevent the program from exiting.
            self.trackingThread.start()
    # This method stops the tracking process.
    def stopTracker(self):
        self.trackerRunning = False

    #endregion === Tracking and Operation ===

    #region === Location Tracking ===

    # This method test whether the app is loaded, and if so, connects to it.
    def testAppConnection(self):
        try:
            self.mem = Pymem("nba2k13.exe")
            self.module = module_from_name(self.mem.process_handle, "nba2k13.exe").lpBaseOfDll
            return True
        except pymem.exception.ProcessNotFound:
            self.mem = None
            self.module = None
            return False

    # Tests whether 2k is currently in an active blacktop game.
    inGameAddress = [[0x004E5608, 0x8], [0x00B06D88, 0x60], [0x00B06C30, 0xF0], [0x0001F2C8, 0x120],[0x009AE494, 0x130]]
    def testInGame(self):
        if (self.getAddressValue(self.inGameAddress[0]) == 1):
            return True
        else:
            return False
    # This helper method returns whatever screen it believes the app to be on right now in string form.
    menuScreenAddress = [[0x00BB0A04, 0x1C, 0x318, 0x3C0, 0x818]]
    def testCurrentScreen(self):
        isConnected = True
        if(self.mem is None):
            isConnected = self.testAppConnection()
        if(isConnected):
            menuScreenVal = self.getAddressValue(self.menuScreenAddress[0])
            if(menuScreenVal == "ERROR"):
                self.mem = None
                self.module = None
                return "Disconnected"
            elif (menuScreenVal == 342581834):
                return "Home"
            elif (menuScreenVal == -721351791):
                return "PickUp"
            elif (menuScreenVal == 178469820):
                return "TeamRoster"
            elif (menuScreenVal == 2051352554):
                return "CreatePlayer"
            elif (menuScreenVal == -1227693132):
                return "LoadRoster"
            elif (menuScreenVal == -996019090):
                return "SaveRoster"
            elif (menuScreenVal == 2134613852):
                return "MyPlayerAccount"
            else:
                if (self.testInGame()):
                    return "InGame"
                return "Unknown"
        else:
            return "Disconnected"

    #endregion === Location Tracking ===

    #region === Game Tracking ===

    # This addressSet determines whether the blacktop mode is 1v1 (1), 2v2 (2), 3v3 (3), 4v4 (4), or 5v5 (5)
    blacktopModeAddress = [0x01BFE7C0, 0x634]
    def getBlacktopMode(self):
        return self.getAddressValue(self.blacktopModeAddress)

    # Returns whether an unpaused game is currently playing.
    isGamePlayingAddress = [[0x004FBDE0, 0x4], [0x004FB8D4, 0x388], [0x004FB060, 0x0], [0x004FB7C0, 0x394],[0x004FB8C8, 0x398]]
    def testIsGameUnpaused(self):
        if (self.getAddressValue(self.isGamePlayingAddress[0]) == 1):
            return True
        else:
            return False

    # This addressSet stores the string value of the currently loaded Roster. If it is empty (0), no Roster is
    # currently loaded.
    loadedRosterAddress = [[0x00028F98, 0x8C], [0x000290D8, 0x10C], [0x000292E8, 0x114], [0x00028F7C, 0x118],
                           [0x00640394, 0x374], [0x0063B6F0, 0x774]]
    # This returns either the currently loaded Roster, "NONE" if no Roster is currently loaded, and
    # "UNOPENED" if 2k itself isn't currently open.
    def getActiveRoster(self):
        rosterAddress = str(self.getAddressValue(self.loadedRosterAddress[0], 's'))
        if (rosterAddress == ".ROS"):
            return None
        else:
            return rosterAddress
    # This method rips basic game information from the current blacktop game, returning them as a neatly formatted
    # dictionary. Assumes 2k is open. If slot stats are provided, it also calculates game scores.
    def ripGameStats(self, slotStats: dict = None):
        if (slotStats is not None):
            newGameStats = self.calculateScores(slotStats=slotStats)
        else:
            newGameStats = {}
        newGameStats["GameMode"] = self.getAddressValue(self.blacktopModeAddress)
        newGameStats["LoadedRoster"] = self.getActiveRoster()
        return newGameStats

    # RosterID: Stores only the Player's ID value.
    # Points: Simply stores how many Points the player's earned this game from all sources.
    # Rebounds: Big value is Defensive Rebounds, small value is Offensive Rebounds.
    # Assists: Big value stores points per assist (whether player assisted a 1 or a 3), small value stores Assists
    # Steals: Big value stores Steals, small value stores Blocks.
    # Turnovers: Big value stores UNKNOWN_VALUE_1, small value stores Turnovers.
    # FG: Big value stores all INSIDE SHOTS attempted (not actual FGs), small value stores all INSIDE SHOTS made.
    # 3PT: Big value stores all 3pt shots attempted, small value stores all 3pt shots made.
    # Fouls: Big value stores UNKNOWN_VALUE_2, small value stores Personal Fouls.
    # Dunks: Big value stores Layups, small value stores Dunks.
    # Stores the individual player stats from each player's Slots.
    boxScoreSlots = [
        {  # Slot 1
            "RosterID": [[0x00E24EC4, 0x18, 0x38, 0x1C, 0x550, 0x2FC]],  # RosterID
            "Points": [[0x00D0F60C, 0x18, 0x18, 0x1C, 0x238, 0x174]],  # Points
            "Rebounds": [[0x004A2CEC, 0xDAC], [0x01805168, 0x6B4, 0x1C, 0x5A4, 0x9E0],
                         [0x017AA980, 0xA4, 0x14, 0x10, 0x170, 0x24, 0x620, 0x5C8], [0x0035FAA0, 0xDAC],
                         [0x00322674, 0xDAC]],  # Rebounds
            "Assists": [[0x017AAA70, 0x254, 0x4, 0x64, 0xF0, 0x544, 0x8D8, 0xB38], [0x00DB4A74, 0x3C, 0x354, 0xA00],
                        [0x00D63F84, 0x1C, 0x354, 0xA00], [0x017AA6C8, 0x30, 0x2E0, 0x24, 0x448, 0x4, 0x1FC, 0x720],
                        [0x017AA6C8, 0x4C, 0x10, 0x24, 0x448, 0x4, 0x1FC, 0x720]],  # Assists
            "Steals": [[0x00E28B84, 0x1C, 0x18, 0x5C, 0x5c, 0x18, 0x23C, 0x754],
                       [0x017AA980, 0x184, 0xE0, 0x10, 0x724, 0x1C, 0x600, 0x5E0],
                       [0x017AA6C8, 0x40, 0x24, 0x4C, 0x5E0, 0x4, 0x1FC, 0x718],
                       [0x00DB1164, 0x38, 0x18, 0x38, 0x18, 0x38, 0xA98, 0x788],
                       [0x00D3664C, 0x4, 0x4, 0x1C, 0x18, 0x23C, 0x754]],  # Steals
            "Turnovers": [[0x00DFF21C, 0x78, 0x1C, 0x6B4, 0x1EC], [0x00E1FE54, 0x18, 0x38, 0x1C, 0x6B4, 0x1EC],
                          [0x00E2003C, 0x78, 0x1C, 0x6B4, 0x1EC], [0x00D92328, 0x38C, 0x2E0, 0x1C, 0x23C, 0x760],
                          [0x00E56CB8, 0x18, 0x27C, 0x1DC, 0x724]],  # Turnovers
            "FG": [[0x00E28B3C, 0x5F8, 0x57C, 0x524, 0x1BC, 0x600], [0x00E4EDE4, 0x4E8, 0x2A8, 0x73C, 0x1DC, 0x4F8],
                   [0x00D94A84, 0x78, 0x428, 0x798, 0x23C, 0x534], [0x00D2E7D4, 0x2D8, 0xE8, 0x114, 0x1C0, 0x62C],
                   [0x00DF26E4, 0x6D4, 0x6C, 0x57C, 0x3CC, 0x56C]],  # FG
            "3PT": [[0x00DFB8FC, 0x7A0, 0x18, 0x58, 0x248, 0x180], [0x00D9623C, 0x710, 0x464, 0x360, 0x25C, 0x538],
                    [0x00D3666C, 0x2F8, 0x394, 0x200, 0x19C, 0x604],
                    [0x00D3402C, 0x3F4, 0x264, 0x1E0, 0x3CC, 0x570],
                    [0x00E0A5CC, 0x218, 0x7C, 0x340, 0x7F4, 0x56C]],  # 3PT
            "Fouls": [[0x00E2C43C, 0x5F4, 0x4AC, 0x200, 0x638, 0x6A4]],
            "Dunks": [[0x00DB9FFC, 0x4, 0x44, 0x3C, 0x7A8, 0x6EC], [0x00DB9FF4, 0x44, 0x3C, 0x7A8, 0x6EC],
                      [0x00E203AC, 0x38, 0x7F4, 0x590], [0x00E203AC, 0x38, 0x1C, 0x7D4, 0x590],
                      [0x00E18654, 0x18, 0x38, 0x1C, 0x7D4, 0x590]
                      ]
        },
        {  # Slot 2
            "RosterID": [[0x00DEFD54, 0x1C, 0x2A0, 0x18, 0x618, 0x4F4]],  # RosterID
            "Points": [[0x0138DE58, 0x28, 0x124, 0x294, 0x8]],  # Points
            "Rebounds": [[0x017AA6C8, 0x50, 0x20, 0x24, 0x8B0, 0x2C, 0x1FC, 0xDC8],
                         [0x017AA6C8, 0x3C, 0x84, 0x74, 0x5F8, 0x4, 0x1FC, 0xDC8],
                         [0x017AA6C8, 0x30, 0x5F8, 0x3, 0x1FC, 0xDC8],
                         [0x017AA980, 0x124, 0xC, 0x1C8, 0x104, 0x620, 0xC90],
                         [0x017AA980, 0x44, 0x14, 0x20, 0x4, 0x620, 0xC90]],  # Rebounds
            "Assists": [[0x00E1D06C, 0x18, 0x18, 0x38, 0x18, 0x5C, 0x6E0, 0xE58], [0x00D18884, 0x1C, 0x6E0, 0xE58],
                        [0x00E62D88, 0x38, 0x9B4, 0x18, 0x1C, 0x218, 0xE24],
                        [0x00E355EC, 0x5C, 0x99C, 0x48, 0x1C0, 0xF1C],
                        [0x00E05B64, 0x18, 0x18, 0x1C, 0x638, 0xD70]],  # Assists
            "Steals": [[0x01843A54, 0x198, 0x8, 0x104, 0x48, 0x74, 0xCE4, 0xB20]],  # Steals
            "Turnovers": [[0x00D1F6BC, 0x18, 0x18, 0x808, 0x280], [0x00D1B794, 0x178, 0x18, 0x38, 0x808, 0x280],
                          [0x00D0F8B4, 0x3F8, 0x18, 0x38, 0x808, 0x280],
                          [0x00D3F93C, 0x5DC, 0x318, 0x708, 0x7E8, 0x280],
                          [0x00DFD19C, 0x578, 0x18, 0x9C, 0x4D4, 0x104]],  # Turnovers
            "FG": [[0x00D0F1D4, 0x118, 0x18, 0x1C, 0x7E8, 0x54], [0x00D5E21C, 0x64C, 0x5F4, 0x640, 0x6D4, 0x688],
                   [0x00D349D0, 0x450, 0x374, 0x73C, 0x6D4, 0x688], [0x00D5B7EC, 0x3E8, 0x220, 0x678, 0x808, 0x54],
                   [0x00EEB094, 0x658, 0x798, 0x6D4, 0x688]],  # FG
            "3PT": [[0x00E1FE0C, 0x78, 0x18, 0x1C, 0x6B4, 0x68C], [0x00D332BC, 0x30C, 0x59C, 0x4BC, 0x6B4, 0x68C],
                    [0x00DB81AC, 0x4F0, 0xD8, 0x69C, 0x7E8, 0x58], [0x00D0F1A4, 0x424, 0x578, 0x5C4, 0x6D4, 0x68C],
                    [0x00D1F824, 0x560, 0x328, 0x7B8, 0x6D4, 0x68C], [0x00DB0A4C, 0x354, 0x7B8, 0x6D4, 0x68C]],
            # 3PT
            "Fouls": [[0x00E1AA4C, 0x6C8, 0x7A0, 0x790, 0x808, 0x278],
                      [0x00D3F93C, 0xD8, 0x7A0, 0x790, 0x808, 0x278],
                      [0x00D55DEC, 0x658, 0x18, 0x478, 0x478, 0x808, 0x278],
                      [0x00E18F1C, 0x118, 0x18, 0x6F8, 0x4F4, 0xFC], [0x016C15FC, 0x444]],
            "Dunks": [[0x0138DE50, 0x28, 0x64, 0x38, 0x30, 0x700], [0x00301CE4, 0x7C0], [0x016C16F8, 0x308],
                      [0x016C16FC, 0x2D8], [0x00E1FEAC, 0x38, 0x18, 0x1C, 0x6B4, 0x6B0]]
        },
        {  # Slot 3
            "RosterID": [[0x00D54FE4, 0x18, 0x18, 0x1C, 0x1C0, 0xD8]],  # RosterID
            "Points": [[0x00E1376C, 0x38, 0x18, 0x5C, 0x4D4, 0x598]],  # Points
            "Rebounds": [[0x018198A0, 0x2C, 0xC, 0xC, 0x48, 0x70, 0x698, 0xFA8],
                         [0x01819900, 0x58, 0x0, 0xC, 0x48, 0x70, 0x698, 0xFA8],
                         [0x00D0F3F4, 0x58, 0x18, 0x58, 0x18, 0x38, 0x3E8, 0x200], [0x00D1B594, 0x38, 0x3E8, 0x200],
                         [0x00D1F4B4, 0x38, 0x1C, 0x3C8, 0x200]],  # Rebounds
            "Assists": [[0x00D1F71C, 0x18, 0x38, 0x1C, 0x910, 0x58, 0x808, 0x944],
                        [0x00D1F494, 0x58, 0x18, 0x1C, 0x7E8, 0x944],
                        [0x017AAA70, 0x34, 0xC, 0xB4, 0xD0, 0x964, 0x3E8, 0x220],
                        [0x01819888, 0x58, 0x4C, 0x34, 0x48, 0x70, 0x698, 0xFC8],
                        [0x00E0A754, 0x18, 0x1C, 0x924, 0x900]],  # Assists
            "Steals": [[0x00D2E0F4, 0x4, 0x64, 0x2C, 0x4C, 0x1C, 0xD88, 0xE28]],  # Steals
            "Turnovers": [[0x00E1C70C, 0x1B8, 0x18, 0x798, 0x4F4, 0x7CC],
                          [0x00E04C1C, 0x58, 0x5A0, 0x4C8, 0x514, 0x554],
                          [0x00D538EC, 0x58, 0x18, 0x64, 0x584, 0x554],
                          [0x00E17274, 0x18, 0x38, 0x1C, 0x4D4, 0x7CC], [0x016C1D24, 0x3EC]],  # Turnovers
            "FG": [[0x00D544EC, 0x264, 0xC, 0x1C, 0x514, 0x328], [0x00D1F414, 0x38, 0x18, 0x284, 0x538, 0x328],
                   [0x00D3FC4C, 0x328, 0x668, 0x67C, 0x7E8, 0x71C], [0x00E1209C, 0x138, 0x18, 0x35C, 0x4D4, 0x5A0],
                   [0x0138DE50, 0x28, 0x2BC, 0x40, 0x30, 0x10]],  # FG
            "3PT": [[0x00D541EC, 0xE4, 0xC, 0x558, 0x32C], [0x00DB019C, 0x1F8, 0x5A0, 0x4E4, 0x538, 0x32C],
                    [0x00E1213C, 0x78, 0x18, 0x3D8, 0x4F4, 0x5A4], [0x00E661D8, 0x98, 0x18, 0x764, 0x558, 0x32C],
                    [0x00DF2B00, 0x7C0, 0x890, 0x728, 0x7E8, 0x720]],  # 3PT
            "Fouls": [[0x00E10D3C, 0x358, 0x18, 0x17C, 0x4D4, 0x7C4],
                      [0x00DFD28C, 0x418, 0x18, 0x17C, 0x4D4, 0x7C4],
                      [0x00D5C5EC, 0x6F8, 0x6B6, 0x4FC, 0x3C8, 0x21C],
                      [0x00D0F204, 0x18, 0x18, 0x1F8, 0x3E8, 0x21C],
                      [0x00E10C4C, 0x278, 0x18, 0x298, 0x4F4, 0x7C4]],
            "Dunks": [[0x00D1B7A4, 0x38, 0x18, 0x38, 0x808, 0x744], [0x00D1B7A4, 0x58, 0x808, 0x744],
                      [0x016C1C34, 0x338], [0x00E1722C, 0x38, 0x18, 0x58, 0x4F4, 0x5C8],
                      [0x00DFFE9C, 0x38, 0x18, 0x5C, 0x4D4, 0x5C8]]
        },
        {  # Slot 4
            "RosterID": [[0x010729A0, 0x240, 0xC0, 0x1F8, 0x1C, 0x2B0]],  # RosterID
            "Points": [[0x0138DE58, 0x28, 0x2BC, 0x44, 0x30, 0x8]],  # Points
            "Rebounds": [[0x00D1B7A4, 0x18, 0x18, 0x5C, 0x7E8, 0xFEC], [0x016C1B40, 0x5C4],
                         [0x00DB2A94, 0x44, 0x38, 0x5C, 0x1C, 0x964, 0xDFC],
                         [0x0110A4F0, 0x4, 0xC, 0x48, 0x70, 0x8, 0x30, 0x8E0], [0x0059D6A0, 0x314]],  # Rebounds
            "Assists": [[0x0110A5B4, 0x8, 0x4, 0xC, 0x48, 0x250, 0x30, 0xFC8], [0x007618C4, 0x33C],
                        [0x016C232C, 0x4A8], [0x00DB2A94, 0x44, 0x38, 0x5C, 0x18, 0x1C, 0x964, 0xE1C],
                        [0x0138DE6C, 0xC, 0x8, 0x48, 0x258, 0x30, 0x238]],  # Assists
            "Steals": [[0x0138DE6C, 0x4, 0x8, 0x48, 0x64, 0x40, 0x214, 0x230]],  # Steals
            "Turnovers": [[0x0138DE58, 0x28, 0x64, 0x44, 0x30, 0x23C], [0x0138DE58, 0x28, 0x258, 0x30, 0x23C],
                          [0x0181987C, 0x114, 0x48, 0x258, 0x30, 0x23C],
                          [0x01819888, 0xD4, 0x48, 0x1C, 0x5DC, 0x23C], [0x0138DE50, 0x28, 0x24C, 0x5DC, 0x23C],
                          [0x016C22FC, 0x53C], [0x0181987C, 0x114, 0x48, 0x124, 0x65C, 0x23C]],  # Turnovers
            "FG": [[0x00D1B57C, 0x18, 0x3B8, 0x3E8, 0x6C0], [0x00D3349C, 0x598, 0x18, 0x398, 0x3E8, 0x6C0],
                   [0x00D0F36C, 0x18, 0xF8, 0x3E8, 0x6C0], [0x00D0F0E4, 0x2D8, 0x18, 0x7C, 0x3C8, 0x6C0]],  # FG
            "3PT": [[0x00D0F8F4, 0x4F8, 0x18, 0x9C, 0x3C8, 0x6C4], [0x016C22CC, 0x344],
                    [0x00D1F6C4, 0x238, 0x18, 0xD8, 0x3E8, 0x6C4], [0x00D0F1D4, 0xB8, 0x18, 0x358, 0x3E8, 0x6C4],
                    [0x00D334DC, 0x78, 0x18, 0x7B8, 0x3E8, 0x6C4]],  # 3PT
            "Fouls": [[0x0138DE58, 0x28, 0x64, 0x3C, 0x3F8, 0x234], [0x0138DE58, 0x28, 0x1C, 0x5DC, 0x234],
                      [0x01819924, 0x1E4, 0x48, 0x24C, 0x5DC, 0x234], [0x018198A0, 0x54, 0x48, 0x124, 0x65C, 0x234],
                      [0x000571B4, 0x320]],
            "Dunks": [[0x0138DE58, 0x28, 0x64, 0x3C, 0x214, 0x700], [0x0138DE50, 0x28, 0x64, 0x38, 0x3F8, 0x700],
                      [0x00165D88, 0x144], [0x00019614, 0x15C], [0x016C23BC, 0x218]]
        },
        {  # Slot 5
            "RosterID": [[0x00E6C43C, 0x38, 0x18, 0x1C, 0xCC, 0x240]],  # RosterID
            "Points": [[0x0138DE50, 0x28, 0x64, 0x40, 0x214, 0x6D0]],  # Points
            "Rebounds": [[0x018198A0, 0x10, 0x14, 0x48, 0x64, 0x48, 0x30, 0x218], [0x00D1F4B4, 0x3C, 0x3C8, 0xF90],
                         [0x00D1F4B4, 0x18, 0x18, 0x38, 0x3E8, 0xF90], [0x00D1B594, 0x38, 0x3E8, 0xF90],
                         [0x017AAA70, 0xC4, 0x4, 0xDC, 0x30, 0x3A4, 0x3E8, 0xF90]],  # Rebounds
            "Assists": [[0x0138DE58, 0x28, 0x70, 0xC, 0x214, 0x238], [0x016C2934, 0x5C8], [0x016C29C4, 0x538],
                        [0x016C2B54, 0x4D8], [0x016C2AE4, 0x3B8]],  # Assists
            "Steals": [[0x0110A5B4, 0xC, 0x4, 0xC, 0x48, 0x254, 0x30, 0xFC0]],  # Steals
            "Turnovers": [[0x01819894, 0x94, 0x48, 0x25C, 0x30, 0x23C],
                          [0x0138DE50, 0x28, 0x2BC, 0x40, 0x3F8, 0x23C], [0x0138DE50, 0x28, 0x24C, 0x7C0, 0x23C],
                          [0x0138DE58, 0x28, 0x70, 0x0, 0x7C0, 0x23C], [0x016C2A84, 0x41C]],  # Turnovers
            "FG": [[0x0138DE50, 0x28, 0x24C, 0x7C0, 0x10], [0x0138DE58, 0x28, 0x70, 0x0, 0x7C0, 0x10],
                   [0x016C2934, 0x3A0], [0x018198A0, 0x54, 0x48, 0x250, 0x3F8, 0x6D8],
                   [0x0138DE50, 0x28, 0x258, 0x214, 0x10]],  # FG
            "3PT": [[0x01819894, 0x94, 0x48, 0x24C, 0x5DC, 0x6DC], [0x0138DE58, 0x28, 0x70, 0x0, 0x5Dc, 0x6DC],
                    [0x018504B0, 0x14], [0x0138DE58, 0x28, 0x70, 0x4, 0x3F8, 0x6DC],
                    [0x0138DE50, 0x28, 0x70, 0xC, 0x214, 0x14]],  # 3PT
            "Fouls": [[0x0138DE50, 0x28, 0x70, 0x8, 0x3F8, 0x234], [0x018198A0, 0x54, 0x48, 0x258, 0x214, 0x234],
                      [0x0181987C, 0x114, 0x48, 0x25C, 0x30, 0x234], [0x0138DE50, 0x28, 0x64, 0x3C, 0x5DC, 0x234],
                      [0x016C2AE4, 0x3B4]],
            "Dunks": [[0x0138DE58, 0x28, 0x70, 0x8, 0x214, 0x700], [0x007618C4, 0x804], [0x01850218, 0x700],
                      [0x016C2208, 0x3E4], [0x0138DE50, 0x28, 0x70, 0x10, 0x30, 0x38]]
        },
        {  # Slot 6
            "RosterID": [[0x00E35864, 0x18, 0x38, 0x1C, 0x4AC, 0x454]],  # RosterID
            "Points": [[0x0138DE58, 0x28, 0x70, 0x2F4, 0x30, 0x8]],  # Points
            "Rebounds": [[0x018198A0, 0x10, 0x14, 0x48, 0x70, 0x2F4, 0x30, 0x218],
                         [0x0138DE6C, 0x4, 0x0, 0x48, 0x70, 0x2F4, 0x30, 0x218],
                         [0x0138DE58, 0x28, 0x70, 0x70, 0x32C, 0x30, 0x218],
                         [0x010DFAF4, 0xC, 0x10, 0x48, 0x64, 0x32C, 0x30, 0x218],
                         [0x0138DE6C, 0xC, 0x10, 0x48, 0x64, 0x32C, 0x30, 0x218]],  # Rebounds
            "Assists": [[0x01851970, 0x238], [0x0138DE50, 0x28, 0x70, 0x2F4, 0x30, 0x238],
                        [0x0138DE58, 0x28, 0x70, 0x2F4, 0x30, 0x238]],  # Assists
            "Steals": [[0x0138DE50, 0x28, 0x70, 0x70, 0x32C, 0x30, 0x230],
                       [0x0138DE6C, 0x4, 0x0, 0x48, 0x2BC, 0x32C, 0x30, 0x230],
                       [0x0138DE5C, 0x4, 0x0, 0x48, 0x2BC, 0x2BC, 0x32C, 0x30, 0x230],
                       [0x018198A0, 0x10, 0x14, 0x48, 0x64, 0x32C, 0x30, 0x230],
                       [0x0138DE50, 0x28, 0x64, 0xA8, 0x32C, 0x30, 0x230]],  # Steals
            "Turnovers": [[0x01819870, 0x184, 0x48, 0x540, 0x30, 0x23C],
                          [0x01819894, 0x94, 0x48, 0x540, 0x30, 0x23C],
                          [0x0138DE58, 0x28, 0x2BC, 0x32C, 0x30, 0x23C],
                          [0x0138DE58, 0x28, 0x70, 0x2F4, 0x30, 0x23C], [0x01851970, 0x23C]],  # Turnovers
            "FG": [[0x0138DE50, 0x28, 0x70, 0x2F4, 0x30, 0x10], [0x0138DE58, 0x28, 0x540, 0x30, 0x10],
                   [0x01819888, 0xD4, 0x48, 0x540, 0x30, 0x10], [0x01819930, 0x1B4, 0x48, 0x540, 0x30, 0x10],
                   [0x0138DE58, 0x28, 0x2BC, 0x32C, 0x30, 0x10]],  # FG
            "3PT": [[0x0138DE50, 0x28, 0x70, 0x2F4, 0x30, 0x14], [0x0138DE50, 0x28, 0x64, 0x32C, 0x30, 0x14],
                    [0x0138DE50, 0x28, 0x540, 0x30, 0x14], [0x01819888, 0xD4, 0x48, 0x540, 0x30, 0x14],
                    [0x01819930, 0x1B8, 0x48, 0x540, 0x30, 0x14]],  # 3PT
            "Fouls": [[0x01819930, 0x1B4, 0x48, 0x540, 0x30, 0x234], [0x01819888, 0xD4, 0x48, 0x540, 0x30, 0x234],
                      [0x0138DE50, 0x28, 0x540, 0x30, 0x234], [0x0138DE50, 0x28, 0x64, 0x32C, 0x30, 0x234],
                      [0x01851970, 0x234]],
            "Dunks": [[0x01819870, 0x184, 0x48, 0x540, 0x30, 0x38]]
        },
        {  # Slot 7
            "RosterID": [[0x017D751C, 0x68C, 0x1C, 0x1B4, 0x15C]],  # RosterID
            "Points": [[0x0138DE58, 0x28, 0x70, 0x70, 0x32C, 0x30, 0x6D0]],  # Points
            "Rebounds": [[0x0138DE58, 0x28, 0x70, 0x70, 0x32C, 0x214, 0x218],
                         [0x0138DE50, 0x28, 0x540, 0x30, 0x8E0], [0x0138DE50, 0x28, 0x70, 0x2F8, 0x30, 0x218],
                         [0x0138DE50, 0x28, 0x544, 0x30, 0x218], [0x0138DE58, 0x28, 0x544, 0x30, 0x218]],
            # Rebounds
            "Assists": [[0x0138DE50, 0x28, 0x70, 0x2F4, 0x214, 0x238], [0x01851C08, 0x238],
                        [0x0138DE50, 0x28, 0x64, 0x32C, 0x214, 0x238],
                        [0x0138DE50, 0x28, 0x2BC, 0x32C, 0x214, 0x238],
                        [0x0138DE50, 0x28, 0x64, 0x330, 0x30, 0x238]],  # Assists
            "Steals": [[0x01851970, 0x8F8], [0x01851C08, 0x230], [0x0138DE50, 0x28, 0x70, 0x2F4, 0x214, 0x230],
                       [0x010DFAF4, 0xC, 0x10, 0x48, 0x70, 0x2F4, 0x214, 0x230],
                       [0x0138DE50, 0x28, 0x64, 0x32C, 0x214, 0x230]],  # Steals
            "Turnovers": [[0x0138DE50, 0x28, 0x70, 0x2F4, 0x214, 0x23C],
                          [0x0138DE50, 0x28, 0x2BC, 0x32C, 0x214, 0x23C], [0x0138DE58, 0x28, 0x540, 0x214, 0x23C],
                          [0x0181987C, 0x114, 0x48, 0x540, 0x214, 0x23C], [0x0138DE50, 0x28, 0x544, 0x30, 0x23C]],
            # Turnovers
            "FG": [[0x01819870, 0x184, 0x48, 0x540, 0x214, 0x10], [0x01851970, 0x6D8],
                   [0x0138DE50, 0x28, 0x2BC, 0x32C, 0x30, 0x6D8], [0x0138DE58, 0x28, 0x2BC, 0x330, 0x30, 0x10],
                   [0x01819870, 0x184, 0x48, 0x544, 0x30, 0x10]],  # FG
            "3PT": [[0x0138DE58, 0x28, 0x64, 0x330, 0x30, 0x14], [0x0138DE58, 0x28, 0x64, 0x32C, 0x30, 0x6DC],
                    [0x01819924, 0x1E4, 0x48, 0x540, 0x30, 0x6DC], [0x018198A0, 0x54, 0x48, 0x540, 0x214, 0x14],
                    [0x01819930, 0x1B4, 0x48, 0x540, 0x214, 0x14]],  # 3PT
            "Fouls": [[0x01819870, 0x184, 0x48, 0x544, 0x30, 0x234], [0x0138DE58, 0x28, 0x64, 0x330, 0x30, 0x234],
                      [0x01819888, 0xD4, 0x48, 0x540, 0x214, 0x234], [0x0138DE50, 0x28, 0x2BC, 0x32C, 0x214, 0x234],
                      [0x01851C08, 0x234]],
            "Dunks": [[0x01851970, 0x700], [0x01819870, 0x184, 0x48, 0x540, 0x30, 0x700],
                      [0x018198A0, 0x54, 0x48, 0x540, 0x214, 0x38], [0x0138DE58, 0x28, 0x2BC, 0x330, 0x30, 0x38],
                      [0x01819930, 0x1B4, 0x48, 0x544, 0x30, 0x38]]
        },
        {  # Slot 8
            "RosterID": [[0x184F2FC, 0x678]],  # RosterID
            "Points": [[0x018198A0, 0x10, 0x14, 0x48, 0x70, 0x2F8, 0x30, 0x6D0]],  # Points
            "Rebounds": [[0x018198A0, 0x2C, 0x4, 0x48, 0x70, 0x2F4, 0x30, 0xFA8],
                         [0x0138DE50, 0x28, 0x70, 0x2F4, 0x30, 0xFA8],
                         [0x0138DE50, 0x28, 0x2BC, 0x330, 0x214, 0x218], [0x01851C08, 0x8E0],
                         [0x0138DE50, 0x28, 0x64, 0x334, 0x30, 0x218]],  # Rebounds
            "Assists": [[0x01851EA0, 0x238], [0x0138DE50, 0x28, 0x70, 0x2FC, 0x30, 0x238],
                        [0x0138DE50, 0x28, 0x64, 0x334, 0x30, 0x238], [0x0138DE58, 0x28, 0x64, 0x334, 0x30, 0x238],
                        [0x0138DE50, 0x28, 0x2BC, 0x334, 0x30, 0x238]],  # Assists
            "Steals": [[0x0138DE50, 0x28, 0x540, 0x3F8, 0x230],
                       [0x018198A0, 0x18, 0x44, 0x4, 0x48, 0x540, 0x3F8, 0x230],
                       [0x01819894, 0x50, 0x14, 0x48, 0x540, 0x30, 0xFC0],
                       [0x0138DE6C, 0x4, 0x8, 0x48, 0x544, 0x30, 0x8F8],
                       [0x0138DE50, 0x28, 0x70, 0x2FC, 0x30, 0x230]],  # Steals
            "Turnovers": [[0x0138DE50, 0x28, 0x64, 0x32C, 0x3F8, 0x23C], [0x01851EA0, 0x23C],
                          [0x0138DE50, 0x28, 0x540, 0x3F8, 0x23C], [0x0138DE58, 0x28, 0x544, 0x214, 0x23C],
                          [0x0138DE50, 0x28, 0x70, 0x2FC, 0x30, 0x23C]],  # Turnovers
            "FG": [[0x0138DE58, 0x28, 0x64, 0x32C, 0x3F8, 0x10], [0x018198A0, 0x54, 0x48, 0x540, 0x3F8, 0x10],
                   [0x01851EA0, 0x10], [0x0138DE50, 0x28, 0x548, 0x30, 0x10],
                   [0x01819888, 0xD4, 0x48, 0x540, 0x214, 0x6D8]],  # FG
            "3PT": [[0x0138DE50, 0x28, 0x2BC, 0x330, 0X214, 0X14], [0x0138DE58, 0x28, 0x544, 0x214, 0x14],
                    [0x0138DE58, 0x28, 0x64, 0x32C, 0x214, 0x6DC], [0x0138DE50, 0x28, 0x540, 0x3F8, 0x14],
                    [0x0138DE50, 0x28, 0x544, 0x30, 0x6DC]],  # 3PT
            "Fouls": [[0x01819870, 0x184, 0x48, 0x548, 0x30, 0x234], [0x018198A0, 0x54, 0x48, 0x540, 0x3F8, 0x234],
                      [0x01819870, 0x184, 0x48, 0x544, 0x214, 0x234], [0x01851EA0, 0x234],
                      [0x0138DE58, 0x28, 0x64, 0x334, 0x30, 0x234]],
            "Dunks": [[0x0181987C, 0x114, 0x48, 0x544, 0x30, 0x700], [0x01819870, 0x184, 0x48, 0x540, 0x3F8, 0x38],
                      [0x0138DE58, 0x28, 0x64, 0x32C, 0x3F8, 0x38], [0x01851C08, 0x700],
                      [0x0138DE50, 0x28, 0x64, 0x334, 0x30, 0x38]]
        },
        {  # Slot 9
            "RosterID": [[0x0184F300, 0x678]],  # RosterID
            "Points": [[0x010DFAF4, 0xC, 0x8, 0x48, 0x70, 0x2F4, 0x214, 0xD98]],  # Points
            "Rebounds": [[0x01843AD4, 0x28, 0x0, 0xC, 0x48, 0x548, 0x214, 0x218],
                         [0x0138DE50, 0x28, 0x544, 0x214, 0x8E0], [0x0138DE5C, 0xC, 0x8, 0x48, 0x54C, 0x30, 0x218],
                         [0x010DFAF4, 0xC, 0x10, 0x48, 0x70, 0x300, 0x30, 0x218],
                         [0x0138DE58, 0x28, 0x70, 0x300, 0x30, 0x218]],  # Rebounds
            "Assists": [[0x0138DE50, 0x28, 0x70, 0x2FC, 0x214, 0x238], [0x016C3FAC, 0x4D8], [0x016C3F3C, 0x3B8],
                        [0x0138DE50, 0x28, 0x2BC, 0x338, 0x30, 0x238],
                        [0x0138DE58, 0x28, 0x64, 0x338, 0x30, 0x238]],  # Assists
            "Steals": [[0x01851C08, 0xFC0]],  # Steals
            "Turnovers": [[0x0138DE58, 0x28, 0x70, 0x300, 0x30, 0x23C], [0x0138DE50, 0x28, 0x54C, 0x30, 0x23C],
                          [0x0138DE50, 0x28, 0x2BC, 0x32C, 0x5DC, 0x23C],
                          [0x0138DE50, 0x28, 0x2BC, 0x330, 0x3F8, 0x23C], [0x0138DE50, 0x28, 0x548, 0x214, 0x23C],
                          [0x01852138, 0x23C]],  # Turnovers
            "FG": [[0x0138DE50, 0x28, 0x540, 0x5DC, 0x10], [0x01819870, 0x184, 0x48, 0x540, 0x5DC, 0x10],
                   [0x0138DE50, 0x28, 0x70, 0x2F8, 0x3F8, 0x10], [0x01819930, 0x1B4, 0x48, 0x54C, 0x30, 0x10],
                   [0x0138DE50, 0x28, 0x2BC, 0x334, 0x30, 0x6D8]],  # FG
            "3PT": [[0x0138DE58, 0x28, 0x70, 0x2Fc, 0x30, 0x6DC], [0x0138DE50, 0x28, 0x548, 0x30, 0x6DC],
                    [0x0138DE50, 0x28, 0x70, 0x2F4, 0x5DC, 0x14], [0x01819930, 0x1B4, 0x48, 0x544, 0x214, 0x6DC],
                    [0x01819888, 0xD4, 0x48, 0x544, 0x3F8, 0x14], [0x0138DE50, 0x28, 0x64, 0x334, 0x214, 0x14]],
            # 3PT
            "Fouls": [[0x0138DE50, 0x28, 0x2BC, 0x32C, 0x5DC, 0x234], [0x018198A0, 0x54, 0x48, 0x54C, 0x30, 0x234],
                      [0x01819888, 0xD4, 0x48, 0x544, 0x3F8, 0x234], [0x0181987C, 0x114, 0x48, 0x548, 0x214, 0x234],
                      [0x01819930, 0x1B4, 0x48, 0x548, 0x214, 0x234]],
            "Dunks": [[0x0138DE50, 0x28, 0x2BC, 0x32C, 0x3F8, 0x700], [0x0138DE58, 0x28, 0x64, 0x32C, 0x5DC, 0x38],
                      [0x01819870, 0x184, 0x48, 0x54C, 0x30, 0x38], [0x0181987C, 0x114, 0x48, 0x544, 0x214, 0x700],
                      [0x01851EA0, 0x700]]
        },
        {  # Slot 10
            "RosterID": [[0x0184F304, 0x678]],  # RosterID
            "Points": [[0x01843B94, 0x8C, 0x0, 0xC, 0x48, 0x54C, 0x30, 0x6D0]],  # Points
            "Rebounds": [[0x018523D0, 0x218], [0x016C4C3C, 0x428], [0x01852138, 0x8E0], [0x016C4544, 0xB20],
                         [0x016C4AB4, 0xC8C]],  # Rebounds
            "Assists": [[0x0138DE58, 0x28, 0x70, 0x300, 0x214, 0x238], [0x016C4BAC, 0x538], [0x016C4C3C, 0x448],
                        [0x018523D0, 0x238], [0x0138DE50, 0x28, 0x64, 0x33C, 0x30, 0x238]],  # Assists
            "Steals": [[0x016C4C3C, 0x440], [0x016C4BAC, 0x530], [0x016C517C, 0x5DC], [0x016C4670, 0xBC8]],
            # Steals
            "Turnovers": [[0x0138DE50, 0x28, 0x64, 0x32C, 0x7C0, 0x23C],
                          [0x01819930, 0x1B4, 0x48, 0x54C, 0x214, 0x23C],
                          [0x0138DE58, 0x28, 0x70, 0x300, 0x214, 0x23C],
                          [0x0138DE58, 0x28, 0x70, 0x2F8, 0x5DC, 0x23C], [0x016C4CCC, 0x3BC]],  # Turnovers
            "FG": [[0x0138DE58, 0x28, 0x64, 0x334, 0x3F8, 0x10], [0x01819870, 0x184, 0x48, 0x548, 0x3F8, 0x10],
                   [0x016C4BAC, 0x310], [0x01819924, 0x1E4, 0x48, 0x54C, 0x214, 0x10],
                   [0x0138DE50, 0x28, 0x2BC, 0x338, 0x30, 0x6D8]],  # FG
            "3PT": [[0x0138DE50, 0x28, 0x70, 0x300, 0x30, 0x6DC], [0x0138DE58, 0x28, 0x2BC, 0x338, 0x30, 0x6DC],
                    [0x0138DE58, 0x28, 0x544, 0x3F8, 0x6DC], [0x0138DE5828, 0x550, 0x30, 0x14],
                    [0x018198A0, 0x54, 0x48, 0x25C, 0x7C0, 0x6DC]],  # 3PT
            "Fouls": [[0x0138DE50, 0x28, 0x64, 0x33C, 0x30, 0x234], [0x0181987C, 0x114, 0x48, 0x540, 0x7C0, 0x234],
                      [0x0138DE50, 0x28, 0x2BC, 0x330, 0x5DC, 0x234], [0x0138DE50, 0x28, 0x64, 0x334, 0x3F8, 0x234],
                      [0x016C4BDC, 0x4A4]],
            "Dunks": [[0x01819870, 0x184, 0x48, 0x540, 0x5DC, 0x700], [0x018198A0, 0x54, 0x48, 0x544, 0x5DC, 0x38],
                      [0x0138DE58, 0x28, 0x64, 0x48, 0x7C0, 0x700], [0x0138DE58, 0x28, 0x70, 0x2F8, 0x3F8, 0x700],
                      [0x016C4C9C, 0x1E8]]
        }
    ]
    # This method rips slot stats from the current blacktop game, returning them as a neatly
    # formatted dictionary. Assumes 2k is open.
    def ripSlotStats(self):
        newSlotStats = {0: {}, 1: {}, 2: {}, 3: {}, 4: {}, 5: {}, 6: {}, 7: {}, 8: {}, 9: {}}

        gameMode = self.getBlacktopMode()
        for i in range(10):
            if ((i % 5) + 1 > gameMode):
                newSlotStats[i]["IsActive"] = 0
            else:
                newSlotStats[i]["IsActive"] = 1
                newSlotStats[i]["RosterID"] = self.getStatValue(i, "RosterID", False)
                newSlotStats[i]["Points"] = self.getStatValue(i, "Points")
                newSlotStats[i]["DefensiveRebounds"] = self.getStatValue(i, "Rebounds")
                newSlotStats[i]["OffensiveRebounds"] = self.getStatValue(i, "Rebounds", True)
                newSlotStats[i]["PointsPerAssist"] = self.getStatValue(i, "Assists", True)
                newSlotStats[i]["AssistCount"] = self.getStatValue(i, "Assists")
                newSlotStats[i]["Steals"] = self.getStatValue(i, "Steals")
                newSlotStats[i]["Blocks"] = self.getStatValue(i, "Blocks", True)
                newSlotStats[i]["Turnovers"] = self.getStatValue(i, "Turnovers")
                newSlotStats[i]["InsidesMade"] = self.getStatValue(i, "FG")
                newSlotStats[i]["InsidesAttempted"] = self.getStatValue(i, "FG", True)
                newSlotStats[i]["ThreesMade"] = self.getStatValue(i, "3PT")
                newSlotStats[i]["ThreesAttempted"] = self.getStatValue(i, "3PT", True)
                newSlotStats[i]["Fouls"] = self.getStatValue(i, "Fouls")
                newSlotStats[i]["Dunks"] = self.getStatValue(i, "Dunks", )
                newSlotStats[i]["Layups"] = self.getStatValue(i, "Dunks", True)
                newSlotStats[i]["Unknown1"] = self.getStatValue(i, "Turnovers", True)
                newSlotStats[i]["Unknown2"] = self.getStatValue(i, "Fouls", True)
        return newSlotStats
    # This method uses some of the above boxScoreSlot addresses, and simply tests if the current running game has
    # been won or not. Assumes a game is playing.
    def testIfGameIsWon(self):
        gameIsPlaying = self.testInGame()
        if (gameIsPlaying):
            gameMode = self.getBlacktopMode()

            # Here we calculate each team's current score.
            ringersScore = 0
            for i in range(0,gameMode):
                ringersScore += self.getStatValue(i, "Points")
            ballerzScore = 0
            for i in range(5,5 + gameMode):
                ballerzScore += self.getStatValue(i, "Points")

            if (ballerzScore >= 21 or ringersScore >= 21):
                if (abs(ballerzScore - ringersScore) >= 2):
                    return True
        return False

    # Here is addresses and methods for manually updating display stats.
    ballerzPointDisplay = [[0x00DF094C,0x2E8,0x184,0x7C0,0x620,0x578],[0x00D7D47C,0x1C,0x5C,0x340,0x620,0x578],[0x00DF09F0,0x2E8,0x568,0x454,0x640,0x578],[0x009C0BE4,0x104],[0x007184E4,0x0]]
    ringersPointDisplay = [[0x00DB5FAC,0x38,0x18,0x38,0x640,0x57C],[0x00DB5CBC,0x18,0x58,0x640,0x57C],[0x00DB8D44,0x58,0x18,0x1C,0x620,0x57C],[0x00DB5CBC,0x18,0x5C,0x620,0x57C]]
    def manuallyUpdatePointDisplay(self):
        gameMode = self.getBlacktopMode()
        ballerzPoints = 0
        slot1Points = self.getStatValue(0,"Points")
        if(slot1Points is not None):
            ballerzPoints += slot1Points
        slot2Points = self.getStatValue(1,"Points")
        if(slot2Points is not None and gameMode >= 2):
            ballerzPoints += slot2Points
        slot3Points = self.getStatValue(2,"Points")
        if(slot3Points is not None and gameMode >= 3):
            ballerzPoints += slot3Points
        slot4Points = self.getStatValue(3,"Points")
        if(slot4Points is not None and gameMode >= 4):
            ballerzPoints += slot4Points
        slot5Points = self.getStatValue(4,"Points")
        if(slot5Points is not None and gameMode >= 5):
            ballerzPoints += slot5Points

        ringersPoints = 0
        slot6Points = self.getStatValue(5,"Points")
        if(slot6Points is not None):
            ringersPoints += slot6Points
        slot7Points = self.getStatValue(6,"Points")
        if(slot7Points is not None and gameMode >= 2):
            ringersPoints += slot7Points
        slot8Points = self.getStatValue(7,"Points")
        if(slot8Points is not None and gameMode >= 3):
            ringersPoints += slot8Points
        slot9Points = self.getStatValue(8,"Points")
        if(slot9Points is not None and gameMode >= 4):
            ringersPoints += slot9Points
        slot10Points = self.getStatValue(9,"Points")
        if(slot10Points is not None and gameMode >= 5):
            ringersPoints += slot10Points


        try:
            self.mem.write_int(self.getPointerAddress(self.ballerzPointDisplay[0]),ballerzPoints)
            self.mem.write_int(self.getPointerAddress(self.ringersPointDisplay[0]),ringersPoints)
            return True
        except pymem.exception.MemoryWriteError:
            return False
    # These two methods deal with distributing the coin. Simply put, they add or remove a single point to
    # Player 1 or 6's FGM and FGA. These points can then be removed before actually ripping stats.
    # TODO determine, is this actually adding to FGM and FGA or just an arbitrary point value? AND MAKE SURE TO GET
    # RID OF THE STATS TOO HOMBRE
    def addCoin(self,team):
        if(team.lower() == "ringers"):
            currentVal = self.mem.read_int(self.getPointerAddress(self.boxScoreSlots[5].get("Points")[0]))
            self.mem.write_int(self.getPointerAddress(self.boxScoreSlots[5].get("Points")[0]),currentVal + 1)
        elif(team.lower() == "ballerz"):
            currentVal = self.mem.read_int(self.getPointerAddress(self.boxScoreSlots[0].get("Points")[0]))
            self.mem.write_int(self.getPointerAddress(self.boxScoreSlots[0].get("Points")[0]),currentVal + 1)
    def removeCoin(self,team):
        if(team.lower() == "ringers"):
            currentVal = self.mem.read_int(self.getPointerAddress(self.boxScoreSlots[5].get("Points")[0]))
            self.mem.write_int(self.getPointerAddress(self.boxScoreSlots[5].get("Points")[0]),currentVal - 1)
        elif (team.lower() == "ballerz"):
            currentVal = self.mem.read_int(self.getPointerAddress(self.boxScoreSlots[0].get("Points")[0]))
            self.mem.write_int(self.getPointerAddress(self.boxScoreSlots[0].get("Points")[0]),currentVal - 1)

    # This method performs the "final rip" of all stats from the game into a single dictionary which it outputs.
    # Use this once a game has been determined to be won.
    def ripAllStats(self):
        slotStats = self.ripSlotStats()
        gameStats = self.ripGameStats(slotStats=slotStats)
        # Remove the coin given. # TODO
        if(gameStats["GameMode"] >= 4):
            pass
        returnStats = {"GameStats" : gameStats,"SlotStats" : slotStats}

        # Store all ripped stats into object.
        return returnStats

    # Given a set of slot stats, this  helper method totals points into usable ballerzScore and ringersScore
    def calculateScores(self,slotStats):
        scoresDict = {"BallerzScore" : 0, "RingerScore" : 0}
        blacktopMode = self.getBlacktopMode()
        if(blacktopMode == 1):
            scoresDict["BallerzScore"] = slotStats[0]["Points"]
            scoresDict["RingersScore"] = slotStats[5]["Points"]
        elif(blacktopMode == 2):
            scoresDict["BallerzScore"] = slotStats[0]["Points"] + slotStats[1]["Points"]
            scoresDict["RingersScore"] = slotStats[5]["Points"] + slotStats[6]["Points"]
        elif(blacktopMode == 3):
            scoresDict["BallerzScore"] = slotStats[0]["Points"] + slotStats[1]["Points"] + slotStats[2]["Points"]
            scoresDict["RingersScore"] = slotStats[5]["Points"] + slotStats[6]["Points"] + slotStats[7]["Points"]
        elif(blacktopMode == 4):
            scoresDict["BallerzScore"] = slotStats[0]["Points"] + slotStats[1]["Points"] + slotStats[2]["Points"] + slotStats[3]["Points"]
            scoresDict["RingersScore"] = slotStats[5]["Points"] + slotStats[6]["Points"] + slotStats[7]["Points"] + slotStats[8]["Points"]
        elif(blacktopMode == 5):
            scoresDict["BallerzScore"] = slotStats[0]["Points"] + slotStats[1]["Points"] + slotStats[2]["Points"] + slotStats[3]["Points"] + slotStats[4]["Points"]
            scoresDict["RingersScore"] = slotStats[5]["Points"] + slotStats[6]["Points"] + slotStats[7]["Points"] + slotStats[8]["Points"] + slotStats[9]["Points"]
        return scoresDict

    # Is 0 if the ball is in play, is any other number (undetermined) if it's not.
    isBallInPlayAddress = [[0x0002BC48,0x164],[0x00035ADC,0x164],[0x00037D14,0x3A4],[0x00037A78,0x3D4],[0x009AEA88,0x154]]
    def testIfBallIsInPlay(self):
        isBallInPlayVal = self.getAddressValue(self.isBallInPlayAddress[0])
        if(isBallInPlayVal == 0):
            return True
        else:
            return False
    ballHolderAddress = [[0x00550FA0,0x8],[0x017AA6C8,0x7C,0x670,0x24,0x3E8,0x4,0x284,0x730],[0x40,0x48,0x24,0x670,0x2C,0x284,0x730],[0x00D3E51C,0x4,0xC,0x18,0x18,0x1C,0x2A4,0x6B0],[0x01843A14,0x30C,0x304,0x70,0x10,0xE0,0x46C,0x450],[0x00DF05EC,0x3C,0x4C,0x38,0x7C8,0x598],[0x00DF05E4,0x18,0x3C,0x44,0x4,0x44,0x7E8,0x598]]
    # This function returns the current ball holder (iValue)
    def getBallHolder(self):
        currentIValue = self.getAddressValue(addressSet=self.ballHolderAddress[0])
        return currentIValue
    # This helper method, when given a COMPLETE list of scraped i values (must be complete, otherwise
    # function will map incorrectly), a dictionary of rosterIDs mapped to a specific blacktop slot, a rosterName,
    # and a data storage object, this function returns a mapped list of each rosterID to its corresponding i value.
    # End result looks like {419052152 (iValue) : 26 (RosterID)}
    def mapIValues(self,iValues: list, rosterIDs: dict, rosterName: str):
        mappedIValues = {}

        # Given a dictionary of rosterIDs mapped to a specific blacktop slot, a rosterName,
        # and a data storage object, will calculate each rosterIDs' a value (the order compared to all other rosterIDs on that
        # team)
        def mapAValues():
            _aValues = {}

            ballerzWeights = {}
            ringersWeights = {}
            for rosterID, slot in rosterIDs.items():

                tempWeight = (self.dataStorage.csvRosterDict[rosterName]["HeightMap"][rosterID][
                                  "RealHeight"] * 1000) + \
                             self.dataStorage.csvRosterDict[rosterName]["HeightMap"][rosterID]["HeightAdjustment"]
                if (slot >= 5):
                    ringersWeights[tempWeight] = rosterID
                else:
                    ballerzWeights[tempWeight] = rosterID

            for index, weight in enumerate(sorted(ringersWeights.keys(), reverse=True)):
                _aValues[index] = ringersWeights[weight]

            for index, weight in enumerate(sorted(ballerzWeights.keys(), reverse=True)):
                _aValues[index + len(ringersWeights)] = ballerzWeights[weight]

            return _aValues

        aValues = mapAValues()

        sortedIValues = sorted(list(iValues))

        for index, iValue in enumerate(sortedIValues):
            mappedIValues[iValue] = aValues[index]

        return mappedIValues
    # This method accepts a set of fully ripped stats, a rosterName, and a iValue times dictionary, and returns
    # a dictionary of ball held times to RosterID.
    def convertIValueTimesToRosterIDs(self,rosterName : str, rippedStats : dict,iValueTimes : dict):
        # Build iValues list
        allIValues = set(iValueTimes["InPlay"].keys()) | set(iValueTimes["OutOfPlay"].keys())
        allIValues.discard(0)
        allIValues = list(allIValues)
        # If there are less IValues than there are slots, that means the iValue list is incomplete and this
        # can't yet successfully calculate ball holding stats.
        if(len(allIValues) < rippedStats["GameStats"]["GameMode"]):
            return None

        # Build RosterID list
        rosterIDSlotDict = {}
        for slot,slotInfo in rippedStats["GameStats"]["SlotStats"].items():
            if(slotInfo["IsActive"] == 1):
                rosterIDSlotDict[slotInfo["RosterID"]] = slot

        # Generate iValueMap
        iValueMap = self.mapIValues(iValues=allIValues,rosterIDs=rosterIDSlotDict,rosterName=rosterName)

        ballHeldDict = {}
        for iValue,rosterID in iValueMap.items():
            ballHeldDict[rosterID]["InPlay"] = iValueTimes[iValue]["InPlay"]
            ballHeldDict[rosterID]["OutOfPlay"] = iValueTimes[iValue]["OutOfPlay"]

        return ballHeldDict

    #endregion === Game Tracking ===

    # These two addressSets deal with tracking and setting the players in the
    # player select menu for blacktop. PlayerCounterAddress keeps track
    # of the numbers of players currently selected, while each individual
    # slot tracks the id of a player. Get and Set methods are provided to print out
    # the currently loaded players, and to load a dict of players into the game.
    playerCounterAddress = [[0x0067634C,0x58],[0x00676E2C,0x0],[0x00678600,0x0],[0x00A91A70,0xB4],[0x00E99380,0x1BC]]
    slotActivatorAddressDict = {
        "Slot1" : 0xE99430,
        "Slot2" : 0xE99438,
        "Slot3" : 0xE99440,
        "Slot4" : 0xE99448,
        "Slot5" : 0xE99450,
        "Slot6" : 0xE99434,
        "Slot7" : 0xE9943C,
        "Slot8" : 0xE99444,
        "Slot9" : 0xE9944C,
        "Slot10" : 0xE99454
    }
    def getLoadedBlacktopPlayers(self):
        loadedPlayerDict = {
            "Slot1" : None,
            "Slot2" : None,
            "Slot3" : None,
            "Slot4" : None,
            "Slot5" : None,
            "Slot6" : None,
            "Slot7" : None,
            "Slot8" : None,
            "Slot9" : None,
            "Slot10" : None,
        }
        for key,value in self.slotActivatorAddressDict.items():
            rawValue = self.mem.read_int(self.module + value)
            rosterID = (rawValue - 30333580) / 484
            loadedPlayerDict[key] = int(rosterID)

        gameMode = self.getBlacktopMode()
        if(gameMode < 5):
            loadedPlayerDict["Slot5"] = None
            loadedPlayerDict["Slot10"] = None
        if(gameMode < 4):
            loadedPlayerDict["Slot4"] = None
            loadedPlayerDict["Slot9"] = None
        if (gameMode < 3):
            loadedPlayerDict["Slot3"] = None
            loadedPlayerDict["Slot8"] = None
        if (gameMode < 2):
            loadedPlayerDict["Slot2"] = None
            loadedPlayerDict["Slot7"] = None
        if (gameMode < 2):
            loadedPlayerDict["Slot1"] = None
            loadedPlayerDict["Slot6"] = None


        return loadedPlayerDict
    def loadBlacktopPlayers(self,playerSlotDict):
        playerCount = 0
        for key,value in playerSlotDict.items():
            if(value != None):
                playerCount += 1
                convertedVal = (value*484) + 30333580
                self.mem.write_int(self.module + self.slotActivatorAddressDict.get(key),convertedVal)
        self.mem.write_int(self.getPointerAddress(self.playerCounterAddress[0]),playerCount)




t = Tracker()
t.testAppConnection()
while True:
    print(t.testIfBallIsInPlay())
    time.sleep(0.5)