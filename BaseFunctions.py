import os
import datetime
import shutil
import tomlkit
import tkinter as tk
import random
import time
import re
import chardet
from pathlib import Path
import glob
import WeightedDict
from tkinter import simpledialog, filedialog


# region === Config and Pathing Setup ===

thisFile = os.path.realpath(__file__)
thisDirectory = os.path.dirname(thisFile)

with open(f"{thisDirectory}\\config.toml", "r") as f:
    config = tomlkit.parse(f.read())


# Simple class to validate and store program paths.
class Paths:

    # init generates all paths necessary for the object.
    def __init__(self):
        self.appdata = os.environ['APPDATA']

        self.root = thisDirectory

        # Path to the base working directory, ie where all program files and
        # data is stored.
        self.workDir = config["paths"]["workDirectory"]
        self.validatePath(self.workDir,createPath=True)
        # Logs folder
        self.logs = f"{self.workDir}\\Logs"
        self.validatePath(self.logs,createPath=True)
        # Backups folder
        self.backups = f"{self.workDir}\\Backups"
        self.validatePath(self.backups,createPath=True)
        # Rosters CSV folder
        self.rosterCSVs = f"{self.workDir}\\RostersCSVs"
        self.validatePath(self.rosterCSVs,createPath=True)
        # Path to data directory, for storing dbs
        self.databases = f"{self.workDir}\\Data"
        self.validatePath(self.databases,createPath=True)

        # Path to the GameData, or program data folder, used to store static data needed
        # to run the program.
        self.programData = f"{self.root}\\GameData"
        self.validatePath(self.programData)
        # Path to the templates folder
        self.templates = f"{self.programData}\\Templates"
        self.validatePath(self.templates)
        # Path to the graphics folder
        self.graphics = f"{self.programData}\\Graphics"
        self.validatePath(self.graphics)
        # Path to the media folder
        self.media = f"{self.programData}\\Media"
        self.validatePath(self.media)
        # Path to the random generation folder
        self.randGen = f"{self.programData}\\RandGen"
        self.validatePath(self.randGen)
        # Path to the factions data folder.
        self.factions = f"{self.programData}\\Factions"
        self.validatePath(self.factions)

        # Path to the RedMC install, which should ALWAYS be in root
        self.redMC = f"{self.root}\\RedMC"
        self.validatePath(self.redMC,subPathsToTest=["RED_MC.exe"])

        # Path to the actual NBA 2k game install folder
        self.gameInstall = config["paths"]["gameInstall"]
        while(not self.validatePath(self.gameInstall,subPathsToTest=["nba2k13.exe"],suppressErrors=True)):
            self.gameInstall = self.getPathFromUser("Invalid game path detected. Please provide a path to your NBA 2K13 install (game) folder.")
        config["paths"]["gameInstall"] = self.gameInstall

        # Path to the 2k game data folder, with rosters, settings, etc
        self.gameRoaming = f"{self.appdata}\\2K Sports\\NBA 2K13"
        self.validatePath(self.gameRoaming,subPathsToTest=["Saves\\Settings.STG"],execAccess=False)
        # Path to folder where 2k Rosters are stored.
        self.rosters = f"{self.gameRoaming}\\Saves"

        # Finally, write the updated TOML back to the file, in case changes were made.
        with open(f'{thisDirectory}\\config.toml', 'w') as f:
            f.write(tomlkit.dumps(config))

    @staticmethod
    # Helper method for testing the validity of a given pathToValidate in different ways.
    def validatePath(pathToValidate : str,  # The path to actually attempt to validate.
                     subPathsToTest : list = None,  # A list of subpaths to test for RELATIVE to the pathToValidate
                     readAccess : bool = True, writeAccess : bool = True, execAccess : bool = True,  # Whether to test for certain accessibilities
                     createPath : bool = False,  # Whether to attempt to create the path if it's missing.
                     suppressErrors : bool = False  # Whether to suppress errors, and return True/False instead.
                     ):

        # Create path, if missing, if specified
        if(createPath):
            os.makedirs(pathToValidate, exist_ok=True)

        # Set up accessibility flag to be tested
        flags = 0
        if (not readAccess):
            flags |= os.R_OK
        if (not writeAccess):
            flags |= os.W_OK
        if (not execAccess):
            flags |= os.X_OK

        # Test accessibility of this path
        if (not os.access(pathToValidate, flags)):
            if(suppressErrors):
                return False
            else:
                raise PermissionError(f"Insufficient permissions for configured directory: {pathToValidate}")

        # Validate any subpaths provided
        if(subPathsToTest is not None):
            if(len(subPathsToTest) > 0):
                for subPath in subPathsToTest:
                    if(not os.path.exists(f"{pathToValidate}\\{subPath}")):
                        if(suppressErrors):
                            return False
                        else:
                            raise ValueError(f"File sub-structure for given path is invalid: {pathToValidate}")
        # Path is valid
        return True

    @staticmethod
    # Helper method for asking the user to supply a path. User is given a prompt, and
    # can either type in a path manually or use Windows Explorer to search for a path.
    def getPathFromUser(message):
        root = tk.Tk()
        root.withdraw()  # Hide the main window

        # Helper class for having the user select a new path, with support for validation
        # of folder and pathsToTestFor
        class DirectoryDialog(simpledialog.Dialog):

            def __init__(self, parent, message, **kwargs):
                self.message = message
                self.directory = ''
                super().__init__(parent, **kwargs)

            def body(self, master):
                tk.Label(master, text=self.message).grid(row=0)
                self.e = tk.Entry(master)
                self.e.grid(row=1)
                tk.Button(master, text="Browse", command=self.browse).grid(row=1, column=1)

            def apply(self):
                self.directory = self.e.get()

            def browse(self):
                self.directory = filedialog.askdirectory()
                self.e.delete(0, 'end')
                self.e.insert('end', self.directory)

        d = DirectoryDialog(root, message)
        return d.directory
paths = Paths()


# endregion === Config and Pathing Setup ===



#region === Miscellaneous Functions ===

# Simple backup management function. Will attempt to backup the file given by filePath
# to the directory backupPath, keeping at maximum backupLimit backups at any time.
def backup(filePath, backupPath, backupLimit=10):
    # Validate and create backup directory if missing
    Paths.validatePath(pathToValidate = backupPath,createPath = True)

    # Get base filename and extension here
    baseName = os.path.basename(filePath)
    fileName,fileExtension = os.path.splitext(baseName)

    # Get list of existing backup files, and sort by creation date
    allFilesInBackupDir = os.listdir(backupPath)
    existingBackups = [f for f in allFilesInBackupDir if f.startswith(f"{fileName}_") and f.endswith(fileExtension)]
    existingBackups = sorted(existingBackups, key=lambda f: os.path.getmtime(os.path.join(backupPath, f)))

    # If we have reached the backup limit, delete the oldest file
    if len(existingBackups) >= backupLimit:
        os.remove(f"{backupPath}\\{existingBackups[0]}")

    # Create a backup
    dt = datetime.datetime.now()
    timestamp = dt.strftime("%m-%d-%Y--%H-%M-%S")
    backupFileName = f"{fileName}_{timestamp}{fileExtension}"
    shutil.copy(filePath, f"{backupPath}\\{backupFileName}")

# This method simply returns true if the string is a number. Includes decimals and signs.
def isNumber(testString):
    try:
        float(testString)
        return True
    except ValueError:
        return False

# Simply returns the average of a list of numbers.
def averageOfList(thisList):
    sumOfList = 0
    counter = 0
    for item in thisList:
        if(str(type(item)) != "<class 'int'>"):
            continue
        else:
            sumOfList += item
            counter += 1
    return sumOfList / counter

# This function returns a string starting at the given index, and removes
# everything before that.
def getStringAt(string, index):
    counter = -1
    value = ''
    for x in string:
        counter += 1
        if index <= counter:
            value += x
    return value

# Given a character or list of characters, this function counts how many times
# they collectively appear in a string.
def countFreq(characters, string):
    charList = str(characters)
    counter = 0
    for x in charList:
        for y in string:
            if x == y:
                counter += 1
    return counter

# This function finds and returns an array of all numbers missing from a sequential list.
# For example, in a list of [1,2,4,5,7] this function would return [3,6]
def find_missing(thisList):
    return [x for x in range(thisList[0], thisList[-1]+1) if x not in thisList]

# Cheaty way to get a dictionary KEY from a VALUE.
def getKeyFromValue(dictionary, targetValue):
    for key, value in dictionary.items():
        if (value == targetValue):
            return key
    raise ValueError(f"Value does not exist in the dictionary: '{targetValue}'")


# This method simply selects a value or values randomly from a given file of words.
# Each word in this file should be separated by newlines - one selection per line.
# -filePath can be a string containing a single file path, or an array of file paths.
# -selectionCount specifies how many random values from the file's you'd like to gen.
# -hatPick means that subsequent random values will never be the same as already picked values.
# -rStringProcessing allows for processing results as rStrings (see below)
def selectRandomFromList(filePath, selectionCount : int = 1, hatPick : bool = False, rStringProcessing : bool = False):
    if(type(filePath) is str):
        filePath = [filePath]
    elif(type(filePath) is not list):
        raise FileNotFoundError(filePath)

    allPotentialValues = []
    for thisFilePath in filePath:
        with open(thisFilePath,"rb") as f:
            fileResult = chardet.detect(f.read())

        with open(thisFilePath,"r",encoding=fileResult["encoding"]) as thisFile:
            allPotentialValues += [line.strip() for line in thisFile]

    returnArray = []
    if(hatPick):
        random.shuffle(allPotentialValues)
        for i in range(min(selectionCount,len(allPotentialValues))):
            returnArray.append(allPotentialValues[i])
    else:
        for i in range(selectionCount):
            returnArray.append(random.choice(allPotentialValues))

    # If rStringProcessing is on, we process the results as rStrings.
    if(rStringProcessing):
        tempArray = []
        for result in returnArray:
            tempArray.append(rStringProcess(result,recursiveProcessing=True))
        returnArray = tempArray

    return returnArray

# This method simply processed an "rString", a simple string randomization format I've designed for extended
# ease of use with randomization. If recursive processing is on, any options picked from word lists will ALSO
# be randomized.
# {choice1,choice2,choice3} is an adLib operator, and would process randomly to select one of the three choices only.
# [path/to/other/wordlist] is a randomList selection operator, and would attempt to fill that spot with a single entry from the randList path.
def rStringProcess(rString,recursiveProcessing : bool = True):

    # Locate all occurrences of {option1, option2, ...} in the string
    options = re.findall('{([^}]*)}', rString)
    # Replace each occurrence with a random choice
    for option in options:
        choicesList = option.split(',')
        choices = WeightedDict.WeightedDict()
        # Test to see if any choices have weights.
        for choice in choicesList:
            if("::" in choice):
                weight = int(choice.split("::")[1])
                choice = choice.split("::")[0]
            else:
                weight = 1
            choices.add(choice,weight)
        rString = rString.replace('{' + option + '}', choices.pull())


    # Locate all occurrences of [path/to/file] in the string
    options = re.findall('\[([^]]*)]', rString)
    # Assume each option is a file path to a wordlist, recursively gen from that list
    for option in options:
        pickedOption = selectRandomFromList(filePath = f"{paths.randGen}\\{option}",rStringProcessing=recursiveProcessing)[0]
        rString = rString.replace(f"[{option}]",pickedOption)

    return rString



#endregion === Miscellaneous Functions ===
