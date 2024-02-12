import os
import BaseFunctions as b
import random as r
import re


# The Weighted Dictionary is a special type of dictionary that uses weights to
# represent frequency of values as if they appeared multiple times within a
# dictionary. This allows us to use probability- if a value of 'guppy' has a
# weight of 4 in a Weighted Dictionary who's total value is 16, then 'guppy'
# makes up 25% of that dictionary and if a value was to be randomly selected
# from it, there is a 25% chance that that value will be 'guppy'.
class WeightedDict:

    # On initialization, the Weighted Dictionary creates its 3 important parts-
    # the contentsList for storing content values, the weightsList for storing
    # the weight of those content values, and the cumulativeList for reading
    # those values as probabilities.
    def __init__(self):
        self.totalVal = 0
        self.contentsList = []
        self.__weightsList = []
        self.__cumulativeList = []
        self.__hatEntries = []
        self.__hatWeights = []

    # __iter__ and __next__ define how the dictionary should be iterated over.
    # By default, the dictionary will return all of its key values, with the
    # final value being the upper limit of the last value, or the total value
    # of the dictionary.
    def __iter__(self):
        self.n = 0
        return self

    # This code might be broken OOF
    def __next__(self):
        keyVal = self.__cumulativeList[self.n]
        self.n += 1
        result = int(keyVal)
        '''if self.n >= self.__keyNum:
            self.n += 1
            raise StopIteration
        return result'''

    # Necessary simple get methods.
    def getWeights(self):
        return self.__weightsList

    def getCums(self):
        return self.__cumulativeList

    def getContent(self):
        return self.contentsList

    # Returns the total value of the weighted dictionary.
    def getTotal(self):
        return self.totalVal

    def getLength(self):
        length = len(self.__weightsList)
        return length

    # Gets the weight of an entry from a key, instead of the entry itself.
    def getWeight(self, key):
        counter = 0
        for x in self.__cumulativeList:
            if key > x:
                counter += 1
            else:
                weight = self.__weightsList[counter]
                break
        return weight

    # This simple regenerates the cumulativeList, from the weightedList, by
    # continuously adding the weightedList's values to a new list. It also sets
    # the total as the highest value.
    def genCumList(self):
        newCumList = []
        value = 0
        for x in self.__weightsList:
            value += x
            newCumList.append(value)
        self.__cumulativeList = newCumList
        self.totalVal = value

    # This method adds a single entry, with a given weight, to the dictionary.
    def w(self, weight, entry):
        self.__weightsList.append(int(weight))
        if type(entry) is str:
            finalEntry = b.convertToTypeExt(entry)
        else:
            finalEntry = entry
        self.contentsList.append(finalEntry)
        self.genCumList()

    # This is the basic function to read a value from a key in a weighted
    # dictionary. The key doesn't function like a regular key in a regular
    # dictionary. If there are 3 entries in a dictionary:
    # {1:'walrus',7:'flounder',16:'duck'} with a total of 16, and a value of 6
    # is given, the value returned will be 'flounder' because the key 6 falls in
    # the range of the 'flounder' value (which includes 2-7, stopping at 1 because
    # that is where the 'walrus' value range begins, and stopping at 8 as that's
    # where the 'duck' value range begins).
    def r(self, key):
        counter = 0
        for x in self.__cumulativeList:
            if key > x:
                counter += 1
            else:
                contents = self.contentsList[counter]
                break
        return contents

    # This method will remove a value from the Weighted Dictionary entirely, and
    # recalculate the cumulativeList accordingly.
    def remove(self, key):
        counter = 0
        for x in self.__cumulativeList:
            if key > x:
                pass
            else:
                valueNumber = counter
                break
            counter += 1
        contents = self.contentsList[valueNumber]
        self.contentsList.remove(contents)
        weight = self.__weightsList[valueNumber]
        self.__weightsList.remove(weight)
        self.genCumList()

    # Randomly picks a value from the dictionary using a random key.
    def randomize(self):
        total = self.getTotal()
        target = r.randint(1, total)
        result = self.r(target)
        return result

    # Special random pick method that removes the entry it picks.
    def hatPick(self):
        total = self.getTotal()
        target = r.randint(1, total)
        result = self.r(target)
        hatWeight = self.getWeight(target)
        hatEntry = result

        # Stores the picked values in a seperate location in case you want to
        # restore the picked values.
        self.__hatEntries.append(hatEntry)
        self.__hatWeights.append(hatWeight)
        self.remove(target)
        return result

    # Restores all the values removed by hat picking to the dictionary.
    def hatRestore(self):
        counter = 0
        for x in self.__hatWeights:
            weight = x
            entry = self.__hatEntries[counter]
            self.w(weight, entry)
            counter += 1
        self.__hatEntries = 0
        self.__hatWeights = 0

    # Ignores weights entirely and treats every entry like it has a weight of 1,
    # so all entries have an equal chance of being selected.
    def weightlessRandomize(self):
        length = len(self.contentsList)
        target = r.randint(0, length - 1)
        result = self.contentsList[target]
        return result

    # Method organizes the weighted dictionary from highest, heaviest values to
    # smallest, lightest values by default. Set mode to 'low' to organize it in
    # the other direction.
    def sort(self, mode='high'):
        length = len(self.__weightsList)
        newWeights = []
        newContents = []
        if mode == 'high':
            for x in range(length):
                targetIndex = b.getMaxIndex(self.__weightsList)
                weight = self.__weightsList[targetIndex]
                contents = self.contentsList[targetIndex]
                newWeights.append(weight)
                newContents.append(contents)
                del self.__weightsList[targetIndex]
                del self.contentsList[targetIndex]
        elif mode == 'low':
            for x in range(length, 0, -1):
                targetIndex = b.getMinIndex(self.__weightsList)
                weight = self.__weightsList[targetIndex]
                contents = self.contentsList[targetIndex]
                newWeights.append(weight)
                newContents.append(contents)
                del self.__weightsList[targetIndex]
                del self.contentsList[targetIndex]
        else:
            print('Error: Improper sort mode for weighted dict.')
        self.__weightsList = newWeights
        self.contentsList = newContents
        self.genCumList()

    # Special alternative to the normal print method that prints contents and
    # their normal weights, instead of their cumulative weights.
    def displayWeights(self):
        counter = 0
        displayDict = {}
        for x in self.__weightsList:
            contents = self.contentsList[counter]
            displayDict[x] = contents
            counter += 1
        return str(displayDict)

    # Method for when the print function is called on a weighted list. It does
    # a quick conversion to display it as an actual dictionary, but it is not
    # in fact a dictionary.
    def __str__(self):
        counter = 0
        displayDict = {}
        for x in self.__cumulativeList:
            contents = self.contentsList[counter]
            displayDict[x] = contents
            counter += 1
        return str(displayDict)


# ==============================================================================
# ==============================================================================
# ==============================================================================

# This function simply generates a probability distribution (normal curved
# weightedDict) object based on a minimum and maximum.
def generateProbabilityDistribution(_minimum, _maximum=False):
    if _maximum == False:
        maximum = _minimum[1]
        minimum = _minimum[0]
    else:
        maximum = _maximum
        minimum = _minimum

    probRange = (maximum - minimum) + 1
    median = float(maximum - float(probRange / 2))
    valueList = []
    for i in range(probRange):
        valueList.append(minimum + i)

    weightList = []
    highestWeight = 0
    timeToSwitch = False
    for i in range(probRange):
        if (i + minimum <= median):
            weightList.append(i + 1)
        else:
            weightList.append((maximum - (i + minimum)) + 1)

    returnWeightedList = WeightedDict()
    for i in range(len(valueList)):
        returnWeightedList.w(weightList[i], valueList[i])

    return returnWeightedList
