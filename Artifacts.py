import Archetypes
import Player
import random



# This file handles the creation of individual Artifact PMods, modifications to players based on rarity.

#region === Globals ===

RARE_SPECIAL_SHOTS = {
'Slayer': [{'Name': 'Tyrion Lannister', 'Shot Form': 36, 'Shot Base': 71, 'Description': "Tyrion Lannister will go down as the greatest disappointment in 2k history, as he could never seem to shoot the ball into the net...like ever. God help this new player with Tyrion's cursed shot."}, {'Name': 'Danny Kowalczyk', 'Shot Form': 82, 'Shot Base': 60, 'Description': "A shot seen whenever new players arrived, Danny's sniper rifle bullet of a shot was completely unique at the time and made for some consistent performances before competitive play was introduced. Can this new player snipe their way to glory with Danny's shot?"}, {'Name': 'Lord Selwig Nara', 'Shot Form': 3, 'Shot Base': 21, 'Description': "Coined as the lock'n'load shot in the later stages of league, Lord Selwig Nara finally found some success near the end of his lengthy career with consistent outlet 3s. Can this new player rise faster than Selwig with his own shot?"}, {'Name': "Jaqen H'Ghar", 'Shot Form': 91, 'Shot Base': 17, 'Description': 'A victim of the time in which he was created, Jaqen never quite saw stardom which could sufficiently match his unrivaled raw talent. His rainbow-bending arch of a shot frightened all who had to defend against it. Will this new player succeed where Jaqen fell short?'}, {'Name': 'Uncle Chicken', 'Shot Form': 3, 'Shot Base': 4, 'Description': 'One of only a few players to truly defy the attribute inflation of PostDEL, at just 70 overall, Uncle Chicken quickly rose to prominence as a legend with a barebones, easily repeatable shot. Can this new player be a darkhorse like Uncle Chicken once was?'}, {'Name': 'Jon Snow', 'Shot Form': 91, 'Shot Base': 38, 'Description': 'A player who had ups and downs in what most would consider a successful career as a legend, Jon Snow rose up as a player who could simply get the job done with his laser-quick shooting form. Will this new player carry on the legacy of the King of the North?'}],
'Vigilante': [{'Name': 'Mahatma Gandhi', 'Shot Form': 66, 'Shot Base': 5, 'Description': "If it weren't for his height and brutal speed, Gandhi could have been one of the all time greats with his under-handed, consistent delivery of 3 pt shots. Can this new player break past the faults of Gandhi with his majestic shot?"}, {'Name': 'Christian Shearcliff', 'Shot Form': 15, 'Shot Base': 38, 'Description': "If there's anything nice to say about Christian Shearcliff it might just be his shooting form, which almost took him to legend status. Can this new player be everything Chris wasn't?"}, {'Name': 'Ni-Gha Die', 'Shot Form': 97, 'Shot Base': 51, 'Description': "Everyone knows that Ni-Gha Die didn't become a legend because of his horrible shot, but hey, he did make it there anyways. Can this new player beat the odds with this wacky and obtrusive shot?"}, {'Name': 'Uncle Chicken', 'Shot Form': 3, 'Shot Base': 4, 'Description': 'One of only a few players to truly defy the attribute inflation of PostDEL, at just 70 overall, Uncle Chicken quickly rose to prominence as a legend with a barebones, easily repeatable shot. Can this new player be a darkhorse like Uncle Chicken once was?'}, {'Name': 'Subway Club', 'Shot Form': 127, 'Shot Base': 59, 'Description': "Who would have thought that for just $12 you could order yourself an excellent basketball player? Everyone was shocked when Subway Club paced the later seasons of league in 3s and 3pt %, as he proved that the overall stat did not need to be in the 90s, or the 80s, or the 70s, or the 60s, or the 50s, to make a good player. Does this player have what it takes to shock everyone with Club's shot?"}],
'Medic': [{'Name': 'Father Titticaca', 'Shot Form': 16, 'Shot Base': 16, 'Description': 'Father Titticaca was an explosion of speed, rebounding, and exceptional shooting ability wrapped into one, and was the backbone of every team with which he played. Can this new player explode into the scene like Titti with his own shot?'}, {'Name': 'Old Sama Benlodan', 'Shot Form': 112, 'Shot Base': 42, 'Description': "Old Sama's carefully set shot will always go down as the pefect fold to his duo Bill Nye. Will this new player find similar success with the same shot?"}, {'Name': 'Daniel Stiefbold', 'Shot Form': 19, 'Shot Base': 72, 'Description': 'One of the quirkier shots in 2k, Daniel Stiefbold went on a tear in the early days of 2k with his scoped-like release. Can this new player exceed expectations like Daniel did with such a strange, exotic shot?'}],
'Guardian': [{'Name': 'The Hound', 'Shot Form': 22, 'Shot Base': 108, 'Description': "Raising his arms high into the air to launch the ball into the net, The Hound's classic shot practically dominated the control-oriented meta in the early days of 2k. Can this new player break out as the new superstar with The Hound's shot?"}, {'Name': 'Old Sama Benlodan', 'Shot Form': 112, 'Shot Base': 42, 'Description': "Old Sama's carefully set shot will always go down as the pefect fold to his duo Bill Nye. Will this new player find similar success with the same shot?"}, {'Name': 'Daniel Stiefbold', 'Shot Form': 19, 'Shot Base': 72, 'Description': 'One of the quirkier shots in 2k, Daniel Stiefbold went on a tear in the early days of 2k with his scoped-like release. Can this new player exceed expectations like Daniel did with such a strange, exotic shot?'}],
'Engineer': [{'Name': 'Gary the Thief', 'Shot Form': 136, 'Shot Base': 82, 'Description': "Gary's robotic dance of a shot eventually carried him to a semi-prominent legend status, which is more than anybody could have ever expected out of the Twitch streamer. Can this new player climb the ladder of greatness like Gary did?"}, {'Name': 'Mike Ehrmantraut', 'Shot Form': 110, 'Shot Base': 107, 'Description': "Known more for his control ability, Mike's clean and consistent shot often went unnoticed in the shadow of his colossal mid plays. Can this new player sink'em like Mike?"}, {'Name': 'Tyrion Lannister', 'Shot Form': 36, 'Shot Base': 71, 'Description': "Tyrion Lannister will go down as the greatest disappointment in 2k history, as he could never seem to shoot the ball into the net...like ever. God help this new player with Tyrion's cursed shot."}],
'Director': [{'Name': 'Alex Somheil', 'Shot Form': 16, 'Shot Base': 2, 'Description': "A shot seen whenever new players arrived, Alex's unmistakablely clean shot proved valuable for the short time him and Danny were viable in competitive play. Can this new player exceed the consistent performances of Alex with his own shot?"}, {'Name': 'Gary the Thief', 'Shot Form': 136, 'Shot Base': 82, 'Description': "Gary's robotic dance of a shot eventually carried him to a semi-prominent legend status, which is more than anybody could have ever expected out of the Twitch streamer. Can this new player climb the ladder of greatness like Gary did?"}, {'Name': 'Mike Ehrmantraut', 'Shot Form': 110, 'Shot Base': 107, 'Description': "Known more for his control ability, Mike's clean and consistent shot often went unnoticed in the shadow of his colossal mid plays. Can this new player sink'em like Mike?"}, {'Name': 'Greg Pelzer', 'Shot Form': 112, 'Shot Base': 46, 'Description': 'Always lingering in between legend and non-legend status, Greg Pelzer was the first player to be fully stripped of the title after it was granted to him. Will this new player find balance where Pelzer teetered off?'}, {'Name': 'Father Titticaca', 'Shot Form': 16, 'Shot Base': 16, 'Description': 'Father Titticaca was an explosion of speed, rebounding, and exceptional shooting ability wrapped into one, and was the backbone of every team with which he played. Can this new player explode into the scene like Titti with his own shot?'}, {'Name': 'Christian Shearcliff', 'Shot Form': 15, 'Shot Base': 38, 'Description': "If there's anything nice to say about Christian Shearcliff it might just be his shooting form, which almost took him to legend status. Can this new player be everything Chris wasn't?"}, {'Name': 'Ni-Gha Die', 'Shot Form': 97, 'Shot Base': 51, 'Description': "Everyone knows that Ni-Gha Die didn't become a legend because of his horrible shot, but hey, he did make it there anyways. Can this new player beat the odds with this wacky and obtrusive shot?"}]
}
EPIC_SPECIAL_SHOTS = {
'Slayer': [{'Name': 'Jaquarius Nocturnal', 'Shot Form': 146, 'Shot Base': 6, 'Description': "Jaquarius didn't have the time to shine as much as his talent allowed him to, and everyone knew that he had what it took to be one of the Gods. His shot was as deadly as his footwork and rebounding. May this new player carry on a great legacy with Jay-Quay's shot."}, {'Name': 'Ser Davos', 'Shot Form': 10, 'Shot Base': 22, 'Description': 'Ser Davos rode the line between non-legend and legend status for quite some time with his strange, side-spinning shot, finding decent success throughout his run. Can this new player succeed where Davos failed?'}, {'Name': 'Subway Jay', 'Shot Form': 56, 'Shot Base': 38, 'Description': "Subway Jay couldn't speak a lick of English, but if there was a language for basketball, he'd probably be a linguistics professor with his leg-kicking, ball-throwing, fun mess of a shot. Can this new player destroy the court like Jay killed it in the league?"}, {'Name': 'The Bro', 'Shot Form': 97, 'Shot Base': 64, 'Description': 'From utter garbage to the heights of legendry, back down to somewhere in between, The Bro has used his exotic shot to reach the extreme highs and lows of the 2k universe. Can this new player ramp it up like The Bro did with this unusual shot?'}, {'Name': 'Ish Tickletits', 'Shot Form': 82, 'Shot Base': 47, 'Description': "Known for his legendary run with Warren's squad in the 2k league, Ish dominated the league for 2 seasons with his sniper rifle shot. Can this new player dominate the competitive scene similarly with this classic shot?"}, {'Name': 'Sprite Agent', 'Shot Form': 101, 'Shot Base': 79, 'Description': 'Like a ghillie in the mist, Sprite Agent was a deadshot sniper with his bullet-like shooting form, finding himself major success in the late league days. Can this new player snipe the competition as Sprite Agent once did?'}, {'Name': 'Imperial Commander', 'Shot Form': 110, 'Shot Base': 57, 'Description': "Imperial Commander could probably shoot 50 basketballs in the span of 5 seconds with his laser-fast form, which made it incredibly hard to block the legendary player. May Imperial Commander's shot bless this new player with success and an increased will to murder Stormcloaks."}, {'Name': 'Ben Linus', 'Shot Form': 131, 'Shot Base': 54, 'Description': 'Ben Linus has charitably gifted many a basketball to the Martians with his unbelievably high-arching shot, but when they did come down, they fell in the hoop for this late-game legend. Can this new player reach the stars like Ben did?'}, {'Name': 'Stacy Harper', 'Shot Form': 146, 'Shot Base': 56, 'Description': 'Although Stacy never reached the expectations everyone had for him, his shot is still unrivaled in smoothness and pace of delivery. Can this new player break ground that Stacy never could with this buttery smooth shot?'}, {'Name': 'Albert Miller', 'Shot Form': 125, 'Shot Base': 4, 'Description': "Overshadowed by all-99 attribute scores, Albert Miller's crisp, high-floating shot may have had more of an impact on the god's career than scholars would give it credit for. Will this new player cement or destroy that theory?"}],
'Vigilante': [{'Name': 'Ser Davos', 'Shot Form': 10, 'Shot Base': 22, 'Description': 'Ser Davos rode the line between non-legend and legend status for quite some time with his strange, side-spinning shot, finding decent success throughout his run. Can this new player succeed where Davos failed?'}, {'Name': 'Subway Jay', 'Shot Form': 56, 'Shot Base': 38, 'Description': "Subway Jay couldn't speak a lick of English, but if there was a language for basketball, he'd probably be a linguistics professor with his leg-kicking, ball-throwing, fun mess of a shot. Can this new player destroy the court like Jay killed it in the league?"}, {'Name': 'The Thor', 'Shot Form': 125, 'Shot Base': 34, 'Description': 'Perhaps one of the fastest-to-legend players to date, Thor annihilated the competition with his high-arching shot in the murky days of 2k. Will this new player climb the ranks as fast as Thor with his own shot?'}, {'Name': 'Stacy Harper', 'Shot Form': 146, 'Shot Base': 56, 'Description': 'Although Stacy never reached the expectations everyone had for him, his shot is still unrivaled in smoothness and pace of delivery. Can this new player break ground that Stacy never could with this buttery smooth shot?'}, {'Name': 'Fat Kid', 'Shot Form': 89, 'Shot Base': 23, 'Description': "Less known for his straight up shot and more for his acrobatic abilites, Fat Kid's classic shot is still a staple to 2k and the mark of one of the first great 3 pt shooters. Can this new player make a name for himself using Fat Kid's age-old shot?"}, {'Name': 'Morgan Freeman', 'Shot Form': 131, 'Shot Base': 34, 'Description': 'You see those craters in the moon? Those are from Morgan Freeman launching the basketball into space every time he took a shot, finding him success as a multi-tool non-legend. Can this new player wreak havoc in space like Morgan did?'}, {'Name': 'Allfather Pickles', 'Shot Form': 17, 'Shot Base': 69, 'Description': "Going under the radar for most of his early days, Allfather truly broke out into stardom during the final stages of the league era, and it's a damn shame we couldn't witness more. Can this new player carry on such a short, but great legacy with Allfather's shot?"}],
'Medic': [{'Name': 'The Thinker', 'Shot Form': 135, 'Shot Base': 26, 'Description': 'Nobody was having any second thinking thoughts about the Thinker with his extraordinarily good, control dominating gameplay and shot. Can this new player revive the glory days of The Thinker with his classic shot?'}, {'Name': 'Morgan Freeman', 'Shot Form': 131, 'Shot Base': 34, 'Description': 'You see those craters in the moon? Those are from Morgan Freeman launching the basketball into space every time he took a shot, finding him success as a multi-tool non-legend. Can this new player wreak havoc in space like Morgan did?'}, {'Name': 'The Night King', 'Shot Form': 32, 'Shot Base': 71, 'Description': "At the very forefront of the early control meta, The Night King defined the meta as he raced to legend status with his clean shot and phenomenal rebounding skills faster than nearly anyone before him. Will this new player be able to say the same after using The Night King's shot?"}],
'Guardian': [{'Name': 'Jaquarius Nocturnal', 'Shot Form': 146, 'Shot Base': 6, 'Description': "Jaquarius didn't have the time to shine as much as his talent allowed him to, and everyone knew that he had what it took to be one of the Gods. His shot was as deadly as his footwork and rebounding. May this new player carry on a great legacy with Jay-Quay's shot."}, {'Name': 'The Night King', 'Shot Form': 32, 'Shot Base': 71, 'Description': "At the very forefront of the early control meta, The Night King defined the meta as he raced to legend status with his clean shot and phenomenal rebounding skills faster than nearly anyone before him. Will this new player be able to say the same after using The Night King's shot?"}, {'Name': 'The Thinker', 'Shot Form': 135, 'Shot Base': 26, 'Description': 'Nobody was having any second thinking thoughts about the Thinker with his extraordinarily good, control dominating gameplay and shot. Can this new player revive the glory days of The Thinker with his classic shot?'}, {'Name': 'Imperial Commander', 'Shot Form': 110, 'Shot Base': 57, 'Description': "Imperial Commander could probably shoot 50 basketballs in the span of 5 seconds with his laser-fast form, which made it incredibly hard to block the legendary player. May Imperial Commander's shot bless this new player with success and an increased will to murder Stormcloaks."}, {'Name': 'The Thor', 'Shot Form': 125, 'Shot Base': 34, 'Description': 'Perhaps one of the fastest-to-legend players to date, Thor anihilated the competition with his high-arching shot in the murky days of 2k. Will this new player climb the ranks as fast as Thor with his own shot?'}, {'Name': 'Morgan Freeman', 'Shot Form': 131, 'Shot Base': 34, 'Description': 'You see those craters in the moon? Those are from Morgan Freeman launching the basketball into space every time he took a shot, finding him success as a multi-tool non-legend. Can this new player wreak havoc in space like Morgan did?'}, {'Name': 'Allfather Pickles', 'Shot Form': 17, 'Shot Base': 69, 'Description': "Going under the radar for most of his early days, Allfather truly broke out into stardom during the final stages of the league era, and it's a damn shame we couldn't witness more. Can this new player carry on such a short, but great legacy with Allfather's shot?"}],
'Engineer': [{'Name': 'The Night King', 'Shot Form': 32, 'Shot Base': 71, 'Description': "At the very forefront of the early control meta, The Night King defined the meta as he raced to legend status with his clean shot and phenomenal rebounding skills faster than nearly anyone before him. Will this new player be able to say the same after using The Night King's shot?"}, {'Name': 'Imperial Commander', 'Shot Form': 110, 'Shot Base': 57, 'Description': "Imperial Commander could probably shoot 50 basketballs in the span of 5 seconds with his laser-fast form, which made it incredibly hard to block the legendary player. May Imperial Commander's shot bless this new player with success and an increased will to murder Stormcloaks."}, {'Name': 'Manager Sneh', 'Shot Form': 127, 'Shot Base': 108, 'Description': 'Despite his label as manager, Sneh was a god awful manager at Subway, but he did manage to sink in many a basketball with his smooth delivery. Can this new player manage to do the same?'}],
'Director': [{'Name': 'Manager Sneh', 'Shot Form': 127, 'Shot Base': 108, 'Description': 'Despite his label as manager, Sneh was a god awful manager at Subway, but he did manage to sink in many a basketball with his smooth delivery. Can this new player manage to do the same?'}, {'Name': 'Imperial Commander', 'Shot Form': 110, 'Shot Base': 57, 'Description': "Imperial Commander could probably shoot 50 basketballs in the span of 5 seconds with his laser-fast form, which made it incredibly hard to block the legendary player. May Imperial Commander's shot bless this new player with success and an increased will to murder Stormcloaks."}, {'Name': 'Ben Linus', 'Shot Form': 131, 'Shot Base': 54, 'Description': 'Ben Linus has charitably gifted many a basketball to the Martians with his unbelievably high-arching shot, but when they did come down, they fell in the hoop for this late-game legend. Can this new player reach the stars like Ben did?'}]
}
LEGENDARY_SPECIAL_SHOTS = {
'Slayer': [{'Name': 'Bill Nye', 'Shot Form': 53, 'Shot Base': 8, 'Description': 'Bill Nye will go down as the greatest 2k player to ever touch the blacktop and his shot will be remembered just as fondly. This new player has hit the jackpot, and the question turns not to whether he will be great, but when he will.'}, {'Name': 'Jacob Rogers', 'Shot Form': 6, 'Shot Base': 7, 'Description': "The ability to leap several feet higher than a normal human being, coupled with a short-statured legend was enough to carry Jake Rogers into God-tier for the entirety of 2ks run. Will the grace of Jake's leap and clean release aid this new player in doing the same?"}, {'Name': 'Timmy Nocturnal', 'Shot Form': 91, 'Shot Base': 42, 'Description': "An uncontested Timmy Nocturnal could take a shot from orbit, locked in a titanium cell, music blasting in his ears, and sink it without batting a fucking eye. Will this player ever miss with Timmy's buttery smooth shooting form?"}, {'Name': 'Jimmy Nocturnal', 'Shot Form': 50, 'Shot Base': 45, 'Description': "The OG, first-ever legend, classic of all classics, Jimmy Nocturnal put everyone into a coffin when he hit the court with his unmistakably clean 3s. Can this new player rebirth what once was with Jimmy's timeless shot?"}, {'Name': 'Dan Harrison', 'Shot Form': 60, 'Shot Base': 44, 'Description': "A shot from the heavens, Dan Harrison's smooth and hasty delivery left every player's jaw on the floor after his godlike dominance at the end of the last league season. Can this new player stand on the shoulders of a giant like Dan?"}, {'Name': 'Lipton Strawberry', 'Shot Form': 91, 'Shot Base': 103, 'Description': "Lipton Strawberry defined an entire era of 2k play with his unblockable, unmissable, destructively clean shot. Will this new player live up to the godly expectations of Lipton's perfect shot?"}],
'Vigilante': [{'Name': 'Jimmy Nocturnal', 'Shot Form': 50, 'Shot Base': 45, 'Description': "The OG, first-ever legend, classic of all classics, Jimmy Nocturnal put everyone into a coffin when he hit the court with his unmistakably clean 3s. Can this new player rebirth what once was with Jimmy's timeless shot?"}, {'Name': 'Dan Harrison', 'Shot Form': 60, 'Shot Base': 44, 'Description': "A shot from the heavens, Dan Harrison's smooth and hasty delivery left every player's jaw on the floor after his godlike dominance at the end of the last league season. Can this new player stand on the shoulders of a giant like Dan?"}, {'Name': 'Dek Nara', 'Shot Form': 125, 'Shot Base': 20, 'Description': "Dek Nara literally pioneered the term God for 2k, and had to be literally banned from play for being so unbelievably good with his high-arching bomb of a shot. This new player should feel honored to carry on the Hawaiian peace God's classic shot."}],
'Medic': [{'Name': 'Lipton Strawberry', 'Shot Form': 91, 'Shot Base': 103, 'Description': "Lipton Strawberry defined an entire era of 2k play with his unblockable, unmissable, destructively clean shot. Will this new player live up to the godly expectations of Lipton's perfect shot?"}],
'Guardian': [{'Name': 'Jimmy Nocturnal', 'Shot Form': 50, 'Shot Base': 45, 'Description': "The OG, first-ever legend, classic of all classics, Jimmy Nocturnal put everyone into a coffin when he hit the court with his unmistakably clean 3s. Can this new player rebirth what once was with Jimmy's timeless shot?"}, {'Name': 'Lipton Strawberry', 'Shot Form': 91, 'Shot Base': 103, 'Description': "Lipton Strawberry defined an entire era of 2k play with his unblockable, unmissable, destructively clean shot. Will this new player live up to the godly expectations of Lipton's perfect shot?"}, {'Name': 'Dan Harrison', 'Shot Form': 60, 'Shot Base': 44, 'Description': "A shot from the heavens, Dan Harrison's smooth and hasty delivery left every player's jaw on the floor after his godlike dominance at the end of the last league season. Can this new player stand on the shoulders of a giant like Dan?"}],
'Engineer': [{'Name': 'Abe Lincoln', 'Shot Form': 91, 'Shot Base': 53, 'Description': "There isn't much to say that hasn't already been said about Abe's silky smooth shot in the history of 2k. This new player should feel blessed to carry on one of the greatest shots ever introduced to 2k."}, {'Name': 'Bill Nye', 'Shot Form': 53, 'Shot Base': 8, 'Description': 'Bill Nye will go down as the greatest 2k player to ever touch the blacktop and his shot will be remembered just as fondly. This new player has hit the jackpot, and the question turns not to whether he will be great, but when he will.'}],
'Director': [{'Name': 'Abe Lincoln', 'Shot Form': 91, 'Shot Base': 53, 'Description': "There isn't much to say that hasn't already been said about Abe's silky smooth shot in the history of 2k. This new player should feel blessed to carry on one of the greatest shots ever introduced to 2k."}, {'Name': 'Jacob Rogers', 'Shot Form': 6, 'Shot Base': 7, 'Description': "The ability to leap several feet higher than a normal human being, coupled with a short-statured legend was enough to carry Jake Rogers into God-tier for the entirety of 2ks run. Will the grace of Jake's leap and clean release aid this new player in doing the same?"}, {'Name': 'Bill Nye', 'Shot Form': 53, 'Shot Base': 8, 'Description': 'Bill Nye will go down as the greatest 2k player to ever touch the blacktop and his shot will be remembered just as fondly. This new player has hit the jackpot, and the question turns not to whether he will be great, but when he will.'}]
}

#endregion === Globals ===

#region === Vigilante ===

def Vigilante_Rare_NancyEmail(player : Player.Player):
    pmod = Player.getPModTemplate()
    # Artifact Name
    pmod["Name"] = '''A Nasty Email from Nancy Soleto'''
    # Artifact Info
    pmod["Type"]["TypeName"] = "Artifact"
    pmod["Type"]["ArchetypeLock"] = "Vigilante"
    pmod["Type"]["Rarity"] = "Rare"
    # Description
    pmod["Description"] = '''Confused by the ferocious nature of a message about putting hyphens in a line of service in TMA, the player changes as follows: Add 10 to all accented secondary attributes. Subtract 10 from all non-accented secondary attributes. Add Scrapper.'''

    # Implementation
    for secondaryAttribute in player["Archetype"].secondaryAttributes:
        if(secondaryAttribute in player["Archetype"].accentedAttributes):
            pmod["Modifications"].append({"Operation": "Add", "Key": secondaryAttribute, "Value": 10})
        else:
            pmod["Modifications"].append({"Operation": "Subtract", "Key": secondaryAttribute, "Value": 10})

    pmod["Modifications"].append({"Operation" : "Set", "Key" : "SigSkill1", "Value" : "Scrapper"})

    # Return
    return pmod
def Vigilante_Rare_ChapApology(player : Player.Player):
    pmod = Player.getPModTemplate()
    # Artifact Name
    pmod["Name"] = '''A Written Apology from Chap'''
    # Artifact Info
    pmod["Type"]["TypeName"] = "Artifact"
    pmod["Type"]["ArchetypeLock"] = "Vigilante"
    pmod["Type"]["Rarity"] = "Rare"
    # Description
    pmod["Description"] = '''Feeling completely unsatisfied by Chap's attempt at an apology which somehow reads as him being the savior of the situation, the player adds 10 to all non-accented secondary attributes. Also subtracts 10 to all accented secondary attributes. Adds Antifreeze and Heat Retention.'''

    # Implementation
    for secondaryAttribute in player["Archetype"].secondaryAttributes:
        if(secondaryAttribute in player["Archetype"].accentedAttributes):
            pmod["Modifications"].append({"Operation": "Subtract", "Key": secondaryAttribute, "Value": 10})
        else:
            pmod["Modifications"].append({"Operation": "Add", "Key": secondaryAttribute, "Value": 10})

    pmod["Modifications"].append({"Operation" : "Set", "Key" : "SigSkill1", "Value" : "Anti-Freeze"})
    pmod["Modifications"].append({"Operation" : "Set", "Key" : "SigSkill2", "Value" : "Heat Retention"})

    # Return
    return pmod
def Vigilante_Rare_NatHound(player : Player.Player):
    pmod = Player.getPModTemplate()
    # Artifact Name
    pmod["Name"] = '''Nat's Vicious, Bloodthirsty Hound from Hell'''
    # Artifact Info
    pmod["Type"]["TypeName"] = "Artifact"
    pmod["Type"]["ArchetypeLock"] = "Vigilante"
    pmod["Type"]["Rarity"] = "Rare"
    # Description
    pmod["Description"] = '''The demon living in Nat's golden retriever has left its host and has attached itself to the player, changing the player as follows: Add 20 to Vertical, Dunk, and Standing Dunk. -5 to all non-accented primary stats. Add Posterizer and Highlight Film.'''

    # Implementation
    pmod["Modifications"].append({"Operation": "Add", "Key": "SVertical", "Value": 20})
    pmod["Modifications"].append({"Operation": "Add", "Key": "SDunk", "Value": 20})
    pmod["Modifications"].append({"Operation": "Add", "Key": "SStdDunk", "Value": 20})

    for primaryAttribute in player["Archetype"].primaryAttributes:
        if(primaryAttribute in player["Archetype"].unaccentedAttributes):
            pmod["Modifications"].append({"Operation": "Subtract", "Key": primaryAttribute, "Value": 5})

    pmod["Modifications"].append({"Operation" : "Set", "Key" : "SigSkill1", "Value" : "Posterizer"})
    pmod["Modifications"].append({"Operation" : "Set", "Key" : "SigSkill2", "Value" : "Highlight Film"})

    # Return
    return pmod
def Vigilante_Rare_RumoroShrug(player : Player.Player):
    pmod = Player.getPModTemplate()
    # Artifact Name
    pmod["Name"] = '''A Smile and a Shrug from Nick Rumoro'''
    # Artifact Info
    pmod["Type"]["TypeName"] = "Artifact"
    pmod["Type"]["ArchetypeLock"] = "Vigilante"
    pmod["Type"]["Rarity"] = "Rare"
    # Description
    pmod["Description"] = '''Sitting in a dulled state of shock after Nick just messaged him 'Everyone does it, get over yourself', shortly following him calling Road Hog for 40 minutes, the player changes as follows: Add 5 to all non-accented primary stats. Subtract 20 from Vertical, Dunk, and Standing Dunk. Add Shot Creator'''

    # Implementation
    pmod["Modifications"].append({"Operation": "Subtract", "Key": "SVertical", "Value": 20})
    pmod["Modifications"].append({"Operation": "Subtract", "Key": "SDunk", "Value": 20})
    pmod["Modifications"].append({"Operation": "Subtract", "Key": "SStdDunk", "Value": 20})

    for primaryAttribute in player["Archetype"].primaryAttributes:
        if(primaryAttribute in player["Archetype"].unaccentedAttributes):
            pmod["Modifications"].append({"Operation": "Add", "Key": primaryAttribute, "Value": 5})

    pmod["Modifications"].append({"Operation" : "Set", "Key" : "SigSkill1", "Value" : "Shot Creator"})

    # Return
    return pmod
def Vigilante_Epic_FernNo(player : Player.Player):
    pmod = Player.getPModTemplate()
    # Artifact Name
    pmod["Name"] = '''A 'No.' from Fernando Valencia, After Being Asked to Accept the Transfer of a User He's Been Working With'''
    # Artifact Info
    pmod["Type"]["TypeName"] = "Artifact"
    pmod["Type"]["ArchetypeLock"] = "Vigilante"
    pmod["Type"]["Rarity"] = "Epic"
    # Description
    pmod["Description"] = '''Feeling belittled and a bit confused from the overly confident rejection, the player adds a rare or epic Engineer special shot:\n\n'''

    # Implementation
    potentialSpecialShots = RARE_SPECIAL_SHOTS["Vigilante"] + EPIC_SPECIAL_SHOTS["Vigilante"]
    specialShotChoice = random.choice(potentialSpecialShots)
    pmod["Modifications"].append({"Operation": "Set", "Key": "AShtForm", "Value": specialShotChoice["Shot Form"]})
    pmod["Modifications"].append({"Operation": "Set", "Key": "AShtBase", "Value": specialShotChoice["Shot Base"]})
    pmod["Description"] += f"**{specialShotChoice['Name']}** - {specialShotChoice['Description']}"

    # Return
    return pmod
def Vigilante_Epic_DrewGall(player : Player.Player):
    pmod = Player.getPModTemplate()
    # Artifact Name
    pmod["Name"] = '''The Gall of Drew Meier'''
    # Artifact Info
    pmod["Type"]["TypeName"] = "Artifact"
    pmod["Type"]["ArchetypeLock"] = "Vigilante"
    pmod["Type"]["Rarity"] = "Epic"
    # Description
    pmod["Description"] = '''Feeling enraged by the absolute nerve of fellow coworker Drew Meier passing his 9th call of the day, the player spitefully changes as follows: Set Passing and Quickness to 99.  Add Dimer and Alley-Ooper. -10 to all primary stats.'''

    # Implementation
    pmod["Modifications"].append({"Operation": "Set", "Key": "SPass", "Value": 99})
    pmod["Modifications"].append({"Operation": "Set", "Key": "SQuick", "Value": 99})

    for primaryAttribute in player["Archetype"].primaryAttributes:
        pmod["Modifications"].append({"Operation": "Subtract", "Key": primaryAttribute, "Value": 10})

    pmod["Modifications"].append({"Operation": "Set", "Key": "SigSkill1", "Value": "Dimer"})
    pmod["Modifications"].append({"Operation": "Set", "Key": "SigSkill2", "Value": "Alley Oopers"})

    # Return
    return pmod
def Vigilante_Epic_ChandaraCandor(player : Player.Player):
    pmod = Player.getPModTemplate()
    # Artifact Name
    pmod["Name"] = '''The Quiet and Friendly Candor of Chandara Cheng'''
    # Artifact Info
    pmod["Type"]["TypeName"] = "Artifact"
    pmod["Type"]["ArchetypeLock"] = "Vigilante"
    pmod["Type"]["Rarity"] = "Epic"
    # Description
    pmod["Description"] = '''Feeling at peace from the soothing and rhythmic tones of Mr. Cheng, the player is changed as follows: Add 10 to all accented primary attributes. Add 10 to all tertiary stats. Subtract 20 from all non-accented attributes. Add 30 to Strength.'''

    # Implementation
    for attribute in Archetypes.ALL_ATTRIBUTES:
        if(attribute == "SStrength"):
            if("SStrength" in player["Archetype"].unaccentedAttributes):
                pmod["Modifications"].append({"Operation": "Add", "Key": attribute, "Value": 10})
            else:
                pmod["Modifications"].append({"Operation": "Add", "Key": attribute, "Value": 30})
        elif(attribute in player["Archetype"].tertiaryAttributes):
            if(attribute in player["Archetype"].unaccentedAttributes):
                pmod["Modifications"].append({"Operation": "Subtract", "Key": attribute, "Value": 10})
            else:
                pmod["Modifications"].append({"Operation": "Add", "Key": attribute, "Value": 10})
        elif(attribute in player["Archetype"].primaryAttributes):
            if(attribute in player["Archetype"].accentedAttributes):
                pmod["Modifications"].append({"Operation": "Add", "Key": attribute, "Value": 10})
        elif(attribute in player["Archetype"].unaccentedAttributes):
            pmod["Modifications"].append({"Operation": "Subtract", "Key": attribute, "Value": 20})



    # Return
    return pmod
def Vigilante_Epic_EddieTHanks(player : Player.Player):
    pmod = Player.getPModTemplate()
    # Artifact Name
    pmod["Name"] = '''Eddie Smith's Memoir, 'THanks for Nothing\''''
    # Artifact Info
    pmod["Type"]["TypeName"] = "Artifact"
    pmod["Type"]["ArchetypeLock"] = "Vigilante"
    pmod["Type"]["Rarity"] = "Epic"
    # Description
    pmod["Description"] = '''Mentally recovering from that journey of a story, the player receives the following changes: Set Vertical and Shoot off Dribble to 25. Set player's shot to a Set Shot. Add 10 to 3pt Shot. Add Deadeye.'''

    # Implementation
    pmod["Modifications"].append({"Operation": "Set", "Key": "SShtOfD", "Value": 25})
    pmod["Modifications"].append({"Operation": "Set", "Key": "SVertical", "Value": 25})

    pmod["Modifications"].append({"Operation": "Set", "Key": "AShtBase", "Value": random.randrange(41,59)})

    pmod["Modifications"].append({"Operation": "Add", "Key": "SSht3PT", "Value": 10})
    pmod["Modifications"].append({"Operation": "Set", "Key": "SigSkill1", "Value": "Deadeye"})



    # Return
    return pmod
def Vigilante_Legendary_TrumpChina(player : Player.Player):
    pmod = Player.getPModTemplate()
    # Artifact Name
    pmod["Name"] = '''Artistic Interpretation of Donald Trump's Relationship with China'''
    # Artifact Info
    pmod["Type"]["TypeName"] = "Artifact"
    pmod["Type"]["ArchetypeLock"] = "Vigilante"
    pmod["Type"]["Rarity"] = "Legendary"
    # Description
    pmod["Description"] = '''It's very big and beautiful, the greatest art. I do have to say it is really great. This sets the player's height to 7'6. Set all Signature Skills to Yao Ming's. Set Vertical to 25, and all secondary stats randomized between 25-40. Add Finisher and Deadeye skills.'''

    # Implementation
    pmod["Modifications"].append({"Operation": "Set", "Key": "HeightIn", "Value": 90})
    pmod["Modifications"].append({"Operation": "Set", "Key": "SVertical", "Value": 25})

    for secondaryAttribute in player["Archetype"].secondaryAttributes:
        pmod["Modifications"].append({"Operation": "Set", "Key": secondaryAttribute, "Value": random.randrange(25,41)})
    
    pmod["Modifications"].append({"Operation": "Set", "Key": "SigSkill1", "Value": "Finisher"})
    pmod["Modifications"].append({"Operation": "Set", "Key": "SigSkill2", "Value": "Deadeye"})

    pmod["Modifications"].append({"Operation": "Set", "Key": "AShtBase", "Value": 124})
    pmod["Modifications"].append({"Operation": "Set", "Key": "AFadeaway", "Value": 30})



    # Return
    return pmod
def Vigilante_Legendary_DickScorecard(player: Player.Player):
    pmod = Player.getPModTemplate()
    # Artifact Name
    pmod["Name"] = '''An Antique Scorecard of the S1 League Championship Game, Signed "A Fine Effort from an Extraordinary Team" by Charles Dick'''
    # Artifact Info
    pmod["Type"]["TypeName"] = "Artifact"
    pmod["Type"]["ArchetypeLock"] = "Vigilante"
    pmod["Type"]["Rarity"] = "Legendary"
    # Description
    pmod[
        "Description"] = '''Shedding a tear at such a beautiful piece of 2k history, the player is reformed in the following fashion: Subtract 10 from all stats. Add Microwave, Deadeye, Spot-up Shooter, Shot Creator, and War General.  Get an epic or legendary special shot:\n\n'''

    # Implementation
    for attribute in Archetypes.ALL_ATTRIBUTES:
        pmod["Modifications"].append({"Operation": "Subtract", "Key": attribute, "Value": 10})

    pmod["Modifications"].append({"Operation": "Set", "Key": "SigSkill1", "Value": "Microwave"})
    pmod["Modifications"].append({"Operation": "Set", "Key": "SigSkill2", "Value": "Deadeye"})
    pmod["Modifications"].append({"Operation": "Set", "Key": "SigSkill3", "Value": "Spot Up Shooter"})
    pmod["Modifications"].append({"Operation": "Set", "Key": "SigSkill4", "Value": "Shot Creator"})
    pmod["Modifications"].append({"Operation": "Set", "Key": "SigSkill5", "Value": "Floor General"})

    potentialSpecialShots = LEGENDARY_SPECIAL_SHOTS["Vigilante"] + EPIC_SPECIAL_SHOTS["Vigilante"]
    specialShotChoice = random.choice(potentialSpecialShots)
    pmod["Modifications"].append({"Operation": "Set", "Key": "AShtForm", "Value": specialShotChoice["Shot Form"]})
    pmod["Modifications"].append({"Operation": "Set", "Key": "AShtBase", "Value": specialShotChoice["Shot Base"]})
    pmod["Description"] += f"**{specialShotChoice['Name']}** - {specialShotChoice['Description']}"


    # Return
    return pmod
def Vigilante_Legendary_EggrollVoucher(player: Player.Player):
    pmod = Player.getPModTemplate()
    # Artifact Name
    pmod["Name"] = '''Voucher Reading '25 percnt of Next Spicy at Eggrol r We', Gloriously Lacking an Expiration Date'''
    # Artifact Info
    pmod["Type"]["TypeName"] = "Artifact"
    pmod["Type"]["ArchetypeLock"] = "Vigilante"
    pmod["Type"]["Rarity"] = "Legendary"
    # Description
    pmod["Description"] = '''Visit Eggrolls R We 1-7 times. For each time you visit, -4 to all attributes, and make another random zone Hot. If the same zone is selected twice, it becomes Burning.\n\n'''

    # Implementation
    eggrollVisits = random.randrange(1,8)

    for attribute in Archetypes.ALL_ATTRIBUTES:
        pmod["Modifications"].append({"Operation": "Subtract", "Key": attribute, "Value": eggrollVisits * 4})

    possibleZones = ["HZ1","HZ2","HZ3","HZ4","HZ5","HZ6","HZ7","HZ8","HZ9","HZ10","HZ11","HZ12","HZ13","HZ14"]
    spicedZones = {}
    for i in range(eggrollVisits):
        thisSpiceyZone = random.choice(possibleZones)
        if(thisSpiceyZone in spicedZones.keys()):
            spicedZones[thisSpiceyZone] = 3
        else:
            spicedZones[thisSpiceyZone] = 2

    for zone,value in spicedZones.items():
        pmod["Modifications"].append({"Operation": "Set", "Key": zone, "Value": value})

    if(eggrollVisits > 1):
        pmod["Description"] += f"This player ordered the spicy at Eggrolls R We {eggrollVisits} times."
    else:
        pmod["Description"] += f"This player ordered the spicy at Eggrolls R We {eggrollVisits} time."

    # Return
    return pmod

#endregion === Vigilante ===

#region === Medics ===

def Medic_Rare_SubwayGiftcard(player : Player.Player):
    pmod = Player.getPModTemplate()
    # Artifact Name
    pmod["Name"] = '''$10 Subway Gift Card, 8 years expired.'''
    # Artifact Info
    pmod["Type"]["TypeName"] = "Artifact"
    pmod["Type"]["ArchetypeLock"] = "Medic"
    pmod["Type"]["Rarity"] = "Rare"
    # Description
    pmod["Description"] = '''Not enough to buy a 6 inch steak and cheese sandwich, but just enough to buy a miniature pizza. Add +10 to Offensive, Defensive Rebound, and Vertical. -10 to all Secondary Stats. Add Break Starter.'''

    # Implementation
    pmod["Modifications"].append({"Operation" : "Add", "Key" : "SDReb", "Value" : 10})
    pmod["Modifications"].append({"Operation" : "Add", "Key" : "SOReb", "Value" : 10})
    pmod["Modifications"].append({"Operation" : "Add", "Key" : "SVertical", "Value" : 10})
    for secondaryAttribute in player["Archetype"].secondaryAttributes:
        pmod["Modifications"].append({"Operation": "Subtract", "Key": secondaryAttribute, "Value": 10})

    pmod["Modifications"].append({"Operation" : "Set", "Key" : "SigSkill1", "Value" : "Break Starter"})

    # Return
    return pmod
def Medic_Rare_WrapApron(player : Player.Player):
    pmod = Player.getPModTemplate()
    # Artifact Name
    pmod["Name"] = ''''This is How You Wrap' Apron'''
    # Artifact Info
    pmod["Type"]["TypeName"] = "Artifact"
    pmod["Type"]["ArchetypeLock"] = "Medic"
    pmod["Type"]["Rarity"] = "Rare"
    # Description
    pmod["Description"] = '''Stylish and groovy, this will surely make the player fit in with the cool crowd. Add +10 to all Secondary Stats. -10 to Offensive, Defensive Rebound, and Vertical. Add Post Playmaker.'''

    # Implementation
    pmod["Modifications"].append({"Operation" : "Subtract", "Key" : "SDReb", "Value" : 10})
    pmod["Modifications"].append({"Operation" : "Subtract", "Key" : "SOReb", "Value" : 10})
    pmod["Modifications"].append({"Operation" : "Subtract", "Key" : "SVertical", "Value" : 10})
    for secondaryAttribute in player["Archetype"].secondaryAttributes:
        pmod["Modifications"].append({"Operation": "Add", "Key": secondaryAttribute, "Value": 10})

    pmod["Modifications"].append({"Operation" : "Set", "Key" : "SigSkill1", "Value" : "Post Playmaker"})

    # Return
    return pmod
def Medic_Rare_Jardeenya(player : Player.Player):
    pmod = Player.getPModTemplate()
    # Artifact Name
    pmod["Name"] = '''An Audio Recording of a Customer Inquiring: 'Can I have the uh JARDEENYA peppas?\''''
    # Artifact Info
    pmod["Type"]["TypeName"] = "Artifact"
    pmod["Type"]["ArchetypeLock"] = "Medic"
    pmod["Type"]["Rarity"] = "Rare"
    # Description
    pmod["Description"] = '''Stunned by the complete butchering of the topping, the player changes as follows: Add +10 to Speed and Quickness. -10 to Strength and On Ball Defense. Add Chasedown Artist.'''

    # Implementation
    pmod["Modifications"].append({"Operation" : "Add", "Key" : "SSpeed", "Value" : 10})
    pmod["Modifications"].append({"Operation" : "Add", "Key" : "SQuick", "Value" : 10})
    pmod["Modifications"].append({"Operation" : "Subtract", "Key" : "SStrength", "Value" : 10})
    pmod["Modifications"].append({"Operation" : "Subtract", "Key" : "SOnBallD", "Value" : 10})

    pmod["Modifications"].append({"Operation" : "Set", "Key" : "SigSkill1", "Value" : "Chase Down Artist"})

    # Return
    return pmod
def Medic_Rare_HoneyOat(player : Player.Player):
    pmod = Player.getPModTemplate()
    # Artifact Name
    pmod["Name"] = '''Newspaper Cutout Advertising the Honey Oat Bread from 2009'''
    # Artifact Info
    pmod["Type"]["TypeName"] = "Artifact"
    pmod["Type"]["ArchetypeLock"] = "Medic"
    pmod["Type"]["Rarity"] = "Rare"
    # Description
    pmod["Description"] = '''Gaslit into thinking that perhaps this bread still exists, the player changes: Add +10 to Strength to On Ball Defense.  -10 to Speed and Quickness. Add Lockdown Defender.'''

    # Implementation
    pmod["Modifications"].append({"Operation" : "Subtract", "Key" : "SSpeed", "Value" : 10})
    pmod["Modifications"].append({"Operation" : "Subtract", "Key" : "SQuick", "Value" : 10})
    pmod["Modifications"].append({"Operation" : "Add", "Key" : "SStrength", "Value" : 10})
    pmod["Modifications"].append({"Operation" : "Add", "Key" : "SOnBallD", "Value" : 10})

    pmod["Modifications"].append({"Operation" : "Set", "Key" : "SigSkill1", "Value" : "Lockdown Defender"})

    # Return
    return pmod
def Medic_Epic_VileSauces(player : Player.Player):
    pmod = Player.getPModTemplate()
    # Artifact Name
    pmod["Name"] = '''A Plastic Bin Filled with a Vile Mixure of Spilled Sauces'''
    # Artifact Info
    pmod["Type"]["TypeName"] = "Artifact"
    pmod["Type"]["ArchetypeLock"] = "Medic"
    pmod["Type"]["Rarity"] = "Epic"
    # Description
    pmod["Description"] = '''Disgusted by the oozing slime within the bin, the player seeks better things and adds a rare or epic Engineer special shot:\n\n'''

    # Implementation
    potentialSpecialShots = RARE_SPECIAL_SHOTS["Medic"] + EPIC_SPECIAL_SHOTS["Medic"]
    specialShotChoice = random.choice(potentialSpecialShots)
    pmod["Modifications"].append({"Operation": "Set", "Key": "AShtForm", "Value": specialShotChoice["Shot Form"]})
    pmod["Modifications"].append({"Operation": "Set", "Key": "AShtBase", "Value": specialShotChoice["Shot Base"]})
    pmod["Description"] += f"**{specialShotChoice['Name']}** - {specialShotChoice['Description']}"

    # Return
    return pmod
def Medic_Epic_CaptionedPhoto(player : Player.Player):
    pmod = Player.getPModTemplate()
    # Artifact Name
    pmod["Name"] = '''A Circled, Highlighted, and Captioned Photo of a Single Olive on the Floor of a Subway Restaurant'''
    # Artifact Info
    pmod["Type"]["TypeName"] = "Artifact"
    pmod["Type"]["ArchetypeLock"] = "Medic"
    pmod["Type"]["Rarity"] = "Epic"
    # Description
    pmod["Description"] = '''Perplexed at the hollywood-esque lengths that Sneh went to produce an image of a tiny fruit, the player morphs as follows: Add +15 to all accented secondary attributes. Set Low-Post Offense to 99. -15 to all non-accented primary attributes. -10 to both Rebounds. Add Ankle Breaker.'''

    # Implementation
    for accentedAttribute in player["Archetype"].accentedAttributes:
        if(accentedAttribute in player["Archetype"].secondaryAttributes):
            pmod["Modifications"].append({"Operation": "Add", "Key": accentedAttribute, "Value": 15})
    for unaccentedAttribute in player["Archetype"].unaccentedAttributes:
        if(unaccentedAttribute in player["Archetype"].primaryAttributes):
            pmod["Modifications"].append({"Operation": "Subtract", "Key": unaccentedAttribute, "Value": 15})

    pmod["Modifications"].append({"Operation": "Set", "Key": "SDLowPost", "Value": 99})
    pmod["Modifications"].append({"Operation": "Subtract", "Key": "SOReb", "Value": 10})
    pmod["Modifications"].append({"Operation": "Subtract", "Key": "SDReb", "Value": 10})

    pmod["Modifications"].append({"Operation": "Set", "Key": "SigSkill1", "Value": "Ankle Breaker"})



    # Return
    return pmod
def Medic_Epic_SpotlessGloves(player : Player.Player):
    pmod = Player.getPModTemplate()
    # Artifact Name
    pmod["Name"] = '''Spotlessly Clean Gloves, demanded to be removed 15 seconds after they were acquired.'''
    # Artifact Info
    pmod["Type"]["TypeName"] = "Artifact"
    pmod["Type"]["ArchetypeLock"] = "Medic"
    pmod["Type"]["Rarity"] = "Epic"
    # Description
    pmod["Description"] = '''Feeling depressed that these beautiful gloves had to go to waste because of an obnoxious, power-hungry sewer mutant of a human being, the player changes as follows: Add 40 to Pass and Hands. -15 to all non-accented Primary and Secondary stats. Add Dimer, Break Starter, and Scrapper.'''

    # Implementation
    for unaccentedAttribute in player["Archetype"].unaccentedAttributes:
        if(unaccentedAttribute in player["Archetype"].primaryAttributes or unaccentedAttribute in player["Archetype"].secondaryAttributes):
            pmod["Modifications"].append({"Operation": "Subtract", "Key": unaccentedAttribute, "Value": 15})

    pmod["Modifications"].append({"Operation": "Add", "Key": "SPass", "Value": 40})
    pmod["Modifications"].append({"Operation": "Add", "Key": "SHands", "Value": 40})

    pmod["Modifications"].append({"Operation": "Set", "Key": "SigSkill1", "Value": "Dimer"})
    pmod["Modifications"].append({"Operation": "Set", "Key": "SigSkill2", "Value": "Break Starter"})
    pmod["Modifications"].append({"Operation": "Set", "Key": "SigSkill3", "Value": "Scrapper"})



    # Return
    return pmod
def Medic_Epic_CCTVFootage(player : Player.Player):
    pmod = Player.getPModTemplate()
    # Artifact Name
    pmod["Name"] = '''CCTV Footage of a Car Banging a U-Turn on the Road Adjacent to Subway'''
    # Artifact Info
    pmod["Type"]["TypeName"] = "Artifact"
    pmod["Type"]["ArchetypeLock"] = "Medic"
    pmod["Type"]["Rarity"] = "Epic"
    # Description
    pmod["Description"] = '''Yep, brace for the dreaded beep. The player changes while bracing for the drive-thru customer in the following way: Add +10 to accented Primary Skills. Spot up tendencies/hotspots will be set to almost always have the player post up for 3s. Add Alley-ooper and Deadeye.'''

    # Implementation
    for accentedAttribute in player["Archetype"].accentedAttributes:
        if(accentedAttribute in player["Archetype"].primaryAttributes):
            pmod["Modifications"].append({"Operation": "Subtract", "Key": accentedAttribute, "Value": 10})

    pmod["Modifications"].append({"Operation": "Set", "Key": "TPostUp", "Value": random.randrange(1,21)})
    pmod["Modifications"].append({"Operation": "Set", "Key": "TPostUp", "Value": random.randrange(70,101)})
    pmod["Modifications"].append({"Operation": "Set", "Key": "HSpt3PLCr", "Value": 15})
    pmod["Modifications"].append({"Operation": "Set", "Key": "HSpt3PLWg", "Value": 15})
    pmod["Modifications"].append({"Operation": "Set", "Key": "HSpt3PTop", "Value": 15})
    pmod["Modifications"].append({"Operation": "Set", "Key": "HSpt3PRWg", "Value": 15})
    pmod["Modifications"].append({"Operation": "Set", "Key": "HSpt3PRCr", "Value": 15})
    pmod["Modifications"].append({"Operation": "Set", "Key": "HSptMdLBl", "Value": 5})
    pmod["Modifications"].append({"Operation": "Set", "Key": "HSptMdLWg", "Value": 5})
    pmod["Modifications"].append({"Operation": "Set", "Key": "HSptMdCtr", "Value": 5})
    pmod["Modifications"].append({"Operation": "Set", "Key": "HSptMdRWg", "Value": 5})
    pmod["Modifications"].append({"Operation": "Set", "Key": "HSptMdRBl", "Value": 5})

    pmod["Modifications"].append({"Operation": "Set", "Key": "SigSkill1", "Value": "Alley Oopers"})
    pmod["Modifications"].append({"Operation": "Set", "Key": "SigSkill2", "Value": "Deadeye"})



    # Return
    return pmod
def Medic_Legendary_CompressOMatic(player : Player.Player):
    pmod = Player.getPModTemplate()
    # Artifact Name
    pmod["Name"] = '''The Compress-O-Matic, invented by Fredwardo Jalapeno'''
    # Artifact Info
    pmod["Type"]["TypeName"] = "Artifact"
    pmod["Type"]["ArchetypeLock"] = "Medic"
    pmod["Type"]["Rarity"] = "Legendary"
    # Description
    pmod["Description"] = '''Enter the Compress-O-Matic 1-5 times, each time the player enters they are squished and lose 3 inches of height, while gaining 5-10 to all secondary attributes.\n\n'''

    # Implementation
    compressions = random.randrange(1,6)
    pmod["Modifications"].append({"Operation": "Subtract", "Key": "HeightIn", "Value": compressions * 3})
    for secondaryAttribute in player["Archetype"].secondaryAttributes:
        pmod["Modifications"].append({"Operation": "Add", "Key": secondaryAttribute, "Value": compressions * random.randrange(5,11)})


    if(compressions > 1):
        pmod["Description"] += f"This player entered and re-entered the Compress-O-Matic {compressions} times."
    else:
        pmod["Description"] += f"This player entered the Compress-O-Matic {compressions} time."

    # Return
    return pmod
def Medic_Legendary_RancidStrawberry(player : Player.Player):
    pmod = Player.getPModTemplate()
    # Artifact Name
    pmod["Name"] = '''A Rancid Strawberry'''
    # Artifact Info
    pmod["Type"]["TypeName"] = "Artifact"
    pmod["Type"]["ArchetypeLock"] = "Medic"
    pmod["Type"]["Rarity"] = "Legendary"
    # Description
    pmod["Description"] = '''Pucker up, this strawberry is pungent with flavor tasted sparingly since the early days of Spritopia. -20 to all primary stats. -10 to all secondary stats. +40 to 3pt.  Get a random epic or legendary special shot:\n\n'''

    # Implementation
    for primaryAttribute in player["Archetype"].primaryAttributes:
        pmod["Modifications"].append({"Operation": "Subtract", "Key": primaryAttribute, "Value": 20})
    for secondaryAttribute in player["Archetype"].secondaryAttributes:
        pmod["Modifications"].append({"Operation": "Subtract", "Key": secondaryAttribute, "Value": 10})
    pmod["Modifications"].append({"Operation": "Add", "Key": "SSht3PT", "Value": 40})

    potentialSpecialShots = LEGENDARY_SPECIAL_SHOTS["Medic"] + EPIC_SPECIAL_SHOTS["Medic"]
    specialShotChoice = random.choice(potentialSpecialShots)
    pmod["Modifications"].append({"Operation": "Set", "Key": "AShtForm", "Value": specialShotChoice["Shot Form"]})
    pmod["Modifications"].append({"Operation": "Set", "Key": "AShtBase", "Value": specialShotChoice["Shot Base"]})
    pmod["Description"] += f"**{specialShotChoice['Name']}** - {specialShotChoice['Description']}"

    # Return
    return pmod
def Medic_Legendary_GreasyIPhone(player : Player.Player):
    pmod = Player.getPModTemplate()
    # Artifact Name
    pmod["Name"] = '''A Greasy, Cracked iPhone 5 Left on the Basketball Court by the Annoying 11 Year Old Kid Who Completely Ruined the Game for Everyone Else'''
    # Artifact Info
    pmod["Type"]["TypeName"] = "Artifact"
    pmod["Type"]["ArchetypeLock"] = "Medic"
    pmod["Type"]["Rarity"] = "Legendary"
    # Description
    pmod["Description"] = '''Feeling unbelievably annoyed at the audacity of the young child, the player changes as follows: Steal, Hustle, Block, Emotion, and Offensive Rebound are set to 99. -20 to all other Primary and Secondary Stats. Make all Hotspots and Freelance Tendencies equal (by their category). Add Pickpocket, Scrapper, Chasedown Artist, Active Hands, and Highlight Film.'''

    # Implementation
    pmod["Modifications"].append({"Operation": "Set", "Key": "SSteal", "Value": 99})
    pmod["Modifications"].append({"Operation": "Set", "Key": "SHustle", "Value": 99})
    pmod["Modifications"].append({"Operation": "Set", "Key": "SBlock", "Value": 99})
    pmod["Modifications"].append({"Operation": "Set", "Key": "SEmotion", "Value": 99})
    pmod["Modifications"].append({"Operation": "Set", "Key": "SOReb", "Value": 99})

    otherAttributes = player["Archetype"].primaryAttributes + player["Archetype"].secondaryAttributes
    otherAttributes.remove("SSteal")
    otherAttributes.remove("SHustle")
    otherAttributes.remove("SBlock")
    otherAttributes.remove("SOReb")

    for otherAttribute in otherAttributes:
        pmod["Modifications"].append({"Operation": "Subtract", "Key": otherAttribute, "Value": 20})

    pmod["Modifications"].append({"Operation": "Set", "Key": "HIso3PLft", "Value": 17})
    pmod["Modifications"].append({"Operation": "Set", "Key": "HIso3PCtr", "Value": 17})
    pmod["Modifications"].append({"Operation": "Set", "Key": "HIso3PRgt", "Value": 16})
    pmod["Modifications"].append({"Operation": "Set", "Key": "HIsoHPLft", "Value": 17})
    pmod["Modifications"].append({"Operation": "Set", "Key": "HIsoHPCtr", "Value": 17})
    pmod["Modifications"].append({"Operation": "Set", "Key": "HIsoHPRgt", "Value": 16})
    pmod["Modifications"].append({"Operation": "Set", "Key": "HP_rLCrnr", "Value": 20})
    pmod["Modifications"].append({"Operation": "Set", "Key": "HP_rLWing", "Value": 20})
    pmod["Modifications"].append({"Operation": "Set", "Key": "HP_rTopOA", "Value": 20})
    pmod["Modifications"].append({"Operation": "Set", "Key": "HP_rRWing", "Value": 20})
    pmod["Modifications"].append({"Operation": "Set", "Key": "HP_rRCrnr", "Value": 20})
    pmod["Modifications"].append({"Operation": "Set", "Key": "HSpt3PLCr", "Value": 10})
    pmod["Modifications"].append({"Operation": "Set", "Key": "HSpt3PLWg", "Value": 10})
    pmod["Modifications"].append({"Operation": "Set", "Key": "HSpt3PTop", "Value": 10})
    pmod["Modifications"].append({"Operation": "Set", "Key": "HSpt3PRWg", "Value": 10})
    pmod["Modifications"].append({"Operation": "Set", "Key": "HSpt3PRCr", "Value": 10})
    pmod["Modifications"].append({"Operation": "Set", "Key": "HSptMdLBl", "Value": 10})
    pmod["Modifications"].append({"Operation": "Set", "Key": "HSptMdLWg", "Value": 10})
    pmod["Modifications"].append({"Operation": "Set", "Key": "HSptMdCtr", "Value": 10})
    pmod["Modifications"].append({"Operation": "Set", "Key": "HSptMdRWg", "Value": 10})
    pmod["Modifications"].append({"Operation": "Set", "Key": "HSptMdRBl", "Value": 10})
    pmod["Modifications"].append({"Operation": "Set", "Key": "HPstRHigh", "Value": 25})
    pmod["Modifications"].append({"Operation": "Set", "Key": "HPstRLow", "Value": 25})
    pmod["Modifications"].append({"Operation": "Set", "Key": "HPstLHigh", "Value": 25})
    pmod["Modifications"].append({"Operation": "Set", "Key": "HPstLLow", "Value": 25})

    pmod["Modifications"].append({"Operation": "Set", "Key": "TTouches", "Value": 50})
    pmod["Modifications"].append({"Operation": "Set", "Key": "TUsePick", "Value": 50})
    pmod["Modifications"].append({"Operation": "Set", "Key": "TSetPick", "Value": 50})
    pmod["Modifications"].append({"Operation": "Set", "Key": "TIsolat", "Value": 50})
    pmod["Modifications"].append({"Operation": "Set", "Key": "TUseOBScr", "Value": 50})
    pmod["Modifications"].append({"Operation": "Set", "Key": "TSetOBScr", "Value": 50})
    pmod["Modifications"].append({"Operation": "Set", "Key": "TPostUp", "Value": 50})
    pmod["Modifications"].append({"Operation": "Set", "Key": "TSpotUp", "Value": 50})
    pmod["Modifications"].append({"Operation": "Set", "Key": "TGiveGo", "Value": 50})

    # Return
    return pmod

#endregion === Medics ===
#region === Guardians ===

def Guardian_Rare_CornpopRazor(player : Player.Player):
    pmod = Player.getPModTemplate()
    # Artifact Name
    pmod["Name"] = '''Cornpop's Razor Blade, stained with the blood of Joe Biden'''
    # Artifact Info
    pmod["Type"]["TypeName"] = "Artifact"
    pmod["Type"]["ArchetypeLock"] = "Guardian"
    pmod["Type"]["Rarity"] = "Rare"
    # Description
    pmod["Description"] = '''The player hates the idea of owning something that was once used to attack a godly man like Joseph Biden, and changes as a result: Add 20 to Offensive Rebound, Subtract 20 from Defensive Rebound.  Add Hustle Points skill.'''

    # Implementation
    pmod["Modifications"].append({"Operation" : "Add", "Key" : "SDReb", "Value" : 20})
    pmod["Modifications"].append({"Operation" : "Subtract", "Key" : "SDReb", "Value" : 20})
    pmod["Modifications"].append({"Operation" : "Set", "Key" : "SigSkill1", "Value" : "Hustle Points"})

    # Return
    return pmod
def Guardian_Rare_BidenDentures(player : Player.Player):
    pmod = Player.getPModTemplate()
    # Artifact Name
    pmod["Name"] = '''Joe Biden's Dentures, stained with the blood of Cornpop.'''
    # Artifact Info
    pmod["Type"]["TypeName"] = "Artifact"
    pmod["Type"]["ArchetypeLock"] = "Guardian"
    pmod["Type"]["Rarity"] = "Rare"
    # Description
    pmod["Description"] = '''Feeling energized at the idea of possessing a battle-tested piece of weaponry, the player changes: Add 20 to Defensive Rebound, Subtract 20 from Offensive Rebound.  Add Scrapper skill.'''

    # Implementation
    pmod["Modifications"].append({"Operation" : "Subtract", "Key" : "SDReb", "Value" : 20})
    pmod["Modifications"].append({"Operation" : "Add", "Key" : "SDReb", "Value" : 20})
    pmod["Modifications"].append({"Operation" : "Set", "Key" : "SigSkill1", "Value" : "Scrapper"})

    # Return
    return pmod
def Guardian_Rare_LearnedRoaches(player : Player.Player):
    pmod = Player.getPModTemplate()
    # Artifact Name
    pmod["Name"] = '''The Roaches Joe Learned A Lot About'''
    # Artifact Info
    pmod["Type"]["TypeName"] = "Artifact"
    pmod["Type"]["ArchetypeLock"] = "Guardian"
    pmod["Type"]["Rarity"] = "Rare"
    # Description
    pmod["Description"] = '''Grinning ear to ear, the player is content; he knows that few others realize the power of having a few roaches over for dinner. Add 5 to all other stats, -10 to 3pt shooting. Add Posterizer.'''

    # Implementation
    for attribute in Archetypes.ALL_ATTRIBUTES:
        if(attribute == "SSht3PT"):
            pmod["Modifications"].append({"Operation" : "Subtract", "Key" : attribute, "Value" : 10})
        else:
            pmod["Modifications"].append({"Operation": "Add", "Key": attribute, "Value": 5})
    pmod["Modifications"].append({"Operation": "Set", "Key": "SigSkill1", "Value": "Posterizer"})

    # Return
    return pmod
def Guardian_Rare_TaughtBiden(player : Player.Player):
    pmod = Player.getPModTemplate()
    # Artifact Name
    pmod["Name"] = '''Joe Biden, the Man the Roaches Taught A Lot To'''
    # Artifact Info
    pmod["Type"]["TypeName"] = "Artifact"
    pmod["Type"]["ArchetypeLock"] = "Guardian"
    pmod["Type"]["Rarity"] = "Rare"
    # Description
    pmod["Description"] = '''C'mon man give him a chance! The player finds no contentment in giving Joe a chance, but does it anyway since the alternative is objectively worse. Add 10 to 3pt shooting, -5 to all other stats. Add Spot-up Shooter skill.'''

    # Implementation
    for attribute in Archetypes.ALL_ATTRIBUTES:
        if(attribute == "SSht3PT"):
            pmod["Modifications"].append({"Operation" : "Add", "Key" : attribute, "Value" : 10})
        else:
            pmod["Modifications"].append({"Operation": "Subtract", "Key": attribute, "Value": 5})
    pmod["Modifications"].append({"Operation": "Set", "Key": "SigSkill1", "Value": "Spot Up Shooter"})

    # Return
    return pmod
def Guardian_Epic_NervousLaughter(player : Player.Player):
    pmod = Player.getPModTemplate()
    # Artifact Name
    pmod["Name"] = '''Nervous Laughter from an Audience in Harlem who Joe Biden just addressed as his '"'Brothas from the Hood\''''
    # Artifact Info
    pmod["Type"]["TypeName"] = "Artifact"
    pmod["Type"]["ArchetypeLock"] = "Guardian"
    pmod["Type"]["Rarity"] = "Epic"
    # Description
    pmod["Description"] = '''Atta boy Joe, way to secure the Blafrican vote! The player adds a rare or epic Engineer special shot:\n\n'''

    # Implementation
    potentialSpecialShots = RARE_SPECIAL_SHOTS["Guardian"] + EPIC_SPECIAL_SHOTS["Guardian"]
    specialShotChoice = random.choice(potentialSpecialShots)
    pmod["Modifications"].append({"Operation": "Set", "Key": "AShtForm", "Value": specialShotChoice["Shot Form"]})
    pmod["Modifications"].append({"Operation": "Set", "Key": "AShtBase", "Value": specialShotChoice["Shot Base"]})
    pmod["Description"] += f"**{specialShotChoice['Name']}** - {specialShotChoice['Description']}"

    # Return
    return pmod
def Guardian_Epic_30330(player : Player.Player):
    pmod = Player.getPModTemplate()
    # Artifact Name
    pmod["Name"] = '''A Confused GPS Device, Desperately Trying to Load the Location of 'JOE 30330\''''
    # Artifact Info
    pmod["Type"]["TypeName"] = "Artifact"
    pmod["Type"]["ArchetypeLock"] = "Guardian"
    pmod["Type"]["Rarity"] = "Epic"
    # Description
    pmod["Description"] = '''The player thought they did everything right -- they agreed with Joe and were on their way to Joe 30330. What went wrong?? The player is anguished and changes as follows: Add Spot Up Shooter and Deadeye. All 3pt Hotzones turn cold. '''

    # Implementation
    pmod["Modifications"].append({"Operation": "Set", "Key": "SigSkill1", "Value": "Spot Up Shooter"})
    pmod["Modifications"].append({"Operation": "Set", "Key": "SigSkill1", "Value": "Deadeye"})

    pmod["Modifications"].append({"Operation": "Set", "Key": "HZ10", "Value": 0})
    pmod["Modifications"].append({"Operation": "Set", "Key": "HZ11", "Value": 0})
    pmod["Modifications"].append({"Operation": "Set", "Key": "HZ12", "Value": 0})
    pmod["Modifications"].append({"Operation": "Set", "Key": "HZ13", "Value": 0})
    pmod["Modifications"].append({"Operation": "Set", "Key": "HZ14", "Value": 0})

    # Return
    return pmod
def Guardian_Epic_PenCoatRack(player : Player.Player):
    pmod = Player.getPModTemplate()
    # Artifact Name
    pmod["Name"] = '''A Pen Joe Biden Mistakenly Gave to a Coat Rack instead of the Small Child to His Left'''
    # Artifact Info
    pmod["Type"]["TypeName"] = "Artifact"
    pmod["Type"]["ArchetypeLock"] = "Guardian"
    pmod["Type"]["Rarity"] = "Epic"
    # Description
    pmod["Description"] = '''It's the thought that counts, even when the thought is half formulated by a deteriorating brain. Vertical is set to 99. Offensive and Defensive Rebound are set to 25. Add Hustle Points.'''

    # Implementation
    pmod["Modifications"].append({"Operation": "Set", "Key": "SVertical", "Value": 99})
    pmod["Modifications"].append({"Operation": "Set", "Key": "SOReb", "Value": 25})
    pmod["Modifications"].append({"Operation": "Set", "Key": "SDReb", "Value": 25})
    pmod["Modifications"].append({"Operation": "Set", "Key": "SigSkill1", "Value": "Hustle Points"})

    # Return
    return pmod
def Guardian_Epic_PonySoldier(player : Player.Player):
    pmod = Player.getPModTemplate()
    # Artifact Name
    pmod["Name"] = '''A Lying Dog-Faced Pony Soldier'''
    # Artifact Info
    pmod["Type"]["TypeName"] = "Artifact"
    pmod["Type"]["ArchetypeLock"] = "Guardian"
    pmod["Type"]["Rarity"] = "Epic"
    # Description
    pmod["Description"] = '''No you didn't. Now sit down fat, before I call Crimea. Add Pickpocket. Steal is set to a number between 80 and 99.  Strength and On-Ball Defense are set to a random number between 25 and 40.'''

    # Implementation
    pmod["Modifications"].append({"Operation": "Set", "Key": "SigSkill1", "Value": "Pick Pocketer"})
    pmod["Modifications"].append({"Operation": "Set", "Key": "SSteal", "Value": random.randrange(80,100)})
    pmod["Modifications"].append({"Operation": "Set", "Key": "SStrength", "Value": random.randrange(25,41)})
    pmod["Modifications"].append({"Operation": "Set", "Key": "SOnBallD", "Value": random.randrange(25,41)})

    # Return
    return pmod
def Guardian_Legendary_JordanLeg(player : Player.Player):
    pmod = Player.getPModTemplate()
    # Artifact Name
    pmod["Name"] = '''Michael Jordan's Amputated Leg'''
    # Artifact Info
    pmod["Type"]["TypeName"] = "Artifact"
    pmod["Type"]["ArchetypeLock"] = "Guardian"
    pmod["Type"]["Rarity"] = "Legendary"
    # Description
    pmod["Description"] = '''Ew what the fuck is that? Before the player can react they are infected by the severed limb and are changed as follows: Set height to 6'6, Set all Signature Skills besides Shot Base to Michael Jordan's.  +30 to Vertical.'''

    # Implementation
    pmod["Modifications"].append({"Operation": "Set", "Key": "HeightIn", "Value": 78})
    pmod["Modifications"].append({"Operation": "Add", "Key": "SVertical", "Value": 30})

    pmod["Modifications"].append({"Operation": "Set", "Key": "AShtForm", "Value": 115})
    pmod["Modifications"].append({"Operation": "Set", "Key": "AFadeaway", "Value": 1})
    pmod["Modifications"].append({"Operation": "Set", "Key": "AContestd", "Value": 0})
    pmod["Modifications"].append({"Operation": "Set", "Key": "AEscDrPlU", "Value": 1})
    pmod["Modifications"].append({"Operation": "Set", "Key": "ARunner", "Value": 16})
    pmod["Modifications"].append({"Operation": "Set", "Key": "AFreeT", "Value": 73})
    pmod["Modifications"].append({"Operation": "Set", "Key": "ADrPullUp", "Value": 4})
    pmod["Modifications"].append({"Operation": "Set", "Key": "ASpinJmpr", "Value": 6})
    pmod["Modifications"].append({"Operation": "Set", "Key": "AHopJmpr", "Value": 2})
    pmod["Modifications"].append({"Operation": "Set", "Key": "APstFade", "Value": 11})
    pmod["Modifications"].append({"Operation": "Set", "Key": "APstHook", "Value": 0})
    pmod["Modifications"].append({"Operation": "Set", "Key": "APstHopSh", "Value": 7})
    pmod["Modifications"].append({"Operation": "Set", "Key": "APstShmSh", "Value": 0})
    pmod["Modifications"].append({"Operation": "Set", "Key": "APstDrvStB", "Value": 3})
    pmod["Modifications"].append({"Operation": "Set", "Key": "APstPrtct", "Value": 0})
    pmod["Modifications"].append({"Operation": "Set", "Key": "APstSpnStB", "Value": 0})
    pmod["Modifications"].append({"Operation": "Set", "Key": "APstPrtSpn", "Value": 0})
    pmod["Modifications"].append({"Operation": "Set", "Key": "AIsoCross", "Value": 5})
    pmod["Modifications"].append({"Operation": "Set", "Key": "AIsoBhBck", "Value": 6})
    pmod["Modifications"].append({"Operation": "Set", "Key": "AIsoSpin", "Value": 4})
    pmod["Modifications"].append({"Operation": "Set", "Key": "AIsoHesit", "Value": 1})
    pmod["Modifications"].append({"Operation": "Set", "Key": "ALayUp", "Value": 7})
    pmod["Modifications"].append({"Operation": "Set", "Key": "AGoToDunk", "Value": 14})
    pmod["Modifications"].append({"Operation": "Set", "Key": "ADunk2", "Value": 13})
    pmod["Modifications"].append({"Operation": "Set", "Key": "ADunk3", "Value": 7})
    pmod["Modifications"].append({"Operation": "Set", "Key": "ADunk4", "Value": 28})
    pmod["Modifications"].append({"Operation": "Set", "Key": "ADunk5", "Value": 60})
    pmod["Modifications"].append({"Operation": "Set", "Key": "ADunk6", "Value": 32})
    pmod["Modifications"].append({"Operation": "Set", "Key": "ADunk7", "Value": 45})
    pmod["Modifications"].append({"Operation": "Set", "Key": "ADunk8", "Value": 34})
    pmod["Modifications"].append({"Operation": "Set", "Key": "ADunk9", "Value": 41})
    pmod["Modifications"].append({"Operation": "Set", "Key": "ADunk10", "Value": 27})
    pmod["Modifications"].append({"Operation": "Set", "Key": "ADunk11", "Value": 2})
    pmod["Modifications"].append({"Operation": "Set", "Key": "ADunk12", "Value": 46})
    pmod["Modifications"].append({"Operation": "Set", "Key": "ADunk13", "Value": 0})
    pmod["Modifications"].append({"Operation": "Set", "Key": "ADunk14", "Value": 0})
    pmod["Modifications"].append({"Operation": "Set", "Key": "ADunk15", "Value": 0})

    # Return
    return pmod
def Guardian_Legendary_FitzgeraldElixir(player : Player.Player):
    pmod = Player.getPModTemplate()
    # Artifact Name
    pmod["Name"] = '''The Mysterious Elixir Last Drunken by Fitzgerald Kambavolo'''
    # Artifact Info
    pmod["Type"]["TypeName"] = "Artifact"
    pmod["Type"]["ArchetypeLock"] = "Guardian"
    pmod["Type"]["Rarity"] = "Legendary"
    # Description
    pmod["Description"] = '''The Guardian takes, randomly, 1-5 swigs of the mysterious elixir. For each swig taken, reduce all stats by 5, and increase height by 3 inches. Add Brick Wall.\n\n'''

    # Implementation
    swigs = random.randrange(1,6)
    for attribute in Archetypes.ALL_ATTRIBUTES:
        pmod["Modifications"].append({"Operation": "Subtract", "Key": attribute, "Value": swigs * 5})
    pmod["Modifications"].append({"Operation": "Add", "Key": "HeightIn", "Value": swigs * 3})
    pmod["Modifications"].append({"Operation": "Set", "Key": "SigSkill1", "Value": "Brick Wall"})

    pmod["Description"] += f"This player took {swigs} swig"
    if(swigs > 1):
        pmod["Description"] += f"s."
    else:
        pmod["Description"] += f"."

    # Return
    return pmod
def Guardian_Legendary_IcyTouch(player : Player.Player):
    pmod = Player.getPModTemplate()
    # Artifact Name
    pmod["Name"] = '''The Icy Touch of the Night King'''
    # Artifact Info
    pmod["Type"]["TypeName"] = "Artifact"
    pmod["Type"]["ArchetypeLock"] = "Guardian"
    pmod["Type"]["Rarity"] = "Legendary"
    # Description
    pmod["Description"] = '''The player vibrates with an ancient power, morphing into a White Walker and changing as follows: All zones are Cold Zones. Reroll all Secondary and Tertiary Stats to be values between 40 and 60. Add Post Proficiency, Post Play Maker, Deadeye, and Finisher. Gain an epic or legendary shot:\n\n'''

    # Implementation
    pmod["Modifications"].append({"Operation": "Set", "Key": "HZ1", "Value": 0})
    pmod["Modifications"].append({"Operation": "Set", "Key": "HZ2", "Value": 0})
    pmod["Modifications"].append({"Operation": "Set", "Key": "HZ3", "Value": 0})
    pmod["Modifications"].append({"Operation": "Set", "Key": "HZ4", "Value": 0})
    pmod["Modifications"].append({"Operation": "Set", "Key": "HZ5", "Value": 0})
    pmod["Modifications"].append({"Operation": "Set", "Key": "HZ6", "Value": 0})
    pmod["Modifications"].append({"Operation": "Set", "Key": "HZ7", "Value": 0})
    pmod["Modifications"].append({"Operation": "Set", "Key": "HZ8", "Value": 0})
    pmod["Modifications"].append({"Operation": "Set", "Key": "HZ9", "Value": 0})
    pmod["Modifications"].append({"Operation": "Set", "Key": "HZ10", "Value": 0})
    pmod["Modifications"].append({"Operation": "Set", "Key": "HZ11", "Value": 0})
    pmod["Modifications"].append({"Operation": "Set", "Key": "HZ12", "Value": 0})
    pmod["Modifications"].append({"Operation": "Set", "Key": "HZ13", "Value": 0})
    pmod["Modifications"].append({"Operation": "Set", "Key": "HZ14", "Value": 0})

    for secondaryAttribute in player["Archetype"].secondaryAttributes:
        pmod["Modifications"].append({"Operation": "Set", "Key": secondaryAttribute, "Value": random.randrange(40,61)})
    for tertiaryAttribute in player["Archetype"].tertiaryAttributes:
        pmod["Modifications"].append({"Operation": "Set", "Key": tertiaryAttribute, "Value": random.randrange(40,61)})

    pmod["Modifications"].append({"Operation": "Set", "Key": "SigSkill1", "Value": "Post Proficiency"})
    pmod["Modifications"].append({"Operation": "Set", "Key": "SigSkill1", "Value": "Post Playmaker"})
    pmod["Modifications"].append({"Operation": "Set", "Key": "SigSkill1", "Value": "Deadeye"})
    pmod["Modifications"].append({"Operation": "Set", "Key": "SigSkill1", "Value": "Finisher"})


    potentialSpecialShots = LEGENDARY_SPECIAL_SHOTS["Guardian"] + EPIC_SPECIAL_SHOTS["Guardian"]
    specialShotChoice = random.choice(potentialSpecialShots)
    pmod["Modifications"].append({"Operation": "Set", "Key": "AShtForm", "Value": specialShotChoice["Shot Form"]})
    pmod["Modifications"].append({"Operation": "Set", "Key": "AShtBase", "Value": specialShotChoice["Shot Base"]})
    pmod["Description"] += f"**{specialShotChoice['Name']}** - {specialShotChoice['Description']}"

    # Return
    return pmod

#endregion === Guardians ===
#region === Engineers ===

def Engineer_Rare_ShirtBearArms(player : Player.Player):
    pmod = Player.getPModTemplate()
    # Artifact Name
    pmod["Name"] = '''A T-Shirt from Scott Brown reading: '2nd to Shoot, 1st to Kill! #RightToBearArms\''''
    # Artifact Info
    pmod["Type"]["TypeName"] = "Artifact"
    pmod["Type"]["ArchetypeLock"] = "Engineer"
    pmod["Type"]["Rarity"] = "Rare"
    # Description
    pmod["Description"] = '''Knowing that hoodlums are terrible shots, and that the player themself is a shooter akin John Wayne, the player lets out a roaring set of laughs. Add 20 to Defensive Rebound, Subtract 20 from Offensive Rebound.  Add Scrapper skill.'''

    # Implementation
    pmod["Modifications"].append({"Operation" : "Add", "Key" : "SDReb", "Value" : 20})
    pmod["Modifications"].append({"Operation" : "Subtract", "Key" : "SOReb", "Value" : 20})
    pmod["Modifications"].append({"Operation" : "Set", "Key" : "SigSkill1", "Value" : "Scrapper"})

    # Return
    return pmod
def Engineer_Rare_ShirtArmedBacon(player : Player.Player):
    pmod = Player.getPModTemplate()
    # Artifact Name
    pmod["Name"] = '''A T-Shirt from Scott Brown reading: 'Be warned, I'm legally armed with weaponry....and BACON!\''''
    # Artifact Info
    pmod["Type"]["TypeName"] = "Artifact"
    pmod["Type"]["ArchetypeLock"] = "Engineer"
    pmod["Type"]["Rarity"] = "Rare"
    # Description
    pmod["Description"] = '''Nodding their head up and down, failing to hold back a good laugh, the player holsters their glock and prepares to make some bacon. Add 20 to Offensive Rebound, Subtract 20 from Defensive Rebound.  Add Hustle Points skill.'''

    # Implementation
    pmod["Modifications"].append({"Operation" : "Subtract", "Key" : "SDReb", "Value" : 20})
    pmod["Modifications"].append({"Operation" : "Add", "Key" : "SOReb", "Value" : 20})
    pmod["Modifications"].append({"Operation" : "Set", "Key" : "SigSkill1", "Value" : "Hustle Points"})

    # Return
    return pmod
def Engineer_Rare_ShirtStupidMask(player : Player.Player):
    pmod = Player.getPModTemplate()
    # Artifact Name
    pmod["Name"] = '''A T-Shirt from Scott Brown reading: 'Keep your mask on, it stops all the STUPID from spilling out!\''''
    # Artifact Info
    pmod["Type"]["TypeName"] = "Artifact"
    pmod["Type"]["ArchetypeLock"] = "Engineer"
    pmod["Type"]["Rarity"] = "Rare"
    # Description
    pmod["Description"] = '''After letting out a hearty chuckle, knowing full and well that the mask mandate is a deep state PSYOP, the player changes: Add 10 Speed, -15 Quickness. Add Chasedown Artist.'''

    # Implementation
    pmod["Modifications"].append({"Operation" : "Add", "Key" : "SSpeed", "Value" : 10})
    pmod["Modifications"].append({"Operation" : "Subtract", "Key" : "SQuick", "Value" : 15})
    pmod["Modifications"].append({"Operation" : "Set", "Key" : "SigSkill1", "Value" : "Chase Down Artist"})

    # Return
    return pmod
def Engineer_Rare_ShirtAllergy(player : Player.Player):
    pmod = Player.getPModTemplate()
    # Artifact Name
    pmod["Name"] = '''A T-Shirt from Scott Brown reading: 'Stay back,  I am deathly allergic to STUPID!\''''
    # Artifact Info
    pmod["Type"]["TypeName"] = "Artifact"
    pmod["Type"]["ArchetypeLock"] = "Engineer"
    pmod["Type"]["Rarity"] = "Rare"
    # Description
    pmod["Description"] = '''Scott's humor knows no bounds, the player revels in sharing an occupation with the next George Carlin. Add 15 Quickness, -10 Speed. Add Post Playmaker.'''

    # Implementation
    pmod["Modifications"].append({"Operation" : "Subtract", "Key" : "SSpeed", "Value" : 10})
    pmod["Modifications"].append({"Operation" : "Add", "Key" : "SQuick", "Value" : 15})
    pmod["Modifications"].append({"Operation" : "Set", "Key" : "SigSkill1", "Value" : "Post Playmaker"})

    # Return
    return pmod
def Engineer_Epic_ShirtBachelors(player : Player.Player):
    pmod = Player.getPModTemplate()
    # Artifact Name
    pmod["Name"] = '''A T-Shirt from Scott Brown reading: 'I wipe my ASS with your bachelor of arts degree!\''''
    # Artifact Info
    pmod["Type"]["TypeName"] = "Artifact"
    pmod["Type"]["ArchetypeLock"] = "Engineer"
    pmod["Type"]["Rarity"] = "Epic"
    # Description
    pmod["Description"] = '''Feeling thankful that they got an engineering degree, the player adds a rare or epic Engineer special shot:\n\n'''

    # Implementation
    potentialSpecialShots = RARE_SPECIAL_SHOTS["Engineer"] + EPIC_SPECIAL_SHOTS["Engineer"]
    specialShotChoice = random.choice(potentialSpecialShots)
    pmod["Modifications"].append({"Operation": "Set", "Key": "AShtForm", "Value": specialShotChoice["Shot Form"]})
    pmod["Modifications"].append({"Operation": "Set", "Key": "AShtBase", "Value": specialShotChoice["Shot Base"]})
    pmod["Description"] += f"**{specialShotChoice['Name']}** - {specialShotChoice['Description']}"

    # Return
    return pmod
def Engineer_Epic_ShirtSarcastic(player : Player.Player):
    pmod = Player.getPModTemplate()
    # Artifact Name
    pmod["Name"] = '''A T-Shirt from Scott Brown reading: 'If you don't want a sarcastic answer, don't ask a STUPID question!\''''
    # Artifact Info
    pmod["Type"]["TypeName"] = "Artifact"
    pmod["Type"]["ArchetypeLock"] = "Engineer"
    pmod["Type"]["Rarity"] = "Epic"
    # Description
    pmod["Description"] = '''So damn true. The player smiles knowingly and changes as follows: Add 20 to Speed and Quickness. Add 15 to accented secondary stats.  Strength and Low Post Defense are set to 25. -6 inches to Height.'''

    # Implementation
    pmod["Modifications"].append({"Operation": "Add", "Key": "SSpeed", "Value": 20})
    pmod["Modifications"].append({"Operation": "Add", "Key": "SQuick", "Value": 20})
    for accentedAttribute in player["Archetype"].accentedAttributes:
        if(accentedAttribute in player["Archetype"].secondaryAttributes):
            pmod["Modifications"].append({"Operation": "Add", "Key": accentedAttribute, "Value": 15})
    pmod["Modifications"].append({"Operation": "Set", "Key": "SStrength", "Value": 25})
    pmod["Modifications"].append({"Operation": "Set", "Key": "SDLowPost", "Value": 25})
    pmod["Modifications"].append({"Operation": "Subtract", "Key": "HeightIn", "Value": 6})


    # Return
    return pmod
def Engineer_Epic_ShirtSpeakMoron(player : Player.Player):
    pmod = Player.getPModTemplate()
    # Artifact Name
    pmod["Name"] = '''A T-Shirt from Scott Brown reading: 'I don't speak MORON, we'll have to communicate in sign language!' Below is an image of a white man giving the middle finger.'''
    # Artifact Info
    pmod["Type"]["TypeName"] = "Artifact"
    pmod["Type"]["ArchetypeLock"] = "Engineer"
    pmod["Type"]["Rarity"] = "Epic"
    # Description
    pmod["Description"] = '''After uncontrollably laughing on the floor, nearly dying from asphyxiation, the player changes as follows: Set Vertical and Dunk to 99. Add 2 Dunk Packages from cool dunk types. Set all tertiary stats to 25. Add Posterizer, Finisher, and Highlight Film.'''

    # Implementation
    pmod["Modifications"].append({"Operation": "Set", "Key": "SVertical", "Value": 99})
    pmod["Modifications"].append({"Operation": "Set", "Key": "SDunk", "Value": 99})
    for tertiaryAttribute in player["Archetype"].tertiaryAttributes:
        pmod["Modifications"].append({"Operation": "Set", "Key": tertiaryAttribute, "Value": 25})
    pmod["Modifications"].append({"Operation": "Set", "Key": "SigSkill1", "Value": "Posterizer"})
    pmod["Modifications"].append({"Operation": "Set", "Key": "SigSkill2", "Value": "Finisher"})
    pmod["Modifications"].append({"Operation": "Set", "Key": "SigSkill3", "Value": "Highlight Film"})

    coolDunks = [23,24,25,26,27,28,35,51,55,63,64,65]
    dunk1 = random.choice(coolDunks)
    coolDunks.remove(dunk1)
    dunk2 = random.choice(coolDunks)

    pmod["Modifications"].append({"Operation": "Set", "Key": "AGoToDunk", "Value": dunk1})
    pmod["Modifications"].append({"Operation": "Set", "Key": "ADunk2", "Value": dunk2})



    # Return
    return pmod
def Engineer_Epic_ShirtTechSupport(player : Player.Player):
    pmod = Player.getPModTemplate()
    # Artifact Name
    pmod["Name"] = '''A T-Shirt from Scott Brown reading: 'Nothing you can do will scare me - I work in TECH SUPPORT!\''''
    # Artifact Info
    pmod["Type"]["TypeName"] = "Artifact"
    pmod["Type"]["ArchetypeLock"] = "Engineer"
    pmod["Type"]["Rarity"] = "Epic"
    # Description
    pmod["Description"] = '''Feeling relieved to work a job that builds so much character, the player evolves: Add 6 inches to height, subtract 30 from speed, quickness, and vertical. Add 20 to non-accented secondary stats. Add Eraser and Brick Wall.'''

    # Implementation
    pmod["Modifications"].append({"Operation": "Add", "Key": "HeightIn", "Value": 6})

    pmod["Modifications"].append({"Operation": "Subtract", "Key": "SSpeed", "Value": 30})
    pmod["Modifications"].append({"Operation": "Subtract", "Key": "SQuick", "Value": 30})
    pmod["Modifications"].append({"Operation": "Subtract", "Key": "SVertical", "Value": 30})

    for unaccentedAttribute in player["Archetype"].unaccentedAttributes:
        if(unaccentedAttribute in player["Archetype"].secondaryAttributes):
            pmod["Modifications"].append({"Operation": "Add", "Key": unaccentedAttribute, "Value": 20})

    pmod["Modifications"].append({"Operation": "Set", "Key": "SigSkill1", "Value": "Eraser"})
    pmod["Modifications"].append({"Operation": "Set", "Key": "SigSkill2", "Value": "Brick Wall"})




    # Return
    return pmod
def Engineer_Legendary_SecuritySerum(player : Player.Player):
    pmod = Player.getPModTemplate()
    # Artifact Name
    pmod["Name"] = '''Security Serum, courtesy of Amalgamo Inc.'''
    # Artifact Info
    pmod["Type"]["TypeName"] = "Artifact"
    pmod["Type"]["ArchetypeLock"] = "Engineer"
    pmod["Type"]["Rarity"] = "Legendary"
    # Description
    pmod["Description"] = '''Take 1-5 swigs of the Security Serum. For each swig taken, -10 Speed and Quickness, -5 Offensive Rebound, +5 Defensive Rebound, and +10 to Low Post Defense and On-Ball Defense.  Add Lockdown Defender and Eraser.\n\n'''

    # Implementation
    swigs = random.randrange(1,6)

    pmod["Modifications"].append({"Operation": "Subtract", "Key": "SSpeed", "Value": swigs * 10})
    pmod["Modifications"].append({"Operation": "Subtract", "Key": "SQuick", "Value": swigs * 10})
    pmod["Modifications"].append({"Operation": "Subtract", "Key": "SOReb", "Value": swigs * 5})
    pmod["Modifications"].append({"Operation": "Add", "Key": "SDReb", "Value": swigs * 5})
    pmod["Modifications"].append({"Operation": "Add", "Key": "SDLowPost", "Value": swigs * 10})
    pmod["Modifications"].append({"Operation": "Add", "Key": "SOnBallD", "Value": swigs * 10})

    pmod["Modifications"].append({"Operation": "Set", "Key": "SigSkill1", "Value": "Lockdown Defender"})
    pmod["Modifications"].append({"Operation": "Set", "Key": "SigSkill1", "Value": "Eraser"})

    pmod["Description"] += f"This player took {swigs} swig"
    if(swigs > 1):
        pmod["Description"] += "s."
    else:
        pmod["Description"] += "."

    # Return
    return pmod
def Engineer_Legendary_LaatzPass(player : Player.Player):
    pmod = Player.getPModTemplate()
    # Artifact Name
    pmod["Name"] = '''Backstage Pass, VIP Tickets to see Michael Laatz in Concert, Won from Laatz' 'ROAD TO SIX YOUTUBE SUBSCRIBERS SWEEPSTAKES\''''
    # Artifact Info
    pmod["Type"]["TypeName"] = "Artifact"
    pmod["Type"]["ArchetypeLock"] = "Engineer"
    pmod["Type"]["Rarity"] = "Legendary"
    # Description
    pmod["Description"] = '''Astonished to own this once in a lifetime opportunity to see the most influential artist in Spritopian history, the player evolves: -25 to Speed, Offensive Rebound, Defensive Rebound, and Pass. Quickness and Dunk are set to 99, and Dunk Tendency is set to 99. +50 to Low Post Offense. Add Ankle Breaker, Finisher, Highlight Film, and Post Proficiency. Add 4 Dunk Packages from cool dunk types.'''

    # Implementation
    pmod["Modifications"].append({"Operation": "Subtract", "Key": "SSpeed", "Value": 25})
    pmod["Modifications"].append({"Operation": "Subtract", "Key": "SOReb", "Value": 25})
    pmod["Modifications"].append({"Operation": "Subtract", "Key": "SDReb", "Value": 25})
    pmod["Modifications"].append({"Operation": "Subtract", "Key": "SPass", "Value": 25})

    pmod["Modifications"].append({"Operation": "Set", "Key": "SQuick", "Value": 99})
    pmod["Modifications"].append({"Operation": "Set", "Key": "SDunk", "Value": 99})
    pmod["Modifications"].append({"Operation": "Set", "Key": "TDunkvLU", "Value": 99})

    pmod["Modifications"].append({"Operation": "Add", "Key": "SOLowPost", "Value": 50})

    pmod["Modifications"].append({"Operation": "Set", "Key": "SigSkill1", "Value": "Ankle Breaker"})
    pmod["Modifications"].append({"Operation": "Set", "Key": "SigSkill1", "Value": "Finisher"})
    pmod["Modifications"].append({"Operation": "Set", "Key": "SigSkill1", "Value": "Highlight Film"})
    pmod["Modifications"].append({"Operation": "Set", "Key": "SigSkill1", "Value": "Post Proficiency"})

    coolDunks = [23,24,25,26,27,28,35,51,55,63,64,65]

    dunk1 = random.choice(coolDunks)
    coolDunks.remove(dunk1)
    dunk2 = random.choice(coolDunks)
    coolDunks.remove(dunk2)
    dunk3 = random.choice(coolDunks)
    coolDunks.remove(dunk3)
    dunk4 = random.choice(coolDunks)

    pmod["Modifications"].append({"Operation": "Set", "Key": "AGoToDunk", "Value": dunk1})
    pmod["Modifications"].append({"Operation": "Set", "Key": "ADunk2", "Value": dunk2})
    pmod["Modifications"].append({"Operation": "Set", "Key": "ADunk3", "Value": dunk3})
    pmod["Modifications"].append({"Operation": "Set", "Key": "ADunk4", "Value": dunk4})


    # Return
    return pmod
def Engineer_Legendary_LavaFloor(player : Player.Player):
    pmod = Player.getPModTemplate()
    # Artifact Name
    pmod["Name"] = '''The Bewildered and Horrified Look on Sneh's Face After Tim Molkosky Cautioned Him that the 'Floor is Lava\''''
    # Artifact Info
    pmod["Type"]["TypeName"] = "Artifact"
    pmod["Type"]["ArchetypeLock"] = "Engineer"
    pmod["Type"]["Rarity"] = "Legendary"
    # Description
    pmod["Description"] = '''Uncomfortable by Sneh's everyone-for-themself approach of locking himself in the freezer, the player changes as follows: All zones are hot zones. Add 20 to all tertiary stats. Randomly subtract 150 from all primary and secondary stats. Add an Epic or Legendary special shot.\n\n'''

    # Implementation
    pmod["Modifications"].append({"Operation": "Set", "Key": "HZ1", "Value": 2})
    pmod["Modifications"].append({"Operation": "Set", "Key": "HZ2", "Value": 2})
    pmod["Modifications"].append({"Operation": "Set", "Key": "HZ3", "Value": 2})
    pmod["Modifications"].append({"Operation": "Set", "Key": "HZ4", "Value": 2})
    pmod["Modifications"].append({"Operation": "Set", "Key": "HZ5", "Value": 2})
    pmod["Modifications"].append({"Operation": "Set", "Key": "HZ6", "Value": 2})
    pmod["Modifications"].append({"Operation": "Set", "Key": "HZ7", "Value": 2})
    pmod["Modifications"].append({"Operation": "Set", "Key": "HZ8", "Value": 2})
    pmod["Modifications"].append({"Operation": "Set", "Key": "HZ9", "Value": 2})
    pmod["Modifications"].append({"Operation": "Set", "Key": "HZ10", "Value": 2})
    pmod["Modifications"].append({"Operation": "Set", "Key": "HZ11", "Value": 2})
    pmod["Modifications"].append({"Operation": "Set", "Key": "HZ12", "Value": 2})
    pmod["Modifications"].append({"Operation": "Set", "Key": "HZ13", "Value": 2})
    pmod["Modifications"].append({"Operation": "Set", "Key": "HZ14", "Value": 2})

    for tertiaryAttribute in player["Archetype"].tertiaryAttributes:
        pmod["Modifications"].append({"Operation": "Add", "Key": tertiaryAttribute, "Value": 20})

    primarySecondaryAttributes = player["Archetype"].primaryAttributes + player["Archetype"].secondaryAttributes
    pointsToSpend = 150
    attributeValues = {}
    while pointsToSpend > 0:
        randomAttribute = random.choice(primarySecondaryAttributes)
        attributeValues[randomAttribute] = attributeValues.get(randomAttribute,0) + 1
        pointsToSpend -= 1
    for attribute,value in attributeValues.items():
        pmod["Modifications"].append({"Operation": "Subtract", "Key": attribute, "Value": value})

    potentialSpecialShots = LEGENDARY_SPECIAL_SHOTS["Engineer"] + EPIC_SPECIAL_SHOTS["Engineer"]
    specialShotChoice = random.choice(potentialSpecialShots)
    pmod["Modifications"].append({"Operation": "Set", "Key": "AShtForm", "Value": specialShotChoice["Shot Form"]})
    pmod["Modifications"].append({"Operation": "Set", "Key": "AShtBase", "Value": specialShotChoice["Shot Base"]})
    pmod["Description"] += f"**{specialShotChoice['Name']}** - {specialShotChoice['Description']}"


    # Return
    return pmod

#endregion === Engineers ===
#region === Directors ===

def Director_Rare_BagOfRocks(player : Player.Player):
    pmod = Player.getPModTemplate()
    # Artifact Name
    pmod["Name"] = '''A Bag of "Rocks" Recovered from a DEA Agent's Remains'''
    # Artifact Info
    pmod["Type"]["TypeName"] = "Artifact"
    pmod["Type"]["ArchetypeLock"] = "Director"
    pmod["Type"]["Rarity"] = "Rare"
    # Description
    pmod["Description"] = '''Blissfully unaware of the difference between rocks and minerals, the player decides these will be perfect for skipping across a good lake. Adds Highlight Film and Dimer. +10 Pass. -10 Hands.'''

    # Implementation
    pmod["Modifications"].append({"Operation" : "Set", "Key" : "SigSkill1", "Value" : "Highlight Film"})
    pmod["Modifications"].append({"Operation" : "Set", "Key" : "SigSkill2", "Value" : "Dimer"})
    pmod["Modifications"].append({"Operation" : "Add", "Key" : "SPass", "Value" : 10})
    pmod["Modifications"].append({"Operation" : "Subtract", "Key" : "SHands", "Value" : 10})

    # Return
    return pmod
def Director_Rare_BagOfMeth(player : Player.Player):
    pmod = Player.getPModTemplate()
    # Artifact Name
    pmod["Name"] = '''A Bag of "Meth" Recovered from a Massive Explosion in the City'''
    # Artifact Info
    pmod["Type"]["TypeName"] = "Artifact"
    pmod["Type"]["ArchetypeLock"] = "Director"
    pmod["Type"]["Rarity"] = "Rare"
    # Description
    pmod["Description"] = '''Knowing that they shouldn't waste good meth, the player snorts the explosive powder and changes: Adds Heat Retention and Shot Creator. +10 Shoot Off Dribble, -10 Shoot In Traffic.'''

    # Implementation
    pmod["Modifications"].append({"Operation" : "Set", "Key" : "SigSkill1", "Value" : "Heat Retention"})
    pmod["Modifications"].append({"Operation" : "Set", "Key" : "SigSkill2", "Value" : "Shot Creator"})
    pmod["Modifications"].append({"Operation" : "Add", "Key" : "SShtOfD", "Value" : 10})
    pmod["Modifications"].append({"Operation" : "Subtract", "Key" : "SShtInT", "Value" : 10})

    # Return
    return pmod
def Director_Rare_HamlinBoxing(player : Player.Player):
    pmod = Player.getPModTemplate()
    # Artifact Name
    pmod["Name"] = '''Howard Hamlin's Pristine Boxing Gear'''
    # Artifact Info
    pmod["Type"]["TypeName"] = "Artifact"
    pmod["Type"]["ArchetypeLock"] = "Director"
    pmod["Type"]["Rarity"] = "Rare"
    # Description
    pmod["Description"] = '''Appreciating the delicate care taken to the dueling gear, the player finds a state of zen and changes as follows: Add 2 inches of height. -10 speed and quickness. Add Defensive Anchor.'''

    # Implementation
    pmod["Modifications"].append({"Operation" : "Subtract", "Key" : "SSpeed", "Value" : 10})
    pmod["Modifications"].append({"Operation" : "Subtract", "Key" : "SQuick", "Value" : 10})
    pmod["Modifications"].append({"Operation" : "Set", "Key" : "SigSkill1", "Value" : "Defensive Anchor"})
    pmod["Modifications"].append({"Operation" : "Add", "Key" : "HeightIn", "Value" : 2})

    # Return
    return pmod
def Director_Rare_JimmyBoxing(player : Player.Player):
    pmod = Player.getPModTemplate()
    # Artifact Name
    pmod["Name"] = '''Jimmy McGill's Wartorn Boxing Gear'''
    # Artifact Info
    pmod["Type"]["TypeName"] = "Artifact"
    pmod["Type"]["ArchetypeLock"] = "Director"
    pmod["Type"]["Rarity"] = "Rare"
    # Description
    pmod["Description"] = '''Feeling perplexed on the very existence of this artifact, the player ponders on this thought and loses 2 inches of height. +10 speed and quickness. Add Chasedown artist.'''

    # Implementation
    pmod["Modifications"].append({"Operation" : "Subtract", "Key" : "HeightIn", "Value" : 2})
    pmod["Modifications"].append({"Operation" : "Add", "Key" : "SSpeed", "Value" : 10})
    pmod["Modifications"].append({"Operation" : "Add", "Key" : "SQuick", "Value" : 10})
    pmod["Modifications"].append({"Operation" : "Set", "Key" : "SigSkill1", "Value" : "Chase Down Artist"})

    # Return
    return pmod
def Director_Epic_Pimento(player : Player.Player):
    pmod = Player.getPModTemplate()
    # Artifact Name
    pmod["Name"] = '''Some Geezer Eating a Pimento Sandwich'''
    # Artifact Info
    pmod["Type"]["TypeName"] = "Artifact"
    pmod["Type"]["ArchetypeLock"] = "Director"
    pmod["Type"]["Rarity"] = "Epic"
    # Description
    pmod["Description"] = '''Having had a good long look at the geezer, the player is rejuvenated and adds a rare or epic Director Special Shot:\n\n'''

    # Implementation
    potentialSpecialShots = RARE_SPECIAL_SHOTS["Director"] + EPIC_SPECIAL_SHOTS["Director"]
    specialShotChoice = random.choice(potentialSpecialShots)
    pmod["Modifications"].append({"Operation" : "Set", "Key" : "AShtForm", "Value" : specialShotChoice["Shot Form"]})
    pmod["Modifications"].append({"Operation" : "Set", "Key" : "AShtBase", "Value" : specialShotChoice["Shot Base"]})
    pmod["Description"] += f"**{specialShotChoice['Name']}** - {specialShotChoice['Description']}"

    # Return
    return pmod
def Director_Epic_VinceHumility(player : Player.Player):
    pmod = Player.getPModTemplate()
    # Artifact Name
    pmod["Name"] = '''Vial of Vince Gilligan's Humility, Liquefied'''
    # Artifact Info
    pmod["Type"]["TypeName"] = "Artifact"
    pmod["Type"]["ArchetypeLock"] = "Director"
    pmod["Type"]["Rarity"] = "Epic"
    # Description
    pmod["Description"] = '''Feeling like they can morph the world in any way they want, but also like they don't want any of the credit for it, the player changes as follows: Add Defensive Anchor and War General. Set Hustle, Pass, Offensive Awareness, and Defensive Awareness to 99. -15 to all other Primary attributes.'''

    # Implementation
    attributesToIncrease = ["SHustle","SPass","SDAwar","SOAwar"]
    for primaryAttribute in player["Archetype"].primaryAttributes:
        if(primaryAttribute in attributesToIncrease):
            pmod["Modifications"].append({"Operation" : "Set", "Key" : primaryAttribute, "Value" : 99})
        else:
            pmod["Modifications"].append({"Operation": "Subtract", "Key": primaryAttribute, "Value": 15})
    pmod["Modifications"].append({"Operation" : "Set", "Key" : "SigSkill1", "Value" : "Defensive Anchor"})
    pmod["Modifications"].append({"Operation" : "Set", "Key" : "SigSkill2", "Value" : "Floor General"})

    # Return
    return pmod
def Director_Epic_SnappedCellphone(player : Player.Player):
    pmod = Player.getPModTemplate()
    # Artifact Name
    pmod["Name"] = '''A Cellphone Snapped Perfectly in Two'''
    # Artifact Info
    pmod["Type"]["TypeName"] = "Artifact"
    pmod["Type"]["ArchetypeLock"] = "Director"
    pmod["Type"]["Rarity"] = "Epic"
    # Description
    pmod["Description"] = '''Feeling pleased at the sight of a southern man grinning with glee at the broken piece of technology, the player evolves as follows: Add 10 to all non-accented stats. Subtract 150 points randomly across all accented stats.'''

    # Implementation
    for unaccentedAttribute in player["Archetype"].unaccentedAttributes:
        pmod["Modifications"].append({"Operation": "Add", "Key": unaccentedAttribute, "Value": 10})

    pointToDistribute = 150
    attributeAdjustments = {}
    while pointToDistribute > 0:
        randomAttributeToDistributeTo = random.choice(player["Archetype"].accentedAttributes)
        attributeAdjustments[randomAttributeToDistributeTo] = attributeAdjustments.get(randomAttributeToDistributeTo,0) + 1
        pointToDistribute -= 1
    for attributeToAdjust,adjustment in attributeAdjustments.items():
        pmod["Modifications"].append({"Operation": "Subtract", "Key": attributeToAdjust, "Value": adjustment})

    # Return
    return pmod
def Director_Epic_BloodCandle(player : Player.Player):
    pmod = Player.getPModTemplate()
    # Artifact Name
    pmod["Name"] = '''A Burnt Out Candle, Stained with a Single Drop of Blood'''
    # Artifact Info
    pmod["Type"]["TypeName"] = "Artifact"
    pmod["Type"]["ArchetypeLock"] = "Director"
    pmod["Type"]["Rarity"] = "Epic"
    # Description
    pmod["Description"] = '''Holy fuck. The player didn't expect such a deeply unnerving artifact and changes as follows: Set Offensive and Defensive awareness to 99.  Add Shot Creator, Brick Wall,  Antifreeze, and Microwave.  Subtract 7 from all secondary stats.'''

    # Implementation
    for secondaryAttribute in player["Archetype"].secondaryAttributes:
        pmod["Modifications"].append({"Operation" : "Subtract", "Key" : secondaryAttribute, "Value" : 7})
    pmod["Modifications"].append({"Operation": "Set", "Key": "SOAwar", "Value": 99})
    pmod["Modifications"].append({"Operation": "Set", "Key": "SDAwar", "Value": 99})
    pmod["Modifications"].append({"Operation": "Set", "Key": "SigSkill1", "Value": "Shot Creator"})
    pmod["Modifications"].append({"Operation": "Set", "Key": "SigSkill1", "Value": "Brick Wall"})
    pmod["Modifications"].append({"Operation": "Set", "Key": "SigSkill1", "Value": "Anti-Freeze"})
    pmod["Modifications"].append({"Operation": "Set", "Key": "SigSkill1", "Value": "Microwave"})

    # Return
    return pmod
def Director_Legendary_SwiftnessSerum(player : Player.Player):
    pmod = Player.getPModTemplate()
    # Artifact Name
    pmod["Name"] = '''Swiftness Serum, courtesy of Amalgamo Inc.'''
    # Artifact Info
    pmod["Type"]["TypeName"] = "Artifact"
    pmod["Type"]["ArchetypeLock"] = "Director"
    pmod["Type"]["Rarity"] = "Legendary"
    # Description
    pmod["Description"] = '''Take 1-5 swigs of the Swiftness Serum, each swig provides the player 5 speed and quickness, along with adding 2 to accented secondary stats. Each swig also burns the liver of the player, removing 10 from ball handling and ball security, as well as subtracting 4 from all non-accented secondary stats.\n\n'''

    # Implementation
    swigs = random.randrange(1,6)
    pmod["Modifications"].append({"Operation": "Add", "Key": "SSpeed", "Value": swigs * 5})
    pmod["Modifications"].append({"Operation": "Add", "Key": "SQuick", "Value": swigs * 5})
    pmod["Modifications"].append({"Operation": "Subtract", "Key": "SBallHndl", "Value": swigs * 10})
    pmod["Modifications"].append({"Operation": "Subtract", "Key": "SBallSec", "Value": swigs * 10})
    for secondaryAttribute in player["Archetype"].secondaryAttributes:
        if(secondaryAttribute in player["Archetype"].accentedAttributes):
            pmod["Modifications"].append({"Operation": "Add", "Key": secondaryAttribute, "Value": swigs * 2})
        else:
            pmod["Modifications"].append({"Operation": "Subtract", "Key": secondaryAttribute, "Value": swigs * 4})

    pmod["Description"] += f"This player took {swigs} swig"
    if(swigs > 1):
        pmod["Description"] += "s."
    else:
        pmod["Description"] += "."

    # Return
    return pmod
def Director_Legendary_MidCertification(player : Player.Player):
    pmod = Player.getPModTemplate()
    # Artifact Name
    pmod["Name"] = '''An Ancient Mid Certification Badge, Passed Down for Hundreds of Years'''
    # Artifact Info
    pmod["Type"]["TypeName"] = "Artifact"
    pmod["Type"]["ArchetypeLock"] = "Director"
    pmod["Type"]["Rarity"] = "Legendary"
    # Description
    pmod["Description"] = '''The player knows the weight that such a certification carries, and feels empowered that they are able to carry on its legacy. Shot Medium, Shot Close, and Consistency are set to 99. Add Corner Specialist and Acrobat. All 3PT Hotzones are Cold Zones. -10 to 3PT shot. Add a epic or legendary shot:\n\n'''

    # Implementation
    pmod["Modifications"].append({"Operation": "Set", "Key": "SShtMed", "Value": 99})
    pmod["Modifications"].append({"Operation": "Set", "Key": "SShtCls", "Value": 99})
    pmod["Modifications"].append({"Operation": "Set", "Key": "SConsis", "Value": 99})

    pmod["Modifications"].append({"Operation": "Subtract", "Key": "SSht3PT", "Value": 10})

    pmod["Modifications"].append({"Operation": "Set", "Key": "SigSkill1", "Value": "Corner Specialist"})
    pmod["Modifications"].append({"Operation": "Set", "Key": "SigSkill1", "Value": "Acrobat"})

    pmod["Modifications"].append({"Operation": "Set", "Key": "HZ10", "Value": 0})
    pmod["Modifications"].append({"Operation": "Set", "Key": "HZ11", "Value": 0})
    pmod["Modifications"].append({"Operation": "Set", "Key": "HZ12", "Value": 0})
    pmod["Modifications"].append({"Operation": "Set", "Key": "HZ13", "Value": 0})
    pmod["Modifications"].append({"Operation": "Set", "Key": "HZ14", "Value": 0})

    pmod["Modifications"].append({"Operation": "Add", "Key": "SSpeed", "Value": 5})

    potentialSpecialShots = LEGENDARY_SPECIAL_SHOTS["Director"] + EPIC_SPECIAL_SHOTS["Director"]
    specialShotChoice = random.choice(potentialSpecialShots)
    pmod["Modifications"].append({"Operation" : "Set", "Key" : "AShtForm", "Value" : specialShotChoice["Shot Form"]})
    pmod["Modifications"].append({"Operation" : "Set", "Key" : "AShtBase", "Value" : specialShotChoice["Shot Base"]})
    pmod["Description"] += f"**{specialShotChoice['Name']}** - {specialShotChoice['Description']}"


    # Return
    return pmod
def Director_Legendary_MilkdudNarcotics(player : Player.Player):
    pmod = Player.getPModTemplate()
    # Artifact Name
    pmod["Name"] = '''An Assorted Baggy of Mystical Melvin Milkdud's Hallucinogenic Narcotics Labeled "Magic Candy for Kids of All Ages!'''
    # Artifact Info
    pmod["Type"]["TypeName"] = "Artifact"
    pmod["Type"]["ArchetypeLock"] = "Director"
    pmod["Type"]["Rarity"] = "Legendary"
    # Description
    pmod["Description"] = '''Putting all their trust into the disheveled and wild eyed 90 year old, the player giddily gulps down 5 of Melvin's finest candies. Add 40 to Vertical, Offensive Rebound, Defensive Rebound. Remove 6-8 inches of height. Randomly assign each non-3pt zone a hot or cold value.\n\n'''

    # Implementation
    pmod["Modifications"].append({"Operation": "Add", "Key": "SVertical", "Value": 40})
    pmod["Modifications"].append({"Operation": "Add", "Key": "SOReb", "Value": 40})
    pmod["Modifications"].append({"Operation": "Add", "Key": "SDReb", "Value": 40})

    pmod["Modifications"].append({"Operation": "Subtract", "Key": "HeightIn", "Value": random.randrange(6,9)})

    pmod["Modifications"].append({"Operation": "Set", "Key": "HZ1", "Value": random.randrange(0, 3)})
    pmod["Modifications"].append({"Operation": "Set", "Key": "HZ2", "Value": random.randrange(0, 3)})
    pmod["Modifications"].append({"Operation": "Set", "Key": "HZ3", "Value": random.randrange(0, 3)})
    pmod["Modifications"].append({"Operation": "Set", "Key": "HZ4", "Value": random.randrange(0, 3)})
    pmod["Modifications"].append({"Operation": "Set", "Key": "HZ5", "Value": random.randrange(0, 3)})
    pmod["Modifications"].append({"Operation": "Set", "Key": "HZ6", "Value": random.randrange(0, 3)})
    pmod["Modifications"].append({"Operation": "Set", "Key": "HZ7", "Value": random.randrange(0, 3)})
    pmod["Modifications"].append({"Operation": "Set", "Key": "HZ8", "Value": random.randrange(0, 3)})
    pmod["Modifications"].append({"Operation": "Set", "Key": "HZ9", "Value": random.randrange(0, 3)})



    # Return
    return pmod

#endregion === Directors ===

testPlayer = Player.Player()
testPlayer["Archetype"] = Archetypes.ARCH_VIGILANTE
testPlayer.genAttributes()

testPMod = Vigilante_Legendary_EggrollVoucher(testPlayer)
testPlayer.compilePMod(testPMod)