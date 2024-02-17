import random
import BaseFunctions as b
import Archetypes
import math
import WeightedDict
import PMod


# EXTRA VALUES:
# -CreationAge
# -RealityType
# -Biography
# -Race
# -Faction

class Player:

    #region === Init and Constants ===
    # Helper maps for easy conversion between ID numbers and their actual values.
    idMap = {
        "PlayStyle" : ["PG - Pass First","PG - Scoring","PG - Defensive","PG - 3PT Specialist","PG - Athletic","PG - All-Around",
                     "SG - Scoring","SG - Defensive","SG - 3PT Specialist","SG - Athletic","SG - Slashing","SG - All-Around",
                     "SF - Scoring","SF - Defensive","SF - 3PT Specialist","SF - Athletic","SF - Slashing","SF - Point Forward",
                     "SF - All-Around","PF - Defensive","PF - Athletic","PF - Back to Basket","PF - Faceup","PF - Rebounding",
                     "PF - All-Around","C - Defensive","C - Athletic","C - Back to Basket","C - Faceup","C - Rebounding","C - All-Around"],
        "PlayType1" : ["None","Isolation","P&R Ball Handler","P&R Roll Man","Post Up Low",
                    "Post Up High","Cutter","Mid Range","3 PT"],
        "PlayType2" : ["None","Isolation","P&R Ball Handler","P&R Roll Man","Post Up Low",
                    "Post Up High","Cutter","Mid Range","3 PT"],
        "PlayType3" : ["None","Isolation","P&R Ball Handler","P&R Roll Man","Post Up Low",
                    "Post Up High","Cutter","Mid Range","3 PT"],
        "PlayType4" : ["None","Isolation","P&R Ball Handler","P&R Roll Man","Post Up Low",
                    "Post Up High","Cutter","Mid Range","3 PT"],
        "SigSkill1" : ["None","Posterizer","Highlight Flim","Finisher","Acrobat","Spot Up Shooter","Shot Creator",
                          "Deadeye","Corner Specialist","Post Proficiency","Ankle Breaker","Post Playmaker","Dimer",
                          "Break Starter","Alley Oopers","Brick Wall","Lockdown Defender","Charge Card","Interceptor",
                          "Pick Pocketer","Active Hands","Eraser","Chase Down Artist","Bruiser","Hustle Points","Scrapper",
                          "Anti-Freeze","Microwave","Heat Rentention","Closer","Floor General","Defensive Anchor",
                          "Gatorade Prime Pack","On Court Coach"],
        "SigSkill2" : ["None","Posterizer","Highlight Flim","Finisher","Acrobat","Spot Up Shooter","Shot Creator",
                          "Deadeye","Corner Specialist","Post Proficiency","Ankle Breaker","Post Playmaker","Dimer",
                          "Break Starter","Alley Oopers","Brick Wall","Lockdown Defender","Charge Card","Interceptor",
                          "Pick Pocketer","Active Hands","Eraser","Chase Down Artist","Bruiser","Hustle Points","Scrapper",
                          "Anti-Freeze","Microwave","Heat Rentention","Closer","Floor General","Defensive Anchor",
                          "Gatorade Prime Pack","On Court Coach"],
        "SigSkill3" : ["None","Posterizer","Highlight Flim","Finisher","Acrobat","Spot Up Shooter","Shot Creator",
                          "Deadeye","Corner Specialist","Post Proficiency","Ankle Breaker","Post Playmaker","Dimer",
                          "Break Starter","Alley Oopers","Brick Wall","Lockdown Defender","Charge Card","Interceptor",
                          "Pick Pocketer","Active Hands","Eraser","Chase Down Artist","Bruiser","Hustle Points","Scrapper",
                          "Anti-Freeze","Microwave","Heat Rentention","Closer","Floor General","Defensive Anchor",
                          "Gatorade Prime Pack","On Court Coach"],
        "SigSkill4" : ["None","Posterizer","Highlight Flim","Finisher","Acrobat","Spot Up Shooter","Shot Creator",
                          "Deadeye","Corner Specialist","Post Proficiency","Ankle Breaker","Post Playmaker","Dimer",
                          "Break Starter","Alley Oopers","Brick Wall","Lockdown Defender","Charge Card","Interceptor",
                          "Pick Pocketer","Active Hands","Eraser","Chase Down Artist","Bruiser","Hustle Points","Scrapper",
                          "Anti-Freeze","Microwave","Heat Rentention","Closer","Floor General","Defensive Anchor",
                          "Gatorade Prime Pack","On Court Coach"],
        "SigSkill5" : ["None","Posterizer","Highlight Flim","Finisher","Acrobat","Spot Up Shooter","Shot Creator",
                          "Deadeye","Corner Specialist","Post Proficiency","Ankle Breaker","Post Playmaker","Dimer",
                          "Break Starter","Alley Oopers","Brick Wall","Lockdown Defender","Charge Card","Interceptor",
                          "Pick Pocketer","Active Hands","Eraser","Chase Down Artist","Bruiser","Hustle Points","Scrapper",
                          "Anti-Freeze","Microwave","Heat Rentention","Closer","Floor General","Defensive Anchor",
                          "Gatorade Prime Pack","On Court Coach"],
        "AShtForm" : ["Release 1", "Release 2", "Release 3", "Release 4", "Release 5", "Release 6", "Release 7",
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
        "AShtBase" : ["Jump Shot 1", "Jump Shot 2", "Jump Shot 3", "Jump Shot 4", "Jump Shot 5", "Jump Shot 6",
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
        "AFadeaway" : ["J Awkward", "J Big Kick", "J Big Kick 2", "J Big Kick 3", "J Lean", "J Small Kick",
                      "J Small Kick 2", "J Small Kick 3", "J Small Kick 4", "S Big Kick", "S Bowed", "S Grounded",
                      "S Hop Back", "S Kick", "S Late Kick", "S Side Hop", "S Small Kick", "S Small Step",
                      "S. Tight",
                      "K. Bryant", "K. Durant", "L. James", "W. Johnson", "S. Marion", "S. Nash", "D. Nowitzki",
                      "P. Pierce", "D. Rose", "E. Turner", "D. Wade", "M. Yao"],
        "AContestd" : ["Normal", "Big"],
        "AEscDrPlU" : ["Bowed", "Elite", "Elite 2", "Normal", "One Foot", "Stiff"],
        "ARunner" : ["Guard Default", "Guard Angled", "Guard Grounded", "Guard High Hold", "Guard High Push",
                    "Guard Hold", "Guard Normal", "Guard Quick Flick", "Guard Quick Release", "Guard Textbook",
                    "Swingman Default", "Swingman Angled", "Swingman Angle Hold", "Swingman Grounded",
                    "Swingman High",
                    "Swingman High Push", "Swingman Hold", "Swingman Straight", "Swingman Quick Release",
                    "Bigman Default", "Bigman Angled", "Bigman Athletic", "Bigman Extend", "Bigman Extend Follow",
                    "Bigman Flick", "Bigman Grounded", "Bigman Hard Flick", "Bigman High Push", "Bigman Hold",
                    "Bigman Textbook", "M. Jordan", "S. Nash", "T. Parker", "C. Paul"],
        "AFreeT" : ["Brave", "Brown", "Cal", "Cap", "Cougar", "Crusader", "Cue", "Cyclone", "Doc", "Gaucho", "Generic", "Hollywood", "Hund", "Lean", "Pitbull", "Push Up", "Robin", "Round", "Sib", "Snoop Dogg", "Spider", "Stag", "C. Aldrich", "L. Aldridge", "R. Allen", "G. Arenas", "R. Artest", "R. Barry", "M. Beasley", "A. Biedrins", "C. Billups", "L. Bird", "M. Bonner", "C. Boozer", "C. Bosh", "E. Brand", "K. Bryant", "V. Carter", "B. Cartwright", "W. Chamberlain", "J. Childress", "M. Conley", "J. Crawford", "G. Davis", "C. Drexler", "T. Duncan", "M. Dunleavy", "K. Durant", "M. Ellis", "P. Ewing", "D. Fisher", "K. Garnett", "M. Gasol", "P. Gasol", "R. Gay", "M. Ginobili", "B. Gordon",
                   "D. Granger", "R. Hamilton", "D. Harris", "C. Hayes", "A. Horford", "J. Hornacek", "D. Howard", "A. Iguodala", "S. Jackson", "L. James", "A. Jamison", "R. Jefferson", "J. Johnson", "M. Johnson", "O. Johnson", "W. Johnson", "M. Jordan", "J. Kidd", "D. Lee", "R. Lewis", "S. Livingston", "K. Love", "C. Maggette", "K. Malone", "S. Marion", "Kev. Martin", "A. Mason", "T. McGrady", "P. Millsap", "A. Mourning", "S. Nash", "Nene", "J. Noah", "D. Nowitzki", "E. Okafor", "J. O'Neal", "S. O'Neal", "T. Parker", "C. Paul", "T. Prince", "M. Redd", "J.J. Redick", "J. Richardson", "A. Rivers", "N. Robinson", "D. Rodman", "R. Rondo", "D. Rose", "J. Salmons", "L. Scola", "R. Sessions",
                   "J.R. Smith", "J. Smith", "J. Stockton", "P. Stojakovic", "R. Stuckey", "I. Thomas", "Ty. Thomas", "H. Turkoglu", "E. Turner", "D. Wade", "D. Waiters", "G. Wallace", "J. West", "De. Williams", "Marv. Williams"],
        "ADrPullUp" : ["Big", "Big 2", "Bowed", "Elite", "Elite 2", "Elite 3", "Elite 4", "Elite 5",
                      "Elite 6",
                      "Elite 7", "Elite 8", "Elite 9", "Normal", "Normal 2", "Normal 3", "Normal 4",
                      "Normal 5",
                      "Normal 6", "Normal 7", "Normal 8", "Normal 9", "Normal 10", "One Foot", "Stiff",
                      "Stiff 2", "Stiff 3", "Stiff 4", "Stiff 5", "Stiff 6"],
        "ASpinJmpr" : ["Big", "Big 2", "Normal", "Normal 2", "Normal 3", "Normal 4", "Normal 5", "Normal 6",
                      "Normal 7", "One Foot", "Stiff", "Stiff 2", "Stiff 3", "Stiff 4"],
        "AHopJmpr" : ["Big", "Big 2", "Normal", "Normal 2", "Normal 3", "Normal 4", "Normal 5", "Normal 6",
                     "Normal 7",
                     "Normal 8", "Normal 9", "Normal 10", "One Foot", "Stiff"],
        "APstFade" : ["Normal", "Fade 2", "Fade 3", "Fade 4", "Fade 5", "Fade 6", "Fade 7", "Fade 8", "Fade 9",
                     "M. Jordan", "K. Malone", "D. Nowitzki", "", "", "", ""],
        "APstHook" : ["Normal", "Hook 1", "Hook 2", "Hook 3", "Hook 4", "Hook 5", "Hook 6", "Hook 7", "Hook 8",
                     "Hook 9", "Hook 10", "Hook 11", "Classic Sky Hook", "", "", "", "", ""],
        "APstHopSh" : ["Normal", "Big", "Compact", "Crusader", "Deliberate", "Gaucho", "One Foot", "Quick"],
        "APstShmSh" : ["Normal", "Big", "One Foot"],
        "APstDrvStB" : ["Normal", "Compact", "Deliberate", "Quick"],
        "APstSpnStB" : ["Normal", "Compact", "Cougar", "Crusader", "Deliberate", "Quick"],
        "APstPrtct" : ["Normal", "Compact", "One Foot"],
        "APstPrtSpn" : ["Normal", "Compact", "Gaucho", "One Foot"],
        "AIsoCross" : ["Crossover 1", "Crossover 2", "Crossover 3", "Crossover 4", "Crossover 5", "Crossover 6"],
        "AIsoBhBck" : ["Behind Back 1", "Behind Back 2", "Behind Back 3", "Behind Back 4", "Behind Back 5",
                      "Behind Back 6", "Behind Back 7"],
        "AIsoSpin" : ["Spin 1", "Spin 2", "Spin 3", "Spin 4", "Spin 5", "Spin 6", "Spin 7"],
        "AIsoHesit" : ["Hesitation 1", "Hesitation 2", "Hesitation 3", "Hesitation 4"],
        "ALayUp" : ["Rookie Guard", "Pro Guard", "All-Star Guard", "J. Crawford", "Classic", "M. Ginobili",
                   "Air Jordan", "K. Bryant", "S. Nash", "T. Parker", "C. Paul", "D. Rose", "R. Rondo",
                   "D. Wade", "", "", "", "", "", ""],
        "AGoToDunk" : ["None", "Under Basket Rim Pulls", "Under Basket Athletic Flushes", "Under Basket One Handers", "Under Basket Bigman Slams", "Rim Grazers off One", "Rim Grazers off Two", "Basic One-Handers off One", "Basic Two-Handers off One", "Basic One-Handers off Two", "Basic Two-Handers off Two", "Bigman One-Handers off One", "Bigman One-Handers off Two", "Athletic One-Handers off One", "Athletic One-Handers off Two", "Hangs off One", "Hangs off Two", "Quick Drops", "Fist Pump Rim Pulls", "Bigman Tomahawks off One", "Bigman Tomahawks off Two", "Side Arm Tomahawks", "Straight Arm Tomahawks", "Cock Back Tomahawks", "Athletic Side Tomahawks", "Athletic Front tomahawks",
                      "Uber Athletic Tomahawks off One", "Uber Athletic Tomahawks off Two", "Leaning Slams", "Front Clutches", "Front Clutches off Two", "Side Clutches off One", "Side Clutches off Two", "Back Scratchers off One", "Back Scratchers off Two", "Back Scratching Rim Hangs", "Bigman Back Scratchers", "Quick Drop-in Back Scratchers", "Reverses off One", "Reverses off Two", "Clutch Reverse off One", "Clutch Reverse off Two", "Baseline Clutch Reverses", "Windmill Reverses", "Switch Hand Reverses", "Baseline Reverses off One", "Baseline Reverses off Two", "Windmill Baseline Reverses", "Clutch Baseline Reverses", "Bigman Baseline Reverses", "Windmills off One", "Leaning Windmills",
                      "Bigman Windmills", "Front Windmills", "Side Windmills", "Athletic Windmills", "Basic 360s", "Athletic 360s off One", "Athletic 360s off Two", "Under Leg 360s", "One Hand Spin Dunks", "Two Hand Spin Dunks", "Cradle Dunks", "Flashy Flushes", "Historic Jordan", "Historic Drexler"],
        "AIntHLght" : ["Default","L. James Anthem","D. Wade Anthem","Huddle Dance - Kicks","Huddle Dance - Pumps",
                      "Huddle Dance - Robot","Huddle Dance - Running","Huddle Dance - Shake","Huddle Dance - Kicks",
                      "Lineup - Back Slide","Lineup - Buzzerbeater","Lineup - Fake Out","Lineup - Get Low","Lineup - Jersey",
                      "Lineup - Jump","Lineup - Low Fives","Lineup - Power Up","Lineup - Push Ups","Lineup - The Wheel",
                      "Trick Shot - Behind Back","Trick Shot - No Look","Trick Shot - On Bended Knees","Trick Shot - Rock the Floor",
                      "Trick Shot - The Runner","Trick Shot - Turn Around","Trick Shot - Underhand"],
        "AIntPreG1" : ["Default","T. Duncan Rim Hang","B. Griffin Rim Hang","K. Garnett Bang Head","L. James Salute","D. Wade Rim Hang",
                      "D. Wade Boxing","L. James Handshake","Ankle Breaker","Boxing Exercise","Boxing Match","Bump and Jump","Bunny Hop",
                      "Cabbage Patch","Double Kneel","Foot Grab","Foot Lock","Gone Fishing","Home Run","Kickoff","Left Hanging",
                      "Left Hanging Again","On Camera","Punching Bag","Rim Hang - Flex","Rim Hang - Swing Out","Rim Hang - Tap","Robot",
                      "Salsa","Shake Up","Shove Off","Superhero","Snap Dance","The Wheelbarrow","Touchdown Pass","Trust My Buddy"],
        "AIntPreG2" : ["Default","T. Duncan Rim Hang","B. Griffin Rim Hang","K. Garnett Bang Head","L. James Salute","D. Wade Rim Hang",
                      "D. Wade Boxing","L. James Handshake","Ankle Breaker","Boxing Exercise","Boxing Match","Bump and Jump","Bunny Hop",
                      "Cabbage Patch","Double Kneel","Foot Grab","Foot Lock","Gone Fishing","Home Run","Kickoff","Left Hanging",
                      "Left Hanging Again","On Camera","Punching Bag","Rim Hang - Flex","Rim Hang - Swing Out","Rim Hang - Tap","Robot",
                      "Salsa","Shake Up","Shove Off","Superhero","Snap Dance","The Wheelbarrow","Touchdown Pass","Trust My Buddy"],
        "AIntPreT1" : ["Default","R. Allen Powder","C. Anthony Inspect Ball","C. Anthony Handshake","C. Billups Inspect Ball",
                      "C. Boozer Smack Table","C. Boozer Inspect Ball","K. Bryant Teammate Hug","K. Bryant Powder","V. Carter Rim Pull-up",
                      "T. Duncan Inspect Ball","K. Durant Shoulder Brush","K. Durant Handshake","K. Garnett Hype Crowd","K. Garnett Powder",
                      "D. Howard Post Play","D. Howard Handshake","L. James Inspect Ball","L. James Powder","M. Jordan Powder",
                      "M. Jordan Powder 2","J. Lin Textbook","D. Nowitzki Low Fives","D. Nowitzki Tie Shoes","C. Paul Teammate Hug",
                      "D. Wade Hype Crowd","D. Wade Handshake","Backflip Grounded","Backflip Elevated","Championship Belt","Chicken Dance",
                      "Dunk On You","Get Hip","Home Run Hit","I Can't Hear You","Kneel and Focus","Push Ups","Take A Bow","The Robot",
                      "The Salsa","Hand Stand","Hype Crowd - Let's Hear It","Hype Crowd - Chest Pump","Hype Crowd - Rally","Hype Crowd - Louder",
                      "Hype Crowd - I Can't Hear You","Hype Crowd - Our House","Powder - Routine Basic","Powder - Routine Spread","Powder - Chest Tap",
                      "Powder - Point To Sky","Stanchion - Head Bang","Stanchion - Beat It","Stanchion - Punch Out 1","Stanchion - Punch Out 2",
                      "Stanchion - Focus","Stanchion - Punch Kick","Stanchion - Punch Bag","Stanchion - Lean Back","Stanchion - Wax On",
                      "With Ball - Dance","With Ball - Around Back","With Ball - Bowling","With Ball - Baseball","With Ball - Football",
                      "With Ball - Hit Head","With Ball - Scratch","With Ball - Weigh It"],
        "AIntPreT2" : ["Default","R. Allen Powder","C. Anthony Inspect Ball","C. Anthony Handshake","C. Billups Inspect Ball",
                      "C. Boozer Smack Table","C. Boozer Inspect Ball","K. Bryant Teammate Hug","K. Bryant Powder","V. Carter Rim Pull-up",
                      "T. Duncan Inspect Ball","K. Durant Shoulder Brush","K. Durant Handshake","K. Garnett Hype Crowd","K. Garnett Powder",
                      "D. Howard Post Play","D. Howard Handshake","L. James Inspect Ball","L. James Powder","M. Jordan Powder",
                      "M. Jordan Powder 2","J. Lin Textbook","D. Nowitzki Low Fives","D. Nowitzki Tie Shoes","C. Paul Teammate Hug",
                      "D. Wade Hype Crowd","D. Wade Handshake","Backflip Grounded","Backflip Elevated","Championship Belt","Chicken Dance",
                      "Dunk On You","Get Hip","Home Run Hit","I Can't Hear You","Kneel and Focus","Push Ups","Take A Bow","The Robot",
                      "The Salsa","Hand Stand","Hype Crowd - Let's Hear It","Hype Crowd - Chest Pump","Hype Crowd - Rally","Hype Crowd - Louder",
                      "Hype Crowd - I Can't Hear You","Hype Crowd - Our House","Powder - Routine Basic","Powder - Routine Spread","Powder - Chest Tap",
                      "Powder - Point To Sky","Stanchion - Head Bang","Stanchion - Beat It","Stanchion - Punch Out 1","Stanchion - Punch Out 2",
                      "Stanchion - Focus","Stanchion - Punch Kick","Stanchion - Punch Bag","Stanchion - Lean Back","Stanchion - Wax On",
                      "With Ball - Dance","With Ball - Around Back","With Ball - Bowling","With Ball - Baseball","With Ball - Football",
                      "With Ball - Hit Head","With Ball - Scratch","With Ball - Weigh It"],
        "Personality" : ["Unpredictable","Laid Back","Neutral","Expressive"]
        }
    extraValuesMap = {
                "CreationAge" : "ExtraValue1", # The age a player was created, such as Deletion Era or New Age
                "RealityType" : "ExtraValue2", # The "type" a player is, like in the medium game. 1 is real, 2 is fictional, 3 is us created.
                "Biography" : "ExtraValue3", # The biography of the player - flavor text.
                "Race" : "ExtraValue4", # The Player's race
                "Faction" : "ExtraValue5", # The Player's faction
                "ExtraValue6" : "ExtraValue6",
                "ExtraValue7" : "ExtraValue7",
                "ExtraValue8" : "ExtraValue8",
                "ExtraValue9" : "ExtraValue9",
                "ExtraValue10" : "ExtraValue10",
                "ExtraValue11" : "ExtraValue11",
                "ExtraValue12" : "ExtraValue12",
                "ExtraValue13" : "ExtraValue13",
                "ExtraValue14" : "ExtraValue14",
                "ExtraValue15" : "ExtraValue15",
                "ExtraValue16" : "ExtraValue16",
                "ExtraValue17" : "ExtraValue17",
                "ExtraValue18" : "ExtraValue18",
                "ExtraValue19" : "ExtraValue19",
                "ExtraValue20" : "ExtraValue20",
                "ExtraValue21" : "ExtraValue21",
                "ExtraValue22" : "ExtraValue22",
                "ExtraValue23" : "ExtraValue23",
                "ExtraValue24" : "ExtraValue24",
                "ExtraValue25" : "ExtraValue25",
                "ExtraValue26" : "ExtraValue26",
                "ExtraValue27" : "ExtraValue27",
                "ExtraValue28" : "ExtraValue28",
                "ExtraValue29" : "ExtraValue29",
                "ExtraValue30" : "ExtraValue30",
                "ExtraValue31" : "ExtraValue31",
                "ExtraValue32" : "ExtraValue32",
                "ExtraValue33" : "ExtraValue33",
                "ExtraValue34" : "ExtraValue34",
                "ExtraValue35" : "ExtraValue35",
                "ExtraValue36" : "ExtraValue36",
                "ExtraValue37" : "ExtraValue37",
                "ExtraValue38" : "ExtraValue38",
                "ExtraValue39" : "ExtraValue39",
                "ExtraValue40" : "ExtraValue40",
                "ExtraValue41" : "ExtraValue41",
                "ExtraValue42" : "ExtraValue42",
                "ExtraValue43" : "ExtraValue43",
                "ExtraValue44" : "ExtraValue44",
                "ExtraValue45" : "ExtraValue45",
                "ExtraValue46" : "ExtraValue46",
                "ExtraValue47" : "ExtraValue47",
                "ExtraValue48" : "ExtraValue48",
                "ExtraValue49" : "ExtraValue49",
                "ExtraValue50" : "ExtraValue50"}

    # Init method for initializing the value dictionary to default values.
    def __init__(self):
        # SpriteID, the unique ID value used to distinguish between all Players.
        self.__spriteID = -1  # -1 Means spriteID has not yet been set, and must be set immediately.

        # Holder for all values in this Player object.
        self.vals = {"First_Name": "",
                    "Last_Name": "",
                    "NickName": "",
                    "Archetype": None, # Default to none - archetype MUST be set.
                    "Rarity": "Common", # Default to common rarity
                    "CAP_Nick": 0,
                    "ArtifactName": None, # Artifacts default to none, and can only be added by generation.
                    "ArtifactDesc": None, # Artifacts default to none, and can only be added by generation.
                    "ArtifactCode": None, # Artifacts default to none, and can only be added by generation.
                    "Hand": 1, # Default is right
                    "Height": 70, # Default is 5'10
                    "Weight": 185.0, # Default is 185
                    "PortrID": 9999,
                    "GenericF": 1,
                    "CF_ID": -1, # NEVER use CF_ID, only for players with actual pictures in base game
                    "AudioID_M": 0,
                    "NmOrder": 0, # Default last name shown
                    "SkinTone": 0, # Default is black
                    "Muscles": 0, # Default is "Buff" (the weaker one)
                    "EyeColor": 0, # Default is Blue
                    "Bodytype": 0, # Default is slim
                    "Clothes": 0, # Default is Jersey
                    "Number": 1, # Default jersey number of 1
                    "Pos": None, # Positions are DIRECTLY tied to archetype, and therefore archetype must first be set. No default.
                    "SecondPos": None, # Positions are DIRECTLY tied to archetype, and therefore archetype must first be set. No default.
                    "PlayInitor": None, # Positions are DIRECTLY tied to archetype, and therefore archetype must first be set. No default.
                    "PlayStyle": 0, # Default of PG - Pass First play style
                    "PlayType1": 0, # Default to having no play types
                    "PlayType2": 0,
                    "PlayType3": 0,
                    "PlayType4": 0,
                    "SShtIns": 60, # Default to minimum value for each attribute
                    "SShtCls": 50,
                    "SShtMed": 25,
                    "SSht3PT": 25,
                    "SShtFT": 25,
                    "SLayUp": 25,
                    "SDunk": 25,
                    "SStdDunk": 25,
                    "SShtInT": 25,
                    "SPstFdaway": 25,
                    "SPstHook": 25,
                    "SShtOfD": 25,
                    "SBallHndl": 25,
                    "SOffHDrib": 25,
                    "SBallSec": 25,
                    "SPass": 25,
                    "SBlock": 25,
                    "SSteal": 25,
                    "SHands": 25,
                    "SOnBallD": 25,
                    "SOReb": 25,
                    "SDReb": 25,
                    "SOLowPost": 25,
                    "SDLowPost": 25,
                    "SOAwar": 25,
                    "SDAwar": 25,
                    "SConsis": 25,
                    "SStamina": 25,
                    "SSpeed": 25,
                    "SQuick": 25,
                    "SStrength": 25,
                    "SVertical": 25,
                    "SHustle": 25,
                    "SDurab": 25,
                    "SPOT": 25,
                    "SEmotion": 25,
                    "SigSkill1": 0, # Default to having no signature skills
                    "SigSkill2": 0,
                    "SigSkill3": 0,
                    "SigSkill4": 0,
                    "SigSkill5": 0,
                    "TShtTend": 0, # All tendencies default to 0.
                    "TInsShots": 0,
                    "TCloseSht": 0,
                    "TMidShots": 0,
                    "T3PTShots": 0,
                    "TPutbacks": 0,
                    "TDriveLn": 0,
                    "TPullUp": 0,
                    "TPumpFake": 0,
                    "TTrplThrt": 0,
                    "TTTShot": 0,
                    "TNoTT": 0,
                    "TStrghtDr": 0,
                    "TSizeUp": 0,
                    "THesitat": 0,
                    "TDriveRvL": 0,
                    "TCrossov": 0,
                    "TSpin": 0,
                    "TStepBack": 0,
                    "THalfSpin": 0,
                    "TDblCross": 0,
                    "TBhndBack": 0,
                    "THesCross": 0,
                    "TInAndOut": 0,
                    "TDPSimpDr": 0,
                    "TAttackB": 0,
                    "TPassOut": 0,
                    "THopStep": 0,
                    "TSpinLUp": 0,
                    "TEuroStep": 0,
                    "TRunner": 0,
                    "TFadeaway": 0,
                    "TStpbJmpr": 0,
                    "TSpinJmpr": 0,
                    "TDunkvLU": 0,
                    "TAlleyOop": 0,
                    "TUseGlass": 0,
                    "TDrawFoul": 0,
                    "TStpThrgh": 0,
                    "TVShCrash": 0,
                    "TUsePick": 0,
                    "TSetPick": 0,
                    "TIsolat": 0,
                    "TUseOBScr": 0,
                    "TSetOBScr": 0,
                    "TSpotUp": 0,
                    "TPostUp": 0,
                    "TGiveGo": 0,
                    "TTouches": 0,
                    "TPostSpn": 0,
                    "TPostDrv": 0,
                    "TPostAgBd": 0,
                    "TLeavePost": 0,
                    "TPostDrpSt": 0,
                    "TPostFaceU": 0,
                    "TPostBDown": 0,
                    "TPostShots": 0,
                    "TPostHook": 0,
                    "TPostFdawy": 0,
                    "TPostShmSh": 0,
                    "TPostHopSh": 0,
                    "TFlshPass": 0,
                    "TThrowAO": 0,
                    "THardFoul": 0,
                    "TTakeChrg": 0,
                    "TPassLane": 0,
                    "TOnBalStl": 0,
                    "TContShot": 0,
                    "TCommFoul": 0,
                    "HIso3PLft": 0, # All hotspots default to 0.
                    "HIso3PCtr": 0,
                    "HIso3PRgt": 0,
                    "HIsoHPLft": 0,
                    "HIsoHPCtr": 0,
                    "HIsoHPRgt": 0,
                    "HP_rLCrnr": 0,
                    "HP_rLWing": 0,
                    "HP_rTopOA": 0,
                    "HP_rRWing": 0,
                    "HP_rRCrnr": 0,
                    "HSpt3PLCr": 0,
                    "HSpt3PLWg": 0,
                    "HSpt3PTop": 0,
                    "HSpt3PRWg": 0,
                    "HSpt3PRCr": 0,
                    "HSptMdLBl": 0,
                    "HSptMdLWg": 0,
                    "HSptMdCtr": 0,
                    "HSptMdRWg": 0,
                    "HSptMdRBl": 0,
                    "HPstRHigh": 0,
                    "HPstRLow": 0,
                    "HPstLHigh": 0,
                    "HPstLLow": 0,
                    "HZ1": 1, # All players have all zones as neutral by default.
                    "HZ2": 1,
                    "HZ3": 1,
                    "HZ4": 1,
                    "HZ5": 1,
                    "HZ6": 1,
                    "HZ7": 1,
                    "HZ8": 1,
                    "HZ9": 1,
                    "HZ10": 1,
                    "HZ11": 1,
                    "HZ12": 1,
                    "HZ13": 1,
                    "HZ14": 1,
                    "AShtForm": 0, # Default to 0 for each signature form animation.
                    "AShtBase": 0,
                    "AFadeaway": 0,
                    "AContestd": 0,
                    "AEscDrPlU": 0,
                    "ARunner": 0,
                    "AFreeT": 0,
                    "ADrPullUp": 0,
                    "ASpinJmpr": 0,
                    "AHopJmpr": 0,
                    "APstFade": 0,
                    "APstHook": 0,
                    "APstHopSh": 0,
                    "APstShmSh": 0,
                    "APstDrvStB": 0,
                    "APstSpnStB": 0,
                    "APstPrtct": 0,
                    "APstPrtSpn": 0,
                    "AIsoCross": 0,
                    "AIsoBhBck": 0,
                    "AIsoSpin": 0,
                    "AIsoHesit": 0,
                    "ALayUp": 0,
                    "AGoToDunk": 0,
                    "ADunk2": 0,
                    "ADunk3": 0,
                    "ADunk4": 0,
                    "ADunk5": 0,
                    "ADunk6": 0,
                    "ADunk7": 0,
                    "ADunk8": 0,
                    "ADunk9": 0,
                    "ADunk10": 0,
                    "ADunk11": 0,
                    "ADunk12": 0,
                    "ADunk13": 0,
                    "ADunk14": 0,
                    "ADunk15": 0,
                    "AIntHLght": 0,
                    "AIntPreG1": 0,
                    "AIntPreG2": 0,
                    "AIntPreT1": 0,
                    "AIntPreT2": 0,
                    "GHeadband": 0, # Default no headband
                    "GHdbndLg": 4, # Default of no headband logo
                    "GUndrshrt": 0, # Default to not having any gear
                    "GUndrsCol": 0, # Default to all gear being white
                    "GLeftArm": 0,
                    "GLArmCol": 0,
                    "GLeftElb": 0,
                    "GLElbCol": 0,
                    "GLeftWrst": 0,
                    "GLWrstC1": 0,
                    "GLWrstC2": 0,
                    "GLeftFngr": 0,
                    "GLFngrCol": 0,
                    "GRghtArm": 0,
                    "GRArmCol": 0,
                    "GRghtElb": 0,
                    "GRElbCol": 0,
                    "GRghtWrst": 0,
                    "GRWrstC1": 0,
                    "GRWrstC2": 0,
                    "GRghtFngr": 0,
                    "GRFngrCol": 0,
                    "GPresShrt": 0,
                    "GPrsShCol": 0,
                    "GLeftLeg": 0,
                    "GLLegCol": 0,
                    "GLeftKnee": 0,
                    "GLKneeCol": 0,
                    "GLeftAnkl": 0,
                    "GLAnklCol": 0,
                    "GRghtLeg": 0,
                    "GRLegCol": 0,
                    "GRghtKnee": 0,
                    "GRKneeCol": 0,
                    "GRghtAnkl": 0,
                    "GRAnklCol": 0,
                    "GSockLngh": 0,
                    "GShsBrLck": 0,
                    "GShsBrand": 0,
                    "GShsModel": 0,
                    "GShsUCusC": 0,
                    "GShsTHC1": 0,
                    "GShsTHC2": 1,
                    "GShsTAC1": 0,
                    "GShsTAC2": 1,
                    "GShsHCol1": "D7D7D7", # TODO maybe add shoe color support?
                    "GShsHCol2": "282828",
                    "GShsHCol3": "878787",
                    "GShsACol1": "282828",
                    "GShsACol2": "D7D7D7",
                    "GShsACol3": "878787",
                    "CAP_FaceT": 0, # Default 0 face type.
                    "CAP_Hstl": 0, # Default bald
                    "CAP_Hcol": 0, # Default black hair
                    "CAP_Hlen": 0, # Default of 0 hair length
                    "CAP_BStyle": 0, # Default of no facial hair
                    "CAP_Moust": 0,
                    "CAP_Goatee": 0,
                    "CAP_Fhcol": 0, # Default of black facial hair
                    "CAP_Eyebr": 0, # Default of no eyebrows
                    "CAP_T_LftN": 0, # Default of no tattoos
                    "CAP_T_LftS": 0,
                    "CAP_T_RgtS": 0,
                    "CAP_T_LftB": 0,
                    "CAP_T_RgtB": 0,
                    "CAP_T_LftF": 0,
                    "CAP_T_RgtF": 0,
                    "HParam1": 0, # All CAP Headshape values default to 0.
                    "HParam2": 0,
                    "HdBrwHght": 0,
                    "HdBrwWdth": 0,
                    "HdBrwSlpd": 0,
                    "HdNkThck": 0,
                    "HdNkFat": 0,
                    "HdChnLen": 0,
                    "HdChnWdth": 0,
                    "HdChnProt": 0,
                    "HdJawSqr": 0,
                    "HdJawWdth": 0,
                    "HdChkHght": 0,
                    "HdChkWdth": 0,
                    "HdChkFull": 0,
                    "HdDefinit": 0,
                    "MtULCurve": 0,
                    "MtULThick": 0,
                    "MtULProtr": 0,
                    "MtLLCurve": 0,
                    "MtLLThick": 0,
                    "MtLLProtr": 0,
                    "MtSzHght": 0,
                    "MtSzWdth": 0,
                    "MtCrvCorn": 0,
                    "ErHeight": 0,
                    "ErWidth": 0,
                    "ErEarLobe": 0,
                    "ErTilt": 0,
                    "NsNsHght": 0,
                    "NsNsWdth": 0,
                    "NsNsProtr": 0,
                    "NsBnBridge": 0,
                    "NsBnDefin": 0,
                    "NsBnWdth": 0,
                    "NsTipHght": 0,
                    "NsTipWdth": 0,
                    "NsTipTip": 0,
                    "NsTipBnd": 0,
                    "NsNtHght": 0,
                    "NsNtWdth": 0,
                    "EsFrmOpen": 0,
                    "EsFrmSpac": 0,
                    "EsFrmLwEl": 0,
                    "EsFrmUpEl": 0,
                    "EsPlcHght": 0,
                    "EsPlcWdth": 0,
                    "EsPlcRot": 0,
                    "EsPlcProt": 0,
                    "EsShpOtEl": 0,
                    "EsShpInEl": 0,
                    "HS_ID": None, # Always set during actual storage of the player - dependent entirely on RosterID.
                    "IsRegNBA": 1,
                    "IsSpecial": 0,
                    "SlotType": 1,
                    "IsGener": 0,
                    "IsDraftee": 0,
                    "IsDrafted": 0,
                    "ASA_ID": 0,
                    "IsFA": 0,
                    "TeamID1": None, # TeamID is always either defined by archetype or manually set.
                    "TeamID2": None, # TeamID is always either defined by archetype or manually set.
                    "BirthDay": 30, # Random default birthday
                    "BirthMonth": 9,
                    "BirthYear": 1998,
                    "YearsPro": 0,
                    "CollegeID": 37, # Everybody goes to college in Bosnia
                    "DraftedBy": -1,
                    "DraftYear": 2005,
                    "DraftRound": 0,
                    "DraftPos": 0,
                    "Personality": 2, # Default is neutral
                    "Play4Winner": 50,
                    "FinSecurity": 50,
                    "Loyalty": 50,
                    "PeakAgeS": 20,
                    "PeakAgeE": 30,
                    "MinsAsg": 30,
                    "Morale": 0,
                    "Fatigue": 0,
                    "FARestr": 0,
                    "CtrThoughts": 0,
                    "InjDaysLeft": 0,
                    "InjType": 0,
                    "StatY0": -1,
                    "StatY1": -1,
                    "StatY2": -1,
                    "StatY3": -1,
                    "StatY4": -1,
                    "StatY5": -1,
                    "StatY6": -1,
                    "StatY7": -1,
                    "StatY8": -1,
                    "StatY9": -1,
                    "StatY10": -1,
                    "StatY11": -1,
                    "StatY12": -1,
                    "StatY13": -1,
                    "StatY14": -1,
                    "StatY15": -1,
                    "StatY16": -1,
                    "StatY17": -1,
                    "StatY18": -1,
                    "StatY19": -1,
                    "StatPOs": -1,
                    "GH_CarPts": 0,
                    "GH_CarFGM": 0,
                    "GH_CarFGA": 0,
                    "GH_CarStl": 0,
                    "GH_CarBlk": 0,
                    "GH_Car3PM": 0,
                    "GH_Car3PA": 0,
                    "GH_CarFTM": 0,
                    "GH_CarFTA": 0,
                    "GH_CarOReb": 0,
                    "GH_CarDReb": 0,
                    "GH_CarRebs": 0,
                    "GH_CarAst": 0,
                    "GH_SeaPts": 0,
                    "GH_SeaFGM": 0,
                    "GH_SeaFGA": 0,
                    "GH_SeaStl": 0,
                    "GH_SeaBlk": 0,
                    "GH_Sea3PM": 0,
                    "GH_Sea3PA": 0,
                    "GH_SeaFTM": 0,
                    "GH_SeaFTA": 0,
                    "GH_SeaOReb": 0,
                    "GH_SeaDReb": 0,
                    "GH_SeaRebs": 0,
                    "GH_SeaAst": 0,
                    "BirdYears": 1,
                    "CClrYears": 0,
                    "CRole": 4,
                    "COption": 0,
                    "CNoTrade": 0,
                    "CYear1": 0,
                    "CYear2": 0,
                    "CYear3": 0,
                    "CYear4": 0,
                    "CYear5": 0,
                    "CYear6": 0,
                    "SgndTYWith": -1,
                    "YrsForCurT": 1,
                    "ExtraValue1": None,
                    "ExtraValue2": None,
                    "ExtraValue3": None,
                    "ExtraValue4": None,
                    "ExtraValue5": None,
                    "ExtraValue6": None,
                    "ExtraValue7": None,
                    "ExtraValue8": None,
                    "ExtraValue9": None,
                    "ExtraValue10": None,
                    "ExtraValue11": None,
                    "ExtraValue12": None,
                    "ExtraValue13": None,
                    "ExtraValue14": None,
                    "ExtraValue15": None,
                    "ExtraValue16": None,
                    "ExtraValue17": None,
                    "ExtraValue18": None,
                    "ExtraValue19": None,
                    "ExtraValue20": None,
                    "ExtraValue21": None,
                    "ExtraValue22": None,
                    "ExtraValue23": None,
                    "ExtraValue24": None,
                    "ExtraValue25": None,
                    "ExtraValue26": None,
                    "ExtraValue27": None,
                    "ExtraValue28": None,
                    "ExtraValue29": None,
                    "ExtraValue30": None,
                    "ExtraValue31": None,
                    "ExtraValue32": None,
                    "ExtraValue33": None,
                    "ExtraValue34": None,
                    "ExtraValue35": None,
                    "ExtraValue36": None,
                    "ExtraValue37": None,
                    "ExtraValue38": None,
                    "ExtraValue39": None,
                    "ExtraValue40": None,
                    "ExtraValue41": None,
                    "ExtraValue42": None,
                    "ExtraValue43": None,
                    "ExtraValue44": None,
                    "ExtraValue45": None,
                    "ExtraValue46": None,
                    "ExtraValue47": None,
                    "ExtraValue48": None,
                    "ExtraValue49": None,
                    "ExtraValue50": None}

        # This helper member tracks whether changes have been made to this Player object,
        # with the intent to organically detect necessary updates.
        self.hasPendingUpdates = False

    # Simple string method for quickly displaying the full object.
    def __str__(self):
        returnString = f"SpriteID: {self.__spriteID}"
        for key,value in self.vals.items():
            if(key in self.extraValuesMap.values()):
                returnString += f"{b.getKeyFromValue(dictionary=self.extraValuesMap,targetValue=key)}: {value}"
            else:
                returnString += f"{key}: {value}"
            if(key in self.idMap.keys()):
                returnString += f" ({self.idMap[key][value]})"
            returnString += "\n"
        return returnString

    # Simple comparator methods for comparing players by their names.
    def __lt__(self, other):
        return f"{self.vals['First_Name']}{self.vals['Last_Name']}" < f"{other.vals['First_Name']}{other.vals['Last_Name']}"
    def __le__(self, other):
        return f"{self.vals['First_Name']}{self.vals['Last_Name']}" <= f"{other.vals['First_Name']}{other.vals['Last_Name']}"
    def __gt__(self, other):
        return f"{self.vals['First_Name']}{self.vals['Last_Name']}" > f"{other.vals['First_Name']}{other.vals['Last_Name']}"
    def __ge__(self, other):
        return f"{self.vals['First_Name']}{self.vals['Last_Name']}" >= f"{other.vals['First_Name']}{other.vals['Last_Name']}"

    #endregion === Init and Constants ===

    #region === Getter and Setter ===

    # Getter and setter for all values in the Player object.
    def __getitem__(self,key):
        # Done first to avoid conflicts later with _Name specifier. Damn RedMC
        if(key == "First_Name" or key == "Last_Name"):
            return self.vals[key]
        # Testing if the key is for SpriteID.
        elif(key == "SpriteID"):
            return self.__spriteID
        # Testing if the key is an ExtraValue.
        elif(key in self.extraValuesMap.keys()):
            return self.vals[self.extraValuesMap[key]]
        # Testing if the key is an ArchetypeName.
        elif(key == "Archetype_Name"):
            if(self.vals["Archetype"] is None):
                return "None"
            else:
                return self.vals["Archetype"].archetypeName
        # Testing if the key is a height represented in some form. (Default form is in inches)
        elif(key.startswith("Height")):
            if(key == "HeightFt"):
                feet = math.floor(self.vals["Height"] / 12)
                inches = self.vals["Height"] - (feet * 12)
                return f"{feet}'{inches}"
            elif(key == "HeightCm"):
                return round(self.vals["Height"] * 2.54,2)
            elif(key == "HeightIn" or key == "Height"):
                return self.vals["Height"]
            else:
                raise ValueError(f"Invalid Height getter: '{key}'")
        # Testing for special handedness accessor.
        elif(key == "HandName"):
            if(self.vals["Hand"] == 0):
                return "Left"
            else:
                return "Right"
        # Testing if this is a mapped key, ending with _Name
        elif(key.endswith("_Name")):
            cleanKey = key.split("_Name")[0]
            if(cleanKey in self.idMap.keys()):
                return self.idMap[cleanKey][self.vals[cleanKey]]
            else:
                raise ValueError(f"'{cleanKey}' has no accessible mapped value using _Name.")
        else:
            return self.vals[key]
    def __setitem__(self,key,value):
        # Done first to avoid conflicts later with _Name specifier. Damn RedMC
        if(key == "First_Name" or key == "Last_Name"):
            self.vals[key] = value
        # Testing if the key is SpriteID, and if so, applying special logic. SpriteID can only be set
        # if the current SpriteID is unset (a negative number), because once set, it should NEVER EVER be changed.
        elif(key == "SpriteID"):
            if(self.__spriteID < 0):
                self.__spriteID = int(value)
            else:
                raise ValueError("ERROR: Can not attempt to change SpriteID of an existing player!!")
        # Testing if the key is an ExtraValue.
        elif(key in self.extraValuesMap.keys()):
            self.vals[self.extraValuesMap[key]] = value
        # Testing if the key is for Archetype.
        elif(key.startswith("Archetype")):
            if(type(value) is str or key == "Archetype_Name"):
                if(value.lower() == "slayer"):
                    self["Archetype"] = Archetypes.ARCH_SLAYER
                elif(value.lower() == "vigilante"):
                    self["Archetype"] = Archetypes.ARCH_VIGILANTE
                elif(value.lower() == "medic"):
                    self["Archetype"] = Archetypes.ARCH_MEDIC
                elif(value.lower() == "guardian"):
                    self["Archetype"] = Archetypes.ARCH_GUARDIAN
                elif(value.lower() == "engineer"):
                    self["Archetype"] = Archetypes.ARCH_ENGINEER
                elif(value.lower() == "director"):
                    self["Archetype"] = Archetypes.ARCH_DIRECTOR
                elif(value.lower() == "none" or value is None):
                    self["Archetype"] = None
                else:
                    raise ValueError(f"Invalid archetype name: '{value}'")
            elif(type(value) is Archetypes.Archetype):
                self.vals["Archetype"] = value
                self.vals["Pos"] = value.inGamePositionId
                self.vals["SecondPos"] = value.inGameSecondaryPositionId
                self.vals["PlayInitor"] = value.isPlayInitiator
                self.vals["TeamID1"] = str(value.jerseyTeamId)
                self.vals["TeamID2"] = str(value.jerseyTeamId)
            elif(value is None):
                self.vals["Archetype"] = None
            else:
                raise TypeError(f"Invalid type for Archetype setter: '{value}', with type '{type(value)}'")
        # Testing if the key is a height represented in some form. (Default form is in inches)
        elif(key.startswith("Height")):
            if(key == "HeightFt"):
                splitHeightFt = value.split("'")
                feet = int(splitHeightFt[0])
                inches = int(splitHeightFt[1])
                self.vals["Height"] = (feet*12) + inches
            elif(key == "HeightCm"):
                self.vals["Height"] = int(math.floor(value/2.54))
            elif(key == "HeightIn" or key == "Height"):
                self.vals["Height"] = int(value)
            else:
                raise ValueError(f"Invalid Height setter: '{key}'")
        # Testing if the key is handedness
        elif(key == "Hand"):
            if(value == "Right"):
                self.vals["Hand"] = 1
            elif(value == "Left"):
                self.vals["Hand"] = 0
            elif(str(value) == "1" or str(value) == "0"):
                self.vals["Hand"] = value
            else:
                raise ValueError(f"Invalid setter for Handedness: '{value}'")
        # Testing if the key is a mapped value
        elif(key in self.idMap.keys() or key.endswith("_Name")):
            cleanKey = key.split("_Name")[0]
            if(value in self.idMap[cleanKey]):
                self.vals[cleanKey] = self.idMap[cleanKey].index(value)
            elif(type(value) is int):
                self.vals[cleanKey] = value
            elif(key.endswith("_Name")):
                raise ValueError(f"'{cleanKey}' is not a mapped value, and can not be accessed using _Name.")
            else:
                raise ValueError(f"Invalid value given for {cleanKey}: '{value}'")
        # Test if its an attribute:
        elif(key in ["SShtIns","SShtCls","SShtMed","SSht3PT","SShtFT","SLayUp","SDunk","SStdDunk","SShtInT","SPstFdaway","SPstHook","SShtOfD","SBallHndl","SOffHDrib","SBallSec","SPass","SBlock","SSteal","SHands","SOnBallD","SOReb","SDReb","SOLowPost","SDLowPost","SOAwar","SDAwar","SConsis","SStamina","SSpeed","SQuick","SStrength","SVertical","SHustle","SDurab","SPOT","SEmotion"]):
            self.vals[key] = int(value)
            if(self.vals[key] > 99):
                self.vals[key] = 99
            elif(self.vals[key] < 25):
                self.vals[key] = 25
            else:
                if(key == "SShtIns" and self.vals["SShtIns"] < 60):
                    self.vals[key] = 60
                elif(key == "SShtCls" and self.vals["SShtCls"] < 50):
                    self.vals[key] = 50
        # Otherwise, store value normally.
        else:
            if(key in self.vals.keys()):
                self.vals[key] = value
            else:
                raise ValueError(f"Key does not exist in player object: '{key}'")

        self.hasPendingUpdates = True

    # Special override function to set SpriteID manually. Should only be used
    # in extremely specific circumstances.
    def overrideSpriteID(self,newSpriteID):
        self.__spriteID = newSpriteID

    #endregion === Getter and Setter ===

    #region === Generators ===

    # Simply randomly assigns an archetype.
    def genArchetype(self):
        archetypes = ["Slayer","Vigilante","Medic","Guardian","Engineer","Director"]
        self["Archetype"] = random.choice(archetypes)
    # Randomly sets a rarity, based on config chances.
    def genRarity(self):
        rarityWeightedDict = WeightedDict.WeightedDict()
        rarityWeightedDict.add("Common", int(b.config["rarities"]["commonChance"] * 100))
        rarityWeightedDict.add("Rare", int(b.config["rarities"]["rareChance"] * 100))
        rarityWeightedDict.add("Epic", int(b.config["rarities"]["epicChance"] * 100))
        rarityWeightedDict.add("Legendary", int(b.config["rarities"]["legendaryChance"] * 100))
        rarityWeightedDict.add("Godlike", int(b.config["rarities"]["godlikeChance"] * 100))
        self.vals["Rarity"] = rarityWeightedDict.pull()
        self.hasPendingUpdates = True
    # Generates all attributes based on the given archetype.
    def genAttributes(self,archetype = None):
        if(archetype is None):
            if(self.vals["Archetype"] is None):
                raise ValueError("Must specify an archetype if the Player's default archetype is None.")
            else:
                archetype = self.vals["Archetype"]

        self.vals["SOffHDrib"] = random.randrange(archetype.attributeRanges.get("SOffHDrib")[0], archetype.attributeRanges.get("SOffHDrib")[1] + 1)
        self.vals["SHands"] = random.randrange(archetype.attributeRanges.get("SHands")[0], archetype.attributeRanges.get("SHands")[1] + 1)
        self.vals["SOAwar"] = random.randrange(archetype.attributeRanges.get("SOAwar")[0], archetype.attributeRanges.get("SOAwar")[1] + 1)
        self.vals["SBallHndl"] = random.randrange(archetype.attributeRanges.get("SBallHndl")[0], archetype.attributeRanges.get("SBallHndl")[1] + 1)
        self.vals["SBallSec"] = random.randrange(archetype.attributeRanges.get("SBallSec")[0], archetype.attributeRanges.get("SBallSec")[1] + 1)
        self.vals["SPass"] = random.randrange(archetype.attributeRanges.get("SPass")[0], archetype.attributeRanges.get("SPass")[1] + 1)
        self.vals["SSpeed"] = random.randrange(archetype.attributeRanges.get("SSpeed")[0], archetype.attributeRanges.get("SSpeed")[1] + 1)
        self.vals["SQuick"] = random.randrange(archetype.attributeRanges.get("SQuick")[0], archetype.attributeRanges.get("SQuick")[1] + 1)
        self.vals["SHustle"] = random.randrange(archetype.attributeRanges.get("SHustle")[0], archetype.attributeRanges.get("SHustle")[1] + 1)
        self.vals["SSteal"] = random.randrange(archetype.attributeRanges.get("SSteal")[0], archetype.attributeRanges.get("SSteal")[1] + 1)
        self.vals["SDLowPost"] = random.randrange(archetype.attributeRanges.get("SDLowPost")[0], archetype.attributeRanges.get("SDLowPost")[1] + 1)
        self.vals["SStrength"] = random.randrange(archetype.attributeRanges.get("SStrength")[0], archetype.attributeRanges.get("SStrength")[1] + 1)
        self.vals["SBlock"] = random.randrange(archetype.attributeRanges.get("SBlock")[0], archetype.attributeRanges.get("SBlock")[1] + 1)
        self.vals["SOnBallD"] = random.randrange(archetype.attributeRanges.get("SOnBallD")[0], archetype.attributeRanges.get("SOnBallD")[1] + 1)
        self.vals["SOReb"] = random.randrange(archetype.attributeRanges.get("SOReb")[0], archetype.attributeRanges.get("SOReb")[1] + 1)
        self.vals["SDReb"] = random.randrange(archetype.attributeRanges.get("SDReb")[0], archetype.attributeRanges.get("SDReb")[1] + 1)
        self.vals["SDAwar"] = random.randrange(archetype.attributeRanges.get("SDAwar")[0], archetype.attributeRanges.get("SDAwar")[1] + 1)
        self.vals["SShtIns"] = random.randrange(archetype.attributeRanges.get("SShtIns")[0], archetype.attributeRanges.get("SShtIns")[1] + 1)
        self.vals["SDunk"] = random.randrange(archetype.attributeRanges.get("SDunk")[0], archetype.attributeRanges.get("SDunk")[1] + 1)
        self.vals["SStdDunk"] = random.randrange(archetype.attributeRanges.get("SStdDunk")[0], archetype.attributeRanges.get("SStdDunk")[1] + 1)
        self.vals["SVertical"] = random.randrange(archetype.attributeRanges.get("SVertical")[0], archetype.attributeRanges.get("SVertical")[1] + 1)
        self.vals["SShtFT"] = random.randrange(archetype.attributeRanges.get("SShtFT")[0], archetype.attributeRanges.get("SShtFT")[1] + 1)
        self.vals["SStamina"] = random.randrange(archetype.attributeRanges.get("SStamina")[0], archetype.attributeRanges.get("SStamina")[1] + 1)
        self.vals["SDurab"] = random.randrange(archetype.attributeRanges.get("SDurab")[0], archetype.attributeRanges.get("SDurab")[1] + 1)
        self.vals["SPOT"] = random.randrange(archetype.attributeRanges.get("SPOT")[0], archetype.attributeRanges.get("SPOT")[1] + 1)
        self.vals["SShtCls"] = random.randrange(archetype.attributeRanges.get("SShtCls")[0], archetype.attributeRanges.get("SShtCls")[1] + 1)
        self.vals["SLayUp"] = random.randrange(archetype.attributeRanges.get("SLayUp")[0], archetype.attributeRanges.get("SLayUp")[1] + 1)
        self.vals["SPstFdaway"] = random.randrange(archetype.attributeRanges.get("SPstFdaway")[0], archetype.attributeRanges.get("SPstFdaway")[1] + 1)
        self.vals["SPstHook"] = random.randrange(archetype.attributeRanges.get("SPstHook")[0], archetype.attributeRanges.get("SPstHook")[1] + 1)
        self.vals["SOLowPost"] = random.randrange(archetype.attributeRanges.get("SOLowPost")[0], archetype.attributeRanges.get("SOLowPost")[1] + 1)
        self.vals["SShtMed"] = random.randrange(archetype.attributeRanges.get("SShtMed")[0], archetype.attributeRanges.get("SShtMed")[1] + 1)
        self.vals["SSht3PT"] = random.randrange(archetype.attributeRanges.get("SSht3PT")[0], archetype.attributeRanges.get("SSht3PT")[1] + 1)
        self.vals["SShtInT"] = random.randrange(archetype.attributeRanges.get("SShtInT")[0], archetype.attributeRanges.get("SShtInT")[1] + 1)
        self.vals["SShtOfD"] = random.randrange(archetype.attributeRanges.get("SShtOfD")[0], archetype.attributeRanges.get("SShtOfD")[1] + 1)
        self.vals["SConsis"] = random.randrange(archetype.attributeRanges.get("SConsis")[0], archetype.attributeRanges.get("SConsis")[1] + 1)

        self.hasPendingUpdates = True
    # Generates all tendencies based on the given archetype.
    def genTendencies(self,archetype = None):
        if(archetype is None):
            if(self.vals["Archetype"] is None):
                raise ValueError("Must specify an archetype if the Player's default archetype is None.")
            else:
                archetype = self.vals["Archetype"]

        self.vals["TShtTend"] = random.randrange(archetype.t_ShotTnd[0], archetype.t_ShotTnd[1] + 1)
        self.vals["TInsShots"] = random.randrange(archetype.t_InsideShot[0], archetype.t_InsideShot[1] + 1)
        self.vals["TCloseSht"] = random.randrange(archetype.t_CloseShot[0], archetype.t_CloseShot[1] + 1)
        self.vals["TMidShots"] = random.randrange(archetype.t_MidShot[0], archetype.t_MidShot[1] + 1)
        self.vals["T3PTShots"] = random.randrange(archetype.t_ShotThreePt[0], archetype.t_ShotThreePt[1] + 1)
        self.vals["TDriveLn"] = random.randrange(archetype.t_DriveLane[0], archetype.t_DriveLane[1] + 1)
        self.vals["TDriveRvL"] = random.randrange(archetype.t_DriveRight[0], archetype.t_DriveRight[1] + 1)
        self.vals["TPullUp"] = random.randrange(archetype.t_PullUp[0], archetype.t_PullUp[1] + 1)
        self.vals["TPumpFake"] = random.randrange(archetype.t_PumpFake[0], archetype.t_PumpFake[1] + 1)
        self.vals["TTrplThrt"] = random.randrange(archetype.t_TripleThreat[0], archetype.t_TripleThreat[1] + 1)
        self.vals["TNoTT"] = random.randrange(archetype.t_NoTripleThreat[0], archetype.t_NoTripleThreat[1] + 1)
        self.vals["TTTShot"] = random.randrange(archetype.t_TripleThreatShot[0], archetype.t_TripleThreatShot[1] + 1)
        self.vals["TSizeUp"] = random.randrange(archetype.t_Sizeup[0], archetype.t_Sizeup[1] + 1)
        self.vals["THesitat"] = random.randrange(archetype.t_Hesitation[0], archetype.t_Hesitation[1] + 1)
        self.vals["TStrghtDr"] = random.randrange(archetype.t_StraightDribble[0], archetype.t_StraightDribble[1] + 1)
        self.vals["TCrossov"] = random.randrange(archetype.t_Crossover[0], archetype.t_Crossover[1] + 1)
        self.vals["TSpin"] = random.randrange(archetype.t_Spin[0], archetype.t_Spin[1] + 1)
        self.vals["TStepBack"] = random.randrange(archetype.t_Stepback[0], archetype.t_Stepback[1] + 1)
        self.vals["THalfSpin"] = random.randrange(archetype.t_Halfspin[0], archetype.t_Halfspin[1] + 1)
        self.vals["TDblCross"] = random.randrange(archetype.t_DoubleCrossover[0], archetype.t_DoubleCrossover[1] + 1)
        self.vals["TBhndBack"] = random.randrange(archetype.t_BehindBack[0], archetype.t_BehindBack[1] + 1)
        self.vals["THesCross"] = random.randrange(archetype.t_HesitationCross[0], archetype.t_HesitationCross[1] + 1)
        self.vals["TInAndOut"] = random.randrange(archetype.t_InNOut[0], archetype.t_InNOut[1] + 1)
        self.vals["TDPSimpDr"] = random.randrange(archetype.t_SimpleDrive[0], archetype.t_SimpleDrive[1] + 1)
        self.vals["TAttackB"] = random.randrange(archetype.t_Attack[0], archetype.t_Attack[1] + 1)
        self.vals["TPassOut"] = random.randrange(archetype.t_PassOut[0], archetype.t_PassOut[1] + 1)
        self.vals["THopStep"] = random.randrange(archetype.t_Hopstep[0], archetype.t_Hopstep[1] + 1)
        self.vals["TSpinLUp"] = random.randrange(archetype.t_SpinLayup[0], archetype.t_SpinLayup[1] + 1)
        self.vals["TEuroStep"] = random.randrange(archetype.t_Eurostep[0], archetype.t_Eurostep[1] + 1)
        self.vals["TRunner"] = random.randrange(archetype.t_Runner[0], archetype.t_Runner[1] + 1)
        self.vals["TFadeaway"] = random.randrange(archetype.t_Fadeaway[0], archetype.t_Fadeaway[1] + 1)
        self.vals["TDunkvLU"] = random.randrange(archetype.t_Dunk[0], archetype.t_Dunk[1] + 1)
        self.vals["TVShCrash"] = random.randrange(archetype.t_Crash[0], archetype.t_Crash[1] + 1)
        self.vals["TTouches"] = random.randrange(archetype.t_Touches[0], archetype.t_Touches[1] + 1)
        self.vals["TUsePick"] = random.randrange(archetype.t_UsePick[0], archetype.t_UsePick[1] + 1)
        self.vals["TSetPick"] = random.randrange(archetype.t_SetPick[0], archetype.t_SetPick[1] + 1)
        self.vals["TIsolat"] = random.randrange(archetype.t_Isolation[0], archetype.t_Isolation[1] + 1)
        self.vals["TUseOBScr"] = random.randrange(archetype.t_UseOffBallScreen[0], archetype.t_UseOffBallScreen[1] + 1)
        self.vals["TSetOBScr"] = random.randrange(archetype.t_SetOffBallScreen[0], archetype.t_SetOffBallScreen[1] + 1)
        self.vals["TPostUp"] = random.randrange(archetype.t_PostUp[0], archetype.t_PostUp[1] + 1)
        self.vals["TSpotUp"] = random.randrange(archetype.t_SpotUp[0], archetype.t_SpotUp[1] + 1)
        self.vals["TPostSpn"] = random.randrange(archetype.t_PostSpin[0], archetype.t_PostSpin[1] + 1)
        self.vals["TPostDrpSt"] = random.randrange(archetype.t_DropStep[0], archetype.t_DropStep[1] + 1)
        self.vals["TPostShmSh"] = random.randrange(archetype.t_Shimmy[0], archetype.t_Shimmy[1] + 1)
        self.vals["TPostFaceU"] = random.randrange(archetype.t_FaceUp[0], archetype.t_LeavePost[1] + 1)
        self.vals["TLeavePost"] = random.randrange(archetype.t_LeavePost[0], archetype.t_LeavePost[1] + 1)
        self.vals["TPostBDown"] = random.randrange(archetype.t_BackDown[0], archetype.t_BackDown[1] + 1)
        self.vals["TPostAgBd"] = random.randrange(archetype.t_AggressiveBackDown[0], archetype.t_AggressiveBackDown[1] + 1)
        self.vals["TPostShots"] = random.randrange(archetype.t_PostShot[0], archetype.t_PostShot[1] + 1)
        self.vals["TPostHook"] = random.randrange(archetype.t_PostHook[0], archetype.t_PostHook[1] + 1)
        self.vals["TPostFdawy"] = random.randrange(archetype.t_PostFade[0], archetype.t_PostFade[1] + 1)
        self.vals["TPostDrv"] = random.randrange(archetype.t_PostDrive[0], archetype.t_PostDrive[1] + 1)
        self.vals["TPostHopSh"] = random.randrange(archetype.t_HopShot[0], archetype.t_HopShot[1] + 1)
        self.vals["TPutbacks"] = random.randrange(archetype.t_Putback[0], archetype.t_Putback[1] + 1)
        self.vals["TFlshPass"] = random.randrange(archetype.t_FlashyPass[0], archetype.t_FlashyPass[1] + 1)
        self.vals["TThrowAO"] = random.randrange(archetype.t_AlleyOop[0], archetype.t_AlleyOop[1] + 1)
        self.vals["TDrawFoul"] = random.randrange(archetype.t_DrawFoul[0], archetype.t_DrawFoul[1] + 1)
        self.vals["TPassLane"] = random.randrange(archetype.t_PlayPassLane[0], archetype.t_PlayPassLane[1] + 1)
        self.vals["TTakeChrg"] = random.randrange(archetype.t_TakeCharge[0], archetype.t_TakeCharge[1] + 1)
        self.vals["TOnBalStl"] = random.randrange(archetype.t_OnBallSteal[0], archetype.t_OnBallSteal[1] + 1)
        self.vals["TContShot"] = random.randrange(archetype.t_Contest[0], archetype.t_Contest[1] + 1)
        self.vals["TCommFoul"] = random.randrange(archetype.t_CommitFoul[0], archetype.t_CommitFoul[1] + 1)
        self.vals["THardFoul"] = random.randrange(archetype.t_HardFoul[0], archetype.t_HardFoul[1] + 1)
        self.vals["TUseGlass"] = random.randrange(archetype.t_UseGlass[0], archetype.t_UseGlass[1] + 1)
        self.vals["TStpbJmpr"] = random.randrange(archetype.t_StepbackJumper[0], archetype.t_StepbackJumper[1] + 1)
        self.vals["TSpinJmpr"] = random.randrange(archetype.t_SpinJumper[0], archetype.t_SpinJumper[1] + 1)
        self.vals["TStpThrgh"] = random.randrange(archetype.t_StepThrough[0], archetype.t_StepThrough[1] + 1)
        self.vals["TAlleyOop"] = random.randrange(archetype.t_ThrowAlleyOop[0], archetype.t_ThrowAlleyOop[1] + 1)
        self.vals["TGiveGo"] = random.randrange(archetype.t_GiveNGo[0], archetype.t_GiveNGo[1] + 1)

        self.hasPendingUpdates = True
    # Generates all hotspots based on the given archetype.
    def genHotspots(self,archetype = None):
        if(archetype is None):
            if(self.vals["Archetype"] is None):
                raise ValueError("Must specify an archetype if the Player's default archetype is None.")
            else:
                archetype = self.vals["Archetype"]

        # Isolation
        isoChoices = WeightedDict.WeightedDict()
        isoChoices.add("HIso3PLft", archetype.HIso3PLftChance)
        isoChoices.add("HIso3PCtr", archetype.HIso3PCtrChance)
        isoChoices.add("HIso3PRgt", archetype.HIso3PRgtChance)
        isoChoices.add("HIsoHPLft", archetype.HIsoHPLftChance)
        isoChoices.add("HIsoHPCtr", archetype.HIsoHPCtrChance)
        isoChoices.add("HIsoHPRgt", archetype.HIsoHPRgtChance)
        for i in range(100):
            pull = isoChoices.pull()
            if (pull == "HIso3PLft"):
                self.vals["HIso3PLft"] += 1
            elif (pull == "HIso3PCtr"):
                self.vals["HIso3PCtr"] += 1
            elif (pull == "HIso3PRgt"):
                self.vals["HIso3PRgt"] += 1
            elif (pull == "HIsoHPLft"):
                self.vals["HIsoHPLft"] += 1
            elif (pull == "HIsoHPCtr"):
                self.vals["HIsoHPCtr"] += 1
            elif (pull == "HIsoHPRgt"):
                self.vals["HIsoHPRgt"] += 1

        # Pick and Roll
        pickRollChoices = WeightedDict.WeightedDict()
        pickRollChoices.add("HP_rLCrnr", archetype.HP_rLCrnrChance)
        pickRollChoices.add("HP_rLWing", archetype.HP_rLWingChance)
        pickRollChoices.add("HP_rTopOA", archetype.HP_rTopOAChance)
        pickRollChoices.add("HP_rRWing", archetype.HP_rRWingChance)
        pickRollChoices.add("HP_rRCrnr", archetype.HP_rRCrnrChance)
        for i in range(100):
            pull = pickRollChoices.pull()
            if (pull == "HP_rLCrnr"):
                self.vals["HP_rLCrnr"] += 1
            elif (pull == "HP_rLWing"):
                self.vals["HP_rLWing"] += 1
            elif (pull == "HP_rTopOA"):
                self.vals["HP_rTopOA"] += 1
            elif (pull == "HP_rRWing"):
                self.vals["HP_rRWing"] += 1
            elif (pull == "HP_rRCrnr"):
                self.vals["HP_rRCrnr"] += 1

        # Spot Up
        spotUpChoices = WeightedDict.WeightedDict()
        spotUpChoices.add("HSpt3PLCr", archetype.HSpt3PLCrChance)
        spotUpChoices.add("HSpt3PLWg", archetype.HSpt3PLWgChance)
        spotUpChoices.add("HSpt3PTop", archetype.HSpt3PTopChance)
        spotUpChoices.add("HSpt3PRWg", archetype.HSpt3PRWgChance)
        spotUpChoices.add("HSpt3PRCr", archetype.HSpt3PRCrChance)
        spotUpChoices.add("HSptMdLBl", archetype.HSptMdLBlChance)
        spotUpChoices.add("HSptMdLWg", archetype.HSptMdLWgChance)
        spotUpChoices.add("HSptMdCtr", archetype.HSptMdCtrChance)
        spotUpChoices.add("HSptMdRWg", archetype.HSptMdRWgChance)
        spotUpChoices.add("HSptMdRBl", archetype.HSptMdRBlChance)
        for i in range(100):
            pull = spotUpChoices.pull()
            if (pull == "HSpt3PLCr"):
                self.vals["HSpt3PLCr"] += 1
            elif (pull == "HSpt3PLWg"):
                self.vals["HSpt3PLWg"] += 1
            elif (pull == "HSpt3PTop"):
                self.vals["HSpt3PTop"] += 1
            elif (pull == "HSpt3PRWg"):
                self.vals["HSpt3PRWg"] += 1
            elif (pull == "HSpt3PRCr"):
                self.vals["HSpt3PRCr"] += 1
            elif (pull == "HSptMdLBl"):
                self.vals["HSptMdLBl"] += 1
            elif (pull == "HSptMdLWg"):
                self.vals["HSptMdLWg"] += 1
            elif (pull == "HSptMdCtr"):
                self.vals["HSptMdCtr"] += 1
            elif (pull == "HSptMdRWg"):
                self.vals["HSptMdRWg"] += 1
            elif (pull == "HSptMdRBl"):
                self.vals["HSptMdRBl"] += 1

        # Post
        postChoices = WeightedDict.WeightedDict()
        postChoices.add("HPstRHigh", archetype.HPstRHighChance)
        postChoices.add("HPstRLow", archetype.HPstRLowChance)
        postChoices.add("HPstLHigh", archetype.HPstLHighChance)
        postChoices.add("HPstLLow", archetype.HPstLLowChance)
        for i in range(100):
            pull = postChoices.pull()
            if (pull == "HPstRHigh"):
                self.vals["HPstRHigh"] += 1
            elif (pull == "HPstRLow"):
                self.vals["HPstRLow"] += 1
            elif (pull == "HPstLHigh"):
                self.vals["HPstLHigh"] += 1
            elif (pull == "HPstLLow"):
                self.vals["HPstLLow"] += 1

        self.hasPendingUpdates = True
    # Generates height based on either a given or, if not provided, the Player's default archetype height range.
    def genHeight(self,archetype = None):
        if(archetype is None):
            if(self.vals["Archetype"] is None):
                raise ValueError("Must specify an archetype if the Player's default archetype is None.")
            else:
                archetype = self.vals["Archetype"]
        self.vals["Height"] = random.randrange(archetype.heightRange[0],archetype.heightRange[1])

        self.hasPendingUpdates = True
    # Rolls all animations.
    def genAnimations(self,archetype = None,dunkCount : int = None):
        if(archetype is None):
            if(self.vals["Archetype"] is None):
                raise ValueError("Must specify an archetype if the Player's default archetype is None.")
            else:
                archetype = self.vals["Archetype"]

        self.vals["AShtForm"] = random.randrange(0, len(self.idMap["AShtForm"]))
        self.vals["AShtBase"] = random.randrange(0, len(self.idMap["AShtBase"]))
        self.vals["AFadeaway"] = random.randrange(0, len(self.idMap["AFadeaway"]))
        self.vals["AContestd"] = random.randrange(0,len(self.idMap["AContestd"]))
        self.vals["AEscDrPlU"] = random.randrange(0,len(self.idMap["AEscDrPlU"]))
        self.vals["ARunner"] = random.randrange(0, len(self.idMap["ARunner"]))
        self.vals["AFreeT"] = random.randrange(0, len(self.idMap["AFreeT"]))
        self.vals["ADrPullUp"] = random.randrange(0, len(self.idMap["ADrPullUp"]))
        self.vals["ASpinJmpr"] = random.randrange(0, len(self.idMap["ASpinJmpr"]))
        self.vals["AHopJmpr"] = random.randrange(0, len(self.idMap["AHopJmpr"]))

        # Post Fade
        postFadeOptions = [num for num in range(len(self.idMap["APstFade"]))]
        if (archetype.inGamePositionId not in [3,4]):
            postFadeOptions.remove(1)
            postFadeOptions.remove(10)
        self.vals["APstFade"] = random.choice(postFadeOptions)

        # Post Hook
        postHookOptions = [num for num in range(len(self.idMap["APstHook"]))]
        if (archetype.inGamePositionId not in [3,4]):
            postHookOptions.remove(12)
            postHookOptions.remove(14)
        self.vals["APstHook"] = random.choice(postHookOptions)

        self.vals["APstHopSh"] = random.randrange(0, len(self.idMap["APstHopSh"]))
        self.vals["APstShmSh"] = random.randrange(0, len(self.idMap["APstShmSh"]))
        self.vals["APstDrvStB"] = random.randrange(0, len(self.idMap["APstDrvStB"]))
        self.vals["APstSpnStB"] = random.randrange(0, len(self.idMap["APstSpnStB"]))
        self.vals["APstPrtct"] = random.randrange(0, len(self.idMap["APstPrtct"]))
        self.vals["APstPrtSpn"] = random.randrange(0, len(self.idMap["APstPrtSpn"]))
        self.vals["AIsoCross"] = random.randrange(0, len(self.idMap["AIsoCross"]))
        self.vals["AIsoBhBck"] = random.randrange(0, len(self.idMap["AIsoBhBck"]))
        self.vals["AIsoSpin"] = random.randrange(0, len(self.idMap["AIsoSpin"]))
        self.vals["AIsoHesit"] = random.randrange(0, len(self.idMap["AIsoHesit"]))


        if (archetype.inGamePositionId in [3,4]):
            layUpOptions = [1,5]
        else:
            layUpOptions = [num for num in range(len(self.idMap["ALayUp"])) if num != 1]
        self.vals["ALayUp"] = random.choice(layUpOptions)

        if(dunkCount is None):
            if(self.vals["SDunk"] <= 49):
                dunkCount = 1
            elif (49 < self.vals["SDunk"] <= 70):
                dunkCount = 2
            elif (70 < self.vals["SDunk"] <= 80):
                dunkCount = 3
            elif (80 < self.vals["SDunk"] <= 90):
                dunkCount = 4
            elif (90 < self.vals["SDunk"] <= 99):
                dunkCount = 5

        dunkOptions = [num for num in range(1, len(self.idMap["AGoToDunk"]))]
        if(dunkCount >= 1):
            thisDunk = random.choice(dunkOptions)
            dunkOptions.remove(thisDunk)
            self.vals["AGoToDunk"] = thisDunk
        if(dunkCount >= 2):
            thisDunk = random.choice(dunkOptions)
            dunkOptions.remove(thisDunk)
            self.vals["ADunk2"] = thisDunk
        if(dunkCount >= 3):
            thisDunk = random.choice(dunkOptions)
            dunkOptions.remove(thisDunk)
            self.vals["ADunk3"] = thisDunk
        if(dunkCount >= 4):
            thisDunk = random.choice(dunkOptions)
            dunkOptions.remove(thisDunk)
            self.vals["ADunk4"] = thisDunk
        if(dunkCount >= 5):
            thisDunk = random.choice(dunkOptions)
            dunkOptions.remove(thisDunk)
            self.vals["ADunk5"] = thisDunk

        self.vals["AIntHLght"] = random.randrange(0, len(self.idMap["AIntHLght"]))
        self.vals["AIntPreG1"] = random.randrange(0, len(self.idMap["AIntPreG1"]))
        self.vals["AIntPreG2"] = random.randrange(0, len(self.idMap["AIntPreG2"]))
        self.vals["AIntPreT1"] = random.randrange(0, len(self.idMap["AIntPreT1"]))
        self.vals["AIntPreT2"] = random.randrange(0, len(self.idMap["AIntPreT2"]))

        self.hasPendingUpdates = True
    # Generates and selects a play style based on archetype and attributes.
    def genPlayStyle(self,archetype = None):
        if(archetype is None):
            if(self.vals["Archetype"] is None):
                raise ValueError("Must specify an archetype if the Player's default archetype is None.")
            else:
                archetype = self.vals["Archetype"]

        potentialStyles = []
        if (archetype.archetypeName == "Slayer"):
            # All positions have access to the three basic styles: All Around, Athletic, and Defensive.
            potentialStyles += [7, 9, 11]

            # All Slayers have "Scoring" available.
            potentialStyles.append(6)

            # Test if the Slayer should have "Slashing" available.
            if (self.vals["SDunk"] >= 80 or self.vals["SLayUp"] >= 75):
                potentialStyles.append(10)

            # Test if the Slayer should have "3pt Specialist" available.
            if (self.vals["SSht3PT"] >= 80):
                potentialStyles.append(8)
        elif (archetype.archetypeName == "Vigilante"):
            # All positions have access to the three basic styles: All Around, Athletic, and Defensive.
            potentialStyles += [13, 15, 18]

            # All Vigilantes have "Scoring" available.
            potentialStyles.append(12)

            # Test if the Vigilante should have "Slashing" available.
            if (self.vals["SDunk"] >= 80 or self.vals["SLayUp"] >= 75):
                potentialStyles.append(16)

            # Test if the Vigilante should have "3pt Specialist" available.
            if (self.vals["SSht3PT"] >= 80):
                potentialStyles.append(14)

            # Vigilantes will NOT have "Point Forward" available.
        elif (archetype.archetypeName == "Medic"):
            # All positions have access to the three basic styles: All Around, Athletic, and Defensive.
            # Medics have all Back to Basket, Faceup, and Rebounding available by default.
            potentialStyles += [25, 26, 30, 27, 28, 29]
        elif (archetype.archetypeName == "Guardian"):
            # All positions have access to the three basic styles: All Around, Athletic, and Defensive.
            # Guardians have all Back to Basket, Faceup, and Rebounding available by default.
            potentialStyles += [19, 20, 24, 21, 22, 23]
        elif (archetype.archetypeName == "Engineer"):

            # All positions have access to the three basic styles: All Around, Athletic, and Defensive.
            potentialStyles += [2, 4, 5]

            # Test if Engineer should have "Pass First" available.
            if (self.vals["SPass"] >= 85):
                potentialStyles.append(0)

            # Engineers will never have "Scoring" or "3pt Specialist" available.
        elif (archetype.archetypeName == "Director"):

            # All positions have access to the three basic styles: All Around, Athletic, and Defensive.
            potentialStyles += [2, 4, 5]

            # Test if Director should have "Pass First" available.
            if (self.vals["SPass"] >= 85):
                potentialStyles.append(0)

            # Test if Director should have "Scoring" available.
            if (self.vals["SShtMed"] >= 80 or self.vals["SShtCls"] >= 90):
                potentialStyles.append(4)

            # Test if Director should have "3pt Specialist" available.
            if (self.vals["SSht3PT"] >= 80):
                potentialStyles.append(1)

        self.vals["PlayStyle"] = random.choice(potentialStyles)

        self.hasPendingUpdates = True
    # Generates a few play types if and only if the archetype is Engineer or Director.
    def genPlayTypes(self, archetype = None):
        if(archetype is None):
            if(self.vals["Archetype"] is None):
                raise ValueError("Must specify an archetype if the Player's default archetype is None.")
            else:
                archetype = self.vals["Archetype"]

        playTypeChoices = [num for num in range(1,len(self.idMap["PlayType1"]))]
        if (archetype.archetypeName == "Director" or archetype.archetypeName == "Engineer"):
            self.vals["PlayType1"] = random.choice(playTypeChoices)
            playTypeChoices.remove(self.vals["PlayType1"])
            self.vals["PlayType2"] = random.choice(playTypeChoices)
        else:
            self.vals["PlayType1"] = "0"
            self.vals["PlayType2"] = "0"
        self.vals["PlayType3"] = "0"
        self.vals["PlayType4"] = "0"

        self.hasPendingUpdates = True
    # This method  randomly selects and generates an artifact based on rarity and archetype..
    def generateArtifact(self,archetype = None,rarity = None):
        if(archetype is None):
            if(self.vals["Archetype"] is None):
                raise ValueError("Must specify an archetype if the Player's default archetype is None.")
            else:
                archetype = self.vals["Archetype"]

        if(rarity is None):
            if(self.vals["Rarity"] is None):
                raise ValueError("Must specify a rarity if the Player's default rarity is None.")
            else:
                rarity = self.vals["Rarity"]

        if(rarity != "Common"):
            artGen = PMod.PModCompiler(f"{b.paths.programData}\\Artifacts.txt",self)
            validNeutralArtifactIndexes = []
            validArchetypalArtifactIndexes = []
            counter = 0
            for artifactDict in artGen.listOfAllPMods:
                if(artifactDict.get("PMOD_RARITY") == rarity):
                    if(artifactDict.get("PMOD_ARCHETYPE_LOCK") == archetype.archetypeName):
                        validArchetypalArtifactIndexes.append(counter)
                    elif(artifactDict.get("PMOD_ARCHETYPE_LOCK") == "Neutral"):
                        validNeutralArtifactIndexes.append(counter)
                counter += 1


            # We decide if the artifact will be archetype based...
            if(random.random() > b.config["rarities"]["archetypeBasedArtifactChance"] and len(validArchetypalArtifactIndexes) > 0):
                artGen.compilePMod(validArchetypalArtifactIndexes[random.randrange(0, len(validArchetypalArtifactIndexes))])
            # Or neutral.
            else:
                artGen.compilePMod(validNeutralArtifactIndexes[random.randrange(0, len(validNeutralArtifactIndexes))])

            self.vals["Artifact"] = artGen.parameters
            del artGen

            for parameter in self.vals["Artifact"].keys():
                if(parameter == "PMOD_NAME" or parameter == "PMOD_DESCRIPTION" or parameter == "PMOD_RARITY" or parameter == "PMOD_ARCHETYPE_LOCK"):
                    continue
                else:
                    value = self.vals["Artifact"].get(parameter)
                    if(value.startswith("-")):
                        self.vals[parameter] -= (int(value) * -1)
                    elif(value.startswith("+")):
                        self.vals[parameter] += int(value)
                    elif(value.startswith("=")):
                        self.vals[parameter] = value.lstrip("=")

        self.hasPendingUpdates = True
    # Generates a few random, miscellaneous, inconsequential values.
    def genMisc(self):
        self.vals["Personality"] = random.randrange(0,len(self.idMap["Personality"]))

        self.hasPendingUpdates = True

    #endregion === Generators ===

