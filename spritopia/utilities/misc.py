from pympler import asizeof
import psutil

# === NUMBER FUNCTIONS ===

# This method simply returns true if the string is a number. Includes decimals and signs.
def isNumber(testString):
    try:
        float(testString)
        return True
    except ValueError:
        return False
# This function converts a decimal number into a "alphaBase26" number, using only letters of the alphabet.
def alphaBase26(decimalNumber : int,maxPlaces : int):
    chars = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

    # Initialize a list to hold the characters for the output string
    letterList = [None] * maxPlaces

    # Manipulate the input decimal number and fill in the output letter list
    for i in range(maxPlaces - 1, -1, -1):
        division = 26 ** i
        index, decimalNumber = divmod(decimalNumber, division)
        letterList[maxPlaces - 1 - i] = chars[index]

    # Concatenate letter list into return string
    returnString = ""
    for letter in letterList:
        returnString += letter
    return returnString
# Converts an integer representing a time in seconds into a neatly formatted time string.
def getTimeString(seconds : int):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60

    if hours > 0:
        return f"{hours}:{minutes:02d}:{seconds:02d}"
    else:
        return f"{minutes}:{seconds:02d}"


# === STRING FUNCTIONS ===

# This function returns a string starting at the given index, and removes
# everything before that.
def getStringAt(string, index):
    counter = -1
    value = ''
    for x in string:
        counter += 1
        if index <= counter:
            value += x
    return value
# Given a character or list of characters, this function counts how many times
# they collectively appear in a string.
def countFreq(characters, string):
    charList = str(characters)
    counter = 0
    for x in charList:
        for y in string:
            if x == y:
                counter += 1
    return counter


# === LIST FUNCTIONS ===

# This function finds and returns an array of all numbers missing from a sequential list.
# For example, in a list of [1,2,4,5,7] this function would return [3,6]
def find_missing(thisList):
    return [x for x in range(thisList[0], thisList[-1]+1) if x not in thisList]
# Simply returns the average of a list of numbers.
def averageOfList(thisList):
    sumOfList = 0
    counter = 0
    for item in thisList:
        if(str(type(item)) != "<class 'int'>"):
            continue
        else:
            sumOfList += item
            counter += 1
    return sumOfList / counter


# === DICT FUNCTIONS ===

# Cheaty way to get a dictionary KEY from a VALUE.
def getKeyFromValue(dictionary, targetValue):
    for key, value in dictionary.items():
        if (value == targetValue):
            return key
    raise ValueError(f"Value does not exist in the dictionary: '{targetValue}'")



# === OTHER ===

# This method accepts any python object, and returns a neat, formatted string displaying its size.
def getMemorySizeOf(thisObject):
    byteSize = asizeof.asizeof(thisObject)

    if(byteSize > 1000):
        kilobyteSize = byteSize / 1024
        if(kilobyteSize > 1000):
            megabyteSize = kilobyteSize / 1024
            if(megabyteSize > 1000):
                gigabyteSize = megabyteSize / 1024
                return f"{round(gigabyteSize,2)} GB"
            else:
                return f"{round(megabyteSize,2)} MB"
        else:
            return f"{round(kilobyteSize,2)} KB"
    else:
        return f"{round(byteSize,2)} bytes"
# This method quickly tests whether an external process exists, by its name.
def testIfProcessExists(processName : str):
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            if processName.lower() == proc.info['name'].lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False

