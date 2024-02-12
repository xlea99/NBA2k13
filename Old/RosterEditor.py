import pyautogui
import os
import time
import BaseFunctions as b
import pyperclip
import random




class RosterEditor:

    WINDOW_NAME = 'NBA 2K13 Roster Editor v0.23.0.4 - by Lefteris "Leftos" Aslanoglou'

    editorPath = ""
    rosterPath = ""
    rosterEditorWindow = None

    # Variables to hold playerData and teamData
    playerData = ""
    teamData = ""

    # This variable stores the found teamId for a placed player.
    foundTeamId = -1

    def __init__(self):
        pass

    def setEditorPath(self,_editorPath):
        self.editorPath = _editorPath

    def setRosterPath(self,_rosterPath):
        self.rosterPath = _rosterPath

    def activateWindow(self):
        self.rosterEditorWindow.activate()
        self.rosterEditorWindow.maximize()

    # This function connects this RosterEditor object to the application if it is
    # open, or opens the application if it is not yet open.
    def connectToRosterEditor(self):
        validWindows = pyautogui.getWindowsWithTitle(self.WINDOW_NAME)
        if(len(validWindows) == 0):
            os.startfile(self.editorPath)
            for i in range(5):
                try:
                    rosterEditor = pyautogui.getWindowsWithTitle(self.WINDOW_NAME)
                    self.rosterEditorWindow = rosterEditor[0]
                except IndexError:
                    time.sleep(1)
        elif(len(validWindows) == 1):
            self.rosterEditorWindow = validWindows[0]
        else:
            print("ERROR: Multiple Roster Editors open. Please close one.")

        self.rosterEditorWindow.maximize()

    # This method uses the "rosterPath" member to open a roster at a specific
    # path on the Roster Editor.
    def openRoster(self):
        existingOpenWindows = pyautogui.getWindowsWithTitle("Open")

        self.activateWindow()
        time.sleep(1)
        pyautogui.moveTo(1870,40,0.3)
        time.sleep(3)
        pyautogui.click()
        time.sleep(4)
        newOpenWindows = pyautogui.getWindowsWithTitle("Open")
        windowsExplorerWindow = None
        for window in newOpenWindows:
            if(window in existingOpenWindows):
                continue
            else:
                windowsExplorerWindow = window
                break
        windowsExplorerWindow.activate()
        pyautogui.write(self.rosterPath)
        time.sleep(1)
        pyautogui.press("enter")

    # This method will paste playerData into the Roster Editor's player tab.
    def pastePlayerData(self,saveData = True):
        newPlayerData = open("newPlayerData.txt", "w")
        newPlayerData.write(self.playerData)
        newPlayerData.close()

        self.activateWindow()
        pyautogui.moveTo(37,76,0.3)
        time.sleep(1)
        pyautogui.click()
        time.sleep(5)
        pyautogui.moveTo(38,132,0.3)
        time.sleep(1)
        pyautogui.click()
        time.sleep(3)

        pyperclip.copy(self.playerData)
        time.sleep(2)
        pyautogui.hotkey("ctrl", "shift", "v")
        time.sleep(10)

        if (saveData == True):
            pyautogui.moveTo(1721, 112, 0.3)
            time.sleep(1)
            pyautogui.click()
            time.sleep(5)


    # This method will paste teamData into the Roster Editor's team tab.
    def pasteTeamData(self,saveData = True):

        self.activateWindow()
        self.activateWindow()
        pyautogui.moveTo(78, 77, 0.3)
        pyautogui.click()
        time.sleep(5)
        pyautogui.moveTo(37, 134, 0.3)
        pyautogui.click()
        time.sleep(3)

        pyperclip.copy(self.teamData)
        time.sleep(2)
        pyautogui.hotkey("ctrl","shift","v")
        time.sleep(10)
        if(saveData == True):
            pyautogui.moveTo(1721, 112, 0.3)
            time.sleep(1)
            pyautogui.click()
            time.sleep(5)

    # This method will copy all playerData from the Roster Editor's player tab
    # and return it as a string.
    def copyPlayerData(self):
        self.activateWindow()
        pyautogui.moveTo(37, 76, 0.3)
        pyautogui.click()
        time.sleep(5)
        pyautogui.moveTo(38, 132, 0.3)
        pyautogui.click()
        time.sleep(3)
        pyautogui.click()

        pyperclip.copy("")
        playerData = ""


        for i in range(5):
            if(len(playerData) > 500000):
                time.sleep(1)
                break
            else:
                pyautogui.hotkey("ctrl", "a")
                time.sleep(15)
                pyautogui.hotkey("ctrl", "c")
                time.sleep(40)
                playerData = pyperclip.paste()



        time.sleep(2)


        self.playerData = playerData

    # This method will copy all teamData from the Roster Editor's team tab
    # and return it as a string.
    def copyTeamData(self):
        self.activateWindow()
        pyautogui.moveTo(78,77,0.3)
        pyautogui.click()
        time.sleep(5)
        pyautogui.moveTo(37,134,0.3)
        pyautogui.click()
        time.sleep(3)

        pyperclip.copy("")
        teamData = ""


        for i in range(5):
            if (len(teamData) > 50000):
                time.sleep(1)
                break
            else:
                pyautogui.hotkey("ctrl", "a")
                time.sleep(15)
                pyautogui.hotkey("ctrl", "c")
                time.sleep(40)
                teamData = pyperclip.paste()



        self.teamData = teamData
    # This method accepts an Archetype object and a playerId,
    # and adds that playerId to the first available team slot
    # on this RosterEditor object's teamData.
    def addPlayerToTeam(self,archetype,playerId):
        playerId = str(playerId)

        columnNumber = 1
        rowNumber = 1
        item = ""
        itemStartIndex = 0
        counter = 0
        tabCheck = False

        searchForOpening = False
        openingFound = False
        for i in self.teamData:
            if(i == "\t" or i == "\n"):
                if(tabCheck == True):
                    counter += 1
                    continue



                if(columnNumber == 1):
                    teamId = item
                    if(teamId in archetype.validTeams):
                        searchForOpening = True

                if(searchForOpening == True):
                    if(columnNumber >= 11):
                        currentPlayerId = item
                        if(currentPlayerId == "-1"):
                            self.foundTeamId = teamId
                            itemEndIndex = counter
                            openingFound = True
                            break
                        else:
                            if(columnNumber == 28):
                                searchForOpening = False

                if(i == "\n"):
                    rowNumber += 1
                    columnNumber = 1
                elif(i == "\t"):
                    columnNumber += 1
                    tabCheck = True
                item = ""
            else:
                if(tabCheck == True):
                    tabCheck = False
                    itemStartIndex = counter
                item += i

            counter += 1
        if(openingFound == True):
            newTeamData = ""
            counter = 0
            for i in self.teamData:
                if(counter >= itemStartIndex and counter < itemEndIndex):
                    if (counter == itemStartIndex):
                        newTeamData += playerId
                else:
                    newTeamData += i
                counter += 1


            self.teamData = newTeamData
            return True
        else:
            print("ERROR: No valid openings for player of ID " + str(playerId) + " and Archetype " + str(archetype))
            return False

    # This method accepts a Player object and overwrites the proper player
    # in the local playerData member.
    def addPlayerToRoster(self,player):
        walrus = open("prePlayersPlayerData.txt", "w")
        walrus.write(self.playerData)
        walrus.close()


        columnNumber = 1
        rowNumber = 1
        item = ""
        counter = 0
        tabCheck = False

        foundOverwriteRow = False
        itemStartIndex = 0
        itemEndIndex = 0

        playerCFID = None
        playerPortraitID = None
        playerASAID = None
        playerAssignedTo = None
        playerIsFA1 = None
        playerIsFA2 = None
        playerRFA = None
        playerIsInFAPool = None
        for i in self.playerData:
            if(i == "\t" or i == "\n"):
                if(tabCheck == True):
                    counter += 1
                    continue

                if(columnNumber == 1):
                    playerId = item
                    if(playerId == str(player.overwritePlayer.foundPlayerId)):
                        foundOverwriteRow = True
                        itemStartIndex = counter

                if(foundOverwriteRow == True):
                    if(columnNumber == 12):
                        playerCFID = item
                    elif(columnNumber == 14):
                        playerPortraitID = item
                    elif(columnNumber == 15):
                        playerASAID = item
                    elif(columnNumber == 18):
                        playerAssignedTo = item
                    elif (columnNumber == 19):
                        playerIsFA1 = item
                    elif (columnNumber == 20):
                        playerIsFA2 = item
                    elif (columnNumber == 21):
                        playerRFA = item
                    elif (columnNumber == 22):
                        playerIsInFAPool = item


                if(i == "\n"):
                    rowNumber += 1
                    columnNumber = 1
                    if(foundOverwriteRow == True):
                        itemEndIndex = counter
                        break
                elif(i == "\t"):
                    columnNumber += 1
                    tabCheck = True
                item = ""
            else:
                if(tabCheck == True):
                    tabCheck = False
                item += i

            counter += 1


        dunkIDList = player.signatureStats.getDunkIDList()


        rosterItems = {"Player" : "",
                       "PlType" : "6",
                       "Position 1" : player.archetype.inGamePositionString,
                       "Position 2" : player.archetype.inGameSecondaryPositionString,
                       "Play Style" : player.playStyle,
                       "Play Type 1" : "PnRBallHandler",
                       "Play Type 2" : "Isolation",
                       "Play Type 3" : "MidRange",
                       "Play Type 4" : "None",
                       "Number" : "0",
                       "CFID" : playerCFID,
                       "Generic Face" : "True",
                       "Portrait ID" : playerPortraitID,
                       "ASAID" : playerASAID,
                       "Team ID 1" : str(player.archetype.jerseyTeamId),
                       "Team ID 2" : str(player.archetype.jerseyTeamId),
                       "Assigned To" : playerAssignedTo,
                       "Is FA1" : "FALSE",
                       "Is FA2" : "FALSE",
                       "RFA" : playerRFA,
                       "IsInFAPool" : playerIsInFAPool,
                       "Is Hidden" : "False",
                       "Injury Type" : "0",
                       "Injury Days" : "0",
                       "Birth Year" : "1971",
                       "Birth Month" : "8",
                       "Birth Day" : "28",
                       "Years Pro" : "1",
                       "Height" : str(player.height * 2.54),
                       "Weight" : "185",
                       "ShoeBrand" : "Generic",
                       "ShoeModel" : "0",
                       "Sh Custom Color" : "False",
                       "Sh Home Team 1" : "#FF000000",
                       "Sh Home Team 2" : "#FF808080",
                       "Sh Home Base" : "#FFFFFFFF",
                       "Sh Away Team 1" : "#FFFFFFFF",
                       "Sh Away Team 2" : "#FF808080",
                       "Sh Away Base" : "#FF000000",
                       "Skintone" : "5",
                       "Eye Color" : "Brown",
                       "Muscle Tone" : "Buff",
                       "Body Type" : "Slim",
                       "CAP Hair Type" : "NoHair",
                       "CAP Hair Color" : "Black",
                       "CAP Eyebrow" : "0",
                       "CAP Moustache" : "0",
                       "CAP Facial Hair Color" : "Black",
                       "CAP Beard" : "0",
                       "CAP Goatee" : "0",
                       "ClothesType" : str(player.getClothesType()),
                       "SigSkill 1" : self.condenseSkillCardString(player.skillCards[0]),
                       "SigSkill 2" : self.condenseSkillCardString(player.skillCards[1]),
                       "SigSkill 3" : self.condenseSkillCardString(player.skillCards[2]),
                       "SigSkill 4" : self.condenseSkillCardString(player.skillCards[3]),
                       "SigSkill 5" : self.condenseSkillCardString(player.skillCards[4]),
                       "RShotInside" : str(player.stats.statsValues.get("Shot Inside")),
                       "RShotClose" : str(player.stats.statsValues.get("Shot Close")),
                       "RShotMid" : str(player.stats.statsValues.get("Shot Medium")),
                       "RBallHandling" : str(player.stats.statsValues.get("Ball Handling")),
                       "RShotThreePoint" : str(player.stats.statsValues.get("Shot Three Point")),
                       "RFreeThrow" : str(player.stats.statsValues.get("Free Throw")),
                       "RHidden" : "25",
                       "RLayup" : str(player.stats.statsValues.get("Layup")),
                       "RDunk" : str(player.stats.statsValues.get("Dunk")),
                       "RStandingDunk" : str(player.stats.statsValues.get("Standing Dunk")),
                       "RShootInTraffic" : str(player.stats.statsValues.get("Shoot In Traffic")),
                       "RShootOffDribble" : str(player.stats.statsValues.get("Shoot Off Dribble")),
                       "RHustle" : str(player.stats.statsValues.get("Hustle")),
                       "ROffHandDribbling" : str(player.stats.statsValues.get("Off Hand Dribbling")),
                       "RBallSecurity" : str(player.stats.statsValues.get("Ball Security")),
                       "RPass" : str(player.stats.statsValues.get("Pass")),
                       "RLowPostDefense" : str(player.stats.statsValues.get("Low Post Defense")),
                       "RLowPostOffense" : str(player.stats.statsValues.get("Low Post Offense")),
                       "RBlock" : str(player.stats.statsValues.get("Block")),
                       "RHands" : str(player.stats.statsValues.get("Hands")),
                       "RSteal" : str(player.stats.statsValues.get("Steal")),
                       "RSpeed" : str(player.stats.statsValues.get("Speed")),
                       "RStamina" : str(player.stats.statsValues.get("Stamina")),
                       "REmotion" : "25",
                       "RVertical" : str(player.stats.statsValues.get("Vertical")),
                       "ROffensive Rebound" : str(player.stats.statsValues.get("Offensive Rebound")),
                       "RDefensive Rebound" : str(player.stats.statsValues.get("Defensive Rebound")),
                       "RDurability" : str(player.stats.statsValues.get("Durability")),
                       "RDefAwareness" : str(player.stats.statsValues.get("Defensive Awareness")),
                       "ROffAwareness" : str(player.stats.statsValues.get("Offensive Awareness")),
                       "RConsistency" : str(player.stats.statsValues.get("Consistency")),
                       "ROnBallDef" : str(player.stats.statsValues.get("On Ball Defense")),
                       "RQuickness" : str(player.stats.statsValues.get("Quickness")),
                       "RPotential" : str(player.stats.statsValues.get("Potential")),
                       "RStrength" : str(player.stats.statsValues.get("Strength")),
                       "RLowPostFadeaway" : str(player.stats.statsValues.get("Post Fadeaway")),
                       "RLowPostHook" : str(player.stats.statsValues.get("Post Hook")),
                       "TShotTnd" : str(player.tendencies.allTendencies.get("t_ShotTnd")),
                       "TInsideShot" : str(player.tendencies.allTendencies.get("t_InsideShot")),
                       "TCloseShot" : str(player.tendencies.allTendencies.get("t_CloseShot")),
                       "TMidShot" : str(player.tendencies.allTendencies.get("t_MidShot")),
                       "TShot3Pt" : str(player.tendencies.allTendencies.get("t_ShotThreePt")),
                       "TDriveLane" : str(player.tendencies.allTendencies.get("t_DriveLane")),
                       "TDriveRight" : str(player.tendencies.allTendencies.get("t_DriveRight")),
                       "TPullUp" : str(player.tendencies.allTendencies.get("t_PullUp")),
                       "TPumpFake" : str(player.tendencies.allTendencies.get("t_PumpFake")),
                       "TTripleThreat" : str(player.tendencies.allTendencies.get("t_TripleThreat")),
                       "TNoTripleThreat" : str(player.tendencies.allTendencies.get("t_NoTripleThreat")),
                       "TTripleThreatShot" : str(player.tendencies.allTendencies.get("t_TripleThreatShot")),
                       "TSizeup" : str(player.tendencies.allTendencies.get("t_Sizeup")),
                       "THesitation" : str(player.tendencies.allTendencies.get("t_Hesitation")),
                       "TStraightDribble" : str(player.tendencies.allTendencies.get("t_StraightDribble")),
                       "TCrossover" : str(player.tendencies.allTendencies.get("t_Crossover")),
                       "TSpin" : str(player.tendencies.allTendencies.get("t_Spin")),
                       "TStepback" : str(player.tendencies.allTendencies.get("t_Stepback")),
                       "THalfspin" : str(player.tendencies.allTendencies.get("t_Halfspin")),
                       "TDoubleCrossover" : str(player.tendencies.allTendencies.get("t_DoubleCrossover")),
                       "TBehindBack" : str(player.tendencies.allTendencies.get("t_BehindBack")),
                       "THesitationCross" : str(player.tendencies.allTendencies.get("t_HesitationCrossover")),
                       "TInNOut" : str(player.tendencies.allTendencies.get("t_InNOut")),
                       "TSimpleDrive" : str(player.tendencies.allTendencies.get("t_SimpleDrive")),
                       "TAttack" : str(player.tendencies.allTendencies.get("t_Attack")),
                       "TPassOut" : str(player.tendencies.allTendencies.get("t_PassOut")),
                       "THopstep" : str(player.tendencies.allTendencies.get("t_Hopstep")),
                       "TSpinLayup" : str(player.tendencies.allTendencies.get("t_SpinLayup")),
                       "TEurostep" : str(player.tendencies.allTendencies.get("t_Eurostep")),
                       "TRunner" : str(player.tendencies.allTendencies.get("t_Runner")),
                       "TFadeaway" : str(player.tendencies.allTendencies.get("t_Fadeaway")),
                       "TDunk" : str(player.stats.get("Dunk")),
                       "TCrash" : str(player.tendencies.allTendencies.get("t_Crash")),
                       "TTouches" : str(player.tendencies.allTendencies.get("t_Touches")),
                       "TUsePick" : str(player.tendencies.allTendencies.get("t_UsePick")),
                       "TSetPick" : str(player.tendencies.allTendencies.get("t_SetPick")),
                       "TIsolation" : str(player.tendencies.allTendencies.get("t_Isolation")),
                       "TUseOffBallScreen" : str(player.tendencies.allTendencies.get("t_UseOffBallScreen")),
                       "TSetOffBallScreen" : str(player.tendencies.allTendencies.get("t_SetOffBallScreen")),
                       "TPostUp" : str(player.tendencies.allTendencies.get("t_PostUp")),
                       "TSpotUp" : str(player.tendencies.allTendencies.get("t_SpotUp")),
                       "TPostSpin" : str(player.tendencies.allTendencies.get("t_PostSpin")),
                       "TDropStep" : str(player.tendencies.allTendencies.get("t_DropStep")),
                       "TShimmy" : str(player.tendencies.allTendencies.get("t_Shimmy")),
                       "TFaceUp" : str(player.tendencies.allTendencies.get("t_FaceUp")),
                       "TLeavePost" : str(player.tendencies.allTendencies.get("t_LeavePost")),
                       "TBackDown" : str(player.tendencies.allTendencies.get("t_BackDown")),
                       "TAggressiveBackDown" : str(player.tendencies.allTendencies.get("t_AggressiveBackDown")),
                       "TPostShot" : str(player.tendencies.allTendencies.get("t_PostShot")),
                       "TPostHook" : str(player.tendencies.allTendencies.get("t_PostHook")),
                       "TPostFade" : str(player.tendencies.allTendencies.get("t_PostFade")),
                       "TPostDrive" : str(player.tendencies.allTendencies.get("t_PostDrive")),
                       "THopShot" : str(player.tendencies.allTendencies.get("t_HopShot")),
                       "TPutback" : str(player.tendencies.allTendencies.get("t_Putback")),
                       "TFlashyPass" : str(player.tendencies.allTendencies.get("t_FlashyPass")),
                       "TAlleyOop" : str(player.tendencies.allTendencies.get("t_AlleyOop")),
                       "TDrawFoul" : str(player.tendencies.allTendencies.get("t_DrawFoul")),
                       "TPlayPassLane" : str(player.tendencies.allTendencies.get("t_PlayPassLane")),
                       "TTakeCharge" : str(player.tendencies.allTendencies.get("t_TakeCharge")),
                       "TOnBallSteal" : str(player.stats.get("Steal")),
                       "TContest" : str(player.tendencies.allTendencies.get("t_Contest")),
                       "TCommitFoul" : str(player.tendencies.allTendencies.get("t_CommitFoul")),
                       "THardFoul" : str(player.tendencies.allTendencies.get("t_HardFoul")),
                       "TUseGlass" : str(player.tendencies.allTendencies.get("t_UseGlass")),
                       "TStepbackJumper" : str(player.tendencies.allTendencies.get("t_StepbackJumper")),
                       "TSpinJumper" : str(player.tendencies.allTendencies.get("t_SpinJumper")),
                       "TStepThrough" : str(player.tendencies.allTendencies.get("t_StepThrough")),
                       "TThrowAlleyOop" : str(player.tendencies.allTendencies.get("t_ThrowAlleyOop")),
                       "TGiveNGo" : str(player.tendencies.allTendencies.get("t_GiveNGo")),
                       "HSIso3L" : "23",
                       "HSIso3C" : "23",
                       "HSIso3R" : "23",
                       "HSIsoPstL" : "8",
                       "HSIsoPstC" : "12",
                       "HSIsoPstR" : "11",
                       "HSSpt3LC" : "11",
                       "HSSpt3LW" : "27",
                       "HSSpt3T" : "13",
                       "HSSpt3RW" : "18",
                       "HSSpt3RC" : "9",
                       "HSSptMidLB" : "3",
                       "HSSptMidLW" : "6",
                       "HSSptMidC" : "5",
                       "HSSptMidRW" : "4",
                       "HSSptMidRB" : "4",
                       "HSPnRLC" : "4",
                       "HSPnRLW" : "33",
                       "HSPnRT" : "37",
                       "HSPnRRW" : "24",
                       "HSPnRRC" : "2",
                       "HSPstRH" : "31",
                       "HSPstLH" : "27",
                       "HSPstRL" : "21",
                       "HSPstLL" : "21",
                       "ContractYearsBeforeOpt" : "0",
                       "ContractOpt" : "None",
                       "ContractNoTrade" : "False",
                       "ContractY1" : "0",
                       "ContractY2" : "0",
                       "ContractY3" : "0",
                       "ContractY4" : "0",
                       "ContractY5" : "0",
                       "ContractY6" : "0",
                       "ContractY7" : "0",
                       "SigFreeThrow" : str(random.randrange(0,122)),
                       # =====
                       "SigShootingForm" : str(player.signatureStats.getShootingFormID()),
                       "SigShotBase" : str(player.signatureStats.getShotBaseID()),
                       "LayupPackage" : "0",
                       "DunkPackage0" : str(dunkIDList[0]),
                       "DunkPackage1" : str(dunkIDList[1]),
                       "DunkPackage2" : str(dunkIDList[2]),
                       "DunkPackage3" : str(dunkIDList[3]),
                       "DunkPackage4" : str(dunkIDList[4]),
                       # =====
                       "DunkPackage5" : "0",
                       "DunkPackage6" : "0",
                       "DunkPackage7" : "0",
                       "DunkPackage8" : "0",
                       "DunkPackage9" : "0",
                       "DunkPackage10" : "0",
                       "DunkPackage11" : "0",
                       "DunkPackage12" : "0",
                       "DunkPackage13" : "0",
                       "DunkPackage14" : "0",
                       "GHeadband" : "0",
                       "GHeadbandLogo" : "0",
                       "GLeftArm" : "0",
                       "GLeftArmColor" : "1",
                       "GLeftElbow" : "0",
                       "GLeftElbowColor" : "1",
                       "GLeftWrist" : "0",
                       "GLeftWristColor1" : "1",
                       "GLeftWristColor2" : "1",
                       "GLeftFingers" : "0",
                       "GLeftFingersColor" : "1",
                       "GRightArm": "0",
                       "GRightArmColor": "1",
                       "GRightElbow": "0",
                       "GRightElbowColor": "1",
                       "GRightWrist": "0",
                       "GRightWristColor1": "1",
                       "GRightWristColor2": "1",
                       "GRightFingers": "0",
                       "GRightFingersColor": "1",
                       "GUndershirt" : "0",
                       "GUndershirtColor" : "1",
                       "GShorts" : "0",
                       "GShortsColor" : "1",
                       "GLeftKnee" : "0",
                       "GLeftKneeColor" : "1",
                       "GLeftLeg" : "0",
                       "GLeftLegColor" : "1",
                       "GLeftAnkle" : "0",
                       "GLeftAnkleColor" : "1",
                       "GRightKnee": "0",
                       "GRightKneeColor": "1",
                       "GRightLeg": "0",
                       "GRightLegColor": "1",
                       "GRightAnkle": "0",
                       "GRightAnkleColor": "1",
                       "GSocks" : "4",
                       "GHomeShoeTrim1" : "0",
                       "GHomeShoeTrim2" : "1",
                       "GAwayShoeTrim1" : "0",
                       "GAwayShoeTrim2" : "1",
                       "SeasonStats0": "-1",
                       "SeasonStats1" : "-1",
                       "SeasonStats2" : "-1",
                       "SeasonStats3" : "-1",
                       "SeasonStats4" : "-1",
                       "SeasonStats5" : "-1",
                       "SeasonStats6" : "-1",
                       "SeasonStats7" : "-1",
                       "SeasonStats8" : "-1",
                       "SeasonStats9" : "-1",
                       "SeasonStats10" : "-1",
                       "SeasonStats11" : "-1",
                       "SeasonStats12" : "-1",
                       "SeasonStats13" : "-1",
                       "SeasonStats14" : "-1",
                       "SeasonStats15" : "-1",
                       "SeasonStats16" : "-1",
                       "SeasonStats17" : "-1",
                       "SeasonStats18" : "-1",
                       "SeasonStats19" : "-1",
                       "SeasonStats20" : "-1",
                       "SeasonStats21" : "-1",
                       "PlayoffStats" : "-1"}

        stitchedString = ""
        for i in rosterItems.values():
            stitchedString += str(i)
            stitchedString += "\t"

        stitchedString.rstrip("\t")

        counter = 0
        newPlayerData = ""
        for i in self.playerData:
            if(counter >= itemStartIndex and counter < itemEndIndex):
                if(counter == itemStartIndex):
                    newPlayerData += "\t" + stitchedString
            else:
                newPlayerData += i
            counter += 1


        walrus = open("postPlayersPlayerData.txt", "w")
        walrus.write(newPlayerData)
        walrus.close()
        self.playerData = newPlayerData

    # This method removes any columns from the playerData that is specified in a
    # columnIndexArray
    def removeColumns(self,columnArray):

        columnIndexArray = []
        for i in columnArray:
            if(type(i) == str):
                columnIndexArray.append(self.getColumnIndex(i))
            else:
                columnIndexArray.append(i)

        print("we is going in with this columnIndexArray: " + str(columnIndexArray))


        columnNumber = 1
        rowNumber = 1
        counter = 0
        tabCheck = False

        deletionColumnFound = False

        newPlayerData = ""

        for i in self.playerData:
            if (i == "\t" or i == "\n"):
                if (tabCheck == True):
                    counter += 1

                if (i == "\n"):
                    rowNumber += 1
                    columnNumber = 1
                    deletionColumnFound = False

                elif (i == "\t"):
                    columnNumber += 1
                    tabCheck = True
                    deletionColumnFound = False


                if (columnNumber in columnIndexArray):
                    deletionColumnFound = True

            else:
                if (tabCheck == True):
                    tabCheck = False

            if (deletionColumnFound == False):
                newPlayerData += i
            counter += 1

        self.playerData = newPlayerData

    # Small helper function that finds the index of a column on playerData, given the column's name.
    def getColumnIndex(self,columnName):
        columnNumber = 1

        item = ""
        foundColumnIndex = False

        for i in self.playerData:
            if(i == "\n"):
                break
            elif(i == "\t"):
                if(item == columnName):
                    foundColumnIndex = True
                    break
                columnNumber += 1
                item = ""
                continue
            else:
                item += i

        if(foundColumnIndex == True):
            return columnNumber
        else:
            print("ERROR: Could not find columnName specified.")

    # This method removes any and all "bad" columns that cause problems when copy-pasting over.
    def removeBadColumns(self):
        listOfBadColumns = ["CFID",
                            "Name",
                            "ASAID",
                            "AssignedTo*",
                            "IsFA1",
                            "IsFA2",
                            "RFA",
                            "IsInFAPool*",
                            "IsHidden*"]

        self.removeColumns(listOfBadColumns)

    # Small helper function to convert a skill card string into a string readable by the roster editor.
    def condenseSkillCardString(self, skillCardString):
        if (skillCardString == "Alley-ooper"):
            newString = "AlleyOoper"
        elif (skillCardString == "Antifreeze"):
            newString = "AntiFreeze"
        elif(skillCardString == "War General"):
            newString = "FloorGeneral"
        else:
            newString = skillCardString.replace(" ", "")

        return newString


walrus = RosterEditor()
walrus.setEditorPath("S:\\Games\\2kStuff\\Roster Editor\\NBA 2K13 Roster Editor.exe")
walrus.setRosterPath("C:\\Users\\timbe\\AppData\\Roaming\\2K Sports\\NBA 2K13\\Saves\\Walrus.ROS")
walrus.connectToRosterEditor()
walrus.activateWindow()
walrus.openRoster()