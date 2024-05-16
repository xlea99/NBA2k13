#region === Imports ===

import math
import os
from datetime import datetime
import time
import re
import json
import threading
import mutagen
import random
import vlc
from pathlib import Path
from spritopia.common import paths
from spritopia.common.logger import log

#endregion === Imports ===


class Radio:

    #region === Setup and Info ===

    # Basic init method to set up members and read default songs.
    def __init__(self,importAll = True):
        self.__activeSong = None
        self.__signalPlay = False
        self.__signalPause = False
        self.__signalSetSong = None
        self.__signalSetTime = -1
        self.__signalSkip = False
        self.__signalSkipHistory = False
        self.__signalStationChange = None
        self.__songIsEnded = False
        def setSongIsEnded(event):
            self.__songIsEnded = True

        self.__vlcInstance = vlc.Instance()
        self.__player = self.__vlcInstance.media_player_new()
        self.__vlcEventManager = self.__player.event_manager()
        self.__vlcEventManager.event_attach(vlc.EventType.MediaPlayerEndReached,setSongIsEnded)

        self.catalog = {}
        self.stations = {}
        self.currentStation = None
        # Import all songs in base music directory by default.
        if(importAll):
            self.loadAllSongs()
            self.loadAllStations()


        # Queue helper members
        self.__autoPlay = True
        self.__autoPopulate = True

        # Set initial station
        self.station(next(iter(self.stations)))

        # Begin radio thread
        self.__lock = threading.Lock()
        self.__thread = threading.Thread(target=self.__run).start()

    # Attempts to load all songs and all stations present in the songs and stations data folders,
    # as well as all subdirectories.
    def loadAllSongs(self):
        for root,dirs,files in os.walk(paths.paths["musicData"] / "songs"):
            for file in files:
                if (file.endswith(".json")):
                    self.importSong(os.path.join(root,file))
    def loadAllStations(self):
        for root,dirs,files in os.walk(paths.paths["musicData"] / "stations"):
            for file in files:
                if (file.endswith(".json")):
                    self.importStation(os.path.join(root,file))

    # Methods to import both songs and radios from respective JSON paths.
    def importSong(self,songJSONPath):
        if(type(songJSONPath) is not Path):
            songJSONPath = Path(songJSONPath)
        with open(songJSONPath,"r") as f:
            thisSong = json.load(f)
        if(thisSong["type"] == "song"):
            # Logic to verify and determine song path
            finalSongPath = paths.paths["media"] / f"music/{thisSong['path']}"
            paths.validatePath(finalSongPath)
            thisSong["path"] = str(finalSongPath)

            # Logic to calculate audio file length
            mutagenFileHandler = mutagen.File(finalSongPath)
            if(mutagenFileHandler is not None and mutagenFileHandler.info.length):
                thisSong["length"] = int(mutagenFileHandler.info.length * 1000)
            else:
                raise TypeError(f"Unsupported audio file type: '{finalSongPath}'")

            self.catalog[thisSong["id"]] = thisSong
            return True
        else:
            return False
    def importStation(self,stationJSONPath):
        if (type(stationJSONPath) is not Path):
            stationJSONPath = Path(stationJSONPath)
        with open(stationJSONPath, "r") as f:
            thisStation = json.load(f)
        if (thisStation["type"] == "station"):
            thisStation["queue"] = []
            thisStation["history"] = []
            thisStation["lastPlayingSong"] = {"SongID" : None, "Time": 0}
            self.stations[thisStation["id"]] = thisStation

            self.refreshStationQueue(stationID=thisStation["id"])
            return True
        else:
            return False

    # Gets the current song played, a target song, OR the full queue.
    def getSong(self,songID=None):
        with self.__lock:
            if(songID is None):
                songID = self.__activeSong
            return f"\"{self.catalog[songID]['name']}\" - {self.catalog[songID]['artist']}"
    def getQueue(self):
        returnString = ""
        for index,queueSong in enumerate(self.queue):
            returnString += f"{index + 1}. {self.getSong(queueSong)}\n"
        return returnString

    # Gets the current time on the playing song.
    def getTime(self):
        with self.__lock:
            seconds = int(self.__player.get_time() / 1000)
            minutes = int(seconds / 60)
            seconds -= (60 * minutes)

            return f"{minutes}:{seconds:02}"

    #endregion === Setup ===

    #region === Looping ===

    # Run loop for managing music playing
    def __run(self):
        while True:
            # We check if a station change has been requested.
            if(self.__signalStationChange):
                self.__updateStationStatus()

            # We check if a song skip has been requested.
            if(self.__signalSkip):
                self.__signalNextQueueSong()
                self.__manageUpdateQueue()
                self.__signalSkip = False

            # We check if there's a change in song
            if (self.__signalSetSong is not None):
                self.__updateSetSong()
                print(self.getSong())

            # Now we check main logic for playing/pausing/timestamping songs
            if(self.__activeSong is not None):
                self.__updateSongStatus()

                # We check if the song has ended here, and handle assignment of the next song.
                if(self.__songIsEnded):
                    self.__signalNextQueueSong()
                    self.__manageUpdateQueue()
            # If there isn't a currently active song, we check to see if there is anything in the queue to play.
            else:
                self.__signalNextQueueSong()
                self.__manageUpdateQueue()

            # Wait at tickrate
            time.sleep(0.03)
    # This run loop method handles checking for station changes.
    def __updateStationStatus(self):
        with self.__lock:
            if(self.currentStation):
                self.stations[self.currentStation]["lastPlayingSong"]["SongID"] = self.__activeSong
                self.stations[self.currentStation]["lastPlayingSong"]["Time"] = self.__player.get_time()

            if(self.stations[self.__signalStationChange]["lastPlayingSong"]["SongID"] is None):
                self.__signalSkip = True
                self.__signalSkipHistory = True
            else:
                self.__activeSong = self.stations[self.__signalStationChange]["lastPlayingSong"]["SongID"]
                self.__signalSetSong = self.stations[self.__signalStationChange]["lastPlayingSong"]["SongID"]
                self.__signalSetTime = self.stations[self.__signalStationChange]["lastPlayingSong"]["Time"]


            self.currentStation = self.__signalStationChange
            self.__signalStationChange = None
    # This run loop method handles setting the signaled song as the playing song in the VLC player.
    def __updateSetSong(self):
        with self.__lock:
            if (self.__signalSetSong not in self.catalog.keys()):
                raise ValueError(f"Song with id '{self.__signalSetSong}' is not in catalog!")

            self.__player.set_media(self.__vlcInstance.media_new(self.catalog[self.__signalSetSong]["path"]))

            if(self.__autoPlay):
                self.__player.play()

            log.debug(f"Set active radio song to '{self.__signalSetSong}' at time '{self.__player.get_time()}'")
            self.__signalSetSong = None
            self.__songIsEnded = False
    # This run loop method handles checking for plays, pauses, and time sets.
    def __updateSongStatus(self):
        with self.__lock:
            # Detect setTime signal.
            if (self.__signalSetTime >= 0):
                if(self.__signalSetTime >= self.catalog[self.__activeSong]["length"]):
                    self.__player.set_time(self.catalog[self.__activeSong]["length"])
                else:
                    self.__player.set_time(self.__signalSetTime)
                log.debug(f"Set current play time of song '{self.__activeSong}' to '{self.__signalSetTime}'")
                self.__signalSetTime = -1
            # Detect play signal.
            if (self.__signalPlay):
                self.__signalPlay = False
                if (not self.__player.is_playing()):
                    log.debug(f"Played/resumed radio at {self.__player.get_time()}")
                    self.__player.play()
            # Detect pause signal.
            if (self.__signalPause):
                self.__signalPause = False
                if (self.__player.is_playing()):
                    log.debug(f"Paused radio at {self.__player.get_time()}")
                    self.__player.pause()
    # This run loop method handles grabbing the next song from the queue and signaling it.
    def __signalNextQueueSong(self):
        with self.__lock:
            previousSong = self.__activeSong
            if (self.stations[self.currentStation]["queue"]):
                nextSong = self.stations[self.currentStation]["queue"].pop(0)
                self.__signalSetSong = nextSong
                self.__activeSong = self.__signalSetSong
            else:
                self.__activeSong = None

            if(self.__signalSkipHistory):
                self.__signalSkipHistory = False
            else:
                if(previousSong is not None):
                    self.stations[self.currentStation]["history"].append(previousSong)
    # This run loop method handles dynamically adding new songs to the queue based on preferences.
    def __manageUpdateQueue(self):
        with self.__lock:
            if(self.__autoPopulate):
                if(len(self.stations[self.currentStation]["queue"]) == 0):
                    self.refreshStationQueue(stationID=self.currentStation)


    #endregion === Looping ===

    #region === Radio Control ===

    # Plays the currently selected song.
    def play(self):
        with self.__lock:
            self.__signalPlay = True
    # Pauses the currently selected song.
    def pause(self):
        with self.__lock:
            self.__signalPause = True
    # Sets the time to play from of the current song. #TODO do we really need support for songs longer than an hour?
    def timestamp(self,timestamp):
        timePattern = r"^[0-9]?\d:[0-5]\d$"
        if(re.fullmatch(timePattern,timestamp)):
            timeString = timestamp
        else:
            timeString = self.catalog[self.__activeSong]["timestamps"].get(timestamp,None)
        if(timeString is None):
            raise ValueError(f"Couldn't get valid timestamp for '{timestamp}'")
        thisTime = datetime.strptime(timeString, "%M:%S")
        milliseconds = ((thisTime.minute * 60) + thisTime.second) * 1000
        with self.__lock:
            self.__signalSetTime = milliseconds
    # Sets the volume of the radio.
    def volume(self,volume):
        if(volume < 0):
            volume = 0
        with self.__lock:
            self.__player.audio_set_volume(volume)

    # Adds the given song to the back (or front) of the queue.
    def enqueueSong(self,songID,placeAtFront=False,stationID=None):
        with self.__lock:
            if (songID not in self.catalog.keys()):
                raise ValueError(f"Song with id '{self.__signalSetSong}' is not in catalog!")
            if(stationID is None):
                stationID = self.currentStation
            if(placeAtFront):
                self.stations[stationID]["queue"].insert(0,songID)
            else:
                self.stations[stationID]["queue"].append(songID)
    # Sets the currently active song, replacing the currently playing song.
    def setSong(self,songID : str):
        self.enqueueSong(songID=songID,placeAtFront=True)
        self.next()
    # Skips to the next song in the queue, or returns to the last played song in history
    def next(self):
        with self.__lock:
            self.__signalSkip = True
    def previous(self):
        if(self.stations[self.currentStation]["history"]):
            self.enqueueSong(self.__activeSong,placeAtFront=True)
            previousSong = self.stations[self.currentStation]["history"].pop()
            self.setSong(previousSong)
            with self.__lock:
                self.__signalSkipHistory = True
    # Switches to the given stationID.
    def station(self,stationID):
        if(stationID not in self.stations.keys()):
            raise ValueError(f"Station '{stationID}' not a registered radio station!")
        self.__signalStationChange = stationID

    # Method to refresh/repopulate a station's queue with configured songs.
    def refreshStationQueue(self,stationID,overwriteExistingQueue=True):
        # Get initial queue or new empty queue
        if(overwriteExistingQueue):
            newQueue = []
        else:
            newQueue = self.stations[stationID]["queue"]

        # Build unshuffled song list, using chances to decide which songs will populate this
        # queue iteration.
        for songID,songChance in self.stations[stationID]["songChances"].items():
            if(random.random() < songChance):
                newQueue.append(songID)

        # Shuffle queue
        random.shuffle(newQueue)

        # Set the station's queue to our new queue.
        self.stations[stationID]["queue"] = newQueue
    # Method to help set the mode for refreshing the queue.
    def setQueueMode(self,autoPopulate=True,autoPlay=True):
        with self.__lock:
            self.__autoPlay = autoPlay
            self.__autoPopulate = autoPopulate

    #endregion === Radio Control ===


r = Radio()
r.play()

