import pyautogui
import time
import os
from spritopia.common.paths import paths
from spritopia.common.logger import log


REDMC_WINDOW_NAME = "RED Modding Center"

# This class simply manages the automation of moving files between RedMC and the program.
class RedMC:

    # Simple init method initializes necessary tracking variables.
    def __init__(self):
        self.isRedMCOpen = False
        self.redMCWindow = None

    # Simply opens RedMC using pyautogui, and maximizes the window.
    def openRedMC(self):
        testWindows = pyautogui.getWindowsWithTitle(REDMC_WINDOW_NAME)
        if(len(testWindows) > 0):
            raise RedMCAlreadyOpenException


        os.startfile(paths["redMC"] / "RED_MC.exe")
        validWindows = []
        for i in range(10):
            validWindows = pyautogui.getWindowsWithTitle(REDMC_WINDOW_NAME)
            if(len(validWindows) == 1):
                self.redMCWindow = validWindows[0]
                break
            else:
                time.sleep(1)
        if(len(validWindows) != 1):
            raise FailedToOpenRedMCException(10)

        self.redMCWindow.maximize()
        self.redMCWindow.activate()
        self.isRedMCOpen = True

        log.debug("Opened RedMC")

    @staticmethod
    # Uses the open RedMC program to load the given rosterName.
    def loadRoster(rosterName):
        if (".ROS" not in rosterName):
            rosterName += ".ROS"
        fullRosterPath = str(paths["gameRosters"] / rosterName)
        if(not os.path.exists(fullRosterPath)):
            raise RosterDoesNotExistException(fullRosterPath)



        pyautogui.keyDown("ctrlleft")
        pyautogui.keyDown("o")
        pyautogui.keyUp("ctrlleft")
        pyautogui.keyUp("o")


        pyautogui.write(fullRosterPath)
        pyautogui.press("enter")

        log.debug(f"Loaded roster '{rosterName}' in RedMC")

    @staticmethod
    # Simply saves the currently loaded roster.
    def saveRoster():
        pyautogui.keyDown("ctrlleft")
        pyautogui.keyDown("s")
        pyautogui.keyUp("ctrlleft")
        pyautogui.keyUp("s")

        log.debug("Saved roster in RedMC")

    # Simply quits out of RedMC. THE FILE MUST BE SAVED BEFORE DOING THIS.
    def closeRedMC(self):
        pyautogui.press("altleft")
        pyautogui.press("up")
        pyautogui.press("up")
        pyautogui.press("enter")

        self.isRedMCOpen = False
        log.debug("Closed RedMC")

    @staticmethod
    # Uses the open RedMC program window to export the currently loaded Roster's
    # CSV files. Will always export to the Airlock CSV folder.
    def exportCSVs(rosterName):
        pyautogui.press("altleft")
        pyautogui.press("up")
        pyautogui.press("up")
        pyautogui.press("up")
        pyautogui.press("up")
        pyautogui.press("up")
        pyautogui.press("enter")

        pyautogui.press("up")
        pyautogui.write(str(paths["gameRosters"] / rosterName))
        pyautogui.press("tab")

        pyautogui.press("tab")
        pyautogui.press("tab")
        pyautogui.press("down")
        pyautogui.press("tab")
        pyautogui.press("tab")
        pyautogui.press("space")
        pyautogui.press("enter")
        pyautogui.press("tab")
        pyautogui.press("tab")
        pyautogui.press("space")

        log.debug(f"Exported all CSVs for roster '{rosterName}' from RedMC")

    @staticmethod
    # Uses the open RedMC program window to import the last exported CSV file set in
    # the target roster folder.
    def importCSVs(rosterName):
        pyautogui.press("altleft")
        pyautogui.press("up")
        pyautogui.press("up")
        pyautogui.press("up")
        pyautogui.press("up")
        pyautogui.press("enter")

        pyautogui.press("up")
        pyautogui.write(rosterName)
        pyautogui.press("tab")

        pyautogui.press("tab")
        pyautogui.press("tab")
        pyautogui.press("down")
        pyautogui.press("tab")
        pyautogui.press("tab")
        pyautogui.press("space")

        pyautogui.press("enter")
        pyautogui.press("tab")
        pyautogui.press("tab")
        pyautogui.press("space")

        log.debug(f"Imported all CSVs for roster '{rosterName}' to RedMC")

    @staticmethod
    # This method simply tests that RedMC is closed for timeoutTime amount of time.
    # It returns true once it's closed, and if timeoutTime elapses, returns false.
    def testIfRedMCClosed(timeoutTime=60):
        for i in range(timeoutTime):
            if (len(pyautogui.getWindowsWithTitle(REDMC_WINDOW_NAME)) > 0):
                time.sleep(0.5)
            else:
                return True

        return False


class RedMCException(TypeError):
    pass
class RedMCAlreadyOpenException(RedMCException):
    def __init__(self):
        super().__init__("Tried opening RedMC when the program is already open!")
class FailedToOpenRedMCException(RedMCException):
    def __init__(self,count):
        super().__init__("Could not open RedMC after trying " + str(count) + " times.")
class RosterDoesNotExistException(RedMCException):
    def __init__(self,rosterPath):
        super().__init__("Roster path does not exist: '" + rosterPath + "'.")



