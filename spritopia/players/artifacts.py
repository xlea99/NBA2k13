from spritopia.players import archetypes, pmod_template
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

#region === Neutrals ===

def Neutral_Rare_GaryGloves(player):
    pmod = pmod_template.getPModTemplate()
    # Artifact Name
    pmod["Name"] = '''Gary's Enchanted Gloves'''
    # Artifact Info
    pmod["Type"]["TypeName"] = "Artifact"
    pmod["Type"]["ArchetypeLock"] = "Neutral"
    pmod["Type"]["Rarity"] = "Rare"
    # Image Path
    pmod["Image"] = "ArtifactIcons\\GaryEnchantedGloves.png"
    # Description
    pmod["Description"] = '''Adds Pickpocket, Active Hands, and Interceptor. Remove 40 attribute points randomly across all primary stats.'''

    # Implementation
    pointsToSpend = 40
    adjustedAttributes = {}
    while pointsToSpend > 0:
        randomAttribute = random.choice(player["Archetype"].primaryAttributes)
        adjustedAttributes[randomAttribute] = adjustedAttributes.get(randomAttribute,0) + 1
        pointsToSpend -= 1
    for adjustedAttribute,value in adjustedAttributes.items():
        pmod["Modifications"].append({"Operation": "Subtract", "Key": adjustedAttribute, "Value": value})

    pmod["Modifications"].append({"Operation": "Set", "Key": "SigSkill1", "Value": "Pick Pocketer"})
    pmod["Modifications"].append({"Operation": "Set", "Key": "SigSkill2", "Value": "Active Hands"})
    pmod["Modifications"].append({"Operation": "Set", "Key": "SigSkill3", "Value": "Interceptor"})


    # Return
    return pmod
def Neutral_Rare_CalebLemonade(player):
    pmod = pmod_template.getPModTemplate()
    # Artifact Name
    pmod["Name"] = '''Glass of Caleb's Lemonade'''
    # Artifact Info
    pmod["Type"]["TypeName"] = "Artifact"
    pmod["Type"]["ArchetypeLock"] = "Neutral"
    pmod["Type"]["Rarity"] = "Rare"
    # Image Path
    pmod["Image"] = "ArtifactIcons\\CalebLemonade.png"
    # Description
    pmod["Description"] = '''-5 to all attributes. Add 5 inches to height.'''

    # Implementation
    for attribute in archetypes.ALL_ATTRIBUTES:
        pmod["Modifications"].append({"Operation": "Subtract", "Key": attribute, "Value": 5})

    pmod["Modifications"].append({"Operation": "Add", "Key": "HeightIn", "Value": 5})


    # Return
    return pmod
def Neutral_Rare_PesticideJuice(player):
    pmod = pmod_template.getPModTemplate()
    # Artifact Name
    pmod["Name"] = '''Happy Happy Pesticide Juice 4 Kids'''
    # Artifact Info
    pmod["Type"]["TypeName"] = "Artifact"
    pmod["Type"]["ArchetypeLock"] = "Neutral"
    pmod["Type"]["Rarity"] = "Rare"
    # Image Path
    pmod["Image"] = "ArtifactIcons\\HHPJuiceforKids.png"
    # Description
    pmod["Description"] = '''Add Antifreeze and Heat Retention. -25 a random, unaccented Primary Stat.'''

    # Implementation
    possibleAttributes = []
    for attribute in player["Archetype"].primaryAttributes:
        if(attribute in player["Archetype"].unaccentedAttributes):
            possibleAttributes.append(attribute)

    pmod["Modifications"].append({"Operation": "Subtract", "Key": random.choice(possibleAttributes), "Value": 25})
    pmod["Modifications"].append({"Operation": "Set", "Key": "SigSkill1", "Value": "Anti-Freeze"})
    pmod["Modifications"].append({"Operation": "Set", "Key": "SigSkill1", "Value": "Heat Retention"})


    # Return
    return pmod
def Neutral_Rare_BuffetSneakers(player):
    pmod = pmod_template.getPModTemplate()
    # Artifact Name
    pmod["Name"] = '''Sneakers that Mike Buffett Sabotaged with Glue'''
    # Artifact Info
    pmod["Type"]["TypeName"] = "Artifact"
    pmod["Type"]["ArchetypeLock"] = "Neutral"
    pmod["Type"]["Rarity"] = "Rare"
    # Image Path
    pmod["Image"] = "ArtifactIcons\\MikeBuffetSneakers.png"
    # Description
    pmod["Description"] = '''Player must have a set shot.  Set Vertical to 25.'''

    # Implementation
    pmod["Modifications"].append({"Operation": "Set", "Key": "AShtBase", "Value": random.randrange(41,59)})
    pmod["Modifications"].append({"Operation": "Set", "Key": "SVertical", "Value": 25})


    # Return
    return pmod
def Neutral_Rare_RomeSandals(player):
    pmod = pmod_template.getPModTemplate()
    # Artifact Name
    pmod["Name"] = '''Sandals Dipped in Rome's Finest Slime Cauldron'''
    # Artifact Info
    pmod["Type"]["TypeName"] = "Artifact"
    pmod["Type"]["ArchetypeLock"] = "Neutral"
    pmod["Type"]["Rarity"] = "Rare"
    # Image Path
    pmod["Image"] = "ArtifactIcons\\SlimeSandals.png"
    # Description
    pmod["Description"] = '''Add 25 to Vertical. -30 to a random, accented Primary Stat.'''

    # Implementation
    pmod["Modifications"].append({"Operation": "Add", "Key": "SVertical", "Value": 25})

    possibleAttributes = []
    for primaryAttribute in player["Archetype"].primaryAttributes:
        if(primaryAttribute in player["Archetype"].accentedAttributes):
            possibleAttributes.append(primaryAttribute)

    pmod["Modifications"].append({"Operation": "Subtract", "Key": random.choice(possibleAttributes), "Value": 30})


    # Return
    return pmod
def Neutral_Rare_ScooterLoops(player):
    pmod = pmod_template.getPModTemplate()
    # Artifact Name
    pmod["Name"] = '''Bowl of Scooter Loops'''
    # Artifact Info
    pmod["Type"]["TypeName"] = "Artifact"
    pmod["Type"]["ArchetypeLock"] = "Neutral"
    pmod["Type"]["Rarity"] = "Rare"
    # Image Path
    pmod["Image"] = "ArtifactIcons\\ScooterLoops.png"
    # Description
    pmod["Description"] = '''A random, accented secondary skill is set to 25. All points lost in the category are randomly distributed across other secondary skills.'''

    # Implementation
    possibleAttributes = []
    for secondaryAttribute in player["Archetype"].secondaryAttributes:
        if(secondaryAttribute in player["Archetype"].accentedAttributes):
            possibleAttributes.append(secondaryAttribute)

    targetAttribute = random.choice(possibleAttributes)
    previousTargetAttributeValue = player[targetAttribute]
    pmod["Modifications"].append({"Operation": "Set", "Key": targetAttribute, "Value": 25})

    pointsToDistribute = previousTargetAttributeValue - 25
    adjustedAttributes = {}
    while pointsToDistribute > 0:
        randomAttribute = random.choice(player["Archetype"].secondaryAttributes)
        adjustedAttributes[randomAttribute] = adjustedAttributes.get(randomAttribute,0) + 1
        pointsToDistribute -= 1
    for adjustedAttribute,value in adjustedAttributes.items():
        pmod["Modifications"].append({"Operation": "Add", "Key": adjustedAttribute, "Value": value})


    # Return
    return pmod
def Neutral_Rare_CornerClub(player):
    pmod = pmod_template.getPModTemplate()
    # Artifact Name
    pmod["Name"] = '''Corner Guy's Famous Subway Club'''
    # Artifact Info
    pmod["Type"]["TypeName"] = "Artifact"
    pmod["Type"]["ArchetypeLock"] = "Neutral"
    pmod["Type"]["Rarity"] = "Rare"
    # Image Path
    pmod["Image"] = "ArtifactIcons\\CornerGuyClub.png"
    # Description
    pmod["Description"] = '''-5 inches to height. +5 to all unaccented primary stats. Adds Corner Specialist.'''

    # Implementation
    for primaryAttribute in player["Archetype"].primaryAttributes:
        if(primaryAttribute in player["Archetype"].unaccentedAttributes):
            pmod["Modifications"].append({"Operation": "Add", "Key": primaryAttribute, "Value": 5})
    pmod["Modifications"].append({"Operation": "Set", "Key": "SigSkill1", "Value": "Corner Specialist"})
    pmod["Modifications"].append({"Operation": "Subtract", "Key": "HeightIn", "Value": 5})





    # Return
    return pmod
def Neutral_Rare_BlueMeth(player):
    pmod = pmod_template.getPModTemplate()
    # Artifact Name
    pmod["Name"] = '''Blue Crystal Meth'''
    # Artifact Info
    pmod["Type"]["TypeName"] = "Artifact"
    pmod["Type"]["ArchetypeLock"] = "Neutral"
    pmod["Type"]["Rarity"] = "Rare"
    # Image Path
    pmod["Image"] = "ArtifactIcons\\BlueMeth.png"
    # Description
    pmod["Description"] = '''Subtract -40 from both Offensive and Defensive Awareness.  Adds Microwave.'''

    # Implementation
    pmod["Modifications"].append({"Operation": "Subtract", "Key": "SOAwar", "Value": 40})
    pmod["Modifications"].append({"Operation": "Subtract", "Key": "SDAwar", "Value": 40})
    pmod["Modifications"].append({"Operation": "Set", "Key": "SigSkill1", "Value": "Microwave"})


    # Return
    return pmod
neutral_rare = [Neutral_Rare_GaryGloves,Neutral_Rare_CalebLemonade,Neutral_Rare_PesticideJuice,
                Neutral_Rare_BuffetSneakers,Neutral_Rare_BlueMeth,Neutral_Rare_RomeSandals,Neutral_Rare_ScooterLoops,
                Neutral_Rare_CornerClub]
def Neutral_Epic_LincolnOs(player):
    pmod = pmod_template.getPModTemplate()
    # Artifact Name
    pmod["Name"] = '''Bowl of Lincoln-O's'''
    # Artifact Info
    pmod["Type"]["TypeName"] = "Artifact"
    pmod["Type"]["ArchetypeLock"] = "Neutral"
    pmod["Type"]["Rarity"] = "Epic"
    # Image Path
    pmod["Image"] = "ArtifactIcons\\LincolnOs.png"
    # Description
    pmod["Description"] = '''A random, accented primary skill is set to 25. All points lost in the category are randomly distributed across secondary skills.'''

    # Implementation
    possibleAttributes = []
    for primaryAttribute in player["Archetype"].primaryAttributes:
        if(primaryAttribute in player["Archetype"].accentedAttributes):
            possibleAttributes.append(primaryAttribute)
    targetAttribute = random.choice(possibleAttributes)
    previousTargetAttributeValue = player[targetAttribute]
    pmod["Modifications"].append({"Operation": "Set", "Key": targetAttribute, "Value": 25})

    pointsToSpend = previousTargetAttributeValue - 25
    adjustedAttributes = {}
    while pointsToSpend > 0:
        randomAttribute = random.choice(player["Archetype"].secondaryAttributes)
        adjustedAttributes[randomAttribute] = adjustedAttributes.get(randomAttribute,0) + 1
        pointsToSpend -= 1
    for adjustedAttribute,value in adjustedAttributes.items():
        pmod["Modifications"].append({"Operation": "Add", "Key": adjustedAttribute, "Value": value})


    # Return
    return pmod
def Neutral_Epic_PilatesCourse(player):
    pmod = pmod_template.getPModTemplate()
    # Artifact Name
    pmod["Name"] = '''Warren the Undying's Intense Pilates Crash Course'''
    # Artifact Info
    pmod["Type"]["TypeName"] = "Artifact"
    pmod["Type"]["ArchetypeLock"] = "Neutral"
    pmod["Type"]["Rarity"] = "Epic"
    # Image Path
    pmod["Image"] = "ArtifactIcons\\WarrenPilatesCourse.png"
    # Description
    pmod["Description"] = '''Add +5-7 to all accented Primary stats. -5 to all other stats.'''

    # Implementation
    for attribute in archetypes.ALL_ATTRIBUTES:
        if(attribute in player["Archetype"].primaryAttributes and attribute in player["Archetype"].accentedAttributes):
            pmod["Modifications"].append({"Operation": "Add", "Key": attribute, "Value": random.randrange(5,8)})
        else:
            pmod["Modifications"].append({"Operation": "Subtract", "Key": attribute, "Value": 5})






    # Return
    return pmod
def Neutral_Epic_PowerWordBo(player):
    pmod = pmod_template.getPModTemplate()
    # Artifact Name
    pmod["Name"] = '''Scroll of Power Word: Bo'''
    # Artifact Info
    pmod["Type"]["TypeName"] = "Artifact"
    pmod["Type"]["ArchetypeLock"] = "Neutral"
    pmod["Type"]["Rarity"] = "Epic"
    # Image Path
    pmod["Image"] = "ArtifactIcons\\PowerWordBo.png"
    # Description
    pmod["Description"] = '''Shot Inside is set to 99. Shot Close, Shot Medium, and Shot 3pt are set to 25.  Add 6 inches to Height.'''

    # Implementation
    pmod["Modifications"].append({"Operation": "Set", "Key": "SShtIns", "Value": 99})
    pmod["Modifications"].append({"Operation": "Set", "Key": "SShtCls", "Value": 25})
    pmod["Modifications"].append({"Operation": "Set", "Key": "SShtMed", "Value": 25})
    pmod["Modifications"].append({"Operation": "Set", "Key": "SSht3PT", "Value": 25})

    pmod["Modifications"].append({"Operation": "Add", "Key": "HeightIn", "Value": 6})


    # Return
    return pmod
def Neutral_Epic_PowerWordConfuse(player):
    pmod = pmod_template.getPModTemplate()
    # Artifact Name
    pmod["Name"] = '''Scroll of Power Word: Confuse'''
    # Artifact Info
    pmod["Type"]["TypeName"] = "Artifact"
    pmod["Type"]["ArchetypeLock"] = "Neutral"
    pmod["Type"]["Rarity"] = "Epic"
    # Image Path
    pmod["Image"] = "ArtifactIcons\\PowerWordConfuse.png"
    # Description
    pmod["Description"] = '''Swap 2 primary and 2 tertiary stats. -3 to all secondary stats.'''

    # Implementation
    for secondaryAttribute in player["Archetype"].secondaryAttributes:
        pmod["Modifications"].append({"Operation": "Subtract", "Key": secondaryAttribute, "Value": 3})

    possiblePrimaryAttributes = player["Archetype"].primaryAttributes.copy()
    primaryAttribute1 = random.choice(possiblePrimaryAttributes)
    possiblePrimaryAttributes.remove(primaryAttribute1)
    primaryAttribute2 = random.choice(possiblePrimaryAttributes)

    possibleTertiaryAttributes = player["Archetype"].tertiaryAttributes.copy()
    tertiaryAttribute1 = random.choice(possibleTertiaryAttributes)
    possibleTertiaryAttributes.remove(tertiaryAttribute1)
    tertiaryAttribute2 = random.choice(possibleTertiaryAttributes)

    pmod["Modifications"].append({"Operation": "Set", "Key": primaryAttribute1, "Value": player[tertiaryAttribute1]})
    pmod["Modifications"].append({"Operation": "Set", "Key": primaryAttribute2, "Value": player[tertiaryAttribute2]})
    pmod["Modifications"].append({"Operation": "Set", "Key": tertiaryAttribute1, "Value": player[primaryAttribute1]})
    pmod["Modifications"].append({"Operation": "Set", "Key": tertiaryAttribute2, "Value": player[primaryAttribute2]})


    # Return
    return pmod
def Neutral_Epic_PowerWordBluegill(player):
    pmod = pmod_template.getPModTemplate()
    # Artifact Name
    pmod["Name"] = '''Scroll of Power Word: Bluegill'''
    # Artifact Info
    pmod["Type"]["TypeName"] = "Artifact"
    pmod["Type"]["ArchetypeLock"] = "Neutral"
    pmod["Type"]["Rarity"] = "Epic"
    # Image Path
    pmod["Image"] = "ArtifactIcons\\PowerWordBluegill.png"
    # Description
    pmod["Description"] = '''Set Dunk, Standing Dunk, and Vertical to 99. Add 3 cool dunk packages. Add Posterizer and Highlight Film. -5-10 to all other stats.'''

    # Implementation
    for attribute in archetypes.ALL_ATTRIBUTES:
        if(attribute in ["SDunk","SStdDunk","SVertical"]):
            pmod["Modifications"].append({"Operation": "Set", "Key": attribute, "Value": 99})
        else:
            pmod["Modifications"].append({"Operation": "Subtract", "Key": attribute, "Value": random.randrange(5,11)})

    pmod["Modifications"].append({"Operation": "Set", "Key": "SigSkill1", "Value": "Posterizer"})
    pmod["Modifications"].append({"Operation": "Set", "Key": "SigSkill2", "Value": "Highlight Film"})

    coolDunks = [23,24,25,26,27,28,35,51,55,63,64,65]
    dunk1 = random.choice(coolDunks)
    coolDunks.remove(dunk1)
    dunk2 = random.choice(coolDunks)
    coolDunks.remove(dunk2)
    dunk3 = random.choice(coolDunks)
    pmod["Modifications"].append({"Operation": "Set", "Key": "AGoToDunk", "Value": dunk1})
    pmod["Modifications"].append({"Operation": "Set", "Key": "ADunk2", "Value": dunk2})
    pmod["Modifications"].append({"Operation": "Set", "Key": "ADunk3", "Value": dunk3})






    # Return
    return pmod
def Neutral_Epic_PowerWordSiamese(player):
    pmod = pmod_template.getPModTemplate()
    # Artifact Name
    pmod["Name"] = '''Scroll of Power Word: Siamese'''
    # Artifact Info
    pmod["Type"]["TypeName"] = "Artifact"
    pmod["Type"]["ArchetypeLock"] = "Neutral"
    pmod["Type"]["Rarity"] = "Epic"
    # Image Path
    pmod["Image"] = "ArtifactIcons\\PowerWordSiamese.png"
    # Description
    pmod["Description"] = '''Both Shot Form and Shot Base are set to the same random ID. Select one primary stat and have it copy the stat of another random primary stat. Add 2 random skill cards.  Set spot-up and post-up tendencies to 50 each.'''

    # Implementation
    shotBaseAndFormChoice = random.randrange(1,125)
    pmod["Modifications"].append({"Operation": "Set", "Key": "AShtForm", "Value": shotBaseAndFormChoice})
    pmod["Modifications"].append({"Operation": "Set", "Key": "AShtBase", "Value": shotBaseAndFormChoice})

    possiblePrimaryAttributes = player["Archetype"].primaryAttributes.copy()
    attributeToReceiveCopy = random.choice(possiblePrimaryAttributes)
    possiblePrimaryAttributes.remove(attributeToReceiveCopy)
    attributeToGiveCopy = random.choice(possiblePrimaryAttributes)
    pmod["Modifications"].append({"Operation": "Set", "Key": attributeToReceiveCopy, "Value": player[attributeToGiveCopy]})


    sigSkillValues = list(range(1,32))
    random.shuffle(sigSkillValues)
    pmod["Modifications"].append({"Operation": "Set", "Key": "SigSkill1", "Value": sigSkillValues[0]})
    pmod["Modifications"].append({"Operation": "Set", "Key": "SigSkill2", "Value": sigSkillValues[1]})

    pmod["Modifications"].append({"Operation": "Set", "Key": "TSpotUp", "Value": 50})
    pmod["Modifications"].append({"Operation": "Set", "Key": "TPostUp", "Value": 50})







    # Return
    return pmod
neutral_epic = [Neutral_Epic_LincolnOs,Neutral_Epic_PilatesCourse,Neutral_Epic_PowerWordBo,Neutral_Epic_PowerWordConfuse,
                Neutral_Epic_PowerWordBluegill,Neutral_Epic_PowerWordSiamese]
def Neutral_Legendary_LaatzCrunch(player):
    pmod = pmod_template.getPModTemplate()
    # Artifact Name
    pmod["Name"] = '''Bowl of Honey Laatz Crunch'''
    # Artifact Info
    pmod["Type"]["TypeName"] = "Artifact"
    pmod["Type"]["ArchetypeLock"] = "Neutral"
    pmod["Type"]["Rarity"] = "Legendary"
    # Image Path
    pmod["Image"] = "ArtifactIcons\\HoneyLaatzCrunch.png"
    # Description
    pmod["Description"] = '''Three random, accented tertiary skills are set to 80. All points gained are randomly removed from other primary skills.'''

    # Implementation
    possibleTeritaryAttributes = []
    for tertiaryAttribute in player["Archetype"].tertiaryAttributes:
        if(tertiaryAttribute in player["Archetype"].accentedAttributes):
            possibleTeritaryAttributes.append(tertiaryAttribute)

    tertiaryAttribute1 = random.choice(possibleTeritaryAttributes)
    possibleTeritaryAttributes.remove(tertiaryAttribute1)
    tertiaryAttribute2 = random.choice(possibleTeritaryAttributes)
    possibleTeritaryAttributes.remove(tertiaryAttribute2)
    tertiaryAttribute3 = random.choice(possibleTeritaryAttributes)

    pointsToDistribute = (80 - player[tertiaryAttribute1]) + (80 - player[tertiaryAttribute2]) + (80 - player[tertiaryAttribute3])
    pmod["Modifications"].append({"Operation": "Set", "Key": tertiaryAttribute1, "Value": 80})
    pmod["Modifications"].append({"Operation": "Set", "Key": tertiaryAttribute2, "Value": 80})
    pmod["Modifications"].append({"Operation": "Set", "Key": tertiaryAttribute3, "Value": 80})

    adjustedAttributes = {}
    while pointsToDistribute > 0:
        randomAttribute = random.choice(player["Archetype"].primaryAttributes)
        adjustedAttributes[randomAttribute] = adjustedAttributes.get(randomAttribute,0) + 1
        pointsToDistribute -= 1
    for adjustedAttribute,value in adjustedAttributes.items():
        pmod["Modifications"].append({"Operation": "Subtract", "Key": adjustedAttribute, "Value": value})







    # Return
    return pmod
def Neutral_Legendary_PowerWordRickMorty(player):
    pmod = pmod_template.getPModTemplate()
    # Artifact Name
    pmod["Name"] = '''Scrolls of Power Words: Rick and Morty'''
    # Artifact Info
    pmod["Type"]["TypeName"] = "Artifact"
    pmod["Type"]["ArchetypeLock"] = "Neutral"
    pmod["Type"]["Rarity"] = "Legendary"
    # Image Path
    pmod["Image"] = "ArtifactIcons\\PowerWordsRickMorty.png"
    # Description
    pmod["Description"] = '''Randomly add 50 to Speed or Quickness. Subtract 50 from the other. Randomly add 25 to Vertical or both Rebounds. Subtract 25 from the other. Randomly add 10 to Shot 3pt or 4 inches to Height. Do the reverse for the other.'''

    # Implementation
    speedQuickGain = random.choice([1,-1])
    pmod["Modifications"].append({"Operation": "Add", "Key": "SSpeed", "Value": 50 * speedQuickGain})
    pmod["Modifications"].append({"Operation": "Add", "Key": "SQuick", "Value": -50 * speedQuickGain})

    reboundVerticalGain = random.choice([1,-1])
    pmod["Modifications"].append({"Operation": "Add", "Key": "SVertical", "Value": 25 * reboundVerticalGain})
    pmod["Modifications"].append({"Operation": "Add", "Key": "SOReb", "Value": -25 * reboundVerticalGain})
    pmod["Modifications"].append({"Operation": "Add", "Key": "SDReb", "Value": -25 * reboundVerticalGain})

    heightThreeGain = random.choice([1,-1])
    pmod["Modifications"].append({"Operation": "Add", "Key": "SSht3PT", "Value": 10 * heightThreeGain})
    pmod["Modifications"].append({"Operation": "Add", "Key": "HeightIn", "Value": -4 * heightThreeGain})





    # Return
    return pmod
def Neutral_Legendary_PrimaryCertificate(player):
    pmod = pmod_template.getPModTemplate()
    # Artifact Name
    pmod["Name"] = '''A Certification, Declaring: 'Ah yes, you know your Primary well!\''''
    # Artifact Info
    pmod["Type"]["TypeName"] = "Artifact"
    pmod["Type"]["ArchetypeLock"] = "Neutral"
    pmod["Type"]["Rarity"] = "Legendary"
    # Image Path
    pmod["Image"] = "ArtifactIcons\\PrimaryCertification.png"
    # Description
    pmod["Description"] = '''Secondary stats are rerolled 25-45. +15 to all unaccented primary stats, +10 to all accented primary stats. Add 2 random skill cards.'''

    # Implementation
    for secondaryAttribute in player["Archetype"].secondaryAttributes:
        pmod["Modifications"].append({"Operation": "Set", "Key": secondaryAttribute, "Value": random.randrange(25,46)})

    for primaryAttribute in player["Archetype"].primaryAttributes:
        if(primaryAttribute in player["Archetype"].accentedAttributes):
            pmod["Modifications"].append({"Operation": "Add", "Key": primaryAttribute, "Value": 10})
        else:
            pmod["Modifications"].append({"Operation": "Add", "Key": primaryAttribute, "Value": 15})


    sigSkillValues = list(range(1,32))
    random.shuffle(sigSkillValues)
    pmod["Modifications"].append({"Operation": "Set", "Key": "SigSkill1", "Value": sigSkillValues[0]})
    pmod["Modifications"].append({"Operation": "Set", "Key": "SigSkill2", "Value": sigSkillValues[1]})





    # Return
    return pmod
def Neutral_Legendary_YesCindy(player):
    pmod = pmod_template.getPModTemplate()
    # Artifact Name
    pmod["Name"] = '''Yes Cindy, I'm sure they're the right ones...'''
    # Artifact Info
    pmod["Type"]["TypeName"] = "Artifact"
    pmod["Type"]["ArchetypeLock"] = "Neutral"
    pmod["Type"]["Rarity"] = "Legendary"
    # Image Path
    pmod["Image"] = "ArtifactIcons\\YesCindy.png"
    # Description
    pmod["Description"] = '''Add 30 to all tertiary stats, remove 20 from all primary stats. Add a fully random special shot:\n\n'''

    # Implementation
    for tertiaryAttribute in player["Archetype"].tertiaryAttributes:
        pmod["Modifications"].append({"Operation": "Add", "Key": tertiaryAttribute, "Value": 30})

    for primaryAttribute in player["Archetype"].primaryAttributes:
        pmod["Modifications"].append({"Operation": "Subtract", "Key": primaryAttribute, "Value": 20})

    potentialSpecialShots = []
    for shotList in RARE_SPECIAL_SHOTS.values():
        potentialSpecialShots += shotList
    for shotList in EPIC_SPECIAL_SHOTS.values():
        potentialSpecialShots += shotList
    for shotList in LEGENDARY_SPECIAL_SHOTS.values():
        potentialSpecialShots += shotList
    specialShotChoice = random.choice(potentialSpecialShots)
    pmod["Modifications"].append({"Operation": "Set", "Key": "AShtForm", "Value": specialShotChoice["Shot Form"]})
    pmod["Modifications"].append({"Operation": "Set", "Key": "AShtBase", "Value": specialShotChoice["Shot Base"]})
    pmod["Description"] += f"**{specialShotChoice['Name']}** - {specialShotChoice['Description']}"



    # Return
    return pmod
neutral_legendary = [Neutral_Legendary_LaatzCrunch,Neutral_Legendary_PowerWordRickMorty,
                     Neutral_Legendary_PrimaryCertificate,Neutral_Legendary_YesCindy]
def Neutral_Godlike_PhysicalizedBiases(player):
    pmod = pmod_template.getPModTemplate()
    # Artifact Name
    pmod["Name"] = '''Physicalized Biases of a Less Refined Time'''
    # Artifact Info
    pmod["Type"]["TypeName"] = "Artifact"
    pmod["Type"]["ArchetypeLock"] = "Neutral"
    pmod["Type"]["Rarity"] = "Godlike"
    # Image Path
    pmod["Image"] = "ArtifactIcons\\PhysicalizedBiases.png"
    # Description
    pmod["Description"] = '''Set 3pt between 80-100. -25 to all other stats'''

    # Implementation
    for attribute in archetypes.ALL_ATTRIBUTES:
        if(attribute == "SSht3PT"):
            pmod["Modifications"].append({"Operation": "Set", "Key": attribute, "Value": random.randrange(80, 100)})
        else:
            pmod["Modifications"].append({"Operation": "Subtract", "Key": attribute, "Value": 25})


    # Return
    return pmod
def Neutral_Godlike_ConcoctionJOE(player):
    pmod = pmod_template.getPModTemplate()
    # Artifact Name
    pmod["Name"] = '''Concoction J.O.E. #30330'''
    # Artifact Info
    pmod["Type"]["TypeName"] = "Artifact"
    pmod["Type"]["ArchetypeLock"] = "Neutral"
    pmod["Type"]["Rarity"] = "Godlike"
    # Image Path
    pmod["Image"] = "ArtifactIcons\\ConcoctionJOE.png"
    # Description
    pmod["Description"] = '''Set all attributes to 30. Add Microwave, War General, Defensive Anchor, Lockdown Defender, and Acrobat. All zones are Burning Zones.'''

    # Implementation
    for attribute in archetypes.ALL_ATTRIBUTES:
        pmod["Modifications"].append({"Operation": "Set", "Key": attribute, "Value": 30})

    pmod["Modifications"].append({"Operation": "Set", "Key": "SigSkill1", "Value": "Microwave"})
    pmod["Modifications"].append({"Operation": "Set", "Key": "SigSkill2", "Value": "Floor General"})
    pmod["Modifications"].append({"Operation": "Set", "Key": "SigSkill3", "Value": "Defensive Anchor"})
    pmod["Modifications"].append({"Operation": "Set", "Key": "SigSkill4", "Value": "Lockdown Defender"})
    pmod["Modifications"].append({"Operation": "Set", "Key": "SigSkill5", "Value": "Acrobat"})

    pmod["Modifications"].append({"Operation": "Set", "Key": "HZ1", "Value": 3})
    pmod["Modifications"].append({"Operation": "Set", "Key": "HZ2", "Value": 3})
    pmod["Modifications"].append({"Operation": "Set", "Key": "HZ3", "Value": 3})
    pmod["Modifications"].append({"Operation": "Set", "Key": "HZ4", "Value": 3})
    pmod["Modifications"].append({"Operation": "Set", "Key": "HZ5", "Value": 3})
    pmod["Modifications"].append({"Operation": "Set", "Key": "HZ6", "Value": 3})
    pmod["Modifications"].append({"Operation": "Set", "Key": "HZ7", "Value": 3})
    pmod["Modifications"].append({"Operation": "Set", "Key": "HZ8", "Value": 3})
    pmod["Modifications"].append({"Operation": "Set", "Key": "HZ9", "Value": 3})
    pmod["Modifications"].append({"Operation": "Set", "Key": "HZ10", "Value": 3})
    pmod["Modifications"].append({"Operation": "Set", "Key": "HZ11", "Value": 3})
    pmod["Modifications"].append({"Operation": "Set", "Key": "HZ12", "Value": 3})
    pmod["Modifications"].append({"Operation": "Set", "Key": "HZ13", "Value": 3})
    pmod["Modifications"].append({"Operation": "Set", "Key": "HZ14", "Value": 3})


    # Return
    return pmod
def Neutral_Godlike_RickAshes(player):
    pmod = pmod_template.getPModTemplate()
    # Artifact Name
    pmod["Name"] = '''The Electrified Ashes of Simple Rick'''
    # Artifact Info
    pmod["Type"]["TypeName"] = "Artifact"
    pmod["Type"]["ArchetypeLock"] = "Neutral"
    pmod["Type"]["Rarity"] = "Godlike"
    # Image Path
    pmod["Image"] = "ArtifactIcons\\ElectrifiedAshes.png"
    # Description
    pmod["Description"] = '''Set all attributes to 70.'''

    # Implementation
    for attribute in archetypes.ALL_ATTRIBUTES:
        pmod["Modifications"].append({"Operation": "Set", "Key": attribute, "Value": 70})


    # Return
    return pmod
def Neutral_Godlike_BrokenPromise(player):
    pmod = pmod_template.getPModTemplate()
    # Artifact Name
    pmod["Name"] = '''The Broken Promise of Fitzgerald Kambavolo's Last Words: 'No One Else\''''
    # Artifact Info
    pmod["Type"]["TypeName"] = "Artifact"
    pmod["Type"]["ArchetypeLock"] = "Neutral"
    pmod["Type"]["Rarity"] = "Godlike"
    # Image Path
    pmod["Image"] = "ArtifactIcons\\NoOneElse.png"
    # Description
    pmod["Description"] = '''Height is set between 8'5 and 8'10. All abilities except for one random primary and one random secondary are set to 25. Give the player Brick Wall.'''

    # Implementation
    randomPrimaryAttribute = random.choice(player["Archetype"].primaryAttributes)
    randomSecondaryAttribute = random.choice(player["Archetype"].secondaryAttributes)

    for attribute in archetypes.ALL_ATTRIBUTES:
        if(attribute not in [randomPrimaryAttribute,randomSecondaryAttribute]):
            pmod["Modifications"].append({"Operation": "Set", "Key": attribute, "Value": 25})

    pmod["Modifications"].append({"Operation": "Set", "Key": "HeightIn", "Value": random.randrange(101,107)})
    pmod["Modifications"].append({"Operation": "Set", "Key": "SigSkill1", "Value": "Brick Wall"})


    # Return
    return pmod
def Neutral_Godlike_RussianRoulette(player):
    pmod = pmod_template.getPModTemplate()
    # Artifact Name
    pmod["Name"] = '''Russian Roulette, A Fuzion Frenzy Special Event!'''
    # Artifact Info
    pmod["Type"]["TypeName"] = "Artifact"
    pmod["Type"]["ArchetypeLock"] = "Neutral"
    pmod["Type"]["Rarity"] = "Godlike"
    # Image Path
    pmod["Image"] = "ArtifactIcons\\FuzionFrenzyRoulette.png"
    # Description
    pmod["Description"] = '''Set all stats to 99. Play 1-6 rounds of Russian Roulette, for each round subtract 7-13 from each stat.\n\n'''

    # Implementation
    currentAttributeVals = {}
    for attribute in archetypes.ALL_ATTRIBUTES:
        currentAttributeVals[attribute] = 99

    roundsOfRussianRoulette = random.randrange(1,7)
    for roundOfRussianRoulette in range(roundsOfRussianRoulette):
        for attribute in currentAttributeVals.keys():
            currentAttributeVals[attribute] -= random.randrange(7,14)

    for attribute,value in currentAttributeVals.items():
        pmod["Modifications"].append({"Operation": "Set", "Key": attribute, "Value": value})

    if(roundsOfRussianRoulette > 1):
        pmod["Description"] += f"This player played {roundsOfRussianRoulette} rounds of Russian Roulette."
    else:
        pmod["Description"] += f"This player played {roundsOfRussianRoulette} round of Russian Roulette."


    # Return
    return pmod
def Neutral_Godlike_PesticideBeer(player):
    pmod = pmod_template.getPModTemplate()
    # Artifact Name
    pmod["Name"] = '''Home Brewed Insecticide Lite Beer by HHP Inc'''
    # Artifact Info
    pmod["Type"]["TypeName"] = "Artifact"
    pmod["Type"]["ArchetypeLock"] = "Neutral"
    pmod["Type"]["Rarity"] = "Godlike"
    # Image Path
    pmod["Image"] = "ArtifactIcons\\HHPBeer.png"
    # Description
    pmod["Description"] = '''Take 100 swigs of the addictive brew. This causes severe alcohol poisoning and sends him into court-mandated rehab. He becomes a new, better person - randomly select a new Primary, Secondary, and Tertiary set, as well as new accents for each stat. Important tendencies are randomized. Add 2 random skill cards.\n\n'''

    # Implementation
    possibleAttributeSets = {"Offensive" : archetypes.OFFENSIVE_ATTRIBUTES, "Control" : archetypes.CONTROL_ATTRIBUTES, "Defensive" : archetypes.DEFENSIVE_ATTRIBUTES}
    allSets = list(possibleAttributeSets.keys())
    random.shuffle(allSets)
    newPrimary,newSecondary,newTertiary = allSets[0],allSets[1],allSets[2]

    newPrimaryAccents = []
    for primaryAttribute in possibleAttributeSets[newPrimary]:
        if(random.randrange(1,6) <= 2):
            newPrimaryAccents.append(primaryAttribute)
    newSecondaryAccents = []
    for secondaryAttribute in possibleAttributeSets[newSecondary]:
        if(random.randrange(1,6) <= 2):
            newSecondaryAccents.append(secondaryAttribute)
    newTertiaryAccents = []
    for tertiaryAttribute in possibleAttributeSets[newTertiary]:
        if(random.randrange(1,6) <= 2):
            newTertiaryAccents.append(tertiaryAttribute)


    for primaryAttribute in possibleAttributeSets[newPrimary]:
        if(primaryAttribute in newPrimaryAccents):
            pmod["Modifications"].append({"Operation": "Set", "Key": primaryAttribute, "Value": random.randrange(80, 100)})
        else:
            pmod["Modifications"].append({"Operation": "Set", "Key": primaryAttribute, "Value": random.randrange(70,86)})
    for secondaryAttribute in possibleAttributeSets[newSecondary]:
        if(secondaryAttribute in newSecondaryAccents):
            pmod["Modifications"].append({"Operation": "Set", "Key": secondaryAttribute, "Value": random.randrange(60, 76)})
        else:
            pmod["Modifications"].append({"Operation": "Set", "Key": secondaryAttribute, "Value": random.randrange(50,66)})
    for tertiaryAttribute in possibleAttributeSets[newTertiary]:
        if(tertiaryAttribute in newTertiaryAccents):
            pmod["Modifications"].append({"Operation": "Set", "Key": tertiaryAttribute, "Value": random.randrange(35, 51)})
        else:
            pmod["Modifications"].append({"Operation": "Set", "Key": tertiaryAttribute, "Value": random.randrange(25,46)})


    pmod["Modifications"].append({"Operation": "Set", "Key": "TSpotUp", "Value": random.randrange(1, 101)})
    pmod["Modifications"].append({"Operation": "Set", "Key": "TPostUp", "Value": random.randrange(1, 101)})
    pmod["Modifications"].append({"Operation": "Set", "Key": "TDunkvLU", "Value": random.randrange(1, 101)})
    pmod["Modifications"].append({"Operation": "Set", "Key": "TPostFaceU", "Value": random.randrange(1, 101)})
    pmod["Modifications"].append({"Operation": "Set", "Key": "TPostBDown", "Value": random.randrange(1, 101)})

    pmod["Modifications"].append({"Operation": "Set", "Key": "SigSkill1", "Value": random.randrange(1, 32)})
    pmod["Modifications"].append({"Operation": "Set", "Key": "SigSkill2", "Value": random.randrange(1, 32)})


    pmod["Description"] += f"{newPrimary} Primary --- Accents ("
    for accent in newPrimaryAccents:
        pmod["Description"] += f"{archetypes.MAPPED_ATTRIBUTES[accent]}, "
    pmod["Description"] = pmod["Description"].rstrip(", ")
    pmod["Description"] += ")\n"

    pmod["Description"] += f"{newSecondary} Secondary --- Accents ("
    for accent in newSecondaryAccents:
        pmod["Description"] += f"{archetypes.MAPPED_ATTRIBUTES[accent]}, "
    pmod["Description"] = pmod["Description"].rstrip(", ")
    pmod["Description"] += ")\n"

    pmod["Description"] += f"{newTertiary} Tertiary --- Accents ("
    for accent in newTertiaryAccents:
        pmod["Description"] += f"{archetypes.MAPPED_ATTRIBUTES[accent]}, "
    pmod["Description"] = pmod["Description"].rstrip(", ")
    pmod["Description"] += ")"


    # Return
    return pmod
def Neutral_Godlike_ArcaneRemnants(player):
    pmod = pmod_template.getPModTemplate()
    # Artifact Name
    pmod["Name"] = '''Remnants of an Arcane Explosion Caused by the Dark Magic of Matt Bleakstar.'''
    # Artifact Info
    pmod["Type"]["TypeName"] = "Artifact"
    pmod["Type"]["ArchetypeLock"] = "Neutral"
    pmod["Type"]["Rarity"] = "Godlike"
    # Image Path
    pmod["Image"] = "ArtifactIcons\\RemnantsArcaneExplosion.png"
    # Description
    pmod["Description"] = '''Randomly assign a stat the value of 30. Randomly assign another stat the value of 32. Randomly assign another stat the value of 34. Keep going until you hit 98, this should cover all stats.'''

    # Implementation
    currentValue = 30
    allAttributes = archetypes.ALL_ATTRIBUTES.copy()
    random.shuffle(allAttributes)
    for attribute in allAttributes:
        pmod["Modifications"].append({"Operation": "Set", "Key": attribute, "Value": currentValue})
        currentValue += 2


    # Return
    return pmod
def Neutral_Godlike_SnehGambling(player):
    pmod = pmod_template.getPModTemplate()
    # Artifact Name
    pmod["Name"] = '''Sneh's Crippling Gambling Addiction'''
    # Artifact Info
    pmod["Type"]["TypeName"] = "Artifact"
    pmod["Type"]["ArchetypeLock"] = "Neutral"
    pmod["Type"]["Rarity"] = "Godlike"
    # Image Path
    pmod["Image"] = "ArtifactIcons\\SnehGambling.png"
    # Description
    pmod["Description"] = '''Set all stats to 25. 7 random stats are set to 99. Add 5 random Skill Cards. Set Height between 6'0 - 7'6.'''

    # Implementation
    possibleAttributes = archetypes.ALL_ATTRIBUTES.copy()
    random.shuffle(possibleAttributes)


    for attribute in archetypes.ALL_ATTRIBUTES:
        if(attribute in possibleAttributes[:7]):
            pmod["Modifications"].append({"Operation": "Set", "Key": attribute, "Value": 99})
        else:
            pmod["Modifications"].append({"Operation": "Set", "Key": attribute, "Value": 25})


    sigSkillValues = list(range(1,32))
    random.shuffle(sigSkillValues)
    pmod["Modifications"].append({"Operation": "Set", "Key": "SigSkill1", "Value": sigSkillValues[0]})
    pmod["Modifications"].append({"Operation": "Set", "Key": "SigSkill2", "Value": sigSkillValues[1]})
    pmod["Modifications"].append({"Operation": "Set", "Key": "SigSkill3", "Value": sigSkillValues[2]})
    pmod["Modifications"].append({"Operation": "Set", "Key": "SigSkill4", "Value": sigSkillValues[3]})
    pmod["Modifications"].append({"Operation": "Set", "Key": "SigSkill5", "Value": sigSkillValues[4]})

    pmod["Modifications"].append({"Operation": "Set", "Key": "HeightIn", "Value": random.randrange(72,91)})



    # Return
    return pmod
def Neutral_Godlike_SHRINKRay(player):
    pmod = pmod_template.getPModTemplate()
    # Artifact Name
    pmod["Name"] = '''Fredwardo's Magnificent S.H.R.I.N.K Ray (Something to Help Reduce Inconsistencies in NBA Knowledge)'''
    # Artifact Info
    pmod["Type"]["TypeName"] = "Artifact"
    pmod["Type"]["ArchetypeLock"] = "Neutral"
    pmod["Type"]["Rarity"] = "Godlike"
    # Image Path
    pmod["Image"] = "ArtifactIcons\\ShrinkRay.png"
    # Description
    pmod["Description"] = '''As a big fan of Fredwardo's past work, the Player points the Ray at his head and hopes for the best. Set height to 1'0. Set all attributes to 90-99.'''

    # Implementation
    for attribute in archetypes.ALL_ATTRIBUTES:
        pmod["Modifications"].append({"Operation": "Set", "Key": attribute, "Value": random.randrange(90,100)})
    pmod["Modifications"].append({"Operation": "Set", "Key": "HeightIn", "Value": 12})


    # Return
    return pmod
def Neutral_Godlike_JuicerBlacklist(player):
    pmod = pmod_template.getPModTemplate()
    # Artifact Name
    pmod["Name"] = '''Jared Juicer's Blacklist'''
    # Artifact Info
    pmod["Type"]["TypeName"] = "Artifact"
    pmod["Type"]["ArchetypeLock"] = "Neutral"
    pmod["Type"]["Rarity"] = "Godlike"
    # Image Path
    pmod["Image"] = "ArtifactIcons\\JuicerBlacklist.png"
    # Description
    pmod["Description"] = '''Amazed that almost every single person he knows is on this blacklist, the player decides to totally rethink his in game strategy. Add 3 random skill cards, randomly set all stats to 25-90. Set Height between 5'0 - 7'9. Add any legendary special shot:\n\n'''

    # Implementation
    for attribute in archetypes.ALL_ATTRIBUTES:
        pmod["Modifications"].append({"Operation": "Set", "Key": attribute, "Value": random.randrange(25,100)})

    sigSkillValues = list(range(1,32))
    random.shuffle(sigSkillValues)
    pmod["Modifications"].append({"Operation": "Set", "Key": "SigSkill1", "Value": sigSkillValues[0]})
    pmod["Modifications"].append({"Operation": "Set", "Key": "SigSkill2", "Value": sigSkillValues[1]})
    pmod["Modifications"].append({"Operation": "Set", "Key": "SigSkill3", "Value": sigSkillValues[2]})

    pmod["Modifications"].append({"Operation": "Set", "Key": "HeightIn", "Value": random.randrange(60,94)})

    potentialSpecialShots = []
    for shotList in LEGENDARY_SPECIAL_SHOTS.values():
        potentialSpecialShots += shotList
    specialShotChoice = random.choice(potentialSpecialShots)
    pmod["Modifications"].append({"Operation": "Set", "Key": "AShtForm", "Value": specialShotChoice["Shot Form"]})
    pmod["Modifications"].append({"Operation": "Set", "Key": "AShtBase", "Value": specialShotChoice["Shot Base"]})
    pmod["Description"] += f"**{specialShotChoice['Name']}** - {specialShotChoice['Description']}"


    # Return
    return pmod
neutral_godlike = [Neutral_Godlike_PhysicalizedBiases,Neutral_Godlike_ConcoctionJOE,Neutral_Godlike_RickAshes,
                   Neutral_Godlike_BrokenPromise,Neutral_Godlike_RussianRoulette,Neutral_Godlike_PesticideBeer,
                   Neutral_Godlike_ArcaneRemnants,Neutral_Godlike_SnehGambling,Neutral_Godlike_SHRINKRay,
                   Neutral_Godlike_JuicerBlacklist]

#endregion === Neutrals ===
#region === Slayers ===

def Slayer_Rare_CornbreadRapier(player):
    pmod = pmod_template.getPModTemplate()
    # Artifact Name
    pmod["Name"] = '''Ancient Rapier, Once Wielded by Sir Alfred Cornbread'''
    # Artifact Info
    pmod["Type"]["TypeName"] = "Artifact"
    pmod["Type"]["ArchetypeLock"] = "Slayer"
    pmod["Type"]["Rarity"] = "Rare"
    # Image Path
    pmod["Image"] = "ArtifactIcons\\CornbreadRapier.png"
    # Description
    pmod["Description"] = '''Delicate and light, this blade helped a legendary general cut down his enemies in the war of 1812. Add +30 to Vertical and Dunk. Subtract -5 from 3pt Shot.'''

    # Implementation
    pmod["Modifications"].append({"Operation": "Add", "Key": "SVertical", "Value": 30})
    pmod["Modifications"].append({"Operation": "Add", "Key": "SDunk", "Value": 30})
    pmod["Modifications"].append({"Operation": "Subtract", "Key": "SSht3PT", "Value": 5})


    # Return
    return pmod
def Slayer_Rare_WojciechMouse(player):
    pmod = pmod_template.getPModTemplate()
    # Artifact Name
    pmod["Name"] = '''Ancient Wired Mouse, Once Wielded by Wojciech Kois'''
    # Artifact Info
    pmod["Type"]["TypeName"] = "Artifact"
    pmod["Type"]["ArchetypeLock"] = "Slayer"
    pmod["Type"]["Rarity"] = "Rare"
    # Image Path
    pmod["Image"] = "ArtifactIcons\\AncientWiredMouse.png"
    # Description
    pmod["Description"] = '''Gaining a vision of a young man watching a very lethargic wizard of ancient times teach his craft, the player is inspired and changes:  Subtract -30 from Speed and Consistency. Add Microwave, Heat Retention, and Antifreeze.'''

    # Implementation
    pmod["Modifications"].append({"Operation": "Subtract", "Key": "SSpeed", "Value": 30})
    pmod["Modifications"].append({"Operation": "Subtract", "Key": "SConsis", "Value": 30})

    pmod["Modifications"].append({"Operation": "Set", "Key": "SigSkill1", "Value": "Microwave"})
    pmod["Modifications"].append({"Operation": "Set", "Key": "SigSkill2", "Value": "Heat Retention"})
    pmod["Modifications"].append({"Operation": "Set", "Key": "SigSkill3", "Value": "Anti-Freeze"})

    # Return
    return pmod
def Slayer_Rare_TimLaser(player):
    pmod = pmod_template.getPModTemplate()
    # Artifact Name
    pmod["Name"] = '''Ancient  Military-Grade Laser Pointer, Once Wielded by Tim Molkowski'''
    # Artifact Info
    pmod["Type"]["TypeName"] = "Artifact"
    pmod["Type"]["ArchetypeLock"] = "Slayer"
    pmod["Type"]["Rarity"] = "Rare"
    # Image Path
    pmod["Image"] = "ArtifactIcons\\AncientLaserPointer.png"
    # Description
    pmod["Description"] = '''Absolutely bewildered by the idea that a teenager once shined this light of lethal caliber directly into their eye, the player changes as follows: Add 3 inches to Height. -25 subtracted randomly across all accented primary stats.'''

    # Implementation
    pmod["Modifications"].append({"Operation": "Add", "Key": "HeightIn", "Value": 3})

    accentedPrimaryAttributes = []
    for primaryAttribute in player["Archetype"].primaryAttributes:
        if(primaryAttribute in player["Archetype"].accentedAttributes):
            accentedPrimaryAttributes.append(primaryAttribute)

    pointsToSpend = 25
    adjustedAttributes = {}
    while pointsToSpend > 0:
        randomAttribute = random.choice(accentedPrimaryAttributes)
        adjustedAttributes[randomAttribute] = adjustedAttributes.get(randomAttribute,0) + 1
        pointsToSpend -= 1

    for adjustedAttribute,adjustedValue in adjustedAttributes.items():
        pmod["Modifications"].append({"Operation": "Subtract", "Key": adjustedAttribute, "Value": adjustedValue})


    # Return
    return pmod
def Slayer_Rare_BartenderSword(player):
    pmod = pmod_template.getPModTemplate()
    # Artifact Name
    pmod["Name"] = '''Ancient All-Powerful-Immortality-Bringing Sword, Once Wielded by a 17 Year Old Bartender.'''
    # Artifact Info
    pmod["Type"]["TypeName"] = "Artifact"
    pmod["Type"]["ArchetypeLock"] = "Slayer"
    pmod["Type"]["Rarity"] = "Rare"
    # Image Path
    pmod["Image"] = "ArtifactIcons\\AncientShearcliffSword.png"
    # Description
    pmod["Description"] = '''Besides gaining the psychotic 3 consciences of Algemi and the disembodied voice of Christian Shearcliff all screaming at each other in their mind, the player also loses 3-4 inches in Height.  Add Spot up Shooter.'''

    # Implementation
    pmod["Modifications"].append({"Operation": "Subtract", "Key": "HeightIn", "Value": random.randrange(3,5)})
    pmod["Modifications"].append({"Operation": "Set", "Key": "SigSkill1", "Value": "Spot Up Shooter"})


    # Return
    return pmod
slayer_rare = [Slayer_Rare_CornbreadRapier,Slayer_Rare_WojciechMouse,Slayer_Rare_TimLaser,Slayer_Rare_BartenderSword]
def Slayer_Epic_SidCharger(player):
    pmod = pmod_template.getPModTemplate()
    # Artifact Name
    pmod["Name"] = '''Ancient iPhone Outlet Adapter, Used by Sidhant Mehta to Flirt with Women'''
    # Artifact Info
    pmod["Type"]["TypeName"] = "Artifact"
    pmod["Type"]["ArchetypeLock"] = "Slayer"
    pmod["Type"]["Rarity"] = "Epic"
    # Image Path
    pmod["Image"] = "ArtifactIcons\\SidChargingCord.png"
    # Description
    pmod["Description"] = '''While being entirely unsuccessful in the romance game, this artifact does add a rare or epic Engineer special shot:\n\n'''

    # Implementation
    potentialSpecialShots = RARE_SPECIAL_SHOTS["Slayer"] + EPIC_SPECIAL_SHOTS["Slayer"]
    specialShotChoice = random.choice(potentialSpecialShots)
    pmod["Modifications"].append({"Operation": "Set", "Key": "AShtForm", "Value": specialShotChoice["Shot Form"]})
    pmod["Modifications"].append({"Operation": "Set", "Key": "AShtBase", "Value": specialShotChoice["Shot Base"]})
    pmod["Description"] += f"**{specialShotChoice['Name']}** - {specialShotChoice['Description']}"


    # Return
    return pmod
def Slayer_Epic_DiamondBoots(player):
    pmod = pmod_template.getPModTemplate()
    # Artifact Name
    pmod["Name"] = '''Ancient Pair of Diamond Boots, Summoned from the Heavens by a Member of the Illuminati'''
    # Artifact Info
    pmod["Type"]["TypeName"] = "Artifact"
    pmod["Type"]["ArchetypeLock"] = "Slayer"
    pmod["Type"]["Rarity"] = "Epic"
    # Image Path
    pmod["Image"] = "ArtifactIcons\\DiamondBoots.png"
    # Description
    pmod["Description"] = '''Knowing full and well that Danny cheated, the player feels justified that they have these boots of retribution. Add +7 to non-accented Primary Skills. Spot up tendencies will be set to almost always have the player post up in the paint.'''

    # Implementation
    for primaryAttribute in player["Archetype"].primaryAttributes:
        if(primaryAttribute in player["Archetype"].unaccentedAttributes):
            pmod["Modifications"].append({"Operation": "Add", "Key": primaryAttribute, "Value": 7})

    pmod["Modifications"].append({"Operation": "Set", "Key": "TSpotUp", "Value": 10})
    pmod["Modifications"].append({"Operation": "Set", "Key": "TPostUp", "Value": 90})


    # Return
    return pmod
def Slayer_Epic_BidenCoffee(player):
    pmod = pmod_template.getPModTemplate()
    # Artifact Name
    pmod["Name"] = '''Ancient Cup of Coffee, Once Wielded by Joe Biden 5 Minutes Ago'''
    # Artifact Info
    pmod["Type"]["TypeName"] = "Artifact"
    pmod["Type"]["ArchetypeLock"] = "Slayer"
    pmod["Type"]["Rarity"] = "Epic"
    # Image Path
    pmod["Image"] = "ArtifactIcons\\JoeCoffee.png"
    # Description
    pmod["Description"] = '''Feeling a bit concerned that Joe Biden just referred to his steaming cup of coffee as an ancient mayan artifact, the player changes as follows: Add 30 to Dunk, Standing Dunk, and Vertical. Subtract 5 from all accented primary stats. Add Posterizer and Finisher. Add 3 cool dunk packages.'''

    # Implementation
    pmod["Modifications"].append({"Operation": "Add", "Key": "SDunk", "Value": 30})
    pmod["Modifications"].append({"Operation": "Add", "Key": "SStdDunk", "Value": 30})
    pmod["Modifications"].append({"Operation": "Add", "Key": "SVertical", "Value": 30})
    
    pmod["Modifications"].append({"Operation": "Set", "Key": "SigSkill1", "Value": "Posterizer"})
    pmod["Modifications"].append({"Operation": "Set", "Key": "SigSkill2", "Value": "Finisher"})

    for primaryAttribute in player["Archetype"].primaryAttributes:
        if(primaryAttribute in player["Archetype"].accentedAttributes):
            pmod["Modifications"].append({"Operation": "Subtract", "Key": primaryAttribute, "Value": 5})

    coolDunks = [23,24,25,26,27,28,35,51,55,63,64,65]
    dunk1 = random.choice(coolDunks)
    coolDunks.remove(dunk1)
    dunk2 = random.choice(coolDunks)
    coolDunks.remove(dunk2)
    dunk3 = random.choice(coolDunks)

    pmod["Modifications"].append({"Operation": "Set", "Key": "AGoToDunk", "Value": dunk1})
    pmod["Modifications"].append({"Operation": "Set", "Key": "ADunk2", "Value": dunk2})
    pmod["Modifications"].append({"Operation": "Set", "Key": "ADunk3", "Value": dunk3})



    # Return
    return pmod
def Slayer_Epic_IlluminatiPizza(player):
    pmod = pmod_template.getPModTemplate()
    # Artifact Name
    pmod["Name"] = '''Ancient Slice of Pizza, Once Widely Considered a Token of  Illuminati Membership.'''
    # Artifact Info
    pmod["Type"]["TypeName"] = "Artifact"
    pmod["Type"]["ArchetypeLock"] = "Slayer"
    pmod["Type"]["Rarity"] = "Epic"
    # Image Path
    pmod["Image"] = "ArtifactIcons\\IlluminatiPizza.png"
    # Description
    pmod["Description"] = '''Ah, a member I see. The player joins the illuminati and changes in the following fashion: Set Offensive and Defensive awareness to 99. Add 20 to Pass. Add Dimer, Post Playmaker, Alley-ooper, and Ankle Breaker. -12 to 3Pt.'''

    # Implementation
    pmod["Modifications"].append({"Operation": "Set", "Key": "SOAwar", "Value": 99})
    pmod["Modifications"].append({"Operation": "Set", "Key": "SDAwar", "Value": 99})

    pmod["Modifications"].append({"Operation": "Add", "Key": "SPass", "Value": 20})

    pmod["Modifications"].append({"Operation": "Set", "Key": "SigSkill1", "Value": "Dimer"})
    pmod["Modifications"].append({"Operation": "Set", "Key": "SigSkill2", "Value": "Post Playmaker"})
    pmod["Modifications"].append({"Operation": "Set", "Key": "SigSkill3", "Value": "Alley Oopers"})
    pmod["Modifications"].append({"Operation": "Set", "Key": "SigSkill4", "Value": "Ankle Breaker"})

    pmod["Modifications"].append({"Operation": "Subtract", "Key": "SSht3PT", "Value": 12})


    # Return
    return pmod
slayer_epic = [Slayer_Epic_SidCharger,Slayer_Epic_DiamondBoots,Slayer_Epic_BidenCoffee,Slayer_Epic_IlluminatiPizza]
def Slayer_Legendary_RuizAspirations(player):
    pmod = pmod_template.getPModTemplate()
    # Artifact Name
    pmod["Name"] = '''A Bottle of David Ruiz's Aspirations'''
    # Artifact Info
    pmod["Type"]["TypeName"] = "Artifact"
    pmod["Type"]["ArchetypeLock"] = "Slayer"
    pmod["Type"]["Rarity"] = "Legendary"
    # Image Path
    pmod["Image"] = "ArtifactIcons\\RuizAspirations.png"
    # Description
    pmod[
        "Description"] = '''David always wanted to be Kobe Bryant, and the player makes the leap where David could not and turns from a soft-spoken Mexican man to a basketball overlord. Set the Shot Form and Base to Kobe Bryant's. Set Shot Form and Shot Base to Kobe Bryant's.  Add 20 to Off Hand Dribbling, Ball Handling, and Vertical. Set all tertiary stats, Passing, and Hustle to 25. -30 to passing. Add Acrobat, Ankle Breaker, and Microwave.'''

    # Implementation
    for tertiaryAttribute in player["Archetype"].tertiaryAttributes:
        pmod["Modifications"].append({"Operation": "Set", "Key": tertiaryAttribute, "Value": 25})
    pmod["Modifications"].append({"Operation": "Set", "Key": "SPass", "Value": 25})
    pmod["Modifications"].append({"Operation": "Set", "Key": "SHustle", "Value": 25})

    pmod["Modifications"].append({"Operation": "Add", "Key": "SOffHDrib", "Value": 20})
    pmod["Modifications"].append({"Operation": "Add", "Key": "SVertical", "Value": 20})
    pmod["Modifications"].append({"Operation": "Add", "Key": "SBallHndl", "Value": 20})


    pmod["Modifications"].append({"Operation": "Set", "Key": "SigSkill1", "Value": "Acrobat"})
    pmod["Modifications"].append({"Operation": "Set", "Key": "SigSkill2", "Value": "Ankle Breaker"})
    pmod["Modifications"].append({"Operation": "Set", "Key": "SigSkill3", "Value": "Microwave"})

    pmod["Modifications"].append({"Operation": "Set", "Key": "AShtForm", "Value": 93})
    pmod["Modifications"].append({"Operation": "Set", "Key": "AShtBase", "Value": 71})

    # Return
    return pmod
def Slayer_Legendary_SpriteBottle(player):
    pmod = pmod_template.getPModTemplate()
    # Artifact Name
    pmod["Name"] = '''A Cold and Refreshing Bottle of Sprite'''
    # Artifact Info
    pmod["Type"]["TypeName"] = "Artifact"
    pmod["Type"]["ArchetypeLock"] = "Slayer"
    pmod["Type"]["Rarity"] = "Legendary"
    # Image Path
    pmod["Image"] = "ArtifactIcons\\Sprite.png"
    # Description
    pmod[
        "Description"] = '''The player realizes that it is Sprite Time and it is Game Time. Set all Signature Skills to Lebron James's.  Add Finisher. -5 to all accented primary stats, add 10 to all non-accented primary stats. Add 40 to dunk.'''

    # Implementation
    for primaryAttribute in player["Archetype"].primaryAttributes:
        if(primaryAttribute in player["Archetype"].accentedAttributes):
            pmod["Modifications"].append({"Operation": "Subtract", "Key": primaryAttribute, "Value": 5})
        else:
            pmod["Modifications"].append({"Operation": "Add", "Key": primaryAttribute, "Value": 10})
    pmod["Modifications"].append({"Operation": "Add", "Key": "SDunk", "Value": 40})
    pmod["Modifications"].append({"Operation": "Set", "Key": "SigSkill1", "Value": "Finisher"})


    pmod["Modifications"].append({"Operation": "Set", "Key": "AFadeaway", "Value": 21})
    pmod["Modifications"].append({"Operation": "Set", "Key": "AContestd", "Value": 0})
    pmod["Modifications"].append({"Operation": "Set", "Key": "AEscDrPlU", "Value": 0})
    pmod["Modifications"].append({"Operation": "Set", "Key": "ARunner", "Value": 15})
    pmod["Modifications"].append({"Operation": "Set", "Key": "AFreeT", "Value": 67})
    pmod["Modifications"].append({"Operation": "Set", "Key": "ADrPullUp", "Value": 9})
    pmod["Modifications"].append({"Operation": "Set", "Key": "ASpinJmpr", "Value": 2})
    pmod["Modifications"].append({"Operation": "Set", "Key": "AHopJmpr", "Value": 10})
    pmod["Modifications"].append({"Operation": "Set", "Key": "APstFade", "Value": 5})
    pmod["Modifications"].append({"Operation": "Set", "Key": "APstHook", "Value": 1})
    pmod["Modifications"].append({"Operation": "Set", "Key": "APstHopSh", "Value": 7})
    pmod["Modifications"].append({"Operation": "Set", "Key": "APstShmSh", "Value": 0})
    pmod["Modifications"].append({"Operation": "Set", "Key": "APstDrvStB", "Value": 3})
    pmod["Modifications"].append({"Operation": "Set", "Key": "APstSpnStB", "Value": 3})
    pmod["Modifications"].append({"Operation": "Set", "Key": "APstPrtct", "Value": 0})
    pmod["Modifications"].append({"Operation": "Set", "Key": "APstPrtSpn", "Value": 2})
    pmod["Modifications"].append({"Operation": "Set", "Key": "AIsoCross", "Value": 5})
    pmod["Modifications"].append({"Operation": "Set", "Key": "AIsoBhBck", "Value": 1})
    pmod["Modifications"].append({"Operation": "Set", "Key": "AIsoSpin", "Value": 5})
    pmod["Modifications"].append({"Operation": "Set", "Key": "AIsoHesit", "Value": 1})
    pmod["Modifications"].append({"Operation": "Set", "Key": "ALayUp", "Value": 0})
    pmod["Modifications"].append({"Operation": "Set", "Key": "AGoToDunk", "Value": 21})
    pmod["Modifications"].append({"Operation": "Set", "Key": "ADunk2", "Value": 13})
    pmod["Modifications"].append({"Operation": "Set", "Key": "ADunk3", "Value": 22})
    pmod["Modifications"].append({"Operation": "Set", "Key": "ADunk4", "Value": 26})
    pmod["Modifications"].append({"Operation": "Set", "Key": "ADunk5", "Value": 29})
    pmod["Modifications"].append({"Operation": "Set", "Key": "ADunk6", "Value": 33})
    pmod["Modifications"].append({"Operation": "Set", "Key": "ADunk7", "Value": 50})
    pmod["Modifications"].append({"Operation": "Set", "Key": "ADunk8", "Value": 62})
    pmod["Modifications"].append({"Operation": "Set", "Key": "ADunk9", "Value": 45})
    pmod["Modifications"].append({"Operation": "Set", "Key": "ADunk10", "Value": 40})
    pmod["Modifications"].append({"Operation": "Set", "Key": "ADunk11", "Value": 60})
    pmod["Modifications"].append({"Operation": "Set", "Key": "ADunk12", "Value": 61})
    pmod["Modifications"].append({"Operation": "Set", "Key": "ADunk13", "Value": 2})

    # Return
    return pmod
def Slayer_Legendary_DagobahVision(player):
    pmod = pmod_template.getPModTemplate()
    # Artifact Name
    pmod["Name"] = '''A Vision from a Space Monk, with Instructions to Seek Out Some Planet called 'Dagobah\''''
    # Artifact Info
    pmod["Type"]["TypeName"] = "Artifact"
    pmod["Type"]["ArchetypeLock"] = "Slayer"
    pmod["Type"]["Rarity"] = "Legendary"
    # Image Path
    pmod["Image"] = "ArtifactIcons\\Dagobah.png"
    # Description
    pmod[
        "Description"] = '''The player visits Dagobah and morphs into a slimy alien midget who can move random objects with his mind. Height is set between 4'0 and 4'6. +10 to Shot 3pt, Speed, and Quickness. Vertical and Strength are set to 99. -40 to Steal and Block. Get an epic or legendary special shot:\n\n'''

    # Implementation
    pmod["Modifications"].append({"Operation": "Add", "Key": "SSht3PT", "Value": 10})
    pmod["Modifications"].append({"Operation": "Add", "Key": "SSpeed", "Value": 10})
    pmod["Modifications"].append({"Operation": "Add", "Key": "SQuick", "Value": 10})

    pmod["Modifications"].append({"Operation": "Subtract", "Key": "SSteal", "Value": 40})
    pmod["Modifications"].append({"Operation": "Subtract", "Key": "SBlock", "Value": 40})

    pmod["Modifications"].append({"Operation": "Set", "Key": "SVertical", "Value": 99})
    pmod["Modifications"].append({"Operation": "Set", "Key": "SStrength", "Value": 99})

    pmod["Modifications"].append({"Operation": "Set", "Key": "HeightIn", "Value": random.randrange(48,55)})

    potentialSpecialShots = LEGENDARY_SPECIAL_SHOTS["Slayer"] + EPIC_SPECIAL_SHOTS["Slayer"]
    specialShotChoice = random.choice(potentialSpecialShots)
    pmod["Modifications"].append({"Operation": "Set", "Key": "AShtForm", "Value": specialShotChoice["Shot Form"]})
    pmod["Modifications"].append({"Operation": "Set", "Key": "AShtBase", "Value": specialShotChoice["Shot Base"]})
    pmod["Description"] += f"**{specialShotChoice['Name']}** - {specialShotChoice['Description']}"


    # Return
    return pmod
slayer_legendary = [Slayer_Legendary_RuizAspirations,Slayer_Legendary_SpriteBottle,Slayer_Legendary_DagobahVision]

#endregion === Slayers ===
#region === Vigilante ===

def Vigilante_Rare_NancyEmail(player):
    pmod = pmod_template.getPModTemplate()
    # Artifact Name
    pmod["Name"] = '''A Nasty Email from Nancy Soleto'''
    # Artifact Info
    pmod["Type"]["TypeName"] = "Artifact"
    pmod["Type"]["ArchetypeLock"] = "Vigilante"
    pmod["Type"]["Rarity"] = "Rare"
    # Image Path
    pmod["Image"] = "ArtifactIcons\\NancyEmail.png"
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
def Vigilante_Rare_ChapApology(player):
    pmod = pmod_template.getPModTemplate()
    # Artifact Name
    pmod["Name"] = '''A Written Apology from Chap'''
    # Artifact Info
    pmod["Type"]["TypeName"] = "Artifact"
    pmod["Type"]["ArchetypeLock"] = "Vigilante"
    pmod["Type"]["Rarity"] = "Rare"
    # Image Path
    pmod["Image"] = "ArtifactIcons\\ChapApology.png"
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
def Vigilante_Rare_NatHound(player):
    pmod = pmod_template.getPModTemplate()
    # Artifact Name
    pmod["Name"] = '''Nat's Vicious, Bloodthirsty Hound from Hell'''
    # Artifact Info
    pmod["Type"]["TypeName"] = "Artifact"
    pmod["Type"]["ArchetypeLock"] = "Vigilante"
    pmod["Type"]["Rarity"] = "Rare"
    # Image Path
    pmod["Image"] = "ArtifactIcons\\NatHound.png"
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
def Vigilante_Rare_RumoroShrug(player):
    pmod = pmod_template.getPModTemplate()
    # Artifact Name
    pmod["Name"] = '''A Smile and a Shrug from Nick Rumoro'''
    # Artifact Info
    pmod["Type"]["TypeName"] = "Artifact"
    pmod["Type"]["ArchetypeLock"] = "Vigilante"
    pmod["Type"]["Rarity"] = "Rare"
    # Image Path
    pmod["Image"] = "ArtifactIcons\\RumoroSmileShrug.png"
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
vigilante_rare = [Vigilante_Rare_NancyEmail,Vigilante_Rare_ChapApology,Vigilante_Rare_NatHound,
                  Vigilante_Rare_RumoroShrug]
def Vigilante_Epic_FernNo(player):
    pmod = pmod_template.getPModTemplate()
    # Artifact Name
    pmod["Name"] = '''A 'No.' from Fernando Valencia, After Being Asked to Accept the Transfer of a User He's Been Working With'''
    # Artifact Info
    pmod["Type"]["TypeName"] = "Artifact"
    pmod["Type"]["ArchetypeLock"] = "Vigilante"
    pmod["Type"]["Rarity"] = "Epic"
    # Image Path
    pmod["Image"] = "ArtifactIcons\\FernandoNo.png"
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
def Vigilante_Epic_DrewGall(player):
    pmod = pmod_template.getPModTemplate()
    # Artifact Name
    pmod["Name"] = '''The Gall of Drew Meier'''
    # Artifact Info
    pmod["Type"]["TypeName"] = "Artifact"
    pmod["Type"]["ArchetypeLock"] = "Vigilante"
    pmod["Type"]["Rarity"] = "Epic"
    # Image Path
    pmod["Image"] = "ArtifactIcons\\DrewGall.png"
    # Description
    pmod["Description"] = '''Feeling enraged by the absolute nerve of fellow coworker Drew Meier passing his 9th call of the day, the player spitefully changes as follows: Set Passing and Quickness to 99.  Add Dimer and Alley-Ooper. -7-10 to all accented primary stats. '''

    # Implementation
    pmod["Modifications"].append({"Operation": "Set", "Key": "SPass", "Value": 99})
    pmod["Modifications"].append({"Operation": "Set", "Key": "SQuick", "Value": 99})

    for primaryAttribute in player["Archetype"].primaryAttributes:
        if(primaryAttribute in player["Archetype"].accentedAttributes):
            pmod["Modifications"].append({"Operation": "Subtract", "Key": primaryAttribute, "Value": random.randrange(7,11)})

    pmod["Modifications"].append({"Operation": "Set", "Key": "SigSkill1", "Value": "Dimer"})
    pmod["Modifications"].append({"Operation": "Set", "Key": "SigSkill2", "Value": "Alley Oopers"})

    # Return
    return pmod
def Vigilante_Epic_ChandaraCandor(player):
    pmod = pmod_template.getPModTemplate()
    # Artifact Name
    pmod["Name"] = '''The Quiet and Friendly Candor of Chandara Cheng'''
    # Artifact Info
    pmod["Type"]["TypeName"] = "Artifact"
    pmod["Type"]["ArchetypeLock"] = "Vigilante"
    pmod["Type"]["Rarity"] = "Epic"
    # Image Path
    pmod["Image"] = "ArtifactIcons\\ChandaraCandor.png"
    # Description
    pmod["Description"] = '''Feeling at peace from the soothing and rhythmic tones of Mr. Cheng, the player is changed as follows: Add 10 to all accented primary attributes. Add 10 to all tertiary stats. Subtract 20 from all non-accented attributes. Add 30 to Strength.'''

    # Implementation
    for attribute in archetypes.ALL_ATTRIBUTES:
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
def Vigilante_Epic_EddieTHanks(player):
    pmod = pmod_template.getPModTemplate()
    # Artifact Name
    pmod["Name"] = '''Eddie Smith's Memoir, 'THanks for Nothing\''''
    # Artifact Info
    pmod["Type"]["TypeName"] = "Artifact"
    pmod["Type"]["ArchetypeLock"] = "Vigilante"
    pmod["Type"]["Rarity"] = "Epic"
    # Image Path
    pmod["Image"] = "ArtifactIcons\\EddieMemoir.png"
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
vigilante_epic = [Vigilante_Epic_FernNo,Vigilante_Epic_DrewGall,Vigilante_Epic_ChandaraCandor,
                  Vigilante_Epic_EddieTHanks]
def Vigilante_Legendary_TrumpChina(player):
    pmod = pmod_template.getPModTemplate()
    # Artifact Name
    pmod["Name"] = '''Artistic Interpretation of Donald Trump's Relationship with China'''
    # Artifact Info
    pmod["Type"]["TypeName"] = "Artifact"
    pmod["Type"]["ArchetypeLock"] = "Vigilante"
    pmod["Type"]["Rarity"] = "Legendary"
    # Image Path
    pmod["Image"] = "ArtifactIcons\\TrumpAndChina.png"
    # Description
    pmod["Description"] = '''It's very big and beautiful, the greatest art. I do have to say it is really great. Set height between 7'3-7'8. Set Vertical to 25, and all secondary stats randomized between 25-40. Add Finisher and Deadeye skills.'''

    # Implementation
    pmod["Modifications"].append({"Operation": "Set", "Key": "HeightIn", "Value": random.randrange(87,93)})
    pmod["Modifications"].append({"Operation": "Set", "Key": "SVertical", "Value": 25})

    for secondaryAttribute in player["Archetype"].secondaryAttributes:
        pmod["Modifications"].append({"Operation": "Set", "Key": secondaryAttribute, "Value": random.randrange(25,41)})
    
    pmod["Modifications"].append({"Operation": "Set", "Key": "SigSkill1", "Value": "Finisher"})
    pmod["Modifications"].append({"Operation": "Set", "Key": "SigSkill2", "Value": "Deadeye"})



    # Return
    return pmod
def Vigilante_Legendary_DickScorecard(player):
    pmod = pmod_template.getPModTemplate()
    # Artifact Name
    pmod["Name"] = '''An Antique Scorecard of the S1 League Championship Game, Signed "A Fine Effort from an Extraordinary Team" by Charles Dick'''
    # Artifact Info
    pmod["Type"]["TypeName"] = "Artifact"
    pmod["Type"]["ArchetypeLock"] = "Vigilante"
    pmod["Type"]["Rarity"] = "Legendary"
    # Image Path
    pmod["Image"] = "ArtifactIcons\\DickScorecard.png"
    # Description
    pmod[
        "Description"] = '''Shedding a tear at such a beautiful piece of 2k history, the player is reformed in the following fashion: Subtract 250 points randomly distributed between all stats. Add Microwave, Deadeye, Spot-up Shooter, Shot Creator, and War General.  Get an epic or legendary special shot:\n\n'''

    # Implementation
    pointsToSpend = 250
    adjustedAttributes = {}
    while pointsToSpend > 0:
        randomAttribute = random.choice(archetypes.ALL_ATTRIBUTES)
        adjustedAttributes[randomAttribute] = adjustedAttributes.get(randomAttribute,0) + 1
        pointsToSpend -= 1
    for adjustedAttribute,value in adjustedAttributes.items():
        pmod["Modifications"].append({"Operation": "Subtract", "Key": adjustedAttribute, "Value": value})


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
def Vigilante_Legendary_EggrollVoucher(player):
    pmod = pmod_template.getPModTemplate()
    # Artifact Name
    pmod["Name"] = '''Voucher Reading '25 percnt of Next Spicy at Eggrol r We', Gloriously Lacking an Expiration Date'''
    # Artifact Info
    pmod["Type"]["TypeName"] = "Artifact"
    pmod["Type"]["ArchetypeLock"] = "Vigilante"
    pmod["Type"]["Rarity"] = "Legendary"
    # Image Path
    pmod["Image"] = "ArtifactIcons\\EggrollCoupon.png"
    # Description
    pmod["Description"] = '''Visit Eggrolls R We 2-7 times. For each time you visit, -1-3 to all attributes, and make another random zone Hot. If the same zone is selected twice, it becomes Burning.\n\n'''

    # Implementation
    eggrollVisits = random.randrange(2,8)

    for attribute in archetypes.ALL_ATTRIBUTES:
        pmod["Modifications"].append({"Operation": "Subtract", "Key": attribute, "Value": eggrollVisits * random.randrange(1,4)})

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
vigilante_legendary = [Vigilante_Legendary_TrumpChina,Vigilante_Legendary_DickScorecard,
                       Vigilante_Legendary_EggrollVoucher]

#endregion === Vigilante ===
#region === Medics ===

def Medic_Rare_SubwayGiftcard(player):
    pmod = pmod_template.getPModTemplate()
    # Artifact Name
    pmod["Name"] = '''$10 Subway Gift Card, 8 years expired.'''
    # Artifact Info
    pmod["Type"]["TypeName"] = "Artifact"
    pmod["Type"]["ArchetypeLock"] = "Medic"
    pmod["Type"]["Rarity"] = "Rare"
    # Image Path
    pmod["Image"] = "ArtifactIcons\\ExpiredSubwayGiftCard.png"
    # Description
    pmod["Description"] = '''Not enough to buy a 6 inch steak and cheese sandwich, but just enough to buy a miniature pizza. Add +5 to Offensive, Defensive Rebound, and Vertical. -5 to all accented Secondary Stats. Add Break Starter.'''

    # Implementation
    pmod["Modifications"].append({"Operation" : "Add", "Key" : "SDReb", "Value" : 5})
    pmod["Modifications"].append({"Operation" : "Add", "Key" : "SOReb", "Value" : 5})
    pmod["Modifications"].append({"Operation" : "Add", "Key" : "SVertical", "Value" : 5})
    for secondaryAttribute in player["Archetype"].secondaryAttributes:
        if(secondaryAttribute in player["Archetype"].accentedAttributes):
            pmod["Modifications"].append({"Operation": "Subtract", "Key": secondaryAttribute, "Value": 5})

    pmod["Modifications"].append({"Operation" : "Set", "Key" : "SigSkill1", "Value" : "Break Starter"})

    # Return
    return pmod
def Medic_Rare_WrapApron(player):
    pmod = pmod_template.getPModTemplate()
    # Artifact Name
    pmod["Name"] = ''''This is How You Wrap' Apron'''
    # Artifact Info
    pmod["Type"]["TypeName"] = "Artifact"
    pmod["Type"]["ArchetypeLock"] = "Medic"
    pmod["Type"]["Rarity"] = "Rare"
    # Image Path
    pmod["Image"] = "ArtifactIcons\\WrapApron.png"
    # Description
    pmod["Description"] = '''Stylish and groovy, this will surely make the player fit in with the cool crowd. Add +5 to all accented Secondary Stats. -5 to Offensive, Defensive Rebound, and Vertical. Add Post Playmaker.'''

    # Implementation
    pmod["Modifications"].append({"Operation" : "Subtract", "Key" : "SDReb", "Value" : 5})
    pmod["Modifications"].append({"Operation" : "Subtract", "Key" : "SOReb", "Value" : 5})
    pmod["Modifications"].append({"Operation" : "Subtract", "Key" : "SVertical", "Value" : 5})
    for secondaryAttribute in player["Archetype"].secondaryAttributes:
        if(secondaryAttribute in player["Archetype"].accentedAttributes):
            pmod["Modifications"].append({"Operation": "Add", "Key": secondaryAttribute, "Value": 5})

    pmod["Modifications"].append({"Operation" : "Set", "Key" : "SigSkill1", "Value" : "Post Playmaker"})

    # Return
    return pmod
def Medic_Rare_Jardeenya(player):
    pmod = pmod_template.getPModTemplate()
    # Artifact Name
    pmod["Name"] = '''An Audio Recording of a Customer Inquiring: 'Can I have the uh JARDEENYA peppas?\''''
    # Artifact Info
    pmod["Type"]["TypeName"] = "Artifact"
    pmod["Type"]["ArchetypeLock"] = "Medic"
    pmod["Type"]["Rarity"] = "Rare"
    # Image Path
    pmod["Image"] = "ArtifactIcons\\Giardiniera.png"
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
def Medic_Rare_HoneyOat(player):
    pmod = pmod_template.getPModTemplate()
    # Artifact Name
    pmod["Name"] = '''Newspaper Cutout Advertising the Honey Oat Bread from 2009'''
    # Artifact Info
    pmod["Type"]["TypeName"] = "Artifact"
    pmod["Type"]["ArchetypeLock"] = "Medic"
    pmod["Type"]["Rarity"] = "Rare"
    # Image Path
    pmod["Image"] = "ArtifactIcons\\HoneyOatBread.png"
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
medic_rare = [Medic_Rare_SubwayGiftcard,Medic_Rare_WrapApron,Medic_Rare_Jardeenya,Medic_Rare_HoneyOat]
def Medic_Epic_VileSauces(player):
    pmod = pmod_template.getPModTemplate()
    # Artifact Name
    pmod["Name"] = '''A Plastic Bin Filled with a Vile Mixure of Spilled Sauces'''
    # Artifact Info
    pmod["Type"]["TypeName"] = "Artifact"
    pmod["Type"]["ArchetypeLock"] = "Medic"
    pmod["Type"]["Rarity"] = "Epic"
    # Image Path
    pmod["Image"] = "ArtifactIcons\\SauceBin.png"
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
def Medic_Epic_CaptionedPhoto(player):
    pmod = pmod_template.getPModTemplate()
    # Artifact Name
    pmod["Name"] = '''A Circled, Highlighted, and Captioned Photo of a Single Olive on the Floor of a Subway Restaurant'''
    # Artifact Info
    pmod["Type"]["TypeName"] = "Artifact"
    pmod["Type"]["ArchetypeLock"] = "Medic"
    pmod["Type"]["Rarity"] = "Epic"
    # Image Path
    pmod["Image"] = "ArtifactIcons\\OlivePhoto.png"
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
def Medic_Epic_SpotlessGloves(player):
    pmod = pmod_template.getPModTemplate()
    # Artifact Name
    pmod["Name"] = '''Spotlessly Clean Gloves, demanded to be removed 15 seconds after they were acquired.'''
    # Artifact Info
    pmod["Type"]["TypeName"] = "Artifact"
    pmod["Type"]["ArchetypeLock"] = "Medic"
    pmod["Type"]["Rarity"] = "Epic"
    # Image Path
    pmod["Image"] = "ArtifactIcons\\SubwayGloves.png"
    # Description
    pmod["Description"] = '''Feeling depressed that these beautiful gloves had to go to waste because of an obnoxious, power-hungry sewer mutant of a human being, the player changes as follows: Add 40 to Pass and Hands. -15 to all accented Secondary stats. Add Dimer, Break Starter, and Scrapper.'''

    # Implementation
    for unaccentedAttribute in player["Archetype"].unaccentedAttributes:
        if(unaccentedAttribute in player["Archetype"].secondaryAttributes):
            pmod["Modifications"].append({"Operation": "Subtract", "Key": unaccentedAttribute, "Value": 15})

    pmod["Modifications"].append({"Operation": "Add", "Key": "SPass", "Value": 40})
    pmod["Modifications"].append({"Operation": "Add", "Key": "SHands", "Value": 40})

    pmod["Modifications"].append({"Operation": "Set", "Key": "SigSkill1", "Value": "Dimer"})
    pmod["Modifications"].append({"Operation": "Set", "Key": "SigSkill2", "Value": "Break Starter"})
    pmod["Modifications"].append({"Operation": "Set", "Key": "SigSkill3", "Value": "Scrapper"})



    # Return
    return pmod
def Medic_Epic_CCTVFootage(player):
    pmod = pmod_template.getPModTemplate()
    # Artifact Name
    pmod["Name"] = '''CCTV Footage of a Car Banging a U-Turn on the Road Adjacent to Subway'''
    # Artifact Info
    pmod["Type"]["TypeName"] = "Artifact"
    pmod["Type"]["ArchetypeLock"] = "Medic"
    pmod["Type"]["Rarity"] = "Epic"
    # Image Path
    pmod["Image"] = "ArtifactIcons\\CCTVSubway.png"
    # Description
    pmod["Description"] = '''Yep, brace for the dreaded beep. The player changes while bracing for the drive-thru customer in the following way: Add +10 to accented Primary Skills. +15-25 to 3pt shot. Spot up tendencies/hotspots will be set to almost always have the player post up for 3s. Add Alley-ooper and Deadeye.'''

    # Implementation
    for accentedAttribute in player["Archetype"].accentedAttributes:
        if(accentedAttribute in player["Archetype"].primaryAttributes):
            pmod["Modifications"].append({"Operation": "Subtract", "Key": accentedAttribute, "Value": 10})

    pmod["Modifications"].append({"Operation": "Set", "Key": "SSht3PT", "Value": random.randrange(15, 26)})

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
medic_epic = [Medic_Epic_VileSauces,Medic_Epic_CaptionedPhoto,Medic_Epic_SpotlessGloves,Medic_Epic_CCTVFootage]
def Medic_Legendary_CompressOMatic(player):
    pmod = pmod_template.getPModTemplate()
    # Artifact Name
    pmod["Name"] = '''The Compress-O-Matic, invented by Fredwardo Jalapeno'''
    # Artifact Info
    pmod["Type"]["TypeName"] = "Artifact"
    pmod["Type"]["ArchetypeLock"] = "Medic"
    pmod["Type"]["Rarity"] = "Legendary"
    # Image Path
    pmod["Image"] = "ArtifactIcons\\CompressOMatic.png"
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
def Medic_Legendary_RancidStrawberry(player):
    pmod = pmod_template.getPModTemplate()
    # Artifact Name
    pmod["Name"] = '''A Rancid Strawberry'''
    # Artifact Info
    pmod["Type"]["TypeName"] = "Artifact"
    pmod["Type"]["ArchetypeLock"] = "Medic"
    pmod["Type"]["Rarity"] = "Legendary"
    # Image Path
    pmod["Image"] = "ArtifactIcons\\RancidStrawberry.png"
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
def Medic_Legendary_GreasyIPhone(player):
    pmod = pmod_template.getPModTemplate()
    # Artifact Name
    pmod["Name"] = '''A Greasy, Cracked iPhone 5 Left on the Basketball Court by the Annoying 11 Year Old Kid Who Completely Ruined the Game for Everyone Else'''
    # Artifact Info
    pmod["Type"]["TypeName"] = "Artifact"
    pmod["Type"]["ArchetypeLock"] = "Medic"
    pmod["Type"]["Rarity"] = "Legendary"
    # Image Path
    pmod["Image"] = "ArtifactIcons\\GreasyCrackediPhone.png"
    # Description
    pmod["Description"] = '''Feeling unbelievably annoyed at the audacity of the young child, the player changes as follows: Steal, Hustle, Block, Emotion, and Offensive Rebound are set to 99. -20 to all other Primary and Secondary Stats. Make all Hotspots and Freelance Tendencies equal (by their category). Add Pickpocket, Scrapper, Chasedown Artist, Active Hands, and Highlight Film.'''

    # Implementation
    pmod["Modifications"].append({"Operation": "Set", "Key": "SSteal", "Value": 99})
    pmod["Modifications"].append({"Operation": "Set", "Key": "SHustle", "Value": 99})
    pmod["Modifications"].append({"Operation": "Set", "Key": "SBlock", "Value": 99})
    pmod["Modifications"].append({"Operation": "Set", "Key": "SEmotion", "Value": 99})
    pmod["Modifications"].append({"Operation": "Set", "Key": "SOReb", "Value": 99})

    otherAttributes = player["Archetype"].primaryAttributes.copy() + player["Archetype"].secondaryAttributes.copy()
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
medic_legendary = [Medic_Legendary_CompressOMatic,Medic_Legendary_RancidStrawberry,Medic_Legendary_GreasyIPhone]

#endregion === Medics ===
#region === Guardians ===

def Guardian_Rare_CornpopRazor(player):
    pmod = pmod_template.getPModTemplate()
    # Artifact Name
    pmod["Name"] = '''Cornpop's Razor Blade, stained with the blood of Joe Biden'''
    # Artifact Info
    pmod["Type"]["TypeName"] = "Artifact"
    pmod["Type"]["ArchetypeLock"] = "Guardian"
    pmod["Type"]["Rarity"] = "Rare"
    # Image Path
    pmod["Image"] = "ArtifactIcons\\StainedRazorBlade.png"
    # Description
    pmod["Description"] = '''The player hates the idea of owning something that was once used to attack a godly man like Joseph Biden, and changes as a result: Add 20 to Offensive Rebound, Subtract 20 from Defensive Rebound.  Add Hustle Points skill.'''

    # Implementation
    pmod["Modifications"].append({"Operation" : "Add", "Key" : "SDReb", "Value" : 20})
    pmod["Modifications"].append({"Operation" : "Subtract", "Key" : "SDReb", "Value" : 20})
    pmod["Modifications"].append({"Operation" : "Set", "Key" : "SigSkill1", "Value" : "Hustle Points"})

    # Return
    return pmod
def Guardian_Rare_BidenDentures(player):
    pmod = pmod_template.getPModTemplate()
    # Artifact Name
    pmod["Name"] = '''Joe Biden's Dentures, stained with the blood of Cornpop.'''
    # Artifact Info
    pmod["Type"]["TypeName"] = "Artifact"
    pmod["Type"]["ArchetypeLock"] = "Guardian"
    pmod["Type"]["Rarity"] = "Rare"
    # Image Path
    pmod["Image"] = "ArtifactIcons\\BloodyDentures.png"
    # Description
    pmod["Description"] = '''Feeling energized at the idea of possessing a battle-tested piece of weaponry, the player changes: Add 20 to Defensive Rebound, Subtract 20 from Offensive Rebound.  Add Scrapper skill.'''

    # Implementation
    pmod["Modifications"].append({"Operation" : "Subtract", "Key" : "SDReb", "Value" : 20})
    pmod["Modifications"].append({"Operation" : "Add", "Key" : "SDReb", "Value" : 20})
    pmod["Modifications"].append({"Operation" : "Set", "Key" : "SigSkill1", "Value" : "Scrapper"})

    # Return
    return pmod
def Guardian_Rare_LearnedRoaches(player):
    pmod = pmod_template.getPModTemplate()
    # Artifact Name
    pmod["Name"] = '''The Roaches Joe Learned A Lot About'''
    # Artifact Info
    pmod["Type"]["TypeName"] = "Artifact"
    pmod["Type"]["ArchetypeLock"] = "Guardian"
    pmod["Type"]["Rarity"] = "Rare"
    # Image Path
    pmod["Image"] = "ArtifactIcons\\ScholarlyRoaches.png"
    # Description
    pmod["Description"] = '''Grinning ear to ear, the player is content; he knows that few others realize the power of having a few roaches over for dinner. Add 5 to all other stats, -10 to 3pt shooting. Add Posterizer.'''

    # Implementation
    for attribute in archetypes.ALL_ATTRIBUTES:
        if(attribute == "SSht3PT"):
            pmod["Modifications"].append({"Operation" : "Subtract", "Key" : attribute, "Value" : 10})
        else:
            pmod["Modifications"].append({"Operation": "Add", "Key": attribute, "Value": 5})
    pmod["Modifications"].append({"Operation": "Set", "Key": "SigSkill1", "Value": "Posterizer"})

    # Return
    return pmod
def Guardian_Rare_TaughtBiden(player):
    pmod = pmod_template.getPModTemplate()
    # Artifact Name
    pmod["Name"] = '''Joe Biden, the Man the Roaches Taught A Lot To'''
    # Artifact Info
    pmod["Type"]["TypeName"] = "Artifact"
    pmod["Type"]["ArchetypeLock"] = "Guardian"
    pmod["Type"]["Rarity"] = "Rare"
    # Image Path
    pmod["Image"] = "ArtifactIcons\\JoeBiden.png"
    # Description
    pmod["Description"] = '''C'mon man give him a chance! The player finds no contentment in giving Joe a chance, but does it anyway since the alternative is objectively worse. Add 10 to 3pt shooting, -5 to all other stats. Add Spot-up Shooter skill.'''

    # Implementation
    for attribute in archetypes.ALL_ATTRIBUTES:
        if(attribute == "SSht3PT"):
            pmod["Modifications"].append({"Operation" : "Add", "Key" : attribute, "Value" : 10})
        else:
            pmod["Modifications"].append({"Operation": "Subtract", "Key": attribute, "Value": 5})
    pmod["Modifications"].append({"Operation": "Set", "Key": "SigSkill1", "Value": "Spot Up Shooter"})

    # Return
    return pmod
guardian_rare = [Guardian_Rare_CornpopRazor,Guardian_Rare_BidenDentures,Guardian_Rare_LearnedRoaches,
                 Guardian_Rare_TaughtBiden]
def Guardian_Epic_NervousLaughter(player):
    pmod = pmod_template.getPModTemplate()
    # Artifact Name
    pmod["Name"] = '''Nervous Laughter from an Audience in Harlem who Joe Biden just addressed as his '"'Brothas from the Hood\''''
    # Artifact Info
    pmod["Type"]["TypeName"] = "Artifact"
    pmod["Type"]["ArchetypeLock"] = "Guardian"
    pmod["Type"]["Rarity"] = "Epic"
    # Image Path
    pmod["Image"] = "ArtifactIcons\\NervousLaughter.png"
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
def Guardian_Epic_30330(player):
    pmod = pmod_template.getPModTemplate()
    # Artifact Name
    pmod["Name"] = '''A Confused GPS Device, Desperately Trying to Load the Location of 'JOE 30330\''''
    # Artifact Info
    pmod["Type"]["TypeName"] = "Artifact"
    pmod["Type"]["ArchetypeLock"] = "Guardian"
    pmod["Type"]["Rarity"] = "Epic"
    # Image Path
    pmod["Image"] = "ArtifactIcons\\GPS30330.png"
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
def Guardian_Epic_PenCoatRack(player):
    pmod = pmod_template.getPModTemplate()
    # Artifact Name
    pmod["Name"] = '''A Pen Joe Biden Mistakenly Gave to a Coat Rack instead of the Small Child to His Left'''
    # Artifact Info
    pmod["Type"]["TypeName"] = "Artifact"
    pmod["Type"]["ArchetypeLock"] = "Guardian"
    pmod["Type"]["Rarity"] = "Epic"
    # Image Path
    pmod["Image"] = "ArtifactIcons\\PenCoatRack.png"
    # Description
    pmod["Description"] = '''It's the thought that counts, even when the thought is half formulated by a deteriorating brain. Vertical is set to 99. Offensive and Defensive Rebound are set to 25. Add Hustle Points.'''

    # Implementation
    pmod["Modifications"].append({"Operation": "Set", "Key": "SVertical", "Value": 99})
    pmod["Modifications"].append({"Operation": "Set", "Key": "SOReb", "Value": 25})
    pmod["Modifications"].append({"Operation": "Set", "Key": "SDReb", "Value": 25})
    pmod["Modifications"].append({"Operation": "Set", "Key": "SigSkill1", "Value": "Hustle Points"})

    # Return
    return pmod
def Guardian_Epic_PonySoldier(player):
    pmod = pmod_template.getPModTemplate()
    # Artifact Name
    pmod["Name"] = '''A Lying Dog-Faced Pony Soldier'''
    # Artifact Info
    pmod["Type"]["TypeName"] = "Artifact"
    pmod["Type"]["ArchetypeLock"] = "Guardian"
    pmod["Type"]["Rarity"] = "Epic"
    # Image Path
    pmod["Image"] = "ArtifactIcons\\DogFacedPonySoldier.png"
    # Description
    pmod["Description"] = '''No you didn't. Now sit down fat, before I call Crimea. Add Pickpocket. Steal is set to a number between 80 and 99.  Strength and On-Ball Defense are set to a random number between 25 and 40.'''

    # Implementation
    pmod["Modifications"].append({"Operation": "Set", "Key": "SigSkill1", "Value": "Pick Pocketer"})
    pmod["Modifications"].append({"Operation": "Set", "Key": "SSteal", "Value": random.randrange(80,100)})
    pmod["Modifications"].append({"Operation": "Set", "Key": "SStrength", "Value": random.randrange(25,41)})
    pmod["Modifications"].append({"Operation": "Set", "Key": "SOnBallD", "Value": random.randrange(25,41)})

    # Return
    return pmod
guardian_epic = [Guardian_Epic_NervousLaughter,Guardian_Epic_30330,Guardian_Epic_PenCoatRack,Guardian_Epic_PonySoldier]
def Guardian_Legendary_JordanLeg(player):
    pmod = pmod_template.getPModTemplate()
    # Artifact Name
    pmod["Name"] = '''Michael Jordan's Amputated Leg'''
    # Artifact Info
    pmod["Type"]["TypeName"] = "Artifact"
    pmod["Type"]["ArchetypeLock"] = "Guardian"
    pmod["Type"]["Rarity"] = "Legendary"
    # Image Path
    pmod["Image"] = "ArtifactIcons\\MichaelJordanLeg.png"
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
def Guardian_Legendary_FitzgeraldElixir(player):
    pmod = pmod_template.getPModTemplate()
    # Artifact Name
    pmod["Name"] = '''The Mysterious Elixir Last Drunken by Fitzgerald Kambavolo'''
    # Artifact Info
    pmod["Type"]["TypeName"] = "Artifact"
    pmod["Type"]["ArchetypeLock"] = "Guardian"
    pmod["Type"]["Rarity"] = "Legendary"
    # Image Path
    pmod["Image"] = "ArtifactIcons\\KambavoloElixir.png"
    # Description
    pmod["Description"] = '''The Guardian takes, randomly, 1-5 swigs of the mysterious elixir. For each swig taken, reduce all stats by 5, and increase height by 3 inches. Add Brick Wall.\n\n'''

    # Implementation
    swigs = random.randrange(1,6)
    for attribute in archetypes.ALL_ATTRIBUTES:
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
def Guardian_Legendary_IcyTouch(player):
    pmod = pmod_template.getPModTemplate()
    # Artifact Name
    pmod["Name"] = '''The Icy Touch of the Night King'''
    # Artifact Info
    pmod["Type"]["TypeName"] = "Artifact"
    pmod["Type"]["ArchetypeLock"] = "Guardian"
    pmod["Type"]["Rarity"] = "Legendary"
    # Image Path
    pmod["Image"] = "ArtifactIcons\\IcyTouch.png"
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
guardian_legendary = [Guardian_Legendary_JordanLeg,Guardian_Legendary_FitzgeraldElixir,
                      Guardian_Legendary_IcyTouch]

#endregion === Guardians ===
#region === Engineers ===

def Engineer_Rare_ShirtBearArms(player):
    pmod = pmod_template.getPModTemplate()
    # Artifact Name
    pmod["Name"] = '''A T-Shirt from Scott Brown reading: '2nd to Shoot, 1st to Kill! #RightToBearArms\''''
    # Artifact Info
    pmod["Type"]["TypeName"] = "Artifact"
    pmod["Type"]["ArchetypeLock"] = "Engineer"
    pmod["Type"]["Rarity"] = "Rare"
    # Image Path
    pmod["Image"] = "ArtifactIcons\\ShirtFirstToKill.png"
    # Description
    pmod["Description"] = '''Knowing that hoodlums are terrible shots, and that the player themself is a shooter akin John Wayne, the player lets out a roaring set of laughs. Add 20 to Defensive Rebound, Subtract 20 from Offensive Rebound.  Add Scrapper skill.'''

    # Implementation
    pmod["Modifications"].append({"Operation" : "Add", "Key" : "SDReb", "Value" : 20})
    pmod["Modifications"].append({"Operation" : "Subtract", "Key" : "SOReb", "Value" : 20})
    pmod["Modifications"].append({"Operation" : "Set", "Key" : "SigSkill1", "Value" : "Scrapper"})

    # Return
    return pmod
def Engineer_Rare_ShirtArmedBacon(player):
    pmod = pmod_template.getPModTemplate()
    # Artifact Name
    pmod["Name"] = '''A T-Shirt from Scott Brown reading: 'Be warned, I'm legally armed with weaponry....and BACON!\''''
    # Artifact Info
    pmod["Type"]["TypeName"] = "Artifact"
    pmod["Type"]["ArchetypeLock"] = "Engineer"
    pmod["Type"]["Rarity"] = "Rare"
    # Image Path
    pmod["Image"] = "ArtifactIcons\\ShirtBaconWeaponry.png"
    # Description
    pmod["Description"] = '''Nodding their head up and down, failing to hold back a good laugh, the player holsters their glock and prepares to make some bacon. Add 20 to Offensive Rebound, Subtract 20 from Defensive Rebound.  Add Hustle Points skill.'''

    # Implementation
    pmod["Modifications"].append({"Operation" : "Subtract", "Key" : "SDReb", "Value" : 20})
    pmod["Modifications"].append({"Operation" : "Add", "Key" : "SOReb", "Value" : 20})
    pmod["Modifications"].append({"Operation" : "Set", "Key" : "SigSkill1", "Value" : "Hustle Points"})

    # Return
    return pmod
def Engineer_Rare_ShirtStupidMask(player):
    pmod = pmod_template.getPModTemplate()
    # Artifact Name
    pmod["Name"] = '''A T-Shirt from Scott Brown reading: 'Keep your mask on, it stops all the STUPID from spilling out!\''''
    # Artifact Info
    pmod["Type"]["TypeName"] = "Artifact"
    pmod["Type"]["ArchetypeLock"] = "Engineer"
    pmod["Type"]["Rarity"] = "Rare"
    # Image Path
    pmod["Image"] = "ArtifactIcons\\ShirtStupidMask.png"
    # Description
    pmod["Description"] = '''After letting out a hearty chuckle, knowing full and well that the mask mandate is a deep state PSYOP, the player changes: Add 10 Speed, -15 Quickness. Add Chasedown Artist.'''

    # Implementation
    pmod["Modifications"].append({"Operation" : "Add", "Key" : "SSpeed", "Value" : 10})
    pmod["Modifications"].append({"Operation" : "Subtract", "Key" : "SQuick", "Value" : 15})
    pmod["Modifications"].append({"Operation" : "Set", "Key" : "SigSkill1", "Value" : "Chase Down Artist"})

    # Return
    return pmod
def Engineer_Rare_ShirtAllergy(player):
    pmod = pmod_template.getPModTemplate()
    # Artifact Name
    pmod["Name"] = '''A T-Shirt from Scott Brown reading: 'Stay back,  I am deathly allergic to STUPID!\''''
    # Artifact Info
    pmod["Type"]["TypeName"] = "Artifact"
    pmod["Type"]["ArchetypeLock"] = "Engineer"
    pmod["Type"]["Rarity"] = "Rare"
    # Image Path
    pmod["Image"] = "ArtifactIcons\\ShirtDeathlyAllergic.png"
    # Description
    pmod["Description"] = '''Scott's humor knows no bounds, the player revels in sharing an occupation with the next George Carlin. Add 15 Quickness, -10 Speed. Add Post Playmaker.'''

    # Implementation
    pmod["Modifications"].append({"Operation" : "Subtract", "Key" : "SSpeed", "Value" : 10})
    pmod["Modifications"].append({"Operation" : "Add", "Key" : "SQuick", "Value" : 15})
    pmod["Modifications"].append({"Operation" : "Set", "Key" : "SigSkill1", "Value" : "Post Playmaker"})

    # Return
    return pmod
engineer_rare = [Engineer_Rare_ShirtBearArms,Engineer_Rare_ShirtArmedBacon,Engineer_Rare_ShirtStupidMask,
                 Engineer_Rare_ShirtAllergy]
def Engineer_Epic_ShirtBachelors(player):
    pmod = pmod_template.getPModTemplate()
    # Artifact Name
    pmod["Name"] = '''A T-Shirt from Scott Brown reading: 'I wipe my ASS with your bachelor of arts degree!\''''
    # Artifact Info
    pmod["Type"]["TypeName"] = "Artifact"
    pmod["Type"]["ArchetypeLock"] = "Engineer"
    pmod["Type"]["Rarity"] = "Epic"
    # Image Path
    pmod["Image"] = "ArtifactIcons\\ShirtsBachelorArts.png"
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
def Engineer_Epic_ShirtSarcastic(player):
    pmod = pmod_template.getPModTemplate()
    # Artifact Name
    pmod["Name"] = '''A T-Shirt from Scott Brown reading: 'If you don't want a sarcastic answer, don't ask a STUPID question!\''''
    # Artifact Info
    pmod["Type"]["TypeName"] = "Artifact"
    pmod["Type"]["ArchetypeLock"] = "Engineer"
    pmod["Type"]["Rarity"] = "Epic"
    # Image Path
    pmod["Image"] = "ArtifactIcons\\ShirtSarcasticAnswer.png"
    # Description
    pmod["Description"] = '''So damn true. The player smiles knowingly and changes as follows: Add 20 to Speed and Quickness. Add 15 to accented secondary stats.  Strength and Low Post Defense are set to 25. -5-7 inches to Height.'''

    # Implementation
    pmod["Modifications"].append({"Operation": "Add", "Key": "SSpeed", "Value": 20})
    pmod["Modifications"].append({"Operation": "Add", "Key": "SQuick", "Value": 20})
    for accentedAttribute in player["Archetype"].accentedAttributes:
        if(accentedAttribute in player["Archetype"].secondaryAttributes):
            pmod["Modifications"].append({"Operation": "Add", "Key": accentedAttribute, "Value": 15})
    pmod["Modifications"].append({"Operation": "Set", "Key": "SStrength", "Value": 25})
    pmod["Modifications"].append({"Operation": "Set", "Key": "SDLowPost", "Value": 25})
    pmod["Modifications"].append({"Operation": "Subtract", "Key": "HeightIn", "Value": random.randrange(5,8)})


    # Return
    return pmod
def Engineer_Epic_ShirtSpeakMoron(player):
    pmod = pmod_template.getPModTemplate()
    # Artifact Name
    pmod["Name"] = '''A T-Shirt from Scott Brown reading: 'I don't speak MORON, we'll have to communicate in sign language!' Below is an image of a white man giving the middle finger.'''
    # Artifact Info
    pmod["Type"]["TypeName"] = "Artifact"
    pmod["Type"]["ArchetypeLock"] = "Engineer"
    pmod["Type"]["Rarity"] = "Epic"
    # Image Path
    pmod["Image"] = "ArtifactIcons\\ShirtMoron.png"
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
def Engineer_Epic_ShirtTechSupport(player):
    pmod = pmod_template.getPModTemplate()
    # Artifact Name
    pmod["Name"] = '''A T-Shirt from Scott Brown reading: 'Nothing you can do will scare me - I work in TECH SUPPORT!\''''
    # Artifact Info
    pmod["Type"]["TypeName"] = "Artifact"
    pmod["Type"]["ArchetypeLock"] = "Engineer"
    pmod["Type"]["Rarity"] = "Epic"
    # Image Path
    pmod["Image"] = "ArtifactIcons\\ShirtTechSupport.png"
    # Description
    pmod["Description"] = '''Feeling relieved to work a job that builds so much character, the player evolves: Add 5-7 inches to height, subtract 30 from speed, quickness, and vertical. Add 20 to non-accented secondary stats. Add Eraser and Brick Wall.'''

    # Implementation
    pmod["Modifications"].append({"Operation": "Add", "Key": "HeightIn", "Value": random.randrange(5,8)})

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
engineer_epic = [Engineer_Epic_ShirtBachelors,Engineer_Epic_ShirtSarcastic,Engineer_Epic_ShirtSpeakMoron,
                 Engineer_Epic_ShirtTechSupport]
def Engineer_Legendary_SecuritySerum(player):
    pmod = pmod_template.getPModTemplate()
    # Artifact Name
    pmod["Name"] = '''Security Serum, courtesy of Amalgamo Inc.'''
    # Artifact Info
    pmod["Type"]["TypeName"] = "Artifact"
    pmod["Type"]["ArchetypeLock"] = "Engineer"
    pmod["Type"]["Rarity"] = "Legendary"
    # Image Path
    pmod["Image"] = "ArtifactIcons\\SecuritySerum.png"
    # Description
    pmod["Description"] = '''Take 1-5 swigs of the Security Serum. For each swig taken, -8-12 Speed and Quickness, and Offensive Rebound, and +8-12 to Defensive Rebound, Low Post Defense, On-Ball Defense, Strength, Ball Security, Block, and Defensive Awareness. Add Lockdown Defender and Eraser.\n\n'''

    # Implementation
    swigs = random.randrange(1,6)

    pmod["Modifications"].append({"Operation": "Subtract", "Key": "SSpeed", "Value": swigs * random.randrange(8,13)})
    pmod["Modifications"].append({"Operation": "Subtract", "Key": "SQuick", "Value": swigs * random.randrange(8,13)})
    pmod["Modifications"].append({"Operation": "Subtract", "Key": "SOReb", "Value": swigs * random.randrange(8,13)})
    pmod["Modifications"].append({"Operation": "Add", "Key": "SDReb", "Value": swigs * random.randrange(8,13)})
    pmod["Modifications"].append({"Operation": "Add", "Key": "SDLowPost", "Value": swigs * random.randrange(8,13)})
    pmod["Modifications"].append({"Operation": "Add", "Key": "SOnBallD", "Value": swigs * random.randrange(8,13)})
    pmod["Modifications"].append({"Operation": "Add", "Key": "SStrength", "Value": swigs * random.randrange(8,13)})
    pmod["Modifications"].append({"Operation": "Add", "Key": "SBallSec", "Value": swigs * random.randrange(8,13)})
    pmod["Modifications"].append({"Operation": "Add", "Key": "SBlock", "Value": swigs * random.randrange(8,13)})
    pmod["Modifications"].append({"Operation": "Add", "Key": "SDAwar", "Value": swigs * random.randrange(8,13)})

    pmod["Modifications"].append({"Operation": "Set", "Key": "SigSkill1", "Value": "Lockdown Defender"})
    pmod["Modifications"].append({"Operation": "Set", "Key": "SigSkill2", "Value": "Eraser"})

    pmod["Description"] += f"This player took {swigs} swig"
    if(swigs > 1):
        pmod["Description"] += "s."
    else:
        pmod["Description"] += "."

    # Return
    return pmod
def Engineer_Legendary_LaatzPass(player):
    pmod = pmod_template.getPModTemplate()
    # Artifact Name
    pmod["Name"] = '''Backstage Pass, VIP Tickets to see Michael Laatz in Concert, Won from Laatz' 'ROAD TO SIX YOUTUBE SUBSCRIBERS SWEEPSTAKES\''''
    # Artifact Info
    pmod["Type"]["TypeName"] = "Artifact"
    pmod["Type"]["ArchetypeLock"] = "Engineer"
    pmod["Type"]["Rarity"] = "Legendary"
    # Image Path
    pmod["Image"] = "ArtifactIcons\\LaatzBackstagePass.png"
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
def Engineer_Legendary_LavaFloor(player):
    pmod = pmod_template.getPModTemplate()
    # Artifact Name
    pmod["Name"] = '''The Bewildered and Horrified Look on Sneh's Face After Tim Molkosky Cautioned Him that the 'Floor is Lava\''''
    # Artifact Info
    pmod["Type"]["TypeName"] = "Artifact"
    pmod["Type"]["ArchetypeLock"] = "Engineer"
    pmod["Type"]["Rarity"] = "Legendary"
    # Image Path
    pmod["Image"] = "ArtifactIcons\\BewilderedSneh.png"
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
engineer_legendary = [Engineer_Legendary_SecuritySerum,Engineer_Legendary_LaatzPass,
                      Engineer_Legendary_LavaFloor]

#endregion === Engineers ===
#region === Directors ===

def Director_Rare_BagOfRocks(player):
    pmod = pmod_template.getPModTemplate()
    # Artifact Name
    pmod["Name"] = '''A Bag of "Rocks" Recovered from a DEA Agent's Remains'''
    # Artifact Info
    pmod["Type"]["TypeName"] = "Artifact"
    pmod["Type"]["ArchetypeLock"] = "Director"
    pmod["Type"]["Rarity"] = "Rare"
    # Image Path
    pmod["Image"] = "ArtifactIcons\\BagOfRocks.png"
    # Description
    pmod["Description"] = '''Blissfully unaware of the difference between rocks and minerals, the player decides these will be perfect for skipping across a good lake. Adds Highlight Film and Dimer. +10 Pass. -10 Hands.'''

    # Implementation
    pmod["Modifications"].append({"Operation" : "Set", "Key" : "SigSkill1", "Value" : "Highlight Film"})
    pmod["Modifications"].append({"Operation" : "Set", "Key" : "SigSkill2", "Value" : "Dimer"})
    pmod["Modifications"].append({"Operation" : "Add", "Key" : "SPass", "Value" : 10})
    pmod["Modifications"].append({"Operation" : "Subtract", "Key" : "SHands", "Value" : 10})

    # Return
    return pmod
def Director_Rare_BagOfMeth(player):
    pmod = pmod_template.getPModTemplate()
    # Artifact Name
    pmod["Name"] = '''A Bag of "Meth" Recovered from a Massive Explosion in the City'''
    # Artifact Info
    pmod["Type"]["TypeName"] = "Artifact"
    pmod["Type"]["ArchetypeLock"] = "Director"
    pmod["Type"]["Rarity"] = "Rare"
    # Image Path
    pmod["Image"] = "ArtifactIcons\\ExplosionMeth.png"
    # Description
    pmod["Description"] = '''Knowing that they shouldn't waste good meth, the player snorts the explosive powder and changes: Adds Heat Retention and Shot Creator. +10 Shoot Off Dribble, -10 Shoot In Traffic.'''

    # Implementation
    pmod["Modifications"].append({"Operation" : "Set", "Key" : "SigSkill1", "Value" : "Heat Retention"})
    pmod["Modifications"].append({"Operation" : "Set", "Key" : "SigSkill2", "Value" : "Shot Creator"})
    pmod["Modifications"].append({"Operation" : "Add", "Key" : "SShtOfD", "Value" : 10})
    pmod["Modifications"].append({"Operation" : "Subtract", "Key" : "SShtInT", "Value" : 10})

    # Return
    return pmod
def Director_Rare_HamlinBoxing(player):
    pmod = pmod_template.getPModTemplate()
    # Artifact Name
    pmod["Name"] = '''Howard Hamlin's Pristine Boxing Gear'''
    # Artifact Info
    pmod["Type"]["TypeName"] = "Artifact"
    pmod["Type"]["ArchetypeLock"] = "Director"
    pmod["Type"]["Rarity"] = "Rare"
    # Image Path
    pmod["Image"] = "ArtifactIcons\\HamlinPristineBoxingGear.png"
    # Description
    pmod["Description"] = '''Appreciating the delicate care taken to the dueling gear, the player finds a state of zen and changes as follows: Add 2 inches of height. -10 speed and quickness. Add Defensive Anchor.'''

    # Implementation
    pmod["Modifications"].append({"Operation" : "Subtract", "Key" : "SSpeed", "Value" : 10})
    pmod["Modifications"].append({"Operation" : "Subtract", "Key" : "SQuick", "Value" : 10})
    pmod["Modifications"].append({"Operation" : "Set", "Key" : "SigSkill1", "Value" : "Defensive Anchor"})
    pmod["Modifications"].append({"Operation" : "Add", "Key" : "HeightIn", "Value" : 2})

    # Return
    return pmod
def Director_Rare_JimmyBoxing(player):
    pmod = pmod_template.getPModTemplate()
    # Artifact Name
    pmod["Name"] = '''Jimmy McGill's Wartorn Boxing Gear'''
    # Artifact Info
    pmod["Type"]["TypeName"] = "Artifact"
    pmod["Type"]["ArchetypeLock"] = "Director"
    pmod["Type"]["Rarity"] = "Rare"
    # Image Path
    pmod["Image"] = "ArtifactIcons\\JimmyWartornBoxingGear.png"
    # Description
    pmod["Description"] = '''Feeling perplexed on the very existence of this artifact, the player ponders on this thought and loses 2 inches of height. +10 speed and quickness. Add Chasedown artist.'''

    # Implementation
    pmod["Modifications"].append({"Operation" : "Subtract", "Key" : "HeightIn", "Value" : 2})
    pmod["Modifications"].append({"Operation" : "Add", "Key" : "SSpeed", "Value" : 10})
    pmod["Modifications"].append({"Operation" : "Add", "Key" : "SQuick", "Value" : 10})
    pmod["Modifications"].append({"Operation" : "Set", "Key" : "SigSkill1", "Value" : "Chase Down Artist"})

    # Return
    return pmod
director_rare = [Director_Rare_BagOfRocks,Director_Rare_BagOfMeth,Director_Rare_HamlinBoxing,
                 Director_Rare_JimmyBoxing]
def Director_Epic_Pimento(player):
    pmod = pmod_template.getPModTemplate()
    # Artifact Name
    pmod["Name"] = '''Some Geezer Eating a Pimento Sandwich'''
    # Artifact Info
    pmod["Type"]["TypeName"] = "Artifact"
    pmod["Type"]["ArchetypeLock"] = "Director"
    pmod["Type"]["Rarity"] = "Epic"
    # Image Path
    pmod["Image"] = "ArtifactIcons\\GeezerPimentoSandwich.png"
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
def Director_Epic_VinceHumility(player):
    pmod = pmod_template.getPModTemplate()
    # Artifact Name
    pmod["Name"] = '''Vial of Vince Gilligan's Humility, Liquefied'''
    # Artifact Info
    pmod["Type"]["TypeName"] = "Artifact"
    pmod["Type"]["ArchetypeLock"] = "Director"
    pmod["Type"]["Rarity"] = "Epic"
    # Image Path
    pmod["Image"] = "ArtifactIcons\\GilliganHumility.png"
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
def Director_Epic_SnappedCellphone(player):
    pmod = pmod_template.getPModTemplate()
    # Artifact Name
    pmod["Name"] = '''A Cellphone Snapped Perfectly in Two'''
    # Artifact Info
    pmod["Type"]["TypeName"] = "Artifact"
    pmod["Type"]["ArchetypeLock"] = "Director"
    pmod["Type"]["Rarity"] = "Epic"
    # Image Path
    pmod["Image"] = "ArtifactIcons\\SnappedCellphone.png"
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
def Director_Epic_BloodCandle(player):
    pmod = pmod_template.getPModTemplate()
    # Artifact Name
    pmod["Name"] = '''A Burnt Out Candle, Stained with a Single Drop of Blood'''
    # Artifact Info
    pmod["Type"]["TypeName"] = "Artifact"
    pmod["Type"]["ArchetypeLock"] = "Director"
    pmod["Type"]["Rarity"] = "Epic"
    # Image Path
    pmod["Image"] = "ArtifactIcons\\BurntCandle.png"
    # Description
    pmod["Description"] = '''Holy fuck. The player didn't expect such a deeply unnerving artifact and changes as follows: Set Offensive and Defensive awareness to 99.  Add Shot Creator, Brick Wall,  Antifreeze, and Microwave.  Subtract 4-7 from all secondary stats.'''

    # Implementation
    for secondaryAttribute in player["Archetype"].secondaryAttributes:
        pmod["Modifications"].append({"Operation" : "Subtract", "Key" : secondaryAttribute, "Value" : random.randrange(4,8)})
    pmod["Modifications"].append({"Operation": "Set", "Key": "SOAwar", "Value": 99})
    pmod["Modifications"].append({"Operation": "Set", "Key": "SDAwar", "Value": 99})
    pmod["Modifications"].append({"Operation": "Set", "Key": "SigSkill1", "Value": "Shot Creator"})
    pmod["Modifications"].append({"Operation": "Set", "Key": "SigSkill1", "Value": "Brick Wall"})
    pmod["Modifications"].append({"Operation": "Set", "Key": "SigSkill1", "Value": "Anti-Freeze"})
    pmod["Modifications"].append({"Operation": "Set", "Key": "SigSkill1", "Value": "Microwave"})

    # Return
    return pmod
director_epic = [Director_Epic_Pimento,Director_Epic_VinceHumility,Director_Epic_SnappedCellphone,
                 Director_Epic_BloodCandle]
def Director_Legendary_SwiftnessSerum(player):
    pmod = pmod_template.getPModTemplate()
    # Artifact Name
    pmod["Name"] = '''Swiftness Serum, courtesy of Amalgamo Inc.'''
    # Artifact Info
    pmod["Type"]["TypeName"] = "Artifact"
    pmod["Type"]["ArchetypeLock"] = "Director"
    pmod["Type"]["Rarity"] = "Legendary"
    # Image Path
    pmod["Image"] = "ArtifactIcons\\SwiftnessSerum.png"
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
def Director_Legendary_MidCertification(player):
    pmod = pmod_template.getPModTemplate()
    # Artifact Name
    pmod["Name"] = '''An Ancient Mid Certification Badge, Passed Down for Hundreds of Years'''
    # Artifact Info
    pmod["Type"]["TypeName"] = "Artifact"
    pmod["Type"]["ArchetypeLock"] = "Director"
    pmod["Type"]["Rarity"] = "Legendary"
    # Image Path
    pmod["Image"] = "ArtifactIcons\\AncientMidCertification.png"
    # Description
    pmod["Description"] = '''The player knows the weight that such a certification carries, and feels empowered that they are able to carry on its legacy. Shot Medium, Shot Close, and Consistency are set to 90-99. Add Corner Specialist and Acrobat. All 3PT Hotzones are Cold Zones.  Add a epic or legendary shot:\n\n'''

    # Implementation
    pmod["Modifications"].append({"Operation": "Set", "Key": "SShtMed", "Value": random.randrange(90,100)})
    pmod["Modifications"].append({"Operation": "Set", "Key": "SShtCls", "Value": random.randrange(90,100)})
    pmod["Modifications"].append({"Operation": "Set", "Key": "SConsis", "Value": random.randrange(90,100)})

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
def Director_Legendary_MilkdudNarcotics(player):
    pmod = pmod_template.getPModTemplate()
    # Artifact Name
    pmod["Name"] = '''An Assorted Baggy of Mystical Melvin Milkdud's Hallucinogenic Narcotics Labeled "Magic Candy for Kids of All Ages!'''
    # Artifact Info
    pmod["Type"]["TypeName"] = "Artifact"
    pmod["Type"]["ArchetypeLock"] = "Director"
    pmod["Type"]["Rarity"] = "Legendary"
    # Image Path
    pmod["Image"] = "ArtifactIcons\\MilkdudCandies.png"
    # Description
    pmod["Description"] = '''Putting all their trust into the disheveled and wild eyed 90 year old, the player giddily gulps down 5 of Melvin's finest candies. Add 40 to Vertical, Offensive Rebound, Defensive Rebound. Remove 6-8 inches of height. Randomly assign each non-3pt zone a hot or cold value.\n\n'''

    # Implementation
    pmod["Modifications"].append({"Operation": "Add", "Key": "SVertical", "Value": 40})
    pmod["Modifications"].append({"Operation": "Add", "Key": "SOReb", "Value": 40})
    pmod["Modifications"].append({"Operation": "Add", "Key": "SDReb", "Value": 40})

    pmod["Modifications"].append({"Operation": "Subtract", "Key": "HeightIn", "Value": random.randrange(6,9)})

    pmod["Modifications"].append({"Operation": "Set", "Key": "HZ1", "Value": random.choice([0,2])})
    pmod["Modifications"].append({"Operation": "Set", "Key": "HZ2", "Value": random.choice([0,2])})
    pmod["Modifications"].append({"Operation": "Set", "Key": "HZ3", "Value": random.choice([0,2])})
    pmod["Modifications"].append({"Operation": "Set", "Key": "HZ4", "Value": random.choice([0,2])})
    pmod["Modifications"].append({"Operation": "Set", "Key": "HZ5", "Value": random.choice([0,2])})
    pmod["Modifications"].append({"Operation": "Set", "Key": "HZ6", "Value": random.choice([0,2])})
    pmod["Modifications"].append({"Operation": "Set", "Key": "HZ7", "Value": random.choice([0,2])})
    pmod["Modifications"].append({"Operation": "Set", "Key": "HZ8", "Value": random.choice([0,2])})
    pmod["Modifications"].append({"Operation": "Set", "Key": "HZ9", "Value": random.choice([0,2])})



    # Return
    return pmod
director_legendary = [Director_Legendary_SwiftnessSerum,Director_Legendary_MidCertification,
                      Director_Legendary_MilkdudNarcotics]

#endregion === Directors ===

ARTIFACTS = {"Neutral" : {"Rare" : neutral_rare, "Epic" : neutral_epic, "Legendary" : neutral_legendary, "Godlike" : neutral_godlike},
             "Slayer" : {"Rare" : slayer_rare, "Epic" : slayer_epic, "Legendary" : slayer_legendary},
             "Vigilante" : {"Rare" : vigilante_rare, "Epic" : vigilante_epic, "Legendary" : vigilante_legendary},
             "Medic" : {"Rare" : medic_rare, "Epic" : medic_epic, "Legendary" : medic_legendary},
             "Guardian" : {"Rare" : guardian_rare, "Epic" : guardian_epic, "Legendary" : guardian_legendary},
             "Engineer" : {"Rare" : engineer_rare, "Epic" : engineer_epic, "Legendary" : engineer_legendary},
             "Director" : {"Rare" : director_rare, "Epic" : director_epic, "Legendary" : director_legendary}}
