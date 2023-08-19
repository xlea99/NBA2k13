import random as r


# The Weighted Dictionary is a special type of dictionary that uses weights to
# represent frequency of values as if they appeared multiple times within a
# dictionary. This allows us to use probability- if a value of 'guppy' has a
# weight of 4 in a Weighted Dictionary who's total value is 16, then 'guppy'
# makes up 25% of that dictionary and if a value was to be randomly selected
# from it, there is a 25% chance that that value will be 'guppy'.
class WeightedDict:

    # Init method simply initializes the totalValue and __valueDictionary for
    # later use.
    def __init__(self):
        self.totalValue = 0
        self.__valueDictionary = {}

    # This method simply adds a single entry with a given weight.
    def add(self,entry,weight):
        if(weight == 0):
            raise EmptyEntryError(entry)
        if(str(type(weight)) != "<class 'int'>"):
            raise InvalidWeightTypeError(weight)
        if(entry in self.__valueDictionary):
            self.__valueDictionary[entry] = self.__valueDictionary.get(entry) + weight
        else:
            self.__valueDictionary[entry] = weight
        self.totalValue += weight

    # This method simply removes an entry from the weightedDicitonary.
    def remove(self,entry):
        self.totalValue -= self.__valueDictionary.get(entry)
        self.__valueDictionary.pop(entry)

    # This method returns a random value from the dictionary, using the listed
    # weights (so a value with weight 4 is twice as likely as a value with weight
    # 2.)
    def pull(self):
        pullValue = r.randrange(1,self.totalValue + 1)

        runningTotal = 0
        for key in self.__valueDictionary:
            runningTotal += self.__valueDictionary.get(key)
            if(runningTotal >= pullValue):
                return key

    # Same as regular pull, except the value is removed.
    def hatPull(self):
        thisPull = self.pull()
        self.remove(thisPull)
        return thisPull

    # Method for when the print function is called on a weighted list. It does
    # a quick conversion to display it as an actual dictionary, but it is not
    # in fact a dictionary.
    def __str__(self):
        return str(self.__valueDictionary)

# ==============================================================================
# ==============================================================================
# ==============================================================================

class WeightedDictError(TypeError):
    pass
class InvalidWeightTypeError(WeightedDictError):
    def __init__(self,weight):
        super().__init__("Invalid weight of " + str(weight) + "! Weight should be int, given value is " + str(type(weight)))
class EmptyEntryError(WeightedDictError):
    def __init__(self,entry):
        super().__init__("Can not add an entry (" + str(entry) + ") with a weight of 0!")


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
    for i in range(probRange):
        if (i + minimum <= median):
            weightList.append(i + 1)
        else:
            weightList.append((maximum - (i + minimum)) + 1)

    returnWeightedList = WeightedDict()
    for i in range(len(valueList)):
        returnWeightedList.add(valueList[i],weightList[i])

    return returnWeightedList