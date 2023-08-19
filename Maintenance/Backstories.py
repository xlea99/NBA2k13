import BaseFunctions as b
import random
import tomlkit
import openai
import concurrent.futures
import sqlite3

# Setup gpt info
alAPIKey = "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"
danAPIKey = "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"
openai.api_key = alAPIKey
model = "gpt-4"


with open("UnrefinedBackstory.toml", "r") as f:
    unrefinedBackstory = tomlkit.parse(f.read())

with open("RefinedBackstory.toml", "r") as f:
    refinedBackstory = tomlkit.parse(f.read())

# This method uses the unrefined backstory template, combined with a base idea, to generate iterations new backstories.
# uniqueness - value between 1 and 3. 1 means more basic backstory, 3 means bizarre backstories, 2 is inbetween.
def genUnrefinedBackstory(idea : str,characterName : str,iterations : int = 3,uniqueness : int = 2, isIdeaRString : bool = True):
    if(uniqueness < 1 or uniqueness > 3):
        raise ValueError(f"Uniqueness value must be between 1-3, not '{uniqueness}'")
    if(isIdeaRString):
        idea = b.rStringProcess(idea)

    # Construct the backstory prompt
    backstoryPrompt = unrefinedBackstory["template"].replace("$BASE_IDEA", idea)
    backstoryPrompt = backstoryPrompt.replace("$BACKSTORY_COUNT",str(iterations))
    backstoryPrompt = backstoryPrompt.replace("$CHARACTER_NAME",characterName)
    backstoryPrompt = backstoryPrompt.replace("$INTEREST_LEVEL",unrefinedBackstory["interest"][f"level{uniqueness}"])
    print(backstoryPrompt)

    # Get the GPT response
    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "system", "content": backstoryPrompt}
        ]
    )

    storiesString = response.to_dict()["choices"][0]["message"]["content"]
    stories = storiesString.split("\n")

    cleanedStories = []
    for story in stories:
        if (story.strip() != ''):
            cleanedStory = story[story.find(".") + 1:].strip()
            if(cleanedStory != ""):
                cleanedStories.append(cleanedStory)

    if(len(cleanedStories) != iterations):
        print("FUCKLLES!")
        return cleanedStories
    else:
        return cleanedStories

# This method uses the refined backstory template to "refine" a backstory and adjust it to a certain degree.
def refineBackstory(baseBackstory : str,characterName : str, modifiers : list,scope : int = 2,characterTraits : list = None):
    if(characterTraits is None):
        characterTraits = []
        for i in range(2):
            if(random.random() > 0.5):
                characterTraits.append(b.selectRandomFromList(f"{b.paths.randGen}\\WordLists\\positive_character_traits.txt")[0])
            else:
                characterTraits.append(b.selectRandomFromList(f"{b.paths.randGen}\\WordLists\\positive_character_traits.txt")[0])
    traitString = ""
    for trait in characterTraits:
        traitString += f"{trait},"
    traitString = traitString.rstrip(",")

    modifierString = ""
    initialNumber = 6
    for modifier in modifiers:
        modifierString += f"{initialNumber}. {modifier}\n"
        initialNumber += 1

    # Construct the backstory prompt
    backstoryPrompt = refinedBackstory["template"].replace("$UNREFINED_BACKSTORY", baseBackstory)
    backstoryPrompt = backstoryPrompt.replace("$SCOPE_LEVEL",refinedBackstory["scope"][f"level{scope}"])
    backstoryPrompt = backstoryPrompt.replace("$CHARACTER_NAME",characterName)
    backstoryPrompt = backstoryPrompt.replace("$MODIFIERS_LIST",modifierString)
    backstoryPrompt = backstoryPrompt.replace("$CHARACTER_TRAITS",traitString)
    print(backstoryPrompt)

    # Get the GPT response
    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "system", "content": backstoryPrompt}
        ]
    )

    storiesString = response.to_dict()["choices"][0]["message"]["content"]
    #stories = storiesString.split("\n")

    return storiesString

# This method attempts to validate that a backstory set conforms to the
# appropriate format.
def validateBackstorySet(backstorySet : list):
    badWords = ["Backstory", "Modifier", "Character"]
    validSet = True
    for backstoryEntry in backstorySet:
        # First, validate that a backstory actually generated at all.
        if(len(backstoryEntry) <= 0):
            validSet = False
            break

        # Next, validate that the backstory begins with an uppercase letter.
        if(backstoryEntry[0].islower()):
            validSet = False
            break

        # Next, validate that the backstory ends with correct punctuation.
        if(backstoryEntry[-1] not in ".!?"):
            validSet = False
            break

        # Next, check for bad characters within the backstory.
        if("\n" in backstoryEntry or "\t" in backstoryEntry):
            validSet = False
            break

        # Finally, test for "bad words" that tend to appear at the beginning of incorrectly generated
        # backstories.
        foundBadWord = False
        for badWord in badWords:
            if(backstoryEntry.startswith(badWord)):
                validSet = False
                foundBadWord = True
                break
        if(foundBadWord):
            break

    return validSet

# Method for mass querying gpt for multiple prompts at the same time. Each prompt
# will return 5 backstories, which will be validated against the desired format.
# characterPrompts should be a list of character modifier lists. Support rString modifiers.
def processBackstories(characterPrompts : list,maxWorkers=10):
    # Create a ThreadPoolExecutor
    with concurrent.futures.ThreadPoolExecutor(max_workers=maxWorkers) as executor:
        # Dict to store the futures
        backstoryFutures = {}
        for characterModifiers in characterPrompts:
            # Process each character modifier with rStringProcess
            processedModifiers = []
            for modifier in characterModifiers:
                processedModifiers.append(b.rStringProcess(modifier))

            # Submit the processed character modifiers to the executor
            future = executor.submit(genSingleBackstorySet, processedModifiers)
            backstoryFutures[future] = processedModifiers


    backstoryList = []
    # Retrieve and store results as they become available.
    for future in concurrent.futures.as_completed(backstoryFutures):
        thisBackstoryEntry = {"modifiers" : backstoryFutures[future],
                              "backstories" : future.result()}
        thisBackstoryEntry["validity"] = validateBackstorySet(thisBackstoryEntry["backstories"])
        backstoryList.append(thisBackstoryEntry)

    return backstoryList


ideaString = '''He is a {obsessive,emoji-spamming,caffeine-fueled,bored-at-3am,keyboard-warrior,sarcastic,never-subbed,ad-block-using,backseat-gamer,serial-clipper,over-opinionated,conspiracy-theorist,whisper-spamming,trolllord,attention-hungry,capital-D-Dramatic,forever-alone,loves-the-sound-of-his-own-typing,infamous-for-wrong-reasons,delusionally-confident,chronically-offensive,saltier-than-the-dead-sea,catfish-king,trigger-happy,focused,determined,interactive,passionate,loyal,competitive,observant,entertaining,playful,tech-savvy,quick-witted,creative,relentless,trolling,ironic,memelord,provocative,confrontational,attention-seeking,cynical,sarcastic,argumentative,sharp-tongued,instigative,excitable} member of the Twitch Chatters,{who is known for his legendary emote combos,with an ability to spot stream snipers instantly,who once orchestrated a global Twitch raid,with a family history of iconic streamers,who can spot a fake donation from miles away,known for his charitable donation trains during fundraisers,who has been banned from multiple channels for trolling,who has an impressive understanding of stream analytics and metrics,whose clips frequently go viral on social media,with a close connection to a famous Twitch partner,who has been part of many legendary Twitch moments and memes,known for his lightning-fast chat reactions during hype moments,who once had a personal feud with a popular streamer,who has inside knowledge of many Twitch scandals,who was instrumental in supporting a small channel's rise to fame,with a talent for predicting plot twists in variety streams,who is notorious for causing chat wars over game preferences,known for his expertise in speedrunning challenges,who seems to always be present, no matter the time of day,with a close alliance with a well-known mod team,who once leaked confidential info during a just chatting session,who frequently donates to troll with text-to-speech,known for his exceptional lurking skills,with a love-hate relationship with chatbots,who once made a streamer laugh so hard they ended the stream early,with a controversial stance on sub-only mode chats,who always triggers chat with his contrarian viewpoints,who wears the Kappa face as his actual profile picture,who claims to have invented the PogChamp face,with the uncanny ability to always ask streamers about their day right after they've answered,who thinks 'Raiding' is his personal chat show,with a proud lineage of getting timed out since Justin.tv,who has a sixth sense for when a streamer is about to go on a bathroom break,often recognized for his essays on why 'streamer has changed',who's been banned more times than he's been welcomed,who prides himself on catching every accidental face reveal,whose 'funny' clips end up more cringe than comedy,with a 'close' friendship with a streamer's bot,who swears he was there during 'the incident' that no one remembers,always the first to remind streamers when their viewer count drops,who has declared personal vendettas against Nightbot,whose 'inside info' comes straight from streamer's Twitter feeds,with the uncanny knack for only chatting during subscriber-only mode,who treats 'emote-only mode' as a personal challenge,often found waging war on anyone who uses the wrong version of 'your',with a self-proclaimed PhD in Twitch drama,who has an archive of every time a streamer's said 'um',the guy who always asks 'is chat broken?' in a moving chat,with his not-so-subtle habit of namedropping 'smaller streamers',who's been 'just about to go to bed' for the last five hours,who's on a first-name basis with Twitch's report function,who believes that his streamer's success is 'mostly' because of him,with a suspicious number of catfishy 'girlfriend' anecdotes}.'''

walrus = genUnrefinedBackstory(idea=ideaString,characterName="John Fucemup",iterations=3,uniqueness=2)
#randomSelection = random.choice(walrus)
#flounder = refineBackstory(baseBackstory=randomSelection,characterName="John Fucemup",modifiers=b.selectRandomFromList(filePath="RefinedModifiers.txt",rStringProcessing=True),scope=1)






'''
timeWasterMessage = "kzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkz" \
                    "kzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkzkz\nCopy this back to me."
ideaString = "Belonging to the historic {respected,feared,mysterious,ornate,lavish,infamous::3,legendary,::7} House of Osman, this individual is {a well-studied historian of the Ottoman Empire,a determined diplomat seeking to restore past glory,a zealous collector of ancient artifacts,one who dreams of seeing their house recognized once more on the world stage,who would give anything for the return of the Sultanate::5}."

def wasteTime(_timeWaster : str):
    # Get the GPT response
    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "system", "content": _timeWaster}
        ]
    )
    return response.to_dict()["choices"][0]["message"]["content"]

conn = sqlite3.connect(f"S:\\Coding\\Projects\\NBA2k13\\Maintenance\\DreamsOfAI.db")
cursor = conn.cursor()

def run_with_timeout(func, timeout_sec):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future = executor.submit(func)
        try:
            return future.result(timeout=timeout_sec)
        except concurrent.futures.TimeoutError:
            return None

for i in range(5000):
    dream = run_with_timeout(lambda: wasteTime(timeWasterMessage), 10)
    if dream is not None:
        print(i)
        cursor.execute("INSERT INTO Dreams (Dream) VALUES (?)", (str(dream),))
        conn.commit()
    else:
        print(f"Skipping iteration {i} due to timeout")
'''