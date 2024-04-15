import os
from pathlib import Path
import tkinter
from tkinter import simpledialog, filedialog
from spritopia.common.config import config

# Helper method for testing the validity of a given pathToValidate in different ways.
def validatePath(pathToValidate: Path,  # The path to actually attempt to validate.
                 subPathsToTest: list = None,  # A list of subpaths to test for RELATIVE to the pathToValidate
                 readAccess: bool = True, writeAccess: bool = True, execAccess: bool = True,
                 # Whether to test for certain accessibility
                 suppressErrors: bool = False  # Whether to suppress errors, and return True/False instead.
                 ):
    # Test that the path actually exists
    if (not pathToValidate.exists()):
        if(suppressErrors):
            return False
        else:
            raise ValueError(f"Path '{pathToValidate}' does not exist!")

    # Set up accessibility flag to be tested
    flags = 0
    if (not readAccess):
        flags |= os.R_OK
    if (not writeAccess):
        flags |= os.W_OK
    if (not execAccess):
        flags |= os.X_OK
    # Test accessibility of this path
    if (not os.access(str(pathToValidate), flags)):
        if (suppressErrors):
            return False
        else:
            raise PermissionError(f"Insufficient permissions for configured directory: {pathToValidate}")

    # Validate any subpaths provided
    if (subPathsToTest):
        for subPath in subPathsToTest:
            fullSubPath = pathToValidate / subPath
            if (not fullSubPath.exists()):
                if (suppressErrors):
                    return False
                else:
                    raise ValueError(f"File sub-structure for given path is invalid: {pathToValidate}")

    # Path is valid
    return True

# Helper method for asking the user to supply a path. User is given a prompt, and
# can either type in a path manually or use Windows Explorer to search for a path.
def getPathFromUser(message):
    root = tkinter.Tk()
    root.withdraw()  # Hide the main window

    # Helper class for having the user select a new path, with support for validation
    # of folder and pathsToTestFor
    class DirectoryDialog(simpledialog.Dialog):

        def __init__(self, parent, _message, **kwargs):
            self._message = message
            self.directory = ''
            self.e = None
            super().__init__(parent, **kwargs)

        def body(self, master):
            tkinter.Label(master, text=self._message).grid(row=0)
            self.e = tkinter.Entry(master)
            self.e.grid(row=1)
            tkinter.Button(master, text="Browse", command=self.browse).grid(row=1, column=1)

        def apply(self):
            self.directory = self.e.get()

        def browse(self):
            self.directory = filedialog.askdirectory()
            self.e.delete(0, 'end')
            self.e.insert('end', self.directory)

    d = DirectoryDialog(root, message)
    return d.directory

# Simple class to validate and store program paths.
class Paths:

    # init generates all paths necessary for the object.
    def __init__(self):
        self.allPaths = {}
        self.add("appData",Path(os.environ['APPDATA']))

    # Method for getting the path with the given name.
    def get(self,pathname):
        return self.__getitem__(pathname)
    def __getitem__(self, key):
        lowerPathname = key.lower()
        if(lowerPathname in self.allPaths.keys()):
            return self.allPaths[lowerPathname]["Path"]
    # Method for registering a new path with the given name, path, and options.
    def add(self,pathname,path,subPathsToTest : list = None,suppressErrors = False):
        if(pathname in self.allPaths.keys()):
            raise ValueError(f"Path name '{pathname}' already exists!")
        if(type(path) is not Path):
            path = Path(path)
        validatePath(pathToValidate=path,subPathsToTest=subPathsToTest,suppressErrors=suppressErrors)
        self.allPaths[pathname.lower()] = {"Path" : path}
    def __setitem__(self,key,value):
        self.add(pathname=key,path=value)


paths = Paths()

# Root path
thisFilePath = Path(__file__).resolve()
rootPath = thisFilePath.parent.parent.parent
paths["root"] = rootPath

# Config path
paths["config"] = paths["root"] / "config"

# Data path
paths["data"] = paths["root"] / "data"
paths["templates"] = paths["data"] / "templates"
paths["factions"] = paths["data"] / "factions"
paths["randGen"] = paths["data"] / "rand_gen"
paths["musicData"] = paths["data"] / "music"

# Registers the data folder given in the config in global paths
paths["saveFolder"] = config["paths"]["saveFolder"]
paths["logs"] = paths["saveFolder"] / "logs"
paths["backups"] = paths["saveFolder"] / "backups"
paths["rosterCSVs"] = paths["saveFolder"] / "roster_csvs"
paths["saveDBs"] = paths["saveFolder"] / "db"

# Registers the NBA2K13 game data and roaming folder in the config in global paths.
paths["gameInstall"] = config["paths"]["gameInstall"]
paths["gameRoaming"] = paths["appdata"] / "2K Sports/NBA 2K13"
paths["gameRosters"] = paths["gameRoaming"] / "Saves"

# Assets path
paths["assets"] = paths["root"] / "assets"
paths["graphics"] = paths["assets"] / "graphics"
paths["media"] = paths["assets"] / "media"
paths["localization"] = paths["assets"] / "localization"

# Tools path
paths["tools"] = paths["root"] / "tools"
paths["redMC"] = paths["tools"] / "RedMC"



