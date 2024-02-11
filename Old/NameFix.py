import sqlite3
import SQLite_Helpers as sqlh
import BaseFunctions as b


TEAM_DICT = {40 : "'65 Celtics",
             41 : "'65 Lakers",
             42 : "'71 Bucks",
             43 : "'71 Lakers",
             44 : "'71 Hawks",
             45 : "'72 Lakers",
             46 : "'72 Knicks",
             47 : "'77 76ers",
             48 : "'85 76ers",
             49 : "'85 Bulls",
             50 : "'86 Bulls",
             51 : "'86 Celtics",
             52 : "'86 Hawks",
             53 : "'87 Lakers",
             54 : "'89 Pistons",
             55 : "'89 Bulls",
             56 : "'90 Cavaliers",
             57 : "'91 Bulls",
             58 : "'91 Lakers",
             59 : "'91 Trail Blazers",
             60 : "'91 Warriors",
             61 : "'93 Bulls",
             62 : "'93 Hornets",
             63 : "'94 Rockets",
             64 : "'94 Nuggets",
             65 : "'95 Knicks",
             66 : "'95 Magic",
             67 : "'96 Bulls",
             68 : "'96 SuperSonics",
             69 : "'98 Bulls",
             70 : "'98 Jazz",
             71 : "'98 Lakes",
             72 : "'99 Spurs",
             73 : "'01 76ers",
             74 : "'02 Kings",
             81 : "Extra Players 1",
             82 : "Extra Players 2",
             83 : "Extra Players 3",
             999 : "Free Agents"}

PROFILE = b.readConfigValue("profileBaseFolder") + "\\" + b.readConfigValue("activeProfile")

# This class is used to figure out which existing 2k player should be
# edited to create a new player. It uses character length of the first
# and last name to ensure no problems in the game due to player naming.
class NameFix:

    # Various members
    preferredFirstNameLength = 0
    preferredLastNameLength = 0
    firstNameLength = 0
    lastNameLength = 0
    needsFirstNameSpaces = True
    needsLastNameSpaces = True
    foundPlayerName = ""
    foundPlayerId = None
    foundPlayerTeam = ""
    needsCustomPlayer = True


    # Blank init
    def __init__(self):
        pass

    # This is the primary method of the class, that uses a preferred first and last
    # name length to determine which player (read from NameFix_FullList.txt) should
    # be used. All players with IDs listed in NameFix_UsedList.txt are skipped over,
    # as they have already been used to create a player.
    def findAvailableName(self,customFirstName,customLastName):
        dbConnect =  sqlite3.connect(PROFILE + "\\Players.db")

        self.preferredFirstNameLength = len(customFirstName)
        self.preferredLastNameLength = len(customLastName)

        c = dbConnect.cursor()
        fullNameList = c.execute('SELECT GameId,DefaultName,AssignedTo FROM DefaultPlayers WHERE IsUsed = 0 AND IsCustom = 0 AND IsBlocked = 0')

        shortestFirstFit = "XXXXXXXXXXXXXXXXXXXX"
        shortestLastFit = "XXXXXXXXXXXXXXXXXXXX"
        shortestFitID = ""
        for player in fullNameList:
            playerID = player[0]
            fullName = player[1]
            playerTeamId = player[2]
            playerFirstName = ""
            playerLastName = ""
            tempString = ""
            for i in fullName:
                if(i == " "):
                    playerFirstName = tempString
                    tempString = ""
                    continue
                else:
                    tempString += i
            playerLastName = tempString

            usedNames = sqlh.convertColumnToList(dbConnect, "GameId", "Players")
            usedNameList = []
            for i in usedNames:
                usedNameList.append(str(i))
            if(playerID in usedNameList):
                continue

            firstLength = len(playerFirstName)
            lastLength = len(playerLastName)
            if(firstLength <= len(shortestFirstFit) and firstLength >= self.preferredFirstNameLength):
                if(lastLength <= len(shortestLastFit) and lastLength >= self.preferredLastNameLength):
                    shortestFirstFit = playerFirstName
                    shortestLastFit = playerLastName
                    shortestFitID = playerID
                    shortestFitTeamId = playerTeamId


        if(len(shortestFirstFit) > 16 or len(shortestLastFit) > 16):
            self.needsCustomPlayer = True
            self.firstNameLength = 16
            self.lastNameLength = 16
            self.foundPlayerName = "(Custom Player)"
            customPlayerCursor = dbConnect.cursor()
            customPlayerList = customPlayerCursor.execute('SELECT GameId FROM DefaultPlayers WHERE IsUsed = 0 AND IsCustom = 1 AND IsBlocked')

            minimum = 10000
            for i in customPlayerList:
                if(i[0] < minimum):
                    minimum = i[0]

            self.foundPlayerId = str(minimum)

            cw = dbConnect.cursor()
            sql = '''UPDATE DefaultPlayers 
                        SET IsUsed = ?
                        WHERE GameId = ?
                        '''

            dataTuple = tuple([1, minimum])
            cw.execute(sql, dataTuple)
            dbConnect.commit()
            dbConnect.close()



        else:
            self.foundPlayerId = shortestFitID
            self.foundPlayerTeam = shortestFitTeamId

            self.firstNameLength = len(shortestFirstFit)
            self.lastNameLength = len(shortestLastFit)

            self.needsCustomPlayer = False
            self.foundPlayerName = shortestFirstFit + " " + shortestLastFit

            cw = dbConnect.cursor()
            sql = '''UPDATE DefaultPlayers 
            SET IsUsed = ?
            WHERE GameId = ?
            '''
            dataTuple = tuple([1,shortestFitID])
            cw.execute(sql,dataTuple)
            dbConnect.commit()
            dbConnect.close()
            if(len(shortestFirstFit) > self.preferredFirstNameLength):
                self.needsFirstNameSpaces = True
            else:
                self.needsFirstNameSpaces = False

            if(len(shortestLastFit) > self.preferredLastNameLength):
                self.needsLastNameSpaces = True
            else:
                self.needsLastNameSpaces = False

        self.addCustomNameToDatabase(customFirstName + " " + customLastName)

    # This simple method adds the player's custom name to the DefaultPlayers database.
    def addCustomNameToDatabase(self,fullName):
        dbConnect = sqlite3.connect(PROFILE + "\\Players.db")

        c = dbConnect.cursor()
        sql = ('''UPDATE DefaultPlayers
        SET NewName=?
        WHERE GameID=?;
        ''')

        valueTuple = tuple([fullName,self.foundPlayerId])
        print("HERES TUPLE:")
        print(valueTuple)

        c.execute(sql,valueTuple)

        dbConnect.commit()
        dbConnect.close()


    # This string method determines what to print based on whether or not the found
    # player is a custom player or not, and how many spaces need to be added to the
    # name.
    def __str__(self):
        returnString = "****************************\n"
        returnString += "PLAYER CREATION INSTRUCTIONS\n"
        if(self.needsCustomPlayer):
            returnString += "\nUse a custom player slot."
        else:
            returnString += "\nPlease overwrite " + str(self.foundPlayerName)
            if(self.needsFirstNameSpaces):
                returnString += "\n*ADD " + str(self.firstNameLength - self.preferredFirstNameLength) + " SPACES TO MAKE FIRST NAME " + str(self.firstNameLength) + " CHARACTERS"
            if (self.needsLastNameSpaces):
                returnString += "\n*ADD " + str(self.lastNameLength - self.preferredLastNameLength) + " SPACES TO MAKE LAST NAME " + str(self.lastNameLength) + " CHARACTERS"

        returnString += "\n****************************"
        return returnString



# This method is unrelated to generating a NameFix object, it is simply a QOL
# method that will generate a new, custom NameList meant to be read by the
# roster editor, so that you can edit custom players without the hassle.
def generateFixedNameList(filePath = False, readCustomNames = True):
    dbConnect = sqlite3.connect(PROFILE + "\\Players.db")

    c = dbConnect.cursor()
    if(readCustomNames == True):
        sql = '''SELECT GameId,NewName FROM DefaultPlayers'''
    else:
        sql = '''SELECT GameId,DefaultName FROM DefaultPlayers'''

    nameInformation = c.execute(sql)

    nameDict = {}
    for entry in nameInformation:
        nameDict[str(entry[0])] = str(entry[1])

    if(filePath == False):
        nameListFile = open("CustomNameList.txt","w")
    else:
        nameListFile = open(str(filePath) + "\\CustomNameList.txt","w")

    for i in range(1515):
        if(str(i) in nameDict.keys()):
            nameToWrite = nameDict.get(str(i))
        else:
            nameToWrite = ""
        nameListFile.write(str(i) + "\t" + nameToWrite + "\n")




    nameListFile.close()

