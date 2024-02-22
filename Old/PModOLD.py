import random

# PMod (PlayerModifier) is a micro-language used for writing generated-on-demand formulas to adjust certain
# player values.

# VALID code lines
# @ParameterName = someValue                    Sets the value of ParameterName to someValue
# $VariableName = someValue                     Declares a variable with name VariableName, with value someValue
# !repeat16,`@ParameterName = someValue`        repeats the code contained in the brackets 16 times.
# !specialShotRareEpic                          simply adds a special shot, either rare or epic.
#
# OPERATORS:
#
# LEFT SIDE ONLY
# @(Object1,Object2,Object3) set the value of all three parameters simultaneously.
#
# BOTH SIDES
# ?[Object1,Object2,Object3] will randomly select and return a value between all listed objects.
# ?<1,5> will randomly select a number between 1 and 5.
# {ObjectList1/ObjectList2} will return all values in ObjectList1 that are not in ObjectList2
# {ObjectList1|ObjectList2} will return all values that are shared between ObjectList1 and ObjectList2
# {Num1+Num2} will return the sum of both numbers.

class PModCompiler:

    # Init method initializes our variables object, the localPlayerObject, and
    # our processedEffects list.
    def __init__(self,fileName,playerObject):
        file = open(fileName,"r")
        self.pmodFileLines = file.readlines()
        file.close()

        self.localPlayerObject = playerObject
        self.initializeVariables()
        self.parameters = {}

        # Stores a quickly-read list of all pmods present in a file.
        self.listOfAllPMods = []
        self.rareSpecialShots = {"Slayer" : [["Tyrion Lannister","36","71","Tyrion Lannister will go down as the greatest disappointment in 2k history, as he could never seem to shoot the ball into the net...like ever. God help this new player with Tyrion's cursed shot."],
                                          ["Danny Kowalczyk", "82", "60","A shot seen whenever new players arrived, Danny's sniper rifle bullet of a shot was completely unique at the time and made for some consistent performances before competitive play was introduced. Can this new player snipe their way to glory with Danny's shot?"],
                                          ["Lord Selwig Nara", "3", "21","Coined as the lock'n'load shot in the later stages of league, Lord Selwig Nara finally found some success near the end of his lengthy career with consistent outlet 3s. Can this new player rise faster than Selwig with his own shot?"],
                                              ["Jaqen H'Ghar","91","17","A victim of the time in which he was created, Jaqen never quite saw stardom which could sufficiently match his unrivaled raw talent. His rainbow-bending arch of a shot frightened all who had to defend against it. Will this new player succeed where Jaqen fell short?"],
                                              ["Uncle Chicken","3","4","One of only a few players to truly defy the attribute inflation of PostDEL, at just 70 overall, Uncle Chicken quickly rose to prominence as a legend with a barebones, easily repeatable shot. Can this new player be a darkhorse like Uncle Chicken once was?"],
                                              ["Jon Snow","91","38","A player who had ups and downs in what most would consider a successful career as a legend, Jon Snow rose up as a player who could simply get the job done with his laser-quick shooting form. Will this new player carry on the legacy of the King of the North?"]],
                              "Vigilante" : [["Mahatma Gandhi","66","5","If it weren't for his height and brutal speed, Gandhi could have been one of the all time greats with his under-handed, consistent delivery of 3 pt shots. Can this new player break past the faults of Gandhi with his majestic shot?"],
                                             ["Christian Shearcliff", "15", "38","If there's anything nice to say about Christian Shearcliff it might just be his shooting form, which almost took him to legend status. Can this new player be everything Chris wasn't?"],
                                             ["Ko Ga Die","97","51","Everyone knows that Ko Ga Die didn't become a legend because of his horrible shot, but hey, he did make it there anyways. Can this new player beat the odds with this wacky and obtrusive shot?"],
                                              ["Uncle Chicken","3","4","One of only a few players to truly defy the attribute inflation of PostDEL, at just 70 overall, Uncle Chicken quickly rose to prominence as a legend with a barebones, easily repeatable shot. Can this new player be a darkhorse like Uncle Chicken once was?"],
                                              ["Subway Club","127","59","Who would have thought that for just $12 you could order yourself an excellent basketball player? Everyone was shocked when Subway Club paced the later seasons of league in 3s and 3pt %, as he proved that the overall stat did not need to be in the 90s, or the 80s, or the 70s, or the 60s, or the 50s, to make a good player. Does this player have what it takes to shock everyone with Club's shot?"]],
                              "Medic" : [["Father Titticaca","16","16","Father Titticaca was an explosion of speed, rebounding, and exceptional shooting ability wrapped into one, and was the backbone of every team with which he played. Can this new player explode into the scene like Titti with his own shot?"],
                                         ["Old Sama Benlodan", "112", "42","Old Sama's carefully set shot will always go down as the pefect fold to his duo Bill Nye. Will this new player find similar success with the same shot?"],
                                         ["Daniel Stiefbold", "19", "72","One of the quirkier shots in 2k, Daniel Stiefbold went on a tear in the early days of 2k with his scoped-like release. Can this new player exceed expectations like Daniel did with such a strange, exotic shot?"]],
                              "Guardian" : [["The Hound","22","108","Raising his arms high into the air to launch the ball into the net, The Hound's classic shot practically dominated the control-oriented meta in the early days of 2k. Can this new player break out as the new superstar with The Hound's shot?"],
                                            ["Old Sama Benlodan", "112", "42","Old Sama's carefully set shot will always go down as the pefect fold to his duo Bill Nye. Will this new player find similar success with the same shot?"],
                                            ["Daniel Stiefbold", "19", "72","One of the quirkier shots in 2k, Daniel Stiefbold went on a tear in the early days of 2k with his scoped-like release. Can this new player exceed expectations like Daniel did with such a strange, exotic shot?"]],
                              "Engineer" : [["Gary the Thief","136","82","Gary's robotic dance of a shot eventually carried him to a semi-prominent legend status, which is more than anybody could have ever expected out of the Twitch streamer. Can this new player climb the ladder of greatness like Gary did?"],
                                            ["Mike Ehrmantraut", "110", "107","Known more for his control ability, Mike's clean and consistent shot often went unnoticed in the shadow of his colossal mid plays. Can this new player sink'em like Mike?"],
                                            ["Tyrion Lannister","36","71","Tyrion Lannister will go down as the greatest disappointment in 2k history, as he could never seem to shoot the ball into the net...like ever. God help this new player with Tyrion's cursed shot."]],
                              "Director" : [["Alex Somheil","16","2","A shot seen whenever new players arrived, Alex's unmistakablely clean shot proved valuable for the short time him and Danny were viable in competitive play. Can this new player exceed the consistent performances of Alex with his own shot?"],
                                            ["Gary the Thief", "136", "82","Gary's robotic dance of a shot eventually carried him to a semi-prominent legend status, which is more than anybody could have ever expected out of the Twitch streamer. Can this new player climb the ladder of greatness like Gary did?"],
                                            ["Mike Ehrmantraut", "110", "107","Known more for his control ability, Mike's clean and consistent shot often went unnoticed in the shadow of his colossal mid plays. Can this new player sink'em like Mike?"],
                                              ["Greg Pelzer","112","46","Always lingering in between legend and non-legend status, Greg Pelzer was the first player to be fully stripped of the title after it was granted to him. Will this new player find balance where Pelzer teetered off?"],
                                            ["Father Titticaca", "16", "16","Father Titticaca was an explosion of speed, rebounding, and exceptional shooting ability wrapped into one, and was the backbone of every team with which he played. Can this new player explode into the scene like Titti with his own shot?"],
                                            ["Christian Shearcliff", "15", "38","If there's anything nice to say about Christian Shearcliff it might just be his shooting form, which almost took him to legend status. Can this new player be everything Chris wasn't?"],
                                            ["Ko Ga Die","97","51","Everyone knows that Ko Ga Die didn't become a legend because of his horrible shot, but hey, he did make it there anyways. Can this new player beat the odds with this wacky and obtrusive shot?"]]}
        self.epicSpecialShots = {"Slayer": [["Jaquarius Nocturnal","146","6","Jaquarius didn't have the time to shine as much as his talent allowed him to, and everyone knew that he had what it took to be one of the Gods. His shot was as deadly as his footwork and rebounding. May this new player carry on a great legacy with Jay-Quay's shot."],
                                         ["Ser Davos", "10", "22","Ser Davos rode the line between non-legend and legend status for quite some time with his strange, side-spinning shot, finding decent success throughout his run. Can this new player succeed where Davos failed?"],
                                         ["Subway Jay","56","38","Subway Jay couldn't speak a lick of English, but if there was a language for basketball, he'd probably be a linguistics professor with his leg-kicking, ball-throwing, fun mess of a shot. Can this new player destroy the court like Jay killed it in the league?"],
                                         ["The Bro", "97", "64","From utter garbage to the heights of legendry, back down to somewhere in between, The Bro has used his exotic shot to reach the extreme highs and lows of the 2k universe. Can this new player ramp it up like The Bro did with this unusual shot?"],
                                         ["Ish Tickletits", "82", "47","Known for his legendary run with Warren's squad in the 2k league, Ish dominated the league for 2 seasons with his sniper rifle shot. Can this new player dominate the competitive scene similarly with this classic shot?"],
                                         ["Sprite Agent", "101", "79","Like a ghillie in the mist, Sprite Agent was a deadshot sniper with his bullet-like shooting form, finding himself major success in the late league days. Can this new player snipe the competition as Sprite Agent once did?"],
                                         ["Imperial Commander", "110", "57","Imperial Commander could probably shoot 50 basketballs in the span of 5 seconds with his laser-fast form, which made it incredibly hard to block the legendary player. May Imperial Commander's shot bless this new player with success and an increased will to murder Stormcloaks."],
                                         ["Ben Linus", "131", "54","Ben Linus has charitably gifted many a basketball to the Martians with his unbelievably high-arching shot, but when they did come down, they fell in the hoop for this late-game legend. Can this new player reach the stars like Ben did?"],
                                         ["Stacy Harper", "146", "56","Although Stacy never reached the expectations everyone had for him, his shot is still unrivaled in smoothness and pace of delivery. Can this new player break ground that Stacy never could with this buttery smooth shot?"],
                                         ["Albert Miller","125","4","Overshadowed by all-99 attribute scores, Albert Miller's crisp, high-floating shot may have had more of an impact on the god's career than scholars would give it credit for. Will this new player cement or destroy that theory?"]],
                              "Vigilante": [["Ser Davos","10","22","Ser Davos rode the line between non-legend and legend status for quite some time with his strange, side-spinning shot, finding decent success throughout his run. Can this new player succeed where Davos failed?"],
                                            ["Subway Jay","56","38","Subway Jay couldn't speak a lick of English, but if there was a language for basketball, he'd probably be a linguistics professor with his leg-kicking, ball-throwing, fun mess of a shot. Can this new player destroy the court like Jay killed it in the league?"],
                                            ["The Thor", "125", "34","Perhaps one of the fastest-to-legend players to date, Thor annihilated the competition with his high-arching shot in the murky days of 2k. Will this new player climb the ranks as fast as Thor with his own shot?"],
                                            ["Stacy Harper", "146", "56","Although Stacy never reached the expectations everyone had for him, his shot is still unrivaled in smoothness and pace of delivery. Can this new player break ground that Stacy never could with this buttery smooth shot?"],
                                            ["Fat Kid", "89", "23","Less known for his straight up shot and more for his acrobatic abilites, Fat Kid's classic shot is still a staple to 2k and the mark of one of the first great 3 pt shooters. Can this new player make a name for himself using Fat Kid's age-old shot?"],
                                            ["Morgan Freeman", "131", "34","You see those craters in the moon? Those are from Morgan Freeman launching the basketball into space every time he took a shot, finding him success as a multi-tool non-legend. Can this new player wreak havoc in space like Morgan did?"],
                                            ["Allfather Pickles","17","69","Going under the radar for most of his early days, Allfather truly broke out into stardom during the final stages of the league era, and it's a damn shame we couldn't witness more. Can this new player carry on such a short, but great legacy with Allfather's shot?"]],
                              "Medic": [["The Thinker","135","26","Nobody was having any second thinking thoughts about the Thinker with his extraordinarily good, control dominating gameplay and shot. Can this new player revive the glory days of The Thinker with his classic shot?"],
                                           ["Morgan Freeman", "131", "34","You see those craters in the moon? Those are from Morgan Freeman launching the basketball into space every time he took a shot, finding him success as a multi-tool non-legend. Can this new player wreak havoc in space like Morgan did?"],
                                           ["The Night King", "32", "71","At the very forefront of the early control meta, The Night King defined the meta as he raced to legend status with his clean shot and phenomenal rebounding skills faster than nearly anyone before him. Will this new player be able to say the same after using The Night King's shot?"]],
                              "Guardian": [["Jaquarius Nocturnal","146","6","Jaquarius didn't have the time to shine as much as his talent allowed him to, and everyone knew that he had what it took to be one of the Gods. His shot was as deadly as his footwork and rebounding. May this new player carry on a great legacy with Jay-Quay's shot."],
                                           ["The Night King", "32", "71","At the very forefront of the early control meta, The Night King defined the meta as he raced to legend status with his clean shot and phenomenal rebounding skills faster than nearly anyone before him. Will this new player be able to say the same after using The Night King's shot?"],
                                           ["The Thinker", "135", "26","Nobody was having any second thinking thoughts about the Thinker with his extraordinarily good, control dominating gameplay and shot. Can this new player revive the glory days of The Thinker with his classic shot?"],
                                           ["Imperial Commander", "110", "57","Imperial Commander could probably shoot 50 basketballs in the span of 5 seconds with his laser-fast form, which made it incredibly hard to block the legendary player. May Imperial Commander's shot bless this new player with success and an increased will to murder Stormcloaks."],
                                           ["The Thor", "125", "34","Perhaps one of the fastest-to-legend players to date, Thor anihilated the competition with his high-arching shot in the murky days of 2k. Will this new player climb the ranks as fast as Thor with his own shot?"],
                                           ["Morgan Freeman", "131", "34","You see those craters in the moon? Those are from Morgan Freeman launching the basketball into space every time he took a shot, finding him success as a multi-tool non-legend. Can this new player wreak havoc in space like Morgan did?"],
                                           ["Allfather Pickles","17","69","Going under the radar for most of his early days, Allfather truly broke out into stardom during the final stages of the league era, and it's a damn shame we couldn't witness more. Can this new player carry on such a short, but great legacy with Allfather's shot?"]],
                              "Engineer": [["The Night King","32","71","At the very forefront of the early control meta, The Night King defined the meta as he raced to legend status with his clean shot and phenomenal rebounding skills faster than nearly anyone before him. Will this new player be able to say the same after using The Night King's shot?"],
                                           ["Imperial Commander", "110", "57","Imperial Commander could probably shoot 50 basketballs in the span of 5 seconds with his laser-fast form, which made it incredibly hard to block the legendary player. May Imperial Commander's shot bless this new player with success and an increased will to murder Stormcloaks."],
                                           ["Manager Sneh", "127", "108","Despite his label as manager, Sneh was a god awful manager at Subway, but he did manage to sink in many a basketball with his smooth delivery. Can this new player manage to do the same?"]],
                              "Director": [["Manager Sneh","127","108","Despite his label as manager, Sneh was a god awful manager at Subway, but he did manage to sink in many a basketball with his smooth delivery. Can this new player manage to do the same?"],
                                           ["Imperial Commander", "110", "57","Imperial Commander could probably shoot 50 basketballs in the span of 5 seconds with his laser-fast form, which made it incredibly hard to block the legendary player. May Imperial Commander's shot bless this new player with success and an increased will to murder Stormcloaks."],
                                           ["Ben Linus", "131", "54","Ben Linus has charitably gifted many a basketball to the Martians with his unbelievably high-arching shot, but when they did come down, they fell in the hoop for this late-game legend. Can this new player reach the stars like Ben did?"]]}

        self.legendarySpecialShots = {"Slayer": [["Bill Nye","53","8","Bill Nye will go down as the greatest 2k player to ever touch the blacktop and his shot will be remembered just as fondly. This new player has hit the jackpot, and the question turns not to whether he will be great, but when he will."],
                                              ["Jacob Rogers", "6", "7","The ability to leap several feet higher than a normal human being, coupled with a short-statured legend was enough to carry Jake Rogers into God-tier for the entirety of 2ks run. Will the grace of Jake's leap and clean release aid this new player in doing the same?"],
                                              ["Timmy Nocturnal", "91", "42","An uncontested Timmy Nocturnal could take a shot from orbit, locked in a titanium cell, music blasting in his ears, and sink it without batting a fucking eye. Will this player ever miss with Timmy's buttery smooth shooting form?"],
					      ["Jimmy Nocturnal","50","45","The OG, first-ever legend, classic of all classics, Jimmy Nocturnal put everyone into a coffin when he hit the court with his unmistakably clean 3s. Can this new player rebirth what once was with Jimmy's timeless shot?"],
                                              ["Dan Harrison", "60", "44", "A shot from the heavens, Dan Harrison's smooth and hasty delivery left every player's jaw on the floor after his godlike dominance at the end of the last league season. Can this new player stand on the shoulders of a giant like Dan?"],
                                              ["Lipton Strawberry","91","103","Lipton Strawberry defined an entire era of 2k play with his unblockable, unmissable, destructively clean shot. Will this new player live up to the godly expectations of Lipton's perfect shot?"]],
                                   "Vigilante": [["Jimmy Nocturnal","50","45","The OG, first-ever legend, classic of all classics, Jimmy Nocturnal put everyone into a coffin when he hit the court with his unmistakably clean 3s. Can this new player rebirth what once was with Jimmy's timeless shot?"],
                                            ["Dan Harrison", "60", "44","A shot from the heavens, Dan Harrison's smooth and hasty delivery left every player's jaw on the floor after his godlike dominance at the end of the last league season. Can this new player stand on the shoulders of a giant like Dan?"],
                                            ["Dek Nara", "125", "20","Dek Nara literally pioneered the term God for 2k, and had to be literally banned from play for being so unbelievably good with his high-arching bomb of a shot. This new player should feel honored to carry on the Hawaiian peace God's classic shot."]],
                                   "Medic": [["Lipton Strawberry","91","103","Lipton Strawberry defined an entire era of 2k play with his unblockable, unmissable, destructively clean shot. Will this new player live up to the godly expectations of Lipton's perfect shot?"]],
                                   "Guardian": [["Jimmy Nocturnal","50","45","The OG, first-ever legend, classic of all classics, Jimmy Nocturnal put everyone into a coffin when he hit the court with his unmistakably clean 3s. Can this new player rebirth what once was with Jimmy's timeless shot?"],
                                              ["Lipton Strawberry","91","103","Lipton Strawberry defined an entire era of 2k play with his unblockable, unmissable, destructively clean shot. Will this new player live up to the godly expectations of Lipton's perfect shot?"],
                                            ["Dan Harrison", "60", "44","A shot from the heavens, Dan Harrison's smooth and hasty delivery left every player's jaw on the floor after his godlike dominance at the end of the last league season. Can this new player stand on the shoulders of a giant like Dan?"]],
                                   "Engineer": [["Abe Lincoln","91","53","There isn't much to say that hasn't already been said about Abe's silky smooth shot in the history of 2k. This new player should feel blessed to carry on one of the greatest shots ever introduced to 2k."],
                                           ["Bill Nye", "53", "8","Bill Nye will go down as the greatest 2k player to ever touch the blacktop and his shot will be remembered just as fondly. This new player has hit the jackpot, and the question turns not to whether he will be great, but when he will."]],
                                   "Director": [["Abe Lincoln","91","53","There isn't much to say that hasn't already been said about Abe's silky smooth shot in the history of 2k. This new player should feel blessed to carry on one of the greatest shots ever introduced to 2k."],
                                          ["Jacob Rogers", "6", "7","The ability to leap several feet higher than a normal human being, coupled with a short-statured legend was enough to carry Jake Rogers into God-tier for the entirety of 2ks run. Will the grace of Jake's leap and clean release aid this new player in doing the same?"],
                                           ["Bill Nye", "53", "8","Bill Nye will go down as the greatest 2k player to ever touch the blacktop and his shot will be remembered just as fondly. This new player has hit the jackpot, and the question turns not to whether he will be great, but when he will."]]}

        self.readFileInfo()

    # This method collects data on the PMod file, and creates a list of valid
    # PMods within the file without wasting resources computing each one.
    # It stores them in self.listOfAllPMods, which is an array of simple dictionaries
    # structured like this:
    #
    # {"PMOD_NAME" : "Caleb's Lemonade",
    #  "PMOD_DESCRIPTION" : "Caleb be drinkin' lemonade.",
    #  "PMOD_RARITY" : "Epic",
    #  "PMOD_ARCHETYPE_LOCK" : "Director",
    #  "PMOD_LINE_RANGE : [178,293]}
    #
    # This specifies that a pmod exists between lines 178 and 293 of the read file
    # that has all the characteristics listed. This makes it easy to select a pmod for generation,
    # THEN generate it.
    def readFileInfo(self):
        pmodLineStart = 0
        pmodName = ""
        pmodDescription = ""
        pmodRarity = ""
        pmodArchetype = ""
        lineCount = 0
        foundPMod = False
        for line in self.pmodFileLines:
            lineCount += 1
            line = line.lstrip(" ")
            line = line.lstrip("\t")
            line = line.strip("\n")
            # We do this if we're currently reading an pmod.
            if(foundPMod):
                # We've found the end of the pmod declaration, and can now store it.
                if(line.startswith("}")):
                    self.listOfAllPMods.append({"PMOD_NAME" : pmodName.strip().strip('"'),
                                                    "PMOD_DESCRIPTION" : pmodDescription.strip().strip('"'),
                                                    "PMOD_RARITY" : pmodRarity.strip().strip('"'),
                                                    "PMOD_ARCHETYPE_LOCK" : pmodArchetype.strip().strip('"'),
                                                    "PMOD_LINE_RANGE" : [pmodLineStart,lineCount]})

                    foundPMod = False
                    pmodName = ""
                    pmodDescription = ""
                    pmodRarity = ""
                    pmodArchetype = ""
                # If it starts with one of these, we've found a special, external pmod variable to
                # store.
                elif(line.startswith("*PMOD_NAME")):
                    foundEquals = False
                    for character in line:
                        if(foundEquals):
                            pmodName += character
                        elif(character == "="):
                            foundEquals = True
                elif (line.startswith("*PMOD_DESCRIPTION")):
                    foundEquals = False
                    for character in line:
                        if (foundEquals):
                            pmodDescription += character
                        elif (character == "="):
                            foundEquals = True
                elif (line.startswith("*PMOD_RARITY")):
                    foundEquals = False
                    for character in line:
                        if (foundEquals):
                            pmodRarity += character
                        elif (character == "="):
                            foundEquals = True
                elif (line.startswith("*PMOD_ARCHETYPE_LOCK")):
                    foundEquals = False
                    for character in line:
                        if (foundEquals):
                            pmodArchetype += character
                        elif (character == "="):
                            foundEquals = True
                else:
                    continue
            # If we find a line beginning with pmod{, then we've found a new
            # pmod to read.
            elif(line.startswith("pmod{")):
                pmodLineStart = lineCount
                foundPMod = True
            # Otherwise, we just skip to the next line.
            else:
                continue

    # This method compiles a single pmod, based on an already found range in the file
    # where the pmod exists.
    def compilePMod(self,listOfAllPModsIndex):
        thisPModDict = self.listOfAllPMods[listOfAllPModsIndex]
        pmodLineStart = thisPModDict.get("PMOD_LINE_RANGE")[0]
        pmodLineStop = thisPModDict.get("PMOD_LINE_RANGE")[1]

        self.parameters["PMOD_NAME"] = thisPModDict.get("PMOD_NAME").strip().strip('"')
        self.parameters["PMOD_DESCRIPTION"] = thisPModDict.get("PMOD_DESCRIPTION").strip().strip('"')
        self.parameters["PMOD_RARITY"] = thisPModDict.get("PMOD_RARITY").strip().strip('"')
        self.parameters["PMOD_ARCHETYPE_LOCK"] = thisPModDict.get("PMOD_ARCHETYPE_LOCK").strip().strip('"')

        lineCount = 0

        for line in self.pmodFileLines:
            lineCount += 1
            if(pmodLineStart <= lineCount <= pmodLineStop):
                line = line.lstrip(" ")
                line = line.lstrip("\t")
                line = line.strip("\n")
                # If we find a # character at the beginning of the line,
                # it's just a comment, and we skip to the next line.
                if(line.startswith("#")):
                    continue
                # If the line begins with @, that means we're setting a
                # parameter.
                elif(line.startswith("@")):
                    self.setParameter(line)
                # If the line begins with $, that means we're declaring or
                # redeclaring a variable.
                elif(line.startswith("$")):
                    self.declareVariable(line)
                # If the line begins with *, it signifies a special variable,
                # such as name or description. We skip this, as it's already
                # been read by self.readFileInfo
                elif(line.startswith("*")):
                    continue
                # These are special functions used only in specific cases, that change
                # the way we operate on this pmod and thus require special code.
                elif(line.startswith("!")):
                    if("!repeat" in line):
                        repeatCount = ""
                        internalExpression = ""
                        runningString = ""
                        foundInternalExpression = False
                        foundRepeatCount = False
                        for character in line:
                            # If we're currently reading the internal expression.
                            if(foundInternalExpression):
                                # Finding a second ` means we've now reached the end of the internalExpression.
                                if(character == "`"):
                                    internalExpression = runningString.strip()
                                    break
                                else:
                                    runningString += character
                            # We're currently reading the repeatCount.
                            elif(foundRepeatCount):
                                # This means we've found the begining of the internal expression, and
                                # have also found the end of our repeatCount.
                                if (character == "`"):
                                    foundInternalExpression = True
                                    repeatCount = int(self.processLiteralValues(runningString.strip()))
                                    foundRepeatCount = False
                                    runningString = ""
                                else:
                                    runningString += character
                            # This means we've found the beginning of our repeatCount.
                            elif(character in "0123456789&"):
                                foundRepeatCount = True
                                runningString += character
                            # Otherwise, we just skip past this character.
                            else:
                                continue
                            # If we find a number

                        # Now we run the internalExpression repeatCount times.
                        for i in range(repeatCount):
                            if(internalExpression.startswith("$")):
                                self.declareVariable(internalExpression)
                            elif(internalExpression.startswith("@")):
                                self.setParameter(internalExpression)
                    elif("!specialShot" in line):
                        rare = False
                        epic = False
                        legendary = False
                        if("Rare" in line):
                            rare = True
                        elif("Epic" in line):
                            epic = True
                        elif("Legendary" in line):
                            legendary = True
                        self.generateSpecialShot(raresAllowed=rare,epicsAllowed=epic,legendariesAllowed=legendary)
                # If the line starts with pmod, that's simply the declaration -
                # we already know we're reading a pmod, so we can skip this.
                elif(line.startswith("pmod")):
                    continue
                # If the line is empty, we obviously skip it.
                elif(line == ""):
                    continue
                # If a line contains only a closed curly brace, that means
                # our pmod declaration is complete.
                elif(line == "}"):
                    #isReadingPMod = False DONT THINK THIS IS NEEDED
                    continue
                # This means the line begins with an unknown character, so we
                # raise an error.
                else:
                    raise InvalidLineException(line,lineCount)
            else:
                continue

    # This method excepts a string that contains an expression to set a parameter, and it processes
    # it as such.
    def setParameter(self,setParameterString):

        operator = ""
        parameterExpression = ""
        readingLeftSide = True
        readingRightSide = False
        readingOperator = False
        runningString = ""
        for character in setParameterString:
            # This means we're on the right-hand side of the expression; the value
            # we are setting the parameter TO.
            if(readingRightSide):
                # We'll process this value into its literal value later - for now, we just
                # append every character we find to runningString.
                runningString += character
            # This means we're on the left-hand side of the expression; the name of the
            # parameter we're setting.
            elif(readingLeftSide):
                # We skip the initial @ operator, as we already know this is a parameter
                # set.
                if(character == "@"):
                    continue
                # This means we've finished reading the left-hand side of the expression, and
                # we now are reading the right-hand side of the expression.
                elif (character in "=-+"):
                    readingOperator = True
                    readingLeftSide = False
                    parameterExpression = runningString.strip().strip('"')
                    runningString = character
                # Otherwise, we simply append the character in the parameter name expression to our
                # running string.
                else:
                    runningString += character
            # This means we're currently reading just the operator of the expression.
            elif(readingOperator):
                # If we find a non-operator character, that means we're now done reading
                # the operator.
                if(character not in "+-="):
                    operator = runningString
                    readingOperator = False
                    readingRightSide = True
                    runningString = character
                else:
                    runningString += character
        # Now that the loop is finished, we have to transfer what we have stored
        # in runningString, which should be the non-literal parameter value, to
        # parameterValue.
        parameterValue = runningString.strip().strip('"')

        literalParameterExpression = self.processLiteralValues(parameterExpression)

        # This means this expression contains multiple parameters that need to be processed
        # in parallel.

        if ("(" in literalParameterExpression):
            listOfParametersToProcess = []
            foundParameterList = False
            runningString = ""
            for character in literalParameterExpression:
                # We're currently reading a parameter.
                if(foundParameterList == True):
                    # A comma means we've just finished reading a single parameter in the parameter list.
                    if(character == ","):
                        listOfParametersToProcess.append(runningString)
                        runningString = ""
                    # If we find a closed parantheses, that means we're now done reading parameters in this list.
                    elif(character == ")"):
                        listOfParametersToProcess.append(runningString)
                        runningString = ""
                        foundParameterList = False
                    # Otherwise, we simply append to the running string as we're still reading a single parameter.
                    else:
                        runningString += character
                # Finding a ( means we just found a new parameter to read.
                elif(character == "("):
                    foundParameterList = True
                else:
                    continue
        # Otherwise, this is just a single parameter.
        else:
            listOfParametersToProcess = [literalParameterExpression]


        # Finally, we process each parameter we found to process.
        for thisParameter in listOfParametersToProcess:
            # This means the pmod sets the parameter to value.
            if(operator == "="):
                self.parameters[thisParameter] = "=" + str(self.processLiteralValues(parameterValue))
            # This means the pmod adds the value to the existing parameter value.
            elif(operator == "+=" or operator == "-="):
                if(operator == "-="):
                    negativeMultiplier = -1
                else:
                    negativeMultiplier = 1

                literalParameterValue = int(self.processLiteralValues(parameterValue)) * negativeMultiplier
                if(self.parameters.get(thisParameter) != None):
                    if("=" in self.parameters.get(thisParameter)):
                        isSetParameter = True
                    else:
                        isSetParameter = False
                    newParameterValue = int(self.parameters.get(thisParameter).lstrip("+=")) + literalParameterValue
                    if(isSetParameter):
                        self.parameters[thisParameter] = "=" + str(newParameterValue)
                    else:
                        if(newParameterValue < 0):
                            self.parameters[thisParameter] = str(newParameterValue)
                        else:
                            self.parameters[thisParameter] = "+" + str(newParameterValue)
                else:
                    if(literalParameterValue < 0):
                        self.parameters[thisParameter] = str(literalParameterValue)
                    else:
                        self.parameters[thisParameter] = "+" + str(literalParameterValue)
            else:
                raise InvalidParameterOperatorException(runningString)

        self.testForUsedValues()

    # This method excepts a string that contains an expression to declare a variable, and it processes
    # it as such.
    def declareVariable(self,declareVariableString):

        variableName = ""
        # We loop through the string to parse what it means into two distinct
        # objects - variableName and variableValue
        foundEquals = False
        runningString = ""
        for character in declareVariableString:
            # This means we're on the right-hand side of the expression; the value
            # we are setting the variable TO.
            if(foundEquals):
                # We'll process this value into its literal value later - for now, we just
                # append every character we find to runningString.
                runningString += character
            # This means we've finished reading the left-hand side of the expression, and
            # we now are reading the right-hand side of the expression.
            elif(character == "="):
                foundEquals = True
                variableName = runningString.strip().strip('"')
                runningString = ""
            # This means we're on the left-hand side of the expression; the name of the
            # variable we're setting.
            else:
                # We skip the initial $ operator, as we already know this is a variable
                # declaration.
                if(character == "$"):
                    continue
                # Otherwise, we simply append the character in the variable name to our
                # running string.
                else:
                    runningString += character
        # Now that the loop is finished, we have to transfer what we have stored
        # in runningString, which should be the non-literal variable value, to
        # variableValue.
        variableValue = runningString.strip().strip('"')

        # Now we set the value of variable name to the literal value of our found variableValue.
        self.variables[variableName] = self.processLiteralValues(variableValue)

    # This special method simply generates a random special shot, and instantly applies its information to this pmod.
    def generateSpecialShot(self,raresAllowed=False,epicsAllowed=False,legendariesAllowed=False):
        archetype = self.parameters.get("PMOD_ARCHETYPE_LOCK")
        validShotDicts = []
        if(raresAllowed):
            for archetypeShots in self.rareSpecialShots:
                if(archetype == None or archetype == "None" or archetype == "Neutral"):
                    for shotDict in self.rareSpecialShots.get(archetypeShots):
                        validShotDicts.append(shotDict)
                elif(archetype.upper() == archetypeShots.upper()):
                    for shotDict in self.rareSpecialShots.get(archetypeShots):
                        validShotDicts.append(shotDict)
        if (epicsAllowed):
            for archetypeShots in self.epicSpecialShots:
                if (archetype == None or archetype == "None" or archetype == "Neutral"):
                    for shotDict in self.epicSpecialShots.get(archetypeShots):
                        validShotDicts.append(shotDict)
                elif (archetype.upper() == archetypeShots.upper()):
                    for shotDict in self.epicSpecialShots.get(archetypeShots):
                        validShotDicts.append(shotDict)
        if (legendariesAllowed):
            for archetypeShots in self.legendarySpecialShots:
                if (archetype == None or archetype == "None" or archetype == "Neutral"):
                    for shotDict in self.legendarySpecialShots.get(archetypeShots):
                        validShotDicts.append(shotDict)
                elif (archetype.upper() == archetypeShots.upper()):
                    for shotDict in self.legendarySpecialShots.get(archetypeShots):
                        validShotDicts.append(shotDict)

        selectedShotDict = validShotDicts[random.randrange(0,len(validShotDicts))]
        selectedShotForm = selectedShotDict[1]
        selectedShotBase = selectedShotDict[2]
        selectedShotDescription = selectedShotDict[3]

        self.setParameter("@AShtForm = " + selectedShotForm)
        self.setParameter("@AShtBase = " + selectedShotBase)
        self.parameters["PMOD_DESCRIPTION"] = self.parameters.get("PMOD_DESCRIPTION") + " ***" + selectedShotDescription +"***"

    # This method converts any variables and randomizer operators found in a string, either value or parameter, into their
    # literal stored values/generated values.
    def processLiteralValues(self, readString):
        firstReturnString = ""
        # Converting all variables into literal values.
        openVariableName = False
        runningVariableName = ""
        for character in readString:
            # This means that we're in the process of reading and converting a single variable into
            # it's literal value.
            if (openVariableName):
                # If closing & is found, find the literal value of the variable.
                if (character == "&"):
                    openVariableName = False
                    variableValue = self.variables.get(runningVariableName)
                    if (variableValue == None):
                        # raise VariableNotFoundException(runningVariableName)
                        runningVariableName = ""
                    else:
                        firstReturnString += self.variables.get(runningVariableName)
                        runningVariableName = ""
                # Otherwise, we're still reading a variable name.
                else:
                    runningVariableName += character
            # OpenVariableName being false, and character == & means we've found a new variable to read.
            elif (character == "&"):
                openVariableName = True
            # Otherwise, we just copy the literal value into the return string.
            else:
                firstReturnString += character
        if (openVariableName):
            raise ExpectedEndOfVariableAccessor(readString)


        secondReturnString = ""
        # Converting all Player Value accessors into their literal values.
        foundPlayerAccessor = False
        runningString = ""
        for character in firstReturnString:
            # This means we're currently reading a playerAccessor that we've already
            # found.
            if(foundPlayerAccessor):
                # Finding a second, closing percentage % symbol means we've reached the
                # end of this playerAccessor.
                if(character == "%"):
                    secondReturnString += str(self.localPlayerObject[runningString])
                    foundPlayerAccessor = False
                    runningString = ""
                # Otherwise, we're still reading the parameter name.
                else:
                    runningString += character
            # If character is %, that means we've found a new player parameter accessor.
            elif(character == "%"):
                foundPlayerAccessor = True
            # Otherwise, we're just reading the base string.
            else:
                secondReturnString += character




        thirdReturnString = ""
        # Converting all object operators into their resulting single objects.
        leftSideValues = []
        rightSideValues = []
        runningValueName = ""
        openObjectArith = False
        inLeftSide = True
        operator = ""
        for character in secondReturnString:
            # If we're currently reading an object arithmetic expression.
            if (openObjectArith):
                # This means we've found the end of the object Arithmetic string,
                # and can calculate and concatenate the result.
                if (character == "}"):
                    # First, we store the variable we were last reading.
                    rightSideValues.append(runningValueName)
                    runningValueName = ""

                    openObjectArith = False
                    resultValuesArray = []
                    if (operator == "|"):
                        for objectSingleValue in leftSideValues:
                            if (objectSingleValue in rightSideValues):
                                resultValuesArray.append(objectSingleValue)
                    elif (operator == "/"):
                        for objectSingleValue in leftSideValues:
                            if (objectSingleValue not in rightSideValues):
                                resultValuesArray.append(objectSingleValue)
                    elif(operator == "+"):
                        resultValuesArray.append(int(leftSideValues[0]) + int(rightSideValues[0]))
                    resultObjectValuesString = ""
                    for resultObjectValue in resultValuesArray:
                        resultObjectValuesString += str(resultObjectValue)
                        resultObjectValuesString += ","
                    thirdReturnString += resultObjectValuesString.rstrip(",")
                # If a comma is found, that means we just completed reading a single
                # object value, and can store it.
                elif (character == ","):
                    if (inLeftSide):
                        leftSideValues.append(runningValueName)
                        runningValueName = ""
                    else:
                        rightSideValues.append(runningValueName)
                        runningValueName = ""
                # If we find our special operating character, we store that as our operator.
                elif (character == "/" or character == "|" or character == "+"):
                    # First, we store the variable we were last reading.
                    leftSideValues.append(runningValueName)
                    runningValueName = ""

                    if (len(operator) != 0):
                        raise MultipleObjectArithmeticOperatorException(firstReturnString)
                    else:
                        operator = character
                        inLeftSide = False
                # Otherwise, we're currently reading a value.
                else:
                    runningValueName += character
            # If we find a {, that means we've found a new object arithmetic expression.
            elif (character == "{"):
                inLeftSide = True
                openObjectArith = True
                leftSideValues = []
                rightSideValues = []
                runningValueName = ""
                operator = ""
            # Otherwise, we simply add the character to the returnString.
            else:
                thirdReturnString += character

        fourthReturnString = ""
        # Converting all randomizer ? operators into a generated random value.
        runningObjectValue = ""
        minRandValue = 0
        maxRandValue = 0
        operatorType = None
        foundRandomOperator = False
        listOfRandomObjects = []
        for character in thirdReturnString:
            # If we're currently reading a random operator
            if(foundRandomOperator):
                # This means we've found the open bracket, the beginning of our expression
                # and the declaration of what type of random operation this is.
                if(character in "<["):
                    if(operatorType != None):
                        raise MultipleObjectArithmeticOperatorException(thirdReturnString)
                    else:
                        operatorType = character
                # Finding a closed bracket means we've reached the end of our random
                # expression.
                elif(character in ">]"):
                    if(operatorType == "["):
                        listOfRandomObjects.append(runningObjectValue)
                        fourthReturnString += listOfRandomObjects[random.randrange(0,len(listOfRandomObjects))]
                    elif(operatorType == "<"):
                        maxRandValue = int(runningObjectValue)
                        fourthReturnString += str(random.randrange(minRandValue,maxRandValue+1))
                    foundRandomOperator = False
                    operatorType = None
                    runningObjectValue = ""
                    minRandValue = 0
                    maxRandValue = 0
                    listOfRandomObjects = []
                # Finding a comma or colon means we've read a distinct objectValue in its
                # entirety, and we need to store it.
                elif(operatorType == "[" and character == ","):
                    listOfRandomObjects.append(runningObjectValue)
                    runningObjectValue = ""
                elif (operatorType == "<" and character == ","):
                    minRandValue = int(runningObjectValue)
                    runningObjectValue = ""
                # Otherwise, we're still reading an object value.
                else:
                    runningObjectValue += character
            # If we find ?, that means we've found a new random
            # expression, and can begin reading it.
            elif(character == "?"):
                foundRandomOperator = True
            else:
                fourthReturnString += character
        if (foundRandomOperator):
            raise ExpectedEndOfRandomizer(readString)

        return fourthReturnString

    # This method resets the variable dictionary, clears the USED_VALUE list, and
    # sets all constant variables to their defaults.
    def initializeVariables(self):
        primaryAttributesString = ""
        for attribute in self.localPlayerObject["Archetype"].primaryStats:
            primaryAttributesString += attribute + ","
        primaryAttributesString = primaryAttributesString.rstrip(",")

        secondaryAttributesString = ""
        for attribute in self.localPlayerObject["Archetype"].secondaryStats:
            secondaryAttributesString += attribute + ","
        secondaryAttributesString = secondaryAttributesString.rstrip(",")

        tertiaryAttributesString = ""
        for attribute in self.localPlayerObject["Archetype"].tertiaryStats:
            tertiaryAttributesString += attribute + ","
        tertiaryAttributesString = tertiaryAttributesString.rstrip(",")

        accentedAttributesString = ""
        for attribute in self.localPlayerObject["Archetype"].accentedAttributes:
            accentedAttributesString += attribute + ","
        accentedAttributesString = accentedAttributesString.rstrip(",")


        self.variables = {"PMOD_NAME" : "New_PMod",
                          "PMOD_DESCRIPTION": "This is a player modifier.",
                          "PMOD_RARITY": "Common",
                          "PMOD_ARCHETYPE_LOCK": "Engineer",

                          # All values pertaining to attributes.
                          "ALL_ATTRIBUTES" : "SShtIns,SShtCls,SShtMed,SSht3PT,SShtFT,SLayUp,SDunk,SStdDunk,SShtInT,SPstFdaway,SPstHook,SShtOfD,SBallHndl,SOffHDrib,SBallSec,SPass,SBlock,SSteal,SHands,SOnBallD,SOReb,SDReb,SOLowPost,SDLowPost,SOAwar,SDAwar,SConsis,SStamina,SSpeed,SQuick,SStrength,SVertical,SHustle,SDurab,SPOT,SEmotion",
                          "PRIMARY_ATTRIBUTES" : primaryAttributesString,
                          "SECONDARY_ATTRIBUTES" : secondaryAttributesString,
                          "TERTIARY_ATTRIBUTES" : tertiaryAttributesString,
                          "ACCENTED_ATTRIBUTES" : accentedAttributesString,
                          "SCORING_ATTRIBUTES" : "SShtCls,SLayUp,SPstFdaway,SPstHook,SOLowPost,SShtMed,SSht3PT,SShtInT,SShtOfD,SConsis",
                          "DEFENSIVE_ATTRIBUTES" : "SDLowPost,SStrength,SBlock,SOnBallD,SOReb,SDReb,SDAwar",
                          "CONTROL_ATTRIBUTES" : "SOffHDrib,SHands,SOAwar,SBallHndl,SHustle,SBallSec,SPass,SSpeed,SSteal,SQuick",

                          "USED_VALUES": ""
                          }

    # This method tests the current effect dictionary to find used and unused parameters.
    def testForUsedValues(self):
        for key in self.parameters:
            if(key not in self.variables.get("USED_VALUES")):
                if(len(self.variables.get("USED_VALUES")) == 0):
                    self.variables["USED_VALUES"] += key
                else:
                    self.variables["USED_VALUES"] += "," + key




class PModException(TypeError):
    pass
class NonIntegerValueProvidedException(PModException):
    def __init__(self, value, parameter):
        super().__init__("at parameter " + str(parameter) + ". When using the [] operator, an integer value to distribute is required. '" + str(value) + "' is not a valid integer value.")
class OperatorWithVariableDeclarationException(PModException):
    def __init__(self,variableValue):
        super().__init__("Variable value should not include an operator (+,-,=): " + str(variableValue))
class ExpectedEndOfVariableAccessor(PModException):
    def __init__(self,readinString):
        super().__init__("Expected '&' to end variable name, but instead got '" + readinString + ". Variables should be defined as &VariableName&.")
class ExpectedEndOfRandomizer(PModException):
    def __init__(self,readinString):
        super().__init__("Expected ']' to end randomize set, but instead got '" + readinString + ". Randomized sets should be defined as [Object,Object,Object...]")
class MultipleObjectArithmeticOperatorException(PModException):
    def __init__(self,objectArithExpression):
        super().__init__("Multiple operator found in a single object arithmetic expression: '" + objectArithExpression + "'")
class VariableNotFoundException(PModException):
    def __init__(self,variableName):
        super().__init__("Variable '" + variableName + "' not found in variable dictionary.")
class InvalidLineException(PModException):
    def __init__(self, line,lineCount):
        super().__init__("Found invalid line '" + line + "' at line " + str(lineCount) + " - lines should begin with #, $, or @.")
class InvalidParameterOperatorException(PModException):
    def __init__(self, line):
        super().__init__("Found invalid parameter operator in '" + line + "' - operator should be +=, -=, or =.")
class MultipleOperatorTypes(PModException):
    def __init__(self, line):
        super().__init__("Multiple operator types found in '" + line + "'.")