import random
import BaseFunctions as b
import Archetypes
import math

SKILL_CARDS_DICT = {0 : "None",
                    1 : "Posterizer",
                    2 : "Highlight Film",
                    3 : "Finisher",
                    4 : "Acrobat",
                    5 : "Spot Up Shooter",
                    6 : "Shot Creator",
                    7 : "Deadeye",
                    8 : "Corner Specialist",
                    9 : "Post Proficiency",
                    10 : "Ankle Breaker",
                    11 : "Post Playmaker",
                    12 : "Dimer",
                    13 : "Break Starter",
                    14 : "Alleyooper",
                    15 : "Brick Wall",
                    16 : "Lockdown Defender",
                    17 : "Charge Card",
                    18 : "Interceptor",
                    19 : "Pickpocket",
                    20 : "Active Hands",
                    21 : "Eraser",
                    22 : "Chasedown Artist",
                    23 : "Bruiser",
                    24 : "Hustle Points",
                    25 : "Scrapper",
                    26 : "Anti-Freeze",
                    27 : "Microwave",
                    28 : "Heat-Retention",
                    29 : "Closer",
                    30 : "Floor General",
                    31 : "Defensive Anchor",
                    32 : "Gatorade Prime Pack",
                    33 : "On Court Coach"}

def getBasicStatsValues():
    return {"Off Hand Dribbling": 0,
                                "Hands": 0,
                                "Offensive Awareness": 0,
                                "Ball Handling": 0,
                                "Ball Security": 0,
                                "Pass": 0,
                                "Speed": 0,
                                "Quickness": 0,
                                "Low Post Defense": 0,
                                "Strength": 0,
                                "Hustle": 0,
                                "Block": 0,
                                "Steal": 0,
                                "On Ball Defense": 0,
                                "Offensive Rebound": 0,
                                "Defensive Rebound": 0,
                                "Defensive Awareness": 0,
                                "Shot Inside": 0,
                                "Dunk": 0,
                                "Standing Dunk": 0,
                                "Vertical": 0,
                                "Free Throw": 0,
                                "Stamina": 0,
                                "Durability": 0,
                                "Potential": 0,
                                "Shot Close": 0,
                                "Layup": 0,
                                "Post Fadeaway": 0,
                                "Post Hook": 0,
                                "Low Post Offense": 0,
                                "Shot Medium": 0,
                                "Shot Three Point": 0,
                                "Shoot In Traffic": 0,
                                "Shoot Off Dribble": 0,
                                "Consistency": 0}
def getBasicStatsBonuses():
    return {"Off Hand Dribbling": 0,
                                 "Hands": 0,
                                 "Offensive Awareness": 0,
                                 "Ball Handling": 0,
                                 "Ball Security": 0,
                                 "Pass": 0,
                                 "Speed": 0,
                                 "Quickness": 0,
                                 "Low Post Defense": 0,
                                 "Strength": 0,
                                 "Hustle": 0,
                                 "Block": 0,
                                 "Steal": 0,
                                 "On Ball Defense": 0,
                                 "Offensive Rebound": 0,
                                 "Defensive Rebound": 0,
                                 "Defensive Awareness": 0,
                                 "Shot Inside": 0,
                                 "Dunk": 0,
                                 "Standing Dunk": 0,
                                 "Vertical": 0,
                                 "Free Throw": 0,
                                 "Stamina": 0,
                                 "Durability": 0,
                                 "Potential": 0,
                                 "Shot Close": 0,
                                 "Layup": 0,
                                 "Post Fadeaway": 0,
                                 "Post Hook": 0,
                                 "Low Post Offense": 0,
                                 "Shot Medium": 0,
                                 "Shot Three Point": 0,
                                 "Shoot In Traffic": 0,
                                 "Shoot Off Dribble": 0,
                                 "Consistency": 0}
def getBasicStatsRarity():
    return {"Off Hand Dribbling": "Common",
                                "Hands": "Common",
                                "Offensive Awareness": "Common",
                                "Ball Handling": "Common",
                                "Ball Security": "Common",
                                "Pass": "Common",
                                "Speed": "Common",
                                "Quickness": "Common",
                                "Low Post Defense": "Common",
                                "Strength": "Common",
                                "Hustle": "Common",
                                "Block": "Common",
                                "Steal": "Common",
                                "On Ball Defense": "Common",
                                "Offensive Rebound": "Common",
                                "Defensive Rebound": "Common",
                                "Defensive Awareness": "Common",
                                "Shot Inside": "Common",
                                "Dunk": "Common",
                                "Standing Dunk": "Common",
                                "Vertical": "Common",
                                "Free Throw": "Common",
                                "Stamina": "Common",
                                "Durability": "Common",
                                "Potential": "Common",
                                "Shot Close": "Common",
                                "Layup": "Common",
                                "Post Fadeaway": "Common",
                                "Post Hook": "Common",
                                "Low Post Offense": "Common",
                                "Shot Medium": "Common",
                                "Shot Three Point": "Common",
                                "Shoot In Traffic": "Common",
                                "Shoot Off Dribble": "Common",
                                "Consistency": "Common"}
def getBasicStatsLimits():
    return {"Off Hand Dribbling": [25, 99],
                       "Hands": [25, 99],
                       "Offensive Awareness": [25, 99],
                       "Ball Handling": [25, 99],
                       "Ball Security": [25, 99],
                       "Pass": [25, 99],
                       "Speed": [25, 99],
                       "Quickness": [25, 99],
                       "Low Post Defense": [25, 99],
                       "Strength": [25, 99],
                       "Hustle": [25, 99],
                       "Block": [25, 99],
                       "Steal": [25, 99],
                       "On Ball Defense": [25, 99],
                       "Offensive Rebound": [25, 99],
                       "Defensive Rebound": [25, 99],
                       "Defensive Awareness": [25, 99],
                       "Shot Inside": [25, 99],
                       "Dunk": [25, 99],
                       "Standing Dunk": [25, 99],
                       "Vertical": [25, 99],
                       "Free Throw": [25, 99],
                       "Stamina": [25, 99],
                       "Durability": [25, 99],
                       "Potential": [25, 99],
                       "Shot Close": [25, 99],
                       "Layup": [25, 99],
                       "Post Fadeaway": [25, 99],
                       "Post Hook": [25, 99],
                       "Low Post Offense": [25, 99],
                       "Shot Medium": [35, 99],
                       "Shot Three Point": [25, 99],
                       "Shoot In Traffic": [25, 99],
                       "Shoot Off Dribble": [25, 99],
                       "Consistency": [25, 99]}
def getEnchantmentTypeNames():
    return {1 : "Divine Strength",
                     2 : "Divine Wisdom",
                     3 : "Divine Grace",
                     4 : "Pestilent Cowardice",
                     5 : "Pestilent Ignorance",
                     6 : "Pestilent Indolence"}


PROFILE = b.readConfigValue("profileBaseFolder") + "\\" + b.readConfigValue("activeProfile")

class Player:

    # This init method has an optional archetype variable to specify the
    # specific archetype this PlayerGen will use. If no archetype is
    # specified, an archetype will be selected at random.
    def __init__(self, _archetype=False):
        if (_archetype == False):
            self.archetype = [Archetypes.ARCH_DIRECTOR,Archetypes.ARCH_ENGINEER,Archetypes.ARCH_GUARDIAN,Archetypes.ARCH_MEDIC,Archetypes.ARCH_SLAYER,Archetypes.ARCH_VIGILANTE][random.randrange(0, 6)]
        else:
            if(_archetype == "Slayer"):
                self.archetype = Archetypes.ARCH_SLAYER
            elif(_archetype == "Vigilante"):
                self.archetype = Archetypes.ARCH_VIGILANTE
            elif(_archetype == "Medic"):
                self.archetype = Archetypes.ARCH_MEDIC
            elif(_archetype == "Guardian"):
                self.archetype = Archetypes.ARCH_GUARDIAN
            elif(_archetype == "Engineer"):
                self.archetype = Archetypes.ARCH_ENGINEER
            elif(_archetype == "Director"):
                self.archetype = Archetypes.ARCH_DIRECTOR
            else:
                self.archetype = _archetype
        self.archetypeName = self.archetype.archetypeName
        self.arrayOfEnchantments = []
        self.__clothesType = "Jersey"
        self.playerRarity = None
        self.stats = None
        self.playStyle = 0
        self.tendencies = self.TendencyDict()
        self.hotspots = self.HotspotDict()
        self.hotzones = self.HotzoneDict()
        self.skillCards = []
        self.overwritePlayer = None
        self.firstName = ""
        self.lastName = ""
        self.signatureStats = None
        self.appearance = None

        self.emotion = 25
        self.hand = "Right"
        self.jerseyNumber = 1


        self.playType1 = None
        self.playType2 = None
        self.playType3 = None
        self.playType4 = None


    # Simple method to display the Player object
    def __str__(self):
        returnString = "===================================================\n"
        returnString += "===================================================\n"
        returnString += "===================================================\n"
        returnString += self.firstName.upper() + " " + self.lastName.upper() + "\n\n"
        returnString += self.archetypeName + " (" + str(self.playerRarity) + ")\n"
        returnString += "Height: " + self.getHeight() + "\n\n"

        if(self.signatureStats.isSpecialShot):
            returnString += "~ ~ ~UNIQUE SHOT~ ~ ~\n"
            returnString += "~" + self.signatureStats.specialShotName + "~\n\n"
            returnString += self.signatureStats.specialShotDesc + "\n\n"

        returnString += self.stats.returnOrderedString()
        returnString += "\n\n-------------------\n    SKILL CARDS  \n-------------------"
        counter = 0
        for i in self.skillCards:
            counter += 1
            returnString += "\nCard " + str(counter) + ": "
            returnString += SKILL_CARDS_DICT.get(i)

        returnString += "\n" + str(self.overwritePlayer) + "\n"

        returnString += "\n" + str(self.signatureStats)

        returnString += "\n===================================================\n"
        returnString += "===================================================\n"
        returnString += "===================================================\n\n\n"

        returnString += "Play Style: " + str(self.playStyle)


        return returnString

    # This method generates a special "Player Card" string, meant to
    # give a quick overview of a player's stats and help in player
    # creation.
    def getPlayerCard(self):
        cardString = ""
        WIDTH = 238

        if(str(self.playerRarity) == "Common"):
            rarityString = " C O M M O N "
            fillCharacter = "-"
        elif (str(self.playerRarity) == "Rare"):
            rarityString = " R A R E "
            fillCharacter = "="
        elif (str(self.playerRarity) == "Epic"):
            rarityString = " E P I C "
            fillCharacter = "~"
        elif (str(self.playerRarity) == "Legendary"):
            rarityString = " L E G E N D A R Y "
            fillCharacter = "*"
        elif (str(self.playerRarity) == "Godlike"):
            rarityString = " G O D L I K E "
            fillCharacter = "!"

        cardString += fillCharacter * WIDTH + "\n"
        cardString += rarityString.center(WIDTH,fillCharacter) + "\n"
        cardString += fillCharacter * WIDTH + "\n\n"

        cardString += self.getName().center(WIDTH) + "\n"
        cardString += self.archetypeName.upper().center(WIDTH) + "\n\n\n"


        SPACE_BETWEEN_TWO = 10
        TWO_ITEMS_ITEM_LENGTH = 25

        # All code pertaining to displaying blessings/curses information.
        if(True):
            allEnchantments = ""
            for enchantmentArray in self.arrayOfEnchantments:
                enchantmentString = getEnchantmentTypeNames().get(enchantmentArray[0])
                if(enchantmentArray[0] <= 3):
                    enchantmentString = "††† " + enchantmentString + " †††"
                else:
                    enchantmentString = "¿¿¿ " + enchantmentString + " ¿¿¿"

                enchantmentString = enchantmentString.center(WIDTH)

                allEnchantments += enchantmentString + "\n"


            cardString += "\n\n" + allEnchantments + "\n\n"


        # All code pertaining to displaying stats by archetype.
        if(True):
            SPACE_BETWEEN_TWO = 20
            TWO_ITEMS_ITEM_LENGTH = 40
            edgesBetweenTwo = (WIDTH - ((TWO_ITEMS_ITEM_LENGTH * 2) + SPACE_BETWEEN_TWO)) / 2
            twoItemTemplate = "{0:" + str(edgesBetweenTwo) + "s}{1:" + str(TWO_ITEMS_ITEM_LENGTH) + "s}{2:" + str(SPACE_BETWEEN_TWO) + "s}{3:" + str(TWO_ITEMS_ITEM_LENGTH) + "s}{4:" + str(edgesBetweenTwo) + "s}"

            SPACE_BETWEEN_FOUR = 10
            FOUR_ITEMS_ITEM_LENGTH = 20
            edgesBetweenFour = (WIDTH - ((3 * SPACE_BETWEEN_FOUR) + (FOUR_ITEMS_ITEM_LENGTH * 4))) / 2
            fourItemTemplate = "{0:" + str(edgesBetweenFour) + "s}{1:" + str(FOUR_ITEMS_ITEM_LENGTH) + "s}{2:" + str(
                SPACE_BETWEEN_FOUR) + "s}{3:" + str(FOUR_ITEMS_ITEM_LENGTH) + "s}{4:" + str(
                SPACE_BETWEEN_FOUR) + "s}{5:" + str(FOUR_ITEMS_ITEM_LENGTH) + "s}{6:" + str(
                SPACE_BETWEEN_FOUR) + "s}{7:" + str(FOUR_ITEMS_ITEM_LENGTH) + "s}{8:" + str(edgesBetweenFour) + "s}"

            SPACE_BETWEEN_FIVE = 8
            FIVE_ITEMS_ITEM_LENGTH = 20
            edgesBetweenFive = (WIDTH - ((4 * SPACE_BETWEEN_FIVE) + (FIVE_ITEMS_ITEM_LENGTH * 5))) /2
            fiveItemTemplate = "{0:" + str(edgesBetweenFive) + "s}{1:" + str(FIVE_ITEMS_ITEM_LENGTH) + "s}{2:" + str(
                SPACE_BETWEEN_FIVE) + "s}{3:" + str(FIVE_ITEMS_ITEM_LENGTH) + "s}{4:" + str(
                SPACE_BETWEEN_FIVE) + "s}{5:" + str(FIVE_ITEMS_ITEM_LENGTH) + "s}{6:" + str(
                SPACE_BETWEEN_FIVE) + "s}{7:" + str(FIVE_ITEMS_ITEM_LENGTH) + "s}{8:" + str(
                SPACE_BETWEEN_FIVE) + "s}{9:" + str(FIVE_ITEMS_ITEM_LENGTH) + "s}{10:" + str(edgesBetweenFive) + "s}"

            SPACE_BETWEEN_SIX = 7
            SIX_ITEMS_ITEM_LENGTH = 20
            edgesBetweenSix = (WIDTH - ((5 * SPACE_BETWEEN_SIX) + (SIX_ITEMS_ITEM_LENGTH * 6))) / 2
            sixItemTemplate = "{0:" + str(edgesBetweenSix) + "s}{1:" + str(SIX_ITEMS_ITEM_LENGTH) + "s}{2:" + str(
                SPACE_BETWEEN_SIX) + "s}{3:" + str(SIX_ITEMS_ITEM_LENGTH) + "s}{4:" + str(
                SPACE_BETWEEN_SIX) + "s}{5:" + str(SIX_ITEMS_ITEM_LENGTH) + "s}{6:" + str(
                SPACE_BETWEEN_SIX) + "s}{7:" + str(SIX_ITEMS_ITEM_LENGTH) + "s}{8:" + str(
                SPACE_BETWEEN_SIX) + "s}{9:" + str(SIX_ITEMS_ITEM_LENGTH) + "s}{10:" + str(
                SPACE_BETWEEN_SIX) + "s}{11:" + str(SIX_ITEMS_ITEM_LENGTH) + "s}{12:" + str(edgesBetweenSix) + "s}"


            if(self.archetypeName == "Slayer"):
                cardString += twoItemTemplate.format("", self.stats.getSingleStatString("Shot Three Point").center(TWO_ITEMS_ITEM_LENGTH," "), "",self.stats.getSingleStatString("Shot Medium").center(TWO_ITEMS_ITEM_LENGTH," "), "") + "\n\n"
                cardString += twoItemTemplate.format("", self.stats.getSingleStatString("Low Post Offense").center(TWO_ITEMS_ITEM_LENGTH," "), "", self.stats.getSingleStatString("Layup").center(TWO_ITEMS_ITEM_LENGTH," "), "") + "\n\n"
                cardString += twoItemTemplate.format("", self.stats.getSingleStatString("Post Fadeaway").center(TWO_ITEMS_ITEM_LENGTH," "), "", self.stats.getSingleStatString("Shot Close").center(TWO_ITEMS_ITEM_LENGTH," "), "") + "\n\n"
                cardString += twoItemTemplate.format("", self.stats.getSingleStatString("Shoot In Traffic").center(TWO_ITEMS_ITEM_LENGTH," "), "", self.stats.getSingleStatString("Shoot Off Dribble").center(TWO_ITEMS_ITEM_LENGTH," "), "") + "\n\n"
                cardString += twoItemTemplate.format("", self.stats.getSingleStatString("Post Hook").center(TWO_ITEMS_ITEM_LENGTH," "), "", self.stats.getSingleStatString("Consistency").center(TWO_ITEMS_ITEM_LENGTH," "), "") + "\n\n\n"

                cardString += twoItemTemplate.format("", self.stats.getSingleStatString("Off Hand Dribbling").center(TWO_ITEMS_ITEM_LENGTH," "), "",
                                                    self.stats.getSingleStatString("Hands").center(TWO_ITEMS_ITEM_LENGTH," "), "") + "\n"
                cardString += twoItemTemplate.format("", self.stats.getSingleStatString("Offensive Awareness").center(TWO_ITEMS_ITEM_LENGTH," "), "",
                                                    self.stats.getSingleStatString("Ball Handling").center(TWO_ITEMS_ITEM_LENGTH," "), "") + "\n"
                cardString += twoItemTemplate.format("", self.stats.getSingleStatString("Ball Security").center(TWO_ITEMS_ITEM_LENGTH," "), "",
                                                    self.stats.getSingleStatString("Pass").center(TWO_ITEMS_ITEM_LENGTH," "), "") + "\n"
                cardString += twoItemTemplate.format("", self.stats.getSingleStatString("Speed").center(TWO_ITEMS_ITEM_LENGTH," "), "",
                                                    self.stats.getSingleStatString("Quickness").center(TWO_ITEMS_ITEM_LENGTH," "), "") + "\n\n"

                cardString += twoItemTemplate.format("", self.stats.getSingleStatString("Shot Inside").center(TWO_ITEMS_ITEM_LENGTH," "), "",
                                                    self.stats.getSingleStatString("Dunk").center(TWO_ITEMS_ITEM_LENGTH," "), "") + "\n"
                cardString += twoItemTemplate.format("", self.stats.getSingleStatString("Standing Dunk").center(TWO_ITEMS_ITEM_LENGTH," "), "",
                                                    self.stats.getSingleStatString("Free Throw").center(TWO_ITEMS_ITEM_LENGTH," "), "") + "\n"
                cardString += twoItemTemplate.format("", self.stats.getSingleStatString("Vertical").center(TWO_ITEMS_ITEM_LENGTH," "), "",
                                                    self.stats.getSingleStatString("Stamina").center(TWO_ITEMS_ITEM_LENGTH," "), "") + "\n"
                cardString += twoItemTemplate.format("", self.stats.getSingleStatString("Durability").center(TWO_ITEMS_ITEM_LENGTH," "), "",
                                                    self.stats.getSingleStatString("Potential").center(TWO_ITEMS_ITEM_LENGTH," "), "") + "\n\n\n"


                cardString += fourItemTemplate.format("",self.stats.getSingleStatString("Strength").center(FOUR_ITEMS_ITEM_LENGTH),"",
                                                      self.stats.getSingleStatString("Low Post Defense").center(FOUR_ITEMS_ITEM_LENGTH),"",
                                                      self.stats.getSingleStatString("Hustle").center(FOUR_ITEMS_ITEM_LENGTH),"",
                                                      self.stats.getSingleStatString("Block").center(FOUR_ITEMS_ITEM_LENGTH),"") + "\n"

                cardString += fiveItemTemplate.format("", self.stats.getSingleStatString("Steal").center(FIVE_ITEMS_ITEM_LENGTH),"",
                                                      self.stats.getSingleStatString("On Ball Defense").center(FIVE_ITEMS_ITEM_LENGTH), "",
                                                      self.stats.getSingleStatString("Offensive Rebound").center(FIVE_ITEMS_ITEM_LENGTH), "",
                                                      self.stats.getSingleStatString("Defensive Rebound").center(FIVE_ITEMS_ITEM_LENGTH),
                                                      "",self.stats.getSingleStatString("Defensive Awareness").center(FIVE_ITEMS_ITEM_LENGTH),
                                                      "") + "\n"
            elif (self.archetypeName == "Vigilante"):
                cardString += twoItemTemplate.format("", self.stats.getSingleStatString("Shoot In Traffic").center(TWO_ITEMS_ITEM_LENGTH," "), "", self.stats.getSingleStatString("Shoot Off Dribble").center(TWO_ITEMS_ITEM_LENGTH," "), "") + "\n\n"
                cardString += twoItemTemplate.format("", self.stats.getSingleStatString("Low Post Offense").center(TWO_ITEMS_ITEM_LENGTH," "), "", self.stats.getSingleStatString("Layup").center(TWO_ITEMS_ITEM_LENGTH," "), "") + "\n\n"
                cardString += twoItemTemplate.format("", self.stats.getSingleStatString("Shot Close").center(TWO_ITEMS_ITEM_LENGTH," "), "", self.stats.getSingleStatString("Post Fadeaway").center(TWO_ITEMS_ITEM_LENGTH," "), "") + "\n\n"
                cardString += twoItemTemplate.format("", self.stats.getSingleStatString("Shot Three Point").center(TWO_ITEMS_ITEM_LENGTH," "), "", self.stats.getSingleStatString("Shot Medium").center(TWO_ITEMS_ITEM_LENGTH," "), "") + "\n\n"
                cardString += twoItemTemplate.format("", self.stats.getSingleStatString("Post Hook").center(TWO_ITEMS_ITEM_LENGTH," "), "", self.stats.getSingleStatString("Consistency").center(TWO_ITEMS_ITEM_LENGTH," "), "") + "\n\n\n"

                cardString += twoItemTemplate.format("", self.stats.getSingleStatString("Low Post Defense").center(TWO_ITEMS_ITEM_LENGTH," "), "",
                                                    self.stats.getSingleStatString("Strength").center(TWO_ITEMS_ITEM_LENGTH," "), "") + "\n"
                cardString += twoItemTemplate.format("", self.stats.getSingleStatString("Hustle").center(TWO_ITEMS_ITEM_LENGTH," "), "",
                                                    self.stats.getSingleStatString("Block").center(TWO_ITEMS_ITEM_LENGTH," "), "") + "\n"
                cardString += twoItemTemplate.format("", self.stats.getSingleStatString("Steal").center(TWO_ITEMS_ITEM_LENGTH," "), "",
                                                    self.stats.getSingleStatString("On Ball Defense").center(TWO_ITEMS_ITEM_LENGTH," "), "") + "\n"
                cardString += twoItemTemplate.format("", self.stats.getSingleStatString("Offensive Rebound").center(TWO_ITEMS_ITEM_LENGTH," "), "",
                                                    self.stats.getSingleStatString("Defensive Rebound").center(TWO_ITEMS_ITEM_LENGTH," "), "") + "\n"
                cardString += twoItemTemplate.format("", self.stats.getSingleStatString("Defensive Awareness").center(TWO_ITEMS_ITEM_LENGTH," "), "",
                                                    self.stats.getSingleStatString("Vertical").center(TWO_ITEMS_ITEM_LENGTH," "), "") + "\n\n"

                cardString += twoItemTemplate.format("", self.stats.getSingleStatString("Shot Inside").center(TWO_ITEMS_ITEM_LENGTH," "), "",
                                                    self.stats.getSingleStatString("Dunk").center(TWO_ITEMS_ITEM_LENGTH," "), "") + "\n"
                cardString += twoItemTemplate.format("", self.stats.getSingleStatString("Standing Dunk").center(TWO_ITEMS_ITEM_LENGTH," "), "",
                                                    self.stats.getSingleStatString("Free Throw").center(TWO_ITEMS_ITEM_LENGTH," "), "") + "\n"
                cardString += twoItemTemplate.format("", self.stats.getSingleStatString("Durability").center(TWO_ITEMS_ITEM_LENGTH," "), "",
                                                    self.stats.getSingleStatString("Stamina").center(TWO_ITEMS_ITEM_LENGTH," "), "") + "\n\n\n"



                cardString += fourItemTemplate.format("", self.stats.getSingleStatString("Potential").center(
                    FOUR_ITEMS_ITEM_LENGTH), "",
                                                      self.stats.getSingleStatString("Off Hand Dribbling").center(
                                                          FOUR_ITEMS_ITEM_LENGTH), "",
                                                      self.stats.getSingleStatString("Hands").center(
                                                          FOUR_ITEMS_ITEM_LENGTH), "",
                                                      self.stats.getSingleStatString("Offensive Awareness").center(
                                                          FOUR_ITEMS_ITEM_LENGTH), "") + "\n"

                cardString += fiveItemTemplate.format("", self.stats.getSingleStatString("Ball Handling").center(
                    FIVE_ITEMS_ITEM_LENGTH), "",
                                                      self.stats.getSingleStatString("Ball Security").center(
                                                          FIVE_ITEMS_ITEM_LENGTH), "",
                                                      self.stats.getSingleStatString("Pass").center(
                                                          FIVE_ITEMS_ITEM_LENGTH), "",
                                                      self.stats.getSingleStatString("Speed").center(
                                                          FIVE_ITEMS_ITEM_LENGTH),
                                                      "", self.stats.getSingleStatString("Quickness").center(
                        FIVE_ITEMS_ITEM_LENGTH),
                                                      "") + "\n"
            elif (self.archetypeName == "Medic"):
                cardString += twoItemTemplate.format("", self.stats.getSingleStatString("Offensive Rebound").center(TWO_ITEMS_ITEM_LENGTH," "), "", self.stats.getSingleStatString("Defensive Rebound").center(TWO_ITEMS_ITEM_LENGTH," "), "") + "\n\n"
                cardString += twoItemTemplate.format("", self.stats.getSingleStatString("On Ball Defense").center(TWO_ITEMS_ITEM_LENGTH," "), "", self.stats.getSingleStatString("Low Post Defense").center(TWO_ITEMS_ITEM_LENGTH," "), "") + "\n\n"
                cardString += twoItemTemplate.format("", self.stats.getSingleStatString("Hustle").center(TWO_ITEMS_ITEM_LENGTH," "), "", self.stats.getSingleStatString("Strength").center(TWO_ITEMS_ITEM_LENGTH," "), "") + "\n\n"
                cardString += twoItemTemplate.format("", self.stats.getSingleStatString("Steal").center(TWO_ITEMS_ITEM_LENGTH," "), "", self.stats.getSingleStatString("Block").center(TWO_ITEMS_ITEM_LENGTH," "), "") + "\n\n"
                cardString += twoItemTemplate.format("", self.stats.getSingleStatString("Defensive Awareness").center(TWO_ITEMS_ITEM_LENGTH," "), "", self.stats.getSingleStatString("Vertical").center(TWO_ITEMS_ITEM_LENGTH," "), "") + "\n\n\n"

                cardString += twoItemTemplate.format("", self.stats.getSingleStatString("Off Hand Dribbling").center(TWO_ITEMS_ITEM_LENGTH," "), "",
                                                    self.stats.getSingleStatString("Hands").center(TWO_ITEMS_ITEM_LENGTH," "), "") + "\n"
                cardString += twoItemTemplate.format("", self.stats.getSingleStatString("Offensive Awareness").center(TWO_ITEMS_ITEM_LENGTH," "), "",
                                                    self.stats.getSingleStatString("Ball Handling").center(TWO_ITEMS_ITEM_LENGTH," "), "") + "\n"
                cardString += twoItemTemplate.format("", self.stats.getSingleStatString("Ball Security").center(TWO_ITEMS_ITEM_LENGTH," "), "",
                                                    self.stats.getSingleStatString("Pass").center(TWO_ITEMS_ITEM_LENGTH," "), "") + "\n"
                cardString += twoItemTemplate.format("", self.stats.getSingleStatString("Speed").center(TWO_ITEMS_ITEM_LENGTH," "), "",
                                                    self.stats.getSingleStatString("Quickness").center(TWO_ITEMS_ITEM_LENGTH," "), "") + "\n\n"

                cardString += twoItemTemplate.format("", self.stats.getSingleStatString("Shot Inside").center(TWO_ITEMS_ITEM_LENGTH," "), "",
                                                    self.stats.getSingleStatString("Dunk").center(TWO_ITEMS_ITEM_LENGTH," "), "") + "\n"
                cardString += twoItemTemplate.format("", self.stats.getSingleStatString("Standing Dunk").center(TWO_ITEMS_ITEM_LENGTH," "), "",
                                                    self.stats.getSingleStatString("Free Throw").center(TWO_ITEMS_ITEM_LENGTH," "), "") + "\n"
                cardString += twoItemTemplate.format("", self.stats.getSingleStatString("Durability").center(TWO_ITEMS_ITEM_LENGTH," "), "",
                                                    self.stats.getSingleStatString("Stamina").center(TWO_ITEMS_ITEM_LENGTH," "), "") + "\n\n\n"

                cardString += fiveItemTemplate.format("", self.stats.getSingleStatString("Potential").center(
                    FIVE_ITEMS_ITEM_LENGTH), "",
                                                      self.stats.getSingleStatString("Shot Close").center(
                                                          FIVE_ITEMS_ITEM_LENGTH), "",
                                                      self.stats.getSingleStatString("Layup").center(
                                                          FIVE_ITEMS_ITEM_LENGTH), "",
                                                      self.stats.getSingleStatString("Post Fadeaway").center(
                                                          FIVE_ITEMS_ITEM_LENGTH),
                                                      "", self.stats.getSingleStatString("Post Hook").center(
                        FIVE_ITEMS_ITEM_LENGTH),
                                                      "") + "\n"

                cardString += sixItemTemplate.format("", self.stats.getSingleStatString("Low Post Offense").center(
                    SIX_ITEMS_ITEM_LENGTH), "",
                                                      self.stats.getSingleStatString("Shot Medium").center(
                                                          SIX_ITEMS_ITEM_LENGTH), "",
                                                      self.stats.getSingleStatString("Shot Three Point").center(
                                                          SIX_ITEMS_ITEM_LENGTH), "",
                                                      self.stats.getSingleStatString("Shoot Off Dribble").center(
                                                          SIX_ITEMS_ITEM_LENGTH),
                                                      "", self.stats.getSingleStatString("Shoot In Traffic").center(
                        SIX_ITEMS_ITEM_LENGTH),
                                                      "", self.stats.getSingleStatString("Consistency").center(
                        SIX_ITEMS_ITEM_LENGTH),
                                                      "") + "\n"
            elif (self.archetypeName == "Guardian"):
                cardString += twoItemTemplate.format("", self.stats.getSingleStatString("Steal").center(TWO_ITEMS_ITEM_LENGTH," "), "", self.stats.getSingleStatString("Block").center(TWO_ITEMS_ITEM_LENGTH," "), "") + "\n\n"
                cardString += twoItemTemplate.format("", self.stats.getSingleStatString("On Ball Defense").center(TWO_ITEMS_ITEM_LENGTH," "), "", self.stats.getSingleStatString("Low Post Defense").center(TWO_ITEMS_ITEM_LENGTH," "), "") + "\n\n"
                cardString += twoItemTemplate.format("", self.stats.getSingleStatString("Hustle").center(TWO_ITEMS_ITEM_LENGTH," "), "", self.stats.getSingleStatString("Strength").center(TWO_ITEMS_ITEM_LENGTH," "), "") + "\n\n"
                cardString += twoItemTemplate.format("", self.stats.getSingleStatString("Offensive Rebound").center(TWO_ITEMS_ITEM_LENGTH," "), "", self.stats.getSingleStatString("Defensive Rebound").center(TWO_ITEMS_ITEM_LENGTH," "), "") + "\n\n"
                cardString += twoItemTemplate.format("", self.stats.getSingleStatString("Defensive Awareness").center(TWO_ITEMS_ITEM_LENGTH," "), "", self.stats.getSingleStatString("Vertical").center(TWO_ITEMS_ITEM_LENGTH," "), "") + "\n\n\n"

                cardString += twoItemTemplate.format("", self.stats.getSingleStatString("Shot Close").center(TWO_ITEMS_ITEM_LENGTH," "), "",
                                                    self.stats.getSingleStatString("Layup").center(TWO_ITEMS_ITEM_LENGTH," "), "") + "\n"
                cardString += twoItemTemplate.format("", self.stats.getSingleStatString("Post Fadeaway").center(TWO_ITEMS_ITEM_LENGTH," "), "",
                                                    self.stats.getSingleStatString("Post Hook").center(TWO_ITEMS_ITEM_LENGTH," "), "") + "\n"
                cardString += twoItemTemplate.format("", self.stats.getSingleStatString("Low Post Offense").center(TWO_ITEMS_ITEM_LENGTH," "), "",
                                                    self.stats.getSingleStatString("Consistency").center(TWO_ITEMS_ITEM_LENGTH," "), "") + "\n"
                cardString += twoItemTemplate.format("", self.stats.getSingleStatString("Shot Medium").center(TWO_ITEMS_ITEM_LENGTH," "), "",
                                                    self.stats.getSingleStatString("Shot Three Point").center(TWO_ITEMS_ITEM_LENGTH," "), "") + "\n"
                cardString += twoItemTemplate.format("", self.stats.getSingleStatString("Shoot In Traffic").center(TWO_ITEMS_ITEM_LENGTH," "), "",
                                                    self.stats.getSingleStatString("Shoot Off Dribble").center(TWO_ITEMS_ITEM_LENGTH," "), "") + "\n\n"

                cardString += twoItemTemplate.format("", self.stats.getSingleStatString("Shot Inside").center(TWO_ITEMS_ITEM_LENGTH," "), "",
                                                    self.stats.getSingleStatString("Dunk").center(TWO_ITEMS_ITEM_LENGTH," "), "") + "\n"
                cardString += twoItemTemplate.format("", self.stats.getSingleStatString("Standing Dunk").center(TWO_ITEMS_ITEM_LENGTH," "), "",
                                                    self.stats.getSingleStatString("Free Throw").center(TWO_ITEMS_ITEM_LENGTH," "), "") + "\n"
                cardString += twoItemTemplate.format("", self.stats.getSingleStatString("Durability").center(TWO_ITEMS_ITEM_LENGTH," "), "",
                                                    self.stats.getSingleStatString("Stamina").center(TWO_ITEMS_ITEM_LENGTH," "), "") + "\n\n\n"


                cardString += fourItemTemplate.format("", self.stats.getSingleStatString("Potential").center(
                    FOUR_ITEMS_ITEM_LENGTH), "",
                                                      self.stats.getSingleStatString("Off Hand Dribbling").center(
                                                          FOUR_ITEMS_ITEM_LENGTH), "",
                                                      self.stats.getSingleStatString("Hands").center(
                                                          FOUR_ITEMS_ITEM_LENGTH), "",
                                                      self.stats.getSingleStatString("Offensive Awareness").center(
                                                          FOUR_ITEMS_ITEM_LENGTH), "") + "\n"

                cardString += fiveItemTemplate.format("", self.stats.getSingleStatString("Ball Handling").center(
                    FIVE_ITEMS_ITEM_LENGTH), "",
                                                      self.stats.getSingleStatString("Ball Security").center(
                                                          FIVE_ITEMS_ITEM_LENGTH), "",
                                                      self.stats.getSingleStatString("Pass").center(
                                                          FIVE_ITEMS_ITEM_LENGTH), "",
                                                      self.stats.getSingleStatString("Speed").center(
                                                          FIVE_ITEMS_ITEM_LENGTH),
                                                      "", self.stats.getSingleStatString("Quickness").center(
                        FIVE_ITEMS_ITEM_LENGTH),
                                                      "") + "\n"
            elif (self.archetypeName == "Engineer"):
                cardString += twoItemTemplate.format("", self.stats.getSingleStatString("Ball Handling").center(TWO_ITEMS_ITEM_LENGTH," "), "", self.stats.getSingleStatString("Ball Security").center(TWO_ITEMS_ITEM_LENGTH," "), "") + "\n\n"
                cardString += twoItemTemplate.format("", self.stats.getSingleStatString("Offensive Awareness").center(TWO_ITEMS_ITEM_LENGTH," "), "", self.stats.getSingleStatString("Off Hand Dribbling").center(TWO_ITEMS_ITEM_LENGTH," "), "") + "\n\n"
                cardString += twoItemTemplate.format("", self.stats.getSingleStatString("Hands").center(TWO_ITEMS_ITEM_LENGTH," "), "", self.stats.getSingleStatString("Pass").center(TWO_ITEMS_ITEM_LENGTH," "), "") + "\n\n"
                cardString += twoItemTemplate.format("", self.stats.getSingleStatString("Speed").center(TWO_ITEMS_ITEM_LENGTH," "), "", self.stats.getSingleStatString("Quickness").center(TWO_ITEMS_ITEM_LENGTH," "), "") + "\n\n\n"

                cardString += twoItemTemplate.format("", self.stats.getSingleStatString("Low Post Defense").center(TWO_ITEMS_ITEM_LENGTH," "), "",
                                                    self.stats.getSingleStatString("Strength").center(TWO_ITEMS_ITEM_LENGTH," "), "") + "\n"
                cardString += twoItemTemplate.format("", self.stats.getSingleStatString("Hustle").center(TWO_ITEMS_ITEM_LENGTH," "), "",
                                                    self.stats.getSingleStatString("Block").center(TWO_ITEMS_ITEM_LENGTH," "), "") + "\n"
                cardString += twoItemTemplate.format("", self.stats.getSingleStatString("Steal").center(TWO_ITEMS_ITEM_LENGTH," "), "",
                                                    self.stats.getSingleStatString("On Ball Defense").center(TWO_ITEMS_ITEM_LENGTH," "), "") + "\n"
                cardString += twoItemTemplate.format("", self.stats.getSingleStatString("Offensive Rebound").center(TWO_ITEMS_ITEM_LENGTH," "), "",
                                                    self.stats.getSingleStatString("Defensive Rebound").center(TWO_ITEMS_ITEM_LENGTH," "), "") + "\n"
                cardString += twoItemTemplate.format("", self.stats.getSingleStatString("Defensive Awareness").center(TWO_ITEMS_ITEM_LENGTH," "), "",
                                                    self.stats.getSingleStatString("Vertical").center(TWO_ITEMS_ITEM_LENGTH," "), "") + "\n\n"

                cardString += twoItemTemplate.format("", self.stats.getSingleStatString("Shot Inside").center(TWO_ITEMS_ITEM_LENGTH," "), "",
                                                    self.stats.getSingleStatString("Dunk").center(TWO_ITEMS_ITEM_LENGTH," "), "") + "\n"
                cardString += twoItemTemplate.format("", self.stats.getSingleStatString("Standing Dunk").center(TWO_ITEMS_ITEM_LENGTH," "), "",
                                                    self.stats.getSingleStatString("Free Throw").center(TWO_ITEMS_ITEM_LENGTH," "), "") + "\n"
                cardString += twoItemTemplate.format("", self.stats.getSingleStatString("Durability").center(TWO_ITEMS_ITEM_LENGTH," "), "",
                                                    self.stats.getSingleStatString("Stamina").center(TWO_ITEMS_ITEM_LENGTH," "), "") + "\n\n\n"

                cardString += fiveItemTemplate.format("", self.stats.getSingleStatString("Potential").center(
                    FIVE_ITEMS_ITEM_LENGTH), "",
                                                      self.stats.getSingleStatString("Shot Close").center(
                                                          FIVE_ITEMS_ITEM_LENGTH), "",
                                                      self.stats.getSingleStatString("Layup").center(
                                                          FIVE_ITEMS_ITEM_LENGTH), "",
                                                      self.stats.getSingleStatString("Post Fadeaway").center(
                                                          FIVE_ITEMS_ITEM_LENGTH),
                                                      "", self.stats.getSingleStatString("Post Hook").center(
                        FIVE_ITEMS_ITEM_LENGTH),
                                                      "") + "\n"

                cardString += sixItemTemplate.format("", self.stats.getSingleStatString("Low Post Offense").center(
                    SIX_ITEMS_ITEM_LENGTH), "",
                                                     self.stats.getSingleStatString("Shot Medium").center(
                                                         SIX_ITEMS_ITEM_LENGTH), "",
                                                     self.stats.getSingleStatString("Shot Three Point").center(
                                                         SIX_ITEMS_ITEM_LENGTH), "",
                                                     self.stats.getSingleStatString("Shoot Off Dribble").center(
                                                         SIX_ITEMS_ITEM_LENGTH),
                                                     "", self.stats.getSingleStatString("Shoot In Traffic").center(
                        SIX_ITEMS_ITEM_LENGTH),
                                                     "", self.stats.getSingleStatString("Consistency").center(
                        SIX_ITEMS_ITEM_LENGTH),
                                                     "") + "\n"
            elif (self.archetypeName == "Director"):
                cardString += twoItemTemplate.format("", self.stats.getSingleStatString("Speed").center(TWO_ITEMS_ITEM_LENGTH," "), "", self.stats.getSingleStatString("Pass").center(TWO_ITEMS_ITEM_LENGTH," "), "") + "\n\n"
                cardString += twoItemTemplate.format("", self.stats.getSingleStatString("Offensive Awareness").center(TWO_ITEMS_ITEM_LENGTH," "), "", self.stats.getSingleStatString("Quickness").center(TWO_ITEMS_ITEM_LENGTH," "), "") + "\n\n"
                cardString += twoItemTemplate.format("", self.stats.getSingleStatString("Hands").center(TWO_ITEMS_ITEM_LENGTH," "), "", self.stats.getSingleStatString("Off Hand Dribbling").center(TWO_ITEMS_ITEM_LENGTH," "), "") + "\n\n"
                cardString += twoItemTemplate.format("", self.stats.getSingleStatString("Ball Handling").center(TWO_ITEMS_ITEM_LENGTH," "), "", self.stats.getSingleStatString("Ball Security").center(TWO_ITEMS_ITEM_LENGTH," "), "") + "\n\n\n"

                cardString += twoItemTemplate.format("", self.stats.getSingleStatString("Shot Close").center(TWO_ITEMS_ITEM_LENGTH," "), "",
                                                    self.stats.getSingleStatString("Layup").center(TWO_ITEMS_ITEM_LENGTH," "), "") + "\n"
                cardString += twoItemTemplate.format("", self.stats.getSingleStatString("Post Fadeaway").center(TWO_ITEMS_ITEM_LENGTH," "), "",
                                                    self.stats.getSingleStatString("Post Hook").center(TWO_ITEMS_ITEM_LENGTH," "), "") + "\n"
                cardString += twoItemTemplate.format("", self.stats.getSingleStatString("Low Post Offense").center(TWO_ITEMS_ITEM_LENGTH," "), "",
                                                    self.stats.getSingleStatString("Consistency").center(TWO_ITEMS_ITEM_LENGTH," "), "") + "\n"
                cardString += twoItemTemplate.format("", self.stats.getSingleStatString("Shot Medium").center(TWO_ITEMS_ITEM_LENGTH," "), "",
                                                    self.stats.getSingleStatString("Shot Three Point").center(TWO_ITEMS_ITEM_LENGTH," "), "") + "\n"
                cardString += twoItemTemplate.format("", self.stats.getSingleStatString("Shoot In Traffic").center(TWO_ITEMS_ITEM_LENGTH," "), "",
                                                    self.stats.getSingleStatString("Shoot Off Dribble").center(TWO_ITEMS_ITEM_LENGTH," "), "") + "\n\n"

                cardString += twoItemTemplate.format("", self.stats.getSingleStatString("Shot Inside").center(TWO_ITEMS_ITEM_LENGTH," "), "",
                                                    self.stats.getSingleStatString("Dunk").center(TWO_ITEMS_ITEM_LENGTH," "), "") + "\n"
                cardString += twoItemTemplate.format("", self.stats.getSingleStatString("Standing Dunk").center(TWO_ITEMS_ITEM_LENGTH," "), "",
                                                    self.stats.getSingleStatString("Free Throw").center(TWO_ITEMS_ITEM_LENGTH," "), "") + "\n"
                cardString += twoItemTemplate.format("", self.stats.getSingleStatString("Vertical").center(TWO_ITEMS_ITEM_LENGTH," "), "",
                                                    self.stats.getSingleStatString("Stamina").center(TWO_ITEMS_ITEM_LENGTH," "), "") + "\n"
                cardString += twoItemTemplate.format("", self.stats.getSingleStatString("Durability").center(TWO_ITEMS_ITEM_LENGTH," "), "",
                                                    self.stats.getSingleStatString("Potential").center(TWO_ITEMS_ITEM_LENGTH," "), "") + "\n\n\n"

                cardString += fourItemTemplate.format("", self.stats.getSingleStatString("Strength").center(
                    FOUR_ITEMS_ITEM_LENGTH), "",
                                                      self.stats.getSingleStatString("Low Post Defense").center(
                                                          FOUR_ITEMS_ITEM_LENGTH), "",
                                                      self.stats.getSingleStatString("Hustle").center(
                                                          FOUR_ITEMS_ITEM_LENGTH), "",
                                                      self.stats.getSingleStatString("Block").center(
                                                          FOUR_ITEMS_ITEM_LENGTH), "") + "\n"

                cardString += fiveItemTemplate.format("", self.stats.getSingleStatString("Steal").center(
                    FIVE_ITEMS_ITEM_LENGTH), "",
                                                      self.stats.getSingleStatString("On Ball Defense").center(
                                                          FIVE_ITEMS_ITEM_LENGTH), "",
                                                      self.stats.getSingleStatString("Offensive Rebound").center(
                                                          FIVE_ITEMS_ITEM_LENGTH), "",
                                                      self.stats.getSingleStatString("Defensive Rebound").center(
                                                          FIVE_ITEMS_ITEM_LENGTH),
                                                      "", self.stats.getSingleStatString("Defensive Awareness").center(
                        FIVE_ITEMS_ITEM_LENGTH),
                                                      "") + "\n"

        # This section prints all necessary signature skill information that we have to
        # enter in manually.
        if(True):

            signaturesString = ""
            # Things to add:
            signaturesString += ("Fadeaway: " + self.signatureStats.shots.get("Fadeaway")).center(WIDTH) + "\n"
            signaturesString += ("Contested: " + self.signatureStats.shots.get("Contested")).center(WIDTH) + "\n"
            signaturesString += ("Escape Dribble Pull Up: " + self.signatureStats.shots.get("Escape Dribble Pull Up")).center(WIDTH) + "\n"
            signaturesString += ("Runner: " + self.signatureStats.shots.get("Runner")).center(WIDTH) + "\n\n"

            signaturesString += ("Dribble Pull Up: " + self.signatureStats.momentumShotsOutside.get("Dribble Pull Up")).center(WIDTH) + "\n"
            signaturesString += ("Spin Jumper: " + self.signatureStats.momentumShotsOutside.get("Spin Jumper")).center(WIDTH) + "\n"
            signaturesString += ("Hop Jumper: " + self.signatureStats.momentumShotsOutside.get("Hop Jumper")).center(WIDTH) + "\n\n"

            signaturesString += ("Post Fade: " + self.signatureStats.postShots.get("Post Fade")).center(WIDTH) + "\n"
            signaturesString += ("Post Hook: " + self.signatureStats.postShots.get("Post Hook")).center(WIDTH) + "\n"
            signaturesString += ("Post Hop Shot: " + self.signatureStats.postShots.get("Post Hop Shot")).center(WIDTH) + "\n"
            signaturesString += ("Post Shimmy Shot: " + self.signatureStats.postShots.get("Post Shimmy Shot")).center(WIDTH) + "\n"
            signaturesString += ("Post Drive Stepback Shot: " + self.signatureStats.postShots.get("Post Drive Stepback Shot")).center(WIDTH) + "\n"
            signaturesString += ("Post Spin Stepback Shot: " + self.signatureStats.postShots.get("Post Spin Stepback Shot")).center(WIDTH) + "\n"
            signaturesString += ("Post Protect Shot: " + self.signatureStats.postShots.get("Post Protect Shot")).center(WIDTH) + "\n"
            signaturesString += ("Post Protect Spin Shot: " + self.signatureStats.postShots.get("Post Protect Spin Shot")).center(WIDTH) + "\n\n"

            signaturesString += ("ISO Crossover: " + self.signatureStats.dribbleMoves.get("ISO Crossover")).center(WIDTH) + "\n"
            signaturesString += ("ISO Behind Back: " + self.signatureStats.dribbleMoves.get("ISO Behind Back")).center(WIDTH) + "\n"
            signaturesString += ("ISO Spin: " + self.signatureStats.dribbleMoves.get("ISO Spin")).center(WIDTH) + "\n"
            signaturesString += ("ISO Hesitation: " + self.signatureStats.dribbleMoves.get("ISO Hesitation")).center(WIDTH) + "\n\n"

            signaturesString += ("Layup Package: " + self.signatureStats.dunksAndLayups.get("Layup Package")).center(WIDTH) + "\n"


            cardString += "\n\n\n\n\n" + "SIGNATURE SKILLS TO ADD".center(WIDTH) + "\n\n" + signaturesString

        cardString += "\n\n\n\n"
        cardString += str(self.overwritePlayer)

        return cardString

    # Method for managing deletion of a Player object.
    def __del__(self):
        self.__clothesType = "Jersey"
        self.arrayOfEnchantments = []
        del self.playerRarity
        del self

    # This class acts as a structure to store all settable stats for a
    # player.
    class StatsDict:
        def __init__(self):
            self.isCursedList = []
            self.isBlessedList = []
            self.statsValues = getBasicStatsValues()
            self.statsLimits = getBasicStatsLimits()
            self.statsBonuses = getBasicStatsBonuses()
            self.statsRarity = getBasicStatsRarity()

        # This dictionary holds the literal values of the stats.
        #statsValues = BASIC_STATS_VALUES

        # This dictionary specifies the limits of each skill. If a value
        # is set below or above the min/max values, the min/max value
        # will be set instead.
        #statsLimits = BASIC_STATS_LIMITS

        # This dictionary remembers any adjustments made to a statistic, via
        # rarity bonuses.
        #statsBonuses = BASIC_STATS_BONUSES

        # This dictionary simply tracks the rarity of a stat increase.
        #statsRarity = BASIC_STATS_RARITY

        # This method adds a rarity bonus to a statistic.
        def addRarityBonus(self, statName, rarityGrade, statBonus):
            currentStatBonus = self.statsBonuses.get(statName)

            if(type(currentStatBonus) == "<class 'int'>"):
                newStatBonus = currentStatBonus + statBonus
            else:
                newStatBonus = statBonus
            currentStatTotal = self.statsValues.get(statName)
            newStatTotal = currentStatTotal + statBonus

            self.statsBonuses.update({statName: newStatBonus})
            self.statsRarity.update({statName: rarityGrade})

            self.set(statName, newStatTotal)

        # These get and set methods allows the various stats to be set
        # and gotten.
        def set(self, statName, value):
            statMin = self.statsLimits.get(statName)[0]
            statMax = self.statsLimits.get(statName)[1]

            if (value > statMax):
                finalValue = statMax
            elif (value < statMin):
                finalValue = statMin
            else:
                finalValue = value

            self.statsValues.update({statName: finalValue})
            return True
        def get(self, statName):
            returnValue = self.statsValues.get(statName)
            return returnValue

        # Returns a neatly formatted string that represents a bonus, if
        # one is present.
        def getBonus(self, statName):
            statRarity = self.statsRarity.get(statName)
            if (statRarity == "Common"):
                return ""
            else:
                returnString = " (" + str(statRarity) +", +" + str(self.statsBonuses.get(statName)) + ")"
                return returnString

        # Simple method to print all stats in a neat and formatted way.
        def __str__(self):
            returnString = \
                "Off Hand Dribbling: " + str(self.statsValues.get("Off Hand Dribbling")) + self.getBonus(
                    "Off Hand Dribbling") + "\n" + \
                "Hands: " + str(self.statsValues.get("Hands")) + self.getBonus("Hands") + "\n" + \
                "Offensive Awareness: " + str(self.statsValues.get("Offensive Awareness")) + self.getBonus(
                    "Offensive Awareness") + "\n" + \
                "Ball Handling: " + str(self.statsValues.get("Ball Handling")) + self.getBonus("Ball Handling") + "\n" + \
                "Ball Security: " + str(self.statsValues.get("Ball Security")) + self.getBonus("Ball Security") + "\n" + \
                "Pass: " + str(self.statsValues.get("Pass")) + self.getBonus("Pass") + "\n" + \
                "Speed: " + str(self.statsValues.get("Speed")) + self.getBonus("Speed") + "\n" + \
                "Quickness: " + str(self.statsValues.get("Quickness")) + self.getBonus("Quickness") + "\n" + \
                "Low Post Defense: " + str(self.statsValues.get("Low Post Defense")) + self.getBonus(
                    "Low Post Defense") + "\n" + \
                "Strength: " + str(self.statsValues.get("Strength")) + self.getBonus("Strength") + "\n" + \
                "Hustle: " + str(self.statsValues.get("Hustle")) + self.getBonus("Hustle") + "\n" + \
                "Block: " + str(self.statsValues.get("Block")) + self.getBonus("Block") + "\n" + \
                "Steal: " + str(self.statsValues.get("Steal")) + self.getBonus("Steal") + "\n" + \
                "On Ball Defense: " + str(self.statsValues.get("On Ball Defense")) + self.getBonus(
                    "On Ball Defense") + "\n" + \
                "Offensive Rebound: " + str(self.statsValues.get("Offensive Rebound")) + self.getBonus(
                    "Offensive Rebound") + "\n" + \
                "Defensive Rebound: " + str(self.statsValues.get("Defensive Rebound")) + self.getBonus(
                    "Defensive Rebound") + "\n" + \
                "Defensive Awareness: " + str(self.statsValues.get("Defensive Awareness")) + self.getBonus(
                    "Defensive Awareness") + "\n" + \
                "Shot Inside: " + str(self.statsValues.get("Shot Inside")) + self.getBonus("Shot Inside") + "\n" + \
                "Dunk: " + str(self.statsValues.get("Dunk")) + self.getBonus("Dunk") + "\n" + \
                "Standing Dunk: " + str(self.statsValues.get("Standing Dunk")) + self.getBonus("Standing Dunk") + "\n" + \
                "Vertical: " + str(self.statsValues.get("Vertical")) + self.getBonus("Vertical") + "\n" + \
                "Free Throw: " + str(self.statsValues.get("Free Throw")) + self.getBonus("Free Throw") + "\n" + \
                "Stamina: " + str(self.statsValues.get("Stamina")) + self.getBonus("Stamina") + "\n" + \
                "Durability: " + str(self.statsValues.get("Durability")) + self.getBonus("Durability") + "\n" + \
                "Potential: " + str(self.statsValues.get("Potential")) + self.getBonus("Potential") + "\n" + \
                "Shot Close: " + str(self.statsValues.get("Shot Close")) + self.getBonus("Shot Close") + "\n" + \
                "Layup: " + str(self.statsValues.get("Layup")) + self.getBonus("Layup") + "\n" + \
                "Post Fadeaway: " + str(self.statsValues.get("Post Fadeaway")) + self.getBonus("Post Fadeaway") + "\n" + \
                "Post Hook: " + str(self.statsValues.get("Post Hook")) + self.getBonus("Post Hook") + "\n" + \
                "Low Post Offense: " + str(self.statsValues.get("Low Post Offense")) + self.getBonus(
                    "Low Post Offense") + "\n" + \
                "Shot Medium: " + str(self.statsValues.get("Shot Medium")) + self.getBonus("Shot Medium") + "\n" + \
                "Shot Three Point: " + str(self.statsValues.get("Shot Three Point")) + self.getBonus(
                    "Shot Three Point") + "\n" + \
                "Shoot In Traffic: " + str(self.statsValues.get("Shoot In Traffic")) + self.getBonus(
                    "Shoot In Traffic") + "\n" + \
                "Shoot Off Dribble: " + str(self.statsValues.get("Shoot Off Dribble")) + self.getBonus(
                    "Shoot Off Dribble") + "\n" + \
                "Consistency: " + str(self.statsValues.get("Consistency")) + self.getBonus("Consistency")
            return returnString


        # This method returns a single Stat, neatly formatted in a string (per __str__ style), including
        # any stat bonuses or enchantments.
        def getSingleStatString(self,statName):
            returnString = statName + ": "



            if(statName in self.isCursedList and statName not in self.isBlessedList):
                returnString += "¿" + str(self.statsValues.get(statName)) + "¿" + self.getBonus(statName)
            elif(statName in self.isBlessedList and statName not in self.isCursedList):
                returnString += "†" + str(self.statsValues.get(statName)) + "†" + self.getBonus(statName)
            elif (statName in self.isBlessedList and statName in self.isCursedList):
                returnString += "¿" + str(self.statsValues.get(statName)) + "†" + self.getBonus(statName)
            else:
                returnString += str(self.statsValues.get(statName)) + self.getBonus(statName)

            return returnString

        # This method is the same as the __str__ method, except that it
        # returns a string to be formatted according to the 2k order.
        def returnOrderedString(self):
            returnString = \
                "Shot Inside: " + str(self.statsValues.get("Shot Inside")) + self.getBonus("Shot Inside") + "\n" + \
                "Shot Close: " + str(self.statsValues.get("Shot Close")) + self.getBonus("Shot Close") + "\n" + \
                "Shot Medium: " + str(self.statsValues.get("Shot Medium")) + self.getBonus("Shot Medium") + "\n" + \
                "Shot Three Point: " + str(self.statsValues.get("Shot Three Point")) + self.getBonus(
                    "Shot Three Point") + "\n" + \
                "Free Throw: " + str(self.statsValues.get("Free Throw")) + self.getBonus("Free Throw") + "\n" + \
                "Layup: " + str(self.statsValues.get("Layup")) + self.getBonus("Layup") + "\n" + \
                "Dunk: " + str(self.statsValues.get("Dunk")) + self.getBonus("Dunk") + "\n" + \
                "Standing Dunk: " + str(self.statsValues.get("Standing Dunk")) + self.getBonus(
                    "Standing Dunk") + "\n" + \
                "Shoot In Traffic: " + str(self.statsValues.get("Shoot In Traffic")) + self.getBonus(
                    "Shoot In Traffic") + "\n" + \
                "Post Fadeaway: " + str(self.statsValues.get("Post Fadeaway")) + self.getBonus(
                    "Post Fadeaway") + "\n" + \
                "Post Hook: " + str(self.statsValues.get("Post Hook")) + self.getBonus("Post Hook") + "\n" + \
                "Shoot Off Dribble: " + str(self.statsValues.get("Shoot Off Dribble")) + self.getBonus(
                    "Shoot Off Dribble") + "\n" + \
                "Ball Handling: " + str(self.statsValues.get("Ball Handling")) + self.getBonus(
                    "Ball Handling") + "\n" + \
                "Off Hand Dribbling: " + str(self.statsValues.get("Off Hand Dribbling")) + self.getBonus(
                    "Off Hand Dribbling") + "\n" + \
                "Ball Security: " + str(self.statsValues.get("Ball Security")) + self.getBonus(
                    "Ball Security") + "\n" + \
                "Pass: " + str(self.statsValues.get("Pass")) + self.getBonus("Pass") + "\n" + \
                "Block: " + str(self.statsValues.get("Block")) + self.getBonus("Block") + "\n" + \
                "Steal: " + str(self.statsValues.get("Steal")) + self.getBonus("Steal") + "\n" + \
                "Hands: " + str(self.statsValues.get("Hands")) + self.getBonus("Hands") + "\n" + \
                "On Ball Defense: " + str(self.statsValues.get("On Ball Defense")) + self.getBonus(
                    "On Ball Defense") + "\n" + \
                "Offensive Rebound: " + str(self.statsValues.get("Offensive Rebound")) + self.getBonus(
                    "Offensive Rebound") + "\n" + \
                "Defensive Rebound: " + str(self.statsValues.get("Defensive Rebound")) + self.getBonus(
                    "Defensive Rebound") + "\n" + \
                "Low Post Offense: " + str(self.statsValues.get("Low Post Offense")) + self.getBonus(
                    "Low Post Offense") + "\n" + \
                "Low Post Defense: " + str(self.statsValues.get("Low Post Defense")) + self.getBonus(
                    "Low Post Defense") + "\n" + \
                "Offensive Awareness: " + str(self.statsValues.get("Offensive Awareness")) + self.getBonus(
                    "Offensive Awareness") + "\n" + \
                "Defensive Awareness: " + str(self.statsValues.get("Defensive Awareness")) + self.getBonus(
                    "Defensive Awareness") + "\n" + \
                "Consistency: " + str(self.statsValues.get("Consistency")) + self.getBonus("Consistency") + "\n" + \
                "Stamina: " + str(self.statsValues.get("Stamina")) + self.getBonus("Stamina") + "\n" + \
                "Speed: " + str(self.statsValues.get("Speed")) + self.getBonus("Speed") + "\n" + \
                "Quickness: " + str(self.statsValues.get("Quickness")) + self.getBonus("Quickness") + "\n" + \
                "Strength: " + str(self.statsValues.get("Strength")) + self.getBonus("Strength") + "\n" + \
                "Vertical: " + str(self.statsValues.get("Vertical")) + self.getBonus("Vertical") + "\n" + \
                "Hustle: " + str(self.statsValues.get("Hustle")) + self.getBonus("Hustle") + "\n" + \
                "Durability: " + str(self.statsValues.get("Durability")) + self.getBonus("Durability") + "\n" + \
                "Potential: " + str(self.statsValues.get("Potential")) + self.getBonus("Potential")
            return returnString

        def resetDicts(self):
            self.statsValues = {"Off Hand Dribbling": 0,
                                "Hands": 0,
                                "Offensive Awareness": 0,
                                "Ball Handling": 0,
                                "Ball Security": 0,
                                "Pass": 0,
                                "Speed": 0,
                                "Quickness": 0,
                                "Low Post Defense": 0,
                                "Strength": 0,
                                "Hustle": 0,
                                "Block": 0,
                                "Steal": 0,
                                "On Ball Defense": 0,
                                "Offensive Rebound": 0,
                                "Defensive Rebound": 0,
                                "Defensive Awareness": 0,
                                "Shot Inside": 0,
                                "Dunk": 0,
                                "Standing Dunk": 0,
                                "Vertical": 0,
                                "Free Throw": 0,
                                "Stamina": 0,
                                "Durability": 0,
                                "Potential": 0,
                                "Shot Close": 0,
                                "Layup": 0,
                                "Post Fadeaway": 0,
                                "Post Hook": 0,
                                "Low Post Offense": 0,
                                "Shot Medium": 0,
                                "Shot Three Point": 0,
                                "Shoot In Traffic": 0,
                                "Shoot Off Dribble": 0,
                                "Consistency": 0}
            self.statsBonuses = {"Off Hand Dribbling": 0,
                                 "Hands": 0,
                                 "Offensive Awareness": 0,
                                 "Ball Handling": 0,
                                 "Ball Security": 0,
                                 "Pass": 0,
                                 "Speed": 0,
                                 "Quickness": 0,
                                 "Low Post Defense": 0,
                                 "Strength": 0,
                                 "Hustle": 0,
                                 "Block": 0,
                                 "Steal": 0,
                                 "On Ball Defense": 0,
                                 "Offensive Rebound": 0,
                                 "Defensive Rebound": 0,
                                 "Defensive Awareness": 0,
                                 "Shot Inside": 0,
                                 "Dunk": 0,
                                 "Standing Dunk": 0,
                                 "Vertical": 0,
                                 "Free Throw": 0,
                                 "Stamina": 0,
                                 "Durability": 0,
                                 "Potential": 0,
                                 "Shot Close": 0,
                                 "Layup": 0,
                                 "Post Fadeaway": 0,
                                 "Post Hook": 0,
                                 "Low Post Offense": 0,
                                 "Shot Medium": 0,
                                 "Shot Three Point": 0,
                                 "Shoot In Traffic": 0,
                                 "Shoot Off Dribble": 0,
                                 "Consistency": 0}
            self.statsRarity = {"Off Hand Dribbling": "Common",
                                "Hands": "Common",
                                "Offensive Awareness": "Common",
                                "Ball Handling": "Common",
                                "Ball Security": "Common",
                                "Pass": "Common",
                                "Speed": "Common",
                                "Quickness": "Common",
                                "Low Post Defense": "Common",
                                "Strength": "Common",
                                "Hustle": "Common",
                                "Block": "Common",
                                "Steal": "Common",
                                "On Ball Defense": "Common",
                                "Offensive Rebound": "Common",
                                "Defensive Rebound": "Common",
                                "Defensive Awareness": "Common",
                                "Shot Inside": "Common",
                                "Dunk": "Common",
                                "Standing Dunk": "Common",
                                "Vertical": "Common",
                                "Free Throw": "Common",
                                "Stamina": "Common",
                                "Durability": "Common",
                                "Potential": "Common",
                                "Shot Close": "Common",
                                "Layup": "Common",
                                "Post Fadeaway": "Common",
                                "Post Hook": "Common",
                                "Low Post Offense": "Common",
                                "Shot Medium": "Common",
                                "Shot Three Point": "Common",
                                "Shoot In Traffic": "Common",
                                "Shoot Off Dribble": "Common",
                                "Consistency": "Common"}

            self.isCursedList = []
            self.isBlessedList = []



        #isCursedList = []
        #isBlessedList = []
        # This method reads a single enchantmentArray into the stats dict, and
        # effects the stats accordingly.
        def readEnchantment(self,enchantmentArray):

            enchantmentType = enchantmentArray[0]
            item1 = enchantmentArray[1]
            item2 = enchantmentArray[2]

            if(enchantmentType == 1):
                currentStatValue = self.get(item1)
                newStatValue = currentStatValue + item2

                self.set(item1,newStatValue)
                self.isBlessedList.append(item1)
            elif (enchantmentType == 2):
                totalValueToSpread = item2

                while (totalValueToSpread > 0):
                    randomStat = item1[random.randrange(0,len(item1))]
                    currentStatValue = self.get(randomStat)
                    self.set(randomStat,currentStatValue + 1)

                    totalValueToSpread += -1

                for i in item1:
                    self.isBlessedList.append(i)
            elif (enchantmentType == 3):
                primaryStatValue = self.get(item2)
                self.set(item1,primaryStatValue)

                self.isBlessedList.append(item1)
            elif (enchantmentType == 4):
                currentStatValue = self.get(item1)
                newStatValue = currentStatValue + item2

                self.set(item1, newStatValue)
                self.isCursedList.append(item1)
            elif (enchantmentType == 5):
                totalValueToSpread = item2

                while (totalValueToSpread < 0):
                    randomStat = item1[random.randrange(0, len(item1))]
                    currentStatValue = self.get(randomStat)
                    self.set(randomStat, currentStatValue - 1)

                    totalValueToSpread += 1

                for i in item1:
                    self.isCursedList.append(i)
            elif (enchantmentType == 6):
                randomStatValue1 = self.get(item1)
                randomStatValue2 = self.get(item2)

                if(randomStatValue1 > randomStatValue2):
                    valueToSet = randomStatValue2

                else:
                    valueToSet = randomStatValue1

                self.set(item1,valueToSet)
                self.set(item2,valueToSet)

                self.isCursedList.append(item1)
                self.isCursedList.append(item2)

    # This method simply picks a play style based on the player's archetype
    # and stats.
    def genPlayStyle(self):

        potentialStyles = []

        if(self.archetypeName == "Slayer"):

            # All positions have access to the three basic styles: All Around, Athletic, and Defensive.
            potentialStyles += [7,9,11]

            # All Slayers have "Scoring" available.
            potentialStyles.append(6)

            # Test if the Slayer should have "Slashing" available.
            if(self.stats.get("Dunk") >= 80 or self.stats.get("Layup") >= 75):
                potentialStyles.append(10)

            # Test if the Slayer should have "3pt Specialist" available.
            if(self.stats.get("Shot Three Point") >= 80):
                potentialStyles.append(8)
        elif(self.archetypeName == "Vigilante"):

            # All positions have access to the three basic styles: All Around, Athletic, and Defensive.
            potentialStyles += [13,15,18]

            # All Vigilantes have "Scoring" available.
            potentialStyles.append(12)

            # Test if the Vigilante should have "Slashing" available.
            if (self.stats.get("Dunk") >= 80 or self.stats.get("Layup") >= 75):
                potentialStyles.append(16)

            # Test if the Vigilante should have "3pt Specialist" available.
            if (self.stats.get("Shot Three Point") >= 80):
                potentialStyles.append(14)

            # Vigilantes will NOT have "Point Forward" available.
        elif(self.archetypeName == "Medic"):
            # All positions have access to the three basic styles: All Around, Athletic, and Defensive.
            # Medics have all Back to Basket, Faceup, and Rebounding available by default.
            potentialStyles += [25,26,30,27,28,29]
        elif(self.archetypeName == "Guardian"):
            # All positions have access to the three basic styles: All Around, Athletic, and Defensive.
            # Guardians have all Back to Basket, Faceup, and Rebounding available by default.
            potentialStyles += [19,20,24,21,22,23]
        elif(self.archetypeName == "Engineer"):

            # All positions have access to the three basic styles: All Around, Athletic, and Defensive.
            potentialStyles += [2,4,5]

            # Test if Engineer should have "Pass First" available.
            if(self.stats.get("Pass") >= 85):
                potentialStyles.append(0)

            # Engineers will never have "Scoring" or "3pt Specialist" available.
        elif(self.archetypeName == "Director"):

            # All positions have access to the three basic styles: All Around, Athletic, and Defensive.
            potentialStyles += [2, 4, 5]

            # Test if Director should have "Pass First" available.
            if (self.stats.get("Pass") >= 85):
                potentialStyles.append(0)

            # Test if Director should have "Scoring" available.
            if(self.stats.get("Shot Medium") >= 80 or self.stats.get("Shot Close") >= 90):
                potentialStyles.append(4)

            # Test if Director should have "3pt Specialist" available.
            if(self.stats.get("Shot Three Point") >= 80):
                potentialStyles.append(1)


        self.playStyle = potentialStyles[random.randrange(0,len(potentialStyles))]

    # This class stores and generates all values pertaining to tendencies.
    class TendencyDict:

        # Holds all tendency values.
        # allTendencies = {}

        def __init__(self):
            self.allTendencies = {}

        # This method generates all tendencies for the tendencyDict, based on value ranges
        # specified in the Archetypes.
        def genTendencies(self,archetype):

            self.allTendencies["t_ShotTnd"] = random.randrange(archetype.t_ShotTnd[0],archetype.t_ShotTnd[1]+1)
            self.allTendencies["t_InsideShot"] = random.randrange(archetype.t_InsideShot[0],archetype.t_InsideShot[1]+1)
            self.allTendencies["t_CloseShot"] = random.randrange(archetype.t_CloseShot[0],archetype.t_CloseShot[1]+1)
            self.allTendencies["t_MidShot"] = random.randrange(archetype.t_MidShot[0],archetype.t_MidShot[1]+1)
            self.allTendencies["t_ShotThreePt"] = random.randrange(archetype.t_ShotThreePt[0],archetype.t_ShotThreePt[1]+1)
            self.allTendencies["t_DriveLane"] = random.randrange(archetype.t_DriveLane[0],archetype.t_DriveLane[1]+1)
            self.allTendencies["t_DriveRight"] = random.randrange(archetype.t_DriveRight[0],archetype.t_DriveRight[1]+1)
            self.allTendencies["t_PullUp"] = random.randrange(archetype.t_PullUp[0],archetype.t_PullUp[1]+1)
            self.allTendencies["t_PumpFake"] = random.randrange(archetype.t_PumpFake[0],archetype.t_PumpFake[1]+1)
            self.allTendencies["t_TripleThreat"] = random.randrange(archetype.t_TripleThreat[0],archetype.t_TripleThreat[1]+1)
            self.allTendencies["t_NoTripleThreat"] = random.randrange(archetype.t_NoTripleThreat[0],archetype.t_NoTripleThreat[1]+1)
            self.allTendencies["t_TripleThreatShot"] = random.randrange(archetype.t_TripleThreatShot[0],archetype.t_TripleThreatShot[1]+1)
            self.allTendencies["t_Sizeup"] = random.randrange(archetype.t_Sizeup[0],archetype.t_Sizeup[1]+1)
            self.allTendencies["t_Hesitation"] = random.randrange(archetype.t_Hesitation[0],archetype.t_Hesitation[1]+1)
            self.allTendencies["t_StraightDribble"] = random.randrange(archetype.t_StraightDribble[0],archetype.t_StraightDribble[1]+1)
            self.allTendencies["t_Crossover"] = random.randrange(archetype.t_Crossover[0],archetype.t_Crossover[1]+1)
            self.allTendencies["t_Spin"] = random.randrange(archetype.t_Spin[0],archetype.t_Spin[1]+1)
            self.allTendencies["t_Stepback"] = random.randrange(archetype.t_Stepback[0],archetype.t_Stepback[1]+1)
            self.allTendencies["t_Halfspin"] = random.randrange(archetype.t_Halfspin[0],archetype.t_Halfspin[1]+1)
            self.allTendencies["t_DoubleCrossover"] = random.randrange(archetype.t_DoubleCrossover[0],archetype.t_DoubleCrossover[1]+1)
            self.allTendencies["t_BehindBack"] = random.randrange(archetype.t_BehindBack[0],archetype.t_BehindBack[1]+1)
            self.allTendencies["t_HesitationCrossover"] = random.randrange(archetype.t_HesitationCross[0],archetype.t_HesitationCross[1]+1)
            self.allTendencies["t_InNOut"] = random.randrange(archetype.t_InNOut[0],archetype.t_InNOut[1]+1)
            self.allTendencies["t_SimpleDrive"] = random.randrange(archetype.t_SimpleDrive[0],archetype.t_SimpleDrive[1]+1)
            self.allTendencies["t_Attack"] = random.randrange(archetype.t_Attack[0],archetype.t_Attack[1]+1)
            self.allTendencies["t_PassOut"] = random.randrange(archetype.t_PassOut[0],archetype.t_PassOut[1]+1)
            self.allTendencies["t_Hopstep"] = random.randrange(archetype.t_Hopstep[0],archetype.t_Hopstep[1]+1)
            self.allTendencies["t_SpinLayup"] = random.randrange(archetype.t_SpinLayup[0],archetype.t_SpinLayup[1]+1)
            self.allTendencies["t_Eurostep"] = random.randrange(archetype.t_Eurostep[0],archetype.t_Eurostep[1]+1)
            self.allTendencies["t_Runner"] = random.randrange(archetype.t_Runner[0],archetype.t_Runner[1]+1)
            self.allTendencies["t_Fadeaway"] = random.randrange(archetype.t_Fadeaway[0],archetype.t_Fadeaway[1]+1)
            self.allTendencies["t_Dunk"] = random.randrange(archetype.t_Dunk[0],archetype.t_Dunk[1]+1)
            self.allTendencies["t_Crash"] = random.randrange(archetype.t_Crash[0],archetype.t_Crash[1]+1)
            self.allTendencies["t_Touches"] = random.randrange(archetype.t_Touches[0],archetype.t_Touches[1]+1)
            self.allTendencies["t_UsePick"] = random.randrange(archetype.t_UsePick[0],archetype.t_UsePick[1]+1)
            self.allTendencies["t_SetPick"] = random.randrange(archetype.t_SetPick[0],archetype.t_SetPick[1]+1)
            self.allTendencies["t_Isolation"] = random.randrange(archetype.t_Isolation[0],archetype.t_Isolation[1]+1)
            self.allTendencies["t_UseOffBallScreen"] = random.randrange(archetype.t_UseOffBallScreen[0],archetype.t_UseOffBallScreen[1]+1)
            self.allTendencies["t_SetOffBallScreen"] = random.randrange(archetype.t_SetOffBallScreen[0],archetype.t_SetOffBallScreen[1]+1)
            self.allTendencies["t_PostUp"] = random.randrange(archetype.t_PostUp[0],archetype.t_PostUp[1]+1)
            self.allTendencies["t_SpotUp"] = random.randrange(archetype.t_SpotUp[0],archetype.t_SpotUp[1]+1)
            self.allTendencies["t_PostSpin"] = random.randrange(archetype.t_PostSpin[0],archetype.t_PostSpin[1]+1)
            self.allTendencies["t_DropStep"] = random.randrange(archetype.t_DropStep[0],archetype.t_DropStep[1]+1)
            self.allTendencies["t_Shimmy"] = random.randrange(archetype.t_Shimmy[0],archetype.t_Shimmy[1]+1)
            self.allTendencies["t_FaceUp"] = random.randrange(archetype.t_FaceUp[0],archetype.t_LeavePost[1]+1)
            self.allTendencies["t_LeavePost"] = random.randrange(archetype.t_LeavePost[0],archetype.t_LeavePost[1]+1)
            self.allTendencies["t_BackDown"] = random.randrange(archetype.t_BackDown[0],archetype.t_BackDown[1]+1)
            self.allTendencies["t_AggressiveBackDown"] = random.randrange(archetype.t_AggressiveBackDown[0],archetype.t_AggressiveBackDown[1]+1)
            self.allTendencies["t_PostShot"] = random.randrange(archetype.t_PostShot[0],archetype.t_PostShot[1]+1)
            self.allTendencies["t_PostHook"] = random.randrange(archetype.t_PostHook[0],archetype.t_PostHook[1]+1)
            self.allTendencies["t_PostFade"] = random.randrange(archetype.t_PostFade[0],archetype.t_PostFade[1]+1)
            self.allTendencies["t_PostDrive"] = random.randrange(archetype.t_PostDrive[0],archetype.t_PostDrive[1]+1)
            self.allTendencies["t_HopShot"] = random.randrange(archetype.t_HopShot[0],archetype.t_HopShot[1]+1)
            self.allTendencies["t_Putback"] = random.randrange(archetype.t_Putback[0],archetype.t_Putback[1]+1)
            self.allTendencies["t_FlashyPass"] = random.randrange(archetype.t_FlashyPass[0],archetype.t_FlashyPass[1]+1)
            self.allTendencies["t_AlleyOop"] = random.randrange(archetype.t_AlleyOop[0],archetype.t_AlleyOop[1]+1)
            self.allTendencies["t_DrawFoul"] = random.randrange(archetype.t_DrawFoul[0],archetype.t_DrawFoul[1]+1)
            self.allTendencies["t_PlayPassLane"] = random.randrange(archetype.t_PlayPassLane[0],archetype.t_PlayPassLane[1]+1)
            self.allTendencies["t_TakeCharge"] = random.randrange(archetype.t_TakeCharge[0],archetype.t_TakeCharge[1]+1)
            self.allTendencies["t_OnBallSteal"] = random.randrange(archetype.t_OnBallSteal[0],archetype.t_OnBallSteal[1]+1)
            self.allTendencies["t_Contest"] = random.randrange(archetype.t_Contest[0],archetype.t_Contest[1]+1)
            self.allTendencies["t_CommitFoul"] = random.randrange(archetype.t_CommitFoul[0],archetype.t_CommitFoul[1]+1)
            self.allTendencies["t_HardFoul"] = random.randrange(archetype.t_HardFoul[0],archetype.t_HardFoul[1]+1)
            self.allTendencies["t_UseGlass"] = random.randrange(archetype.t_UseGlass[0],archetype.t_UseGlass[1]+1)
            self.allTendencies["t_StepbackJumper"] = random.randrange(archetype.t_StepbackJumper[0],archetype.t_StepbackJumper[1]+1)
            self.allTendencies["t_SpinJumper"] = random.randrange(archetype.t_SpinJumper[0],archetype.t_SpinJumper[1]+1)
            self.allTendencies["t_StepThrough"] = random.randrange(archetype.t_StepThrough[0],archetype.t_StepThrough[1]+1)
            self.allTendencies["t_ThrowAlleyOop"] = random.randrange(archetype.t_ThrowAlleyOop[0],archetype.t_ThrowAlleyOop[1]+1)
            self.allTendencies["t_GiveNGo"] = random.randrange(archetype.t_GiveNGo[0],archetype.t_GiveNGo[1]+1)


        def get(self,tendencyName):
            return self.allTendencies.get(tendencyName)
    def genTendencyDict(self):
        tendencyDict = self.TendencyDict()
        tendencyDict.genTendencies(self.archetype)

        self.tendencies = tendencyDict

    # This class stores and generates all values pertaining to hotspots.
    class HotspotDict:

        def __init__(self):
            self.allHotspots = {}


        def genHotspots(self,archetype):
            archetype.generateHotspotValues()

            self.allHotspots["HIso3PLft"] = archetype.HIso3PLft
            self.allHotspots["HIso3PCtr"] = archetype.HIso3PCtr
            self.allHotspots["HIso3PRgt"] = archetype.HIso3PRgt
            self.allHotspots["HIsoHPLft"] = archetype.HIsoHPLft
            self.allHotspots["HIsoHPCtr"] = archetype.HIsoHPCtr
            self.allHotspots["HIsoHPRgt"] = archetype.HIsoHPRgt
            self.allHotspots["HP_rLCrnr"] = archetype.HP_rLCrnr
            self.allHotspots["HP_rLWing"] = archetype.HP_rLWing
            self.allHotspots["HP_rTopOA"] = archetype.HP_rTopOA
            self.allHotspots["HP_rRWing"] = archetype.HP_rRWing
            self.allHotspots["HP_rRCrnr"] = archetype.HP_rRCrnr
            self.allHotspots["HSpt3PLCr"] = archetype.HSpt3PLCr
            self.allHotspots["HSpt3PLWg"] = archetype.HSpt3PLWg
            self.allHotspots["HSpt3PTop"] = archetype.HSpt3PTop
            self.allHotspots["HSpt3PRWg"] = archetype.HSpt3PRWg
            self.allHotspots["HSpt3PRCr"] = archetype.HSpt3PRCr
            self.allHotspots["HSptMdLBl"] = archetype.HSptMdLBl
            self.allHotspots["HSptMdLWg"] = archetype.HSptMdLWg
            self.allHotspots["HSptMdCtr"] = archetype.HSptMdCtr
            self.allHotspots["HSptMdRWg"] = archetype.HSptMdRWg
            self.allHotspots["HSptMdRBl"] = archetype.HSptMdRBl
            self.allHotspots["HPstRHigh"] = archetype.HPstRHigh
            self.allHotspots["HPstRLow"] = archetype.HPstRLow
            self.allHotspots["HPstLHigh"] = archetype.HPstLHigh
            self.allHotspots["HPstLLow"] = archetype.HPstLLow

        def get(self,hotspotName):
            return self.allHotspots.get(hotspotName)
    def genHotspotDict(self):
        self.hotspots.genHotspots(self.archetype)

    # This class stores and generates all values pertaining to hotzones.
    # By default, ALL players have neutral zones for each, unless given
    # an artifact.
    class HotzoneDict:

        def __init__(self):
            self.allHotzones = {}


        def genHotzones(self,archetype):

            self.allHotzones["HZ1"]  = random.randrange(archetype.HZ1[0],archetype.HZ1[1]+1)
            self.allHotzones["HZ2"]  = random.randrange(archetype.HZ2[0],archetype.HZ2[1]+1)
            self.allHotzones["HZ3"]  = random.randrange(archetype.HZ3[0],archetype.HZ3[1]+1)
            self.allHotzones["HZ4"]  = random.randrange(archetype.HZ4[0],archetype.HZ4[1]+1)
            self.allHotzones["HZ5"]  = random.randrange(archetype.HZ5[0],archetype.HZ5[1]+1)
            self.allHotzones["HZ6"]  = random.randrange(archetype.HZ6[0],archetype.HZ6[1]+1)
            self.allHotzones["HZ7"]  = random.randrange(archetype.HZ7[0],archetype.HZ7[1]+1)
            self.allHotzones["HZ8"]  = random.randrange(archetype.HZ8[0],archetype.HZ8[1]+1)
            self.allHotzones["HZ9"]  = random.randrange(archetype.HZ9[0],archetype.HZ9[1]+1)
            self.allHotzones["HZ10"] = random.randrange(archetype.HZ10[0],archetype.HZ10[1]+1)
            self.allHotzones["HZ11"] = random.randrange(archetype.HZ11[0],archetype.HZ11[1]+1)
            self.allHotzones["HZ12"] = random.randrange(archetype.HZ12[0],archetype.HZ12[1]+1)
            self.allHotzones["HZ13"] = random.randrange(archetype.HZ13[0],archetype.HZ13[1]+1)
            self.allHotzones["HZ14"] = random.randrange(archetype.HZ14[0],archetype.HZ14[1]+1)

        def get(self,hotzoneName):
            return self.allHotzones.get(hotzoneName)
    def genHotzoneDict(self):
        self.hotzones.genHotzones(self.archetype)

    # This method generates initial statistics for the Player object based
    # on the 'archetype' variable.
    def genInitialArchStats(self):

        newStats = self.StatsDict()

        newStats.set("Off Hand Dribbling",random.randrange(self.archetype.skill_OffHandDribbling[0],self.archetype.skill_OffHandDribbling[1]+1))
        newStats.set("Hands", random.randrange(self.archetype.skill_Hands[0],self.archetype.skill_Hands[1]+1))
        newStats.set("Offensive Awareness",random.randrange(self.archetype.skill_OffensiveAwareness[0],self.archetype.skill_OffensiveAwareness[1]+1))
        newStats.set("Ball Handling",random.randrange(self.archetype.skill_BallHandling[0],self.archetype.skill_BallHandling[1]+1))
        newStats.set("Ball Security",random.randrange(self.archetype.skill_BallSecurity[0],self.archetype.skill_BallSecurity[1]+1))
        newStats.set("Pass", random.randrange(self.archetype.skill_Pass[0],self.archetype.skill_Pass[1]+1))
        newStats.set("Speed", random.randrange(self.archetype.skill_Speed[0],self.archetype.skill_Speed[1]+1))
        newStats.set("Quickness", random.randrange(self.archetype.skill_Quickness[0],self.archetype.skill_Quickness[1]+1))
        newStats.set("Low Post Defense",random.randrange(self.archetype.skill_LowPostDefense[0],self.archetype.skill_LowPostDefense[1]+1))
        newStats.set("Strength", random.randrange(self.archetype.skill_Strength[0],self.archetype.skill_Strength[1]+1))
        newStats.set("Hustle", random.randrange(self.archetype.skill_Hustle[0],self.archetype.skill_Hustle[1]+1))
        newStats.set("Block", random.randrange(self.archetype.skill_Block[0],self.archetype.skill_Block[1]+1))
        newStats.set("Steal", random.randrange(self.archetype.skill_Steal[0],self.archetype.skill_Steal[1]+1))
        newStats.set("On Ball Defense",random.randrange(self.archetype.skill_OnBallDefense[0],self.archetype.skill_OnBallDefense[1]+1))
        newStats.set("Offensive Rebound",random.randrange(self.archetype.skill_OffensiveRebound[0],self.archetype.skill_OffensiveRebound[1]+1))
        newStats.set("Defensive Rebound",random.randrange(self.archetype.skill_DefensiveRebound[0],self.archetype.skill_DefensiveRebound[1]+1))
        newStats.set("Defensive Awareness",random.randrange(self.archetype.skill_DefensiveAwareness[0],self.archetype.skill_DefensiveAwareness[1]+1))
        newStats.set("Shot Inside",random.randrange(self.archetype.skill_ShotInside[0],self.archetype.skill_ShotInside[1]+1))
        newStats.set("Dunk", random.randrange(self.archetype.skill_Dunk[0],self.archetype.skill_Dunk[1]+1))
        newStats.set("Standing Dunk",random.randrange(self.archetype.skill_StandingDunk[0],self.archetype.skill_StandingDunk[1]+1))
        newStats.set("Vertical", random.randrange(self.archetype.skill_Vertical[0],self.archetype.skill_Vertical[1]+1))
        newStats.set("Free Throw", random.randrange(self.archetype.skill_FreeThrow[0],self.archetype.skill_FreeThrow[1]+1))
        newStats.set("Stamina", random.randrange(self.archetype.skill_Stamina[0],self.archetype.skill_Stamina[1]+1))
        newStats.set("Durability",random.randrange(self.archetype.skill_Durability[0],self.archetype.skill_Durability[1]+1))
        newStats.set("Potential", random.randrange(self.archetype.skill_Potential[0],self.archetype.skill_Potential[1]+1))
        newStats.set("Shot Close", random.randrange(self.archetype.skill_ShotClose[0],self.archetype.skill_ShotClose[1]+1))
        newStats.set("Layup", random.randrange(self.archetype.skill_Layup[0],self.archetype.skill_Layup[1]+1))
        newStats.set("Post Fadeaway",random.randrange(self.archetype.skill_PostFadeaway[0],self.archetype.skill_PostFadeaway[1]+1))
        newStats.set("Post Hook", random.randrange(self.archetype.skill_PostHook[0],self.archetype.skill_PostHook[1]+1))
        newStats.set("Low Post Offense",random.randrange(self.archetype.skill_LowPostOffense[0],self.archetype.skill_LowPostOffense[1]+1))
        newStats.set("Shot Medium",random.randrange(self.archetype.skill_ShotMedium[0],self.archetype.skill_ShotMedium[1]+1))
        newStats.set("Shot Three Point",random.randrange(self.archetype.skill_ShotThreePt[0],self.archetype.skill_ShotThreePt[1]+1))
        newStats.set("Shoot In Traffic",random.randrange(self.archetype.skill_ShootInTraffic[0],self.archetype.skill_ShootInTraffic[1]+1))
        newStats.set("Shoot Off Dribble",random.randrange(self.archetype.skill_ShootOffDribble[0],self.archetype.skill_ShootOffDribble[1]+1))
        newStats.set("Consistency",random.randrange(self.archetype.skill_Consistency[0],self.archetype.skill_Consistency[1]+1))

        self.stats = newStats

    # This variable and class manage the 'rarity' aspect of a player. Rarities
    # can range from Common, Rare, Epic, Legendary, to Godlike. Higher rarities
    # give extra stat bonuses and unlock access to more skill cards.
    class Rarity:

        # The archetype of the player.
        archetype = None

        # This dictionary stores the ranges of stat increases
        # available by each rarity.
        rarityRanges = {"Rare": [1, 6],
                        "Epic": [6, 10],
                        "Legendary": [10, 15],
                        "Godlike": [10, 25]}
        raritySkillCardRanges = {"Common" : [0,0],
                                "Rare" : [1,2],
                                 "Epic" : [2,3],
                                 "Legendary" : [3,5],
                                 "Godlike" : [5,5]}

        # These are the chances for various rarities to occur.
        rareChance = float(b.readConfigValue("rareChance"))
        epicChance = float(b.readConfigValue("epicChance"))
        legendaryChance = float(b.readConfigValue("legendaryChance"))
        godlikeChance = float(b.readConfigValue("godlikeChance"))

        # This represents the actual rarity of this player.
        localRarity = None

        # Simple initialization method only requires an archetype object.
        def __init__(self, _archetype):
            self.archetype = _archetype
            self.bonusArray = []
            self.skillCardsArray = []

        # Simply str method to print the rarity name and nothing else.
        def __str__(self):
            return self.localRarity

        # Simply randomly assigns a local rarity
        def genLocalRarity(self):
            rareRange = 1 - self.rareChance
            epicRange = rareRange - self.epicChance
            legendaryRange = epicRange - self.legendaryChance
            godlikeRange = legendaryRange - self.godlikeChance

            rarityRoll = random.uniform(0, 1)
            if (1 > rarityRoll > rareRange):
                self.localRarity = "Rare"
            elif (rareRange > rarityRoll > epicRange):
                self.localRarity = "Epic"
            elif (epicRange > rarityRoll > legendaryRange):
                self.localRarity = "Legendary"
            elif (legendaryRange > rarityRoll > godlikeRange):
                self.localRarity = "Godlike"
            else:
                self.localRarity = "Common"

        # This method will generate a 2D array of stat bonus arrays,
        # based on the archetype of this Rarity object.
        bonusArray = []

        # This method randomly generates a rarity array, intended to
        # be injected into a StatsDict object. The rarity array will
        # contain information about rarities, skill names, and bonus
        # values.
        def genStatBonuses(self):
            coreStats = []
            for i in self.archetype.coreSkills:
                coreStats.append(i)

            rarityArray = []
            if (self.localRarity == "Rare"):
                rarityArray.append("Rare")
            if (self.localRarity == "Epic"):
                rarityArray.append("Rare")
                rarityArray.append("Epic")
            if (self.localRarity == "Legendary"):
                rarityArray.append("Rare")
                rarityArray.append("Epic")
                rarityArray.append("Legendary")
            if (self.localRarity == "Godlike"):
                rarityArray.append("Rare")
                rarityArray.append("Epic")
                rarityArray.append("Legendary")
                rarityArray.append("Godlike")

            fixedLength = len(rarityArray)
            bonusNumber = len(rarityArray)
            coreNumber = 6
            finalBonusArray = []
            for i in range(fixedLength):
                randomStat = coreStats[random.randrange(0, coreNumber)]
                randomRarity = rarityArray[random.randrange(0, bonusNumber)]

                coreStats.remove(randomStat)
                rarityArray.remove(randomRarity)

                bonusRange = self.rarityRanges.get(randomRarity)
                randomBonus = random.randrange(bonusRange[0], bonusRange[1])

                nextStatBonus = [randomStat, randomRarity, randomBonus]
                finalBonusArray.append(nextStatBonus)
                bonusNumber = bonusNumber - 1
                coreNumber = coreNumber - 1
            self.bonusArray = finalBonusArray

        # This method generates a random number of skill cards according
        # to localRating.
        def genSkillCards(self):
            skillCardsRange = self.raritySkillCardRanges.get(self.localRarity)
            minimum = skillCardsRange[0]
            maximum = skillCardsRange[1] + 1

            numberOfCards = random.randrange(minimum,maximum)
            availableSkillCardList = []
            for i in self.archetype.availableSkillCards:
                availableSkillCardList.append(i)

            skillCards = []
            for i in range(numberOfCards):
                randomCard = availableSkillCardList[random.randrange(0,len(availableSkillCardList))]
                skillCards.append(randomCard)

                availableSkillCardList.remove(randomCard)

            requiredNones = 5 - len(skillCards)
            for i in range(requiredNones):
                skillCards.append(0)



            self.skillCardsArray = skillCards
        # This array stores information about the skill cards that this rarity randomly
        # generated.
        skillCardsArray = []
    # This method randomly generates rarity information for this Player object,
    # as well as injects stat bonuses into the stats StatsDict.
    def genRarityInformation(self):
        self.playerRarity = self.Rarity(self.archetype)
        self.playerRarity.genLocalRarity()
        self.playerRarity.genStatBonuses()

        bonusArray = self.playerRarity.bonusArray
        for i in bonusArray:
            self.stats.addRarityBonus(i[0], i[1], i[2])

        self.playerRarity.genSkillCards()
        self.skillCards = self.playerRarity.skillCardsArray

    # A class, member, and method for dealing with enchantments (blessings/curses).
    class Enchantment:
        
        def __init__(self):
            self.enchantmentType = 0
            self.item1 = None
            self.item2 = None
            self.priority = 0



        
        
        # An enchantment array differs depending on its type. These are the following
        # types:
        #
        # [1,"Primary/Secondary Stat",###] Boosts the stat by the number. (Divine Strength)
        # [2,["Primary/Secondary Stat 1","Primary/Secondary Stat 2", ...],###] Randomly distributed the # among the stat array. (Divine Wisdom)
        # [3,"Non-Primary Stat","Primary Stat"] Copies the value of a Primary stat to a Non-Primary Stat. (Divine Grace)
        # [4, "Primary Stat",###] Reduces the stat by the number. (Pestilent Weakness)
        # [5, ["Primary/Secondary Stat 1","Primary/Secondary Stat 2", ...],###] Randomly distributes the -# among the stat array. (Pestilent Ignorance)
        # [6,"Random Stat 1","Random Stat 2"] Selects two random stats, and sets both stats to the value of the lesser stat. (Pestinlent Indolence)
        enchantmentType = 0
        item1 = None
        item2 = None

        # Generates a random enchantment. If type is 0, curse/blessing will be picked randomly. If type is 1,
        # enchantment will be a blessing. If type is 2, enchantment will be a curse.
        def genRandomEnchantmentType(self,type = 0):

            if(type == 0):
                enchantArray = [1,2,3,4,5,6]
            elif(type == 1):
                enchantArray = [1,2,3]
            elif(type == 2):
                enchantArray = [4,5,6]


            enchantmentType = enchantArray[random.randrange(0,len(enchantArray))]
            self.enchantmentType = enchantmentType

        # This method populates the enchantmentArray with the necessary information.
        def genEnchantmentInformation(self,archetype):

            if(self.enchantmentType == 1):
                possibleStats = archetype.primaryStats + archetype.secondaryStats
                randomStat = possibleStats[random.randrange(0,len(possibleStats))]

                self.item1 = randomStat
                self.item2 = random.randrange(1,15)
            elif(self.enchantmentType == 4):
                possibleStats = archetype.primaryStats + archetype.secondaryStats
                randomStat = possibleStats[random.randrange(0, len(possibleStats))]

                self.item1 = randomStat
                self.item2 = random.randrange(-15, -1)
            elif(self.enchantmentType == 2):
                possibleStats = archetype.primaryStats + archetype.secondaryStats
                numberOfStats = random.randrange(3,7)
                finalStats = []

                for i in range(numberOfStats):
                    randomStat = possibleStats[random.randrange(0, len(possibleStats))]
                    finalStats.append(randomStat)

                self.item1 = finalStats
                self.item2 = random.randrange(10,25)
            elif (self.enchantmentType == 5):
                possibleStats = archetype.primaryStats + archetype.secondaryStats
                numberOfStats = random.randrange(3, 7)
                finalStats = []

                for i in range(numberOfStats):
                    randomStat = possibleStats[random.randrange(0, len(possibleStats))]
                    finalStats.append(randomStat)

                self.item1 = finalStats
                self.item2 = random.randrange(-25, -10)
            elif(self.enchantmentType == 3):
                possibleNonPrimaryStats = archetype.tertiaryStats + archetype.secondaryStats
                possiblePrimaryStats = archetype.primaryStats

                nonPrimaryStat = possibleNonPrimaryStats[random.randrange(0, len(possibleNonPrimaryStats))]
                primaryStat = possiblePrimaryStats[random.randrange(0, len(possiblePrimaryStats))]

                self.item1 = nonPrimaryStat
                self.item2 = primaryStat
            elif(self.enchantmentType == 6):
                possibleFirstStats = archetype.primaryStats + archetype.secondaryStats
                possibleSecondStats = archetype.secondaryStats + archetype.tertiaryStats

                randomStat1 = possibleFirstStats[random.randrange(0, len(possibleFirstStats))]

                while True:
                    randomStat2 = possibleSecondStats[random.randrange(0, len(possibleSecondStats))]
                    if(randomStat2 == randomStat1):
                        continue
                    else:
                        break

                self.item1 = randomStat1
                self.item2 = randomStat2

        # This simple method sets a priority for this enchantment, so that it is applied
        # in the correct order.
        def genPriority(self):

            if(self.enchantmentType == 1):
                self.priorty = 1
            elif (self.enchantmentType == 2):
                self.priorty = 3
            elif (self.enchantmentType == 3):
                self.priorty = 6
            elif (self.enchantmentType == 4):
                self.priorty = 2
            elif (self.enchantmentType == 5):
                self.priorty = 4
            elif (self.enchantmentType == 6):
                self.priorty = 5
        priority = 0

        # Converts the entire object to an array.
        def convertToArray(self):
            return [self.enchantmentType, self.item1, self.item2,self.priority]

        # Methods to generate a complete curse/blessing.
        def genCurse(self,archetype):
            self.genRandomEnchantmentType(2)
            self.genEnchantmentInformation(archetype)
            self.genPriority()

            return self.convertToArray()
        def genBlessing(self,archetype):
            self.genRandomEnchantmentType(1)
            self.genEnchantmentInformation(archetype)
            self.genPriority()

            return self.convertToArray()
    def generateArrayOfEnchantments(self):

        listOfPriorities = []


        COMMON_CHANCE_FOR_ONE = float(b.readConfigValue("commonChanceForOne"))
        COMMON_CHANCE_FOR_TWO = float(b.readConfigValue("commonChanceForTwo"))

        RARE_CHANCE_FOR_ONE = float(b.readConfigValue("rareChanceForOne"))
        RARE_CHANCE_FOR_TWO = float(b.readConfigValue("rareChanceForTwo"))

        EPIC_CHANCE_FOR_ONE = float(b.readConfigValue("epicChanceForOne"))
        EPIC_CHANCE_FOR_TWO = float(b.readConfigValue("epicChanceForTwo"))

        LEGENDARY_CHANCE_FOR_ONE = float(b.readConfigValue("legendaryChanceForOne"))
        LEGENDARY_CHANCE_FOR_TWO = float(b.readConfigValue("legendaryChanceForTwo"))



        if(str(self.playerRarity) == "Common"):
            num = random.uniform(0,1)

            if(num <= COMMON_CHANCE_FOR_ONE and num >= COMMON_CHANCE_FOR_TWO):
                blessingCount = 1
                curseCount = 1
            elif(num <= COMMON_CHANCE_FOR_TWO):
                blessingCount = 2
                curseCount = 2
            else:
                blessingCount = 0
                curseCount = 0
        elif (str(self.playerRarity) == "Rare"):
            num = random.uniform(0, 1)

            if (num <= RARE_CHANCE_FOR_ONE and num >= RARE_CHANCE_FOR_TWO):
                blessingCount = 1
                curseCount = 1
            elif (num <= RARE_CHANCE_FOR_TWO):
                blessingCount = 2
                curseCount = 2
            else:
                blessingCount = 0
                curseCount = 0
        elif (str(self.playerRarity) == "Epic"):
            num = random.uniform(0, 1)

            if (num <= EPIC_CHANCE_FOR_ONE and num >= EPIC_CHANCE_FOR_TWO):
                blessingCount = 1
                curseCount = 1
            elif (num <= EPIC_CHANCE_FOR_TWO):
                blessingCount = 2
                curseCount = 2
            else:
                blessingCount = 0
                curseCount = 0
        elif (str(self.playerRarity) == "Legendary"):
            num = random.uniform(0, 1)

            if (num <= LEGENDARY_CHANCE_FOR_ONE and num >= LEGENDARY_CHANCE_FOR_TWO):
                blessingCount = 1
                curseCount = 1
            elif (num <= LEGENDARY_CHANCE_FOR_TWO):
                blessingCount = 2
                curseCount = 2
            else:
                blessingCount = 0
                curseCount = 0
        elif (str(self.playerRarity) == "Godlike"):
            blessingCount = 2
            curseCount = 1



        for i in range(blessingCount):
            newBlessing = self.Enchantment()
            finalBlessing = newBlessing.genBlessing(self.archetype)
            self.arrayOfEnchantments.append(finalBlessing)

        for i in range(curseCount):
            newCurse = self.Enchantment()
            finalCurse = newCurse.genCurse(self.archetype)
            self.arrayOfEnchantments.append(finalCurse)


        for i in range(len(self.arrayOfEnchantments) - 1):


            for j in range(len(self.arrayOfEnchantments) - i - 1):

                if(self.arrayOfEnchantments[j][3] < self.arrayOfEnchantments[j + 1][3]):
                    self.arrayOfEnchantments[j], self.arrayOfEnchantments[j + 1] = self.arrayOfEnchantments[j + 1], self.arrayOfEnchantments[j]
    # Simple method to read all enchantments generated into the stats dict.
    def readEnchantmentsIntoStats(self):
        for i in self.arrayOfEnchantments:
            self.stats.readEnchantment(i)

    # This variable stores a NameFix object, that points to a player that this
    # Player object will overwrite. It ensures that the overwritten player has
    # exactly the same First and Last name length as this player to avoid
    # conflicts within the roster.
    # This method sets the first and last name for the player, as well as generates
    # the overwritePlayer NameFix object.
    def setName(self,_firstName,_lastName):
        self.firstName = _firstName
        self.lastName = _lastName

    def getName(self):
        returnString = ""
        returnString += self.firstName + " " + self.lastName
        return returnString

    # This class stores information and generation methods for signature moves and
    # shots.
    class Signature:

        SHOTS = {
            "Shooting Form": ["Release 1", "Release 2", "Release 3", "Release 4", "Release 5", "Release 6", "Release 7",
                              "Release 8", "Release 9", "Release 10", "Release 11", "Release 12", "Release 13",
                              "Release 14", "Release 15", "Release 16", "Release 17", "Release 18", "Release 19",
                              "Release 20", "Release 21", "Release 22", "Release 23", "Release 24", "Release 25",
                              "Release 26", "Release 27", "Release 28", "Release 29", "Release 30", "Release 31",
                              "Release 32", "Release 33", "Release 34", "Release 35", "Release 36", "Release 37",
                              "Release 38", "Release 39", "Release 40", "Release 41", "Release 42", "Release 43",
                              "Release 44", "Release 45", "Release 46", "Release 47", "Release 48", "Release 49",
                              "Release 50", "Release 51", "Release 52", "Release 53", "Release 54", "Release 55",
                              "Release 56", "Release 57", "Release 58", "Release 59", "Release 60", "Release 61",
                              "Release 62", "Release 63", "Release 64", "Release 65", "Release 66", "Release 67",
                              "Release 68", "Release 69", "Release 70", "Release 71", "Release 72", "Release 73",
                              "Release 74", "Release 75", "Release 76", "Release 77", "Release 78", "Release 79",
                              "Release 80", "Release 81", "L. Aldridge", "R. Allen", "C. Anthony", "G. Arenas",
                              "A. Bargnani", "D. Barnett", "M. Beasley", "C. Billups", "L. Bird", "A. Bogut",
                              "C. Boozer",
                              "C. Bosh", "K. Bryant", "M. Camby", "V. Carter", "S. Curry", "K. Duckworth", "T. Duncan",
                              "K. Durant", "M. Ellis", "T. Evans", "P. Ewing", "D. Gallinari", "K. Garnett", "P. Gasol",
                              "R. Gay", "M. Ginobili", "D. Granger", "B. Griffin", "D. Howard", "A. Iguodala",
                              "L. James",
                              "J. Johnson", "M. Johnson", "M. Jordan", "J. Kidd", "B. Laimbeer", "D. Lee", "B. Lopez",
                              "K. Love", "K. Malone", "K. Martin", "T. McGrady", "S. Nash", "D. Nowitzki", "S. O'Neal",
                              "C. Oakley", "T. Parker", "C. Paul", "P. Pierce", "Z. Randolph", "A. Rivers",
                              "O. Robertson",
                              "D. Robinson", "D. Rose", "J. Smith", "J. Stockton", "A. Stoudemire", "D. Wade",
                              "D. Waiters",
                              "J. Wall", "G. Wallace", "J. West", "R. Westbrook", "D. Williams", "M. Yao"],
            "Shot Base": ["Jump Shot 1", "Jump Shot 2", "Jump Shot 3", "Jump Shot 4", "Jump Shot 5", "Jump Shot 6",
                          "Jump Shot 7", "Jump Shot 8", "Jump Shot 9", "Jump Shot 10", "Jump Shot 11", "Jump Shot 12",
                          "Jump Shot 13", "Jump Shot 14", "Jump Shot 15", "Jump Shot 16", "Jump Shot 17",
                          "Jump Shot 18",
                          "Jump Shot 19", "Jump Shot 20", "Jump Shot 21", "Jump Shot 22", "Jump Shot 23",
                          "Jump Shot 24",
                          "Jump Shot 25", "Jump Shot 26", "Jump Shot 27", "Jump Shot 28", "Jump Shot 29",
                          "Jump Shot 30",
                          "Jump Shot 31", "Jump Shot 32", "Jump Shot 33", "Jump Shot 34", "Jump Shot 35",
                          "Jump Shot 36",
                          "Jump Shot 37", "Jump Shot 38", "Jump Shot 39", "Jump Shot 40", "Jump Shot 41", "Set Shot 1",
                          "Set Shot 2", "Set Shot 3", "Set Shot 4", "Set Shot 5", "Set Shot 6", "Set Shot 7",
                          "Set Shot 8",
                          "Set Shot 9", "Set Shot 10", "Set Shot 11", "Set Shot 12", "Set Shot 13", "Set Shot 14",
                          "Set Shot 15", "Set Shot 16", "Set Shot 17", "Set Shot 18", "L. Aldridge", "R. Allen",
                          "C. Anthony", "G. Arenas", "A. Bargnani", "D. Barnett", "M. Beasley", "C. Billups", "L. Bird",
                          "A. Bogut", "C. Boozer", "C. Bosh", "K. Bryant", "M. Camby", "V. Carter", "S. Curry",
                          "K. Duckworth", "T. Duncan", "K. Durant", "M. Ellis", "T. Evans", "P. Ewing", "D. Gallinari",
                          "K. Garnett", "P. Gasol", "R. Gay", "M. Ginobili", "D. Granger", "B. Griffin", "D. Howard",
                          "A. Iguodala", "L. James", "J. Johnson", "M. Johnson", "M. Jordan", "J. Kidd", "B. Laimbeer",
                          "D. Lee", "B. Lopez", "K. Love", "K. Malone", "K. Martin", "T. McGrady", "S. Nash",
                          "D. Nowitzki",
                          "S. O'Neal", "C. Oakley", "T. Parker", "C. Paul", "P. Pierce", "Z. Randolph", "A. Rivers",
                          "O. Robertson", "D. Robinson", "D. Rose", "J. Smith", "J. Stockton", "A. Stoudemire",
                          "D. Wade",
                          "D. Waiters", "J. Wall", "G. Wallace", "J. West", "R. Westbrook", "D. Williams", "M. Yao"],
            "Fadeaway": ["J Awkward", "J Big Kick", "J Big Kick 2", "J Big Kick 3", "J Lean", "J Small Kick",
                         "J Small Kick 2", "J Small Kick 3", "J Small Kick 4", "S Big Kick", "S Bowed", "S Grounded",
                         "S Hop Back", "S Kick", "S Late Kick", "S Side Hop", "S Small Kick", "S Small Step",
                         "S. Tight",
                         "K. Bryant", "K. Durant", "L. James", "W. Johnson", "S. Marion", "S. Nash", "D. Nowitzki",
                         "P. Pierce", "D. Rose", "E. Turner", "D. Wade", "M. Yao"],
            "Contested": ["Normal", "Big"],
            "Escape Dribble Pull Up": ["Bowed", "Elite", "Elite 2", "Normal", "One Foot", "Stiff"],
            "Runner": ["Guard Default", "Guard Angled", "Guard Grounded", "Guard High Hold", "Guard High Push",
                       "Guard Hold", "Guard Normal", "Guard Quick Flick", "Guard Quick Release", "Guard Textbook",
                       "Swingman Default", "Swingman Angled", "Swingman Angle Hold", "Swingman Grounded",
                       "Swingman High",
                       "Swingman High Push", "Swingman Hold", "Swingman Straight", "Swingman Quick Release",
                       "Bigman Default", "Bigman Angled", "Bigman Athletic", "Bigman Extend", "Bigman Extend Follow",
                       "Bigman Flick", "Bigman Grounded", "Bigman Hard Flick", "Bigman High Push", "Bigman Hold",
                       "Bigman Textbook", "M. Jordan", "S. Nash", "T. Parker", "C. Paul"]
        }
        MOMENTUM_SHOTS_OUTSIDE = {
            "Dribble Pull Up": ["Big", "Big 2", "Bowed", "Elite", "Elite 2", "Elite 3", "Elite 4", "Elite 5",
                                "Elite 6",
                                "Elite 7", "Elite 8", "Elite 9", "Normal", "Normal 2", "Normal 3", "Normal 4",
                                "Normal 5",
                                "Normal 6", "Normal 7", "Normal 8", "Normal 9", "Normal 10", "One Foot", "Stiff",
                                "Stiff 2", "Stiff 3", "Stiff 4", "Stiff 5", "Stiff 6"],
            "Spin Jumper": ["Big", "Big 2", "Normal", "Normal 2", "Normal 3", "Normal 4", "Normal 5", "Normal 6",
                            "Normal 7", "One Foot", "Stiff", "Stiff 2", "Stiff 3", "Stiff 4"],
            "Hop Jumper": ["Big", "Big 2", "Normal", "Normal 2", "Normal 3", "Normal 4", "Normal 5", "Normal 6",
                           "Normal 7",
                           "Normal 8", "Normal 9", "Normal 10", "One Foot", "Stiff"]}
        POST_SHOTS = {
            "Post Fade": ["Normal", "Fade 2", "Fade 3", "Fade 4", "Fade 5", "Fade 6", "Fade 7", "Fade 8", "Fade 9",
                          "M. Jordan", "K. Malone", "D. Nowitzki"],
            "Post Hook": ["Normal", "Hook 1", "Hook 2", "Hook 3", "Hook 4", "Hook 5", "Hook 6", "Hook 7", "Hook 8",
                          "Hook 9", "Hook 10", "Hook 11", "Classic Sky Hook"],
            "Post Hop Shot": ["Normal", "Big", "Compact", "Crusader", "Deliberate", "Gaucho", "One Foot", "Quick"],
            "Post Shimmy Shot": ["Normal", "Big", "One Foot"],
            "Post Drive Stepback Shot": ["Normal", "Compact", "Deliberate", "Quick"],
            "Post Spin Stepback Shot": ["Normal", "Compact", "Cougar", "Crusader", "Deliberate", "Quick"],
            "Post Protect Shot": ["Normal", "Compact", "One Foot"],
            "Post Protect Spin Shot": ["Normal", "Compact", "Gaucho", "One Foot"]}
        DRIBBLE_MOVES = {
            "ISO Crossover": ["Crossover 1", "Crossover 2", "Crossover 3", "Crossover 4", "Crossover 5", "Crossover 6"],
            "ISO Behind Back": ["Behind Back 1", "Behind Back 2", "Behind Back 3", "Behind Back 4", "Behind Back 5",
                                "Behind Back 6", "Behind Back 7"],
            "ISO Spin": ["Spin 1", "Spin 2", "Spin 3", "Spin 4", "Spin 5", "Spin 6", "Spin 7"],
            "ISO Hesitation": ["Hesitation 1", "Hesitation 2", "Hesitation 3", "Hesitation 4"]}
        DUNKS_AND_LAYUPS = {
            "Layup Package": ["Rookie Guard", "Pro Guard", "All-Star Guard", "J. Crawford", "Classic", "M. Ginobili",
                              "Air Jordan", "K. Bryant", "S. Nash", "T. Parker", "C. Paul", "D. Rose", "R. Rondo",
                              "D. Wade"],
            "Goto Dunk Package": ["Under Basket Rim Pulls","Under Basket Athletic Flushes","Under Basket One Handers",
                                  "Under Basket Bigman Slams","Rim Grazers off one","Rim Grazers off two","Basic One Handers off one",
                                  "Basic Two-Handers Off one","Basic one handers off two","Basic two Handers off two","Athletic One handers Off one",
                                  "Athletic One handers Off two","Hangs off one","Hangs off two","Quick Drops",
                                  "Fist Pump Rim Pulls","Side Arm Tomahawks","Straight Arm Tomahawks","Cock back tomahawks",
                                  "Athletic Side Tomahawks","Athletic Front tomahawks","Uber athletic Tomahawks off one",
                                  "Uber athletic Tomahawks off two","Leaning Slams","Front Clutches","Front Clutches off two",
                                  "Side Clutches off one","Side Clutches off two","Back Scratchers off one","Back Scratchers off two",
                                  "Back Scratchers rim hangs","Quick Drop in BackScratchers","Reverses off one","Reverses off two",
                                  "Clutch reverse off one","Clutch reverse off two","Baseline Clutch reverses","Windmill reverses",
                                  "Switch hand reverses","Baseline reverses off one","Baseline reverses off two","Windmill Baseline reverses",
                                  "Clutch Baseline reverses","Windmills Off one","Leaning Windmills","Front Windmills","Side Windmills",
                                  "Athletic Windmills","Basic 360s","Athletic 360s off one","Athletic 360s off two","Under Leg 360s",
                                  "One hand Spin Dunks","Two Hand Spin Dunks","Cradle Dunks","Flashey Flushes","Historic Jordan","Historic Drexler"],
            "Extra Dunk Packages": []}

        SHOOTING_FORM_IDS = {"Release 1" : 0, "Release 2" : 1, "Release 3" : 2, "Release 4" : 3, "Release 5" : 4, "Release 6" : 5, "Release 7" : 6,
                              "Release 8" : 7, "Release 9" : 8, "Release 10" : 9, "Release 11" : 10, "Release 12" : 11, "Release 13" : 12,
                              "Release 14" : 13, "Release 15" : 14, "Release 16" : 15, "Release 17" : 16, "Release 18" : 17, "Release 19" : 18,
                              "Release 20" : 19, "Release 21" : 20, "Release 22" : 21, "Release 23" : 22, "Release 24" : 23, "Release 25" : 24,
                              "Release 26" : 25, "Release 27" : 26, "Release 28" : 27, "Release 29" : 28, "Release 30" : 29, "Release 31" : 30,
                              "Release 32" : 31, "Release 33" : 32, "Release 34" : 33, "Release 35" : 34, "Release 36" : 35, "Release 37" : 36,
                              "Release 38" : 37, "Release 39" : 38, "Release 40" : 39, "Release 41" : 40, "Release 42" : 41, "Release 43" : 42,
                              "Release 44" : 43, "Release 45" : 44, "Release 46" : 45, "Release 47" : 46, "Release 48" : 47, "Release 49" : 48,
                              "Release 50" : 49, "Release 51" : 50, "Release 52" : 51, "Release 53" : 52, "Release 54" : 53, "Release 55" : 54,
                              "Release 56" : 55, "Release 57" : 56, "Release 58" : 57, "Release 59" : 58, "Release 60" : 59, "Release 61" : 60,
                              "Release 62" : 61, "Release 63" : 62, "Release 64" : 63, "Release 65" : 64, "Release 66" : 65, "Release 67" : 66,
                              "Release 68" : 67, "Release 69" : 68, "Release 70" : 69, "Release 71" : 70, "Release 72" : 71, "Release 73" : 72,
                              "Release 74" : 73, "Release 75" : 74, "Release 76" : 75, "Release 77" : 76, "Release 78" : 77, "Release 79" : 78,
                              "Release 80" : 79, "Release 81" : 80, "L. Aldridge" : 81, "R. Allen" : 82, "C. Anthony" : 83, "G. Arenas" : 84,
                              "A. Bargnani" : 85, "D. Barnett" : 86, "M. Beasley" : 87, "C. Billups" : 88, "L. Bird" : 89, "A. Bogut" : 90,
                              "C. Boozer" : 91,
                              "C. Bosh" : 92, "K. Bryant" : 93, "M. Camby" : 94, "V. Carter" : 95, "S. Curry" : 96, "K. Duckworth" : 97, "T. Duncan" : 98,
                              "K. Durant" : 99, "M. Ellis" : 100, "T. Evans" : 101, "P. Ewing" : 102, "D. Gallinari" : 103, "K. Garnett" : 104, "P. Gasol" : 105,
                              "R. Gay" : 106, "M. Ginobili" : 107, "D. Granger" : 108, "B. Griffin" : 109, "D. Howard" : 110, "A. Iguodala" : 111,
                              "L. James" : 112,
                              "J. Johnson" : 113, "M. Johnson" : 114, "M. Jordan" : 115, "J. Kidd" : 116, "B. Laimbeer" : 117, "D. Lee" : 118, "B. Lopez" : 119,
                              "K. Love" : 120, "K. Malone" : 121, "K. Martin" : 122, "T. McGrady" : 123, "S. Nash" : 124, "D. Nowitzki" : 125, "S. O'Neal" : 126,
                              "C. Oakley" : 127, "T. Parker" : 128, "C. Paul" : 129, "P. Pierce" : 130, "Z. Randolph" : 131, "A. Rivers" : 132,
                              "O. Robertson" : 133,
                              "D. Robinson" : 134, "D. Rose" : 135, "J. Smith" : 136, "J. Stockton" : 137, "A. Stoudemire" : 138, "D. Wade" : 139,
                              "D. Waiters" : 140,
                              "J. Wall" : 141, "G. Wallace" : 142, "J. West" : 143, "R. Westbrook" : 144, "D. Williams" : 145, "M. Yao" : 146}
        SHOT_BASE_IDS = {"Jump Shot 1" : 0, "Jump Shot 2" : 1, "Jump Shot 3" : 2, "Jump Shot 4" : 3, "Jump Shot 5" : 4, "Jump Shot 6" : 5,
                          "Jump Shot 7" : 6, "Jump Shot 8" : 7, "Jump Shot 9" : 8, "Jump Shot 10" : 9, "Jump Shot 11" : 10, "Jump Shot 12" : 11,
                          "Jump Shot 13" : 12, "Jump Shot 14" : 13, "Jump Shot 15" : 14, "Jump Shot 16" : 15, "Jump Shot 17" : 16,
                          "Jump Shot 18" : 17,
                          "Jump Shot 19" : 18, "Jump Shot 20" : 19, "Jump Shot 21" : 20, "Jump Shot 22" : 21, "Jump Shot 23" : 22,
                          "Jump Shot 24" : 23,
                          "Jump Shot 25" : 24, "Jump Shot 26" : 25, "Jump Shot 27" : 26, "Jump Shot 28" : 27, "Jump Shot 29" : 28,
                          "Jump Shot 30" : 29,
                          "Jump Shot 31" : 30, "Jump Shot 32" : 31, "Jump Shot 33" : 32, "Jump Shot 34" : 33, "Jump Shot 35" : 34,
                          "Jump Shot 36" : 35,
                          "Jump Shot 37" : 36, "Jump Shot 38" : 37, "Jump Shot 39" : 38, "Jump Shot 40" : 39, "Jump Shot 41" : 40, "Set Shot 1" : 41,
                          "Set Shot 2" : 42, "Set Shot 3" : 43, "Set Shot 4" : 44, "Set Shot 5" : 45, "Set Shot 6" : 46, "Set Shot 7" : 47,
                          "Set Shot 8" : 48,
                          "Set Shot 9" : 49, "Set Shot 10" : 50, "Set Shot 11" : 51, "Set Shot 12" : 52, "Set Shot 13" : 53, "Set Shot 14" : 54,
                          "Set Shot 15" : 55, "Set Shot 16" : 56, "Set Shot 17" : 57, "Set Shot 18" : 58, "L. Aldridge" : 59, "R. Allen" : 60,
                          "C. Anthony" : 61, "G. Arenas" : 62, "A. Bargnani" : 63, "D. Barnett" : 64, "M. Beasley" : 65, "C. Billups" : 66, "L. Bird" : 67,
                          "A. Bogut" : 68, "C. Boozer" : 69, "C. Bosh" : 70, "K. Bryant" : 71, "M. Camby" : 72, "V. Carter" : 73, "S. Curry" : 74,
                          "K. Duckworth" : 75, "T. Duncan" : 76, "K. Durant" : 77, "M. Ellis" : 78, "T. Evans" : 79, "P. Ewing" : 80, "D. Gallinari" : 81,
                          "K. Garnett" : 82, "P. Gasol" : 83, "R. Gay" : 84, "M. Ginobili" : 85, "D. Granger" : 86, "B. Griffin" : 87, "D. Howard" : 88,
                          "A. Iguodala" : 89, "L. James" : 90, "J. Johnson" : 91, "M. Johnson" : 92, "M. Jordan" : 93, "J. Kidd" : 94, "B. Laimbeer" : 95,
                          "D. Lee" : 96, "B. Lopez" : 97, "K. Love" : 98, "K. Malone" : 99, "K. Martin" : 100, "T. McGrady" : 101, "S. Nash" : 102,
                          "D. Nowitzki" : 103,
                          "S. O'Neal" : 104, "C. Oakley" : 105, "T. Parker" : 106, "C. Paul" : 107, "P. Pierce" : 108, "Z. Randolph" : 109, "A. Rivers" : 110,
                          "O. Robertson" : 111, "D. Robinson" : 112, "D. Rose" : 113, "J. Smith" : 114, "J. Stockton" : 115, "A. Stoudemire" : 116,
                          "D. Wade" : 117,
                          "D. Waiters" : 118, "J. Wall" : 119, "G. Wallace" : 120, "J. West" : 121, "R. Westbrook" : 122, "D. Williams" : 123, "M. Yao" : 124}
        DUNK_IDS = {"Under Basket Rim Pulls" : 1,"Under Basket Athletic Flushes" : 2,"Under Basket One Handers" : 3,
                    "Under Basket Bigman Slams" : 4,"Rim Grazers off one" : 5,"Rim Grazers off two" : 6,
                    "Basic One Handers off one" : 7,"Basic Two-Handers Off one" : 8,"Basic one handers off two" : 9,
                    "Basic two Handers off two" : 10,"Athletic One handers Off one" : 13,"Athletic One handers Off two" : 14,
                    "Hangs off one" : 15,"Hangs off two" : 16,"Quick Drops" : 17,
                    "Fist Pump Rim Pulls" : 18,"Side Arm Tomahawks" : 21,"Straight Arm Tomahawks" : 22,
                    "Cock back tomahawks" : 23,"Athletic Side Tomahawks" : 24,"Athletic Front tomahawks" : 25,
                    "Uber athletic Tomahawks off one" : 26,"Uber athletic Tomahawks off two" : 27,"Leaning Slams" : 28,
                    "Front Clutches" : 29,"Front Clutches off two" : 30,"Side Clutches off one" : 31,
                    "Side Clutches off two" : 32,"Back Scratchers off one" : 33,"Back Scratchers off two" : 34,
                    "Back Scratchers rim hangs" : 35,"Quick Drop in BackScratchers" : 37,"Reverses off one" : 38,
                    "Reverses off two" : 39,"Clutch reverse off one" : 40,"Clutch reverse off two" : 41,
                    "Baseline Clutch reverses" : 42,"Windmill reverses" : 43,"Switch hand reverses" : 44,
                    "Baseline reverses off one" : 45,"Baseline reverses off two" : 46,"Windmill Baseline reverses" : 47,
                    "Clutch Baseline reverses" : 48,"Windmills Off one" : 50,"Leaning Windmills" : 51,
                    "Front Windmills" : 53,"Side Windmills" : 54,"Athletic Windmills" : 55,
                    "Basic 360s" : 56,"Athletic 360s off one" : 57,"Athletic 360s off two" : 58,
                    "Under Leg 360s" : 59,"One hand Spin Dunks" : 60,"Two Hand Spin Dunks" : 61,
                    "Cradle Dunks" : 62,"Flashey Flushes" : 63,"Historic Jordan" : 64,"Historic Drexler" : 65}

        ALTERNATIVE_POST_SHOTS = {
            "Post Fade": ["Normal", "Fade 1","Fade 2", "Fade 3", "Fade 4", "Fade 5", "Fade 6", "Fade 7", "Fade 8", "Fade 9",
                          "B. Cartwright","M. Jordan", "K. Malone", "D. Nowitzki"],
            "Post Hook": ["Normal", "Hook 1", "Hook 2", "Hook 3", "Hook 4", "Hook 5", "Hook 6", "Hook 7", "Hook 8",
                          "Hook 9", "Hook 10", "Hook 11", "Hook 12", "Classic Sky Hook","S. O'Neal"],
            "Post Hop Shot": ["Normal", "Big", "Compact", "Crusader", "Deliberate", "Gaucho", "One Foot", "Quick"],
            "Post Shimmy Shot": ["Normal", "Big", "One Foot"],
            "Post Drive Stepback Shot": ["Normal", "Compact", "Deliberate", "Quick"],
            "Post Spin Stepback Shot": ["Normal", "Compact", "Cougar", "Crusader", "Deliberate", "Quick"],
            "Post Protect Shot": ["Normal", "Compact", "One Foot"],
            "Post Protect Spin Shot": ["Normal", "Compact", "Gaucho", "One Foot"]}
        ALTERNATIVE_DUNKS_AND_LAYUPS = {
            "Layup Package": ["Classic","Rookie Bigman"],
            "Goto Dunk Package": ["Under Basket Rim Pulls", "Under Basket Athletic Flushes", "Under Basket One Handers",
                                  "Under Basket Bigman Slams", "Rim Grazers off one", "Rim Grazers off two", "Basic One Handers off one",
                                  "Basic Two-Handers Off one", "Basic one handers off two", "Basic two Handers off two", "Athletic One handers Off one",
                                  "Athletic One handers Off two", "Hangs off one", "Hangs off two", "Quick Drops",
                                  "Fist Pump Rim Pulls", "Side Arm Tomahawks", "Straight Arm Tomahawks", "Cock back tomahawks",
                                  "Athletic Side Tomahawks", "Athletic Front tomahawks", "Uber athletic Tomahawks off one",
                                  "Uber athletic Tomahawks off two", "Leaning Slams", "Front Clutches", "Front Clutches off two",
                                  "Side Clutches off one", "Side Clutches off two", "Back Scratchers off one", "Back Scratchers off two",
                                  "Back Scratchers rim hangs", "Quick Drop in BackScratchers", "Reverses off one", "Reverses off two",
                                  "Clutch reverse off one", "Clutch reverse off two", "Baseline Clutch reverses", "Windmill reverses",
                                  "Switch hand reverses", "Baseline reverses off one", "Baseline reverses off two", "Windmill Baseline reverses",
                                  "Clutch Baseline reverses", "Windmills Off one", "Leaning Windmills", "Front Windmills", "Side Windmills",
                                  "Athletic Windmills", "Basic 360s", "Athletic 360s off one", "Athletic 360s off two", "Under Leg 360s",
                                  "One hand Spin Dunks", "Two Hand Spin Dunks", "Cradle Dunks", "Flashey Flushes", "Historic Jordan", "Historic Drexler"],
            "Extra Dunk Packages": []}



        def getShootingFormID(self):
            shootingFormID = self.SHOOTING_FORM_IDS.get(self.shots.get("Shooting Form"))
            return shootingFormID
        def getShotBaseID(self):
            shotBaseID = self.SHOT_BASE_IDS.get(self.shots.get("Shot Base"))
            return shotBaseID
        def getDunkIDList(self):
            dunkIDList = [self.DUNK_IDS.get(self.dunksAndLayups.get("Goto Dunk Package").rstrip("\n\t "))]
            print("Just assigned this value as BaseDunkPackage to dunkIDList: " + str(self.DUNK_IDS.get(self.dunksAndLayups.get("Goto Dunk Package"))))
            for dunkPackage in self.dunksAndLayups.get("Extra Dunk Packages"):
                dunkIDList.append(self.DUNK_IDS.get(dunkPackage.rstrip("\n\t ")))
                print("Just appended this dunk value: " + str(self.DUNK_IDS.get(dunkPackage)) + " ... from this dunk package: " + str(dunkPackage.rstrip("\n\t ")))

            listLength = len(dunkIDList)
            for i in range(6):
                if(i < listLength):
                    continue
                else:
                    dunkIDList.append(0)

            return dunkIDList



        rarity = None

        def __init__(self,rarity):
            self.rarity = rarity
            self.shots = {}
            self.momentumShotsOutside = {}
            self.postShots = {}
            self.dribbleMoves = {}
            self.dunksAndLayups = {}
            self.isSpecialShot = False
            self.specialShotName = ""
            self.specialShotDesc = ""

        shots = {}
        momentumShotsOutside = {}
        postShots = {}
        dribbleMoves = {}
        dunksAndLayups = {}

        def __str__(self):

            returnString = "*****************************\n"
            returnString += "******** SIGNATURE *********\n"
            returnString += "*****************************\n\n"
            returnString += "SHOTS:\n"
            returnString += "Shooting Form: " + self.shots.get("Shooting Form") + "\n"
            returnString += "Shot Base: " + self.shots.get("Shot Base") + "\n"
            returnString += "Fadeaway: " + self.shots.get("Fadeaway") + "\n"
            returnString += "Contested: " + self.shots.get("Contested") + "\n"
            returnString += "Escape Dribble Pull Up: " + self.shots.get("Escape Dribble Pull Up") + "\n\n"
            returnString += "Runner: " + self.shots.get("Runner") + "\n\n"
            returnString += "MOMENTUM SHOTS OUTSIDE:\n"
            returnString += "Dribble Pull Up: " + self.momentumShotsOutside.get("Dribble Pull Up") + "\n"
            returnString += "Spin Jumper: " + self.momentumShotsOutside.get("Spin Jumper") + "\n"
            returnString += "Hop Jumper: " + self.momentumShotsOutside.get("Hop Jumper") + "\n\n"
            returnString += "POST SHOTS:\n"
            returnString += "Post Fade: " + self.postShots.get("Post Fade") + "\n"
            returnString += "Post Hook: " + self.postShots.get("Post Hook") + "\n"
            returnString += "Post Hop Shot: " + self.postShots.get("Post Hop Shot") + "\n"
            returnString += "Post Shimmy Shot: " + self.postShots.get("Post Shimmy Shot") + "\n"
            returnString += "Post Drive Stepback Shot: " + self.postShots.get("Post Drive Stepback Shot") + "\n"
            returnString += "Post Spin Stepback Shot: " + self.postShots.get("Post Spin Stepback Shot") + "\n"
            returnString += "Post Protect Shot: " + self.postShots.get("Post Protect Shot") + "\n"
            returnString += "Post Protect Spin Shot: " + self.postShots.get("Post Protect Spin Shot") + "\n\n"
            returnString += "DRIBBLE MOVES:\n"
            returnString += "ISO Crossover: " + self.dribbleMoves.get("ISO Crossover") + "\n"
            returnString += "ISO Behind Back: " + self.dribbleMoves.get("ISO Behind Back") + "\n"
            returnString += "ISO Spin: " + self.dribbleMoves.get("ISO Spin") + "\n"
            returnString += "ISO Hesitation: " + self.dribbleMoves.get("ISO Hesitation") + "\n\n"
            returnString += "DUNKS AND LAYUPS:\n"
            returnString += "Layup Package: " + self.dunksAndLayups.get("Layup Package") + "\n"
            returnString += "Goto Dunk Package: " + self.dunksAndLayups.get("Goto Dunk Package") + "\n"

            counter = 0
            for i in self.dunksAndLayups.get("Extra Dunk Packages"):
                counter += 1
                returnString += "Extra Dunk Package " + str(counter) + ": " + i + "\n"
            return returnString

        def genShots(self,archetype):
            self.shots["Shooting Form"] = self.SHOTS.get("Shooting Form")[random.randrange(0, len(self.SHOTS.get("Shooting Form")))]
            self.shots["Shot Base"] = self.SHOTS.get("Shot Base")[random.randrange(0, len(self.SHOTS.get("Shot Base")))]
            self.shots["Fadeaway"] = self.SHOTS.get("Fadeaway")[random.randrange(0, len(self.SHOTS.get("Fadeaway")))]
            self.shots["Contested"] = self.SHOTS.get("Contested")[random.randrange(0, len(self.SHOTS.get("Contested")))]
            self.shots["Escape Dribble Pull Up"] = self.SHOTS.get("Escape Dribble Pull Up")[random.randrange(0, len(self.SHOTS.get("Escape Dribble Pull Up")))]
            self.shots["Runner"] = self.SHOTS.get("Runner")[random.randrange(0, len(self.SHOTS.get("Runner")))]

            self.momentumShotsOutside["Dribble Pull Up"] = self.MOMENTUM_SHOTS_OUTSIDE.get("Dribble Pull Up")[random.randrange(0, len(self.MOMENTUM_SHOTS_OUTSIDE.get("Dribble Pull Up")))]
            self.momentumShotsOutside["Spin Jumper"] = self.MOMENTUM_SHOTS_OUTSIDE.get("Spin Jumper")[random.randrange(0, len(self.MOMENTUM_SHOTS_OUTSIDE.get("Spin Jumper")))]
            self.momentumShotsOutside["Hop Jumper"] = self.MOMENTUM_SHOTS_OUTSIDE.get("Hop Jumper")[random.randrange(0, len(self.MOMENTUM_SHOTS_OUTSIDE.get("Hop Jumper")))]


            if(archetype.inGamePositionId == 3 or archetype.inGamePositionId == 4):
                self.postShots["Post Fade"] = self.ALTERNATIVE_POST_SHOTS.get("Post Fade")[random.randrange(0, len(self.ALTERNATIVE_POST_SHOTS.get("Post Fade")))]
                self.postShots["Post Hook"] = self.ALTERNATIVE_POST_SHOTS.get("Post Hook")[random.randrange(0, len(self.ALTERNATIVE_POST_SHOTS.get("Post Hook")))]
                self.postShots["Post Hop Shot"] = self.ALTERNATIVE_POST_SHOTS.get("Post Hop Shot")[random.randrange(0, len(self.ALTERNATIVE_POST_SHOTS.get("Post Hop Shot")))]
                self.postShots["Post Shimmy Shot"] = self.ALTERNATIVE_POST_SHOTS.get("Post Shimmy Shot")[random.randrange(0, len(self.ALTERNATIVE_POST_SHOTS.get("Post Shimmy Shot")))]
                self.postShots["Post Drive Stepback Shot"] = self.ALTERNATIVE_POST_SHOTS.get("Post Drive Stepback Shot")[random.randrange(0, len(self.ALTERNATIVE_POST_SHOTS.get("Post Drive Stepback Shot")))]
                self.postShots["Post Spin Stepback Shot"] = self.ALTERNATIVE_POST_SHOTS.get("Post Spin Stepback Shot")[random.randrange(0, len(self.ALTERNATIVE_POST_SHOTS.get("Post Spin Stepback Shot")))]
                self.postShots["Post Protect Shot"] = self.ALTERNATIVE_POST_SHOTS.get("Post Protect Shot")[random.randrange(0, len(self.ALTERNATIVE_POST_SHOTS.get("Post Protect Shot")))]
                self.postShots["Post Protect Spin Shot"] = self.ALTERNATIVE_POST_SHOTS.get("Post Protect Spin Shot")[random.randrange(0, len(self.ALTERNATIVE_POST_SHOTS.get("Post Protect Spin Shot")))]
            else:
                self.postShots["Post Fade"] = self.POST_SHOTS.get("Post Fade")[random.randrange(0, len(self.POST_SHOTS.get("Post Fade")))]
                self.postShots["Post Hook"] = self.POST_SHOTS.get("Post Hook")[random.randrange(0, len(self.POST_SHOTS.get("Post Hook")))]
                self.postShots["Post Hop Shot"] = self.POST_SHOTS.get("Post Hop Shot")[random.randrange(0, len(self.POST_SHOTS.get("Post Hop Shot")))]
                self.postShots["Post Shimmy Shot"] = self.POST_SHOTS.get("Post Shimmy Shot")[random.randrange(0, len(self.POST_SHOTS.get("Post Shimmy Shot")))]
                self.postShots["Post Drive Stepback Shot"] = self.POST_SHOTS.get("Post Drive Stepback Shot")[random.randrange(0, len(self.POST_SHOTS.get("Post Drive Stepback Shot")))]
                self.postShots["Post Spin Stepback Shot"] = self.POST_SHOTS.get("Post Spin Stepback Shot")[random.randrange(0, len(self.POST_SHOTS.get("Post Spin Stepback Shot")))]
                self.postShots["Post Protect Shot"] = self.POST_SHOTS.get("Post Protect Shot")[random.randrange(0, len(self.POST_SHOTS.get("Post Protect Shot")))]
                self.postShots["Post Protect Spin Shot"] = self.POST_SHOTS.get("Post Protect Spin Shot")[random.randrange(0, len(self.POST_SHOTS.get("Post Protect Spin Shot")))]

            self.dribbleMoves["ISO Crossover"] = self.DRIBBLE_MOVES.get("ISO Crossover")[random.randrange(0, len(self.DRIBBLE_MOVES.get("ISO Crossover")))]
            self.dribbleMoves["ISO Behind Back"] = self.DRIBBLE_MOVES.get("ISO Behind Back")[random.randrange(0, len(self.DRIBBLE_MOVES.get("ISO Behind Back")))]
            self.dribbleMoves["ISO Spin"] = self.DRIBBLE_MOVES.get("ISO Spin")[random.randrange(0, len(self.DRIBBLE_MOVES.get("ISO Spin")))]
            self.dribbleMoves["ISO Hesitation"] = self.DRIBBLE_MOVES.get("ISO Hesitation")[random.randrange(0, len(self.DRIBBLE_MOVES.get("ISO Hesitation")))]

            if (archetype.inGamePositionId == 3 or archetype.inGamePositionId == 4):
                self.dunksAndLayups["Layup Package"] = self.ALTERNATIVE_DUNKS_AND_LAYUPS.get("Layup Package")[random.randrange(0, len(self.ALTERNATIVE_DUNKS_AND_LAYUPS.get("Layup Package")))]
            else:
                self.dunksAndLayups["Layup Package"] = self.DUNKS_AND_LAYUPS.get("Layup Package")[random.randrange(0, len(self.DUNKS_AND_LAYUPS.get("Layup Package")))]

            listOfDunks = []
            for i in self.DUNKS_AND_LAYUPS.get("Goto Dunk Package"):
                listOfDunks.append(i)
            randomDunk = listOfDunks[random.randrange(0, len(listOfDunks))]
            self.dunksAndLayups["Goto Dunk Package"] = randomDunk
            listOfDunks.remove(randomDunk)
            self.dunksAndLayups["Extra Dunk Packages"] = []
            if (str(self.rarity) == "Rare"):
                randomDunk1 = listOfDunks[random.randrange(0, len(listOfDunks))]
                listOfDunks.remove(randomDunk1)
                self.dunksAndLayups["Extra Dunk Packages"].append(randomDunk1)

            elif (str(self.rarity) == "Epic"):
                randomDunk1 = listOfDunks[random.randrange(0, len(listOfDunks))]
                listOfDunks.remove(randomDunk1)
                self.dunksAndLayups["Extra Dunk Packages"].append(randomDunk1)
                randomDunk2 = listOfDunks[random.randrange(0, len(listOfDunks))]
                listOfDunks.remove(randomDunk2)
                self.dunksAndLayups["Extra Dunk Packages"].append(randomDunk2)

            elif (str(self.rarity) == "Legendary"):
                randomDunk1 = listOfDunks[random.randrange(0, len(listOfDunks))]
                listOfDunks.remove(randomDunk1)
                self.dunksAndLayups["Extra Dunk Packages"].append(randomDunk1)
                randomDunk2 = listOfDunks[random.randrange(0, len(listOfDunks))]
                listOfDunks.remove(randomDunk2)
                self.dunksAndLayups["Extra Dunk Packages"].append(randomDunk2)
                randomDunk3 = listOfDunks[random.randrange(0, len(listOfDunks))]
                listOfDunks.remove(randomDunk3)
                self.dunksAndLayups["Extra Dunk Packages"].append(randomDunk3)

            elif (str(self.rarity) == "Godlike"):
                randomDunk1 = listOfDunks[random.randrange(0, len(listOfDunks))]
                listOfDunks.remove(randomDunk1)
                self.dunksAndLayups["Extra Dunk Packages"].append(randomDunk1)
                randomDunk2 = listOfDunks[random.randrange(0, len(listOfDunks))]
                listOfDunks.remove(randomDunk2)
                self.dunksAndLayups["Extra Dunk Packages"].append(randomDunk2)
                randomDunk3 = listOfDunks[random.randrange(0, len(listOfDunks))]
                listOfDunks.remove(randomDunk3)
                self.dunksAndLayups["Extra Dunk Packages"].append(randomDunk3)
                randomDunk4 = listOfDunks[random.randrange(0, len(listOfDunks))]
                listOfDunks.remove(randomDunk4)
                self.dunksAndLayups["Extra Dunk Packages"].append(randomDunk4)


        RARE_SPECIAL_SHOTS = {"Slayer" : [["Tyrion Lannister","Release 37","K. Bryant","Tyrion Lannister will go down as the greatest disappointment in 2k history, as he could never seem to shoot the ball into the net...like ever. God help this new player with Tyrion's cursed shot."],
                                          ["Danny Kowalczyk", "R. Allen", "R. Allen","A shot seen whenever new players arrived, Danny's sniper rifle bullet of a shot was completely unique at the time and made for some consistent performances before competitive play was introduced. Can this new player snipe their way to glory with Danny's shot?"],
                                          ["Lord Selwig Nara", "Release 4", "Jump Shot 22","Coined as the lock'n'load shot in the later stages of league, Lord Selwig Nara finally found some success near the end of his lengthy career with consistent outlet 3s. Can this new player rise faster than Selwig with his own shot?"],
                                          ],
                              "Vigilante" : [["Mahatma Gandhi","Release 67","Jump Shot 6","If it weren't for his height and brutal speed, Gandhi could have been one of the all time greats with his under-handed, consistent delivery of 3 pt shots. Can this new player break past the faults of Gandhi with his majestic shot?"],
                                             ["Christian Shearcliff", "Release 16", "Jump Shot 39","If there's anything nice to say about Christian Shearcliff it might just be his shooting form, which almost took him to legend status. Can this new player be everything Chris wasn't?"],
                                             ["Ni-Gha Die","K. Duckworth","Set Shot 11","Everyone knows that Ni-Gha Die didn't become a legend because of his horrible shot, but hey, he did make it there anyways. Can this new player beat the odds with this wacky and obtrusive shot?"]],
                              "Medic" : [["Father Titticaca","Release 17","Jump Shot 17","Father Titticaca was an explosion of speed, rebounding, and exceptional shooting ability wrapped into one, and was the backbone of every team with which he played. Can this new player explode into the scene like Titti with his own shot?"],
                                         ["Old Sama Benlodan", "L. James", "Set Shot 2","Old Sama's carefully set shot will always go down as the pefect fold to his duo Bill Nye. Will this new player find similar success with the same shot?"],
                                         ["Daniel Stiefbold", "Release 20", "M. Camby","One of the quirkier shots in 2k, Daniel Stiefbold went on a tear in the early days of 2k with his scoped-like release. Can this new player exceed expectations like Daniel did with such a strange, exotic shot?"]],
                              "Guardian" : [["The Hound","Release 23","P. Pierce","Raising his arms high into the air to launch the ball into the net, The Hound's classic shot practically dominated the control-oriented meta in the early days of 2k. Can this new player break out as the new superstar with The Hound's shot?"],
                                            ["Old Sama Benlodan", "L. James", "Set Shot 2","Old Sama's carefully set shot will always go down as the pefect fold to his duo Bill Nye. Will this new player find similar success with the same shot?"],
                                            ["Daniel Stiefbold", "Release 20", "M. Camby","One of the quirkier shots in 2k, Daniel Stiefbold went on a tear in the early days of 2k with his scoped-like release. Can this new player exceed expectations like Daniel did with such a strange, exotic shot?"]],
                              "Engineer" : [["Gary the Thief","J. Smith","K. Garnett","Gary's robotic dance of a shot eventually carried him to a semi-prominent legend status, which is more than anybody could have ever expected out of the Twitch streamer. Can this new player climb the ladder of greatness like Gary did?"],
                                            ["Mike Ehrmantraut", "D. Howard", "C. Paul","Known more for his control ability, Mike's clean and consistent shot often went unnoticed in the shadow of his colossal mid plays. Can this new player sink'em like Mike?"],
                                            ["Tyrion Lannister", "Release 37", "K. Bryant","Tyrion Lannister will go down as the greatest disappointment in 2k history, as he could never seem to shoot the ball into the net...like ever. God help this new player with Tyrion's cursed shot."]],
                              "Director" : [["Alex Somheil","Release 17","Jump Shot 3","A shot seen whenever new players arrived, Alex's unmistakablely clean shot proved valuable for the short time him and Danny were viable in competitive play. Can this new player exceed the consistent performances of Alex with his own shot?"],
                                            ["Gary the Thief", "J. Smith", "K. Garnett","Gary's robotic dance of a shot eventually carried him to a semi-prominent legend status, which is more than anybody could have ever expected out of the Twitch streamer. Can this new player climb the ladder of greatness like Gary did?"],
                                            ["Mike Ehrmantraut", "D. Howard", "C. Paul","Known more for his control ability, Mike's clean and consistent shot often went unnoticed in the shadow of his colossal mid plays. Can this new player sink'em like Mike?"],
                                            ["Father Titticaca", "Release 17", "Jump Shot 17","Father Titticaca was an explosion of speed, rebounding, and exceptional shooting ability wrapped into one, and was the backbone of every team with which he played. Can this new player explode into the scene like Titti with his own shot?"],
                                            ["Christian Shearcliff", "Release 16", "Jump Shot 39","If there's anything nice to say about Christian Shearcliff it might just be his shooting form, which almost took him to legend status. Can this new player be everything Chris wasn't?"],
                                            ["Ni-Gha Die","K. Duckworth","Set Shot 11","Everyone knows that Ni-Gha Die didn't become a legend because of his horrible shot, but hey, he did make it there anyways. Can this new player beat the odds with this wacky and obtrusive shot?"]]}

        EPIC_SPECIAL_SHOTS = {"Slayer": [["Jaquarius Nigga","M. Yao","Jump Shot 7","Jaquarius didn't have the time to shine as much as his talent allowed him to, and everyone knew that he had what it took to be one of the Gods. His shot was as deadly as his footwork and rebounding. May this new player carry on a great legacy with Jay-Quay's shot."],
                                         ["Ser Davos", "Release 11", "Jump Shot 23","Ser Davos rode the line between non-legend and legend status for quite some time with his strange, side-spinning shot, finding decent success throughout his run. Can this new player succeed where Davos failed?"],
                                         ["Subway Jay","Release 57","Jump Shot 39","Subway Jay couldn't speak a lick of English, but if there was a language for basketball, he'd probably be a linguistics professor with his leg-kicking, ball-throwing, fun mess of a shot. Can this new player destroy the court like Jay killed it in the league?"],
                                         ["The Bro", "K. Duckworth", "D. Barnett","From utter garbage to the heights of legendry, back down to somewhere in between, The Bro has used his exotic shot to reach the extreme highs and lows of the 2k universe. Can this new player ramp it up like The Bro did with this unusual shot?"],
                                         ["Ish Tickletits", "R. Allen", "Set Shot 7","Known for his legendary run with Warren's squad in the 2k league, Ish dominated the league for 2 seasons with his sniper rifle shot. Can this new player dominate the competitive scene similarly with this classic shot?"],
                                         ["Sprite Agent", "T. Evans", "T. Evans","Like a ghillie in the mist, Sprite Agent was a deadshot sniper with his bullet-like shooting form, finding himself major success in the late league days. Can this new player snipe the competition as Sprite Agent once did?"],
                                         ["Imperial Commander", "D. Howard", "Set Shot 17","Imperial Commander could probably shoot 50 basketballs in the span of 5 seconds with his laser-fast form, which made it incredibly hard to block the legendary player. May Imperial Commander's shot bless this new player with success and an increased will to murder Stormcloaks."],
                                         ["Ben Linus", "Z. Randolph", "Set Shot 14","Ben Linus has charitably gifted many a basketball to the Martians with his unbelievably high-arching shot, but when they did come down, they fell in the hoop for this late-game legend. Can this new player reach the stars like Ben did?"],
                                         ["Stacy Harper", "M. Yao", "Set Shot 16","Although Stacy never reached the expectations everyone had for him, his shot is still unrivaled in smoothness and pace of delivery. Can this new player break ground that Stacy never could with this buttery smooth shot?"]],
                              "Vigilante": [["Ser Davos","Release 11","Jump Shot 23","Ser Davos rode the line between non-legend and legend status for quite some time with his strange, side-spinning shot, finding decent success throughout his run. Can this new player succeed where Davos failed?"],
                                            ["Subway Jay","Release 57","Jump Shot 39","Subway Jay couldn't speak a lick of English, but if there was a language for basketball, he'd probably be a linguistics professor with his leg-kicking, ball-throwing, fun mess of a shot. Can this new player destroy the court like Jay killed it in the league?"],
                                            ["The Thor", "D. Nowitzki", "Jump Shot 35","Perhaps one of the fastest-to-legend players to date, Thor annihilated the competition with his high-arching shot in the murky days of 2k. Will this new player climb the ranks as fast as Thor with his own shot?"],
                                            ["Stacy Harper", "M. Yao", "Set Shot 16","Although Stacy never reached the expectations everyone had for him, his shot is still unrivaled in smoothness and pace of delivery. Can this new player break ground that Stacy never could with this buttery smooth shot?"],
                                            ["Fat Kid", "L. Bird", "Jump Shot 24","Less known for his straight up shot and more for his acrobatic abilites, Fat Kid's classic shot is still a staple to 2k and the mark of one of the first great 3 pt shooters. Can this new player make a name for himself using Fat Kid's age-old shot?"],
                                            ["Morgan Freeman", "Z. Randolph", "Jump Shot 35","You see those craters in the moon? Those are from Morgan Freeman launching the basketball into space every time he took a shot, finding him success as a multi-tool non-legend. Can this new player wreak havoc in space like Morgan did?"],
                                            ["Allfather Pickles","Release 18","C. Boozer","Going under the radar for most of his early days, Allfather truly broke out into stardom during the final stages of the league era, and it's a damn shame we couldn't witness more. Can this new player carry on such a short, but great legacy with Allfather's shot?"]],
                              "Medic": [["The Thinker","D. Rose","Jump Shot 27","Nobody was having any second thinking thoughts about the Thinker with his extraordinarily good, control dominating gameplay and shot. Can this new player revive the glory days of The Thinker with his classic shot?"]],
                              "Guardian": [["Jaquarius Nigga","M. Yao","Jump Shot 7","Jaquarius didn't have the time to shine as much as his talent allowed him to, and everyone knew that he had what it took to be one of the Gods. His shot was as deadly as his footwork and rebounding. May this new player carry on a great legacy with Jay-Quay's shot."],
                                           ["The Night King", "Release 33", "K. Bryant","At the very forefront of the early control meta, The Night King defined the meta as he raced to legend status with his clean shot and phenomenal rebounding skills faster than nearly anyone before him. Will this new player be able to say the same after using The Night King's shot?"],
                                           ["The Thinker", "D. Rose", "Jump Shot 27","Nobody was having any second thinking thoughts about the Thinker with his extraordinarily good, control dominating gameplay and shot. Can this new player revive the glory days of The Thinker with his classic shot?"],
                                           ["Imperial Commander", "D. Howard", "Set Shot 17","Imperial Commander could probably shoot 50 basketballs in the span of 5 seconds with his laser-fast form, which made it incredibly hard to block the legendary player. May Imperial Commander's shot bless this new player with success and an increased will to murder Stormcloaks."],
                                           ["The Thor", "D. Nowitzki", "Jump Shot 35","Perhaps one of the fastest-to-legend players to date, Thor anihilated the competition with his high-arching shot in the murky days of 2k. Will this new player climb the ranks as fast as Thor with his own shot?"],
                                           ["Morgan Freeman", "Z. Randolph", "Jump Shot 35","You see those craters in the moon? Those are from Morgan Freeman launching the basketball into space every time he took a shot, finding him success as a multi-tool non-legend. Can this new player wreak havoc in space like Morgan did?"],
                                           ["Allfather Pickles","Release 18","C. Boozer","Going under the radar for most of his early days, Allfather truly broke out into stardom during the final stages of the league era, and it's a damn shame we couldn't witness more. Can this new player carry on such a short, but great legacy with Allfather's shot?"]],
                              "Engineer": [["The Night King","Release 33","K. Bryant","At the very forefront of the early control meta, The Night King defined the meta as he raced to legend status with his clean shot and phenomenal rebounding skills faster than nearly anyone before him. Will this new player be able to say the same after using The Night King's shot?"],
                                           ["Manager Sneh", "C. Oakley", "P. Pierce","Despite his label as manager, Sneh was a god awful manager at Subway, but he did manage to sink in many a basketball with his smooth delivery. Can this new player manage to do the same?"]],
                              "Director": [["Manager Sneh","C. Oakley","P. Pierce","Despite his label as manager, Sneh was a god awful manager at Subway, but he did manage to sink in many a basketball with his smooth delivery. Can this new player manage to do the same?"],
                                           ["Ben Linus", "Z. Randolph", "Set Shot 14","Ben Linus has charitably gifted many a basketball to the Martians with his unbelievably high-arching shot, but when they did come down, they fell in the hoop for this late-game legend. Can this new player reach the stars like Ben did?"]]}

        LEGENDARY_SPECIAL_SHOTS = {"Slayer": [["Bill Nye","Release 54","Jump Shot 9","Bill Nye will go down as the greatest 2k player to ever touch the blacktop and his shot will be remembered just as fondly. This new player has hit the jackpot, and the question turns not to whether he will be great, but when he will."],
                                              ["Jacob Rogers", "Release 7", "Jump Shot 8","The ability to leap several feet higher than a normal human being, coupled with a short-statured legend was enough to carry Jake Rogers into God-tier for the entirety of 2ks run. Will the grace of Jake's leap and clean release aid this new player in doing the same?"],
                                              ["Timmy Nigga", "C. Boozer", "Set Shot 2","An uncontested Timmy Nigga could take a shot from orbit, locked in a titanium cell, music blasting in his ears, and sink it without batting a fucking eye. Will this player ever miss with Timmy's buttery smooth shooting form?"],
                                              ["Dan Harrison", "Release 61", "Set Shot 4", "A shot from the heavens, Dan Harrison's smooth and hasty delivery left every player's jaw on the floor after his godlike dominance at the end of the last league season. Can this new player stand on the shoulders of a giant like Dan?"],
                                              ["Lipton Strawberry","C. Boozer","D. Nowitzki","Lipton Strawberry defined an entire era of 2k play with his unblockable, unmissable, destructively clean shot. Will this new player live up to the godly expectations of Lipton's perfect shot?"]],
                                   "Vigilante": [["Jimmy Nigga","Release 51","Set Shot 5","The OG, first-ever legend, classic of all classics, Jimmy Nigga put everyone into a coffin when he hit the court with his unmistakably clean 3s. Can this new player rebirth what once was with Jimmy's timeless shot?"],
                                            ["Dan Harrison", "Release 61", "Set Shot 4","A shot from the heavens, Dan Harrison's smooth and hasty delivery left every player's jaw on the floor after his godlike dominance at the end of the last league season. Can this new player stand on the shoulders of a giant like Dan?"],
                                            ["Dek Nara", "D. Nowitzki", "Jump Shot 21","Dek Nara literally pioneered the term God for 2k, and had to be literally banned from play for being so unbelievably good with his high-arching bomb of a shot. This new player should feel honored to carry on the Hawaiian peace God's classic shot."]],
                                   "Medic": [],
                                   "Guardian": [["Jimmy Nigga","Release 51","Set Shot 5","The OG, first-ever legend, classic of all classics, Jimmy Nigga put everyone into a coffin when he hit the court with his unmistakably clean 3s. Can this new player rebirth what once was with Jimmy's timeless shot?"]],
                                   "Engineer": [],
                                   "Director": [["Abe Lincoln","C. Boozer","Set Shot 13","There isn't much to say that hasn't already been said about Abe's silky smooth shot in the history of 2k. This new player should feel blessed to carry on one of the greatest shots ever introduced to 2k."],
                                           ["Bill Nye", "Release 54", "Jump Shot 9","Bill Nye will go down as the greatest 2k player to ever touch the blacktop and his shot will be remembered just as fondly. This new player has hit the jackpot, and the question turns not to whether he will be great, but when he will."]]}

        specialShotRarities = {"Rare" : 0.01,
                               "Epic" : 0.05,
                               "Legendary" : 0.2,
                               "Godlike" : 0.75,
                               "Common" : 0}

        isSpecialShot = False
        specialShotName = ""
        specialShotDesc = ""
        def genSpecialShots(self,archetypeName):

            chance = self.specialShotRarities.get(str(self.rarity))
            randGen = (random.uniform(0,1)) + chance
            if(randGen > 1):
                self.isSpecialShot = True
                usedSpecialShots = open("Old/UsedSpecialShots.txt", "r")
                possibleShots = []

                if (str(self.rarity) == "Rare" or str(self.rarity) == "Epic" or str(self.rarity) == "Legendary" or str(self.rarity) == "Godlike"):
                    for player in self.RARE_SPECIAL_SHOTS.get(archetypeName):
                        playerName = player[0]
                        if (playerName in usedSpecialShots):
                            continue
                        possibleShots.append(player)

                if(str(self.rarity) == "Epic" or str(self.rarity) == "Legendary" or str(self.rarity) == "Godlike"):
                    for player in self.EPIC_SPECIAL_SHOTS.get(archetypeName):
                        playerName = player[0]
                        if (playerName in usedSpecialShots):
                            continue
                        possibleShots.append(player)

                if (str(self.rarity) == "Legendary" or str(self.rarity) == "Godlike"):
                    for player in self.LEGENDARY_SPECIAL_SHOTS.get(archetypeName):
                        playerName = player[0]
                        if (playerName in usedSpecialShots):
                            continue
                        possibleShots.append(player)

                usedSpecialShots.close()

                if(len(possibleShots) == 0):
                    self.isSpecialShot = False
                    return False

                randomPlayer = possibleShots[random.randrange(0,len(possibleShots))]
                usedSpecialShots = open("Old/UsedSpecialShots.txt", "a")
                usedSpecialShots.write(randomPlayer[0] + "\n")
                usedSpecialShots.close()

                self.specialShotName = randomPlayer[0]
                self.specialShotDesc = randomPlayer[3]

                self.shots["Shooting Form"] = randomPlayer[1]
                self.shots["Shot Base"] = randomPlayer[2]
    def genSignatureStats(self):
        self.signatureStats = self.Signature(self.playerRarity)
        self.signatureStats.genShots(self.archetype)
        # SPECIAL SHOTS TEMPORARILY DISABLED, COME BACK TO THIS LATER!!!
        #self.signatureStats.genSpecialShots(self.archetypeName)

    # Members and methods for the player's clothes type.
    def setClothesType(self,_clothesType):
        if(_clothesType.upper() == "SUIT"):
            self.__clothesType = "Suit"
        elif(_clothesType.upper() == "JERSEY"):
            self.__clothesType = "Jersey"
        elif(_clothesType.upper() == "STREET"):
            self.__clothesType = "Street"
        else:
            return False
    def getClothesType(self):
        return self.__clothesType

    # This class tracks appearance information for the player, including height, weight,
    # accessories, tattoos, and Headshape information.
    class Appearance:

        def genHeadshapeDictionary(self):
            headshapeDict = {
                        "HParam1" : None,
                        "HParam2" : None,
                        "HdBrwHght" : None,
                        "HdBrwWdth" : None,
                        "HdBrwSlpd" : None,
                        "HdNkThck" : None,
                        "HdNkFat" : None,
                        "HdChnLen" : None,
                        "HdChnWdth" : None,
                        "HdChnProt" : None,
                        "HdJawSqr" : None,
                        "HdJawWdth" : None,
                        "HdChkHght" : None,
                        "HdChkWdth" : None,
                        "HdChkFull" : None,
                        "HdDefinit" : None,
                        "MtULCurve" : None,
                        "MtULThick" : None,
                        "MtULProtr" : None,
                        "MtLLCurve" : None,
                        "MtLLThick" : None,
                        "MtLLProtr" : None,
                        "MtSzHght" : None,
                        "MtSzWdth" : None,
                        "MtCrvCorn" : None,
                        "ErHeight" : None,
                        "ErWidth" : None,
                        "ErEarLobe" : None,
                        "ErTilt" : None,
                        "NsNsHght" : None,
                        "NsNsWdth" : None,
                        "NsNsProtr" : None,
                        "NsBnBridge" : None,
                        "NsBnDefin" : None,
                        "NsBnWdth" : None,
                        "NsTipHght" : None,
                        "NsTipWdth" : None,
                        "NsTipTip" : None,
                        "NsTipBnd" : None,
                        "NsNtHght" : None,
                        "NsNtWdth" : None,
                        "EsFrmOpen" : None,
                        "EsFrmSpac" : None,
                        "EsFrmLwEl" : None,
                        "EsFrmUpEl" : None,
                        "EsPlcHght" : None,
                        "EsPlcWdth" : None,
                        "EsPlcRot" : None,
                        "EsPlcProt" : None,
                        "EsShpOtEl" : None,
                        "EsShpInEl" : None
                        }

            return headshapeDict

        # Init method initializes the many CAP member variables.
        def __init__(self):
            # Controlled by respective get/set/genHeight functions.
            self.height = None
            # Changes skin tone. 0 darkest, 5 lightest.
            self.skinTone = 0
            # 0 = "Buff" (weaker), 1 = "Ripped" (stronger)
            self.muscles = 0
            # 0 = Blue, 1 = Brown, 2 = Green, 3 = Hazel, 4 = Amber, 5 = Gray
            self.eyeColor = 0
            # 0 = Slim, 1 = Normal, 2 = Thick, 3 = Athletic
            self.bodyType = 0
            self.weight = 0
            # 0 = Jersey, 1 = Practice, 2 = Suit, 3 = Casual 1, 4 = Casual 2
            self.clothes = 0
            # HeadshapeID must be connected to a valid Headshape. Set to 0 to disable.
            # If headshapeID is not 0, headshapeInfo will provide an array of all
            # headshape values.
            self.headshapeID = 0
            self.headshapeInfo= self.genHeadshapeDictionary()

            # Determines which "FaceType" is used (0-3)
            self.faceType = 0
            # Hair styles:
            # 0 - No Hair, 1 - Short Stubble, 2 - Medium Stubble, 3 - Dark Stubble
            # 4 - Dark Recessed Stubble, 5 - Balding Stubble, 6 - Short Buzz
            # 7 - Buzz, 8 - Widow's Peak Buzz, 9 - Balding Buzz
            # 10 - Natural Waves, 11 - Natural Patches, 12 - Natural Part
            # 13 - Natural Fauxhawk, 14 - Natural Balding, 15 - Thick Cornrows
            # 16 - Thin Cornrows, 17 - Afro, 18 - Messy
            # 19 - Twisties, 20 - Short Dreads, 21 - Medium Dreads
            # 22 - Tied Dreads, 23 - Dreads Tail, 24 - Mop
            # 25 - Mop Tail, 26 - Straight Short, 27 - Straight Long
            # 28 - Straight Flat, 29 - Straight Part, 30 - Straight Tail
            # 31 - Straight Balding, 32 - Spikey, 33 - Curly
            # 34 - Balding Flat, 35 - Short Flat, 36 - Medium Flat
            # 37 - Wavy, 38 - Shaggy, 39 - Mohawk, 40 - The Patch
            self.hairStyle = 0
            # Hair colors:
            # 0 - Black, 1 - Dark Brown, 2 - Medium Brown, 3 - Light Brown
            # 4 - Very Light Brown, 5 - Dark Blonde, 6 - Medium Blonde
            # 7 - Light Blonde, 8 - Very Light Blonde, 9 - Gray, 10 - White
            # 11 - Red, 12 - Green, 13 - Blue, 14 - Yellow, 15 - Orange
            self.hairColor = 0
            # Value betweeen 0 - 255 for select hairstyles.
            self.hairLength = 0
            # Picks beard - value between 0 and 13.
            self.beardStyle = 0
            # Picks moustache - value between 0 and 7
            self.moustacheStyle = 0
            # Picks goatee - value between 0 and 20
            self.goateeStyle = 0
            # Facial hair colors:
            # 0 - Black, 1 - Dark Brown, 2 - Medium Brown, 3 - Light Brown
            # 4 - Very Light Brown, 5 - Dark Blonde, 6 - Medium Blonde
            # 7 - Light Blonde, 8 - Very Light Blonde, 9 - Gray, 10 - White
            # 11 - Red, 12 - Green, 13 - Blue, 14 - Yellow, 15 - Orange
            self.facialHairColor = 0
            # Picks eyebrows - value between 0 and 10
            self.eyebrowStyle = 0

            # Left neck tattoo - value between 0 and 37
            self.leftNeckTattoo = 0
            # Left shoulder tattoo - value between 0 and 27
            self.leftShoulderTattoo = 0
            # Right shoulder tattoo - value between 0 and 27
            self.rightShoulderTattoo = 0
            # Left bicep tattoo - value between 0 and 60
            self.leftBicepTattoo = 0
            # Right bicep tattoo - value between 0 and 60
            self.rightBicepTattoo = 0
            # Left forearm tattoo - value between 0 and 59
            self.leftForearmTattoo = 0
            # Right forearm tattoo - value between 0 and 59
            self.rightForearmTattoo = 0

            # Whether or not player wears a headband - 0 = false, 1 = true.
            self.wearsHeadband = 0
            # Position of headband logo - 0 = Front Left, 1 = Front, 2 = Front Right, 3 = Back, 4 = No Logo
            self.headbandLogoPosition = 0
            # What type of undershirt the player wears. 0 = None, 1 = Undershirt, 2 = Shortsleeve Shirt, 3 = Longsleeve shirt
            self.undershirtType = 0
            # What color the player's undershirt is. 0 = White, 1 = Black, 2 = Team Color 1, 3 = Team Color 2
            self.undershirtColor = 0
            # What gear the player wears on their left arm. 0 = None, 1 = Sleeve, 2 = Padded Sleeve, 3 = Short Sleeve, 4 = Shoulder Sleeve, 5 = Full Arm Sleeve, 6 = PowerWEB Armsleeve
            self.leftArmGear = 0
            # What color the player's left arm gear is. 0 = White, 1 = Black, 2 = Team Color 1, 3 = Team Color 2
            self.leftArmGearColor = 0
            # What gear the player wears on their left elbow. 0 = None, 1 = Pad, 2 = Sleeve, 3 = Small Band, 4 = Medium Band, 5 = High Band, 6 = Brace, 7 = Strap
            self.leftElbowGear = 0
            # What color the player's left elbow gear is. 0 = White, 1 = Black, 2 = Team Color 1, 3 = Team Color 2
            self.leftElbowGearColor = 0
            # What gear the player wears on their left wrist. 0 = None, 1 = Forearm Band, 2 = Wrist Band, 3 = Protective Wrist Band, 4 = Double Wrist Band, 5 = Rubberband, 6 = Double Rubberband, 7 = Powerband, 8 = Wrist Wrap, 9 = Hand Wrap
            self.leftWristGear = 0
            # What color the player's left wrist gear is. 0 = White, 1 = Black, 2 = Team Color 1, 3 = Team Color 2
            self.leftWristGearColor1 = 0
            self.leftWristGearColor2 = 0
            # What gear the player wears on their left fingers. 0 = None, 1 = Finger Strap, 2 = Double Finger Strap, 3 = Long Index Strap, 4 = Long Middle Strap, 5 = Long Double Strap
            self.leftFingersGear = 0
            # What color the player's left finger gear is. 0 = White, 1 = Black, 2 = Team Color 1, 3 = Team Color 2
            self.leftFingersGearColor = 0
            # What gear the player wears on their right arm. 0 = None, 1 = Sleeve, 2 = Padded Sleeve, 3 = Short Sleeve, 4 = Shoulder Sleeve, 5 = Full Arm Sleeve, 6 = PowerWEB Armsleeve
            self.rightArmGear = 0
            # What color the player's right arm gear is. 0 = White, 1 = Black, 2 = Team Color 1, 3 = Team Color 2
            self.rightArmGearColor = 0
            # What gear the player wears on their right elbow. 0 = None, 1 = Pad, 2 = Sleeve, 3 = Small Band, 4 = Medium Band, 5 = High Band, 6 = Brace, 7 = Strap
            self.rightElbowGear = 0
            # What color the player's right elbow gear is. 0 = White, 1 = Black, 2 = Team Color 1, 3 = Team Color 2
            self.rightElbowGearColor = 0
            # What gear the player wears on their right wrist. 0 = None, 1 = Forearm Band, 2 = Wrist Band, 3 = Protective Wrist Band, 4 = Double Wrist Band, 5 = Rubberband, 6 = Double Rubberband, 7 = Powerband, 8 = Wrist Wrap, 9 = Hand Wrap
            self.rightWristGear = 0
            # What color the player's right wrist gear is. 0 = White, 1 = Black, 2 = Team Color 1, 3 = Team Color 2
            self.rightWristGearColor1 = 0
            self.rightWristGearColor2 = 0
            # What gear the player wears on their right fingers. 0 = None, 1 = Finger Strap, 2 = Double Finger Strap, 3 = Long Index Strap, 4 = Long Middle Strap, 5 = Long Double Strap
            self.rightFingersGear = 0
            # What color the player's right finger gear is. 0 = White, 1 = Black, 2 = Team Color 1, 3 = Team Color 2
            self.rightFingersGearColor = 0

            # What type of pressure shorts the player wears. 0 = None, 1 = Pressure Shorts, 2 = High Thigh Pad
            self.pressureShorts = 0
            # What color the player's shorts are. 0 = White, 1 = Black, 2 = Team Color 1, 3 = Team Color 2
            self.pressureShortsColor = 0
            # What gear the player wears on their left leg. 0 = None, 1 = Leg Sleeve, 2 = Calf Sleeve, 3 = Padded Calf Sleeve, 4 = Half Calf Sleeve, 5 = Hex Pad Half Calf Sleeve, 6 = Jordan Calf Sleeve, 7 = Mid Calf Sleeve
            self.leftLegGear = 0
            # What color the player's left leg gear is. 0 = White, 1 = Black, 2 = Team Color 1, 3 = Team Color 2
            self.leftLegGearColor = 0
            # What gear the player wears on their left knee. 0 = None, 1 = Pad, 2 = Hex Pad, 3 = Brace, 4 = Sleeve, 5 = Strap
            self.leftKneeGear = 0
            # What color the player's left knee gear is. 0 = White, 1 = Black, 2 = Team Color 1, 3 = Team Color 2
            self.leftKneeGearColor = 0
            # What gear the player wears on their left ankle. 0 = None, 1 = Ankle Brace, 2 = Ankle Wrap
            self.leftAnkleGear = 0
            # What color the player's left ankle gear is. 0 = White, 1 = Black, 2 = Team Color 1, 3 = Team Color 2
            self.leftAnkleGearColor = 0
            # What gear the player wears on their right leg. 0 = None, 1 = Leg Sleeve, 2 = Calf Sleeve, 3 = Padded Calf Sleeve, 4 = Half Calf Sleeve, 5 = Hex Pad Half Calf Sleeve, 6 = Jordan Calf Sleeve, 7 = Mid Calf Sleeve
            self.rightLegGear = 0
            # What color the player's right leg gear is. 0 = White, 1 = Black, 2 = Team Color 1, 3 = Team Color 2
            self.rightLegGearColor = 0
            # What gear the player wears on their right knee. 0 = None, 1 = Pad, 2 = Hex Pad, 3 = Brace, 4 = Sleeve, 5 = Strap
            self.rightKneeGear = 0
            # What color the player's right knee gear is. 0 = White, 1 = Black, 2 = Team Color 1, 3 = Team Color 2
            self.rightKneeGearColor = 0
            # What gear the player wears on their right ankle. 0 = None, 1 = Ankle Brace, 2 = Ankle Wrap
            self.rightAnkleGear = 0
            # What color the player's right ankle gear is. 0 = White, 1 = Black, 2 = Team Color 1, 3 = Team Color 2
            self.rightAnkleGearColor = 0
            # Determines the player's sock length, 0 = No Socks, 1 = Ankle Socks, 2 = Short Socks, 3 = Short Double Socks, 4 = Medium Socks, 5 = Medium Double Socks, 6 = Medium Long Socks, 7 = Long Socks, 8 = Striped Long Socks
            self.sockLength = 0


        # A member for storing height (in centimeters), as well as a function to
        # get height in 2k format and a function to generate a random height.
        def setHeight(self, _height):
            if ("'" in str(_height)):
                feet = int(str(_height)[0])
                inches = int(b.getStringAt(str(_height), 2))
                inches += (feet * 12)
                self.height = (inches * 2.54) # Convert inches to CM for RedMC
            else:
                self.height = _height
        def getHeight(self):
            feet = math.floor(self.height / 12)
            inches = self.height % 12
            returnString = str(feet) + "'" + str(inches)
            return returnString
        def genHeight(self,archetype):
                heightRange = archetype.heightRange
                minimum = heightRange[0]
                maximum = heightRange[1]

                randomHeight = random.randrange(minimum, maximum)
                self.height = randomHeight
    # Method for generating initial Appearance information.
    def genAppearance(self,height = False):
        self.appearance = self.Appearance()
        if(height != False):
            self.appearance.setHeight(height)

    # This struct class serves as a container to manage and hold all extra values that pertain to players
    # that could be customized at player creation time. Gen Sprite Values simply initializes the empty
    # variables - all sprite values come externally or are entered manually.
    class SpriteValues:
        def __init__(self):
            self.CreationAge = None # The age a player was created, such as Deletion Era or New Age
            self.RealityType = None # The "type" a player is, like in the medium game. 1 is real, 2 is fictional, 3 is us created.
            self.ExtraValue3 = None
            self.ExtraValue4 = None
            self.ExtraValue5 = None
            self.ExtraValue6 = None
            self.ExtraValue7 = None
            self.ExtraValue8 = None
            self.ExtraValue9 = None
            self.ExtraValue10 = None
            self.ExtraValue11 = None
            self.ExtraValue12 = None
            self.ExtraValue13 = None
            self.ExtraValue14 = None
            self.ExtraValue15 = None
            self.ExtraValue16 = None
            self.ExtraValue17 = None
            self.ExtraValue18 = None
            self.ExtraValue19 = None
            self.ExtraValue20 = None
            self.ExtraValue21 = None
            self.ExtraValue22 = None
            self.ExtraValue23 = None
            self.ExtraValue24 = None
            self.ExtraValue25 = None
            self.ExtraValue26 = None
            self.ExtraValue27 = None
            self.ExtraValue28 = None
            self.ExtraValue29 = None
            self.ExtraValue30 = None
            self.ExtraValue31 = None
            self.ExtraValue32 = None
            self.ExtraValue33 = None
            self.ExtraValue34 = None
            self.ExtraValue35 = None
            self.ExtraValue36 = None
            self.ExtraValue37 = None
            self.ExtraValue38 = None
            self.ExtraValue39 = None
            self.ExtraValue40 = None
            self.ExtraValue41 = None
            self.ExtraValue42 = None
            self.ExtraValue43 = None
            self.ExtraValue44 = None
            self.ExtraValue45 = None
            self.ExtraValue46 = None
            self.ExtraValue47 = None
            self.ExtraValue48 = None
            self.ExtraValue49 = None
            self.ExtraValue50 = None
            # This helper dictionary helps other external methods, like DataStorage, convert
            # values that have been defined into simple, dumb extra values for ease of use.
            self.extraValuesDefined = {
                "ExtraValue1" : self.CreationAge,
                "ExtraValue2" : self.RealityType,
                "ExtraValue3" : self.ExtraValue3,
                "ExtraValue4" : self.ExtraValue4,
                "ExtraValue5" : self.ExtraValue5,
                "ExtraValue6" : self.ExtraValue6,
                "ExtraValue7" : self.ExtraValue7,
                "ExtraValue8" : self.ExtraValue8,
                "ExtraValue9" : self.ExtraValue9,
                "ExtraValue10" : self.ExtraValue10,
                "ExtraValue11" : self.ExtraValue11,
                "ExtraValue12" : self.ExtraValue12,
                "ExtraValue13" : self.ExtraValue13,
                "ExtraValue14" : self.ExtraValue14,
                "ExtraValue15" : self.ExtraValue15,
                "ExtraValue16" : self.ExtraValue16,
                "ExtraValue17" : self.ExtraValue17,
                "ExtraValue18" : self.ExtraValue18,
                "ExtraValue19" : self.ExtraValue19,
                "ExtraValue20" : self.ExtraValue20,
                "ExtraValue21" : self.ExtraValue21,
                "ExtraValue22" : self.ExtraValue22,
                "ExtraValue23" : self.ExtraValue23,
                "ExtraValue24" : self.ExtraValue24,
                "ExtraValue25" : self.ExtraValue25,
                "ExtraValue26" : self.ExtraValue26,
                "ExtraValue27" : self.ExtraValue27,
                "ExtraValue28" : self.ExtraValue28,
                "ExtraValue29" : self.ExtraValue29,
                "ExtraValue30" : self.ExtraValue30,
                "ExtraValue31" : self.ExtraValue31,
                "ExtraValue32" : self.ExtraValue32,
                "ExtraValue33" : self.ExtraValue33,
                "ExtraValue34" : self.ExtraValue34,
                "ExtraValue35" : self.ExtraValue35,
                "ExtraValue36" : self.ExtraValue36,
                "ExtraValue37" : self.ExtraValue37,
                "ExtraValue38" : self.ExtraValue38,
                "ExtraValue39" : self.ExtraValue39,
                "ExtraValue40" : self.ExtraValue40,
                "ExtraValue41" : self.ExtraValue41,
                "ExtraValue42" : self.ExtraValue42,
                "ExtraValue43" : self.ExtraValue43,
                "ExtraValue44" : self.ExtraValue44,
                "ExtraValue45" : self.ExtraValue45,
                "ExtraValue46" : self.ExtraValue46,
                "ExtraValue47" : self.ExtraValue47,
                "ExtraValue48" : self.ExtraValue48,
                "ExtraValue49" : self.ExtraValue49,
                "ExtraValue50" : self.ExtraValue50
            }

        # Simply returns the value associated with a "dumb" extraValue label used by external functions.
        # For example, ExtraValue1 returns CreationAge.
        def getFromExtraValuesDefined(self,extraValue):
            return self.extraValuesDefined.get(extraValue)
    def genSpriteValues(self):
        self.spriteValues = self.SpriteValues()

    # Randomly generates an emotion value 25 - 99
    def genEmotion(self):
        self.emotion = random.randint(25,100)

    # This is a helper method designed to make the process of generating a player easier.
    # It will automatically generate various necessary stats to the Player object, that
    # would otherwise take multiple separate methods.
    def generatePlayer(self,firstName, lastName, setHeight = False, genPlayerCard = False):
        self.genInitialArchStats()
        self.genPlayStyle()
        self.genRarityInformation()

        if(setHeight != False):
            self.genAppearance(setHeight)
        else:
            self.genAppearance()
            self.appearance.genHeight(self.archetype)

        self.genEmotion()

        self.setName(firstName, lastName)

        self.genSignatureStats()
        self.genTendencyDict()

        self.genHotspotDict()
        self.genHotzoneDict()
        self.genSpriteValues()

        self.generateArrayOfEnchantments()
        self.readEnchantmentsIntoStats()

        if(genPlayerCard == True):
            newPlayerFile = open(str("Players\\" + firstName + " " + lastName + ".txt"), "w")
            newPlayerFile.write(self.getPlayerCard())



