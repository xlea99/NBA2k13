import _tkinter
from tkinter import *
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import vlc
import tkinter.font as tkFont
import customtkinter
import os
os.add_dll_directory(r'C:\Program Files\VideoLAN\VLC')
import pygame
from PIL import ImageTk,Image
import Archetypes
import Player
import Tracker
import DataStorage
import BaseFunctions as b
import Helpers as h
import threading
import random
import WeightedDict



ARCHETYPE_OPTIONS = [
            "Slayer",
            "Vigilante",
            "Medic",
            "Guardian",
            "Engineer",
            "Director"]
HEIGHT_OPTIONS = [
            "5'3",
            "5'4",
            "5'5",
            "5'6",
            "5'7",
            "5'8",
            "5'9",
            "5'10",
            "5'11",
            "6'0",
            "6'1",
            "6'2",
            "6'3",
            "6'4",
            "6'5",
            "6'6",
            "6'7",
            "6'8",
            "6'9",
            "6'10",
            "6'11",
            "7'0",
            "7'1",
            "7'2",
            "7'3",
            "7'4",
            "7'5",
            "7'6"
        ]
STAT_OPTIONS = ["Stats", "Stat Totals", "Bio"]

INTRODUCTIONS = ["\\W1.ogg","\\W2.ogg","\\W3.ogg","\\W4.ogg","\\W5.ogg","\\W6.ogg","\\W7.ogg","\\W8.ogg","\\W9.ogg","\\W10.ogg","\\W11.ogg","\\W12.ogg","\\W13.ogg"]

# These are the basic stats that will be pulled whenever we want to generate a stats table.
TABLE_STATS = ["SpriteID","IsActive","Wins","Points","DefensiveRebounds","OffensiveRebounds","AssistCount","Steals","Blocks","Turnovers","InsidesMade","InsidesAttempted","ThreesMade","ThreesAttempted"]

class GUI:

    def __init__(self,openRoot=True):
        customtkinter.set_appearance_mode("System")  # Modes: system (default), light, dark
        customtkinter.set_default_color_theme("green")  # Themes: blue (default), dark-blue, green

        pygame.mixer.init()

        self.root = None
        if(openRoot):
            self.openRoot()

        self.nba2k_Logo = ImageTk.PhotoImage(Image.open(f"{b.paths.graphics}\\2kReader.png"))

        self.outgoingChanges = []
        self.incomingChanges = []

        self.previousScreen = None
        self.currentScreen = None

        # Global media player to avoid headaches.
        self.mediaPlayer = None

        self.saveButton = customtkinter.CTkButton(self.root, text="SAVE", command=self.saveData, font=customtkinter.CTkFont(family="Bahnschrift SemiBold", size=10), fg_color="#535454", width=10,text_color="grey")
        self.saveLabel = customtkinter.CTkLabel(self.root, text="", font=customtkinter.CTkFont(family="Bahnschrift SemiBold", size=10), text_color="yellow")

        self.playerbaseOptions = None

        # Simply used to not duplicate instantiation of statripper or data storage object.
        self.statsRipper = StatsRipper.StatsRipper()
        self.globalDataStorage = DataStorage.DataStorage()

        # This tries to store information about whether or not a game is currently
        # running.
        self.isGameActive = False
        # This stores information on whether or not we've saved a single game's data.
        self.isGameSaved = False
        # This stores information on whether or not we've added a coin to Alex's team.
        self.isCoinGiven = False
        # Stores whether a game is won or not.
        self.isGameWon = False
        # Stores the currently running

        # This stores whether or not a loaded Roster has been stored in game, after
        # going to a screen like Create a Player.
        self.hasSavedRoster = False
        # Stores the roster that was last open by 2k.
        self.lastOpenRoster = None

        # Various filters for tableStats.
        self.tableStats_RosterFilter = "Premier.ROS"
        self.tableStats_GameCutoff = None
        self.tableStats_GameMin = None
        self.tableStats_ArchetypeFilter = None
        self.tableStats_TechnicianFilter = None

        self.currentJerseyDict = {"alexSlayerJersey" : None,
                             "alexVigilanteJersey" : None,
                             "alexMedicJersey" : None,
                             "alexGuardianJersey" : None,
                             "alexEngineerJersey" : None,
                             "alexDirectorJersey" : None,
                             "dannySlayerJersey" : None,
                             "dannyVigilanteJersey" : None,
                             "dannyMedicJersey" : None,
                             "dannyGuardianJersey" : None,
                             "dannyEngineerJersey" : None,
                             "dannyDirectorJersey" : None,
                             }
        self.newJerseyName = None

        # =================================================================
        # ================Player Search Members============================
        # =================================================================
        # The actual list box (Search Box) we will use to view players in.
        self.searchBox = Listbox(self.root, width=25, font=tkFont.Font(family="Bahnschrift SemiBold", size=15))
        # This member stores an ordered list of SpriteIDs as they currently
        # exist in the search menu.
        self.playerSearchIDs = []
        # This members stores an ordered list of names, corresponding to
        # self.playerSearchIDs, used to display individual players in
        # the search list.
        self.playerSearchNames = []
        # Stores the last picked playerID in the search menu.
        self.lastPickedPlayerID = None
        # Stores any filters applied to the search menu.
        self.searchBoxFilters = {}
        self.searchMenu_ResetFilters()


        # =================================================================
        # ================Pickup Menu Members==============================
        # =================================================================
        self.pickerRoster = None
        self.isOnPlayerPicker = False
        self.alexPicks = []
        self.dannyPicks = []
        self.alexFrame = customtkinter.CTkFrame(self.root)
        self.alexPickOneLabel = customtkinter.CTkLabel(self.alexFrame,text="---", font=customtkinter.CTkFont(family="Bahnschrift SemiBold", size=25),justify="center")
        self.alexPickTwoLabel = customtkinter.CTkLabel(self.alexFrame, text="---", font=customtkinter.CTkFont(family="Bahnschrift SemiBold", size=25),justify="center")
        self.alexPickThreeLabel = customtkinter.CTkLabel(self.alexFrame, text="---", font=customtkinter.CTkFont(family="Bahnschrift SemiBold", size=25),justify="center")
        self.alexPickFourLabel = customtkinter.CTkLabel(self.alexFrame, text="---", font=customtkinter.CTkFont(family="Bahnschrift SemiBold", size=25),justify="center")
        self.alexPickFiveLabel = customtkinter.CTkLabel(self.alexFrame, text="---", font=customtkinter.CTkFont(family="Bahnschrift SemiBold", size=25),justify="center")
        self.dannyFrame = customtkinter.CTkFrame(self.root)
        self.dannyPickOneLabel = customtkinter.CTkLabel(self.dannyFrame, text="---", font=customtkinter.CTkFont(family="Bahnschrift SemiBold", size=25),justify="center")
        self.dannyPickTwoLabel = customtkinter.CTkLabel(self.dannyFrame, text="---", font=customtkinter.CTkFont(family="Bahnschrift SemiBold", size=25),justify="center")
        self.dannyPickThreeLabel = customtkinter.CTkLabel(self.dannyFrame, text="---", font=customtkinter.CTkFont(family="Bahnschrift SemiBold", size=25),justify="center")
        self.dannyPickFourLabel = customtkinter.CTkLabel(self.dannyFrame, text="---", font=customtkinter.CTkFont(family="Bahnschrift SemiBold", size=25),justify="center")
        self.dannyPickFiveLabel = customtkinter.CTkLabel(self.dannyFrame, text="---", font=customtkinter.CTkFont(family="Bahnschrift SemiBold", size=25),justify="center")

    # Simply opens the GUI CTkinter root.
    def openRoot(self):
        self.root = customtkinter.CTk()
        self.root.title("Spritopia Presents:")
        self.root.geometry("1920x1080")
        self.root.attributes('-fullscreen', True)
        self.root.iconbitmap(f"{b.paths.graphics}\\sprite.ico")

    def startupScreen(self):
        previewMovieLabel = Label(self.root)
        previewMovieLabel.place(x=0,y=0,relwidth=1, relheight=1)
        vlcInstance = vlc.Instance("-q")
        self.mediaPlayer = vlcInstance.media_player_new(f"{b.paths.media}\\NormalVid.mp4")

        # Set the video output window
        self.mediaPlayer.set_hwnd(previewMovieLabel.winfo_id())

        # Start playing the video and audio
        self.mediaPlayer.play()

        fontSize = 60

        startButton = customtkinter.CTkButton(self.root, text="Start", command=self.goToMainMenu, font=customtkinter.CTkFont(family="Bahnschrift SemiBold", size=fontSize), fg_color="#2eb217")
        startButton.pack(side=BOTTOM, pady=150)

    # This method takes us to the main menu from whatever screen we're
    # currently on.
    def goToMainMenu(self):
        self.wipeScreen("MainMenu")

        pygame.mixer.music.stop()

        pygame.mixer.music.load(f"{b.paths.media}\\{random.choice(INTRODUCTIONS)}")
        pygame.mixer.music.play(loops=0)
        pygame.mixer.music.set_volume(0.075)

        pygame.mixer.music.queue(f"{b.paths.media}\\Title.ogg")




        nba2k_Label = Label(self.root, image=self.nba2k_Logo)
        nba2k_Label.photo = self.nba2k_Logo
        nba2k_Label.grid(column=0,row=0,columnspan=3)

        self.saveButton.place(x=20,y=1020)
        self.saveLabel.place(x=80, y=1020)

        fontSize = 60

        playButton = customtkinter.CTkButton(self.root, text="Play", command=self.goToPlayMenu, font=customtkinter.CTkFont(family="Bahnschrift SemiBold", size=fontSize), fg_color="#2eb217")
        playButton.grid(column=1,row=1,padx=10, pady=30)

        capMenuButton = customtkinter.CTkButton(self.root, text="Create a Player", command=self.goToCAPMenu, font=customtkinter.CTkFont(family="Bahnschrift SemiBold", size=fontSize), fg_color="#2eb217")
        capMenuButton.grid(column=1,row=2,padx=10, pady=30)

        searchButton = customtkinter.CTkButton(self.root, text='Search', command=self.goToSearchMenu, font=customtkinter.CTkFont(family="Bahnschrift SemiBold", size=fontSize), fg_color="#2eb217")
        searchButton.grid(column=1,row=3,padx=10, pady=30)

        settingsButton = customtkinter.CTkButton(self.root, text='Settings', command=self.goToSettingsMenu, font=customtkinter.CTkFont(family="Bahnschrift SemiBold", size=fontSize), fg_color="#2eb217")
        settingsButton.grid(column=1,row=4,padx=10,pady=30)

        genStatReportButton = customtkinter.CTkButton(self.root, text='Generate Stats Report', command=self.goToGenStatReportMenu, font=customtkinter.CTkFont(family="Bahnschrift SemiBold", size=fontSize), fg_color="#2eb217")
        genStatReportButton.grid(column=1,row=5,padx=10, pady=30)

        exitButton = customtkinter.CTkButton(self.root, text="Quit", command=self.root.destroy, font=customtkinter.CTkFont(family="Bahnschrift SemiBold", size=fontSize), fg_color="#2eb217")
        exitButton.grid(column=1, row=6, padx=10, pady=30)

    # Settings Menus
    def goToSettingsMenu(self):

        self.wipeScreen("SettingsMenu")

        self.root.geometry("345x400+650+250")


        nba2k_Label = Label(self.root, image=self.nba2k_Logo)
        nba2k_Label.photo = self.nba2k_Logo
        nba2k_Label.grid(column=0, row=0, columnspan=3)

        fontSize = 60

        jerseyMenuButton = customtkinter.CTkButton(self.root, text="Jerseys", command=self.goToJerseysMenu, font=customtkinter.CTkFont(family="Bahnschrift SemiBold", size=fontSize), fg_color="#2eb217")
        jerseyMenuButton.grid(column=1,row=1,padx=10, pady=30)

        mainMenuButton = customtkinter.CTkButton(self.root, text="Main Menu", command=self.goToMainMenu,font=customtkinter.CTkFont(family="Bahnschrift SemiBold", size=fontSize),fg_color="#2eb217")
        mainMenuButton.grid(column=1,row=2,padx=10, pady=30)
    # TODO :(
    def goToJerseysMenu(self):

        self.wipeScreen("SettingsMenu")

        self.root.geometry("345x400+650+250")

        nba2k_Label = Label(self.root, image=self.nba2k_Logo)
        nba2k_Label.photo = self.nba2k_Logo
        nba2k_Label.grid(column=0, row=0, columnspan=3)

        technicianOptions = ["Alex","Danny"]
        technicianFilterVar = StringVar(None)
        technicianFilterVar.set("Alex")
        archetypeOptions = ["Slayer","Vigilante","Guardian","Medic","Engineer","Director"]
        archetypeFilterVar = StringVar(None)
        archetypeFilterVar.set("Slayer")
        rosterOptions = self.globalDataStorage.csv_GetSavedRosterList()
        rosterFilterVar = StringVar(None)
        rosterFilterVar.set("Premier")


        # Method for quickly scraping all jersey cfg info
        # TODO STILL BROKEN!
        def readCurrentJerseyDict():
            configPath = f"{b.paths.rosterCSVs}\\{rosterFilterVar.get()}\\settings.cfg"
            # These variables control what jersey images are shown in the Jersey selection screen.
            self.currentJerseyDict = {"alexSlayerJersey": b.readConfigValue("alexSlayerJersey",configFilePath=configPath),
                                      "alexVigilanteJersey": b.readConfigValue("alexVigilanteJersey",configFilePath=configPath),
                                      "alexMedicJersey": b.readConfigValue("alexMedicJersey",configFilePath=configPath),
                                      "alexGuardianJersey": b.readConfigValue("alexGuardianJersey",configFilePath=configPath),
                                      "alexEngineerJersey": b.readConfigValue("alexEngineerJersey",configFilePath=configPath),
                                      "alexDirectorJersey": b.readConfigValue("alexDirectorJersey",configFilePath=configPath),
                                      "dannySlayerJersey": b.readConfigValue("dannySlayerJersey",configFilePath=configPath),
                                      "dannyVigilanteJersey": b.readConfigValue("dannyVigilanteJersey",configFilePath=configPath),
                                      "dannyMedicJersey": b.readConfigValue("dannyMedicJersey",configFilePath=configPath),
                                      "dannyGuardianJersey": b.readConfigValue("dannyGuardianJersey",configFilePath=configPath),
                                      "dannyEngineerJersey": b.readConfigValue("dannyEngineerJersey",configFilePath=configPath),
                                      "dannyDirectorJersey": b.readConfigValue("dannyDirectorJersey",configFilePath=configPath),
                                      }
        readCurrentJerseyDict()

        currentJerseyLabel = Label(self.root)
        currentJerseyLabel.place(x=150,y=300)
        currentJerseyName = customtkinter.CTkLabel(self.root, text="BobcatsClassicHomeII",font=customtkinter.CTkFont(family="Bahnschrift SemiBold", size=30))
        currentJerseyName.place(x=150, y=650)

        selectedJerseyLabel = Label(self.root)
        selectedJerseyLabel.place(x=1350,y=300)
        selectedJerseyName = customtkinter.CTkLabel(self.root, text="BullsHome",font=customtkinter.CTkFont(family="Bahnschrift SemiBold", size=30))
        selectedJerseyName.place(x=1350, y=650)
        selectedJerseyVar = StringVar(None)
        selectedJerseyVar.set("GrizzliesAway")
        # This method will update both the current and selected jersey images with the correct images based on new selections.
        def updateJerseyImages():
            currentJerseyImage = ImageTk.PhotoImage(Image.open(f"{b.paths.graphics}\\Jerseys\\{self.currentJerseyDict[technicianFilterVar.get().lower() + archetypeFilterVar.get() + 'Jersey']}.PNG" ))
            selectedJerseyImage = ImageTk.PhotoImage(Image.open(f"{b.paths.graphics}\\Jerseys\\{selectedJerseyVar.get()}.PNG"))
            currentJerseyLabel.configure(image=currentJerseyImage)
            currentJerseyLabel.image = currentJerseyImage
            selectedJerseyLabel.configure(image=selectedJerseyImage)
            selectedJerseyLabel.image = selectedJerseyImage

            currentJerseyName.configure(text=self.currentJerseyDict.get(technicianFilterVar.get().lower() + archetypeFilterVar.get() + "Jersey"))
            selectedJerseyName.configure(text = selectedJerseyVar.get())
        updateJerseyImages()

        archetypeMenu = OptionMenu(self.root, archetypeFilterVar,command=lambda x: updateJerseyImages(), *archetypeOptions)
        archetypeMenu.place(x=300,y=855)
        archetypeMenuConfig = self.root.nametowidget(archetypeMenu.menuname)
        archetypeMenuConfig.config(font=tkFont.Font(family='Helvetica', size=25))
        archetypeMenu.config(bg="#36393e", fg="WHITE", highlightthickness=0, font=tkFont.Font(family='Helvetica', size=25))
        archetypeMenu["menu"].config(bg="#36393e", fg="WHITE")
        technicianMenu = OptionMenu(self.root, technicianFilterVar,command=lambda x: updateJerseyImages(), *technicianOptions)
        technicianMenu.place(x=300,y=915)
        technicianMenuConfig = self.root.nametowidget(technicianMenu.menuname)
        technicianMenuConfig.config(font=tkFont.Font(family='Helvetica', size=25))
        technicianMenu.config(bg="#36393e", fg="WHITE", highlightthickness=0, font=tkFont.Font(family='Helvetica', size=25))
        technicianMenu["menu"].config(bg="#36393e", fg="WHITE")
        rosterMenu = OptionMenu(self.root, rosterFilterVar,command=lambda x: updateJerseyImages(), *rosterOptions)
        rosterMenu.place(x=300,y=975)
        rosterMenuConfig = self.root.nametowidget(rosterMenu.menuname)
        rosterMenuConfig.config(font=tkFont.Font(family='Helvetica', size=25))
        rosterMenu.config(bg="#36393e", fg="WHITE", highlightthickness=0, font=tkFont.Font(family='Helvetica', size=25))
        rosterMenu["menu"].config(bg="#36393e", fg="WHITE")


        # This simple method just updates the selectedJerseyVar with whatever is next (1) or previous (-1) in the dictionary.
        def cycleJersey(direction=1):
            tempList = list(DataStorage.JERSEY_DICT)
            targetIndex = tempList.index(selectedJerseyVar.get()) + direction
            if(targetIndex == len(tempList)):
                targetIndex = 0
            selectedJerseyVar.set(tempList[targetIndex])
            updateJerseyImages()
        previousJerseyButton = customtkinter.CTkButton(self.root, text="<",command=lambda: cycleJersey(-1), font=customtkinter.CTkFont(family="Bahnschrift SemiBold", size=30),fg_color="#2eb217")
        previousJerseyButton.place(x=1150,y=400)

        previous5JerseysButton = customtkinter.CTkButton(self.root, text="<<",command=lambda: cycleJersey(-5), font=customtkinter.CTkFont(family="Bahnschrift SemiBold", size=30),fg_color="#2eb217")
        previous5JerseysButton.place(x=1150,y=475)

        previous10JerseysButton = customtkinter.CTkButton(self.root, text="<<<",command=lambda: cycleJersey(-10), font=customtkinter.CTkFont(family="Bahnschrift SemiBold", size=30),fg_color="#2eb217")
        previous10JerseysButton.place(x=1150,y=550)


        nextJerseyButton = customtkinter.CTkButton(self.root, text=">",command=lambda: cycleJersey(1), font=customtkinter.CTkFont(family="Bahnschrift SemiBold", size=30),fg_color="#2eb217")
        nextJerseyButton.place(x=1760,y=400)

        next5JerseysButton = customtkinter.CTkButton(self.root, text=">>",command=lambda: cycleJersey(5), font=customtkinter.CTkFont(family="Bahnschrift SemiBold", size=30),fg_color="#2eb217")
        next5JerseysButton.place(x=1760,y=475)

        next10JerseysButton = customtkinter.CTkButton(self.root, text=">>>",command=lambda: cycleJersey(10), font=customtkinter.CTkFont(family="Bahnschrift SemiBold", size=30),fg_color="#2eb217")
        next10JerseysButton.place(x=1760,y=550)

        # Simply sets the jersey for the archetype/technician combo, and then updates the images/text.
        # This commits all changes in the config to an outgoing change on Premier roster.
        # TODO add support for other rosters, revert changes, etc.
        # TODO hehe, you guessed it. BROKEN!
        def setNewJersey():
            currentRosterName = rosterFilterVar.get()
            targetParameter = technicianFilterVar.get().lower() + archetypeFilterVar.get() + "Jersey"
            b.setConfigValue(parameterName=targetParameter,parameterValue=selectedJerseyVar.get(),configFilePath=f"{b.paths.rosterCSVs}\\{currentRosterName}\\settings.cfg")
            self.currentJerseyDict[targetParameter] = selectedJerseyVar.get()
            self.globalDataStorage.csv_UpdateAllJerseys(currentRosterName)
            self.outgoingChanges.append(currentRosterName)
            updateJerseyImages()
        updateButton = customtkinter.CTkButton(self.root, text="Update",command=lambda: setNewJersey(),font=customtkinter.CTkFont(family="Bahnschrift SemiBold", size=50),fg_color="#2eb217")
        updateButton.place(x=1440,y=800)

        mainMenuButton = customtkinter.CTkButton(self.root, text="Main Menu", command=self.goToMainMenu,font=customtkinter.CTkFont(family="Bahnschrift SemiBold", size=30),fg_color="#2eb217")
        mainMenuButton.place(x=850,y=915)


    # Play Menus
    def goToPlayMenu(self):

        self.wipeScreen("ModesMenu")

        self.root.geometry("345x400+650+250")

        nba2k_Label = Label(self.root, image=self.nba2k_Logo)
        nba2k_Label.photo = self.nba2k_Logo
        nba2k_Label.grid(column=0, row=0, columnspan=3)

        fontSize = 60

        twoKButton = customtkinter.CTkButton(self.root, text="2k13", command=self.open_2k13, font=customtkinter.CTkFont(family="Bahnschrift SemiBold", size=fontSize), fg_color="#2eb217")
        twoKButton.grid(column=1,row=1,padx=10, pady=30)

        premierButton = customtkinter.CTkButton(self.root, text="Premier", command=lambda: self.goToPickerMenu("Premier"), font=customtkinter.CTkFont(family="Bahnschrift SemiBold", size=fontSize), fg_color="#2eb217")
        premierButton.grid(column=1,row=2,padx=10, pady=30)

        wildButton = customtkinter.CTkButton(self.root, text="Wild", command=lambda: self.goToPickerMenu("Wild"),font=customtkinter.CTkFont(family="Bahnschrift SemiBold", size=fontSize), fg_color="#2eb217")
        wildButton.grid(column=1,row=3,padx=10, pady=30)

        leagueButton = customtkinter.CTkButton(self.root, text="League", command=lambda: self.goToPickerMenu("Wild"),font=customtkinter.CTkFont(family="Bahnschrift SemiBold", size=fontSize), fg_color="#2eb217")
        leagueButton.grid(column=1,row=4,padx=10, pady=30)

        mainMenuButton = customtkinter.CTkButton(self.root, text="Main Menu", command=self.goToMainMenu,font=customtkinter.CTkFont(family="Bahnschrift SemiBold", size=fontSize), fg_color="#2eb217")
        mainMenuButton.grid(column=1,row=5,padx=10, pady=30)
    def goToPickerMenu(self,rosterName):
        self.wipeScreen("PickerMenu|" + str(rosterName))

        self.isOnPlayerPicker = True
        self.pickerRoster = rosterName
        self.root.geometry("345x400+650+250")

        nba2k_Label = Label(self.root, image=self.nba2k_Logo)
        nba2k_Label.photo = self.nba2k_Logo
        nba2k_Label.grid(column=0, row=0, columnspan=3)

        fontSize = 30
        fontSizeAlt = 45
        fontSizeEntry = 25

        FILTER_OPTIONS = ["Any","Slayer","Vigilante","Medic","Guardian","Engineer","Director"]

        mode = StringVar(None)
        mode.set("4v4")
        MODE_OPTIONS = ["1v1","2v2","3v3","4v4","5v5"]


        self.alexFrame.place(x=1400, y=150, height=635, width=450)
        self.dannyFrame.place(x=65, y=150, height=635, width=450)



        selectionFrame = customtkinter.CTkFrame(self.root)
        selectionFrame.place(x=600, y=100, height=700, width=710)

        alexLabel = customtkinter.CTkLabel(self.root, text="ALEX",font=customtkinter.CTkFont(family="Bahnschrift SemiBold", size=fontSize))
        alexLabel.place(x=1550, y=100)

        dannyLabel = customtkinter.CTkLabel(self.root, text="DANNY",font=customtkinter.CTkFont(family="Bahnschrift SemiBold", size=fontSize))
        dannyLabel.place(x=215, y=100)

        spacerAlexLabel = customtkinter.CTkLabel(self.alexFrame, text="==============================",font=customtkinter.CTkFont(family="Bahnschrift SemiBold", size=24))
        spacerAlexLabel.grid(column=0, row=0, columnspan=3)



        spacerDannyLabel = customtkinter.CTkLabel(self.dannyFrame, text="==============================",font=customtkinter.CTkFont(family="Bahnschrift SemiBold", size=24))
        spacerDannyLabel.grid(column=0, row=0, columnspan=3)


        mainMenuButton = customtkinter.CTkButton(self.root, text="Main Menu", command=self.goToMainMenu,font=customtkinter.CTkFont(family="Bahnschrift SemiBold", size=30), fg_color="#2eb217")
        mainMenuButton.place(x=835, y=1000)

        if(rosterName == "Wild"):
            self.playerbaseOptions = h.getDictOfPlayerNames(dataStorageObject=self.globalDataStorage)
        else:
            self.playerbaseOptions = h.getDictOfPlayerNames("Premier",dataStorageObject=self.globalDataStorage)

        searchLabel = customtkinter.CTkLabel(selectionFrame, text="Select a Player",font=customtkinter.CTkFont(family="Bahnschrift SemiBold", size=fontSizeAlt))
        searchLabel.grid(column=0,row=1, padx=5, pady=10, columnspan=4)

        selectionResult = StringVar(None)
        searchEntry = customtkinter.CTkEntry(selectionFrame, textvariable=selectionResult, width=400, font=customtkinter.CTkFont(family="Bahnschrift", size=fontSizeEntry))
        searchEntry.grid(column=1,row=2, padx=5, pady=10)

        addToDannyButton = customtkinter.CTkButton(selectionFrame, text="< Add", command=lambda: self.drawAndUpdateLabels(mode,self.lastPickedPlayerID,"danny"),font=customtkinter.CTkFont(family="Bahnschrift SemiBold", size=fontSizeEntry), fg_color="#2eb217")
        addToDannyButton.grid(column=0, padx=5,row=3,pady=10)

        selectPlayerButton = customtkinter.CTkButton(selectionFrame, text="View Playercard", command=lambda: self.goToPlayerFile(),font=customtkinter.CTkFont(family="Bahnschrift SemiBold", size=fontSizeEntry), fg_color="#2eb217")
        selectPlayerButton.grid(column=1, padx=5,row=3,pady=10)

        addToAlexButton = customtkinter.CTkButton(selectionFrame, text="Add >", command=lambda: self.drawAndUpdateLabels(mode,self.lastPickedPlayerID,"alex"),font=customtkinter.CTkFont(family="Bahnschrift SemiBold", size=fontSizeEntry), fg_color="#2eb217")
        addToAlexButton.grid(column=2, padx=5,row=3,pady=10)

        alexRemoveButton = customtkinter.CTkButton(self.root,text="Remove Player",command=lambda: self.drawAndUpdateLabels(mode,-1,"alex"),font=customtkinter.CTkFont(family="Bahnschrift SemiBold", size=fontSize),fg_color="#2eb217")
        alexRemoveButton.place(x=1480,y=800,width=300)
        dannyRemoveButton = customtkinter.CTkButton(self.root,text="Remove Player",command=lambda: self.drawAndUpdateLabels(mode,-1,"danny"),font=customtkinter.CTkFont(family="Bahnschrift SemiBold", size=fontSize),fg_color="#2eb217")
        dannyRemoveButton.place(x=145,y=800,width=300)




        # This is a listbox for search query
        self.searchBox.place(x=820,y=410,width=270,height=380)
        self.searchBox.tkraise()
        self.searchBox.config(bg="#36393e", fg="WHITE", highlightthickness=0)
        self.searchMenu_ClearSearchbox()

        filterStr = StringVar(None)
        filterStr.set("Any")

        def archFilterFunc():
            searchEntry.delete(0,END)
            self.searchMenu_Check(searchEntry,self.playerbaseOptions,filterName="Archetype",filterVal=filterStr.get())
        archFilterMenu = OptionMenu(selectionFrame, filterStr, *FILTER_OPTIONS,command=lambda x: archFilterFunc())
        archFilterMenu.grid(column=1,row=5,padx=5, pady=20)

        archFilterMenuFont = tkFont.Font(family='Helvetica', size=25)
        modeMenuFont = tkFont.Font(family='Helvetica', size=25)
        dropFont = tkFont.Font(family='Helvetica', size=25)

        archFilterMenuConfig = self.root.nametowidget(archFilterMenu.menuname)
        archFilterMenuConfig.config(font=archFilterMenuFont)
        archFilterMenu.config(bg="#36393e", fg="WHITE", highlightthickness=0, font=dropFont)
        archFilterMenu["menu"].config(bg="#36393e", fg="WHITE")


        swapTeamsButton = customtkinter.CTkButton(self.root, text="Swap Teams", command=lambda: self.swapPickerTeams(mode),font=customtkinter.CTkFont(family="Bahnschrift SemiBold", size=fontSize),fg_color="#2eb217")
        swapTeamsButton.place(x=835, y=870)

        randTeamsButton = customtkinter.CTkButton(self.root, text="Random Teams", command=lambda: self.randomPlayerPicks(mode),font=customtkinter.CTkFont(family="Bahnschrift SemiBold", size=fontSize),fg_color="#2eb217")
        randTeamsButton.place(x=835, y=935)

        self.drawLabels(mode)

        modeMenu = OptionMenu(self.root, mode, *MODE_OPTIONS,command=lambda x: self.drawLabels(mode))
        modeMenu.place(x=860,y=810,width=200)
        self.alexPickOneLabel.grid(column=1, row=1, pady=40)
        self.dannyPickOneLabel.grid(column=1, row=1, pady=40)
        self.alexPickTwoLabel.grid(column=1, row=2, pady=40)
        self.dannyPickTwoLabel.grid(column=1, row=2, pady=40)
        self.alexPickThreeLabel.grid(column=1, row=3, pady=40)
        self.dannyPickThreeLabel.grid(column=1, row=3, pady=40)
        self.alexPickFourLabel.grid(column=1, row=4, pady=40)
        self.dannyPickFourLabel.grid(column=1, row=4, pady=40)

        modeMenuConfig = self.root.nametowidget(modeMenu.menuname)
        modeMenuConfig.config(font=modeMenuFont)
        modeMenu.config(bg="#36393e", fg="WHITE", highlightthickness=0, font=dropFont)
        modeMenu["menu"].config(bg="#36393e", fg="WHITE")


        # This creates a binding on the listbox on click
        self.searchBox.bind("<<ListboxSelect>>", lambda x: self.searchMenu_Fillout(searchEntry))

        # This creates a binding on the entry box
        searchEntry.bind("<KeyRelease>", lambda x: self.searchMenu_Check(searchEntry,self.playerbaseOptions))

        self.searchMenu_Update()
    def swapPickerTeams(self,modeVar):
        transfer = self.alexPicks
        self.alexPicks = self.dannyPicks
        self.dannyPicks = transfer
        self.drawLabels(modeVar)
    def randomPlayerPicks(self,modeVar):
        self.alexPicks = []
        self.dannyPicks = []

        self.updatePickedPlayers(-1,"Alex")
        self.updatePickedPlayers(-1,"Danny")

        spriteIDsHat = WeightedDict.WeightedDict()
        for spriteID in self.playerbaseOptions.keys():
            spriteIDsHat.add(spriteID,1)

        for i in range(int(modeVar.get()[0])):
            self.alexPicks.append(spriteIDsHat.hatPull())
            self.dannyPicks.append(spriteIDsHat.hatPull())

        self.drawLabels(modeVar)

    def drawLabels(self,modeVar):
        try:
            self.alexPickOneLabel.configure(text=h.getFullPlayerName(self.alexPicks[0],dataStorageObject=self.globalDataStorage))
        except IndexError:
            self.alexPickOneLabel.configure(text="---")
        try:
            self.alexPickTwoLabel.configure(text=h.getFullPlayerName(self.alexPicks[1],dataStorageObject=self.globalDataStorage))
        except IndexError:
            self.alexPickTwoLabel.configure(text="---")
        try:
            self.alexPickThreeLabel.configure(text=h.getFullPlayerName(self.alexPicks[2],dataStorageObject=self.globalDataStorage))
        except IndexError:
            self.alexPickThreeLabel.configure(text="---")
        try:
            self.alexPickFourLabel.configure(text=h.getFullPlayerName(self.alexPicks[3],dataStorageObject=self.globalDataStorage))
        except IndexError:
            self.alexPickFourLabel.configure(text="---")
        try:
            self.alexPickFiveLabel.configure(text=h.getFullPlayerName(self.alexPicks[4],dataStorageObject=self.globalDataStorage))
        except IndexError:
            self.alexPickFiveLabel.configure(text="---")

        try:
            self.dannyPickOneLabel.configure(text=h.getFullPlayerName(self.dannyPicks[0],dataStorageObject=self.globalDataStorage))
        except IndexError:
            self.dannyPickOneLabel.configure(text="---")
        try:
            self.dannyPickTwoLabel.configure(text=h.getFullPlayerName(self.dannyPicks[1],dataStorageObject=self.globalDataStorage))
        except IndexError:
            self.dannyPickTwoLabel.configure(text="---")
        try:
            self.dannyPickThreeLabel.configure(text=h.getFullPlayerName(self.dannyPicks[2],dataStorageObject=self.globalDataStorage))
        except IndexError:
            self.dannyPickThreeLabel.configure(text="---")
        try:
            self.dannyPickFourLabel.configure(text=h.getFullPlayerName(self.dannyPicks[3],dataStorageObject=self.globalDataStorage))
        except IndexError:
            self.dannyPickFourLabel.configure(text="---")
        try:
            self.dannyPickFiveLabel.configure(text=h.getFullPlayerName(self.dannyPicks[4],dataStorageObject=self.globalDataStorage))
        except IndexError:
            self.dannyPickFiveLabel.configure(text="---")


        mode = int(modeVar.get()[0])
        if(mode > 1):
            self.alexPickTwoLabel.grid(column=1, row=2, pady=40)
            self.dannyPickTwoLabel.grid(column=1, row=2, pady=40)
        if (mode > 2):
            self.alexPickThreeLabel.grid(column=1, row=3, pady=40)
            self.dannyPickThreeLabel.grid(column=1, row=3, pady=40)
        if (mode > 3):
            self.alexPickFourLabel.grid(column=1, row=4, pady=40)
            self.dannyPickFourLabel.grid(column=1, row=4, pady=40)
        if (mode > 4):
            self.alexPickFiveLabel.grid(column=1, row=5, pady=40)
            self.dannyPickFiveLabel.grid(column=1, row=5, pady=40)

        if(mode < 5):
            self.alexPickFiveLabel.grid_forget()
            self.dannyPickFiveLabel.grid_forget()
        if(mode < 4):
            self.alexPickFourLabel.grid_forget()
            self.dannyPickFourLabel.grid_forget()
        if(mode < 3):
            self.alexPickThreeLabel.grid_forget()
            self.dannyPickThreeLabel.grid_forget()
        if(mode < 2):
            self.alexPickTwoLabel.grid_forget()
            self.dannyPickTwoLabel.grid_forget()
    # This method simply manages updated the pickedPlayerLists with new spriteIDs. If a spriteID of -1 is supplied,
    # it is assumed to mean that a player is being removed instead from the given pickedPlayerList.
    def updatePickedPlayers(self,pickedPlayerID,technician):
        if(pickedPlayerID is None):
            return False

        if("alex" in technician.lower()):
            technician = "alex"
        elif("danny" in technician.lower()):
            technician = "danny"
        else:
            print("ERROR: Invalid technician name.")
            return False

        if(str(type(pickedPlayerID)) == "<class 'str'>"):
            pickedPlayerID = int(pickedPlayerID)

        if(pickedPlayerID in self.alexPicks):
            messagebox.showerror("Check again, Punk", f"{h.getFullPlayerName(pickedPlayerID,dataStorageObject=self.globalDataStorage)} has already been picked by Alex!")
            return False
        elif(pickedPlayerID in self.dannyPicks):
            messagebox.showerror("Check again, Punk", f"{h.getFullPlayerName(pickedPlayerID,dataStorageObject=self.globalDataStorage)} has already been picked by Danny!")
            return False
        else:
            if(technician == "alex"):
                if(pickedPlayerID == -1):
                    if(len(self.alexPicks) <= 0):
                        return False
                    else:
                        del self.alexPicks[-1]
                else:
                    if(len(self.alexPicks) > 5):
                        return False
                    else:
                        self.alexPicks.append(pickedPlayerID)
            elif(technician == "danny"):
                if(pickedPlayerID == -1):
                    if(len(self.dannyPicks) <= 0):
                        return False
                    else:
                        del self.dannyPicks[-1]
                else:
                    if(len(self.dannyPicks) > 5):
                        return False
                    else:
                        self.dannyPicks.append(pickedPlayerID)
    # Simple helper to combine the above two methods.
    def drawAndUpdateLabels(self,modeVar,pickedPlayerID,technician):
        self.updatePickedPlayers(pickedPlayerID,technician)
        self.drawLabels(modeVar)


    # CAP menu methods.
    def goToCAPMenu(self):

        self.wipeScreen("CAPMenu")

        self.root.geometry("345x400+650+250")

        nba2k_Label = Label(self.root, image=self.nba2k_Logo)
        nba2k_Label.photo = self.nba2k_Logo
        nba2k_Label.grid(column=0, row=0, columnspan=3)


        fontSize = 45
        fontSizeEntry = 25

        fnLabel = StringVar()
        fnLabel.set("Enter First Name:")

        fnLabelDir = customtkinter.CTkLabel(self.root, textvariable=fnLabel, height=2,font=customtkinter.CTkFont(family="Bahnschrift SemiBold", size=fontSize))
        fnLabelDir.grid(column=1,row=1,padx=100, pady=15)

        fnName = StringVar(None)
        fnNameEntry = customtkinter.CTkEntry(self.root, textvariable=fnName, width=400, font=customtkinter.CTkFont(family="Bahnschrift", size=fontSizeEntry))
        fnNameEntry.grid(column=1,row=2,padx=100, pady=15)

        lnLabel = StringVar()
        lnLabel.set("Enter Last Name:")
        lnLabelDir = customtkinter.CTkLabel(self.root, textvariable=lnLabel, height=2,font=customtkinter.CTkFont(family="Bahnschrift SemiBold", size=fontSize))
        lnLabelDir.grid(column=1,row=3,padx=100, pady=15)

        lnName = StringVar(None)
        lnNameEntry = customtkinter.CTkEntry(self.root, textvariable=lnName, width=400, font=customtkinter.CTkFont(family="Bahnschrift", size=fontSizeEntry))
        lnNameEntry.grid(column=1,row=4,padx=100, pady=15)

        # This is the important variable to .get()
        archetype = StringVar(None)
        archetype.set("Slayer")
        # This is the actual dropdown menu
        dropArchetype = OptionMenu(self.root, archetype, *ARCHETYPE_OPTIONS)
        # dropArchetype.grid(column=0,row=0,padx=10,pady=10)
        dropArchetype.grid(column=1,row=5,padx=100, pady=15)

        # This is the important variable to .get()
        heightVar = StringVar(None)
        heightVar.set("Archetype")
        heightOptions = [
            "5'3",
            "5'4",
            "5'5",
            "5'6",
            "5'7",
            "5'8",
            "5'9",
            "5'10",
            "5'11",
            "6'0",
            "6'1",
            "6'2",
            "6'3",
            "6'4",
            "6'5",
            "6'6",
            "6'7",
            "6'8",
            "6'9",
            "6'10",
            "6'11",
            "7'0",
            "7'1",
            "7'2",
            "7'3",
            "7'4",
            "7'5",
            "7'6",
            "Archetype"
        ]
        # This is the actual dropdown menu
        dropHeight = OptionMenu(self.root, heightVar, *heightOptions)
        # dropHeight.grid(column=0,row=0,padx=10,pady=10)
        dropHeight.grid(column=1,row=6,padx=100, pady=15)

        rosterVar = StringVar(None)
        rosterVar.set("None")
        rosterOptions = ["None"] + self.globalDataStorage.csv_GetSavedRosterList()
        dropRoster = OptionMenu(self.root, rosterVar, *rosterOptions)
        dropRoster.grid(column=1,row=7,padx=100,pady=15)


        submitButton = customtkinter.CTkButton(self.root, text="Submit", command=lambda: self.CAPMenu_SubmitCAP(fnName.get(),lnName.get(),archetype.get(),heightVar.get(),rosterVar.get()),font=customtkinter.CTkFont(family="Bahnschrift SemiBold", size=fontSize), fg_color="#2eb217")
        # submitButton.grid(column=0,row=0,padx=10,pady=10)1,row=4, pady=10)
        submitButton.grid(column=1,row=8,padx=100, pady=15)
        mainMenuButton = customtkinter.CTkButton(self.root, text="Main Menu", command=self.goToMainMenu,font=customtkinter.CTkFont(family="Bahnschrift SemiBold", size=fontSize), fg_color="#2eb217")
        mainMenuButton.grid(column=1,row=9,padx=100, pady=15)

        # This is for color configuration
        dropFont = tkFont.Font(family='Helvetica', size=35)
        archetypeMenuFont = tkFont.Font(family='Helvetica', size=25)
        heightMenuFont = tkFont.Font(family='Helvetica', size=20)
        rosterMenuFont = tkFont.Font(family='Helvetica', size=20)

        archetypeMenu = self.root.nametowidget(dropArchetype.menuname)
        archetypeMenu.config(font=archetypeMenuFont)
        dropArchetype.config(bg="#36393e", fg="WHITE", highlightthickness=0, font=dropFont)
        dropArchetype["menu"].config(bg="#36393e", fg="WHITE")

        heightMenu = self.root.nametowidget(dropHeight.menuname)
        heightMenu.config(font=heightMenuFont)
        dropHeight.config(bg="#36393e", fg="WHITE", highlightthickness=0, font=dropFont)
        dropHeight["menu"].config(bg="#36393e", fg="WHITE")

        rosterMenu = self.root.nametowidget(dropRoster.menuname)
        rosterMenu.config(font=rosterMenuFont)
        dropRoster.config(bg="#36393e", fg="WHITE", highlightthickness=0, font=dropFont)
        dropRoster["menu"].config(bg="#36393e", fg="WHITE")
    def CAPMenu_SubmitCAP(self,firstName,lastName,archetypeName,heightValue,rosterToAddPlayerTo):

        pygame.mixer.init()

        if(rosterToAddPlayerTo != "None"):
            for flaggedRoster in self.incomingChanges:
                if(flaggedRoster.split(".ROS")[0] == rosterToAddPlayerTo):
                    messagebox.showinfo(title="ALERT ALERT", message="Roster '" + rosterToAddPlayerTo + "' has incoming changes that must be saved. Player was created, but not added to Roster.")

        if archetypeName == "Slayer":
            if heightValue not in HEIGHT_OPTIONS[0:8] and heightValue != "Archetype":
                messagebox.showerror('Error', heightValue + " does not fit the height bounds for " + archetypeName)
        elif archetypeName == "Vigilante":
            if heightValue not in HEIGHT_OPTIONS[6:13] and heightValue != "Archetype":
                messagebox.showerror('Error', heightValue + " does not fit the height bounds for " + archetypeName)
        elif archetypeName == "Medic":
            if heightValue not in HEIGHT_OPTIONS[12:22] and heightValue != "Archetype":
                messagebox.showerror('Error', heightValue + " does not fit the height bounds for " + archetypeName)
        elif archetypeName == "Guardian":
            if heightValue not in HEIGHT_OPTIONS[21:30] and heightValue != "Archetype":
                messagebox.showerror('Error', heightValue + " does not fit the height bounds for " + archetypeName)
        elif archetypeName == "Engineer":
            if heightValue not in HEIGHT_OPTIONS[6:13] and heightValue != "Archetype":
                messagebox.showerror('Error', heightValue + " does not fit the height bounds for " + archetypeName)
        elif archetypeName == "Director":
            if heightValue not  in HEIGHT_OPTIONS[0:8] and heightValue != "Archetype":
                messagebox.showerror('Error', heightValue + " does not fit the height bounds for " + archetypeName)


        if(heightValue == "Archetype"):
            heightValue = None

        # TODO DEFINITELY overhaul this
        newPlayer = Player.Player()
        newPlayer["First_Name"] = firstName
        newPlayer["Last_Name"] = lastName
        newPlayer["Archetype"] = archetypeName
        newPlayer.genRarity()
        newPlayer.genAttributes()
        newPlayer.genHeight()
        newPlayer.genTendencies()
        newPlayer.genHotspots()
        newPlayer.genPlayTypes()
        newPlayer.genPlayStyle()
        newPlayer.genAnimations()
        newPlayer.genMisc()
        newPlayer.generateArtifact()

        b.backup(f"{b.paths.databases}\\Players.db",f"{b.paths.backups}\\PlayerData",20)
        newSpriteID = h.savePlayerObjectToPlayersFile(newPlayer,dataStorageObject=self.globalDataStorage)
        if (rosterToAddPlayerTo != "None"):
            h.addPlayerToRoster(newSpriteID, rosterToAddPlayerTo, dataStorageObject=self.globalDataStorage,saveFile=True)
            self.outgoingChanges.append(rosterToAddPlayerTo)


        if(newPlayer["Rarity"] == "Rare"):
            pygame.mixer.music.load(f"{b.paths.media}\\Rare.ogg")
            pygame.mixer.music.play(loops=0)
            pygame.mixer.music.set_volume(0.075)
        elif(newPlayer["Rarity"] == "Epic"):
            pygame.mixer.music.load(f"{b.paths.media}\\Epic.ogg")
            pygame.mixer.music.play(loops=0)
            pygame.mixer.music.set_volume(0.075)
        elif (newPlayer["Rarity"] == "Legendary"):
            pygame.mixer.music.load(f"{b.paths.media}\\Legendary.ogg")
            pygame.mixer.music.play(loops=0)
            pygame.mixer.music.set_volume(0.075)
        elif (newPlayer["Rarity"] == "Godlike"):
            pygame.mixer.music.load(f"{b.paths.media}\\Godlike.mp3")
            pygame.mixer.music.play(loops=0)
            pygame.mixer.music.set_volume(0.4)
        elif (newPlayer["Rarity"] == "Common"):
            pygame.mixer.music.load(f"{b.paths.media}\\Common.ogg")
            pygame.mixer.music.play(loops=0)
            pygame.mixer.music.set_volume(0.075)



        messagebox.showinfo('Success!', firstName + " " + lastName + " has been created!")


    # Search menu methods.
    def goToSearchMenu(self):
        self.wipeScreen("PlayerSearchMenu")

        self.root.geometry("420x500+650+250")

        nba2k_Label = Label(self.root, image=self.nba2k_Logo)
        nba2k_Label.photo = self.nba2k_Logo
        nba2k_Label.grid(column=0, row=0, columnspan=3)


        fontSize = 45
        fontSizeEntry = 25
        fontSizeListbox = 15

        playerbaseOptions = h.getDictOfPlayerNames()

        searchLabel = customtkinter.CTkLabel(self.root, text="Search Playerbase:",font=customtkinter.CTkFont(family="Bahnschrift SemiBold", size=fontSize))
        searchLabel.grid(column=1,row=1,padx=100, pady=10)

        searchResult = StringVar(None)
        searchEntry = customtkinter.CTkEntry(self.root, textvariable=searchResult, width=400, font=customtkinter.CTkFont(family="Bahnschrift", size=fontSizeEntry))
        searchEntry.grid(column=1,row=2,padx=100, pady=10)


        searchPlayerButton = customtkinter.CTkButton(self.root, text="Search Player", command=lambda: self.goToPlayerFile(),font=customtkinter.CTkFont(family="Bahnschrift SemiBold", size=fontSizeEntry), fg_color="#2eb217")
        searchPlayerButton.grid(column=1,row=3,padx=100, pady=10)

        # This is a listbox for search query

        self.searchBox.grid(column=1,row=4,padx=100, pady=10)
        self.searchBox.config(bg="#36393e", fg="WHITE", highlightthickness=0)
        self.searchMenu_ClearSearchbox()


        mainMenuButton = customtkinter.CTkButton(self.root, text="Main Menu", command=self.goToMainMenu,font=customtkinter.CTkFont(family="Bahnschrift SemiBold", size=fontSize), fg_color="#2eb217")
        mainMenuButton.grid(column=1,row=5,padx=100, pady=10)

        clearListButton = customtkinter.CTkButton(self.root, text="Clear results", command=lambda: self.searchMenu_ClearSearchbox(),font=customtkinter.CTkFont(family="Bahnschrift SemiBold", size=fontSize), fg_color="#2eb217")
        clearListButton.grid(column=1,row=6,padx=100, pady=10)



        # This creates a binding on the listbox on click
        self.searchBox.bind("<<ListboxSelect>>", lambda x: self.searchMenu_Fillout(searchEntry))

        # This creates a binding on the entry box
        searchEntry.bind("<KeyRelease>", lambda x: self.searchMenu_Check(searchEntry,playerbaseOptions))

        self.searchMenu_Update()
    # This method recalculates the values of self.playerSearchIDs and self.playerSearchNames,
    # then updates the searchMenu.
    def searchMenu_Check(self,searchEntry,playerbaseOptions,filterName=None,filterVal=None):
        if(filterName is not None):
            self.searchBoxFilters[filterName] = filterVal

        searchEntryString = searchEntry.get()
        self.playerSearchIDs = []
        self.playerSearchNames = []

        for spriteID, fullName in playerbaseOptions.items():
            if(searchEntryString.lower() in fullName.lower() or searchEntryString == ""):
                if(self.searchBoxFilters.get("Archetype") != "Any"):
                    if(self.globalDataStorage.playersDB_ReadElement(spriteID,"Archetype").lower() != self.searchBoxFilters.get("Archetype").lower()):
                        continue
                self.playerSearchIDs.append(spriteID)
                self.playerSearchNames.append(fullName)

        # Update listbox with selected items
        self.searchMenu_Update()
    # This method updates the searchMenu with all names in self.playerSearchNames
    def searchMenu_Update(self):
        self.searchMenu_ClearSearchbox()

        # Add players to listbox
        for item in self.playerSearchNames:
            self.searchBox.insert(END, item)
    def searchMenu_Fillout(self,searchEntry):
        # Delete whatever is in the entry box
        searchEntry.delete(0, END)

        # Add clicked list item to entry box by comparing the index of the
        # selected playerName to self.playerSearchIDs.
        try:
            searchEntry.insert(0, self.playerSearchNames[self.searchBox.curselection()[0]])
            self.lastPickedPlayerID = self.playerSearchIDs[self.searchBox.curselection()[0]]
        except (_tkinter.TclError, IndexError):
            searchEntry.insert(0,"")
            self.lastPickedPlayerID = None
    def searchMenu_ClearSearchbox(self):
        self.searchBox.delete(0, END)
    def searchMenu_ResetFilters(self):
        self.searchBoxFilters = {"Archetype" : "Any"}

    # Player file menu methods.
    def goToPlayerFile(self):
        if(self.lastPickedPlayerID is None):
            print("WARNING: Picked player seems to have a SpriteID of None!")
        spriteID = int(self.lastPickedPlayerID)
        playerName = h.getFullPlayerName(spriteID,dataStorageObject=self.globalDataStorage)

        self.wipeScreen("PlayerFile|" + str(spriteID))








        self.root.geometry("440x550+650+250")

        archetypeName =  str(self.globalDataStorage.playersDB_ReadElement(spriteID, "Archetype"))
        if(archetypeName is None):
            archetypeName = "Classic"

        rarityName =  str(self.globalDataStorage.playersDB_ReadElement(spriteID, "Rarity"))
        if (rarityName is None):
            rarityName = "Classic"


        nba2k_Label = Label(self.root, image=self.nba2k_Logo)
        nba2k_Label.photo = self.nba2k_Logo
        nba2k_Label.grid(column=0, row=0, columnspan=3)

        playerNameFontSize = 20
        archetypeFontSize = 16
        rarityFontSize = 16
        if(16 <= len(playerName) < 20):
            playerNameFontSize = 28
            archetypeFontSize = 22
            rarityFontSize = 18
        elif(12 <= len(playerName) < 16):
            playerNameFontSize = 32
            archetypeFontSize = 25
            rarityFontSize = 20
        elif (8 <= len(playerName) < 12):
            playerNameFontSize = 45
            archetypeFontSize = 35
            rarityFontSize = 30
        elif (4 <= len(playerName) < 8):
            playerNameFontSize = 80
            archetypeFontSize = 40
            rarityFontSize=30

        rarityColor = "white"

        if (rarityName == "Common"):
            rarityColor = "white"
        elif(rarityName == "Rare"):
            rarityColor = "green"
        elif(rarityName == "Epic"):
            rarityColor = "purple"
        elif(rarityName == "Legendary"):
            rarityColor = "yellow"
        elif(rarityName == "Godlike"):
            rarityColor = "red"



        basicInfoFrame = customtkinter.CTkFrame(self.root)
        basicInfoFrame.place(x=800,y=100)

        resultLabel = customtkinter.CTkLabel(basicInfoFrame, text=playerName,font=customtkinter.CTkFont(family="Bahnschrift SemiBold", size=playerNameFontSize))
        resultLabel.grid(column=0,row=0,padx=10)
        #TODO LINK BIO HERE AS TOOLTIP
        CreateToolTip(resultLabel,"Here will be a bio about the player")

        archetypeLabel = customtkinter.CTkLabel(basicInfoFrame, text=archetypeName,font=customtkinter.CTkFont(family="Bahnschrift SemiBold", size=archetypeFontSize))
        archetypeLabel.grid(column=0,row=1,padx=10)

        rarityLabel = customtkinter.CTkLabel(basicInfoFrame, text=rarityName.upper(),font=customtkinter.CTkFont(family="Bahnschrift SemiBold", size=rarityFontSize),text_color=rarityColor)
        rarityLabel.grid(column=0,row=2,padx=10)



        PRIMARY_STAT_FONT_SIZE = 24
        SECONDARY_STAT_FONT_SIZE = 16
        TERTIARY_STAT_FONT_SIZE = 8
        PRIMARY_PADY = 5
        SECONDARY_PADY = 3
        TERTIARY_PADY = 1
        scoringFontSize = None
        scoringPadY = None
        defensiveFontSize = None
        defensivePadY = None
        controlFontSize = None
        controlPadY = None


        if(archetypeName == "Slayer"):
            scoringFontSize = PRIMARY_STAT_FONT_SIZE
            scoringPadY = PRIMARY_PADY
            defensiveFontSize = TERTIARY_STAT_FONT_SIZE
            defensivePadY = TERTIARY_PADY
            controlFontSize = SECONDARY_STAT_FONT_SIZE
            controlPadY = SECONDARY_PADY
            CreateToolTip(archetypeLabel,text="Shorter player who excels at shooting the basketball at any area on the court.\n Has decent ball control, but very poor defense - easy to block, doesn't deal well with contested shots.\n Slayers are different than Vigilantes in that they can create shot opportunities through movement, avoiding contested shots altogether.\n Worst rebounder in the game.")
        elif(archetypeName == "Vigilante"):
            scoringFontSize = PRIMARY_STAT_FONT_SIZE
            scoringPadY = PRIMARY_PADY
            defensiveFontSize = SECONDARY_STAT_FONT_SIZE
            defensivePadY = SECONDARY_PADY
            controlFontSize = TERTIARY_STAT_FONT_SIZE
            controlPadY = TERTIARY_PADY
            CreateToolTip(archetypeLabel,text="Mid sized player with strong scoring ability, even in the face of defense.\n Quite slow generally, and the worst ball control in the game.\n Decent rebounders, especially in the offense.\n One of the best attackers, whether they have the ball or not.\n Also plays a decent defense.")
        elif (archetypeName == "Medic"):
            scoringFontSize = TERTIARY_STAT_FONT_SIZE
            scoringPadY = TERTIARY_PADY
            defensiveFontSize = PRIMARY_STAT_FONT_SIZE
            defensivePadY = PRIMARY_PADY
            controlFontSize = SECONDARY_STAT_FONT_SIZE
            controlPadY = SECONDARY_PADY
            CreateToolTip(archetypeLabel, text="Incredibly passive, often very tall players who simply help the team in the background.\n Best rebounder in the game, but completely incapable of scoring, often even at close range.\n Has decent ball control to get the ball to a more active player.")
        elif (archetypeName == "Guardian"):
            scoringFontSize = SECONDARY_STAT_FONT_SIZE
            scoringPadY = SECONDARY_PADY
            defensiveFontSize = PRIMARY_STAT_FONT_SIZE
            defensivePadY = PRIMARY_PADY
            controlFontSize = TERTIARY_STAT_FONT_SIZE
            controlPadY = TERTIARY_PADY
            CreateToolTip(archetypeLabel, text="Massive, lumbering giants that essentially plant themselves where they'll cause the most havoc for the other team.\n Excellent defenders and tower over shooters to block their shots, somewhat decent scorers, but unbearably slow.\n Poor ball control all around means you don't want them to ever be moving with the ball.")
        elif (archetypeName == "Engineer"):
            scoringFontSize = TERTIARY_STAT_FONT_SIZE
            scoringPadY = TERTIARY_PADY
            defensiveFontSize = SECONDARY_STAT_FONT_SIZE
            defensivePadY = SECONDARY_PADY
            controlFontSize = PRIMARY_STAT_FONT_SIZE
            controlPadY = PRIMARY_PADY
            CreateToolTip(archetypeLabel, text="Mid-sized players that are experts at bringing the ball from point A to point B as safely as possible.\n Fantastic ball handlers, pretty quick, and very difficult to steal from.\n Where Medics are extremely passive supports, preferring to play in the paint, Engineers are frequently moving the ball all around the court.\n They emphasize ball safety above all. ")
        elif (archetypeName == "Director"):
            scoringFontSize = SECONDARY_STAT_FONT_SIZE
            scoringPadY = SECONDARY_PADY
            defensiveFontSize = TERTIARY_STAT_FONT_SIZE
            defensivePadY = TERTIARY_PADY
            controlFontSize = PRIMARY_STAT_FONT_SIZE
            controlPadY = PRIMARY_PADY
            CreateToolTip(archetypeLabel, text="Shorter players who command the the game from whatever position they're in.\n Where the Engineer slowly, carefully crafts his plays, the Director dynamically and often boldly commands play across the court, whether that means a risky pass, juking a defender, or even shooting the ball himself.\n Directors only excel in the offense, and take a back seat when the ball is with the other team.")
        else:
            scoringFontSize = SECONDARY_STAT_FONT_SIZE
            scoringPadY = SECONDARY_PADY
            defensiveFontSize = TERTIARY_STAT_FONT_SIZE
            defensivePadY = TERTIARY_PADY
            controlFontSize = PRIMARY_STAT_FONT_SIZE
            controlPadY = PRIMARY_PADY
            CreateToolTip(archetypeLabel, text="Shorter players who command the the game from whatever position they're in.\n Where the Engineer slowly, carefully crafts his plays, the Director dynamically and often boldly commands play across the court, whether that means a risky pass, juking a defender, or even shooting the ball himself.\n Directors only excel in the offense, and take a back seat when the ball is with the other team.")




        archetypeName = self.globalDataStorage.playersDB_ReadElement(spriteID, "Archetype")
        arch = None
        if(archetypeName is None):
            arch = Archetypes.ARCH_SLAYER
        else:
            if(archetypeName.lower() == "slayer"):
                arch = Archetypes.ARCH_SLAYER
            elif(archetypeName.lower() == "vigilante"):
                arch = Archetypes.ARCH_VIGILANTE
            elif (archetypeName.lower() == "medic"):
                arch = Archetypes.ARCH_MEDIC
            elif (archetypeName.lower() == "guardian"):
                arch = Archetypes.ARCH_GUARDIAN
            elif (archetypeName.lower() == "engineer"):
                arch = Archetypes.ARCH_ENGINEER
            elif (archetypeName.lower() == "director"):
                arch = Archetypes.ARCH_DIRECTOR

        belowAverageColor =  "Red"
        averageColor =  "Yellow"
        aboveAverageColor =  "Green"

        # Do this for all stats.
        avgSOffHDrib = b.averageOfList(arch.attributeRanges.get("SOffHDrib"))
        avgSHands = b.averageOfList(arch.attributeRanges.get("SHands"))
        avgSOAwar = b.averageOfList(arch.attributeRanges.get("SOAwar"))
        avgSBallHndl = b.averageOfList(arch.attributeRanges.get("SBallHndl"))
        avgSBallSec = b.averageOfList(arch.attributeRanges.get("SBallSec"))
        avgSPass = b.averageOfList(arch.attributeRanges.get("SPass"))
        avgSSpeed = b.averageOfList(arch.attributeRanges.get("SSpeed"))
        avgSQuick = b.averageOfList(arch.attributeRanges.get("SQuick"))
        avgSHustle = b.averageOfList(arch.attributeRanges.get("SHustle"))
        avgSSteal = b.averageOfList(arch.attributeRanges.get("SSteal"))
        avgSDLowPost = b.averageOfList(arch.attributeRanges.get("SDLowPost"))
        avgSStrength = b.averageOfList(arch.attributeRanges.get("SStrength"))
        avgSBlock = b.averageOfList(arch.attributeRanges.get("SBlock"))
        avgSOnBallD = b.averageOfList(arch.attributeRanges.get("SOnBallD"))
        avgSOReb = b.averageOfList(arch.attributeRanges.get("SOReb"))
        avgSDReb = b.averageOfList(arch.attributeRanges.get("SDReb"))
        avgSDAwar = b.averageOfList(arch.attributeRanges.get("SDAwar"))
        avgSShtIns = b.averageOfList(arch.attributeRanges.get("SShtIns"))
        avgSDunk = b.averageOfList(arch.attributeRanges.get("SDunk"))
        avgSStdDunk = b.averageOfList(arch.attributeRanges.get("SStdDunk"))
        avgSVertical = b.averageOfList(arch.attributeRanges.get("SVertical"))
        avgSShtFT = b.averageOfList(arch.attributeRanges.get("SShtFT"))
        avgSStamina = b.averageOfList(arch.attributeRanges.get("SStamina"))
        avgSDurab = b.averageOfList(arch.attributeRanges.get("SDurab"))
        avgSPOT = b.averageOfList(arch.attributeRanges.get("SPOT"))
        avgSShtCls = b.averageOfList(arch.attributeRanges.get("SShtCls"))
        avgSLayUp = b.averageOfList(arch.attributeRanges.get("SLayUp"))
        avgSPstFdaway = b.averageOfList(arch.attributeRanges.get("SPstFdaway"))
        avgSPstHook = b.averageOfList(arch.attributeRanges.get("SPstHook"))
        avgSOLowPost = b.averageOfList(arch.attributeRanges.get("SOLowPost"))
        avgSShtMed = b.averageOfList(arch.attributeRanges.get("SShtMed"))
        avgSSht3PT = b.averageOfList(arch.attributeRanges.get("SSht3PT"))
        avgSShtInT = b.averageOfList(arch.attributeRanges.get("SShtInT"))
        avgSShtOfD = b.averageOfList(arch.attributeRanges.get("SShtOfD"))
        avgSConsis = b.averageOfList(arch.attributeRanges.get("SConsis"))


        if(avgSOffHDrib > int(self.globalDataStorage.playersDB_ReadElement(spriteID, "SOffHDrib"))):
            clrSOffHDrib = belowAverageColor
        elif(avgSOffHDrib < int(self.globalDataStorage.playersDB_ReadElement(spriteID, "SOffHDrib"))):
            clrSOffHDrib = aboveAverageColor
        else:
            clrSOffHDrib = averageColor

        if(avgSHands > int(self.globalDataStorage.playersDB_ReadElement(spriteID, "SHands"))):
            clrSHands = belowAverageColor
        elif(avgSHands < int(self.globalDataStorage.playersDB_ReadElement(spriteID, "SHands"))):
            clrSHands = aboveAverageColor
        else:
            clrSHands = averageColor

        if(avgSOAwar > int(self.globalDataStorage.playersDB_ReadElement(spriteID, "SOAwar"))):
            clrSOAwar = belowAverageColor
        elif(avgSOAwar < int(self.globalDataStorage.playersDB_ReadElement(spriteID, "SOAwar"))):
            clrSOAwar = aboveAverageColor
        else:
            clrSOAwar = averageColor

        if (avgSBallHndl > int(self.globalDataStorage.playersDB_ReadElement(spriteID, "SBallHndl"))):
            clrSBallHndl = belowAverageColor
        elif (avgSBallHndl < int(self.globalDataStorage.playersDB_ReadElement(spriteID, "SBallHndl"))):
            clrSBallHndl = aboveAverageColor
        else:
            clrSBallHndl = averageColor

        if (avgSBallSec > int(self.globalDataStorage.playersDB_ReadElement(spriteID, "SBallSec"))):
            clrSBallSec = belowAverageColor
        elif (avgSBallSec < int(self.globalDataStorage.playersDB_ReadElement(spriteID, "SBallSec"))):
            clrSBallSec = aboveAverageColor
        else:
            clrSBallSec = averageColor

        if (avgSPass > int(self.globalDataStorage.playersDB_ReadElement(spriteID, "SPass"))):
            clrSPass = belowAverageColor
        elif (avgSPass < int(self.globalDataStorage.playersDB_ReadElement(spriteID, "SPass"))):
            clrSPass = aboveAverageColor
        else:
            clrSPass = averageColor

        if (avgSSpeed > int(self.globalDataStorage.playersDB_ReadElement(spriteID, "SSpeed"))):
            clrSSpeed = belowAverageColor
        elif (avgSSpeed < int(self.globalDataStorage.playersDB_ReadElement(spriteID, "SSpeed"))):
            clrSSpeed = aboveAverageColor
        else:
            clrSSpeed = averageColor

        if (avgSQuick > int(self.globalDataStorage.playersDB_ReadElement(spriteID, "SQuick"))):
            clrSQuick = belowAverageColor
        elif (avgSQuick < int(self.globalDataStorage.playersDB_ReadElement(spriteID, "SQuick"))):
            clrSQuick = aboveAverageColor
        else:
            clrSQuick = averageColor

        if (avgSHustle > int(self.globalDataStorage.playersDB_ReadElement(spriteID, "SHustle"))):
            clrSHustle = belowAverageColor
        elif (avgSHustle < int(self.globalDataStorage.playersDB_ReadElement(spriteID, "SHustle"))):
            clrSHustle = aboveAverageColor
        else:
            clrSHustle = averageColor

        if (avgSSteal > int(self.globalDataStorage.playersDB_ReadElement(spriteID, "SSteal"))):
            clrSSteal = belowAverageColor
        elif (avgSSteal < int(self.globalDataStorage.playersDB_ReadElement(spriteID, "SSteal"))):
            clrSSteal = aboveAverageColor
        else:
            clrSSteal = averageColor

        if (avgSDLowPost > int(self.globalDataStorage.playersDB_ReadElement(spriteID, "SDLowPost"))):
            clrSDLowPost = belowAverageColor
        elif (avgSDLowPost < int(self.globalDataStorage.playersDB_ReadElement(spriteID, "SDLowPost"))):
            clrSDLowPost = aboveAverageColor
        else:
            clrSDLowPost = averageColor

        if (avgSStrength > int(self.globalDataStorage.playersDB_ReadElement(spriteID, "SStrength"))):
            clrSStrength = belowAverageColor
        elif (avgSStrength < int(self.globalDataStorage.playersDB_ReadElement(spriteID, "SStrength"))):
            clrSStrength = aboveAverageColor
        else:
            clrSStrength = averageColor

        if (avgSBlock > int(self.globalDataStorage.playersDB_ReadElement(spriteID, "SBlock"))):
            clrSBlock = belowAverageColor
        elif (avgSBlock < int(self.globalDataStorage.playersDB_ReadElement(spriteID, "SBlock"))):
            clrSBlock = aboveAverageColor
        else:
            clrSBlock = averageColor

        if (avgSOnBallD > int(self.globalDataStorage.playersDB_ReadElement(spriteID, "SOnBallD"))):
            clrSOnBallD = belowAverageColor
        elif (avgSOnBallD < int(self.globalDataStorage.playersDB_ReadElement(spriteID, "SOnBallD"))):
            clrSOnBallD = aboveAverageColor
        else:
            clrSOnBallD = averageColor

        if (avgSOReb > int(self.globalDataStorage.playersDB_ReadElement(spriteID, "SOReb"))):
            clrSOReb = belowAverageColor
        elif (avgSOReb < int(self.globalDataStorage.playersDB_ReadElement(spriteID, "SOReb"))):
            clrSOReb = aboveAverageColor
        else:
            clrSOReb = averageColor

        if (avgSDReb > int(self.globalDataStorage.playersDB_ReadElement(spriteID, "SDReb"))):
            clrSDReb = belowAverageColor
        elif (avgSDReb < int(self.globalDataStorage.playersDB_ReadElement(spriteID, "SDReb"))):
            clrSDReb = aboveAverageColor
        else:
            clrSDReb = averageColor

        if (avgSDAwar > int(self.globalDataStorage.playersDB_ReadElement(spriteID, "SDAwar"))):
            clrSDAwar = belowAverageColor
        elif (avgSDAwar < int(self.globalDataStorage.playersDB_ReadElement(spriteID, "SDAwar"))):
            clrSDAwar = aboveAverageColor
        else:
            clrSDAwar = averageColor

        if (avgSShtIns > int(self.globalDataStorage.playersDB_ReadElement(spriteID, "SShtIns"))):
            clrSShtIns = belowAverageColor
        elif (avgSShtIns < int(self.globalDataStorage.playersDB_ReadElement(spriteID, "SShtIns"))):
            clrSShtIns = aboveAverageColor
        else:
            clrSShtIns = averageColor

        if (avgSDunk > int(self.globalDataStorage.playersDB_ReadElement(spriteID, "SDunk"))):
            clrSDunk = belowAverageColor
        elif (avgSDunk < int(self.globalDataStorage.playersDB_ReadElement(spriteID, "SDunk"))):
            clrSDunk = aboveAverageColor
        else:
            clrSDunk = averageColor

        if (avgSStdDunk > int(self.globalDataStorage.playersDB_ReadElement(spriteID, "SStdDunk"))):
            clrSStdDunk = belowAverageColor
        elif (avgSStdDunk < int(self.globalDataStorage.playersDB_ReadElement(spriteID, "SStdDunk"))):
            clrSStdDunk = aboveAverageColor
        else:
            clrSStdDunk = averageColor

        if (avgSVertical > int(self.globalDataStorage.playersDB_ReadElement(spriteID, "SVertical"))):
            clrSVertical = belowAverageColor
        elif (avgSVertical < int(self.globalDataStorage.playersDB_ReadElement(spriteID, "SVertical"))):
            clrSVertical = aboveAverageColor
        else:
            clrSVertical = averageColor

        if (avgSShtFT > int(self.globalDataStorage.playersDB_ReadElement(spriteID, "SShtFT"))):
            clrSShtFT = belowAverageColor
        elif (avgSShtFT < int(self.globalDataStorage.playersDB_ReadElement(spriteID, "SShtFT"))):
            clrSShtFT = aboveAverageColor
        else:
            clrSShtFT = averageColor

        if (avgSStamina > int(self.globalDataStorage.playersDB_ReadElement(spriteID, "SStamina"))):
            clrSStamina = belowAverageColor
        elif (avgSStamina < int(self.globalDataStorage.playersDB_ReadElement(spriteID, "SStamina"))):
            clrSStamina = aboveAverageColor
        else:
            clrSStamina = averageColor

        if (avgSDurab > int(self.globalDataStorage.playersDB_ReadElement(spriteID, "SDurab"))):
            clrSDurab = belowAverageColor
        elif (avgSDurab < int(self.globalDataStorage.playersDB_ReadElement(spriteID, "SDurab"))):
            clrSDurab = aboveAverageColor
        else:
            clrSDurab = averageColor

        if (avgSPOT > int(self.globalDataStorage.playersDB_ReadElement(spriteID, "SPOT"))):
            clrSPOT = belowAverageColor
        elif (avgSPOT < int(self.globalDataStorage.playersDB_ReadElement(spriteID, "SPOT"))):
            clrSPOT = aboveAverageColor
        else:
            clrSPOT = averageColor

        if (avgSShtCls > int(self.globalDataStorage.playersDB_ReadElement(spriteID, "SShtCls"))):
            clrSShtCls = belowAverageColor
        elif (avgSShtCls < int(self.globalDataStorage.playersDB_ReadElement(spriteID, "SShtCls"))):
            clrSShtCls = aboveAverageColor
        else:
            clrSShtCls = averageColor

        if (avgSLayUp > int(self.globalDataStorage.playersDB_ReadElement(spriteID, "SLayUp"))):
            clrSLayUp = belowAverageColor
        elif (avgSLayUp < int(self.globalDataStorage.playersDB_ReadElement(spriteID, "SLayUp"))):
            clrSLayUp = aboveAverageColor
        else:
            clrSLayUp = averageColor

        if (avgSPstFdaway > int(self.globalDataStorage.playersDB_ReadElement(spriteID, "SPstFdaway"))):
            clrSPstFdaway = belowAverageColor
        elif (avgSPstFdaway < int(self.globalDataStorage.playersDB_ReadElement(spriteID, "SPstFdaway"))):
            clrSPstFdaway = aboveAverageColor
        else:
            clrSPstFdaway = averageColor

        if (avgSPstHook > int(self.globalDataStorage.playersDB_ReadElement(spriteID, "SPstHook"))):
            clrSPstHook = belowAverageColor
        elif (avgSPstHook < int(self.globalDataStorage.playersDB_ReadElement(spriteID, "SPstHook"))):
            clrSPstHook = aboveAverageColor
        else:
            clrSPstHook = averageColor

        if (avgSOLowPost > int(self.globalDataStorage.playersDB_ReadElement(spriteID, "SOLowPost"))):
            clrSOLowPost = belowAverageColor
        elif (avgSOLowPost < int(self.globalDataStorage.playersDB_ReadElement(spriteID, "SOLowPost"))):
            clrSOLowPost = aboveAverageColor
        else:
            clrSOLowPost = averageColor

        if (avgSShtMed > int(self.globalDataStorage.playersDB_ReadElement(spriteID, "SShtMed"))):
            clrSShtMed = belowAverageColor
        elif (avgSShtMed < int(self.globalDataStorage.playersDB_ReadElement(spriteID, "SShtMed"))):
            clrSShtMed = aboveAverageColor
        else:
            clrSShtMed = averageColor

        if (avgSSht3PT > int(self.globalDataStorage.playersDB_ReadElement(spriteID, "SSht3PT"))):
            clrSSht3PT = belowAverageColor
        elif (avgSSht3PT < int(self.globalDataStorage.playersDB_ReadElement(spriteID, "SSht3PT"))):
            clrSSht3PT = aboveAverageColor
        else:
            clrSSht3PT = averageColor

        if (avgSShtInT > int(self.globalDataStorage.playersDB_ReadElement(spriteID, "SShtInT"))):
            clrSShtInT = belowAverageColor
        elif (avgSShtInT < int(self.globalDataStorage.playersDB_ReadElement(spriteID, "SShtInT"))):
            clrSShtInT = aboveAverageColor
        else:
            clrSShtInT = averageColor

        if (avgSShtOfD > int(self.globalDataStorage.playersDB_ReadElement(spriteID, "SShtOfD"))):
            clrSShtOfD = belowAverageColor
        elif (avgSShtOfD < int(self.globalDataStorage.playersDB_ReadElement(spriteID, "SShtOfD"))):
            clrSShtOfD = aboveAverageColor
        else:
            clrSShtOfD = averageColor

        if (avgSConsis > int(self.globalDataStorage.playersDB_ReadElement(spriteID, "SConsis"))):
            clrSConsis = belowAverageColor
        elif (avgSConsis < int(self.globalDataStorage.playersDB_ReadElement(spriteID, "SConsis"))):
            clrSConsis = aboveAverageColor
        else:
            clrSConsis = averageColor

        attributesFrame = customtkinter.CTkFrame(self.root)
        attributesFrame.place(x=1400,y=100,height=850, width=450)

        averagePretext = "Average: "
        shootThreeLabel = customtkinter.CTkLabel(attributesFrame, text="Shot 3PT: " + str(self.globalDataStorage.playersDB_ReadElement(spriteID,"SSht3PT")),font=customtkinter.CTkFont(family="Bahnschrift SemiBold", size=scoringFontSize),text_color=clrSSht3PT)
        shootThreeLabel.grid(column=0,row=0,pady = scoringPadY)
        CreateToolTip(shootThreeLabel, text=averagePretext + str(avgSSht3PT))

        shootMediumLabel = customtkinter.CTkLabel(attributesFrame, text="Shot Med: " + str(self.globalDataStorage.playersDB_ReadElement(spriteID,"SShtMed")),font=customtkinter.CTkFont(family="Bahnschrift SemiBold", size=scoringFontSize),text_color=clrSShtMed)
        shootMediumLabel.grid(column=1,row=0,pady = scoringPadY)
        CreateToolTip(shootMediumLabel, text=averagePretext + str(avgSShtMed))

        shootInTrafficLabel = customtkinter.CTkLabel(attributesFrame, text="SITraffic: " + str(self.globalDataStorage.playersDB_ReadElement(spriteID,"SShtInT")),font=customtkinter.CTkFont(family="Bahnschrift SemiBold", size=scoringFontSize),text_color=clrSShtInT)
        shootInTrafficLabel.grid(column=0,row=1,pady = scoringPadY)
        CreateToolTip(shootInTrafficLabel, text=averagePretext + str(avgSShtInT))

        shootOffDribbleLabel = customtkinter.CTkLabel(attributesFrame, text="SODribble: " + str(self.globalDataStorage.playersDB_ReadElement(spriteID,"SShtOfD")),font=customtkinter.CTkFont(family="Bahnschrift SemiBold", size=scoringFontSize),text_color=clrSShtOfD)
        shootOffDribbleLabel.grid(column=1,row=1,pady = scoringPadY)
        CreateToolTip(shootOffDribbleLabel, text=averagePretext + str(avgSShtOfD))

        lowPostOffenseLabel = customtkinter.CTkLabel(attributesFrame, text="LPOffense: " + str(self.globalDataStorage.playersDB_ReadElement(spriteID,"SOLowPost")),font=customtkinter.CTkFont(family="Bahnschrift SemiBold", size=scoringFontSize),text_color=clrSOLowPost)
        lowPostOffenseLabel.grid(column=0,row=2,pady = scoringPadY)
        CreateToolTip(lowPostOffenseLabel, text=averagePretext + str(avgSOLowPost))

        postHookLabel = customtkinter.CTkLabel(attributesFrame, text="PHook: " + str(self.globalDataStorage.playersDB_ReadElement(spriteID,"SPstHook")),font=customtkinter.CTkFont(family="Bahnschrift SemiBold", size=scoringFontSize),text_color=clrSPstHook)
        postHookLabel.grid(column=1,row=2,pady = scoringPadY)
        CreateToolTip(postHookLabel, text=averagePretext + str(avgSPstHook))

        postFadeawayLabel = customtkinter.CTkLabel(attributesFrame, text="PFade: " + str(self.globalDataStorage.playersDB_ReadElement(spriteID,"SPstFdaway")),font=customtkinter.CTkFont(family="Bahnschrift SemiBold", size=scoringFontSize),text_color=clrSPstFdaway)
        postFadeawayLabel.grid(column=0,row=3,pady = scoringPadY)
        CreateToolTip(postFadeawayLabel, text=averagePretext + str(avgSPstFdaway))

        layupLabel = customtkinter.CTkLabel(attributesFrame, text="Layup: " + str(self.globalDataStorage.playersDB_ReadElement(spriteID,"SLayUp")),font=customtkinter.CTkFont(family="Bahnschrift SemiBold", size=scoringFontSize),text_color=clrSLayUp)
        layupLabel.grid(column=1,row=3,pady = scoringPadY)
        CreateToolTip(layupLabel, text=averagePretext + str(avgSLayUp))

        shotCloseLabel = customtkinter.CTkLabel(attributesFrame, text="Shot Close: " + str(self.globalDataStorage.playersDB_ReadElement(spriteID,"SShtCls")),font=customtkinter.CTkFont(family="Bahnschrift SemiBold", size=scoringFontSize),text_color=clrSShtCls)
        shotCloseLabel.grid(column=0,row=4,pady = scoringPadY)
        CreateToolTip(shotCloseLabel, text=averagePretext + str(avgSShtCls))

        consistencyLabel = customtkinter.CTkLabel(attributesFrame, text="Consistency: " + str(self.globalDataStorage.playersDB_ReadElement(spriteID,"SConsis")),font=customtkinter.CTkFont(family="Bahnschrift SemiBold", size=scoringFontSize),text_color=clrSConsis)
        consistencyLabel.grid(column=1,row=4,pady = scoringPadY)
        CreateToolTip(consistencyLabel, text=averagePretext + str(avgSConsis))

        spacer1Label = customtkinter.CTkLabel(attributesFrame, text="==============================",font=customtkinter.CTkFont(family="Bahnschrift SemiBold", size=24))
        spacer1Label.grid(column=0, row=5, columnspan=2)

        offensiveReboundLabel = customtkinter.CTkLabel(attributesFrame, text="OffRebound: " + str(self.globalDataStorage.playersDB_ReadElement(spriteID,"SOReb")),font=customtkinter.CTkFont(family="Bahnschrift SemiBold", size=defensiveFontSize),text_color=clrSOReb)
        offensiveReboundLabel.grid(column=0,row=6,pady=defensivePadY)
        CreateToolTip(offensiveReboundLabel, text=averagePretext + str(avgSOReb))

        defensiveReboundLabel = customtkinter.CTkLabel(attributesFrame, text="DefRebound: " + str(self.globalDataStorage.playersDB_ReadElement(spriteID,"SDReb")),font=customtkinter.CTkFont(family="Bahnschrift SemiBold", size=defensiveFontSize),text_color=clrSDReb)
        defensiveReboundLabel.grid(column=1,row=6,pady=defensivePadY)
        CreateToolTip(defensiveReboundLabel, text=averagePretext + str(avgSDReb))

        onBallDefenseLabel = customtkinter.CTkLabel(attributesFrame, text="OBDefense: " + str(self.globalDataStorage.playersDB_ReadElement(spriteID,"SOnBallD")),font=customtkinter.CTkFont(family="Bahnschrift SemiBold", size=defensiveFontSize),text_color=clrSOnBallD)
        onBallDefenseLabel.grid(column=0,row=7,pady=defensivePadY)
        CreateToolTip(onBallDefenseLabel, text=averagePretext + str(avgSOnBallD))

        blockLabel = customtkinter.CTkLabel(attributesFrame, text="Block: " + str(self.globalDataStorage.playersDB_ReadElement(spriteID,"SBlock")),font=customtkinter.CTkFont(family="Bahnschrift SemiBold", size=defensiveFontSize),text_color=clrSBlock)
        blockLabel.grid(column=1,row=7,pady=defensivePadY)
        CreateToolTip(blockLabel, text=averagePretext + str(avgSBlock))

        strengthLabel = customtkinter.CTkLabel(attributesFrame, text="Strength: " + str(self.globalDataStorage.playersDB_ReadElement(spriteID,"SStrength")),font=customtkinter.CTkFont(family="Bahnschrift SemiBold", size=defensiveFontSize),text_color=clrSStrength)
        strengthLabel.grid(column=0,row=8,pady=defensivePadY)
        CreateToolTip(strengthLabel, text=averagePretext + str(avgSStrength))

        lowPostDefenseLabel = customtkinter.CTkLabel(attributesFrame, text="LPDefense: " + str(self.globalDataStorage.playersDB_ReadElement(spriteID,"SDLowPost")),font=customtkinter.CTkFont(family="Bahnschrift SemiBold", size=defensiveFontSize),text_color=clrSDLowPost)
        lowPostDefenseLabel.grid(column=1,row=8,pady=defensivePadY)
        CreateToolTip(lowPostDefenseLabel, text=averagePretext + str(avgSDLowPost))

        defensiveAwarenessLabel = customtkinter.CTkLabel(attributesFrame, text="DAware: " + str(self.globalDataStorage.playersDB_ReadElement(spriteID,"SDAwar")),font=customtkinter.CTkFont(family="Bahnschrift SemiBold", size=defensiveFontSize),text_color=clrSDAwar)
        defensiveAwarenessLabel.grid(column=0,row=9, columnspan=2,pady=defensivePadY)
        CreateToolTip(defensiveAwarenessLabel, text=averagePretext + str(avgSDAwar))

        spacer2Label = customtkinter.CTkLabel(attributesFrame, text="==============================",font=customtkinter.CTkFont(family="Bahnschrift SemiBold", size=24))
        spacer2Label.grid(column=0, row=10, columnspan=2)

        stealLabel = customtkinter.CTkLabel(attributesFrame, text="Steal: " + str(self.globalDataStorage.playersDB_ReadElement(spriteID,"SSteal")),font=customtkinter.CTkFont(family="Bahnschrift SemiBold", size=controlFontSize),text_color=clrSSteal)
        stealLabel.grid(column=0,row=11,pady=controlPadY)
        CreateToolTip(stealLabel, text=averagePretext + str(avgSSteal))

        hustleLabel = customtkinter.CTkLabel(attributesFrame, text="Hustle: " + str(self.globalDataStorage.playersDB_ReadElement(spriteID,"SHustle")),font=customtkinter.CTkFont(family="Bahnschrift SemiBold", size=controlFontSize),text_color=clrSHustle)
        hustleLabel.grid(column=1,row=11,pady=controlPadY)
        CreateToolTip(hustleLabel, text=averagePretext + str(avgSHustle))

        quicknessLabel = customtkinter.CTkLabel(attributesFrame, text="Quickness: " + str(self.globalDataStorage.playersDB_ReadElement(spriteID,"SQuick")),font=customtkinter.CTkFont(family="Bahnschrift SemiBold", size=controlFontSize),text_color=clrSQuick)
        quicknessLabel.grid(column=0,row=12,pady=controlPadY)
        CreateToolTip(quicknessLabel, text=averagePretext + str(avgSQuick))

        speedLabel = customtkinter.CTkLabel(attributesFrame, text="Speed: " + str(self.globalDataStorage.playersDB_ReadElement(spriteID,"SSpeed")),font=customtkinter.CTkFont(family="Bahnschrift SemiBold", size=controlFontSize),text_color=clrSSpeed)
        speedLabel.grid(column=1,row=12,pady=controlPadY)
        CreateToolTip(speedLabel, text=averagePretext + str(avgSSpeed))

        passLabel = customtkinter.CTkLabel(attributesFrame, text="Pass: " + str(self.globalDataStorage.playersDB_ReadElement(spriteID,"SPass")),font=customtkinter.CTkFont(family="Bahnschrift SemiBold", size=controlFontSize),text_color=clrSPass)
        passLabel.grid(column=0,row=13,pady=controlPadY)
        CreateToolTip(passLabel, text=averagePretext + str(avgSPass))

        ballSecurityLabel = customtkinter.CTkLabel(attributesFrame, text="BSecurity: " + str(self.globalDataStorage.playersDB_ReadElement(spriteID,"SBallSec")),font=customtkinter.CTkFont(family="Bahnschrift SemiBold", size=controlFontSize),text_color=clrSBallSec)
        ballSecurityLabel.grid(column=1,row=13,pady=controlPadY)
        CreateToolTip(ballSecurityLabel, text=averagePretext + str(avgSBallSec))

        ballHandlingLabel = customtkinter.CTkLabel(attributesFrame, text="BHandle: " + str(self.globalDataStorage.playersDB_ReadElement(spriteID,"SBallHndl")),font=customtkinter.CTkFont(family="Bahnschrift SemiBold", size=controlFontSize),text_color=clrSBallHndl)
        ballHandlingLabel.grid(column=0,row=14,pady=controlPadY)
        CreateToolTip(ballHandlingLabel, text=averagePretext + str(avgSBallHndl))

        offensiveAwarenessLabel = customtkinter.CTkLabel(attributesFrame, text="OAware: " + str(self.globalDataStorage.playersDB_ReadElement(spriteID,"SOAwar")),font=customtkinter.CTkFont(family="Bahnschrift SemiBold", size=controlFontSize),text_color=clrSOAwar)
        offensiveAwarenessLabel.grid(column=1,row=14,pady=controlPadY)
        CreateToolTip(offensiveAwarenessLabel, text=averagePretext + str(avgSOAwar))

        handsLabel = customtkinter.CTkLabel(attributesFrame, text="Hands: " + str(self.globalDataStorage.playersDB_ReadElement(spriteID,"SHands")),font=customtkinter.CTkFont(family="Bahnschrift SemiBold", size=controlFontSize),text_color=clrSHands)
        handsLabel.grid(column=0,row=15,pady=controlPadY)
        CreateToolTip(handsLabel, text=averagePretext + str(avgSHands))

        offHandDribblingLabel = customtkinter.CTkLabel(attributesFrame, text="OHDribble: " + str(self.globalDataStorage.playersDB_ReadElement(spriteID,"SOffHDrib")),font=customtkinter.CTkFont(family="Bahnschrift SemiBold", size=controlFontSize),text_color=clrSOffHDrib)
        offHandDribblingLabel.grid(column=1,row=15,pady=controlPadY)
        CreateToolTip(offHandDribblingLabel, text=averagePretext + str(avgSOffHDrib))

        spacer3Label = customtkinter.CTkLabel(attributesFrame, text="==============================",font=customtkinter.CTkFont(family="Bahnschrift SemiBold", size=24))
        spacer3Label.grid(column=0, row=16, columnspan=2)

        shotInsideLabel = customtkinter.CTkLabel(attributesFrame, text="Shot Inside: " + str(self.globalDataStorage.playersDB_ReadElement(spriteID,"SShtIns")) + " ",font=customtkinter.CTkFont(family="Bahnschrift SemiBold", size=16, slant="italic"),text_color=clrSShtIns)
        shotInsideLabel.grid(column=0,row=17,pady=1,padx=5,columnspan=2)
        CreateToolTip(shotInsideLabel, text=averagePretext + str(avgSShtIns))

        dunkLabel = customtkinter.CTkLabel(attributesFrame, text="Dunk: " + str(self.globalDataStorage.playersDB_ReadElement(spriteID,"SDunk")) + " ",font=customtkinter.CTkFont(family="Bahnschrift SemiBold", size=16, slant="italic"),text_color=clrSDunk)
        dunkLabel.grid(column=0,row=18,pady=1,padx=5,columnspan=2)
        CreateToolTip(dunkLabel, text=averagePretext + str(avgSDunk))

        standingDunkLabel = customtkinter.CTkLabel(attributesFrame, text="StandDunk: " + str(self.globalDataStorage.playersDB_ReadElement(spriteID,"SStdDunk")) + " ",font=customtkinter.CTkFont(family="Bahnschrift SemiBold", size=16, slant="italic"),text_color=clrSStdDunk)
        standingDunkLabel.grid(column=0,row=19,pady=1,padx=5,columnspan=2)
        CreateToolTip(standingDunkLabel, text=averagePretext + str(avgSStdDunk))

        verticalLabel = customtkinter.CTkLabel(attributesFrame, text="Vertical: " + str(self.globalDataStorage.playersDB_ReadElement(spriteID,"SVertical")) + " ",font=customtkinter.CTkFont(family="Bahnschrift SemiBold", size=16, slant="italic"),text_color=clrSVertical)
        verticalLabel.grid(column=0,row=20,pady=1,padx=5,columnspan=2)
        CreateToolTip(verticalLabel, text=averagePretext + str(avgSVertical))

        playerHeight = float(self.globalDataStorage.playersDB_ReadElement(spriteID, "Height")) /2.54
        playerHeightStr = str(int(playerHeight/12)) + "'" + str(int((playerHeight % 12))) + " "

        heightLabel = customtkinter.CTkLabel(attributesFrame, text="Height: " + playerHeightStr,font=customtkinter.CTkFont(family="Bahnschrift SemiBold", size=16, slant="italic"))
        heightLabel.grid(column=0,row=21,pady=1,padx=5,columnspan=2)

        artifactFrame = customtkinter.CTkFrame(self.root)
        artifactFrame.place(x=100,y=100)

        artifactName = self.globalDataStorage.playersDB_ReadElement(spriteID, "ArtifactName")
        artifactLabel = customtkinter.CTkLabel(artifactFrame, text=artifactName,font=customtkinter.CTkFont(family="Bahnschrift SemiBold", size=20), text_color="White", wraplength=400, justify="center")
        artifactLabel.grid(column=0,row=0)

        artifactDesc = self.globalDataStorage.playersDB_ReadElement(spriteID, "ArtifactDesc")
        CreateToolTip(artifactLabel, artifactDesc)

        mainMenuButton = customtkinter.CTkButton(self.root, text="Main Menu", command=self.goToMainMenu,font=customtkinter.CTkFont(family="Bahnschrift SemiBold", size=30), fg_color="#2eb217")
        mainMenuButton.place(x=860, y=1000)

    # Stat Report Menu methods.
    def goToGenStatReportMenu(self):
        self.wipeScreen("StatReportMenu")

        self.root.geometry("400x300+650+250")

        nba2k_Label = Label(self.root, image=self.nba2k_Logo)
        nba2k_Label.photo = self.nba2k_Logo
        nba2k_Label.grid(column=0, row=0, columnspan=3)

        fontSize=25

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background="black", fieldbackground="black", foreground="white", highlightthickness=0, bd=0,font=('Segoe UI', 14), rowheight=30)  # Modify the font of the body
        style.configure("Treeview.Heading", font=('Segoe UI', 16, 'bold'))  # Modify the font of the headings
        style.layout("Treeview", [('Treeview.treearea', {'sticky': 'nswe'})])  # Remove the borders

        allColumns = ['Name', 'Arch', 'Games',"Wins", 'PPG', 'RPG', 'APG', 'SPG', 'TPG', 'FGM', 'FGA', 'FG%', '3PM', '3PA', '3P%', 'Points', 'Rbds', 'Assists', 'Steals', 'Blocks','Win%']
        columnDataTypes = ["str","str","int","int","float","float","float","float","float","float","float","float","float","float","float","int","int","int","int","int","float"]
        thisSet = ttk.Treeview(self.root,columns=allColumns,selectmode="extended",show='headings',height=25)
        thisSet.place(x=50,y=100,width=1800)
        counter = 0
        for column in allColumns:
            if(column == "Sprite ID"):
                widthVal = 100
            elif(column == "Name"):
                widthVal = 200
            elif (column == "Arch"):
                widthVal = 100
            else:
                widthVal = 80
            thisSet.heading(column,text = column, command = lambda _dt = columnDataTypes[counter], _col = column: self.tableSort(thisSet,_col,False,_dt))
            thisSet.column(column,anchor=CENTER,width=widthVal)
            counter += 1



        horizontalScroll = ttk.Scrollbar(self.root, orient="horizontal", command=thisSet.xview)
        horizontalScroll.place(x=50, y=890, width=1800)
        thisSet.configure(xscrollcommand=horizontalScroll.set)
        verticalScroll = ttk.Scrollbar(self.root, orient="vertical", command=thisSet.yview)
        verticalScroll.place(x=1850, y=100, height=790)
        thisSet.configure(yscrollcommand=verticalScroll.set)


        # ========================================
        # ============FILTERS AND FUN=============
        # ========================================


        rosterOptions = ["All","Premier","Wild"]
        rosterFilterVar = StringVar(None)
        rosterFilterVar.set("Premier")
        def editRosterFilter():
            if(rosterFilterVar.get() == "All"):
                self.tableStats_RosterFilter = None
            else:
                self.tableStats_RosterFilter = rosterFilterVar.get() + ".ROS"
            self.genStatTable(self.getTableStats(),thisSet)
        rosterFilterMenu = OptionMenu(self.root, rosterFilterVar, *rosterOptions, command= lambda x: editRosterFilter())
        rosterFilterMenu.place(x=100,y=915)
        rosterFilterMenuConfig = self.root.nametowidget(rosterFilterMenu.menuname)
        rosterFilterMenuConfig.config(font=tkFont.Font(family='Helvetica', size=25))
        rosterFilterMenu.config(bg="#36393e", fg="WHITE", highlightthickness=0, font=tkFont.Font(family='Helvetica', size=25))
        rosterFilterMenu["menu"].config(bg="#36393e", fg="WHITE")

        technicianOptions = ["Any","Alex","Danny"]
        technicianFilterVar = StringVar(None)
        technicianFilterVar.set("Any")
        def editTechnicianFilter():
            if(technicianFilterVar.get() == "Any"):
                self.tableStats_TechnicianFilter = None
            else:
                self.tableStats_TechnicianFilter = technicianFilterVar.get()
            self.genStatTable(self.getTableStats(),thisSet)
        technicianMenu = OptionMenu(self.root, technicianFilterVar, *technicianOptions, command= lambda x: editTechnicianFilter())
        technicianMenu.place(x=300,y=915)
        technicianMenuConfig = self.root.nametowidget(rosterFilterMenu.menuname)
        technicianMenuConfig.config(font=tkFont.Font(family='Helvetica', size=25))
        technicianMenu.config(bg="#36393e", fg="WHITE", highlightthickness=0, font=tkFont.Font(family='Helvetica', size=25))
        technicianMenu["menu"].config(bg="#36393e", fg="WHITE")

        gameMinVar = StringVar(None)
        def editGameMinFilter():
            if(gameMinVar.get() == ""):
                self.tableStats_GameMin = None
                self.genStatTable(self.getTableStats(),thisSet)
            else:
                self.tableStats_GameMin = int(gameMinVar.get())
                self.genStatTable(self.getTableStats(),thisSet)
        gameMinEntry = customtkinter.CTkEntry(self.root, textvariable=gameMinVar, width=400, font=customtkinter.CTkFont(family="Helvetica", size=25))
        gameMinEntry.place(x=450, y=915,width=100)


        gameCutoffVar = StringVar(None)
        def editGameCutoffFilter():
            if(gameCutoffVar.get() == ""):
                self.tableStats_GameCutoff = None
                self.genStatTable(self.getTableStats(),thisSet)
            else:
                self.tableStats_GameCutoff = int(gameCutoffVar.get())
                self.genStatTable(self.getTableStats(),thisSet)
        gameCutoffEntry = customtkinter.CTkEntry(self.root, textvariable=gameCutoffVar, width=400, font=customtkinter.CTkFont(family="Helvetica", size=25))
        gameCutoffEntry.place(x=450, y=985,width=100)


        def submitFilters():
            editGameMinFilter()
            editGameCutoffFilter()
        submitFiltersButton = customtkinter.CTkButton(self.root, text="Submit", command=submitFilters,font=customtkinter.CTkFont(family="Bahnschrift SemiBold", size=fontSize),fg_color="#2eb217")
        submitFiltersButton.place(x=800,y=1015)


        self.genStatTable(self.getTableStats(),thisSet)

        mainMenuButton = customtkinter.CTkButton(self.root, text="Main Menu", command=self.goToMainMenu,font=customtkinter.CTkFont(family="Bahnschrift SemiBold", size=fontSize),fg_color="#2eb217")
        mainMenuButton.place(x=800,y=915)
    # Helper method to quickly return relevant table stats.
    def getTableStats(self):
        if(self.tableStats_RosterFilter is None):
            spriteIDList = list(range(0, self.globalDataStorage.playersDB_GetPlayerCount()))
        else:
            spriteIDList = list(self.globalDataStorage.csvRosterDict[self.tableStats_RosterFilter.split(".ROS")[0]]["SpriteIDs"].values())

        fullStatsDict = self.globalDataStorage.statsDB_ReadTotalStat(spriteID=spriteIDList, statisticName=TABLE_STATS, gameCutoff=self.tableStats_GameCutoff, rosterFilter=self.tableStats_RosterFilter,technicianFilter=self.tableStats_TechnicianFilter)
        for thisSpriteID in spriteIDList:
            if(self.tableStats_GameMin is not None):
                if(fullStatsDict[thisSpriteID]["IsActive"] < self.tableStats_GameMin):
                    fullStatsDict.pop(thisSpriteID)

        return fullStatsDict

    def genStatTable(self,playerProfileList, tableSet):
        for item in tableSet.get_children():
            tableSet.delete(item)

        counter = 0
        for spriteID, statDict in playerProfileList.items():
            tableSet.insert(parent='', index='end', iid=counter, text='',
                       values=(h.getFullPlayerName(spriteID,dataStorageObject=self.globalDataStorage),
                               self.globalDataStorage.playersDB_ReadElement(spriteID,"Archetype"),
                               statDict["IsActive"],
                               statDict["Wins"],
                               round(statDict["Points"] / statDict["IsActive"],1) if statDict["IsActive"] != 0 else 0.0,
                               round((statDict["OffensiveRebounds"] + statDict["DefensiveRebounds"]) / statDict["IsActive"],1) if statDict["IsActive"] != 0 else 0.0,
                               round(statDict["AssistCount"] / statDict["IsActive"],1) if statDict["IsActive"] != 0 else 0.0,
                               round(statDict["Steals"] / statDict["IsActive"],1) if statDict["IsActive"] != 0 else 0.0,
                               round(statDict["Turnovers"] / statDict["IsActive"],1) if statDict["IsActive"] != 0 else 0.0,
                               round(statDict["InsidesMade"] / statDict["IsActive"],1) if statDict["IsActive"] != 0 else 0.0,
                               round(statDict["InsidesAttempted"] / statDict["IsActive"],1) if statDict["IsActive"] != 0 else 0.0,
                               round(statDict["InsidesMade"] / statDict["InsidesAttempted"] * 100,1) if statDict["InsidesAttempted"] != 0 else 0.0,
                               round(statDict["ThreesMade"] / statDict["IsActive"],1) if statDict["IsActive"] != 0 else 0.0,
                               round(statDict["ThreesAttempted"] / statDict["IsActive"],1) if statDict["IsActive"] != 0 else 0.0,
                               round(statDict["ThreesMade"] / statDict["ThreesAttempted"] * 100,1) if statDict["ThreesAttempted"] != 0 else 0.0,
                               statDict["Points"],
                               statDict["OffensiveRebounds"] + statDict["DefensiveRebounds"],
                               statDict["AssistCount"],
                               statDict["Steals"],
                               statDict["Blocks"],
                               round(statDict["Wins"] / statDict["IsActive"] * 100,1) if statDict["IsActive"] != 0 else 0.0))
            counter += 1

    def tableSort(self,treeview,sortByColumn,isReverse,dataType):

        sortList = []
        value = None
        for child in treeview.get_children(''):
            if (dataType == "str"):
                value = treeview.set(child,sortByColumn)
            elif (dataType == "int"):
                value = int(treeview.set(child,sortByColumn))
            elif (dataType == "float"):
                value = float(treeview.set(child,sortByColumn))
            sortList.append((value,child))

        sortList.sort(reverse=isReverse)

        # rearrange items in sorted positions
        for index, (value, childNum) in enumerate(sortList):
            treeview.move(childNum, '', index)

        # reverse sort next time
        treeview.heading(sortByColumn, command=lambda: self.tableSort(treeview, sortByColumn, not isReverse,dataType))

    # DEPRECATED FUNCTION. Stats ripping is handled by secondary loop and
    # checkGameStatus function now.
    @staticmethod
    def ripStats():
        messagebox.showinfo(title="Wow", message="How does it feel to be a moron?")
        '''
        try:
            d = DataStorage.DataStorage()
            stats = StatsRipper.StatsRipper()
            stats.attachTo2K()
            stats.ripAllStats()
            newGameID = d.statsTable_AddBlankGame()
            d.statsTable_Save()
            d.statsTable_UpdateGameStatsFromObject(newGameID, stats)
            d.statsTable_Save()
            messagebox.showinfo(title="Success!", message="Stats from the current game were read in!")
        except:
            messagebox.showinfo(title="You're an idiot!", message="Fuck you, that didn't work. Open 2k.")
        '''

    # This function simply opens NBA2k13.exe (the game itself). If there are any outgoing changes that
    # need to be saved first, it instead displays an error message.
    def open_2k13(self):
        if(len(self.outgoingChanges) > 0):
            messagebox.showinfo(title="Uhhhh...", message="Bottom left of the screen. Read it. Then read it again.")
        else:
            os.system(f"{b.paths.gameInstall}\\nba2k13.exe")
    # This function handles both incoming and outgoing save functions for data management. This function
    # is run when the user clicks "save data" and it intelligently determines whether to do an incoming
    # or outgoing save.
    def saveData(self):
        if(len(self.outgoingChanges) > 0):
            if(len(self.incomingChanges) > 0):
                messagebox.showerror(title="SERIOUS WARNING", message="This should NEVER EVER HAPPEN. An outgoing AND incoming change has been detected - please manually correct before proceeding.")

            processedRosters = []
            for rosterToExport in self.outgoingChanges:
                if(rosterToExport not in processedRosters):
                    b.backup(f"{b.paths.rosters}\\{rosterToExport}.ROS", f"{b.paths.backups}\\RosterBackups\\{rosterToExport}",10)
                    processedRosters.append(rosterToExport)
                    h.saveCSVChangesToFiles(rosterToExport,dataStorageObject=self.globalDataStorage)
                    h.exportRosterData(rosterName=rosterToExport,dataStorageObject=self.globalDataStorage)
            self.outgoingChanges = []
            messagebox.showinfo(title="Bazinga!", message="Outgoing changes have been saved!")
        elif(len(self.incomingChanges) > 0):
            if(self.hasSavedRoster == False):
                messagebox.showerror(title="Unbelievable.", message="Hey super-genius, you might wanna, you know, save the actual IN GAME ROSTER first?")

            processedRosters = []
            for rosterToImport in self.incomingChanges:
                if(rosterToImport not in processedRosters):
                    processedRosters.append(rosterToImport)
                    h.importRosterData(rosterName=rosterToImport.split(".ROS")[0],dataStorageObject=self.globalDataStorage)
                    # If this Roster is marked to have CAP info ripped and sent to Players.xml, we do that here.
                    if(rosterToImport.split(".ROS")[0] in b.config["loading"]["CAPRosters"]):
                        b.backup(f"{b.paths.databases}\\Players.db",f"{b.paths.backups}\\PlayerData",20)
                        #if(str(self.globalDataStorage.loadedRosterName).split(".ROS")[0] != rosterToImport.split(".ROS")[0]):
                        print("importing this mothafucka: " + str(rosterToImport))
                        allSpriteIDsInRoster = self.globalDataStorage.csvRosterDict[rosterToImport.split(".ROS")[0]]["SpriteIDs"].values()
                        for spriteID in allSpriteIDsInRoster:
                            if(spriteID != -1):
                                h.updateCAPInfoFromRosterSet("Premier",spriteID,dataStorageObject=self.globalDataStorage)
            self.incomingChanges = []
            messagebox.showinfo(title="Bazinga!", message="Incoming changes have been saved!")
        else:
            messagebox.showerror(title="Are you stupid?", message="There's literally nothing to save.")

    # This method simply manages going back to the previous menu.
    def goToPreviousMenu(self):
        if(self.previousScreen == "MainMenu"):
            self.goToMainMenu()
        elif(self.previousScreen == "ModesMenu"):
            self.goToPlayMenu()
        elif(self.previousScreen.startswith("PickerMenu")):
            self.goToPickerMenu(self.previousScreen.split("|")[1])
        elif(self.previousScreen == "CAPMenu"):
            self.goToCAPMenu()
        elif(self.previousScreen == "PlayerSearchMenu"):
            self.goToSearchMenu()
        elif(self.previousScreen.startswith == "PlayerFile"):
            self.goToPlayerFile()
        elif(self.previousScreen == "StatReportMenu"):
            self.goToGenStatReportMenu()
        else:
            self.goToMainMenu()

    # This helper function simply wipes the entire screen of all elements.
    def wipeScreen(self,newMenu,wipeSave : bool = False,wipeHeader : bool = False):
        self.previousScreen = self.currentScreen
        self.currentScreen = newMenu


        self.isOnPlayerPicker = False
        self.searchMenu_ResetFilters()

        pygame.mixer.music.stop()

        for forgetRoot in self.root.grid_slaves():
            forgetRoot.grid_forget()

        for widget in self.root.winfo_children():
            widget.forget()

        for forgetPlace in self.root.place_slaves():
            if(wipeSave):
                if (forgetPlace == self.saveButton or forgetPlace == self.saveLabel):
                    continue
            forgetPlace.place_forget()

        if(self.mediaPlayer is not None):
            self.mediaPlayer.stop()
            self.mediaPlayer = None



    # Here are listed the secondary loop, and all of its submethods.
    #
    # updateSaveGameButton - Simply updates the saveGameButton to check if new changes have been made.
    # checkGameStatus - Checks the game to see if the game is loaded, what screen we're on, whether to save game data, and whether to append incoming changes.
    # updatePlayerPicker - This dynamically updates the in-game Player Picker with players picked in the GUI, as long as the GUI is currently on the picker screen.
    def secondaryLoop(self):
        self.updateSaveGameButton()
        self.checkGameStatus()

        self.root.after(500,self.secondaryLoop)
    def updateSaveGameButton(self):
        # This block updates the save button.
        if (len(self.outgoingChanges) > 0):
            self.saveButton.configure(fg_color="#2eb217")
            self.saveButton.configure(text_color="white")
            self.saveLabel.configure(text="There are " + str(len(self.outgoingChanges)) + " pending changes!")
        elif (len(self.incomingChanges) > 0):
            self.saveButton.configure(fg_color="#2eb217")
            self.saveButton.configure(text_color="white")
            self.saveLabel.configure(text="There are " + str(len(self.incomingChanges)) + " unsaved Rosters!")
        else:
            self.saveButton.configure(fg_color="#535454")
            self.saveButton.configure(text_color="grey")
            self.saveLabel.configure(text="")
        self.saveLabel.update()
        self.saveButton.update()
    def checkGameStatus(self):
        gameIsOpen = self.statsRipper.attachTo2K()
        if(gameIsOpen):
            activeRoster = self.statsRipper.getActiveRoster()
            if(activeRoster != self.lastOpenRoster):
                self.lastOpenRoster = activeRoster

            currentScreen = self.statsRipper.getMenuScreen()
            inGame = self.statsRipper.testInGame()
            if(inGame):
                self.isGameActive = True
            else:
                # This rare scenario means the game was closed before being one. By default,
                # saving in this case is disabled, but supported.
                '''
                if(self.isGameActive):
                    if(not self.isGameSaved):
                        d = DataStorage.DataStorage()
                        newGameID = d.statsTable_AddBlankGame()
                        d.statsTable_Save()
                        d.statsTable_UpdateGameStatsFromObject(newGameID, self.statsRipper)
                        d.statsTable_Save()
                '''
                self.isGameActive = False
                self.isGameSaved = False


            # Here we make sure values are consistent in case of closings or crashes.
            if(currentScreen != "InGame"):
                if(self.isCoinGiven):
                    self.isCoinGiven = False
                if(self.isGameWon):
                    self.isGameWon = False

            if(currentScreen == "CreatePlayer"):
                self.hasSavedRoster = False
                if (activeRoster != "UNOPENED" and activeRoster != "NONE"):
                    if (activeRoster not in self.incomingChanges):
                        self.incomingChanges.append(activeRoster)
            elif(currentScreen == "InGame"):
                # Once isGameWon is set to True, the game MUST be exited for it to be set
                # to false.
                if(not self.isGameWon):
                    self.isGameWon = self.statsRipper.testIfGameIsWon()
                self.statsRipper.manuallyUpdatePointDisplay()
                if(not self.isGameWon and not self.isCoinGiven):
                    print("WELL HOWDY")
                    self.isCoinGiven = True
                    gameMode = self.statsRipper.getBlacktopMode()
                    if(gameMode >= 4):
                        self.statsRipper.addCoin("Alex")
                    else:
                        self.statsRipper.addCoin("Danny")
                if(self.isGameWon):
                    if(self.isCoinGiven):
                        self.isCoinGiven = False
                        gameMode = self.statsRipper.getBlacktopMode()
                        if (gameMode >= 4):
                            self.statsRipper.removeCoin("Alex")
                        else:
                            self.statsRipper.removeCoin("Danny")
                    self.statsRipper.manuallyUpdatePointDisplay()
                    if(self.isGameSaved == False):
                        b.backup(f"{b.paths.databases}\\Stats.db",f"{b.paths.backups}\\StatsData",30)
                        self.statsRipper.ripAllStats()
                        self.isGameSaved = True
                        self.globalDataStorage.statsDB_AddRippedGame(self.statsRipper)
                        pygame.mixer.music.load(f"{b.paths.media}\\Common.ogg")
                        pygame.mixer.music.play(loops=0)
                        pygame.mixer.music.set_volume(0.075)

            elif(currentScreen == "SaveRoster"):
                self.hasSavedRoster = True
            elif(currentScreen == "LoadRoster"):
                if(len(self.incomingChanges) > 0):
                    if(self.hasSavedRoster == False):
                        messagebox.showerror(title="UH, HELLO!", message="Hey, idiot, looks like you're trying to load a Roster when you might've made changes to the currently loaded roster. Might wanna double check what you're doing.")
            elif(currentScreen == "PickUp"):
                if(self.isOnPlayerPicker):
                    self.updatePlayerPicker()



        else:
            pass
    def updatePlayerPicker(self):
        currentMode = self.statsRipper.getBlacktopMode()

        playerDictToLoad = {
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
        if(len(self.dannyPicks) >= 1):
            playerDictToLoad["Slot1"] = int(self.globalDataStorage.csv_GetRosterIDFromSpriteID(self.pickerRoster,self.dannyPicks[0]))
        if(len(self.dannyPicks) >= 2 and currentMode >= 2):
            playerDictToLoad["Slot2"] = int(self.globalDataStorage.csv_GetRosterIDFromSpriteID(self.pickerRoster,self.dannyPicks[1]))
        if(len(self.dannyPicks) >= 3 and currentMode >= 3):
            playerDictToLoad["Slot3"] = int(self.globalDataStorage.csv_GetRosterIDFromSpriteID(self.pickerRoster,self.dannyPicks[2]))
        if(len(self.dannyPicks) >= 4 and currentMode >= 4):
            playerDictToLoad["Slot4"] = int(self.globalDataStorage.csv_GetRosterIDFromSpriteID(self.pickerRoster,self.dannyPicks[3]))
        if(len(self.dannyPicks) >= 5 and currentMode == 5):
            playerDictToLoad["Slot5"] = int(self.globalDataStorage.csv_GetRosterIDFromSpriteID(self.pickerRoster,self.dannyPicks[4]))

        if(len(self.alexPicks) >= 1):
            playerDictToLoad["Slot6"] = int(self.globalDataStorage.csv_GetRosterIDFromSpriteID(self.pickerRoster,self.alexPicks[0]))
        if(len(self.alexPicks) >= 2 and currentMode >= 2):
            playerDictToLoad["Slot7"] = int(self.globalDataStorage.csv_GetRosterIDFromSpriteID(self.pickerRoster,self.alexPicks[1]))
        if(len(self.alexPicks) >= 3 and currentMode >= 3):
            playerDictToLoad["Slot8"] = int(self.globalDataStorage.csv_GetRosterIDFromSpriteID(self.pickerRoster,self.alexPicks[2]))
        if(len(self.alexPicks) >= 4 and currentMode >= 4):
            playerDictToLoad["Slot9"] = int(self.globalDataStorage.csv_GetRosterIDFromSpriteID(self.pickerRoster,self.alexPicks[3]))
        if(len(self.alexPicks) >= 5 and currentMode == 5):
            playerDictToLoad["Slot10"] = int(self.globalDataStorage.csv_GetRosterIDFromSpriteID(self.pickerRoster,self.alexPicks[4]))

        self.statsRipper.loadBlacktopPlayers(playerDictToLoad)


    # The main loop is essentially a wrapper function for the GUI main loop, as well as
    # opening a new thread to run the secondary loop on.
    def runMainLoop(self):
        secondaryThread = threading.Thread(self.secondaryLoop())
        secondaryThread.start()
        self.root.mainloop()



class ToolTip(object):

    def __init__(self, widget):
        self.widget = widget
        self.tipwindow = None
        self.id = None
        self.x = self.y = 0
        self.text = ""

    def showtip(self, text):
        # Display text in tooltip window
        self.text = text
        if self.tipwindow or not self.text:
            return
        x, y, cx, cy = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + 80
        y = y + cy + self.widget.winfo_rooty() +0
        self.tipwindow = tw = Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry("+%d+%d" % (x, y))
        label = Label(tw, text=self.text, justify=LEFT,
                      background="#ffffe0", relief=SOLID, borderwidth=1,
                      font=("Calibri", "16", "normal"),wraplength=500)
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()
def CreateToolTip(widget, text):
    toolTip = ToolTip(widget)
    def enter(event):
        toolTip.showtip(text)
    def leave(event):
        toolTip.hidetip()
    widget.bind('<Enter>', enter)
    widget.bind('<Leave>', leave)
