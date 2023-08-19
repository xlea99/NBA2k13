import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from PIL import ImageTk,Image
import customtkinter
import vlc
import os
os.add_dll_directory(r'C:\Program Files\VideoLAN\VLC')
import pygame
import Archetypes
import Player
import StatsRipper
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

    def __init__(self, openRoot=True):
        self.root = None
        if openRoot:
            self.openRoot()

        self.headerFrame = tk.Frame(self.root)
        self.mainFrame = tk.Frame(self.root)
        self.headerFrame.grid(row=0, column=0)
        self.mainFrame.grid(row=1, column=0)

        # Global media player to avoid headaches.
        self.mediaPlayer = None
        pygame.mixer.init()

        self.previousScreen = None
        self.currentScreen = None

        # Various constant buttons
        self.saveButton = None

        # Necessary graphics
        self.readerPhoto = tk.PhotoImage(file=f"{b.paths.graphics}\\2kReader.png")
    def openRoot(self):
        self.root = tk.Tk()
        self.root.title("Spritopia Presents:")
        self.root.geometry("1920x1080")
        self.root.configure(bg="#1C1C1C")
        #self.root.attributes('-fullscreen', True)
        self.root.iconbitmap(f"{b.paths.graphics}\\sprite.ico")

    # This method attempts to build the header frame with its default contents.
    def buildHeader(self):
        reader = tk.Label(self.headerFrame, image=self.readerPhoto)
        backButton = tk.Button(self.headerFrame, text="<BACK", command=self.previousScreen, font=("Bahnschrift SemiBold", 10), fg="#535454", width=10, bg="grey")  # Adjusted the colors, but might need fine-tuning.
        self.saveButton = tk.Button(self.headerFrame, text="SAVE", command=self.saveData, font=("Bahnschrift SemiBold", 10), fg="#535454", width=10, bg="grey")

        reader.pack()
        self.saveButton.place(x=1820, y=15)
        backButton.place(x=100, y=15)

    def startupScreen(self):
        previewMovieLabel = tk.Label(self.root)
        previewMovieLabel.place(x=0,y=0,relwidth=1, relheight=1)
        vlcInstance = vlc.Instance("-q")
        self.mediaPlayer = vlcInstance.media_player_new(f"{b.paths.media}\\NormalVid.mp4")

        # Set the video output window
        self.mediaPlayer.set_hwnd(previewMovieLabel.winfo_id())

        # Start playing the video and audio
        self.mediaPlayer.play()

        fontSize = 60

        startButton = customtkinter.CTkButton(self.root, text="Start", command=self.goToMainMenu, font=customtkinter.CTkFont(family="Bahnschrift SemiBold", size=fontSize), fg_color="#2eb217")
        startButton.pack(side=tk.BOTTOM, pady=150)

    # This method takes us to the main menu from whatever screen we're
    # currently on.
    def goToMainMenu(self):
        self.wipeMainFrame("MainMenu")

        pygame.mixer.music.stop()

        pygame.mixer.music.load(f"{b.paths.media}\\{random.choice(INTRODUCTIONS)}")
        pygame.mixer.music.play(loops=0)
        pygame.mixer.music.set_volume(0.075)

        pygame.mixer.music.queue(f"{b.paths.media}\\Title.ogg")




        nba2k_Label = tk.Label(self.root, image=self.nba2k_Logo)
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

    def saveData(self):
        print("beansy")

    # This helper function simply wipes the entire screen of all elements.
    def wipeMainFrame(self,newMainFrame):
        self.previousScreen = self.currentScreen
        self.currentScreen = newMainFrame


        self.isOnPlayerPicker = False
        self.searchMenu_ResetFilters()

        pygame.mixer.music.stop()

        for forgetRoot in self.root.grid_slaves():
            forgetRoot.grid_forget()

        for widget in self.root.winfo_children():
            widget.forget()

        for forgetPlace in self.root.place_slaves():
            if (forgetPlace == self.saveButton or forgetPlace == self.saveLabel):
                continue
            forgetPlace.place_forget()

        if(self.mediaPlayer is not None):
            self.mediaPlayer.stop()
            self.mediaPlayer = None


    # The main loop is essentially a wrapper function for the GUI main loop, as well as
    # opening a new thread to run the secondary loop on.
    def runMainLoop(self):
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
        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry("+%d+%d" % (x, y))
        label = tk.Label(tw, text=self.text, justify=tk.LEFT,
                      background="#ffffe0", relief=tk.SOLID, borderwidth=1,
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
