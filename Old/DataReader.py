import BaseFunctions as b
import time
import csv
import Tracker
import Player
import xml.etree.ElementTree as ET

# THIS FILE CONTAINS OLD SQL BASE DATA STORAGE CODE FOR BACKUP REASONS.
BASE_CSV_DIRECTORY = "S:\\Coding\\Projects\\NBA2k13\\CSVs"
DATA_PATH = "/Data"

# This class handles all communications with the Database
class DataStorage:

    def __init__(self):
        pass

    # This method uses the directoryName variable to read the four CSVs
    # into a return array containing 4 sub-arrays, associated with each four CSVs
    # [PlayersCSV,HeadshapesCSV,TeamsCSV,JerseysCSV]
    def readBaseCSVs(self,rosterName):
        csvDirectory = BASE_CSV_DIRECTORY + "\\" + rosterName
        playersCSV = []
        headshapesCSV = []
        teamsCSV = []
        jerseysCSV = []
        # Open CSV files.
        BasePlayersCSVFile = open(csvDirectory + "\\Players.csv", 'r', encoding="utf16")
        BaseHeadshapesCSVFile = open(csvDirectory + "\\Headshapes.csv", 'r', encoding="utf16")
        BaseTeamsCSVFile = open(csvDirectory + "\\Teams.csv", 'r', encoding="utf16")
        BaseJerseysCSVFile = open(csvDirectory + "\\Jerseys.csv", 'r', encoding="utf16")
        # Convert CSV files into Python csv_reader objects
        BasePlayersCSVReader = csv.reader(BasePlayersCSVFile, delimiter=',')
        BaseHeadshapesCSVReader = csv.reader(BaseHeadshapesCSVFile, delimiter=',')
        BaseTeamsCSVReader = csv.reader(BaseTeamsCSVFile, delimiter=',')
        BaseJerseysCSVReader = csv.reader(BaseJerseysCSVFile, delimiter=",")
        # Populate the self variables with CSV information, then close the CSV files.
        for row in BasePlayersCSVReader:
            playersCSV.append(row)
        BasePlayersCSVFile.close()
        for row in BaseHeadshapesCSVReader:
            headshapesCSV.append(row)
        BaseHeadshapesCSVFile.close()
        for row in BaseTeamsCSVReader:
            teamsCSV.append(row)
        for row in BaseJerseysCSVReader:
            jerseysCSV.append(row)
        BaseTeamsCSVFile.close()
        del playersCSV[0]
        del headshapesCSV[0]
        del teamsCSV[0]
        del jerseysCSV[0]
        return [playersCSV, headshapesCSV, teamsCSV, jerseysCSV]

    # This method adds a single player from a set of CSVs associated with a single roster
    # to the super Player table. This method should ONLY EVER BE MANUALLY CALLED, as there
    # is no reason to use this in Top-Down automation. Only used as a convenience method to
    # add players from Rosters we've previously made/2k default rosters.
    def storePlayerFromRoster(self,rosterPlayerID,rosterName,playerCategory,playerSource):
        playerID = rosterPlayerID + 1
        csvArray = self.readBaseCSVs(rosterName)
        playerCSV = csvArray[0]
        headshapeCSV = csvArray[1]

        addPlayerToRosterSQL = '''INSERT INTO Players(FirstName,LastName,Archetype,Rarity,PlayerSource,PlayerCategory,Height,Weight,
        Hand,Personality,CFID,AudioID,PlayInitiator,PlayStyle,PlayType1,PlayType2,PlayType3,PlayType4,
        PositionPrimary,PositionSecondary,Stat_ShotInside,Stat_ShotClose,Stat_ShotMedium,Stat_ShotThreePoint,Stat_FreeThrow,Stat_Layup,Stat_Dunk,Stat_StandingDunk,Stat_ShootInTraffic,
	    Stat_PostFadeaway,Stat_PostHook,Stat_ShootOffDribble,Stat_BallHandling,Stat_OffHandDribbling,Stat_BallSecurity,Stat_Pass,Stat_Block,
	    Stat_Steal,Stat_Hands,Stat_OnBallDefense,Stat_OffensiveRebound,Stat_DefensiveRebound,Stat_LowPostOffense,Stat_LowPostDefense,Stat_OffensiveAwareness,
	    Stat_DefensiveAwareness,Stat_Consistency,Stat_Stamina,Stat_Speed,Stat_Quickness,Stat_Strength,Stat_Vertical,Stat_Hustle,
	    Stat_Durability,Stat_Potential,Stat_Emotion,SkillCard1,SkillCard2,SkillCard3,SkillCard4,SkillCard5,Sig_ShootingForm,Sig_ShotBase,
	    Sig_Fadeaway,Sig_Contested,Sig_EscapeDribblePullUp,Sig_Runner,Sig_FreeThrow,Sig_DribblePullUp,Sig_SpinJumper,Sig_HopJumper,Sig_PostFade,
	    Sig_PostHook,Sig_PostHopShot,Sig_PostShimmyShot,Sig_PostDriveStepbackShot,Sig_PostSpinStepbackShot,Sig_PostProtectShot,Sig_PostProtectSpinShot,Sig_ISOCrossover,
	    Sig_ISOBehindBack,Sig_ISOSpin,Sig_ISOHesitation,Sig_LayupPackage,Sig_GotoDunkPackage,Sig_ExtraDunkPackage1,Sig_ExtraDunkPackage2,
	    Sig_ExtraDunkPackage3,Sig_ExtraDunkPackage4,Tend_ShotTnd,Tend_InsideShot,Tend_CloseShot,Tend_MidShot,Tend_ShotThreePt,Tend_Putback,
        Tend_DriveLane,Tend_PullUp,Tend_PumpFake,Tend_TripleThreat,Tend_TripleThreatShot,Tend_NoTripleThreat,Tend_StraightDribble,Tend_Sizeup,Tend_Hesitation,
        Tend_DriveRight,Tend_Crossover,Tend_Spin,Tend_Stepback,Tend_Halfspin,Tend_DoubleCrossover,Tend_BehindBack,Tend_HesitationCrossover,Tend_InNOut,
        Tend_SimpleDrive,Tend_Attack,Tend_PassOut,Tend_HopStep,Tend_SpinLayup,Tend_Eurostep,Tend_Runner,Tend_Fadeaway,Tend_StepbackJumper,
        Tend_SpinJumper,Tend_Dunk,Tend_AlleyOop,Tend_UseGlass,Tend_Drawfoul,Tend_StepThrough,Tend_Crash,Tend_UsePick,Tend_SetPick,
        Tend_Isolation,Tend_UseOffBallScreen,Tend_SetOffBallScreen,Tend_SpotUp,Tend_PostUp,Tend_GiveNGo,Tend_Touches,Tend_PostSpin,Tend_PostDrive,
        Tend_AggressiveBackDown,Tend_LeavePost,Tend_DropStep,Tend_FaceUp,Tend_BackDown,Tend_PostShot,Tend_PostHook,Tend_PostFade,Tend_Shimmy,Tend_HopShot,
        Tend_FlashyPass,Tend_ThrowAlleyOop,Tend_HardFoul,Tend_TakeCharge,Tend_PlayPassLane,Tend_OnBallSteal,Tend_Contest,Tend_CommitFoul,HSpot_Iso3PLft,HSpot_Iso3PCtr,HSpot_Iso3PRgt,
        HSpot_IsoHPLft,HSpot_IsoHPCtr,HSpot_IsoHPRgt,HSpot_P_rLCrnr,HSpot_P_rLWing,HSpot_P_rTopOA,HSpot_P_rRWing,HSpot_P_rRCrnr,HSpot_Spt3PLCr,
        HSpot_Spt3PLWg,HSpot_Spt3PTop,HSpot_Spt3PRWg,HSpot_Spt3PRCr,HSpot_SptMdLBl,HSpot_SptMdLWg,HSpot_SptMdCtr,HSpot_SptMdRWg,HSpot_SptMdRBl,
        HSpot_PstRHigh,HSpot_PstRLow,HSpot_PstLHigh,HSpot_PstLLow,NameOrder,
	    SkinTone,Muscles,EyeColor,BodyType,Clothes,JerseyNumber,HShape_HParam1,HShape_HParam2,HShape_HdBrwHght,HShape_HdBrwWdth,HShape_HdBrwSlpd,
        HShape_HdNkThck,HShape_HdNkFat,HShape_HdChnLen,HShape_HdChnWdth,HShape_HdChnProt,HShape_HdJawSqr,HShape_HdJawWdth,HShape_HdChkHght,HShape_HdChkWdth,
        HShape_HdChkFull,HShape_HdDefinit,HShape_MtULCurve,HShape_MtULThick,HShape_MtULProtr,HShape_MtLLCurve,HShape_MtLLThick,HShape_MtLLProtr,HShape_MtSzHght,
        HShape_MtSzWdth,HShape_MtCrvCorn,HShape_ErHeight,HShape_ErWidth,HShape_ErEarLobe,HShape_ErTilt,HShape_NsNsHght,HShape_NsNsWdth,HShape_NsNsProtr,
        HShape_NsBnBridge,HShape_NsBnDefin,HShape_NsBnWdth,HShape_NsTipHght,HShape_NsTipWdth,HShape_NsTipTip,HShape_NsTipBnd,HShape_NsNtHght,
        HShape_NsNtWdth,HShape_EsFrmOpen,HShape_EsFrmSpac,HShape_EsFrmLwEl,HShape_EsFrmUpEl,HShape_EsPlcHght,HShape_EsPlcWdth,HShape_EsPlcRot,HShape_EsPlcProt,
        HShape_EsShpOtEl,HShape_EsShpInEl,CAP_FaceT,CAP_Hstl,CAP_Hcol,CAP_Hlen,CAP_BStyle,CAP_Moust,CAP_Goatee,
        CAP_Fhcol,CAP_Eyebr,CAP_T_LftN,CAP_T_LftS,CAP_T_RgtS,CAP_T_LftB,CAP_T_RgtB,CAP_T_LftF,CAP_T_RgtF,Gear_Headband,
        Gear_HdbndLg,Gear_Undrshrt,Gear_UndrsCol,Gear_LeftArm,Gear_LArmCol,Gear_LeftElb,Gear_LElbCol,Gear_LeftWrst,Gear_LWrstC1,
        Gear_LWrstC2,Gear_LeftFngr,Gear_LFngrCol,Gear_RghtArm,Gear_RArmCol,Gear_RghtElb,Gear_RElbCol,Gear_RghtWrst,Gear_RWrstC1,Gear_RWrstC2,
        Gear_RghtFngr,Gear_RFngrCol,Gear_PresShrt,Gear_PrsShCol,Gear_LeftLeg,Gear_LLegCol,Gear_LeftKnee,Gear_LKneeCol,Gear_LeftAnkl,Gear_LAnklCol,
        Gear_RghtLeg,Gear_RLegCol,Gear_RghtKnee,Gear_RKneeCol,Gear_RghtAnkl,Gear_RAnklCol,Gear_SockLngh,Gear_ShsBrLck,Gear_ShsBrand,Gear_ShsModel,
        Gear_ShsUCusC,Gear_ShsTHC1,Gear_ShsTHC2,Gear_ShsTAC1,Gear_ShsTAC2,Gear_ShsHCol1,Gear_ShsHCol2,Gear_ShsHCol3,Gear_ShsACol1,Gear_ShsACol2,Gear_ShsACol3)
        VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'''
        dataTuple = [playerCSV[playerID][3], # First Name
                     playerCSV[playerID][2], # Last Name
                     "None", # No Archetype
                     "None", # No Rarity
                     playerSource, # Pre-decided PlayerSource
                     playerCategory, # Pre-decided PlayerCategory
                     playerCSV[playerID][14], # Height
                     playerCSV[playerID][15], # Weight
                     playerCSV[playerID][19], # Handedness
                     playerCSV[playerID][27], # Personality
                     playerCSV[playerID][35], # CFID
                     playerCSV[playerID][36], # AudioID_M
                     playerCSV[playerID][60], # Play Initiator
                     playerCSV[playerID][61], # PlayStyle
                     playerCSV[playerID][62], # PlayType1
                     playerCSV[playerID][63], # PlayType2
                     playerCSV[playerID][64], # PlayType3
                     playerCSV[playerID][65], # PlayType4
                     playerCSV[playerID][12], # PrimaryPosition
                     playerCSV[playerID][13] # Secondary Position
                     ] # Adding basic information about the player.
        for i in range(124,165): # Appending each stat and skill card to the tuple.
            dataTuple.append(playerCSV[playerID][i])
        for i in range(273,301): # Appending each signature animation to the tuple.
            dataTuple.append(playerCSV[playerID][i])
        for i in range(165,234): # Appending each tendency to the tuple.
            dataTuple.append(playerCSV[playerID][i])
        for i in range(234,259): # Appending each hotspot to the tuple.
            dataTuple.append(playerCSV[playerID][i])
        dataTuple += [playerCSV[playerID][37], # Name Order
                      playerCSV[playerID][38], # Skin Tone
                      playerCSV[playerID][39], # Muscles
                      playerCSV[playerID][40], # Eye Color
                      playerCSV[playerID][41], # Body Type
                      playerCSV[playerID][42], # Clothes
                      playerCSV[playerID][66] # Number
                      ] # Adding various CAP information not classified as official CAP info.
        for i in range(2,53): # Adding all headshape info to the tuple.
            dataTuple.append(headshapeCSV[int(playerCSV[playerID][43]) + 1][i])
        for i in range(44,60): # Adding all official CAP info to the tuple.
            dataTuple.append(playerCSV[playerID][i])
        for i in range(329,380): # Adding all gear info to the tuple.
            dataTuple.append(playerCSV[playerID][i])

        dataTuple = tuple(dataTuple)
        database = sqlite3.connect(DATABASE_PATH)
        cursor = database.cursor()
        cursor.execute(addPlayerToRosterSQL,dataTuple)
        database.commit()
        database.close()

    # This method will add 4 entirely new Roster tables to the database, meant for
    # storing all information within a Roster with name rosterName_TableType. Adds no data,
    # just the tables themselves.
    def generateNewRosterTables(self,rosterName="RosterTemplate"):
        database = sqlite3.connect(DATABASE_PATH)
        cursor = database.cursor()
        createNewPlayersRosterTableSQL = 'CREATE TABLE "ROS_' + rosterName + '_Players" '
        createNewPlayersRosterTableSQL += '''(
                                    "P_RosterID"    INTEGER,"SpriteID" INTEGER,
	                                "P_Last_Name" TEXT,"P_First_Name"    TEXT,"P_NickName"  TEXT,"P_IsRegNBA"  INTEGER,"P_IsSpecial" INTEGER,
                                    "P_SlotType"  INTEGER,"P_IsGener"   INTEGER,"P_IsDraftee" INTEGER,"P_IsDrafted" INTEGER,"P_ASA_ID"    INTEGER,"P_Pos"   INTEGER,"P_SecondPos" INTEGER,"P_Height"    REAL,"P_Weight"    REAL,
                                    "P_BirthDay"  INTEGER,"P_BirthMonth"    INTEGER,"P_BirthYear" INTEGER,"P_Hand"  INTEGER,"P_YearsPro"  INTEGER,"P_CollegeID" INTEGER,"P_DraftedBy" INTEGER,"P_DraftYear" INTEGER,"P_DraftRound"    INTEGER,"P_DraftPos"  INTEGER,"P_CAP_Nick"  INTEGER,"P_Personality"   INTEGER,
                                    "P_Play4Winner"   INTEGER,"P_FinSecurity"   INTEGER,"P_Loyalty"   INTEGER,"P_PeakAgeS"  INTEGER,"P_PeakAgeE"  INTEGER,"P_PortrID"   INTEGER,"P_GenericF"  INTEGER,"P_CF_ID" INTEGER,"P_AudioID_M" INTEGER,"P_NmOrder"   INTEGER,
                                    "P_SkinTone"  INTEGER,"P_Muscles"   INTEGER,"P_EyeColor"  INTEGER,"P_Bodytype"  INTEGER,"P_Clothes"   INTEGER,"P_HS_ID" INTEGER,"P_CAP_FaceT" INTEGER,"P_CAP_Hstl"  INTEGER,"P_CAP_Hcol"  INTEGER,"P_CAP_Hlen"  INTEGER,"P_CAP_BStyle"    INTEGER,"P_CAP_Moust" INTEGER,"P_CAP_Goatee"    INTEGER,"P_CAP_Fhcol" INTEGER,"P_CAP_Eyebr" INTEGER,"P_CAP_T_LftN"    INTEGER,"P_CAP_T_LftS"    INTEGER,"P_CAP_T_RgtS"    INTEGER,"P_CAP_T_LftB"    INTEGER,"P_CAP_T_RgtB"    INTEGER,"P_CAP_T_LftF"    INTEGER,
                                    "P_CAP_T_RgtF"    INTEGER,"P_PlayInitor"    INTEGER,"P_PlayStyle" INTEGER,"P_PlayType1" INTEGER,"P_PlayType2" INTEGER,"P_PlayType3" INTEGER,"P_PlayType4" INTEGER,"P_Number"    INTEGER,"P_IsFA"  INTEGER,"P_TeamID1"   INTEGER,"P_TeamID2"   INTEGER,"P_MinsAsg"   INTEGER,
                                    "P_Morale"    INTEGER,"P_Fatigue"   INTEGER,"P_FARestr"   INTEGER,"P_CtrThoughts"   INTEGER,"P_InjDaysLeft"   INTEGER,"P_InjType"   INTEGER,"P_StatY0"    INTEGER,"P_StatY1"    INTEGER,"P_StatY2"    INTEGER,"P_StatY3"    INTEGER,"P_StatY4"    INTEGER,"P_StatY5"    INTEGER,"P_StatY6"    INTEGER,
                                    "P_StatY7"    INTEGER,"P_StatY8"    INTEGER,"P_StatY9"    INTEGER,"P_StatY10"   INTEGER,"P_StatY11"   INTEGER,"P_StatY12"   INTEGER,"P_StatY13"   INTEGER,"P_StatY14"   INTEGER,"P_StatY15"   INTEGER,"P_StatY16"   INTEGER,"P_StatY17"   INTEGER,"P_StatY18"   INTEGER,
                                    "P_StatY19"   INTEGER,"P_StatPOs"   INTEGER,"P_GH_CarPts" INTEGER,"P_GH_CarFGM" INTEGER,"P_GH_CarFGA" INTEGER,"P_GH_CarStl" INTEGER,"P_GH_CarBlk" INTEGER,"P_GH_Car3PM" INTEGER,"P_GH_Car3PA" INTEGER,"P_GH_CarFTM" INTEGER,"P_GH_CarFTA" INTEGER,"P_GH_CarOReb"    INTEGER,"P_GH_CarDReb"    INTEGER,"P_GH_CarRebs"    INTEGER,
                                    "P_GH_CarAst" INTEGER,"P_GH_SeaPts" INTEGER,"P_GH_SeaFGM" INTEGER,"P_GH_SeaFGA" INTEGER,"P_GH_SeaStl" INTEGER,"P_GH_SeaBlk" INTEGER,"P_GH_Sea3PM" INTEGER,"P_GH_Sea3PA" INTEGER,"P_GH_SeaFTM" INTEGER,"P_GH_SeaFTA" INTEGER,"P_GH_SeaOReb"    INTEGER,"P_GH_SeaDReb"    INTEGER,"P_GH_SeaRebs"    INTEGER,
                                    "P_GH_SeaAst" INTEGER,"P_SShtIns"   INTEGER,"P_SShtCls"   INTEGER,"P_SShtMed"   INTEGER,"P_SSht3PT"   INTEGER,"P_SShtFT"    INTEGER,"P_SLayUp"    INTEGER,"P_SDunk" INTEGER,"P_SStdDunk"  INTEGER,"P_SShtInT"   INTEGER,"P_SPstFdaway"    INTEGER,"P_SPstHook"  INTEGER,"P_SShtOfD"   INTEGER,"P_SBallHndl" INTEGER,"P_SOffHDrib" INTEGER,"P_SBallSec"  INTEGER,
                                    "P_SPass" INTEGER,"P_SBlock"    INTEGER,"P_SSteal"    INTEGER,"P_SHands"    INTEGER,"P_SOnBallD"  INTEGER,"P_SOReb" INTEGER,"P_SDReb" INTEGER,"P_SOLowPost" INTEGER,"P_SDLowPost" INTEGER,"P_SOAwar"    INTEGER,"P_SDAwar"    INTEGER,"P_SConsis"   INTEGER,"P_SStamina"  INTEGER,"P_SSpeed"    INTEGER,"P_SQuick"    INTEGER,"P_SStrength" INTEGER,
                                    "P_SVertical" INTEGER,"P_SHustle"   INTEGER,"P_SDurab"    INTEGER,"P_SPOT"  INTEGER,"P_SEmotion"  INTEGER,"P_SigSkill1" INTEGER,"P_SigSkill2" INTEGER,"P_SigSkill3" INTEGER,"P_SigSkill4" INTEGER,"P_SigSkill5" INTEGER,"P_TShtTend"  INTEGER,"P_TInsShots" INTEGER,"P_TCloseSht" INTEGER,"P_TMidShots" INTEGER,"P_T3PTShots" INTEGER,"P_TPutbacks" INTEGER,
                                    "P_TDriveLn"  INTEGER,"P_TPullUp"   INTEGER,"P_TPumpFake" INTEGER,"P_TTrplThrt" INTEGER,"P_TTTShot"   INTEGER,"P_TNoTT" INTEGER,"P_TStrghtDr" INTEGER,"P_TSizeUp"   INTEGER,"P_THesitat"  INTEGER,"P_TDriveRvL" INTEGER,"P_TCrossov"  INTEGER,"P_TSpin" INTEGER,"P_TStepBack" INTEGER,"P_THalfSpin" INTEGER,"P_TDblCross" INTEGER,
                                    "P_TBhndBack" INTEGER,"P_THesCross" INTEGER,"P_TInAndOut" INTEGER,"P_TDPSimpDr" INTEGER,"P_TAttackB"  INTEGER,"P_TPassOut"  INTEGER,"P_THopStep"  INTEGER,"P_TSpinLUp"  INTEGER,"P_TEuroStep" INTEGER,"P_TRunner"   INTEGER,"P_TFadeaway" INTEGER,"P_TStpbJmpr" INTEGER,"P_TSpinJmpr" INTEGER,"P_TDunkvLU"  INTEGER,
                                    "P_TAlleyOop" INTEGER,"P_TUseGlass" INTEGER,"P_TDrawFoul" INTEGER,"P_TStpThrgh" INTEGER,"P_TVShCrash" INTEGER,"P_TUsePick"  INTEGER,"P_TSetPick"  INTEGER,"P_TIsolat"   INTEGER,"P_TUseOBScr" INTEGER,"P_TSetOBScr" INTEGER,"P_TSpotUp"   INTEGER,"P_TPostUp"   INTEGER,"P_TGiveGo"   INTEGER,
                                    "P_TTouches"  INTEGER,"P_TPostSpn"  INTEGER,"P_TPostDrv"  INTEGER,"P_TPostAgBd" INTEGER,"P_TLeavePost"    INTEGER,"P_TPostDrpSt"    INTEGER,"P_TPostFaceU"    INTEGER,"P_TPostBDown"    INTEGER,"P_TPostShots"    INTEGER,"P_TPostHook" INTEGER,"P_TPostFdawy"    INTEGER,"P_TPostShmSh"    INTEGER,"P_TPostHopSh"    INTEGER,
                                    "P_TFlshPass" INTEGER,"P_TThrowAO"  INTEGER,"P_THardFoul" INTEGER,"P_TTakeChrg" INTEGER,"P_TPassLane" INTEGER,"P_TOnBalStl" INTEGER,"P_TContShot" INTEGER,"P_TCommFoul" INTEGER,"P_HIso3PLft" INTEGER,"P_HIso3PCtr" INTEGER,"P_HIso3PRgt" INTEGER,"P_HIsoHPLft" INTEGER,"P_HIsoHPCtr" INTEGER,"P_HIsoHPRgt" INTEGER,"P_HP_rLCrnr" INTEGER,"P_HP_rLWing" INTEGER,
                                    "P_HP_rTopOA" INTEGER,"P_HP_rRWing" INTEGER,"P_HP_rRCrnr" INTEGER,"P_HSpt3PLCr" INTEGER,"P_HSpt3PLWg" INTEGER,"P_HSpt3PTop" INTEGER,"P_HSpt3PRWg" INTEGER,"P_HSpt3PRCr" INTEGER,"P_HSptMdLBl" INTEGER,"P_HSptMdLWg" INTEGER,"P_HSptMdCtr" INTEGER,"P_HSptMdRWg" INTEGER,"P_HSptMdRBl" INTEGER,"P_HPstRHigh" INTEGER,"P_HPstRLow"  INTEGER,"P_HPstLHigh" INTEGER,"P_HPstLLow"  INTEGER,"P_HZ1"   INTEGER,"P_HZ2"   INTEGER,
                                    "P_HZ3"   INTEGER,"P_HZ4"   INTEGER,"P_HZ5"   INTEGER,"P_HZ6"   INTEGER,"P_HZ7"   INTEGER,"P_HZ8"   INTEGER,"P_HZ9"   INTEGER,"P_HZ10"  INTEGER,"P_HZ11"  INTEGER,"P_HZ12"  INTEGER,"P_HZ13"  INTEGER,"P_HZ14"  INTEGER,"P_AShtForm"  INTEGER,"P_AShtBase"  INTEGER,"P_AFadeaway" INTEGER,"P_AContestd" INTEGER,"P_AEscDrPlU" INTEGER,
                                    "P_ARunner"   INTEGER,"P_AFreeT"    INTEGER,"P_ADrPullUp" INTEGER,"P_ASpinJmpr" INTEGER,"P_AHopJmpr"  INTEGER,"P_APstFade"  INTEGER,"P_APstHook"  INTEGER,"P_APstHopSh" INTEGER,"P_APstShmSh" INTEGER,"P_APstDrvStB"    INTEGER,"P_APstSpnStB"    INTEGER,"P_APstPrtct" INTEGER,"P_APstPrtSpn"    INTEGER,"P_AIsoCross" INTEGER,"P_AIsoBhBck" INTEGER,"P_AIsoSpin"  INTEGER,
                                    "P_AIsoHesit" INTEGER,"P_ALayUp"    INTEGER,"P_AGoToDunk" INTEGER,"P_ADunk2"    INTEGER,"P_ADunk3"    INTEGER,"P_ADunk4"    INTEGER,"P_ADunk5"    INTEGER,"P_ADunk6"    INTEGER,"P_ADunk7"    INTEGER,"P_ADunk8"    INTEGER,"P_ADunk9"    INTEGER,"P_ADunk10"   INTEGER,"P_ADunk11"   INTEGER,"P_ADunk12"   INTEGER,"P_ADunk13"   INTEGER,"P_ADunk14"   INTEGER,"P_ADunk15"   INTEGER,"P_AIntHLght" INTEGER,
                                    "P_AIntPreG1" INTEGER,"P_AIntPreG2" INTEGER,"P_AIntPreT1" INTEGER,"P_AIntPreT2" INTEGER,"P_BirdYears" INTEGER,"P_CClrYears" INTEGER,"P_CRole" INTEGER,"P_COption"   INTEGER,"P_CNoTrade"  INTEGER,"P_CYear1"    INTEGER,"P_CYear2"    INTEGER,"P_CYear3"    INTEGER,"P_CYear4"    INTEGER,"P_CYear5"    INTEGER,"P_CYear6"    INTEGER,"P_SgndTYWith"    INTEGER,"P_YrsForCurT"    INTEGER,"P_GHeadband" INTEGER,"P_GHdbndLg"  INTEGER,"P_GUndrshrt" INTEGER,"P_GUndrsCol" INTEGER,
                                    "P_GLeftArm"  INTEGER,"P_GLArmCol"  INTEGER,"P_GLeftElb"  INTEGER,"P_GLElbCol"  INTEGER,"P_GLeftWrst" INTEGER,"P_GLWrstC1"  INTEGER,"P_GLWrstC2"  INTEGER,"P_GLeftFngr" INTEGER,"P_GLFngrCol" INTEGER,"P_GRghtArm"  INTEGER,"P_GRArmCol"  INTEGER,"P_GRghtElb"  INTEGER,"P_GRElbCol"  INTEGER,"P_GRghtWrst" INTEGER,"P_GRWrstC1"  INTEGER,"P_GRWrstC2"  INTEGER,"P_GRghtFngr" INTEGER,"P_GRFngrCol" INTEGER,"P_GPresShrt" INTEGER,
                                    "P_GPrsShCol" INTEGER,"P_GLeftLeg"  INTEGER,"P_GLLegCol"  INTEGER,"P_GLeftKnee" INTEGER,"P_GLKneeCol" INTEGER,"P_GLeftAnkl" INTEGER,"P_GLAnklCol" INTEGER,"P_GRghtLeg"  INTEGER,"P_GRLegCol"  INTEGER,"P_GRghtKnee" INTEGER,"P_GRKneeCol" INTEGER,"P_GRghtAnkl" INTEGER,"P_GRAnklCol" INTEGER,"P_GSockLngh" INTEGER,"P_GShsBrLck" INTEGER,"P_GShsBrand" INTEGER,"P_GShsModel" INTEGER,
                                    "P_GShsUCusC" INTEGER,"P_GShsTHC1"  INTEGER,"P_GShsTHC2"  INTEGER,"P_GShsTAC1"  INTEGER,"P_GShsTAC2"  INTEGER,"P_GShsHCol1" BLOB,"P_GShsHCol2" BLOB,"P_GShsHCol3" BLOB,"P_GShsACol1" BLOB,"P_GShsACol2" BLOB,"P_GShsACol3" BLOB
                                    );'''
        createNewTeamsRosterTableSQL = 'CREATE TABLE "ROS_' + rosterName + '_Teams" '
        createNewTeamsRosterTableSQL += '''(
                                    "T_ID"  INTEGER,"T_Name"    TEXT,"T_City"    TEXT,"T_CityUnique"  TEXT,"T_Abbr"    TEXT,"T_Nickname"    TEXT,"T___Name"  BLOB,"T___City"  BLOB,"T___CityUnq"   BLOB,"T___TeamAbbr"  BLOB,"T_TType"   INTEGER,"T_IsSpecial"   INTEGER,
                                    "T_Division"    INTEGER,"T_Year"    INTEGER,"T_Logo"    BLOB,"T_GID" INTEGER,"T_Color1"  BLOB,"T_Color2"  BLOB,"T_AudioID1"    INTEGER,"T_SomeID1" INTEGER,"T_SomeID2" INTEGER,"T_ArenaID" INTEGER,"T_Rival1"  INTEGER,"T_Rival2"  INTEGER,"T_Rival3"  INTEGER,"T_RivalPO" INTEGER,
                                    "T_AttndReg"    REAL,"T_AttndEx" REAL,"T_Chemistry"   REAL,"T_PlNum"   INTEGER,"T_Ros_PG"  INTEGER,"T_Ros_SG"  INTEGER,"T_Ros_SF"  INTEGER,"T_Ros_PF"  INTEGER,"T_Ros_C"   INTEGER,"T_Ros_S6"  INTEGER,"T_Ros_S7"  INTEGER,"T_Ros_S8"  INTEGER,"T_Ros_S9"  INTEGER,
                                    "T_Ros_S10" INTEGER,"T_Ros_S11" INTEGER,"T_Ros_S12" INTEGER,"T_Ros_R13" INTEGER,"T_Ros_R14" INTEGER,"T_Ros_R15" INTEGER,"T_Ros_R16" INTEGER,"T_Ros_R17" INTEGER,"T_Ros_R18" INTEGER,"T_Ros_R19" INTEGER,"T_Ros_R20" INTEGER,"T_Sit_Strt_PG" INTEGER,
                                    "T_Sit_Strt_SG" INTEGER,"T_Sit_Strt_SF" INTEGER,"T_Sit_Strt_PF" INTEGER,"T_Sit_Strt_C"  INTEGER,"T_Sit_Bnch_PG" INTEGER,"T_Sit_Bnch_SG" INTEGER,"T_Sit_Bnch_SF" INTEGER,"T_Sit_Bnch_PF" INTEGER,"T_Sit_Bnch_C"  INTEGER,"T_Sit_Tall_PG" INTEGER,"T_Sit_Tall_SG" INTEGER,
                                    "T_Sit_Tall_SF" INTEGER,"T_Sit_Tall_PF" INTEGER,"T_Sit_Tall_C"  INTEGER,"T_Sit_Quck_PG" INTEGER,"T_Sit_Quck_SG" INTEGER,"T_Sit_Quck_SF" INTEGER,"T_Sit_Quck_PF" INTEGER,"T_Sit_Quck_C"  INTEGER,"T_Sit_Dfns_PG" INTEGER,"T_Sit_Dfns_SG" INTEGER,"T_Sit_Dfns_SF" INTEGER,"T_Sit_Dfns_PF" INTEGER,"T_Sit_Dfns_C"  INTEGER,
                                    "T_Sit_3PT_PG"  INTEGER,"T_Sit_3PT_SG"  INTEGER,"T_Sit_3PT_SF"  INTEGER,"T_Sit_3PT_PF"  INTEGER,"T_Sit_3PT_C"   INTEGER,"T_Sit_FT_PG"   INTEGER,"T_Sit_FT_SG"   INTEGER,"T_Sit_FT_SF"   INTEGER,"T_Sit_FT_PF"   INTEGER,"T_Sit_FT_C"    INTEGER,"T_Staff_HC"    INTEGER,"T_Staff_AC"    INTEGER,"T_Staff_SPr2"  INTEGER,
                                    "T_Staff_SPr3"  INTEGER,"T_Staff_SPr1"  INTEGER,"T_Staff_Trn"   INTEGER,"T_Staff_SNBA"  INTEGER,"T_StatCurS"    INTEGER,"T_StatCurP"    INTEGER,"T_StatPrevS"   INTEGER,"T_StatPrevP"   INTEGER,"T_CurStreak"   INTEGER,"T_CurHStr" INTEGER,"T_CurRStr" INTEGER,"T_WAhAtHalf"   INTEGER,"T_LAhAtHalf"   INTEGER,
                                    "T_WBhAtHalf"   INTEGER,"T_LBhAtHalf"   INTEGER,"T_WAhAft3rd"   INTEGER,"T_LAhAft3rd"   INTEGER,"T_WBhAft3rd"   INTEGER,"T_LBhAft3rd"   INTEGER,"T_WAg500plus"  INTEGER,"T_LAg500plus"  INTEGER,"T_WBetterFG"   INTEGER,"T_LBetterFG"   INTEGER,"T_WMoreRebs"   INTEGER,"T_LMoreRebs"   INTEGER,"T_WFewerTOs"   INTEGER,
                                    "T_LFewerTOs"   INTEGER,"T_H_DivTtls"   INTEGER,"T_H_POAps" INTEGER,"T_H_LastPOAp"  INTEGER,"T_H_ConfTtls"  INTEGER,"T_H_NBAChmps"  INTEGER,"T_Record0" INTEGER,"T_Record1" INTEGER,"T_Record2" INTEGER,"T_Record3" INTEGER,"T_Record4" INTEGER,"T_Record5" INTEGER,"T_Record6" INTEGER,
                                    "T_Record7" INTEGER,"T_Record8" INTEGER,"T_Record9" INTEGER,"T_Record10"    INTEGER,"T_Record11"    INTEGER,"T_Record12"    INTEGER,"T_Record13"    INTEGER,"T_Record14"    INTEGER,"T_Record15"    INTEGER,"T_Record16"    INTEGER,"T_Record17"    INTEGER,"T_Record18"    INTEGER,"T_Record19"    INTEGER,"T_TSC_1ScrO"   INTEGER,"T_TSC_2ScrO"   INTEGER,"T_TSC_3ScrO"   INTEGER,"T_AutoCamps"   INTEGER
                                    );'''
        createNewHeadshapesRosterTableSQL = 'CREATE TABLE "ROS_' + rosterName + '_Headshapes" '
        createNewHeadshapesRosterTableSQL += '''(
                                    "H_ID" INTEGER,"H_HParam1" INTEGER,"H_HParam2" INTEGER,"H_HdBrwHght" INTEGER,"H_HdBrwWdth" INTEGER,"H_HdBrwSlpd" INTEGER,"H_HdNkThck" INTEGER,"H_HdNkFat" INTEGER,"H_HdChnLen" INTEGER,"H_HdChnWdth" INTEGER,"H_HdChnProt" INTEGER,"H_HdJawSqr" INTEGER,"H_HdJawWdth" INTEGER,"H_HdChkHght" INTEGER,"H_HdChkWdth" INTEGER,"H_HdChkFull" INTEGER,"H_HdDefinit" INTEGER,
                                    "H_MtULCurve" INTEGER,"H_MtULThick" INTEGER,"H_MtULProtr" INTEGER,"H_MtLLCurve" INTEGER,"H_MtLLThick" INTEGER,"H_MtLLProtr" INTEGER,"H_MtSzHght" INTEGER,"H_MtSzWdth" INTEGER,"H_MtCrvCorn" INTEGER,"H_ErHeight" INTEGER,"H_ErWidth" INTEGER,"H_ErEarLobe" INTEGER,"H_ErTilt" INTEGER,"H_NsNsHght" INTEGER,"H_NsNsWdth" INTEGER,"H_NsNsProtr" INTEGER,"H_NsBnBridge" INTEGER,
                                    "H_NsBnDefin" INTEGER,"H_NsBnWdth" INTEGER,"H_NsTipHght" INTEGER,"H_NsTipWdth" INTEGER,"H_NsTipTip" INTEGER,"H_NsTipBnd" INTEGER,"H_NsNtHght" INTEGER,"H_NsNtWdth" INTEGER,"H_EsFrmOpen" INTEGER,"H_EsFrmSpac" INTEGER,"H_EsFrmLwEl" INTEGER,"H_EsFrmUpEl" INTEGER,"H_EsPlcHght" INTEGER,"H_EsPlcWdth" INTEGER,"H_EsPlcRot" INTEGER,"H_EsPlcProt" INTEGER,"H_EsShpOtEl" INTEGER,"H_EsShpInEl" INTEGER
                                    );'''
        createNewJerseysRosterTableSQL = 'CREATE TABLE "ROS_' + rosterName + '_Jerseys" '
        createNewJerseysRosterTableSQL += '''(
                                    "J_ID" INTEGER,"J_Texture" BLOB,"J_Logo" BLOB,"J_GID" INTEGER,"J_Name" BLOB,"J_CATTmplNm" BLOB,"J_JerseyID" INTEGER,"J_JType_c" INTEGER,"J_JType" INTEGER,"J_JType2" INTEGER,"J_CAT_Usage" INTEGER,"J_ShortsStl" INTEGER,"J_JModel" INTEGER,
                                    "J_IsAway" INTEGER,"J_SocksCol" INTEGER,"J_UseCusClrs" INTEGER,"J_CusClrs4Nm" INTEGER,"J_TColor1" BLOB,"J_TColor2" BLOB,"J_TColor3" BLOB,"J_TColor4" BLOB,"J_TColor5" BLOB,"J_TColor6" BLOB,"J_JColor1" INTEGER,"J_JColor2" INTEGER,
                                    "J_JColor3" INTEGER,"J_LColor1" INTEGER,"J_LColor2" INTEGER,"J_LColor3" INTEGER,"J_NameColor" INTEGER,"J_FrNumCol1" INTEGER,"J_FrNumCol2" INTEGER,"J_BkNumCol1" INTEGER,"J_BkNumCol2" INTEGER,"J_ShsColor1" INTEGER,"J_ShsColor2" INTEGER,"J_ShsColor3" INTEGER
                                    );'''
        cursor.execute(createNewPlayersRosterTableSQL)
        cursor.execute(createNewTeamsRosterTableSQL)
        cursor.execute(createNewHeadshapesRosterTableSQL)
        cursor.execute(createNewJerseysRosterTableSQL)
        database.commit()
        database.close()

    # This method simply stores the entire playersCSV of a given Roster into its respective Roster table.
    # This WILL overwrite existing data in the table.
    def storeFullPlayersCSV(self,rosterName):


        playersCSV = self.readBaseCSVs(rosterName)[0]

        rosterTableString = "ROS_" + rosterName + "_Players"
        storeSingleRowSQL = '''INSERT OR REPLACE INTO ''' + rosterTableString + ''' (
	                        SpriteID,P_RosterID,P_Last_Name,P_First_Name,P_NickName,P_IsRegNBA,P_IsSpecial,P_SlotType,P_IsGener,P_IsDraftee,
	                        P_IsDrafted,P_ASA_ID,P_Pos,P_SecondPos,P_Height,P_Weight,P_BirthDay,P_BirthMonth,P_BirthYear,P_Hand,
	                        P_YearsPro,P_CollegeID,P_DraftedBy,P_DraftYear,P_DraftRound,P_DraftPos,P_CAP_Nick,P_Personality,P_Play4Winner,P_FinSecurity,P_Loyalty,P_PeakAgeS,
	                        P_PeakAgeE,P_PortrID,P_GenericF,P_CF_ID,P_AudioID_M,P_NmOrder,P_SkinTone,P_Muscles,P_EyeColor,P_Bodytype,P_Clothes,P_HS_ID,
	                        P_CAP_FaceT,P_CAP_Hstl,P_CAP_Hcol,P_CAP_Hlen,P_CAP_BStyle,P_CAP_Moust,P_CAP_Goatee,P_CAP_Fhcol,P_CAP_Eyebr,P_CAP_T_LftN,P_CAP_T_LftS,
	                        P_CAP_T_RgtS,P_CAP_T_LftB,P_CAP_T_RgtB,P_CAP_T_LftF,P_CAP_T_RgtF,P_PlayInitor,P_PlayStyle,P_PlayType1,P_PlayType2,P_PlayType3,P_PlayType4,
	                        P_Number,P_IsFA,P_TeamID1,P_TeamID2,P_MinsAsg,P_Morale,P_Fatigue,P_FARestr,P_CtrThoughts,P_InjDaysLeft,P_InjType,
	                        P_StatY0,P_StatY1,P_StatY2,P_StatY3,P_StatY4,P_StatY5,P_StatY6,P_StatY7,P_StatY8,P_StatY9,P_StatY10,
	                        P_StatY11,P_StatY12,P_StatY13,P_StatY14,P_StatY15,P_StatY16,P_StatY17,P_StatY18,P_StatY19,P_StatPOs,P_GH_CarPts,P_GH_CarFGM,P_GH_CarFGA,
	                        P_GH_CarStl,P_GH_CarBlk,P_GH_Car3PM,P_GH_Car3PA,P_GH_CarFTM,P_GH_CarFTA,P_GH_CarOReb,P_GH_CarDReb,P_GH_CarRebs,P_GH_CarAst,P_GH_SeaPts,P_GH_SeaFGM,
	                        P_GH_SeaFGA,P_GH_SeaStl,P_GH_SeaBlk,P_GH_Sea3PM,P_GH_Sea3PA,P_GH_SeaFTM,P_GH_SeaFTA,P_GH_SeaOReb,P_GH_SeaDReb,P_GH_SeaRebs,P_GH_SeaAst,P_SShtIns,
	                        P_SShtCls,P_SShtMed,P_SSht3PT,P_SShtFT,P_SLayUp,P_SDunk,P_SStdDunk,P_SShtInT,P_SPstFdaway,P_SPstHook,P_SShtOfD,P_SBallHndl,
	                        P_SOffHDrib,P_SBallSec,P_SPass,P_SBlock,P_SSteal,P_SHands,P_SOnBallD,P_SOReb,P_SDReb,P_SOLowPost,P_SDLowPost,P_SOAwar,P_SDAwar,P_SConsis,
	                        P_SStamina,P_SSpeed,P_SQuick,P_SStrength,P_SVertical,P_SHustle,P_SDurab,P_SPOT,P_SEmotion,P_SigSkill1,P_SigSkill2,P_SigSkill3,P_SigSkill4,P_SigSkill5,
	                        P_TShtTend,P_TInsShots,P_TCloseSht,P_TMidShots,P_T3PTShots,P_TPutbacks,P_TDriveLn,P_TPullUp,P_TPumpFake,P_TTrplThrt,P_TTTShot,P_TNoTT,
	                        P_TStrghtDr,P_TSizeUp,P_THesitat,P_TDriveRvL,P_TCrossov,P_TSpin,P_TStepBack,P_THalfSpin,P_TDblCross,P_TBhndBack,P_THesCross,P_TInAndOut,P_TDPSimpDr,P_TAttackB,
	                        P_TPassOut,P_THopStep,P_TSpinLUp,P_TEuroStep,P_TRunner,P_TFadeaway,P_TStpbJmpr,P_TSpinJmpr,P_TDunkvLU,P_TAlleyOop,P_TUseGlass,P_TDrawFoul,P_TStpThrgh,P_TVShCrash,
	                        P_TUsePick,P_TSetPick,P_TIsolat,P_TUseOBScr,P_TSetOBScr,P_TSpotUp,P_TPostUp,P_TGiveGo,P_TTouches,P_TPostSpn,P_TPostDrv,P_TPostAgBd,P_TLeavePost,
	                        P_TPostDrpSt,P_TPostFaceU,P_TPostBDown,P_TPostShots,P_TPostHook,P_TPostFdawy,P_TPostShmSh,P_TPostHopSh,P_TFlshPass,P_TThrowAO,P_THardFoul,P_TTakeChrg,P_TPassLane,
	                        P_TOnBalStl,P_TContShot,P_TCommFoul,P_HIso3PLft,P_HIso3PCtr,P_HIso3PRgt,P_HIsoHPLft,P_HIsoHPCtr,P_HIsoHPRgt,P_HP_rLCrnr,P_HP_rLWing,P_HP_rTopOA,P_HP_rRWing,
	                        P_HP_rRCrnr,P_HSpt3PLCr,P_HSpt3PLWg,P_HSpt3PTop,P_HSpt3PRWg,P_HSpt3PRCr,P_HSptMdLBl,P_HSptMdLWg,P_HSptMdCtr,P_HSptMdRWg,P_HSptMdRBl,P_HPstRHigh,P_HPstRLow,
	                        P_HPstLHigh,P_HPstLLow,P_HZ1,P_HZ2,P_HZ3,P_HZ4,P_HZ5,P_HZ6,P_HZ7,P_HZ8,P_HZ9,P_HZ10,P_HZ11,P_HZ12,
	                        P_HZ13,P_HZ14,P_AShtForm,P_AShtBase,P_AFadeaway,P_AContestd,P_AEscDrPlU,P_ARunner,P_AFreeT,P_ADrPullUp,P_ASpinJmpr,P_AHopJmpr,P_APstFade,
	                        P_APstHook,P_APstHopSh,P_APstShmSh,P_APstDrvStB,P_APstSpnStB,P_APstPrtct,P_APstPrtSpn,P_AIsoCross,P_AIsoBhBck,P_AIsoSpin,P_AIsoHesit,P_ALayUp,P_AGoToDunk,P_ADunk2,P_ADunk3,
	                        P_ADunk4,P_ADunk5,P_ADunk6,P_ADunk7,P_ADunk8,P_ADunk9,P_ADunk10,P_ADunk11,P_ADunk12,P_ADunk13,P_ADunk14,P_ADunk15,P_AIntHLght,
	                        P_AIntPreG1,P_AIntPreG2,P_AIntPreT1,P_AIntPreT2,P_BirdYears,P_CClrYears,P_CRole,P_COption,P_CNoTrade,P_CYear1,P_CYear2,P_CYear3,
	                        P_CYear4,P_CYear5,P_CYear6,P_SgndTYWith,P_YrsForCurT,P_GHeadband,P_GHdbndLg,P_GUndrshrt,P_GUndrsCol,P_GLeftArm,P_GLArmCol,P_GLeftElb,
	                        P_GLElbCol,P_GLeftWrst,P_GLWrstC1,P_GLWrstC2,P_GLeftFngr,P_GLFngrCol,P_GRghtArm,P_GRArmCol,P_GRghtElb,P_GRElbCol,P_GRghtWrst,P_GRWrstC1,P_GRWrstC2,
	                        P_GRghtFngr,P_GRFngrCol,P_GPresShrt,P_GPrsShCol,P_GLeftLeg,P_GLLegCol,P_GLeftKnee,P_GLKneeCol,P_GLeftAnkl,P_GLAnklCol,P_GRghtLeg,P_GRLegCol,
	                        P_GRghtKnee,P_GRKneeCol,P_GRghtAnkl,P_GRAnklCol,P_GSockLngh,P_GShsBrLck,P_GShsBrand,P_GShsModel,P_GShsUCusC,P_GShsTHC1,P_GShsTHC2,
	                        P_GShsTAC1,P_GShsTAC2,P_GShsHCol1,P_GShsHCol2,P_GShsHCol3,P_GShsACol1,P_GShsACol2,P_GShsACol3
	                        )VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);'''
        findSpriteIDSQL = "SELECT SpriteID FROM " + rosterTableString + " WHERE P_RosterID="

        for row in playersCSV:
            database = sqlite3.connect(DATABASE_PATH)
            dataTuple = []
            counter = 0
            spriteID = database.execute(findSpriteIDSQL + str("'"+row[1]+"'")).fetchone()
            database.commit()
            database.close()

            if(spriteID == None):
                spriteID = -1
            else:
                spriteID = spriteID[0]
            for column in row:
                if(counter == 0):
                    dataTuple.append(spriteID)
                else:
                    dataTuple.append(column)
                counter += 1

            database = sqlite3.connect(DATABASE_PATH)
            dataTuple = tuple(dataTuple)
            database.execute(storeSingleRowSQL,dataTuple)
            database.commit()
            database.close()
            print("Just added/updated this value: " + dataTuple[1])

        database.commit()
        database.close()

    # Updates a Roster Table entirely with new CSV information. If the Roster doesn't currently exist in
    # the database, this method creates 4 new tables for it.
    def syncRoster(self,rosterName,throwErrorIfNoTables=False):
        database = sqlite3.connect(DATABASE_PATH)
        cursor = database.cursor()

        rosterPlayersTable = "ROS_" + rosterName + "_Players"
        rosterTeamsTable = "ROS_" + rosterName + "_Teams"
        rosterJerseysTable = "ROS_" + rosterName + "_Jerseys"
        rosterHeadshapesTable = "ROS_" + rosterName + "_Headshapes"
        if(throwErrorIfNoTables == False):
            # First, test to see if the roster tables exist. If they don't, create them.
            try:
                test = cursor.execute("SELECT SpriteID FROM " + rosterPlayersTable)
            except sqlite3.OperationalError:
                self.generateNewRosterTables(rosterName)
        else:
            test = cursor.execute("SELECT SpriteID FROM " + rosterPlayersTable)

        self.storeFullPlayersCSV(rosterName)



    # This method accepts a GameStats object, assuming that it is already populated
    # with statistics from a game, and stores them in the GameStats table.
    def storeGameStats(self,rippedStats,datePlayed=-1,startTime=-1,endTime=-1,customRule1=False,customRule2=False,customRule3=False,
                       customRule4=False,customRule5=False,customRule6=False,customRule7=False,customRule8=False,
                       customRule9=False,customRule10=False,):
        database = sqlite3.connect(DATABASE_PATH)
        cursor = database.cursor()


        rippedStats = StatsRipper.StatsRipper()
        storeGameStatsSQL = '''INSERT INTO GameStats (
                        	GameMode,DatePlayed,TimeBegan,TimeEnded,Roster,Team1Score,Team2Score,Slot1_SpriteID,Slot1_RosterID,Slot1_Points,Slot1_DefensiveRebounds,
                            Slot1_OffensiveRebounds,Slot1_PointsPerAssist,Slot1_Assists,Slot1_Steals,Slot1_Blocks,Slot1_Turnovers,Slot1_UnknownValue1,Slot1_InsideShotsMade,
                            Slot1_InsideShotsAttempted,Slot1_3ptShotsMade,Slot1_3ptShotsAttempted,Slot1_Fouls,Slot1_UnknownValue2,Slot1_Dunks,Slot1_Layups,Slot2_SpriteID,
                            Slot2_RosterID,Slot2_Points,Slot2_DefensiveRebounds,Slot2_OffensiveRebounds,Slot2_PointsPerAssist,Slot2_Assists,Slot2_Steals,Slot2_Blocks,Slot2_Turnovers,
                            Slot2_UnknownValue1,Slot2_InsideShotsMade,Slot2_InsideShotsAttempted,Slot2_3ptShotsMade,Slot2_3ptShotsAttempted,Slot2_Fouls,Slot2_UnknownValue2,Slot2_Dunks,Slot2_Layups,Slot3_SpriteID,
                            Slot3_RosterID,Slot3_Points,Slot3_DefensiveRebounds,Slot3_OffensiveRebounds,Slot3_PointsPerAssist,Slot3_Assists,Slot3_Steals,Slot3_Blocks,Slot3_Turnovers,
                            Slot3_UnknownValue1,Slot3_InsideShotsMade,Slot3_InsideShotsAttempted,Slot3_3ptShotsMade,Slot3_3ptShotsAttempted,Slot3_Fouls,Slot3_UnknownValue2,Slot3_Dunks,
                            Slot3_Layups,Slot4_SpriteID,Slot4_RosterID,Slot4_Points,Slot4_DefensiveRebounds,Slot4_OffensiveRebounds,Slot4_PointsPerAssist,Slot4_Assists,Slot4_Steals,Slot4_Blocks,
                            Slot4_Turnovers,Slot4_UnknownValue1,Slot4_InsideShotsMade,Slot4_InsideShotsAttempted,Slot4_3ptShotsMade,Slot4_3ptShotsAttempted,Slot4_Fouls,Slot4_UnknownValue2,Slot4_Dunks,Slot4_Layups,
                            Slot5_SpriteID,Slot5_RosterID,Slot5_Points,Slot5_DefensiveRebounds,Slot5_OffensiveRebounds,Slot5_PointsPerAssist,Slot5_Assists,Slot5_Steals,Slot5_Blocks,Slot5_Turnovers,Slot5_UnknownValue1,
                            Slot5_InsideShotsMade,Slot5_InsideShotsAttempted,Slot5_3ptShotsMade,Slot5_3ptShotsAttempted,Slot5_Fouls,Slot5_UnknownValue2,Slot5_Dunks,Slot5_Layups,Slot6_SpriteID,Slot6_RosterID,Slot6_Points,Slot6_DefensiveRebounds,
                            Slot6_OffensiveRebounds,Slot6_PointsPerAssist,Slot6_Assists,Slot6_Steals,Slot6_Blocks,Slot6_Turnovers,Slot6_UnknownValue1,Slot6_InsideShotsMade,Slot6_InsideShotsAttempted,Slot6_3ptShotsMade,
                            Slot6_3ptShotsAttempted,Slot6_Fouls,Slot6_UnknownValue2,Slot6_Dunks,Slot6_Layups,Slot7_SpriteID,Slot7_RosterID,Slot7_Points,Slot7_DefensiveRebounds,Slot7_OffensiveRebounds,Slot7_PointsPerAssist,
                            Slot7_Assists,Slot7_Steals,Slot7_Blocks,Slot7_Turnovers,Slot7_UnknownValue1,Slot7_InsideShotsMade,Slot7_InsideShotsAttempted,Slot7_3ptShotsMade,Slot7_3ptShotsAttempted,Slot7_Fouls,
                            Slot7_UnknownValue2,Slot7_Dunks,Slot7_Layups,Slot8_SpriteID,Slot8_RosterID,Slot8_Points,Slot8_DefensiveRebounds,Slot8_OffensiveRebounds,Slot8_PointsPerAssist,Slot8_Assists,Slot8_Steals,
                            Slot8_Blocks,Slot8_Turnovers,Slot8_UnknownValue1,Slot8_InsideShotsMade,Slot8_InsideShotsAttempted,Slot8_3ptShotsMade,Slot8_3ptShotsAttempted,Slot8_Fouls,Slot8_UnknownValue2,
                            Slot8_Dunks,Slot8_Layups,Slot9_SpriteID,Slot9_RosterID,Slot9_Points,Slot9_DefensiveRebounds,Slot9_OffensiveRebounds,Slot9_PointsPerAssist,Slot9_Assists,Slot9_Steals,
                            Slot9_Blocks,Slot9_Turnovers,Slot9_UnknownValue1,Slot9_InsideShotsMade,Slot9_InsideShotsAttempted,Slot9_3ptShotsMade,Slot9_3ptShotsAttempted,Slot9_Fouls,Slot9_UnknownValue2,
                            Slot9_Dunks,Slot9_Layups,Slot10_SpriteID,Slot10_RosterID,Slot10_Points,Slot10_DefensiveRebounds,Slot10_OffensiveRebounds,Slot10_PointsPerAssist,Slot10_Assists,
                            Slot10_Steals,Slot10_Blocks,Slot10_Turnovers,Slot10_UnknownValue1,Slot10_InsideShotsMade,Slot10_InsideShotsAttempted,Slot10_3ptShotsMade,Slot10_3ptShotsAttempted,Slot10_Fouls,Slot10_UnknownValue2,Slot10_Dunks,
                            Slot10_Layups,CustomRule1,CustomRule2,CustomRule3,CustomRule4,CustomRule5,CustomRule6,
                            CustomRule7,CustomRule8,CustomRule9,CustomRule10,
                            );''' # Simply stores all values from the game into the GameStats table.
        dataTuple = [rippedStats.gameMode,datePlayed,startTime,endTime,rippedStats.loadedRoster]
        team1Total = 0
        team2Total = 0
        for i in range(10):
            if(i < 5):
                if(rippedStats.slotStats[i][0] == 0):
                    continue
                else:
                    team1Total += rippedStats.slotStats[i][2] # Add all points together to find team total.
            else:
                if (rippedStats.slotStats[i][0] == 0):
                    continue
                else:
                    team2Total += rippedStats.slotStats[i][2]  # Add all points together to find team total.
        dataTuple += [team1Total,team2Total]
        for i in range(10):
            getPlayerSpriteIDSQL = "SELECT SpriteID FROM ROS_"
            getPlayerSpriteIDSQL += rippedStats.loadedRoster.strip(".ROS")
            getPlayerSpriteIDSQL += "_Players WHERE P_RosterID = "
            getPlayerSpriteIDSQL += str(rippedStats.slotStats[i][1])
            getPlayerSpriteIDSQL += ";"



myTree = ET.parse(DATA_PATH+"\\Players.xml")
myRoot = myTree.getroot()
walrus = myRoot.find("PLAYER[@spriteID='1']")
for i in walrus:
    print(i.tag,i.text)