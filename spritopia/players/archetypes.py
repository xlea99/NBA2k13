# Helper constants for accessing attribute accessors based on attribute categories.
OFFENSIVE_ATTRIBUTES = ["SShtCls","SLayUp","SPstFdaway","SPstHook","SOLowPost","SShtMed","SSht3PT","SShtInT","SShtOfD","SConsis"]
DEFENSIVE_ATTRIBUTES = ["SDLowPost","SStrength","SBlock","SOnBallD","SOReb","SDReb","SDAwar"]
CONTROL_ATTRIBUTES = ["SOffHDrib","SHands","SOAwar","SBallHndl","SHustle","SBallSec","SPass","SSpeed","SSteal","SQuick"]
GENERAL_ATTRIBUTES = ["SShtIns","SDunk","SStdDunk","SVertical","SShtFT","SStamina","SDurab","SPOT"]
ALL_ATTRIBUTES = ["SShtCls","SLayUp","SPstFdaway","SPstHook","SOLowPost","SShtMed","SSht3PT","SShtInT","SShtOfD","SConsis","SDLowPost","SStrength","SBlock","SOnBallD","SOReb","SDReb","SDAwar","SOffHDrib","SHands","SOAwar","SBallHndl","SHustle","SBallSec","SPass","SSpeed","SSteal","SQuick","SShtIns","SDunk","SStdDunk","SVertical","SShtFT","SStamina","SDurab","SPOT"]

# Helper map to map attribute accessors to the actual attribute name.
MAPPED_ATTRIBUTES = {"SShtIns": "Shot Inside",
                    "SShtCls": "Shot Close",
                    "SShtMed": "Shot Medium",
                    "SSht3PT": "Shot 3 PT",
                    "SShtFT": "Free Throw",
                    "SLayUp": "Lay Up",
                    "SDunk": "Dunk",
                    "SStdDunk": "Standing Dunk",
                    "SShtInT": "Shoot In Traffic",
                    "SPstFdaway": "Post Fadeaway",
                    "SPstHook": "Post Hook",
                    "SShtOfD": "Shoot Off Dribble",
                    "SBallHndl": "Ball Handling",
                    "SOffHDrib": "Off Hand Dribble",
                    "SBallSec": "Ball Security",
                    "SPass": "Pass",
                    "SBlock": "Block",
                    "SSteal": "Steal",
                    "SHands": "Hands",
                    "SOnBallD": "On Ball Defense",
                    "SOReb": "Off. Rebound",
                    "SDReb": "Def. Rebound",
                    "SOLowPost": "Low Post Offense",
                    "SDLowPost": "Low Post Defense",
                    "SOAwar": "Off. Awareness",
                    "SDAwar": "Def. Awareness",
                    "SConsis": "Consistency",
                    "SStamina": "Stamina",
                    "SSpeed": "Speed",
                    "SQuick": "Quickness",
                    "SStrength": "Strength",
                    "SVertical": "Vertical",
                    "SHustle": "Hustle",
                    "SDurab": "Durability",
                    "SPOT": "Potential",
                    "SEmotion": "Emotion"}

# This class represents a specific character 'Archetype,' of which
# there are 6.
class Archetype:
    def __init__(self, _archetypeID, _archetypeName):
        # This is a unique ID to distinguish between multiple archetypes.
        self.__archetypeID = _archetypeID
        self.archetypeName = _archetypeName

        self.attributeRanges = {"SShtIns" : [25,30],
                        "SShtCls" : [25,30],
                        "SShtMed" : [25,30],
                        "SSht3PT" : [25,30],
                        "SShtFT" : [25,30],
                        "SLayUp" : [25,30],
                        "SDunk" : [25,30],
                        "SStdDunk" : [25,30],
                        "SShtInT" : [25,30],
                        "SPstFdaway" : [25,30],
                        "SPstHook" : [25,30],
                        "SShtOfD" : [25,30],
                        "SBallHndl" : [25,30],
                        "SOffHDrib" : [25,30],
                        "SBallSec" : [25,30],
                        "SPass" : [25,30],
                        "SBlock" : [25,30],
                        "SSteal" : [25,30],
                        "SHands" : [25,30],
                        "SOnBallD" : [25,30],
                        "SOReb" : [25,30],
                        "SDReb" : [25,30],
                        "SOLowPost" : [25,30],
                        "SDLowPost" : [25,30],
                        "SOAwar" : [25,30],
                        "SDAwar" : [25,30],
                        "SConsis" : [25,30],
                        "SStamina" : [25,30],
                        "SSpeed" : [25,30],
                        "SQuick" : [25,30],
                        "SStrength" : [25,30],
                        "SVertical" : [25,30],
                        "SHustle" : [25,30],
                        "SDurab" : [25,30],
                        "SPOT" : [25,30],
                        "SEmotion" : [25,30]}

        # This is a list of all character skills available to the archetype.
        self.availableSkillCards = []

        # This stores the range of possible heights of the archetype.
        self.heightRange = []

        # This array stores which variables (indexed IDs) are 'core' to the
        # archetype, and the inverse.
        self.accentedAttributes = []
        self.unaccentedAttributes = []

        self.primaryAttributes = []
        self.secondaryAttributes = []
        self.tertiaryAttributes = []
        self.generalAttributes = GENERAL_ATTRIBUTES

        # This list roughly ranks the "importance" of each attribute to archetype.
        self.attributeImportance = []

        # This array contains valid team IDs for each archetype.
        self.validTeams = []

        # This value correlates to an in-game position that will always be used per archetype. Positions
        # are as follows:
        #
        # 0 - Point Guard
        # 1 - Shooting Guard
        # 2 - Small Forward
        # 3 - Power Forward
        # 4 - Center
        # 5 - None
        self.inGamePositionId = 5
        self.inGameSecondaryPositionId = 5
        self.inGamePositionString = "None"
        self.inGameSecondaryPositionString = "None"

        # Whether or not the player is a play initiator. Limited only to directors and engineers.
        self.isPlayInitiator = 0

        # This value relates to the ID number set in "TeamId1" and "TeamID2" to
        # get respective player jerseys by archetype.
        self.jerseyTeamId = -1


        # Here, all tendencies are listed as two number arrays.
        self.t_ShotTnd = []
        self.t_InsideShot = []
        self.t_CloseShot = []
        self.t_MidShot = []
        self.t_ShotThreePt = []
        self.t_DriveLane = []
        self.t_DriveRight = []
        self.t_PullUp = []
        self.t_PumpFake = []
        self.t_TripleThreat = []
        self.t_NoTripleThreat = []
        self.t_TripleThreatShot = []
        self.t_Sizeup = []
        self.t_Hesitation = []
        self.t_StraightDribble = []
        self.t_Crossover = []
        self.t_Spin = []
        self.t_Stepback = []
        self.t_Halfspin = []
        self.t_DoubleCrossover = []
        self.t_BehindBack = []
        self.t_HesitationCross = []
        self.t_InNOut = []
        self.t_SimpleDrive = []
        self.t_Attack = []
        self.t_PassOut = []
        self.t_Hopstep = []
        self.t_SpinLayup = []
        self.t_Eurostep = []
        self.t_Runner = []
        self.t_Fadeaway = []
        self.t_Dunk = []
        self.t_Crash = []
        self.t_Touches = []
        self.t_UsePick = []
        self.t_SetPick = []
        self.t_Isolation = []
        self.t_UseOffBallScreen = []
        self.t_SetOffBallScreen = []
        self.t_PostUp = []
        self.t_SpotUp = []
        self.t_PostSpin = []
        self.t_DropStep = []
        self.t_Shimmy = []
        self.t_FaceUp = []
        self.t_LeavePost = []
        self.t_BackDown = []
        self.t_AggressiveBackDown = []
        self.t_PostShot = []
        self.t_PostHook = []
        self.t_PostFade = []
        self.t_PostDrive = []
        self.t_HopShot = []
        self.t_Putback = []
        self.t_FlashyPass = []
        self.t_AlleyOop = []
        self.t_DrawFoul = []
        self.t_PlayPassLane = []
        self.t_TakeCharge = []
        self.t_OnBallSteal = []
        self.t_Contest = []
        self.t_CommitFoul = []
        self.t_HardFoul = []
        self.t_UseGlass = []
        self.t_StepbackJumper = []
        self.t_SpinJumper = []
        self.t_StepThrough = []
        self.t_ThrowAlleyOop = []
        self.t_GiveNGo = []

        # All hotspots listed as raw values, as well as chances that
        # the given archetype is going to get it.
        self.HIso3PLft = 0
        self.HIso3PCtr = 0
        self.HIso3PRgt = 0
        self.HIsoHPLft = 0
        self.HIsoHPCtr = 0
        self.HIsoHPRgt = 0
        self.HP_rLCrnr = 0
        self.HP_rLWing = 0
        self.HP_rTopOA = 0
        self.HP_rRWing = 0
        self.HP_rRCrnr = 0
        self.HSpt3PLCr = 0
        self.HSpt3PLWg = 0
        self.HSpt3PTop = 0
        self.HSpt3PRWg = 0
        self.HSpt3PRCr = 0
        self.HSptMdLBl = 0
        self.HSptMdLWg = 0
        self.HSptMdCtr = 0
        self.HSptMdRWg = 0
        self.HSptMdRBl = 0
        self.HPstRHigh = 0
        self.HPstRLow = 0
        self.HPstLHigh = 0
        self.HPstLLow = 0
        self.HIso3PLftChance = 0
        self.HIso3PCtrChance = 0
        self.HIso3PRgtChance = 0
        self.HIsoHPLftChance = 0
        self.HIsoHPCtrChance = 0
        self.HIsoHPRgtChance = 0
        self.HP_rLCrnrChance = 0
        self.HP_rLWingChance = 0
        self.HP_rTopOAChance = 0
        self.HP_rRWingChance = 0
        self.HP_rRCrnrChance = 0
        self.HSpt3PLCrChance = 0
        self.HSpt3PLWgChance = 0
        self.HSpt3PTopChance = 0
        self.HSpt3PRWgChance = 0
        self.HSpt3PRCrChance = 0
        self.HSptMdLBlChance = 0
        self.HSptMdLWgChance = 0
        self.HSptMdCtrChance = 0
        self.HSptMdRWgChance = 0
        self.HSptMdRBlChance = 0
        self.HPstRHighChance = 0
        self.HPstRLowChance = 0
        self.HPstLHighChance = 0
        self.HPstLLowChance = 0

    # Built in __eq__ magic method for testing against simple strings.
    def __eq__(self, other):
        # Check if 'other' is a string and compare it with the archetype name
        if isinstance(other, str):
            return self.archetypeName.lower() == other.lower()
        # Optionally, you can also enable comparison with other Archetype instances
        elif isinstance(other, Archetype):
            return self.archetypeName == other.archetypeName
        # Return NotImplemented when comparing with other types
        return NotImplemented

    # Simplified string method for getting the Archetype name.
    def __str__(self):
        return self.archetypeName


    # "Overloads" on methods that may be called on archetypes thinking its a string, simply
    # for ease of use.
    def lower(self):
        return self.archetypeName.lower()
    def upper(self):
        return self.archetypeName.upper()
    def capitalize(self):
        return self.archetypeName.capitalize()

    # STATS/SKILLS


#region ATTRIBUTES - Slayer
ARCH_SLAYER = Archetype(1,"Slayer")
ARCH_SLAYER.heightRange = [63,70]
ARCH_SLAYER.validTeams = ["1","2","3","4","5","6","7","8","9"]
ARCH_SLAYER.jerseyTeamId = 0
ARCH_SLAYER.inGamePositionId = 1
ARCH_SLAYER.inGamePositionString = "SG"
ARCH_SLAYER.inGameSecondaryPositionId = 0
ARCH_SLAYER.inGameSecondaryPositionString = "PG"

ARCH_SLAYER.primaryAttributes = OFFENSIVE_ATTRIBUTES
ARCH_SLAYER.secondaryAttributes = CONTROL_ATTRIBUTES
ARCH_SLAYER.tertiaryAttributes = DEFENSIVE_ATTRIBUTES

ARCH_SLAYER.accentedAttributes = ["SLayUp", "SShtMed","SSht3PT","SShtOfD","SConsis","SOAwar","SPass","SSpeed","SHustle","SQuick","SDLowPost","SStrength","SBlock","SOnBallD"]
ARCH_SLAYER.unaccentedAttributes = ['SShtCls', 'SPstFdaway', 'SPstHook', 'SOLowPost', 'SShtInT', 'SOReb', 'SDReb', 'SDAwar', 'SOffHDrib', 'SHands', 'SBallHndl', 'SBallSec', 'SSteal', 'SShtIns', 'SDunk', 'SStdDunk', 'SVertical', 'SShtFT', 'SStamina', 'SDurab', 'SPOT']
ARCH_SLAYER.attributeImportance = ['SSht3PT', 'SSpeed', 'SShtOfD', 'SConsis', 'SShtInT', 'SBallSec', 'SVertical', 'SSteal', 'SDReb', 'SOReb', 'SBallHndl', 'SOffHDrib', 'SDunk', 'SQuick', 'SOAwar', 'SOnBallD', 'SDAwar', 'SLayUp', 'SShtMed', 'SHands', 'SPass', 'SHustle', 'SStrength', 'SBlock', 'SShtIns', 'SStdDunk', 'SShtCls', 'SPstFdaway', 'SPstHook', 'SOLowPost', 'SDLowPost']
ARCH_SLAYER.attributeRanges["SOffHDrib"] = [45, 65]
ARCH_SLAYER.attributeRanges["SHands"] = [45, 65]
ARCH_SLAYER.attributeRanges["SOAwar"] = [50, 70]
ARCH_SLAYER.attributeRanges["SBallHndl"] = [40, 60]
ARCH_SLAYER.attributeRanges["SBallSec"] = [40, 60]
ARCH_SLAYER.attributeRanges["SPass"] = [50, 70]
ARCH_SLAYER.attributeRanges["SSpeed"] = [55, 75]
ARCH_SLAYER.attributeRanges["SQuick"] = [55, 75]
ARCH_SLAYER.attributeRanges["SHustle"] = [50, 70]
ARCH_SLAYER.attributeRanges["SSteal"] = [35, 55]
ARCH_SLAYER.attributeRanges["SDLowPost"] = [35, 50]
ARCH_SLAYER.attributeRanges["SStrength"] = [35, 50]
ARCH_SLAYER.attributeRanges["SBlock"] = [35, 50]
ARCH_SLAYER.attributeRanges["SOnBallD"] = [35, 50]
ARCH_SLAYER.attributeRanges["SOReb"] = [25, 40]
ARCH_SLAYER.attributeRanges["SDReb"] = [25, 40]
ARCH_SLAYER.attributeRanges["SDAwar"] = [25, 45]
ARCH_SLAYER.attributeRanges["SShtIns"] = [70, 90]
ARCH_SLAYER.attributeRanges["SDunk"] = [30, 50]
ARCH_SLAYER.attributeRanges["SStdDunk"] = [20, 40]
ARCH_SLAYER.attributeRanges["SVertical"] = [30, 50]
ARCH_SLAYER.attributeRanges["SShtFT"] = [80, 99]
ARCH_SLAYER.attributeRanges["SStamina"] = [50, 85]
ARCH_SLAYER.attributeRanges["SDurab"] = [50, 85]
ARCH_SLAYER.attributeRanges["SPOT"] = [25, 99]
ARCH_SLAYER.attributeRanges["SShtCls"] = [80, 90]
ARCH_SLAYER.attributeRanges["SLayUp"] = [85, 99]
ARCH_SLAYER.attributeRanges["SPstFdaway"] = [75, 90]
ARCH_SLAYER.attributeRanges["SPstHook"] = [75, 90]
ARCH_SLAYER.attributeRanges["SOLowPost"] = [75, 90]
ARCH_SLAYER.attributeRanges["SShtMed"] = [75, 95]
ARCH_SLAYER.attributeRanges["SSht3PT"] = [70, 80]
ARCH_SLAYER.attributeRanges["SShtInT"] = [65, 85]
ARCH_SLAYER.attributeRanges["SShtOfD"] = [75, 99]
ARCH_SLAYER.attributeRanges["SConsis"] = [80, 99]


#"Posterizer","Finisher","Spot-up Shooter","Shot Creator", "Deadeye", "Corner Specialist","Post Proficiency", "Post Playmaker", "Dimer","Alley-ooper", "Antifreeze", "Microwave","Heat Retention"
ARCH_SLAYER.availableSkillCards = ["1","3","5","6", "7", "8","9", "11", "12","14", "26", "27","28"]
#endregion ATTRIBUTES - Slayer
#region TENDENCIES - Slayer
ARCH_SLAYER.t_ShotTnd = [70,100]
ARCH_SLAYER.t_InsideShot = [0,60]
ARCH_SLAYER.t_CloseShot = [0,60]
ARCH_SLAYER.t_MidShot = [70,100]
ARCH_SLAYER.t_ShotThreePt = [80,100]
ARCH_SLAYER.t_Putback = [0, 100]

ARCH_SLAYER.t_DriveLane = [0,100]
ARCH_SLAYER.t_DriveRight = [0,100]

ARCH_SLAYER.t_PullUp = [70,100]

ARCH_SLAYER.t_PumpFake = [0,100]
ARCH_SLAYER.t_TripleThreat = [0,100]
ARCH_SLAYER.t_NoTripleThreat = [0,75]
ARCH_SLAYER.t_TripleThreatShot = [60,100]

ARCH_SLAYER.t_Sizeup = [0,100]
ARCH_SLAYER.t_Hesitation = [0,100]
ARCH_SLAYER.t_StraightDribble = [0,100]

ARCH_SLAYER.t_Crossover = [0,75]
ARCH_SLAYER.t_Spin = [0,75]
ARCH_SLAYER.t_Stepback = [0,75]
ARCH_SLAYER.t_Halfspin = [0,75]
ARCH_SLAYER.t_DoubleCrossover = [0,75]
ARCH_SLAYER.t_BehindBack = [0,75]
ARCH_SLAYER.t_HesitationCross = [0,75]
ARCH_SLAYER.t_InNOut = [0,75]
ARCH_SLAYER.t_SimpleDrive = [0,75]

ARCH_SLAYER.t_Attack = [40,100]
ARCH_SLAYER.t_PassOut = [0,60]

ARCH_SLAYER.t_Hopstep = [0,100]
ARCH_SLAYER.t_SpinLayup = [0,100]
ARCH_SLAYER.t_Eurostep = [0,100]

ARCH_SLAYER.t_Runner = [0,100]
ARCH_SLAYER.t_Fadeaway = [0,100]
ARCH_SLAYER.t_StepbackJumper = [0, 100]
ARCH_SLAYER.t_SpinJumper = [0, 100]

ARCH_SLAYER.t_Dunk = [0,100] # Uses Dunk Stat instead

ARCH_SLAYER.t_Crash = [0,100]
ARCH_SLAYER.t_AlleyOop = [25, 75]
ARCH_SLAYER.t_DrawFoul = [0, 100]
ARCH_SLAYER.t_UseGlass = [0, 100]
ARCH_SLAYER.t_StepThrough = [0, 100]

ARCH_SLAYER.t_Touches = [75,100]
ARCH_SLAYER.t_UsePick = [80,100]
ARCH_SLAYER.t_SetPick = [0,10]
ARCH_SLAYER.t_Isolation = [75,100]
ARCH_SLAYER.t_UseOffBallScreen = [60,100]
ARCH_SLAYER.t_SetOffBallScreen = [0,15]
ARCH_SLAYER.t_PostUp = [0,10]
ARCH_SLAYER.t_SpotUp = [80,100]
ARCH_SLAYER.t_GiveNGo = [0, 30]

ARCH_SLAYER.t_PostSpin = [0,100]
ARCH_SLAYER.t_DropStep = [0,100]
ARCH_SLAYER.t_Shimmy = [0,100]
ARCH_SLAYER.t_FaceUp = [0,100]
ARCH_SLAYER.t_LeavePost = [0,100]
ARCH_SLAYER.t_BackDown = [0,100]
ARCH_SLAYER.t_AggressiveBackDown = [0,100]
ARCH_SLAYER.t_PostShot = [0,100]
ARCH_SLAYER.t_PostHook = [0,100]
ARCH_SLAYER.t_PostFade = [0,100]
ARCH_SLAYER.t_PostDrive = [0,100]
ARCH_SLAYER.t_HopShot = [0,100]

ARCH_SLAYER.t_FlashyPass = [25,60]
ARCH_SLAYER.t_ThrowAlleyOop = [25, 60]

ARCH_SLAYER.t_PlayPassLane = [0,100]
ARCH_SLAYER.t_TakeCharge = [0,100]
ARCH_SLAYER.t_OnBallSteal = [0,100] # This will be set to the steal stat.
ARCH_SLAYER.t_Contest = [0,25]
ARCH_SLAYER.t_CommitFoul = [0,100]
ARCH_SLAYER.t_HardFoul = [0,100]
#endregion TENDENCIES - Slayer
#region HOTSPOTS - Slayer
# Isolation
ARCH_SLAYER.HIso3PLftChance = 32
ARCH_SLAYER.HIso3PCtrChance = 32
ARCH_SLAYER.HIso3PRgtChance = 32
ARCH_SLAYER.HIsoHPLftChance = 2
ARCH_SLAYER.HIsoHPCtrChance = 2
ARCH_SLAYER.HIsoHPRgtChance = 2

# Pick and Roll
ARCH_SLAYER.HP_rLCrnrChance = 5
ARCH_SLAYER.HP_rLWingChance = 20
ARCH_SLAYER.HP_rTopOAChance = 20
ARCH_SLAYER.HP_rRWingChance = 20
ARCH_SLAYER.HP_rRCrnrChance = 5

# Spot Up
ARCH_SLAYER.HSpt3PLCrChance = 30
ARCH_SLAYER.HSpt3PLWgChance = 30
ARCH_SLAYER.HSpt3PTopChance = 30
ARCH_SLAYER.HSpt3PRWgChance = 30
ARCH_SLAYER.HSpt3PRCrChance = 30
ARCH_SLAYER.HSptMdLBlChance = 2
ARCH_SLAYER.HSptMdLWgChance = 2
ARCH_SLAYER.HSptMdCtrChance = 2
ARCH_SLAYER.HSptMdRWgChance = 2
ARCH_SLAYER.HSptMdRBlChance = 2

# Post
ARCH_SLAYER.HPstRHighChance = 30
ARCH_SLAYER.HPstRLowChance = 20
ARCH_SLAYER.HPstLHighChance = 30
ARCH_SLAYER.HPstLLowChance = 20
#endregion HOTSPOTS - Slayer

#region ATTRIBUTES - Vigilante
ARCH_VIGILANTE = Archetype(2,"Vigilante")
ARCH_VIGILANTE.heightRange = [69,75]
ARCH_VIGILANTE.validTeams = ["11","12","13","14","15","16","17","18","19"]
ARCH_VIGILANTE.jerseyTeamId = 1
ARCH_VIGILANTE.inGamePositionId = 2
ARCH_VIGILANTE.inGamePositionString = "SF"
ARCH_VIGILANTE.inGameSecondaryPositionId = 3
ARCH_VIGILANTE.inGameSecondaryPositionString = "PF"

ARCH_VIGILANTE.primaryAttributes = OFFENSIVE_ATTRIBUTES
ARCH_VIGILANTE.secondaryAttributes = DEFENSIVE_ATTRIBUTES
ARCH_VIGILANTE.tertiaryAttributes = CONTROL_ATTRIBUTES

ARCH_VIGILANTE.accentedAttributes = ["SShtCls","SPstFdaway","SPstHook","SOLowPost","SShtInT","SDLowPost","SStrength","SBlock","SOnBallD","SOAwar","SHustle","SPass","SSpeed","SQuick"]
ARCH_VIGILANTE.unaccentedAttributes = ['SLayUp', 'SShtMed', 'SSht3PT', 'SShtOfD', 'SConsis', 'SOReb', 'SDReb', 'SDAwar', 'SOffHDrib', 'SHands', 'SBallHndl', 'SBallSec', 'SSteal', 'SShtIns', 'SDunk', 'SStdDunk', 'SVertical', 'SShtFT', 'SStamina', 'SDurab', 'SPOT']
ARCH_VIGILANTE.attributeImportance = ['SSht3PT', 'SShtInT', 'SShtOfD', 'SSpeed', 'SConsis', 'SVertical', 'SDReb', 'SOReb', 'SOnBallD', 'SDunk', 'SSteal', 'SLayUp', 'SBallHndl', 'SBallSec', 'SStrength', 'SBlock', 'SDAwar', 'SStdDunk', 'SShtMed', 'SShtCls', 'SOffHDrib', 'SHands', 'SOAwar', 'SPass', 'SQuick', 'SHustle', 'SDLowPost', 'SPstFdaway', 'SPstHook', 'SOLowPost', 'SShtIns']
ARCH_VIGILANTE.attributeRanges["SOffHDrib"] = [25, 40]
ARCH_VIGILANTE.attributeRanges["SHands"] = [25, 40]
ARCH_VIGILANTE.attributeRanges["SOAwar"] = [30, 50]
ARCH_VIGILANTE.attributeRanges["SBallHndl"] = [25, 40]
ARCH_VIGILANTE.attributeRanges["SBallSec"] = [25, 40]
ARCH_VIGILANTE.attributeRanges["SPass"] = [35, 50]
ARCH_VIGILANTE.attributeRanges["SSpeed"] = [30, 60]
ARCH_VIGILANTE.attributeRanges["SQuick"] = [30, 60]
ARCH_VIGILANTE.attributeRanges["SHustle"] = [30, 50]
ARCH_VIGILANTE.attributeRanges["SSteal"] = [25, 35]
ARCH_VIGILANTE.attributeRanges["SDLowPost"] = [50, 70]
ARCH_VIGILANTE.attributeRanges["SStrength"] = [50, 70]
ARCH_VIGILANTE.attributeRanges["SBlock"] = [50, 70]
ARCH_VIGILANTE.attributeRanges["SOnBallD"] = [50, 70]
ARCH_VIGILANTE.attributeRanges["SOReb"] = [40, 50]
ARCH_VIGILANTE.attributeRanges["SDReb"] = [40, 50]
ARCH_VIGILANTE.attributeRanges["SDAwar"] = [40, 60]
ARCH_VIGILANTE.attributeRanges["SShtIns"] = [80, 99]
ARCH_VIGILANTE.attributeRanges["SDunk"] = [85, 99]
ARCH_VIGILANTE.attributeRanges["SStdDunk"] = [70, 90]
ARCH_VIGILANTE.attributeRanges["SVertical"] = [40, 60]
ARCH_VIGILANTE.attributeRanges["SShtFT"] = [80, 100]
ARCH_VIGILANTE.attributeRanges["SStamina"] = [50, 85]
ARCH_VIGILANTE.attributeRanges["SDurab"] = [50, 85]
ARCH_VIGILANTE.attributeRanges["SPOT"] = [25, 99]
ARCH_VIGILANTE.attributeRanges["SShtCls"] = [85, 99]
ARCH_VIGILANTE.attributeRanges["SLayUp"] = [75, 90]
ARCH_VIGILANTE.attributeRanges["SPstFdaway"] = [85, 99]
ARCH_VIGILANTE.attributeRanges["SPstHook"] = [85, 99]
ARCH_VIGILANTE.attributeRanges["SOLowPost"] = [85, 99]
ARCH_VIGILANTE.attributeRanges["SShtMed"] = [70, 85]
ARCH_VIGILANTE.attributeRanges["SSht3PT"] = [65, 75]
ARCH_VIGILANTE.attributeRanges["SShtInT"] = [75, 99]
ARCH_VIGILANTE.attributeRanges["SShtOfD"] = [65, 85]
ARCH_VIGILANTE.attributeRanges["SConsis"] = [60, 90]

# "Posterizer","Highlight Film", "Finisher","Acrobat","Deadeye","Corner Specialist","Brick Wall", "Hustle Points", "Floor General"
ARCH_VIGILANTE.availableSkillCards = ["1", "2", "3","4", "7", "8","15", "24", "30"]
#endregion ATTRIBUTES - Vigilante
#region TENDENCIES - Vigilante
ARCH_VIGILANTE.t_ShotTnd = [60,100]
ARCH_VIGILANTE.t_InsideShot = [25,75]
ARCH_VIGILANTE.t_CloseShot = [25,75]
ARCH_VIGILANTE.t_MidShot = [50,100]
ARCH_VIGILANTE.t_ShotThreePt = [50,100]
ARCH_VIGILANTE.t_Putback = [0, 100]

ARCH_VIGILANTE.t_DriveLane = [0,100]
ARCH_VIGILANTE.t_DriveRight = [0,100]

ARCH_VIGILANTE.t_PullUp = [50,100]

ARCH_VIGILANTE.t_PumpFake = [0,100]
ARCH_VIGILANTE.t_TripleThreat = [0,100]
ARCH_VIGILANTE.t_NoTripleThreat = [0,75]
ARCH_VIGILANTE.t_TripleThreatShot = [60,100]

ARCH_VIGILANTE.t_Sizeup = [0,100]
ARCH_VIGILANTE.t_Hesitation = [0,100]
ARCH_VIGILANTE.t_StraightDribble = [0,100]

ARCH_VIGILANTE.t_Crossover = [0,50]
ARCH_VIGILANTE.t_Spin = [0,50]
ARCH_VIGILANTE.t_Stepback = [0,50]
ARCH_VIGILANTE.t_Halfspin = [0,50]
ARCH_VIGILANTE.t_DoubleCrossover = [0,50]
ARCH_VIGILANTE.t_BehindBack = [0,50]
ARCH_VIGILANTE.t_HesitationCross = [0,50]
ARCH_VIGILANTE.t_InNOut = [0,50]
ARCH_VIGILANTE.t_SimpleDrive = [0,50]

ARCH_VIGILANTE.t_Attack = [40,100]
ARCH_VIGILANTE.t_PassOut = [0,60]

ARCH_VIGILANTE.t_Hopstep = [0,100]
ARCH_VIGILANTE.t_SpinLayup = [0,100]
ARCH_VIGILANTE.t_Eurostep = [0,100]

ARCH_VIGILANTE.t_Runner = [0,100]
ARCH_VIGILANTE.t_Fadeaway = [0,100]
ARCH_VIGILANTE.t_StepbackJumper = [0, 100]
ARCH_VIGILANTE.t_SpinJumper = [0, 100]

ARCH_VIGILANTE.t_Dunk = [0,100] # Uses Dunk Stat instead

ARCH_VIGILANTE.t_Crash = [0,100]
ARCH_VIGILANTE.t_AlleyOop = [0, 40]
ARCH_VIGILANTE.t_DrawFoul = [0, 100]
ARCH_VIGILANTE.t_UseGlass = [0, 100]
ARCH_VIGILANTE.t_StepThrough = [0, 100]

ARCH_VIGILANTE.t_Touches = [0,100]
ARCH_VIGILANTE.t_UsePick = [25,100]
ARCH_VIGILANTE.t_SetPick = [25,100]
ARCH_VIGILANTE.t_Isolation = [40,75]
ARCH_VIGILANTE.t_UseOffBallScreen = [25,100]
ARCH_VIGILANTE.t_SetOffBallScreen = [25,100]
ARCH_VIGILANTE.t_PostUp = [25,75]
ARCH_VIGILANTE.t_SpotUp = [60,100]
ARCH_VIGILANTE.t_GiveNGo = [0,50]

ARCH_VIGILANTE.t_PostSpin = [0,100]
ARCH_VIGILANTE.t_DropStep = [0,100]
ARCH_VIGILANTE.t_Shimmy = [0,100]
ARCH_VIGILANTE.t_FaceUp = [0,100]
ARCH_VIGILANTE.t_LeavePost = [0,100]
ARCH_VIGILANTE.t_BackDown = [0,100]
ARCH_VIGILANTE.t_AggressiveBackDown = [0,100]
ARCH_VIGILANTE.t_PostShot = [0,100]
ARCH_VIGILANTE.t_PostHook = [0,100]
ARCH_VIGILANTE.t_PostFade = [0,100]
ARCH_VIGILANTE.t_PostDrive = [0,100]
ARCH_VIGILANTE.t_HopShot = [0,100]

ARCH_VIGILANTE.t_FlashyPass = [0,25]
ARCH_VIGILANTE.t_ThrowAlleyOop = [0, 25]

ARCH_VIGILANTE.t_PlayPassLane = [0,100]
ARCH_VIGILANTE.t_TakeCharge = [0,100]
ARCH_VIGILANTE.t_OnBallSteal = [0,100]
ARCH_VIGILANTE.t_Contest = [30,80]
ARCH_VIGILANTE.t_CommitFoul = [0,100]
ARCH_VIGILANTE.t_HardFoul = [0,100]
#endregion TENDENCIES - Vigilante
#region HOTSPOTS - Vigilante
# Isolation
ARCH_VIGILANTE.HIso3PLftChance = 28
ARCH_VIGILANTE.HIso3PCtrChance = 28
ARCH_VIGILANTE.HIso3PRgtChance = 28
ARCH_VIGILANTE.HIsoHPLftChance = 5
ARCH_VIGILANTE.HIsoHPCtrChance = 5
ARCH_VIGILANTE.HIsoHPRgtChance = 5

# Pick and Roll
ARCH_VIGILANTE.HP_rLCrnrChance = 10
ARCH_VIGILANTE.HP_rLWingChance = 15
ARCH_VIGILANTE.HP_rTopOAChance = 15
ARCH_VIGILANTE.HP_rRWingChance = 15
ARCH_VIGILANTE.HP_rRCrnrChance = 10

# Spot Up
ARCH_VIGILANTE.HSpt3PLCrChance = 28
ARCH_VIGILANTE.HSpt3PLWgChance = 28
ARCH_VIGILANTE.HSpt3PTopChance = 28
ARCH_VIGILANTE.HSpt3PRWgChance = 28
ARCH_VIGILANTE.HSpt3PRCrChance = 28
ARCH_VIGILANTE.HSptMdLBlChance = 5
ARCH_VIGILANTE.HSptMdLWgChance = 5
ARCH_VIGILANTE.HSptMdCtrChance = 5
ARCH_VIGILANTE.HSptMdRWgChance = 5
ARCH_VIGILANTE.HSptMdRBlChance = 5

# Post
ARCH_VIGILANTE.HPstRHighChance = 30
ARCH_VIGILANTE.HPstRLowChance = 20
ARCH_VIGILANTE.HPstLHighChance = 30
ARCH_VIGILANTE.HPstLLowChance = 20
#endregion HOTSPOTS - Vigilante

#region ATTRIBUTES - Medic
ARCH_MEDIC = Archetype(3,"Medic")
ARCH_MEDIC.heightRange = [73,82]
ARCH_MEDIC.validTeams = ["21","22","23","24","25","26","27","28","29"]
ARCH_MEDIC.jerseyTeamId = 2
ARCH_MEDIC.inGamePositionId = 4
ARCH_MEDIC.inGamePositionString = "C"
ARCH_MEDIC.inGameSecondaryPositionId = 0
ARCH_MEDIC.inGameSecondaryPositionString = "PG"

ARCH_MEDIC.primaryAttributes = DEFENSIVE_ATTRIBUTES
ARCH_MEDIC.secondaryAttributes = CONTROL_ATTRIBUTES
ARCH_MEDIC.tertiaryAttributes = OFFENSIVE_ATTRIBUTES

ARCH_MEDIC.accentedAttributes = ["SShtCls","SOAwar","SPstFdaway","SPstHook","SOLowPost","SShtInT","SOReb", "SDReb", "SDAwar","SOffHDrib","SHands","SBallSec","SBallHndl","SSteal"]
ARCH_MEDIC.unaccentedAttributes = ['SLayUp', 'SShtMed', 'SSht3PT', 'SShtOfD', 'SConsis', 'SDLowPost', 'SStrength', 'SBlock', 'SOnBallD', 'SHustle', 'SPass', 'SSpeed', 'SQuick', 'SShtIns', 'SDunk', 'SStdDunk', 'SVertical', 'SShtFT', 'SStamina', 'SDurab', 'SPOT']
ARCH_MEDIC.attributeImportance = ['SVertical', 'SDReb', 'SOReb', 'SSpeed', 'SPass', 'SDAwar', 'SSteal', 'SSht3PT', 'SBallSec', 'SOnBallD', 'SOAwar', 'SQuick', 'SHustle', 'SBlock', 'SStrength', 'SHands', 'SOffHDrib', 'SBallHndl', 'SDunk', 'SStdDunk', 'SShtIns', 'SShtInT', 'SShtOfD', 'SConsis', 'SShtCls', 'SShtMed', 'SLayUp', 'SPstFdaway', 'SPstHook', 'SOLowPost', 'SDLowPost']
ARCH_MEDIC.attributeRanges["SOffHDrib"] = [55, 75]
ARCH_MEDIC.attributeRanges["SHands"] = [60, 80]
ARCH_MEDIC.attributeRanges["SOAwar"] = [40, 60]
ARCH_MEDIC.attributeRanges["SBallHndl"] = [50, 70]
ARCH_MEDIC.attributeRanges["SBallSec"] = [50, 70]
ARCH_MEDIC.attributeRanges["SPass"] = [40, 60]
ARCH_MEDIC.attributeRanges["SSpeed"] = [45, 65]
ARCH_MEDIC.attributeRanges["SQuick"] = [45, 65]
ARCH_MEDIC.attributeRanges["SHustle"] = [40, 60]
ARCH_MEDIC.attributeRanges["SSteal"] = [45, 65]
ARCH_MEDIC.attributeRanges["SDLowPost"] = [70, 90]
ARCH_MEDIC.attributeRanges["SStrength"] = [65, 85]
ARCH_MEDIC.attributeRanges["SBlock"] = [70, 90]
ARCH_MEDIC.attributeRanges["SOnBallD"] = [65, 85]
ARCH_MEDIC.attributeRanges["SOReb"] = [80, 99]
ARCH_MEDIC.attributeRanges["SDReb"] = [80, 99]
ARCH_MEDIC.attributeRanges["SDAwar"] = [70, 99]
ARCH_MEDIC.attributeRanges["SShtIns"] = [60, 65]
ARCH_MEDIC.attributeRanges["SDunk"] = [40, 60]
ARCH_MEDIC.attributeRanges["SStdDunk"] = [40, 60]
ARCH_MEDIC.attributeRanges["SVertical"] = [80, 99]
ARCH_MEDIC.attributeRanges["SShtFT"] = [80, 99]
ARCH_MEDIC.attributeRanges["SStamina"] = [50, 85]
ARCH_MEDIC.attributeRanges["SDurab"] = [50, 85]
ARCH_MEDIC.attributeRanges["SPOT"] = [25, 99]
ARCH_MEDIC.attributeRanges["SShtCls"] = [50, 60]
ARCH_MEDIC.attributeRanges["SLayUp"] = [25, 40]
ARCH_MEDIC.attributeRanges["SPstFdaway"] = [35, 50]
ARCH_MEDIC.attributeRanges["SPstHook"] = [35, 50]
ARCH_MEDIC.attributeRanges["SOLowPost"] = [35, 50]
ARCH_MEDIC.attributeRanges["SShtMed"] = [25, 40]
ARCH_MEDIC.attributeRanges["SSht3PT"] = [25, 35]
ARCH_MEDIC.attributeRanges["SShtInT"] = [35, 50]
ARCH_MEDIC.attributeRanges["SShtOfD"] = [25, 40]
ARCH_MEDIC.attributeRanges["SConsis"] = [25, 40]

# "Ankle Breaker", "Post Playmaker", "Dimer","Break Starter", "Brick Wall", "Lockdown Defender","Interceptor", "Pickpocket", "Eraser","Scrapper"
ARCH_MEDIC.availableSkillCards = ["10", "11", "12","13", "15", "16","18", "19", "21","25"]
#endregion ATTRIBUTES - Medic
#region TENDENCIES - Medic
ARCH_MEDIC.t_ShotTnd = [0,30]
ARCH_MEDIC.t_InsideShot = [0,50]
ARCH_MEDIC.t_CloseShot = [0,50]
ARCH_MEDIC.t_MidShot = [0,20]
ARCH_MEDIC.t_ShotThreePt = [0,5]
ARCH_MEDIC.t_Putback = [60, 100]

ARCH_MEDIC.t_DriveLane = [0,50]
ARCH_MEDIC.t_DriveRight = [0,100]

ARCH_MEDIC.t_PullUp = [0,30]

ARCH_MEDIC.t_PumpFake = [0,70]
ARCH_MEDIC.t_TripleThreat = [0,100]
ARCH_MEDIC.t_NoTripleThreat = [50,100]
ARCH_MEDIC.t_TripleThreatShot = [0,5]

ARCH_MEDIC.t_Sizeup = [0,100]
ARCH_MEDIC.t_Hesitation = [0,100]
ARCH_MEDIC.t_StraightDribble = [0,100]

ARCH_MEDIC.t_Crossover = [0,75]
ARCH_MEDIC.t_Spin = [0,75]
ARCH_MEDIC.t_Stepback = [0,75]
ARCH_MEDIC.t_Halfspin = [0,75]
ARCH_MEDIC.t_DoubleCrossover = [0,75]
ARCH_MEDIC.t_BehindBack = [0,75]
ARCH_MEDIC.t_HesitationCross = [0,75]
ARCH_MEDIC.t_InNOut = [0,75]
ARCH_MEDIC.t_SimpleDrive = [0,75]

ARCH_MEDIC.t_Attack = [0,25]
ARCH_MEDIC.t_PassOut = [60,100]

ARCH_MEDIC.t_Hopstep = [0,100]
ARCH_MEDIC.t_SpinLayup = [0,100]
ARCH_MEDIC.t_Eurostep = [0,100]

ARCH_MEDIC.t_Runner = [0,100]
ARCH_MEDIC.t_Fadeaway = [0,100]
ARCH_MEDIC.t_StepbackJumper = [0, 100]
ARCH_MEDIC.t_SpinJumper = [0, 100]

ARCH_MEDIC.t_Dunk = [0,100] # Uses Dunk Stat instead

ARCH_MEDIC.t_Crash = [0,100]
ARCH_MEDIC.t_AlleyOop = [25, 75]
ARCH_MEDIC.t_DrawFoul = [0, 100]
ARCH_MEDIC.t_UseGlass = [0, 100]
ARCH_MEDIC.t_StepThrough = [0, 100]

ARCH_MEDIC.t_Touches = [0,100]
ARCH_MEDIC.t_UsePick = [0,10]
ARCH_MEDIC.t_SetPick = [80,100]
ARCH_MEDIC.t_Isolation = [0,5]
ARCH_MEDIC.t_UseOffBallScreen = [0,5]
ARCH_MEDIC.t_SetOffBallScreen = [80,100]
ARCH_MEDIC.t_PostUp = [40,80]
ARCH_MEDIC.t_SpotUp = [0,10]
ARCH_MEDIC.t_GiveNGo = [0, 100]

ARCH_MEDIC.t_PostSpin = [0,100]
ARCH_MEDIC.t_DropStep = [0,100]
ARCH_MEDIC.t_Shimmy = [0,100]
ARCH_MEDIC.t_FaceUp = [0,100]
ARCH_MEDIC.t_LeavePost = [0,100]
ARCH_MEDIC.t_BackDown = [0,100]
ARCH_MEDIC.t_AggressiveBackDown = [0,100]
ARCH_MEDIC.t_PostShot = [0,100]
ARCH_MEDIC.t_PostHook = [0,100]
ARCH_MEDIC.t_PostFade = [0,100]
ARCH_MEDIC.t_PostDrive = [0,100]
ARCH_MEDIC.t_HopShot = [0,100]

ARCH_MEDIC.t_FlashyPass = [25,70]
ARCH_MEDIC.t_ThrowAlleyOop = [25, 70]

ARCH_MEDIC.t_PlayPassLane = [0,100]
ARCH_MEDIC.t_TakeCharge = [25,100]
ARCH_MEDIC.t_OnBallSteal = [0,100]
ARCH_MEDIC.t_Contest = [75,100]
ARCH_MEDIC.t_CommitFoul = [0,100]
ARCH_MEDIC.t_HardFoul = [0,100]
#endregion TENDENCIES - Medic
#region HOTSPOTS - Medic
# Isolation
ARCH_MEDIC.HIso3PLftChance = 1
ARCH_MEDIC.HIso3PCtrChance = 1
ARCH_MEDIC.HIso3PRgtChance = 1
ARCH_MEDIC.HIsoHPLftChance = 32
ARCH_MEDIC.HIsoHPCtrChance = 32
ARCH_MEDIC.HIsoHPRgtChance = 32

# Pick and Roll
ARCH_MEDIC.HP_rLCrnrChance = 5
ARCH_MEDIC.HP_rLWingChance = 20
ARCH_MEDIC.HP_rTopOAChance = 20
ARCH_MEDIC.HP_rRWingChance = 20
ARCH_MEDIC.HP_rRCrnrChance = 5

# Spot Up
ARCH_MEDIC.HSpt3PLCrChance = 1
ARCH_MEDIC.HSpt3PLWgChance = 1
ARCH_MEDIC.HSpt3PTopChance = 1
ARCH_MEDIC.HSpt3PRWgChance = 1
ARCH_MEDIC.HSpt3PRCrChance = 1
ARCH_MEDIC.HSptMdLBlChance = 32
ARCH_MEDIC.HSptMdLWgChance = 5
ARCH_MEDIC.HSptMdCtrChance = 5
ARCH_MEDIC.HSptMdRWgChance = 5
ARCH_MEDIC.HSptMdRBlChance = 32

# Post
ARCH_MEDIC.HPstRHighChance = 20
ARCH_MEDIC.HPstRLowChance = 30
ARCH_MEDIC.HPstLHighChance = 20
ARCH_MEDIC.HPstLLowChance = 30
#endregion HOTSPOTS - Medic

#region ATTRIBUTES - Guardian
ARCH_GUARDIAN = Archetype(4,"Guardian")
ARCH_GUARDIAN.heightRange = [82, 90]
ARCH_GUARDIAN.validTeams = ["41","42","43","44","45","46","47","48","49"]
ARCH_GUARDIAN.jerseyTeamId = 3
ARCH_GUARDIAN.inGamePositionId = 3
ARCH_GUARDIAN.inGamePositionString = "PF"
ARCH_GUARDIAN.inGameSecondaryPositionId = 2
ARCH_GUARDIAN.inGameSecondaryPositionString = "SF"

ARCH_GUARDIAN.primaryAttributes = DEFENSIVE_ATTRIBUTES
ARCH_GUARDIAN.secondaryAttributes = OFFENSIVE_ATTRIBUTES
ARCH_GUARDIAN.tertiaryAttributes = CONTROL_ATTRIBUTES

ARCH_GUARDIAN.accentedAttributes = ["SShtCls","SPstFdaway","SPstHook","SOLowPost","SShtInT","SDLowPost", "SStrength", "SBlock", "SOnBallD","SOffHDrib","SHands","SBallHndl","SBallSec","SSteal"]
ARCH_GUARDIAN.unaccentedAttributes = ['SLayUp', 'SShtMed', 'SSht3PT', 'SShtOfD', 'SConsis', 'SOReb', 'SDReb', 'SDAwar', 'SOAwar', 'SHustle', 'SPass', 'SSpeed', 'SQuick', 'SShtIns', 'SDunk', 'SStdDunk', 'SVertical', 'SShtFT', 'SStamina', 'SDurab', 'SPOT']
ARCH_GUARDIAN.attributeImportance = ['SSht3PT', 'SDReb', 'SOReb', 'SOnBallD', 'SDAwar', 'SSpeed', 'SShtInT', 'SVertical', 'SBallHndl', 'SBallSec', 'SOAwar', 'SSteal', 'SHands', 'SQuick', 'SHustle', 'SDunk', 'SStdDunk', 'SLayUp', 'SShtMed', 'SShtOfD', 'SConsis', 'SPass', 'SOffHDrib', 'SShtIns', 'SShtCls', 'SStrength', 'SBlock', 'SDLowPost', 'SPstFdaway', 'SPstHook', 'SOLowPost']
ARCH_GUARDIAN.attributeRanges["SOffHDrib"] = [35, 50]
ARCH_GUARDIAN.attributeRanges["SHands"] = [35, 50]
ARCH_GUARDIAN.attributeRanges["SOAwar"] = [25, 35]
ARCH_GUARDIAN.attributeRanges["SBallHndl"] = [35, 50]
ARCH_GUARDIAN.attributeRanges["SBallSec"] = [35, 50]
ARCH_GUARDIAN.attributeRanges["SPass"] = [25, 45]
ARCH_GUARDIAN.attributeRanges["SSpeed"] = [25, 45]
ARCH_GUARDIAN.attributeRanges["SQuick"] = [25, 45]
ARCH_GUARDIAN.attributeRanges["SHustle"] = [25, 35]
ARCH_GUARDIAN.attributeRanges["SSteal"] = [25, 45]
ARCH_GUARDIAN.attributeRanges["SDLowPost"] = [80, 99]
ARCH_GUARDIAN.attributeRanges["SStrength"] = [85, 99]
ARCH_GUARDIAN.attributeRanges["SBlock"] = [80, 99]
ARCH_GUARDIAN.attributeRanges["SOnBallD"] = [80, 99]
ARCH_GUARDIAN.attributeRanges["SOReb"] = [65, 85]
ARCH_GUARDIAN.attributeRanges["SDReb"] = [65, 85]
ARCH_GUARDIAN.attributeRanges["SDAwar"] = [70, 99]
ARCH_GUARDIAN.attributeRanges["SShtIns"] = [80, 99]
ARCH_GUARDIAN.attributeRanges["SDunk"] = [50, 70]
ARCH_GUARDIAN.attributeRanges["SStdDunk"] = [85, 99]
ARCH_GUARDIAN.attributeRanges["SVertical"] = [25, 40]
ARCH_GUARDIAN.attributeRanges["SShtFT"] = [80, 99]
ARCH_GUARDIAN.attributeRanges["SStamina"] = [50, 85]
ARCH_GUARDIAN.attributeRanges["SDurab"] = [50, 85]
ARCH_GUARDIAN.attributeRanges["SPOT"] = [25, 99]
ARCH_GUARDIAN.attributeRanges["SShtCls"] = [65, 75]
ARCH_GUARDIAN.attributeRanges["SLayUp"] = [50, 70]
ARCH_GUARDIAN.attributeRanges["SPstFdaway"] = [50, 70]
ARCH_GUARDIAN.attributeRanges["SPstHook"] = [50, 70]
ARCH_GUARDIAN.attributeRanges["SOLowPost"] = [50, 70]
ARCH_GUARDIAN.attributeRanges["SShtMed"] = [40, 60]
ARCH_GUARDIAN.attributeRanges["SSht3PT"] = [55, 65]
ARCH_GUARDIAN.attributeRanges["SShtInT"] = [50, 70]
ARCH_GUARDIAN.attributeRanges["SShtOfD"] = [40, 60]
ARCH_GUARDIAN.attributeRanges["SConsis"] = [40, 60]

# "Posterizer", "Finisher", "Deadeye","Brick Wall", "Lockdown Defender", "Interceptor","Active Hands", "Eraser", "Hustle Points","Scrapper"
ARCH_GUARDIAN.availableSkillCards = ["1", "3", "7","15", "16", "18","20", "21", "24","25"]
#endregion ATTRIBUTES - Guardian
#region TENDENCIES - Guardian
ARCH_GUARDIAN.t_ShotTnd = [25,75]
ARCH_GUARDIAN.t_InsideShot = [25,75]
ARCH_GUARDIAN.t_CloseShot = [25,75]
ARCH_GUARDIAN.t_MidShot = [25,75]
ARCH_GUARDIAN.t_ShotThreePt = [25,75]
ARCH_GUARDIAN.t_Putback = [60, 100]

ARCH_GUARDIAN.t_DriveLane = [0,100]
ARCH_GUARDIAN.t_DriveRight = [0,100]

ARCH_GUARDIAN.t_PullUp = [0,100]

ARCH_GUARDIAN.t_PumpFake = [0,100]
ARCH_GUARDIAN.t_TripleThreat = [0,100]
ARCH_GUARDIAN.t_NoTripleThreat = [0,100]
ARCH_GUARDIAN.t_TripleThreatShot = [0,100]

ARCH_GUARDIAN.t_Sizeup = [0,100]
ARCH_GUARDIAN.t_Hesitation = [0,100]
ARCH_GUARDIAN.t_StraightDribble = [0,100]

ARCH_GUARDIAN.t_Crossover = [0,50]
ARCH_GUARDIAN.t_Spin = [0,50]
ARCH_GUARDIAN.t_Stepback = [0,50]
ARCH_GUARDIAN.t_Halfspin = [0,50]
ARCH_GUARDIAN.t_DoubleCrossover = [0,50]
ARCH_GUARDIAN.t_BehindBack = [0,50]
ARCH_GUARDIAN.t_HesitationCross = [0,50]
ARCH_GUARDIAN.t_InNOut = [0,50]
ARCH_GUARDIAN.t_SimpleDrive = [0,50]

ARCH_GUARDIAN.t_Attack = [0,100]
ARCH_GUARDIAN.t_PassOut = [0,70]

ARCH_GUARDIAN.t_Hopstep = [0,100]
ARCH_GUARDIAN.t_SpinLayup = [0,100]
ARCH_GUARDIAN.t_Eurostep = [0,100]

ARCH_GUARDIAN.t_Runner = [0,100]
ARCH_GUARDIAN.t_Fadeaway = [0,100]
ARCH_GUARDIAN.t_StepbackJumper = [0, 100]
ARCH_GUARDIAN.t_SpinJumper = [0, 100]

ARCH_GUARDIAN.t_Dunk = [0,100] # Uses Dunk Stat instead

ARCH_GUARDIAN.t_Crash = [0,100]
ARCH_GUARDIAN.t_AlleyOop = [0, 40]
ARCH_GUARDIAN.t_DrawFoul = [0, 100]
ARCH_GUARDIAN.t_UseGlass = [0, 100]
ARCH_GUARDIAN.t_StepThrough = [0, 100]

ARCH_GUARDIAN.t_Touches = [0,100]
ARCH_GUARDIAN.t_UsePick = [0,10]
ARCH_GUARDIAN.t_SetPick = [85,100]
ARCH_GUARDIAN.t_Isolation = [20,45]
ARCH_GUARDIAN.t_UseOffBallScreen = [0,10]
ARCH_GUARDIAN.t_SetOffBallScreen = [85,100]
ARCH_GUARDIAN.t_PostUp = [75,100]
ARCH_GUARDIAN.t_SpotUp = [25,55]
ARCH_GUARDIAN.t_GiveNGo = [0, 100]

ARCH_GUARDIAN.t_PostSpin = [0,100]
ARCH_GUARDIAN.t_DropStep = [0,100]
ARCH_GUARDIAN.t_Shimmy = [0,100]
ARCH_GUARDIAN.t_FaceUp = [0,100]
ARCH_GUARDIAN.t_LeavePost = [0,100]
ARCH_GUARDIAN.t_BackDown = [0,100]
ARCH_GUARDIAN.t_AggressiveBackDown = [0,100]
ARCH_GUARDIAN.t_PostShot = [0,100]
ARCH_GUARDIAN.t_PostHook = [0,100]
ARCH_GUARDIAN.t_PostFade = [0,100]
ARCH_GUARDIAN.t_PostDrive = [0,100]
ARCH_GUARDIAN.t_HopShot = [0,100]

ARCH_GUARDIAN.t_FlashyPass = [0,25]
ARCH_GUARDIAN.t_ThrowAlleyOop = [0, 25]

ARCH_GUARDIAN.t_PlayPassLane = [0,100]
ARCH_GUARDIAN.t_TakeCharge = [25,100]
ARCH_GUARDIAN.t_OnBallSteal = [75,100]
ARCH_GUARDIAN.t_Contest = [0,100]
ARCH_GUARDIAN.t_CommitFoul = [0,100]
ARCH_GUARDIAN.t_HardFoul = [0,100]
#endregion TENDENCIES - Guardian
#region HOTSPOTS - Guardian
# Isolation
ARCH_GUARDIAN.HIso3PLftChance = 10
ARCH_GUARDIAN.HIso3PCtrChance = 10
ARCH_GUARDIAN.HIso3PRgtChance = 10
ARCH_GUARDIAN.HIsoHPLftChance = 25
ARCH_GUARDIAN.HIsoHPCtrChance = 25
ARCH_GUARDIAN.HIsoHPRgtChance = 25

# Pick and Roll
ARCH_GUARDIAN.HP_rLCrnrChance = 5
ARCH_GUARDIAN.HP_rLWingChance = 20
ARCH_GUARDIAN.HP_rTopOAChance = 20
ARCH_GUARDIAN.HP_rRWingChance = 20
ARCH_GUARDIAN.HP_rRCrnrChance = 5

# Spot Up
ARCH_GUARDIAN.HSpt3PLCrChance = 8
ARCH_GUARDIAN.HSpt3PLWgChance = 8
ARCH_GUARDIAN.HSpt3PTopChance = 8
ARCH_GUARDIAN.HSpt3PRWgChance = 8
ARCH_GUARDIAN.HSpt3PRCrChance = 8
ARCH_GUARDIAN.HSptMdLBlChance = 20
ARCH_GUARDIAN.HSptMdLWgChance = 20
ARCH_GUARDIAN.HSptMdCtrChance = 20
ARCH_GUARDIAN.HSptMdRWgChance = 20
ARCH_GUARDIAN.HSptMdRBlChance = 20

# Post
ARCH_GUARDIAN.HPstRHighChance = 40
ARCH_GUARDIAN.HPstRLowChance = 20
ARCH_GUARDIAN.HPstLHighChance = 40
ARCH_GUARDIAN.HPstLLowChance = 20
#endregion HOTSPOTS - Guardian

#region ATTRIBUTES - Engineer
ARCH_ENGINEER = Archetype(5,"Engineer")
ARCH_ENGINEER.heightRange = [69,77]
ARCH_ENGINEER.validTeams = ["51","52","53","54","55","56","57","58","59"]
ARCH_ENGINEER.jerseyTeamId = 4
ARCH_ENGINEER.inGamePositionId = 0
ARCH_ENGINEER.inGamePositionString = "PG"
ARCH_ENGINEER.inGameSecondaryPositionId = 4
ARCH_ENGINEER.inGameSecondaryPositionString = "C"

ARCH_ENGINEER.primaryAttributes = CONTROL_ATTRIBUTES
ARCH_ENGINEER.secondaryAttributes = DEFENSIVE_ATTRIBUTES
ARCH_ENGINEER.tertiaryAttributes = OFFENSIVE_ATTRIBUTES

ARCH_ENGINEER.isPlayInitiator = 1

ARCH_ENGINEER.accentedAttributes = ["SLayUp","SShtMed","SSht3PT","SShtOfD","SConsis","SOReb", "SDReb", "SDAwar", "SOffHDrib", "SHands", "SBallSec", "SBallHndl", "SSteal"]
ARCH_ENGINEER.unaccentedAttributes = ['SShtCls', 'SPstFdaway', 'SPstHook', 'SOLowPost', 'SShtInT', 'SDLowPost', 'SStrength', 'SBlock', 'SOnBallD', 'SOAwar', 'SHustle', 'SPass', 'SSpeed', 'SQuick', 'SShtIns', 'SDunk', 'SStdDunk', 'SVertical', 'SShtFT', 'SStamina', 'SDurab', 'SPOT']
ARCH_ENGINEER.attributeImportance = ['SBallSec', 'SSpeed', 'SSteal', 'SDAwar', 'SDReb', 'SOReb', 'SSht3PT', 'SVertical', 'SOAwar', 'SBallHndl', 'SQuick', 'SHustle', 'SHands', 'SPass', 'SOffHDrib', 'SOnBallD', 'SStrength', 'SBlock', 'SShtInT', 'SShtOfD', 'SConsis', 'SLayUp', 'SDunk', 'SStdDunk', 'SShtIns', 'SShtMed', 'SPstFdaway', 'SPstHook', 'SShtCls', 'SDLowPost', 'SOLowPost']
ARCH_ENGINEER.attributeRanges["SOffHDrib"] = [85, 99]
ARCH_ENGINEER.attributeRanges["SHands"] = [85, 99]
ARCH_ENGINEER.attributeRanges["SOAwar"] = [70, 90]
ARCH_ENGINEER.attributeRanges["SBallHndl"] = [85, 99]
ARCH_ENGINEER.attributeRanges["SBallSec"] = [85, 99]
ARCH_ENGINEER.attributeRanges["SPass"] = [70, 90]
ARCH_ENGINEER.attributeRanges["SSpeed"] = [65, 85]
ARCH_ENGINEER.attributeRanges["SQuick"] = [65, 85]
ARCH_ENGINEER.attributeRanges["SHustle"] = [70, 90]
ARCH_ENGINEER.attributeRanges["SSteal"] = [80, 99]
ARCH_ENGINEER.attributeRanges["SDLowPost"] = [40, 60]
ARCH_ENGINEER.attributeRanges["SStrength"] = [40, 60]
ARCH_ENGINEER.attributeRanges["SBlock"] = [40, 60]
ARCH_ENGINEER.attributeRanges["SOnBallD"] = [40, 60]
ARCH_ENGINEER.attributeRanges["SOReb"] = [55, 75]
ARCH_ENGINEER.attributeRanges["SDReb"] = [55, 75]
ARCH_ENGINEER.attributeRanges["SDAwar"] = [50, 70]
ARCH_ENGINEER.attributeRanges["SShtIns"] = [60, 65]
ARCH_ENGINEER.attributeRanges["SDunk"] = [25, 40]
ARCH_ENGINEER.attributeRanges["SStdDunk"] = [30, 50]
ARCH_ENGINEER.attributeRanges["SVertical"] = [70, 90]
ARCH_ENGINEER.attributeRanges["SShtFT"] = [80, 99]
ARCH_ENGINEER.attributeRanges["SStamina"] = [50, 85]
ARCH_ENGINEER.attributeRanges["SDurab"] = [50, 85]
ARCH_ENGINEER.attributeRanges["SPOT"] = [25, 99]
ARCH_ENGINEER.attributeRanges["SShtCls"] = [55, 65]
ARCH_ENGINEER.attributeRanges["SLayUp"] = [35, 50]
ARCH_ENGINEER.attributeRanges["SPstFdaway"] = [25, 40]
ARCH_ENGINEER.attributeRanges["SPstHook"] = [25, 40]
ARCH_ENGINEER.attributeRanges["SOLowPost"] = [25, 40]
ARCH_ENGINEER.attributeRanges["SShtMed"] = [35, 50]
ARCH_ENGINEER.attributeRanges["SSht3PT"] = [30, 40]
ARCH_ENGINEER.attributeRanges["SShtInT"] = [25, 40]
ARCH_ENGINEER.attributeRanges["SShtOfD"] = [35, 50]
ARCH_ENGINEER.attributeRanges["SConsis"] = [35, 50]

# "Shot Creator", "Ankle Breaker", "Post Playmaker","Dimer", "Break Starter", "Alley-ooper","Antifreeze", "Microwave", "Heat Retention","Floor General", "Defensive Anchor"
ARCH_ENGINEER.availableSkillCards = ["6", "10", "11","12", "13", "14","26", "27", "28","30", "31"]
#endregion ATTRIBUTES - Engineer
#region TENDENCIES - Engineer
ARCH_ENGINEER.t_ShotTnd = [0,30]
ARCH_ENGINEER.t_InsideShot = [0,50]
ARCH_ENGINEER.t_CloseShot = [0,50]
ARCH_ENGINEER.t_MidShot = [0,20]
ARCH_ENGINEER.t_ShotThreePt = [0,5]
ARCH_ENGINEER.t_Putback = [0, 60]

ARCH_ENGINEER.t_DriveLane = [0,100]
ARCH_ENGINEER.t_DriveRight = [0,100]

ARCH_ENGINEER.t_PullUp = [0,50]

ARCH_ENGINEER.t_PumpFake = [0,70]
ARCH_ENGINEER.t_TripleThreat = [0,100]
ARCH_ENGINEER.t_NoTripleThreat = [50,100]
ARCH_ENGINEER.t_TripleThreatShot = [0,5]

ARCH_ENGINEER.t_Sizeup = [50,100]
ARCH_ENGINEER.t_Hesitation = [0,100]
ARCH_ENGINEER.t_StraightDribble = [0,50]

ARCH_ENGINEER.t_Crossover = [60,100]
ARCH_ENGINEER.t_Spin = [60,100]
ARCH_ENGINEER.t_Stepback = [60,100]
ARCH_ENGINEER.t_Halfspin = [60,100]
ARCH_ENGINEER.t_DoubleCrossover = [60,100]
ARCH_ENGINEER.t_BehindBack = [60,100]
ARCH_ENGINEER.t_HesitationCross = [60,100]
ARCH_ENGINEER.t_InNOut = [60,100]
ARCH_ENGINEER.t_SimpleDrive = [60,100]

ARCH_ENGINEER.t_Attack = [0,25]
ARCH_ENGINEER.t_PassOut = [70,100]

ARCH_ENGINEER.t_Hopstep = [0,100]
ARCH_ENGINEER.t_SpinLayup = [0,100]
ARCH_ENGINEER.t_Eurostep = [0,100]

ARCH_ENGINEER.t_Runner = [0,100]
ARCH_ENGINEER.t_Fadeaway = [0,100]
ARCH_ENGINEER.t_StepbackJumper = [0, 100]
ARCH_ENGINEER.t_SpinJumper = [0, 100]

ARCH_ENGINEER.t_Dunk = [0,100] # Uses Dunk Stat instead

ARCH_ENGINEER.t_Crash = [0,100]
ARCH_ENGINEER.t_AlleyOop = [60, 100]
ARCH_ENGINEER.t_DrawFoul = [0, 100]
ARCH_ENGINEER.t_UseGlass = [0, 100]
ARCH_ENGINEER.t_StepThrough = [0, 100]

ARCH_ENGINEER.t_Touches = [0,100]
ARCH_ENGINEER.t_UsePick = [60,100]
ARCH_ENGINEER.t_SetPick = [60,100]
ARCH_ENGINEER.t_Isolation = [0,10]
ARCH_ENGINEER.t_UseOffBallScreen = [60,100]
ARCH_ENGINEER.t_SetOffBallScreen = [60,100]
ARCH_ENGINEER.t_PostUp = [20,55]
ARCH_ENGINEER.t_SpotUp = [0,10]
ARCH_ENGINEER.t_GiveNGo = [0, 100]

ARCH_ENGINEER.t_PostSpin = [0,100]
ARCH_ENGINEER.t_DropStep = [0,100]
ARCH_ENGINEER.t_Shimmy = [0,100]
ARCH_ENGINEER.t_FaceUp = [0,100]
ARCH_ENGINEER.t_LeavePost = [0,100]
ARCH_ENGINEER.t_BackDown = [0,100]
ARCH_ENGINEER.t_AggressiveBackDown = [0,100]
ARCH_ENGINEER.t_PostShot = [0,100]
ARCH_ENGINEER.t_PostHook = [0,100]
ARCH_ENGINEER.t_PostFade = [0,100]
ARCH_ENGINEER.t_PostDrive = [0,100]
ARCH_ENGINEER.t_HopShot = [0,100]

ARCH_ENGINEER.t_FlashyPass = [40,100]
ARCH_ENGINEER.t_ThrowAlleyOop = [40, 100]

ARCH_ENGINEER.t_PlayPassLane = [0,100]
ARCH_ENGINEER.t_TakeCharge = [0,100]
ARCH_ENGINEER.t_OnBallSteal = [0,100]
ARCH_ENGINEER.t_Contest = [30,80]
ARCH_ENGINEER.t_CommitFoul = [0,100]
ARCH_ENGINEER.t_HardFoul = [0,100]
#endregion TENDENCIES - Engineer
#region HOTSPOTS - Engineer
# Isolation
ARCH_ENGINEER.HIso3PLftChance = 2
ARCH_ENGINEER.HIso3PCtrChance = 2
ARCH_ENGINEER.HIso3PRgtChance = 2
ARCH_ENGINEER.HIsoHPLftChance = 30
ARCH_ENGINEER.HIsoHPCtrChance = 30
ARCH_ENGINEER.HIsoHPRgtChance = 30

# Pick and Roll
ARCH_ENGINEER.HP_rLCrnrChance = 5
ARCH_ENGINEER.HP_rLWingChance = 20
ARCH_ENGINEER.HP_rTopOAChance = 20
ARCH_ENGINEER.HP_rRWingChance = 20
ARCH_ENGINEER.HP_rRCrnrChance = 5

# Spot Up
ARCH_ENGINEER.HSpt3PLCrChance = 1
ARCH_ENGINEER.HSpt3PLWgChance = 1
ARCH_ENGINEER.HSpt3PTopChance = 1
ARCH_ENGINEER.HSpt3PRWgChance = 1
ARCH_ENGINEER.HSpt3PRCrChance = 1
ARCH_ENGINEER.HSptMdLBlChance = 32
ARCH_ENGINEER.HSptMdLWgChance = 5
ARCH_ENGINEER.HSptMdCtrChance = 5
ARCH_ENGINEER.HSptMdRWgChance = 5
ARCH_ENGINEER.HSptMdRBlChance = 32

# Post
ARCH_ENGINEER.HPstRHighChance = 20
ARCH_ENGINEER.HPstRLowChance = 30
ARCH_ENGINEER.HPstLHighChance = 20
ARCH_ENGINEER.HPstLLowChance = 30
#endregion HOTSPOTS - Engineer

#region ATTRIBUTES - Director
ARCH_DIRECTOR = Archetype(6,"Director")
ARCH_DIRECTOR.heightRange = [63,72]
ARCH_DIRECTOR.validTeams = ["61","62","63","64","65","66","67","68","69"]
ARCH_DIRECTOR.jerseyTeamId = 5
ARCH_DIRECTOR.inGamePositionId = 0
ARCH_DIRECTOR.inGamePositionString = "PG"
ARCH_DIRECTOR.inGameSecondaryPositionId = 1
ARCH_DIRECTOR.inGameSecondaryPositionString = "SG"

ARCH_DIRECTOR.primaryAttributes = CONTROL_ATTRIBUTES
ARCH_DIRECTOR.secondaryAttributes = OFFENSIVE_ATTRIBUTES
ARCH_DIRECTOR.tertiaryAttributes = DEFENSIVE_ATTRIBUTES

ARCH_DIRECTOR.isPlayInitiator = 1

ARCH_DIRECTOR.accentedAttributes = ["SLayUp", "SShtMed", "SSht3PT", "SShtOfD", "SConsis", "SOAwar", "SPass", "SSpeed", "SHustle", "SQuick","SOReb","SDReb","SDAwar"]
ARCH_DIRECTOR.unaccentedAttributes = ['SShtCls', 'SPstFdaway', 'SPstHook', 'SOLowPost', 'SShtInT', 'SDLowPost', 'SStrength', 'SBlock', 'SOnBallD', 'SOffHDrib', 'SHands', 'SBallHndl', 'SBallSec', 'SSteal', 'SShtIns', 'SDunk', 'SStdDunk', 'SVertical', 'SShtFT', 'SStamina', 'SDurab', 'SPOT']
ARCH_DIRECTOR.attributeImportance = ['SSht3PT', 'SSpeed', 'SBallSec', 'SBallHndl', 'SQuick', 'SSteal', 'SVertical', 'SShtOfD', 'SConsis', 'SHustle', 'SOffHDrib', 'SHands', 'SPass', 'SShtInT', 'SDAwar', 'SOReb', 'SDReb', 'SOAwar', 'SDunk', 'SStdDunk', 'SLayUp', 'SShtCls', 'SOnBallD', 'SStrength', 'SBlock', 'SShtMed', 'SPstFdaway', 'SPstHook', 'SOLowPost', 'SShtIns', 'SDLowPost']
ARCH_DIRECTOR.attributeRanges["SOffHDrib"] = [70, 90]
ARCH_DIRECTOR.attributeRanges["SHands"] = [75, 95]
ARCH_DIRECTOR.attributeRanges["SOAwar"] = [80, 99]
ARCH_DIRECTOR.attributeRanges["SBallHndl"] = [65, 85]
ARCH_DIRECTOR.attributeRanges["SBallSec"] = [65, 85]
ARCH_DIRECTOR.attributeRanges["SPass"] = [85, 99]
ARCH_DIRECTOR.attributeRanges["SSpeed"] = [80, 99]
ARCH_DIRECTOR.attributeRanges["SQuick"] = [80, 99]
ARCH_DIRECTOR.attributeRanges["SHustle"] = [80, 99]
ARCH_DIRECTOR.attributeRanges["SSteal"] = [65, 85]
ARCH_DIRECTOR.attributeRanges["SDLowPost"] = [25, 40]
ARCH_DIRECTOR.attributeRanges["SStrength"] = [25, 40]
ARCH_DIRECTOR.attributeRanges["SBlock"] = [25, 40]
ARCH_DIRECTOR.attributeRanges["SOnBallD"] = [25, 40]
ARCH_DIRECTOR.attributeRanges["SOReb"] = [30, 45]
ARCH_DIRECTOR.attributeRanges["SDReb"] = [30, 45]
ARCH_DIRECTOR.attributeRanges["SDAwar"] = [35, 50]
ARCH_DIRECTOR.attributeRanges["SShtIns"] = [70, 90]
ARCH_DIRECTOR.attributeRanges["SDunk"] = [70, 90]
ARCH_DIRECTOR.attributeRanges["SStdDunk"] = [50, 70]
ARCH_DIRECTOR.attributeRanges["SVertical"] = [50, 70]
ARCH_DIRECTOR.attributeRanges["SShtFT"] = [80, 99]
ARCH_DIRECTOR.attributeRanges["SStamina"] = [50, 85]
ARCH_DIRECTOR.attributeRanges["SDurab"] = [50, 85]
ARCH_DIRECTOR.attributeRanges["SPOT"] = [25, 99]
ARCH_DIRECTOR.attributeRanges["SShtCls"] = [70, 80]
ARCH_DIRECTOR.attributeRanges["SLayUp"] = [40, 60]
ARCH_DIRECTOR.attributeRanges["SPstFdaway"] = [40, 60]
ARCH_DIRECTOR.attributeRanges["SPstHook"] = [40, 60]
ARCH_DIRECTOR.attributeRanges["SOLowPost"] = [40, 60]
ARCH_DIRECTOR.attributeRanges["SShtMed"] = [50, 70]
ARCH_DIRECTOR.attributeRanges["SSht3PT"] = [58, 68]
ARCH_DIRECTOR.attributeRanges["SShtInT"] = [40, 60]
ARCH_DIRECTOR.attributeRanges["SShtOfD"] = [50, 70]
ARCH_DIRECTOR.attributeRanges["SConsis"] = [50, 70]

# "Highlight Film", "Finisher", "Acrobat","Shot Creator", "Post Proficiency", "Ankle Breaker","Post Playmaker", "Dimer", "Break Starter","Alley-ooper", "Antifreeze", "Microwave","Heat Retention", "Floor General"
ARCH_DIRECTOR.availableSkillCards = ["2", "3", "4","6", "9", "10","11", "12", "13","14", "26", "27","28", "30"]
#endregion ATTRIBUTES - Director
#region TENDENCIES - Director
ARCH_DIRECTOR.t_ShotTnd = [25,85]
ARCH_DIRECTOR.t_InsideShot = [25,85]
ARCH_DIRECTOR.t_CloseShot = [25,85]
ARCH_DIRECTOR.t_MidShot = [25,85]
ARCH_DIRECTOR.t_ShotThreePt = [25,85]
ARCH_DIRECTOR.t_Putback = [0, 60]

ARCH_DIRECTOR.t_DriveLane = [40,100]
ARCH_DIRECTOR.t_DriveRight = [0,100]

ARCH_DIRECTOR.t_PullUp = [0,100]

ARCH_DIRECTOR.t_PumpFake = [0,100]
ARCH_DIRECTOR.t_TripleThreat = [0,100]
ARCH_DIRECTOR.t_NoTripleThreat = [0,100]
ARCH_DIRECTOR.t_TripleThreatShot = [0,100]

ARCH_DIRECTOR.t_Sizeup = [50,100]
ARCH_DIRECTOR.t_Hesitation = [0,100]
ARCH_DIRECTOR.t_StraightDribble = [0,50]

ARCH_DIRECTOR.t_Crossover = [60,100]
ARCH_DIRECTOR.t_Spin = [60,100]
ARCH_DIRECTOR.t_Stepback = [60,100]
ARCH_DIRECTOR.t_Halfspin = [60,100]
ARCH_DIRECTOR.t_DoubleCrossover = [60,100]
ARCH_DIRECTOR.t_BehindBack = [60,100]
ARCH_DIRECTOR.t_HesitationCross = [60,100]
ARCH_DIRECTOR.t_InNOut = [60,100]
ARCH_DIRECTOR.t_SimpleDrive = [60,100]

ARCH_DIRECTOR.t_Attack = [50,100]
ARCH_DIRECTOR.t_PassOut = [50,100]

ARCH_DIRECTOR.t_Hopstep = [0,100]
ARCH_DIRECTOR.t_SpinLayup = [0,100]
ARCH_DIRECTOR.t_Eurostep = [0,100]

ARCH_DIRECTOR.t_Runner = [0,100]
ARCH_DIRECTOR.t_Fadeaway = [0,100]
ARCH_DIRECTOR.t_StepbackJumper = [0, 100]
ARCH_DIRECTOR.t_SpinJumper = [0, 100]

ARCH_DIRECTOR.t_Dunk = [0,100] # Uses Dunk Stat instead

ARCH_DIRECTOR.t_Crash = [0,100]
ARCH_DIRECTOR.t_AlleyOop = [60, 100]
ARCH_DIRECTOR.t_DrawFoul = [0, 100]
ARCH_DIRECTOR.t_UseGlass = [0, 100]
ARCH_DIRECTOR.t_StepThrough = [0, 100]

ARCH_DIRECTOR.t_Touches = [0,100]
ARCH_DIRECTOR.t_UsePick = [50,90]
ARCH_DIRECTOR.t_SetPick = [10,40]
ARCH_DIRECTOR.t_Isolation = [50,100]
ARCH_DIRECTOR.t_UseOffBallScreen = [50,90]
ARCH_DIRECTOR.t_SetOffBallScreen = [10,40]
ARCH_DIRECTOR.t_PostUp = [0,30]
ARCH_DIRECTOR.t_SpotUp = [25,85]
ARCH_DIRECTOR.t_GiveNGo = [0, 100]

ARCH_DIRECTOR.t_PostSpin = [0,100]
ARCH_DIRECTOR.t_DropStep = [0,100]
ARCH_DIRECTOR.t_Shimmy = [0,100]
ARCH_DIRECTOR.t_FaceUp = [0,100]
ARCH_DIRECTOR.t_LeavePost = [0,100]
ARCH_DIRECTOR.t_BackDown = [0,100]
ARCH_DIRECTOR.t_AggressiveBackDown = [0,100]
ARCH_DIRECTOR.t_PostShot = [0,100]
ARCH_DIRECTOR.t_PostHook = [0,100]
ARCH_DIRECTOR.t_PostFade = [0,100]
ARCH_DIRECTOR.t_PostDrive = [0,100]
ARCH_DIRECTOR.t_HopShot = [0,100]

ARCH_DIRECTOR.t_FlashyPass = [40,100]
ARCH_DIRECTOR.t_ThrowAlleyOop = [40, 100]

ARCH_DIRECTOR.t_PlayPassLane = [0,100]
ARCH_DIRECTOR.t_TakeCharge = [0,100]
ARCH_DIRECTOR.t_OnBallSteal = [0,25]
ARCH_DIRECTOR.t_Contest = [0,100]
ARCH_DIRECTOR.t_CommitFoul = [0,100]
ARCH_DIRECTOR.t_HardFoul = [0,100]
#endregion TENDENCIES - Director
#region HOTSPOTS - Director
# Isolation
ARCH_DIRECTOR.HIso3PLftChance = 20
ARCH_DIRECTOR.HIso3PCtrChance = 20
ARCH_DIRECTOR.HIso3PRgtChance = 20
ARCH_DIRECTOR.HIsoHPLftChance = 20
ARCH_DIRECTOR.HIsoHPCtrChance = 20
ARCH_DIRECTOR.HIsoHPRgtChance = 20

# Pick and Roll
ARCH_DIRECTOR.HP_rLCrnrChance = 5
ARCH_DIRECTOR.HP_rLWingChance = 20
ARCH_DIRECTOR.HP_rTopOAChance = 20
ARCH_DIRECTOR.HP_rRWingChance = 20
ARCH_DIRECTOR.HP_rRCrnrChance = 5

# Spot Up
ARCH_DIRECTOR.HSpt3PLCrChance = 20
ARCH_DIRECTOR.HSpt3PLWgChance = 20
ARCH_DIRECTOR.HSpt3PTopChance = 20
ARCH_DIRECTOR.HSpt3PRWgChance = 20
ARCH_DIRECTOR.HSpt3PRCrChance = 20
ARCH_DIRECTOR.HSptMdLBlChance = 20
ARCH_DIRECTOR.HSptMdLWgChance = 20
ARCH_DIRECTOR.HSptMdCtrChance = 20
ARCH_DIRECTOR.HSptMdRWgChance = 20
ARCH_DIRECTOR.HSptMdRBlChance = 20

# Post
ARCH_DIRECTOR.HPstRHighChance = 20
ARCH_DIRECTOR.HPstRLowChance = 20
ARCH_DIRECTOR.HPstLHighChance = 20
ARCH_DIRECTOR.HPstLLowChance = 20
#endregion HOTSPOTS - Engineer

#region ATTRIBUTES - None
ARCH_NONE = Archetype(0,"None")
ARCH_NONE.heightRange = [63,90]
ARCH_NONE.validTeams = ["1","2","3","4","5","6","7","8","9"]
ARCH_NONE.jerseyTeamId = 0
ARCH_NONE.inGamePositionId = 1
ARCH_NONE.inGamePositionString = "SG"
ARCH_NONE.inGameSecondaryPositionId = 0
ARCH_NONE.inGameSecondaryPositionString = "PG"

ARCH_NONE.primaryAttributes = OFFENSIVE_ATTRIBUTES
ARCH_NONE.secondaryAttributes = DEFENSIVE_ATTRIBUTES
ARCH_NONE.tertiaryAttributes = CONTROL_ATTRIBUTES

ARCH_NONE.accentedAttributes = ["SLayUp", "SShtMed","SSht3PT","SShtOfD","SConsis","SOAwar","SPass","SSpeed","SHustle","SQuick","SDLowPost","SStrength","SBlock","SOnBallD"]
ARCH_NONE.unaccentedAttributes = ['SShtCls', 'SPstFdaway', 'SPstHook', 'SOLowPost', 'SShtInT', 'SOReb', 'SDReb', 'SDAwar', 'SOffHDrib', 'SHands', 'SBallHndl', 'SBallSec', 'SSteal', 'SShtIns', 'SDunk', 'SStdDunk', 'SVertical', 'SShtFT', 'SStamina', 'SDurab', 'SPOT']
ARCH_NONE.attributeImportance = ['SSht3PT', 'SDReb', 'SOReb', 'SOnBallD', 'SDAwar', 'SSpeed', 'SShtInT', 'SVertical', 'SBallHndl', 'SBallSec', 'SOAwar', 'SSteal', 'SHands', 'SQuick', 'SHustle', 'SDunk', 'SStdDunk', 'SLayUp', 'SShtMed', 'SShtOfD', 'SConsis', 'SPass', 'SOffHDrib', 'SShtIns', 'SShtCls', 'SStrength', 'SBlock', 'SDLowPost', 'SPstFdaway', 'SPstHook', 'SOLowPost']
ARCH_NONE.attributeRanges["SOffHDrib"] = [25, 99]
ARCH_NONE.attributeRanges["SHands"] = [25, 99]
ARCH_NONE.attributeRanges["SOAwar"] = [25, 99]
ARCH_NONE.attributeRanges["SBallHndl"] = [25, 99]
ARCH_NONE.attributeRanges["SBallSec"] = [25, 99]
ARCH_NONE.attributeRanges["SPass"] = [25, 99]
ARCH_NONE.attributeRanges["SSpeed"] = [25, 99]
ARCH_NONE.attributeRanges["SQuick"] = [25, 99]
ARCH_NONE.attributeRanges["SHustle"] = [25, 99]
ARCH_NONE.attributeRanges["SSteal"] = [25, 99]
ARCH_NONE.attributeRanges["SDLowPost"] = [25, 99]
ARCH_NONE.attributeRanges["SStrength"] = [25, 99]
ARCH_NONE.attributeRanges["SBlock"] = [25, 99]
ARCH_NONE.attributeRanges["SOnBallD"] = [25, 99]
ARCH_NONE.attributeRanges["SOReb"] = [25, 99]
ARCH_NONE.attributeRanges["SDReb"] = [25, 99]
ARCH_NONE.attributeRanges["SDAwar"] = [25, 99]
ARCH_NONE.attributeRanges["SShtIns"] = [60, 99]
ARCH_NONE.attributeRanges["SDunk"] = [25, 99]
ARCH_NONE.attributeRanges["SStdDunk"] = [25, 99]
ARCH_NONE.attributeRanges["SVertical"] = [25, 99]
ARCH_NONE.attributeRanges["SShtFT"] = [25, 99]
ARCH_NONE.attributeRanges["SStamina"] = [25, 99]
ARCH_NONE.attributeRanges["SDurab"] = [25, 99]
ARCH_NONE.attributeRanges["SPOT"] = [25, 99]
ARCH_NONE.attributeRanges["SShtCls"] = [25, 99]
ARCH_NONE.attributeRanges["SLayUp"] = [25, 99]
ARCH_NONE.attributeRanges["SPstFdaway"] = [25, 99]
ARCH_NONE.attributeRanges["SPstHook"] = [25, 99]
ARCH_NONE.attributeRanges["SOLowPost"] = [25, 99]
ARCH_NONE.attributeRanges["SShtMed"] = [50, 99]
ARCH_NONE.attributeRanges["SSht3PT"] = [25, 99]
ARCH_NONE.attributeRanges["SShtInT"] = [25, 99]
ARCH_NONE.attributeRanges["SShtOfD"] = [25, 99]
ARCH_NONE.attributeRanges["SConsis"] = [25, 99]


#"Posterizer","Finisher","Spot-up Shooter","Shot Creator", "Deadeye", "Corner Specialist","Post Proficiency", "Post Playmaker", "Dimer","Alley-ooper", "Antifreeze", "Microwave","Heat Retention"
ARCH_NONE.availableSkillCards = ["1","3","5","6", "7", "8","9", "11", "12","14", "26", "27","28"]
#endregion ATTRIBUTES - None
#region TENDENCIES - None
ARCH_NONE.t_ShotTnd = [0,100]
ARCH_NONE.t_InsideShot = [0,100]
ARCH_NONE.t_CloseShot = [0,100]
ARCH_NONE.t_MidShot = [0,100]
ARCH_NONE.t_ShotThreePt = [0,100]
ARCH_NONE.t_Putback = [0,100]

ARCH_NONE.t_DriveLane = [0,100]
ARCH_NONE.t_DriveRight = [0,100]

ARCH_NONE.t_PullUp = [0,100]

ARCH_NONE.t_PumpFake = [0,100]
ARCH_NONE.t_TripleThreat = [0,100]
ARCH_NONE.t_NoTripleThreat = [0,100]
ARCH_NONE.t_TripleThreatShot = [0,100]

ARCH_NONE.t_Sizeup = [0,100]
ARCH_NONE.t_Hesitation = [0,100]
ARCH_NONE.t_StraightDribble = [0,100]

ARCH_NONE.t_Crossover = [0,100]
ARCH_NONE.t_Spin = [0,100]
ARCH_NONE.t_Stepback = [0,100]
ARCH_NONE.t_Halfspin = [0,100]
ARCH_NONE.t_DoubleCrossover = [0,100]
ARCH_NONE.t_BehindBack = [0,100]
ARCH_NONE.t_HesitationCross = [0,100]
ARCH_NONE.t_InNOut = [0,100]
ARCH_NONE.t_SimpleDrive = [0,100]

ARCH_NONE.t_Attack = [0,100]
ARCH_NONE.t_PassOut = [0,100]

ARCH_NONE.t_Hopstep = [0,100]
ARCH_NONE.t_SpinLayup = [0,100]
ARCH_NONE.t_Eurostep = [0,100]

ARCH_NONE.t_Runner = [0,100]
ARCH_NONE.t_Fadeaway = [0,100]
ARCH_NONE.t_StepbackJumper = [0,100]
ARCH_NONE.t_SpinJumper = [0,100]

ARCH_NONE.t_Dunk = [0,100]

ARCH_NONE.t_Crash = [0,100]
ARCH_NONE.t_AlleyOop = [0,100]
ARCH_NONE.t_DrawFoul = [0,100]
ARCH_NONE.t_UseGlass = [0,100]
ARCH_NONE.t_StepThrough = [0,100]

ARCH_NONE.t_Touches = [0,100]
ARCH_NONE.t_UsePick = [0,100]
ARCH_NONE.t_SetPick = [0,100]
ARCH_NONE.t_Isolation = [0,100]
ARCH_NONE.t_UseOffBallScreen = [0,100]
ARCH_NONE.t_SetOffBallScreen = [0,100]
ARCH_NONE.t_PostUp = [0,100]
ARCH_NONE.t_SpotUp = [0,100]
ARCH_NONE.t_GiveNGo = [0,100]

ARCH_NONE.t_PostSpin = [0,100]
ARCH_NONE.t_DropStep = [0,100]
ARCH_NONE.t_Shimmy = [0,100]
ARCH_NONE.t_FaceUp = [0,100]
ARCH_NONE.t_LeavePost = [0,100]
ARCH_NONE.t_BackDown = [0,100]
ARCH_NONE.t_AggressiveBackDown = [0,100]
ARCH_NONE.t_PostShot = [0,100]
ARCH_NONE.t_PostHook = [0,100]
ARCH_NONE.t_PostFade = [0,100]
ARCH_NONE.t_PostDrive = [0,100]
ARCH_NONE.t_HopShot = [0,100]

ARCH_NONE.t_FlashyPass = [0,100]
ARCH_NONE.t_ThrowAlleyOop = [0,100]

ARCH_NONE.t_PlayPassLane = [0,100]
ARCH_NONE.t_TakeCharge = [0,100]
ARCH_NONE.t_OnBallSteal = [0,100]
ARCH_NONE.t_Contest = [0,100]
ARCH_NONE.t_CommitFoul = [0,100]
ARCH_NONE.t_HardFoul = [0,100]
#endregion TENDENCIES - None
#region HOTSPOTS - None
# Isolation
ARCH_NONE.HIso3PLftChance =  1
ARCH_NONE.HIso3PCtrChance =  1
ARCH_NONE.HIso3PRgtChance =  1
ARCH_NONE.HIsoHPLftChance = 1
ARCH_NONE.HIsoHPCtrChance = 1
ARCH_NONE.HIsoHPRgtChance = 1

# Pick and Roll
ARCH_NONE.HP_rLCrnrChance = 1
ARCH_NONE.HP_rLWingChance = 1
ARCH_NONE.HP_rTopOAChance = 1
ARCH_NONE.HP_rRWingChance = 1
ARCH_NONE.HP_rRCrnrChance = 1

# Spot Up
ARCH_NONE.HSpt3PLCrChance = 1
ARCH_NONE.HSpt3PLWgChance = 1
ARCH_NONE.HSpt3PTopChance = 1
ARCH_NONE.HSpt3PRWgChance = 1
ARCH_NONE.HSpt3PRCrChance = 1
ARCH_NONE.HSptMdLBlChance = 1
ARCH_NONE.HSptMdLWgChance = 1
ARCH_NONE.HSptMdCtrChance = 1
ARCH_NONE.HSptMdRWgChance = 1
ARCH_NONE.HSptMdRBlChance = 1

# Post
ARCH_NONE.HPstRHighChance = 1
ARCH_NONE.HPstRLowChance = 1
ARCH_NONE.HPstLHighChance = 1
ARCH_NONE.HPstLLowChance = 1
#endregion HOTSPOTS - None


possibleArchetypes = {"Director" : ARCH_DIRECTOR,
                      "Engineer" : ARCH_ENGINEER,
                      "Guardian" : ARCH_GUARDIAN,
                      "Medic" : ARCH_MEDIC,
                      "Slayer" : ARCH_SLAYER,
                      "Vigilante" : ARCH_VIGILANTE,
                      "None" : ARCH_NONE}


