import re
import chardet
import random
from spritopia.utilities import weighted_dict

# This method simply selects a value or values randomly from a given file of words.
# Each word in this file should be separated by newlines - one selection per line.
# -filePath can be a string containing a single file path, or an array of file paths.
# -selectionCount specifies how many random values from the file's you'd like to gen.
# -hatPick means that subsequent random values will never be the same as already picked values.
# -rStringProcessing allows for processing results as rStrings (see below)
def rFile(filePath, selectionCount : int = 1, hatPick : bool = False, rStringProcessing : bool = False):
    if(type(filePath) is str):
        filePath = [filePath]
    elif(type(filePath) is not list):
        raise FileNotFoundError(filePath)

    allPotentialValues = []
    for thisFilePath in filePath:
        with open(thisFilePath,"rb") as f:
            fileResult = chardet.detect(f.read())

        with open(thisFilePath,"r",encoding=fileResult["encoding"]) as thisFile:
            allPotentialValues += [line.strip() for line in thisFile]

    returnArray = []
    if(hatPick):
        random.shuffle(allPotentialValues)
        for i in range(min(selectionCount,len(allPotentialValues))):
            returnArray.append(allPotentialValues[i])
    else:
        for i in range(selectionCount):
            returnArray.append(random.choice(allPotentialValues))

    # If rStringProcessing is on, we process the results as rStrings.
    if(rStringProcessing):
        tempArray = []
        for result in returnArray:
            tempArray.append(rStringProcess(result,recursiveProcessing=True))
        returnArray = tempArray

    return returnArray

# This method simply processed an "rString", a simple string randomization format I've designed for extended
# ease of use with randomization. If recursive processing is on, any options picked from word lists will ALSO
# be randomized.
# {choice1,choice2,choice3} is an adLib operator, and would process randomly to select one of the three choices only.
# [path/to/other/wordlist] is a randomList selection operator, and would attempt to fill that spot with a single entry from the randList path.
def rString(string,recursiveProcessing : bool = True,randListPath = ""):

    # Locate all occurrences of {option1, option2, ...} in the string
    options = re.findall('{([^}]*)}', string)
    # Replace each occurrence with a random choice
    for option in options:
        choicesList = option.split(',')
        choices = weighted_dict.WeightedDict()
        # Test to see if any choices have weights.
        for choice in choicesList:
            if("::" in choice):
                weight = int(choice.split("::")[1])
                choice = choice.split("::")[0]
            else:
                weight = 1
            choices.add(choice,weight)
        string = string.replace('{' + option + '}', choices.pull())

    # Locate all occurrences of [path/to/file] in the string
    options = re.findall(r'\[([^]]*)]', string)
    # Assume each option is a file path to a wordlist, recursively gen from that list
    for option in options:
        pickedOption = rFile(filePath = f"{randListPath}\\{option}",rStringProcessing=recursiveProcessing)[0]
        string = string.replace(f"[{option}]",pickedOption)

    return string