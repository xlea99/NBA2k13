from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import tkinter.font as tkFont
import customtkinter
import os
from PIL import ImageTk,Image
import Player
import DataStorage
import BaseFunctions as b




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

GRAPHICS_PATH = b.readConfigValue("alexGraphicsPath")
ICON_PATH = GRAPHICS_PATH + "\\sprite.ico"
LOGO_PATH = GRAPHICS_PATH + "\\2kMASSIVE_1920_329.png"
READER_PATH = GRAPHICS_PATH + "\\2kReader.png"

class GUI:

    def __init__(self,openRoot=True):
        customtkinter.set_appearance_mode("System")  # Modes: system (default), light, dark
        customtkinter.set_default_color_theme("green")  # Themes: blue (default), dark-blue, green

        self.__root = None
        self.__root = None
        if(openRoot):
            self.openRoot()

    def openRoot(self):
        self.__root = customtkinter.CTk()
        self.__root.title("Spritopia Presents:")
        self.__root.geometry("310x400+650+250")
        self.__root.iconbitmap(ICON_PATH)

    # Main menu methods
    def goToMainMenu(self):
        for forgetRoot in self.__root.grid_slaves():
            forgetRoot.grid_forget()
        self.__root.attributes('-fullscreen', True)

        nba2k_Logo = ImageTk.PhotoImage(Image.open(READER_PATH))
        nba2k_Label = Label(self.__root, image=nba2k_Logo)
        nba2k_Label.photo = nba2k_Logo
        nba2k_Label.grid(column=0,row=0,columnspan=3)

        lebronLogo = ImageTk.PhotoImage(Image.open(GRAPHICS_PATH + "\\lebronSpriteTime.png"))
        lebronLabel = Label(self.__root, image=lebronLogo)
        lebronLabel.photo = lebronLogo
        lebronLabel.grid(column=0, row=1, rowspan=4)

        fontSize = 60

        TwokButton = customtkinter.CTkButton(self.__root, text="Play 2k13", command=self.open_2k13, text_font=tkFont.Font(family="Bahnschrift SemiBold", size=fontSize), fg_color="#2eb217")
        TwokButton.grid(column=1,row=1,padx=10, pady=30)

        capMenuButton = customtkinter.CTkButton(self.__root, text="Create a Player", command=self.goToCAPMenu, text_font=tkFont.Font(family="Bahnschrift SemiBold", size=fontSize), fg_color="#2eb217")
        capMenuButton.grid(column=1,row=2,padx=10, pady=30)

        searchButton = customtkinter.CTkButton(self.__root, text='Search', command=self.goToSearchMenu, text_font=tkFont.Font(family="Bahnschrift SemiBold", size=fontSize), fg_color="#2eb217")
        searchButton.grid(column=1,row=3,padx=10, pady=30)

        genStatReportButton = customtkinter.CTkButton(self.__root, text='Generate Stats Report', command=self.goToGenStatReportMenu, text_font=tkFont.Font(family="Bahnschrift SemiBold", size=fontSize), fg_color="#2eb217")
        genStatReportButton.grid(column=1,row=4,padx=10, pady=30)

        exitButton = customtkinter.CTkButton(self.__root, text="Quit", command=self.__root.destroy, text_font=tkFont.Font(family="Bahnschrift SemiBold", size=fontSize), fg_color="#2eb217")
        exitButton.grid(column=1, row=5, padx=10, pady=30)

    # CAP menu methods.
    def goToCAPMenu(self):

        for forgetRoot in self.__root.grid_slaves():
            forgetRoot.grid_forget()
        self.__root.geometry("345x400+650+250")

        nba2k_Logo = ImageTk.PhotoImage(Image.open(READER_PATH))
        nba2k_Label = Label(self.__root, image=nba2k_Logo)
        nba2k_Label.photo = nba2k_Logo
        nba2k_Label.grid(column=0, row=0, columnspan=3)

        fontSize = 45
        fontSizeEntry = 25

        fnLabel = StringVar()
        fnLabel.set("Enter First Name:")

        fnLabelDir = customtkinter.CTkLabel(self.__root, textvariable=fnLabel, height=2,text_font=tkFont.Font(family="Bahnschrift SemiBold", size=fontSize))
        fnLabelDir.grid(column=1,row=1,padx=100, pady=15)

        fnName = StringVar(None)
        fnNameEntry = customtkinter.CTkEntry(self.__root, textvariable=fnName, width=400, text_font=tkFont.Font(family="Bahnschrift", size=fontSizeEntry))
        fnNameEntry.grid(column=1,row=2,padx=100, pady=15)

        lnLabel = StringVar()
        lnLabel.set("Enter Last Name:")
        lnLabelDir = customtkinter.CTkLabel(self.__root, textvariable=lnLabel, height=2,text_font=tkFont.Font(family="Bahnschrift SemiBold", size=fontSize))
        lnLabelDir.grid(column=1,row=3,padx=100, pady=15)

        lnName = StringVar(None)
        lnNameEntry = customtkinter.CTkEntry(self.__root, textvariable=lnName, width=400, text_font=tkFont.Font(family="Bahnschrift", size=fontSizeEntry))
        lnNameEntry.grid(column=1,row=4,padx=100, pady=15)

        # This is the important variable to .get()
        archetype = StringVar(None)
        archetype.set("Slayer")
        # This is the actual dropdown menu
        dropArchetype = OptionMenu(self.__root, archetype, *ARCHETYPE_OPTIONS)
        # dropArchetype.grid(column=0,row=0,padx=10,pady=10)
        dropArchetype.grid(column=1,row=5,padx=100, pady=15)

        # This is the important variable to .get()
        heightVar = StringVar(None)
        heightVar.set("6'0")
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
            "7'6"
        ]
        # This is the actual dropdown menu
        dropHeight = OptionMenu(self.__root, heightVar, *heightOptions)
        # dropHeight.grid(column=0,row=0,padx=10,pady=10)
        dropHeight.grid(column=1,row=6,padx=100, pady=15)



        submitButton = customtkinter.CTkButton(self.__root, text="Submit", command=lambda: self.CAPMenu_SubmitCAP(fnName.get(),lnName.get(),archetype.get(),heightVar.get()),text_font=tkFont.Font(family="Bahnschrift SemiBold", size=fontSize), fg_color="#2eb217")
        # submitButton.grid(column=0,row=0,padx=10,pady=10)1,row=4, pady=10)
        submitButton.grid(column=1,row=7,padx=100, pady=15)
        mainMenuButton = customtkinter.CTkButton(self.__root, text="Main Menu", command=self.goToMainMenu,text_font=tkFont.Font(family="Bahnschrift SemiBold", size=fontSize), fg_color="#2eb217")
        mainMenuButton.grid(column=1,row=8,padx=100, pady=15)

        # This is for color configuration
        dropFont = tkFont.Font(family='Helvetica', size=35)
        archetypeMenuFont = tkFont.Font(family='Helvetica', size=25)
        heightMenuFont = tkFont.Font(family='Helvetica', size=20)

        archetypeMenu = self.__root.nametowidget(dropArchetype.menuname)
        archetypeMenu.config(font=archetypeMenuFont)
        dropArchetype.config(bg="#36393e", fg="WHITE", highlightthickness=0, font=dropFont)
        dropArchetype["menu"].config(bg="#36393e", fg="WHITE")

        heightMenu = self.__root.nametowidget(dropHeight.menuname)
        heightMenu.config(font=heightMenuFont)
        dropHeight.config(bg="#36393e", fg="WHITE", highlightthickness=0, font=dropFont)
        dropHeight["menu"].config(bg="#36393e", fg="WHITE")
    def CAPMenu_SubmitCAP(self,firstName,lastName,archetypeName,heightValue):

        newPlayer = Player.Player(archetypeName)
        newPlayer.generatePlayer(firstName,lastName,heightValue,True)
        DataStorage.savePlayerObjectToPlayersFile(newPlayer)

        if archetypeName == "Slayer":
            if heightValue in HEIGHT_OPTIONS[0:8]:
                messagebox.showinfo('Success!', firstName + " " + lastName + " has been created!")
            else:
                messagebox.showerror('Error', heightValue + " does not fit the height bounds for " + archetypeName)
        elif archetypeName == "Vigilante":
            if heightValue in HEIGHT_OPTIONS[6:13]:
                messagebox.showinfo('Success!', firstName + " " + lastName + " has been created!")
            else:
                messagebox.showerror('Error', heightValue + " does not fit the height bounds for " + archetypeName)
        elif archetypeName == "Medic":
            if heightValue in HEIGHT_OPTIONS[12:22]:
                messagebox.showinfo('Success!', firstName + " " + lastName + " has been created!")
            else:
                messagebox.showerror('Error', heightValue + " does not fit the height bounds for " + archetypeName)
        elif archetypeName == "Guardian":
            if heightValue in HEIGHT_OPTIONS[21:30]:
                messagebox.showinfo('Success!', firstName + " " + lastName + " has been created!")
            else:
                messagebox.showerror('Error', heightValue + " does not fit the height bounds for " + archetypeName)
        elif archetypeName == "Engineer":
            if heightValue in HEIGHT_OPTIONS[6:13]:
                messagebox.showinfo('Success!', firstName + " " + lastName + " has been created!")
            else:
                messagebox.showerror('Error', heightValue + " does not fit the height bounds for " + archetypeName)
        elif archetypeName == "Director":
            if heightValue in HEIGHT_OPTIONS[0:8]:
                messagebox.showinfo('Success!', firstName + " " + lastName + " has been created!")
            else:
                messagebox.showerror('Error', heightValue + " does not fit the height bounds for " + archetypeName)
    # Search menu methods.
    def goToSearchMenu(self):
        for forgetRoot in self.__root.grid_slaves():
            forgetRoot.grid_forget()
        self.__root.geometry("420x500+650+250")

        nba2k_Logo = ImageTk.PhotoImage(Image.open(READER_PATH))
        nba2k_Label = Label(self.__root, image=nba2k_Logo)
        nba2k_Label.photo = nba2k_Logo
        nba2k_Label.grid(column=0, row=0, columnspan=3)

        fontSize = 45
        fontSizeEntry = 25
        fontSizeListbox = 15


        playerbaseOptions = DataStorage.getListOfPlayerNames()

        searchLabel = customtkinter.CTkLabel(self.__root, text="Search Playerbase:",text_font=tkFont.Font(family="Bahnschrift SemiBold", size=fontSize))
        searchLabel.grid(column=1,row=1,padx=100, pady=10)

        searchResult = StringVar(None)
        searchEntry = customtkinter.CTkEntry(self.__root, textvariable=searchResult, width=400, text_font=tkFont.Font(family="Bahnschrift", size=fontSizeEntry))
        searchEntry.grid(column=1,row=2,padx=100, pady=10)

        searchPlayerButton = customtkinter.CTkButton(self.__root, text="Search Player", command=lambda: self.goToPlayerFile(searchResult.get()),text_font=tkFont.Font(family="Bahnschrift SemiBold", size=fontSizeEntry), fg_color="#2eb217")
        searchPlayerButton.grid(column=1,row=3,padx=100, pady=10)

        # This is a listbox for search query
        list_Box = Listbox(self.__root, width=17, font=tkFont.Font(family="Bahnschrift SemiBold", size=fontSizeListbox))
        list_Box.grid(column=1,row=4,padx=100, pady=10)
        list_Box.delete(0, END)
        list_Box.config(bg="#36393e", fg="WHITE", highlightthickness=0)

        mainMenuButton = customtkinter.CTkButton(self.__root, text="Main Menu", command=self.goToMainMenu,text_font=tkFont.Font(family="Bahnschrift SemiBold", size=fontSize), fg_color="#2eb217")
        mainMenuButton.grid(column=1,row=5,padx=100, pady=10)

        clearListButton = customtkinter.CTkButton(self.__root, text="Clear results", command=lambda: self.searchMenu_ClearListbox(list_Box),text_font=tkFont.Font(family="Bahnschrift SemiBold", size=fontSize), fg_color="#2eb217")
        clearListButton.grid(column=1,row=6,padx=100, pady=10)



        # This creates a binding on the listbox on click
        list_Box.bind("<<ListboxSelect>>", lambda x: self.searchMenu_Fillout(list_Box,searchEntry))

        # This creates a binding on the entry box
        searchEntry.bind("<KeyRelease>", lambda x: self.searchMenu_Check(searchEntry,list_Box,playerbaseOptions))

        playerbaseData = []
        self.searchMenu_Update(list_Box,playerbaseData)
    def searchMenu_Check(self,searchEntry,list_Box,playerbaseOptions):
        searchEntryString = searchEntry.get()
        # This controls the dropdown menu options to be selected


        if searchEntryString == '':
            playerbaseData = playerbaseOptions
        else:
            playerbaseData = []
            for item in playerbaseOptions:
                if searchEntryString.lower() in item.lower():
                    playerbaseData.append(item)

        # Update listbox with selected items
        self.searchMenu_Update(list_Box,playerbaseData)
    def searchMenu_Update(self,list_Box,playerbaseData):
        # Clear the listbox
        list_Box.delete(0, END)

        # Add players to listbox
        for item in playerbaseData:
            list_Box.insert(END, item)
    def searchMenu_Fillout(self,list_Box,searchEntry):
        # Delete whatever is in the entry box
        searchEntry.delete(0, END)

        # Add clicked list item to entry box
        searchEntry.insert(0, list_Box.get(ACTIVE))
    def searchMenu_ClearListbox(self,list_Box):
        list_Box.delete(0, END)
    # Player file menu methods.
    def goToPlayerFile(self,playerName):
        for forgetRoot in self.__root.grid_slaves():
            forgetRoot.grid_forget()
        self.__root.geometry("440x550+650+250")

        nba2k_Logo = ImageTk.PhotoImage(Image.open(READER_PATH))
        nba2k_Label = Label(self.__root, image=nba2k_Logo)
        nba2k_Label.photo = nba2k_Logo
        nba2k_Label.grid(column=0, row=0, columnspan=3)

        fontSize = 30

        resultLabel = customtkinter.CTkLabel(self.__root, text=playerName,text_font=tkFont.Font(family="Bahnschrift SemiBold", size=60))
        resultLabel.grid(column=1,row=1,padx=10, pady=10)

        mainMenuButton = customtkinter.CTkButton(self.__root, text="Main Menu", command=self.goToMainMenu,text_font=tkFont.Font(family="Bahnschrift SemiBold", size=30), fg_color="#2eb217")
        mainMenuButton.grid(column=1,row=2,padx=10, pady=10)

        ppgLabel = customtkinter.CTkLabel(self.__root, text="PPG: " + "null",text_font=tkFont.Font(family="Bahnschrift SemiBold", size=fontSize))
        ppgLabel.grid(column=0,row=3, pady=5)

        rpgLabel = customtkinter.CTkLabel(self.__root, text="RPG: " + "null",text_font=tkFont.Font(family="Bahnschrift SemiBold", size=fontSize))
        rpgLabel.grid(column=0,row=4, pady=5)

        apgLabel = customtkinter.CTkLabel(self.__root, text="APG: " + "null",text_font=tkFont.Font(family="Bahnschrift SemiBold", size=fontSize))
        apgLabel.grid(column=0,row=5, pady=5)

        spgLabel = customtkinter.CTkLabel(self.__root, text="SPG: " + "null",text_font=tkFont.Font(family="Bahnschrift SemiBold", size=fontSize))
        spgLabel.grid(column=0,row=6, pady=5)

        bpgLabel = customtkinter.CTkLabel(self.__root, text="BPG: " + "null",text_font=tkFont.Font(family="Bahnschrift SemiBold", size=fontSize))
        bpgLabel.grid(column=0,row=7, pady=5)

        tpgLabel = customtkinter.CTkLabel(self.__root, text="TPG: " + "null",text_font=tkFont.Font(family="Bahnschrift SemiBold", size=fontSize))
        tpgLabel.grid(column=0,row=8, pady=5)

        fgmLabel = customtkinter.CTkLabel(self.__root, text="FGA: " + "null",text_font=tkFont.Font(family="Bahnschrift SemiBold", size=fontSize))
        fgmLabel.grid(column=0,row=9, pady=5)

        fgaLabel = customtkinter.CTkLabel(self.__root, text="FGM: " + "null",text_font=tkFont.Font(family="Bahnschrift SemiBold", size=fontSize))
        fgaLabel.grid(column=0,row=10, pady=5)

        fgpercLabel = customtkinter.CTkLabel(self.__root, text="FG%: " + "null",text_font=tkFont.Font(family="Bahnschrift SemiBold", size=fontSize))
        fgpercLabel.grid(column=0,row=11, pady=5)

        threepmLabel = customtkinter.CTkLabel(self.__root, text="3PM: " + "null",text_font=tkFont.Font(family="Bahnschrift SemiBold", size=fontSize))
        threepmLabel.grid(column=0,row=12, pady=5)

        threepaLabel = customtkinter.CTkLabel(self.__root, text="3PA: " + "null",text_font=tkFont.Font(family="Bahnschrift SemiBold", size=fontSize))
        threepaLabel.grid(column=0,row=13, pady=5)

        threepercLabel = customtkinter.CTkLabel(self.__root, text="3P%: " + "null",text_font=tkFont.Font(family="Bahnschrift SemiBold", size=fontSize))
        threepercLabel.grid(column=0,row=14, pady=5)

        pointsTotLabel = customtkinter.CTkLabel(self.__root, text="Points: " + "null",text_font=tkFont.Font(family="Bahnschrift SemiBold", size=fontSize))
        pointsTotLabel.grid(column=2,row=3, pady=5)

        reboundsTotLabel = customtkinter.CTkLabel(self.__root, text="Rebounds: " + "null",text_font=tkFont.Font(family="Bahnschrift SemiBold", size=fontSize))
        reboundsTotLabel.grid(column=2,row=4, pady=5)

        assistsTotLabel = customtkinter.CTkLabel(self.__root, text="Assists: " + "null",text_font=tkFont.Font(family="Bahnschrift SemiBold", size=fontSize))
        assistsTotLabel.grid(column=2,row=5, pady=5)

        stealsTotLabel = customtkinter.CTkLabel(self.__root, text="Steals: " + "null",text_font=tkFont.Font(family="Bahnschrift SemiBold", size=fontSize))
        stealsTotLabel.grid(column=2,row=6, pady=5)

        blocksTotLabel = customtkinter.CTkLabel(self.__root, text="Blocks: " + "null",text_font=tkFont.Font(family="Bahnschrift SemiBold", size=fontSize))
        blocksTotLabel.grid(column=2,row=7, pady=5)

        threesAttemptedTotLabel = customtkinter.CTkLabel(self.__root, text="3pts Attempted: " + "null",text_font=tkFont.Font(family="Bahnschrift SemiBold", size=fontSize))
        threesAttemptedTotLabel.grid(column=2,row=8, pady=5)

        threesMadeTotLabel = customtkinter.CTkLabel(self.__root, text="3pts Made: " + "null",text_font=tkFont.Font(family="Bahnschrift SemiBold", size=fontSize))
        threesMadeTotLabel.grid(column=2,row=9, pady=5)
    def goToGenStatReportMenu(self):
        for forgetRoot in self.__root.grid_slaves():
            forgetRoot.grid_forget()
        self.__root.geometry("400x300+650+250")

        nba2k_Logo = ImageTk.PhotoImage(Image.open(READER_PATH))
        nba2k_Label = Label(self.__root, image=nba2k_Logo)
        nba2k_Label.photo = nba2k_Logo
        nba2k_Label.grid(column=0, row=0, columnspan=3)

        fontSize=45

        style = ttk.Style()
        style.configure("Treeview", highlightthickness=0, bd=0,
                        font=('Segoe UI', 14), rowheight=30)  # Modify the font of the body
        style.configure("Treeview.Heading", font=('Segoe UI', 16, 'bold'))  # Modify the font of the headings
        style.layout("Treeview", [('Treeview.treearea', {'sticky': 'nswe'})])  # Remove the borders

        allColumns = ['Sprite ID', 'Name', 'PPG', 'RPG', 'APG', 'SPG', 'BPG', 'TPG', 'FGM', 'FGA', 'FG%', '3PM', '3PA', '3P%', 'Points', 'Rebounds', 'Assists', 'Steals', 'Blocks']
        set = ttk.Treeview(self.__root,columns=allColumns,show='headings',height=20)
        set.grid(column=0, row=1, columnspan=3, padx=100, pady=100)

        #set['columns'] = ('Sprite ID', 'Name', 'PPG', 'RPG', 'APG', 'SPG', 'BPG', 'TPG','FGM','FGA','FG%', '3PM', '3PA','3P%','Points','Rebounds','Assists','Steals','Blocks')

        for column in allColumns:
            if(column == "Sprite ID"):
                widthVal = 100
            elif(column == "Name"):
                widthVal = 200
            else:
                widthVal = 80
            set.heading(column,text = column, command = lambda _col = column: self.tableSort(set,_col,False))
            set.column(column,anchor=CENTER,width=widthVal)



        playerProfiles = DataStorage.getTableStats()
        self.genStatTable(playerProfiles,set)

        mainMenuButton = customtkinter.CTkButton(self.__root, text="Main Menu", command=self.goToMainMenu,
                                                 text_font=tkFont.Font(family="Bahnschrift SemiBold", size=fontSize),
                                                 fg_color="#2eb217")
        mainMenuButton.grid(column=1, row=5, padx=100, pady=10)
    def genStatTable(self,playerProfileList,tableSet):
        counter = 0
        for player in playerProfileList.values():
            tableSet.insert(parent='', index='end', iid=counter, text='',
                       values=(int(player.get("SpriteID")),
                               player.get("Name"),
                               player.get("PointsPerGame"),
                               player.get("ReboundsPerGame"),
                               player.get("AssistsPerGame"),
                               player.get("StealsPerGame"),
                               player.get("BlocksPerGame"),
                               player.get("TurnoversPerGame"),
                               player.get("FieldGoalsMadePerGame"),
                               player.get("FieldGoalsAttemptedPerGame"),
                               round(player.get("FieldGoalsPercentage") * 100,1),
                               player.get("ThreesMadePerGame"),
                               player.get("ThreesAttemptedPerGame"),
                               round(player.get("ThreePointPercentage") * 100,1),
                               player.get("RawPointsTotal"),
                               player.get("RawReboundsTotal"),
                               player.get("RawAssistsTotal"),
                               player.get("RawStealsTotal"),
                               player.get("RawBlocksTotal")))
            counter += 1
    def tableSort(self,treeview,sortByColumn,isReverse):
        l = [(treeview.set(k, sortByColumn), k) for k in treeview.get_children('')]
        l.sort(reverse=isReverse)

        # rearrange items in sorted positions
        for index, (val, k) in enumerate(l):
            treeview.move(k, '', index)

        # reverse sort next time
        treeview.heading(sortByColumn, command=lambda: \
            self.tableSort(treeview, sortByColumn, not isReverse))


    def open_2k13(self):
        os.system('S:\\Games\\SteamLibrary\\steamapps\\common\\NBA2K13\\nba2k13.exe')

    def runMainLoop(self):
        self.__root.mainloop()


