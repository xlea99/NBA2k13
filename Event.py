import BaseFunctions as b
import Helpers as h
import DataStorage
import lxml.etree as ET
import random

# This method constructs a new event element to be stored in the events root element.
def genEventElement(dataStorageObject=None):
    if(dataStorageObject is not None):
        d = dataStorageObject
    else:
        d = DataStorage.DataStorage()
        d.gauntletTable_Open()

    return d.gauntletTable_AddBlankEntry("EVENTS")
# These two methods simply construct a new effect or condition XML element, off of a rootTree element.
def effect(rootTree,effectString,effectText=None):
    newEffectElement = ET.SubElement(rootTree, "Effect")
    if(effectText is not None):
        newEffectElement.set("text", effectText)
    newEffectElement.text = effectString
    return newEffectElement
def condition(rootTree,conditionString):
    newConditionElement = ET.SubElement(rootTree, "Condition")
    newConditionElement.text = conditionString
    return newConditionElement



# Selects a player with > 0 tentacles and a positive opinion of someone else. They give a tentacle to
# a friend.
'''
def e_GestureOfGoodwill(dataStorageObject=None):
    if(dataStorageObject is not None):
        d = dataStorageObject
    else:
        d = DataStorage.DataStorage()
        d.gauntletTable_Open()

    eligibleBenefactors = d.gauntletTableRoot.xpath("./PLAYERS/ENTRY/Tentacles[text()>0]/following-sibling::Opinion[text()>=1]/..")
    if(len(eligibleBenefactors) == 0):
        return False
    benefactor = random.choice(eligibleBenefactors).attrib.get("ID")

    validBeneficiarys = d.gauntletTableRoot.xpath("//GAUNTLET/PLAYERS//ENTRY[@ID=" + str(benefactor) + "]/Opinion[text()>=1]")
    if(len(validBeneficiarys) == 0):
        return False
    beneficiary = random.choice(validBeneficiarys).attrib.get("of")

    benefactorName = h.getFullPlayerName(d.gauntletTableRoot.xpath("//GAUNTLET/PLAYERS//ENTRY[@ID=" + str(benefactor) + "]/SpriteID")[0].text)
    beneficiaryName = h.getFullPlayerName(d.gauntletTableRoot.xpath("//GAUNTLET/PLAYERS//ENTRY[@ID=" + str(beneficiary) + "]/SpriteID")[0].text)
    eventElement = genEventElement(dataStorageObject)
    eventElement.find("Splash").text = "A Gesture of Goodwill"
    effect(eventElement,"~//GAUNTLET/PLAYERS/ENTRY[@ID='" + str(benefactor) + "']/Tentacles~ += -1",effectText=benefactorName + " has decided, out of the kindness of his heart, to give his good friend " + beneficiaryName + " one of his tentacles.")
    effect(eventElement,"~//GAUNTLET/PLAYERS/ENTRY[@ID='" + str(beneficiary) + "']/Tentacles~ += 1")
    if(int(d.gauntletTableRoot.xpath("./PLAYERS/ENTRY[@ID=" + str(beneficiary) + "]/Opinion[@of=" + benefactor + "]")[0].text) < d.OPINION_MAX):
        effect(eventElement,"~//GAUNTLET/PLAYERS/ENTRY[@ID='" + str(beneficiary) + "']/Opinion[@of='" + str(benefactor) + "']~ += 1",effectText=beneficiaryName + "'s opinion of " + benefactorName + " has increased.")
'''


# This helper class manages the selection and deployment of events.
class GauntletEvents:

    def __init__(self,dataStorageObject=None):
        if(dataStorageObject is not None):
            self.d = dataStorageObject
        else:
            self.d = DataStorage.DataStorage()

        self.d.gauntletTable_Open()

        self.allEvents = [e_GestureOfGoodwill]


    def genRandomEvent(self):
        targetEvent = random.choice(self.allEvents)
        print(targetEvent)
        targetEvent(self.d)



class EventCompiler:

    def __init__(self,dataStorageObject = None):
        # First, we ensure a local data object is saved for quick processing.
        if(dataStorageObject is not None):
            self.d = dataStorageObject
        else:
            self.d = DataStorage.DataStorage()
        self.d.gauntletTable_Open()
        self.d.playersTable_Open()
        self.d.statsTable_Open()

        # This variable stores information about events currently happening.
        # Key values are displayed as big, splash text, while value values, when in
        # array form, are listed as bullet points below the splash.
        self.bulletin = {}

    def compileEvent(self,eventElement):
        pass

    # This method accepts a full condition, including and (&&) and or (||) operators, then returns
    # True or False based on whether the FULL CONDITION is true.
    def evaluateFullCondition(self,conditionString):
        conditionArray = []
        runningString = ""
        counter = -1
        parenthesisLevel = 0
        skipNext = False
        # First, we generate an array of conditions and operators.
        for c in conditionString:
            counter += 1
            if(skipNext):
                skipNext = False
                continue
            # If c is a parenthesis, for now, we append it and assume we've read
            # a full condition statement. Later on, we'll double check to make sure these
            # aren't internal parenthesis.
            if(c in "()"):
                if(runningString.strip() != ""):
                    conditionArray.append(runningString)
                conditionArray.append(c)
                runningString = ""
            # If c == & or c == |, we check if the next character is a &, meaning we've found an operator.
            elif(c in "&|"):
                if(c == "&"):
                    try:
                        if(conditionString[counter+1] == "&"):
                            if(runningString.strip() != ""):
                                conditionArray.append(runningString)
                            conditionArray.append("&&")
                            runningString = ""
                            skipNext = True
                        else:
                            runningString += c
                    except:
                        continue
                elif(c== "|"):
                    try:
                        if(conditionString[counter+1] == "|"):
                            if (runningString.strip() != ""):
                                conditionArray.append(runningString)
                            conditionArray.append("||")
                            runningString = ""
                            skipNext = True
                        else:
                            runningString += c
                    except:
                        continue
            # Otherwise, we simply append to runningString.
            else:
                runningString += c
        if (runningString.strip() != ""):
            conditionArray.append(runningString)

        # This submethod accepts a single condition string, given by the higher method from a CONDITION
        # element's truth string. It evaluates this single condition, then returns either True or False.
        # <Condition truth="~$WINNERS/Tentacles~ > (~//GAUNTLET/GLOBAL_VARIABLES/MaxTentacles~ - 6)">
        # Listed as a submethod due to the fact that it will never be used outside of this, to keep things
        # tidy.
        def evaluateSingleCondition(conditionString):
            leftSide = []
            rightSide = []
            operator = None

            counter = -1
            readingXPath = False
            readingString = False
            readingNumber = False
            readingLiteral = False
            skipNext = False
            runningString = ""
            for c in conditionString:
                counter += 1
                # If skipNext is set to True, we simply skip this character.
                if (skipNext):
                    skipNext = False
                # Do this when reading an Xpath
                elif (readingXPath):
                    # If we find a ~ character, and we're not reading a literal, that means we've
                    # reached the end of our XPath expression.
                    if (c == "~" and readingLiteral == False):
                        readingXPath = False
                        # Means we're still reading the left side
                        if (operator is None):
                            leftSide.append(self.processXPath(runningString).text)
                        else:
                            rightSide.append(self.processXPath(runningString).text)
                        runningString = ""
                    # If we're reading a literal, we append the next character no matter what
                    # it is, as it's a literal. There are some special cases listed below.
                    elif (readingLiteral):
                        readingLiteral = False
                        if (c == "n"):
                            runningString += "\n"
                        elif (c == "t"):
                            runningString += "\t"
                        else:
                            runningString += c
                    # If we find a \ character, that means we've found a literal, and the next
                    # character must be appended to runningString unconditionally.
                    elif (c == "\\"):
                        readingLiteral = True
                    # Otherwise, we simply append the character to runningString.
                    else:
                        runningString += c
                # Do this when reading a simple value, like "Walrus".
                elif (readingString):
                    # If c == " and readingLiteral is false, we've found the end of our
                    # string expression.
                    if (c == '"' and readingLiteral == False):
                        readingString = False
                        if (operator is None):
                            leftSide.append(runningString)
                        else:
                            rightSide.append(runningString)
                        runningString = ""
                    # If we're reading a literal, we append the next character no matter what
                    # it is, as it's a literal. There are some special cases listed below.
                    elif (readingLiteral):
                        readingLiteral = False
                        if (c == "n"):
                            runningString += "\n"
                        elif (c == "t"):
                            runningString += "\t"
                        else:
                            runningString += c
                    # If we find a \ character, that means we've found a literal, and the next
                    # character must be appended to runningString unconditionally.
                    elif (c == "\\"):
                        readingLiteral = True
                    else:
                        runningString += c
                # Do this when reading a number, like 5, -17, or 12.23
                elif (readingNumber):
                    # Numbers don't have as clear of an end - instead, we check if c is a
                    # space, newline, tab, final character, or parenthesis to determine if it's the end
                    # of a number.
                    if (c in " \t\n()+-/*" or c == conditionString[-1]):
                        readingNumber = False
                        # If c is a number, this is because it's also the last character, and we still need
                        # to append it.
                        if (b.isNumber(c)):
                            runningString += c
                        # Here we test to ensure that runningString actually contains a number.
                        if (b.isNumber(runningString)):
                            # A simple, somewhat sloppy way to determine if it's a float or int.
                            if ("." in runningString):
                                actualNumber = float(runningString)
                            else:
                                actualNumber = int(runningString)
                            # Finally, we test which side to append to.
                            if (operator is None):
                                leftSide.append(actualNumber)
                            else:
                                rightSide.append(actualNumber)
                            runningString = ""
                        else:
                            raise InvalidNumber(runningString)
                        # Finally, we test for some special cases of if c is a parenthesis or arithmetic
                        # operator.
                        if (c in "()+-*/"):
                            if (operator is None):
                                leftSide.append(c)
                            else:
                                rightSide.append(c)


                    # Since there are no special literal characters for numbers, if we haven't
                    # reached the end of the number, we simply append to runningString.from
                    else:
                        runningString += c
                # If c == ~ and all readingExpressions are False, that means we've found a
                # new XPath expression.
                elif (c == "~"):
                    readingXPath = True
                # If c == " and all readingExpressions are False, that means we've found a
                # new string.
                elif (c == '"'):
                    readingString = True
                # If c == (isnum) and all readingExpressions are False, that means we've
                # found a new number.
                elif (b.isNumber(c)):
                    runningString += c
                    # If c also happens to be the last character of the string, we need to
                    # instantly append this number and close readingNumber again.
                    if (c == conditionString[-1]):
                        # It can only be an int, since this number is a single character.
                        actualNumber = int(runningString)
                        # We test which side to append to.
                        if (operator is None):
                            leftSide.append(actualNumber)
                        else:
                            rightSide.append(actualNumber)
                        runningString = ""
                    # Otherwise, we proceed as normal.
                    else:
                        readingNumber = True
                # We simply append our parenthesis to the appropriate side if we find
                # one.
                elif (c in "()"):
                    if (operator is None):
                        leftSide.append(c)
                    else:
                        rightSide.append(c)
                # If we find c == =, we've likely found our operator.
                elif (c == "="):
                    # This is an equality operator done correctly.
                    if (conditionString[counter + 1] == "="):
                        operator = "=="
                        skipNext = True
                    else:
                        raise InvalidOperator(c + conditionString[counter + 1])
                # If c == > or <, we've also likely found our operator.
                elif (c == ">" or c == "<"):
                    if (conditionString[counter + 1] == "="):
                        operator = c + "="
                        skipNext = True
                    else:
                        operator = c
                # If c == ! and the next character is =, again we've found our operator.
                elif (c == "!"):
                    if (conditionString[counter + 1] == "="):
                        operator = "!="
                        skipNext = True
                    else:
                        raise InvalidOperator(c + conditionString[counter + 1])
                # If c == +, *, /, or -, we've likely found an arithmetic operator between two
                # sub expressions.
                elif (c in "+*/-"):
                    # These operators are simple, in that they always are arithmetic. We simply
                    # append to appropriate side and move on.
                    if (c in "+*/"):
                        if (operator is None):
                            leftSide.append(c)
                        else:
                            rightSide.append(c)
                    # - is somewhat trickier, as it could be the subtraction operator OR the beginning
                    # of a negative number. We test for both here.
                    elif (c == "-"):
                        # This means we've found a negative number.
                        if (b.isNumber(conditionString[counter + 1])):
                            runningString += "-"
                            readingNumber = True
                        # Otherwise, this is a subtraction operator.
                        else:
                            if (operator is None):
                                leftSide.append(c)
                            else:
                                rightSide.append(c)
                # If c is simply empty space, we just skip it.
                elif (c == " "):
                    continue
                # Otherwise, this character is a syntax error.
                else:
                    raise UnexpectedCharacter(c, counter)

            leftSideValue = self.calculateExpressionValue(leftSide)
            rightSideValue = self.calculateExpressionValue(rightSide)
            if (operator == "=="):
                return (leftSideValue == rightSideValue)
            elif (operator == "!="):
                return (leftSideValue != rightSideValue)
            elif (operator == ">"):
                return (leftSideValue > rightSideValue)
            elif (operator == "<"):
                return (leftSideValue < rightSideValue)
            elif (operator == ">="):
                return (leftSideValue >= rightSideValue)
            elif (operator == "<="):
                return (leftSideValue <= rightSideValue)


        simplifiedConditionArray = []
        # Now, we convert all string expressions into booleans before we calculate the combined
        # truth value of the entire expression.
        for unprocessedItem in conditionArray:
            if(unprocessedItem != "&&" and unprocessedItem != "||" and unprocessedItem not in "()"):
                simplifiedConditionArray.append(evaluateSingleCondition(unprocessedItem.strip()))
            else:
                simplifiedConditionArray.append(unprocessedItem)

        # This sub-method accepts a multi-condition array, complete with will simple booleans and operators
        # like this: (True && False) || False, and returns either true or false based on its actual
        # result. It doesn't need to be used anywhere else and could potentially add confusion to include as
        # a class method, so it's put here for simplicity.
        def evaluateFullConditionArray(_conditionArray):
            # First, we simply calculate what the highest "parenthesis value" is. In other words,
            # what the highest priority part of the expression is to compute.
            highestParenthesisValue = 0
            parenthesisValue = 0
            for value in _conditionArray:
                if (value == "("):
                    parenthesisValue += 1
                    if (parenthesisValue > highestParenthesisValue):
                        highestParenthesisValue = parenthesisValue
                elif (value == ")"):
                    parenthesisValue -= 1

            # Now, we process the most important section of the expressionArray.
            resultConditionArray = []
            counter = -1
            parenthesisValue = 0
            currentTruth = None
            nextOperator = None
            for item in _conditionArray:
                counter += 1
                if (item == "("):
                    parenthesisValue += 1
                    if (parenthesisValue != highestParenthesisValue):
                        resultConditionArray.append("(")
                    continue
                elif (item == ")"):
                    if (parenthesisValue == highestParenthesisValue):
                        resultConditionArray.append(currentTruth)
                        currentTruth = None
                        nextOperator = None
                    else:
                        resultConditionArray.append(")")
                    parenthesisValue -= 1
                    continue
                # Now that we've found our highPrio section, we begin calculating it.
                if (parenthesisValue == highestParenthesisValue):
                    if (str(item) == "&&" or str(item) == "||"):
                        nextOperator = item
                    else:
                        if (nextOperator is None):
                            if (currentTruth is not None):
                                raise JoinedBooleans(_conditionArray)
                            else:
                                currentTruth = item
                        else:
                            if (nextOperator == "&&"):
                                if (currentTruth and item):
                                    currentTruth = True
                                else:
                                    currentTruth = False
                            elif (nextOperator == "||"):
                                if (currentTruth or item):
                                    currentTruth = True
                                else:
                                    currentTruth = False
                else:
                    resultConditionArray.append(item)

            # If HPV was 0, the value wasn't appended as no closing parenthesis was found,
            # so we need to do that here.
            if (highestParenthesisValue == 0):
                resultConditionArray.append(currentTruth)



            # If HPV was not 0, that means there's still more of this expression to
            # calculate at lower priority. We now do this using recursion, until we reach HPV
            # of 0.
            if (highestParenthesisValue != 0):
                return evaluateFullConditionArray(resultConditionArray)
            else:
                return resultConditionArray[0]

        return evaluateFullConditionArray(simplifiedConditionArray)

    # This method calculates the actual value of a single "side" of an argument. These arguments
    # may be simple, single expressions, or may contain complex expressions like xpaths and arithmetic
    # operators. Accepts an array like this: [7, '*', '(', 5, '+', 2, ')'] to represent 7 * (5+2)
    def calculateExpressionValue(self,expressionArray):
        # First, we simply calculate what the highest "parenthesis value" is. In other words,
        # what the highest priority part of the expression is to calculate.
        highestParenthesisValue = 0
        parenthesisValue = 0
        for value in expressionArray:
            if(value == "("):
                parenthesisValue += 1
                if(parenthesisValue > highestParenthesisValue):
                    highestParenthesisValue = parenthesisValue
            elif(value == ")"):
                parenthesisValue -= 1

        # Now, we process the most important section of the expressionArray.
        resultExpressionArray = []
        counter = -1
        parenthesisValue = 0
        runningValue = None
        calculatingString = False
        calculatingNumber = False
        nextOperator = None
        for value in expressionArray:
            counter += 1
            if (value == "("):
                parenthesisValue += 1
                continue
            elif (value == ")"):
                if(parenthesisValue == highestParenthesisValue):
                    if(resultExpressionArray is not None):
                        resultExpressionArray.append(runningValue)
                    runningValue = None
                    calculatingString= False
                    calculatingNumber = False
                    nextOperator = None
                parenthesisValue -= 1
                continue
            # Now that we've found our highPrio section, we begin calculating it.
            if(parenthesisValue == highestParenthesisValue):
                if(str(value) in "+-/*"):
                    nextOperator = value
                elif(str(type(value)) == "<class 'str'>"):
                    if(not calculatingString):
                        if(calculatingNumber):
                            # The only case in which a number and a string should appear
                            # together is for multiplicative concatenation.
                            if(nextOperator == "*"):
                                calculatingNumber = False
                                calculatingString = True
                                runningValue = runningValue * value
                                continue
                            # Otherwise, this is a MixedType error.
                            else:
                                raise MixedTypeCalculation(expressionArray)
                        else:
                            calculatingString = True
                    if(nextOperator == "+" or nextOperator is None):
                        if(runningValue is not None):
                            runningValue = str(runningValue) + value
                        else:
                            runningValue = value
                    else:
                        raise InvalidStringArithmetic(nextOperator)
                elif(str(type(value)) == "<class 'int'>" or str(type(value)) == "<class 'float'>"):
                    if(not calculatingNumber):
                        if(calculatingString):
                            raise MixedTypeCalculation(expressionArray)
                        else:
                            calculatingNumber = True
                    if(nextOperator is None):
                        runningValue = value
                    elif(nextOperator == "+"):
                        runningValue += value
                    elif(nextOperator == "-"):
                        runningValue = runningValue - value
                    elif(nextOperator == "*"):
                        runningValue = runningValue * value
                    elif(nextOperator == "/"):
                        runningValue = runningValue / value
            else:
                if(value is not None):
                    resultExpressionArray.append(value)

        # If HPV was 0, the value wasn't appended as no closing parenthesis was found,
        # so we need to do that here.
        if(highestParenthesisValue == 0):
            if(runningValue is not None):
                resultExpressionArray.append(runningValue)



        # If HPV was not 0, that means there's still more of this expression to
        # calculate at lower priority. We now do this using recursion, until we reach HPV
        # of 0.
        if(highestParenthesisValue != 0):
            return self.calculateExpressionValue(resultExpressionArray)
        else:
            return resultExpressionArray[0]

    # This method will read the content written within a single "Effect" element, if it has one,
    # and act upon its contents accordingly. For example, if the Effect element's contents
    # contains an XPath and operator, it'll process that XPath so that it actually
    # effects the Roster.
    def processEffectString(self,effectString):
        currentElement = None
        operator = None


        parenthesisLevel = 0
        readingXpath = False
        readingLiteral = False
        runningString = ""
        for c in effectString:
            # Do this if we're currently reading an Xpath
            if(readingXpath):
                # If c is a ~ and we're not reading a literal, that means
                # we've reached the end of this xpath expression.
                if(c == "~" and readingLiteral == False):
                    readingXpath = False
                    newElement = self.processXPath(runningString)
                    if(currentElement is not None):
                        if(operator is not None):
                            if(str(type(newElement)) == "<class 'lxml.etree._Element'>"):
                                if(operator == "="):
                                    currentElement.text = newElement.text
                                elif (operator == "+="):
                                    if(b.isNumber(newElement.text) and b.isNumber(currentElement.text)):
                                        currentElement.text = str(float(currentElement.text) + float(newElement.text))
                                    else:
                                        currentElement.text = currentElement.text + newElement.text
                            else:
                                if(operator == "="):
                                    currentElement = newElement.text
                                elif (operator == "+="):
                                    if(b.isNumber(newElement.text) and b.isNumber(currentElement)):
                                        currentElement.text = str(float(currentElement) + float(newElement.text))
                                    else:
                                        currentElement = currentElement + newElement.text
                        else:
                            raise OperatorRequired(effectString)
                    else:
                        currentElement = newElement
                    runningString = ""
                # Otherwise, we simply add the character to the runningString.
                else:
                    runningString += c
            # Do this if we're currently reading a literal value.
            elif(readingLiteral):
                pass
            # If c == ~, we've found the beginning of an xpath.
            elif(c == '~' and readingXpath == False):
                readingXpath = True

    # This method takes an xpath accessor value, like ~//GAUNTLET/PLAYERS/ENTRY[@ID=2]/Tentacles~
    # and returns the result of its xpath.
    def processXPath(self, accessor):
        rootName = ""

        if (accessor.startswith("//")):
            rootName = accessor.split('//')[1].split("/")[0]
        else:
            print("ERROR: xPath accessors beginning with anything other than '//' are currently not supported!")
            return False

        rootElementMap = {
            "GAUNTLET": self.d.gauntletTableRoot,
            "PLAYERS": self.d.playersTableRoot,
            "STATS": self.d.statsTableRoot
        }

        if rootName not in rootElementMap:
            raise InvalidRootName(rootName)

        rootElement = rootElementMap[rootName]

        literalXpath = accessor.strip('~')
        return rootElement.xpath(literalXpath)


class InvalidRootName(TypeError):
    def __init__(self,rootName):
        super().__init__("Invalid rootName given: " + str(rootName) + " is not a valid file to read from.")
class OperatorRequired(TypeError):
    def __init__(self,expressionString):
        super().__init__("Expression contains multiple xpath values with no operator: " + expressionString)
class InvalidOperator(TypeError):
    def __init__(self,operatorString):
        if(operatorString.startswith("=")):
            super().__init__("Invalid operator detected: " + operatorString + " | did you mean == for equality operator?")
        else:
            super().__init__("Invalid operator detected: " + operatorString)
class InvalidNumber(TypeError):
    def __init__(self,numberString):
        super().__init__("Invalid number in expression: " + numberString)
class UnexpectedCharacter(TypeError):
    def __init__(self,unexpectedCharacter,position):
        super().__init__("Unexpected character '" + unexpectedCharacter + "' found at position " + str(position) + ".")
class MixedTypeCalculation(TypeError):
    def __init__(self,expressions):
        super().__init__("Tying to combine string and number operations into one expression: " + expressions)
class InvalidStringArithmetic(TypeError):
    def __init__(self,operator):
        super().__init__("Cannot perform '" + str(operator) + "' on two strings.")
class JoinedBooleans(TypeError):
    def __init__(self,conditionArray):
        super().__init__("Found two booleans not joined by an operator in this expression: " + str(conditionArray))






# Serves as a sort of struct for automating the process of adding and processing
# events on the XML file.
class Event:

    def __init__(self,d):
        self.d = d
        self.titleSplash = None

d = DataStorage.DataStorage()
GAUNTLET = {}


GAUNTLET = {"PLAYERS" : {}}

# This method parses the entire Gauntlet.xml file, and stores its contents in the
# GAUNTLET dictionary. This will overwrite the current contents of the dictionary,
# and can later be used to store any changes made by events into the Gauntlet file.
#
# This function is 'dumb' in how it reads the XML file - it has only a few rules.
# If an element is found anywhere in the file, it adds a key with the name of that Element
# under as a dictionary entry under the subelement it exists within. If an element has no
# subelements, it is instead added as a simple value.
def element_to_dict(element):
    result = {}
    result.update(parse_attributes(element))

    # if the element has subelements, recursively convert them to dictionaries
    result['subelements'] = []
    for child in element:
        subelement = {}
        subelement.update(parse_attributes(child))
        if len(child) == 0:
            subelement['text'] = child.text
        else:
            subelement['subelements'] = element_to_dict(child)
        result['subelements'].append({child.tag: subelement})
    return result

def parse_attributes(element):
    result = {}
    for key, value in element.attrib.items():
        result[key] = value
    return result



d.gauntletTable_Open()
print(element_to_dict(d.gauntletTableRoot))


def GestureOfGoodwill(rootEvent):
    beneficiaryID = None
    benefactorID = None
    randPlayerList = random.shuffle(list(GAUNTLET['PLAYERS'].keys()))
    for randomPlayerKey in randPlayerList:
        for playerToFindOpinionOfKey in randPlayerList[::-1]:
            if(GAUNTLET['PLAYERS'][randomPlayerKey]['Opinions'][playerToFindOpinionOfKey] >= 1):
                beneficiaryID = randomPlayerKey
                benefactorID = playerToFindOpinionOfKey
                break
    if(benefactorID is None):
        return False
    addSplash(getPlayerName(benefactorID) + " has decided, out of the kindness of his heart, to give his good friend " + getPlayerName(beneficiaryID) + " one of his tentacles.")
    addEffect(rootEvent,"GAUNTLET['PLAYERS']["+benefactorID+"]['Tentacles'] -= 1")
    addEffect(rootEvent,"GAUNTLET['PLAYERS']["+beneficiaryID+"]['Tentacles'] += 1")
    if(GAUNTLET['PLAYERS'][beneficiaryID]['Opinions'][benefactorID] < MAX_OPINION):
        addEffect(rootEvent,"GAUNTLET['PLAYERS']["+beneficiaryID+"]['Opinions'][benefactorID] += 1")
    return True











'''
testString = "//GAUNTLET/PLAYERS/ENTRY[@ID=2]/Tentacles"
ec = EventCompiler()
print(type(ec.processXPath(testString)[0]))
'''
#d = DataStorage.DataStorage()
#g = GauntletEvents(d)
#g.genRandomEvent()
#d.gauntletTable_Save()




#hippoTest = '(("flounder" == "flounder" && "walrus" != "walrus") || 16/3 > 4) && (("flounder" == "flounder" && "walrus" != "walrus") || 16/4 > 4)'
#ec = EventCompiler()
#for i in range(5000):
#    print(str(ec.evaluateFullCondition(hippoTest)) + " | " + str(i))



#test = "(5+1) - 5 *5"
#print(eval(test))
