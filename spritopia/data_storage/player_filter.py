from spritopia.data_storage.data_storage import d

'''
thisFilter = {
    "type": "and",
    "conditions": [
        {
            # Filters only for spriteIDs who have >= 30 Hesitation Tendency
            "type": "greater_than_or_equal_to",
            "domain": "Players",
            "field": "THesitat",
            "value": 30
        },
        {
            # Filters only for spriteIDs which have > 0.8 average steal
            "type": "greater_than",
            "domain": "Stats",
            "subdomain": "Averages",
            "field": "Steals",
            "value": 0.8
        },
        {
            # Filters only for spriteIDs which exist on the given roster
            "type": "special",
            "field": "is_on_roster",
            "value": "Premier"
        }
    ]
}
'''


#region === Condition Types ===

# All possible conditions.
def equals(playerValue,testValue):
    return playerValue == testValue
def does_not_equal(playerValue,testValue):
    return playerValue != testValue
def greater_than(playerValue,testValue):
    return playerValue > testValue
def greater_than_or_equal_to(playerValue,testValue):
    return playerValue >= testValue
def less_than(playerValue,testValue):
    return playerValue < testValue
def less_than_or_equal_to(playerValue,testValue):
    return playerValue <= testValue
def contains(playerValue,testValue):
    return testValue in playerValue
conditionTypeDict = {
    "equals": equals,
    "does_not_equal": does_not_equal,
    "greater_than": greater_than,
    "greater_than_or_equal_to": greater_than_or_equal_to,
    "less_than": less_than,
    "less_than_or_equal_to": less_than_or_equal_to,
    "contains": contains
}

#endregion === Condition Types ===

#region === Special Condition Types ===

def is_on_roster(value,spriteID):
    thisRosterDict = d.rosters.get(value,None)
    if(thisRosterDict):
        return spriteID in thisRosterDict["SpriteIDs"].values()
    else:
        return False
specialConditionTypeDict = {
    "is_on_roster": is_on_roster
}

#endregion === Special Condition Types ===

# Function to evaluate a single condition against the given spriteID
def evalCondition(condition : dict,spriteID):
    # Specifically for operator conditions such as "and" or "or".
    if(condition["type"] == "and"):
        conditionTruth = True
        for subCondition in condition["conditions"]:
            if(not evalCondition(condition=subCondition,spriteID=spriteID)):
                conditionTruth = False
                break
        return conditionTruth
    elif(condition["type"] == "or"):
        conditionTruth = False
        for subCondition in condition["conditions"]:
            if (evalCondition(condition=subCondition, spriteID=spriteID)):
                conditionTruth = True
                break
        return conditionTruth
    elif(condition["type"] == "not"):
        return not evalCondition(condition=condition["condition"],spriteID=spriteID)
    # Specifically for special condition types that don't adhere to normal logic.
    elif(condition["type"] == "special"):
        return specialConditionTypeDict[condition["field"]](value=condition["value"],spriteID=spriteID)
    # All other normal condition types.
    else:
        if(condition["domain"] == "Players"):
            thisPlayerValue = d.players[spriteID][condition["field"]]
        elif(condition["domain"] == "Stats"):
            try:
                thisPlayerValue = d.stats["Players"][spriteID][condition["subdomain"]][condition["field"]]
            except KeyError as e:
                if(spriteID in d.stats["Players"].keys()):
                    raise e
                else:
                    return False
        else:
            raise ValueError(f"Invalid condition domain: '{condition['domain']}'")

        return conditionTypeDict[condition["type"]](playerValue=thisPlayerValue,testValue=condition["value"])

# Function to return a list of all spriteIDs that conform to the given conditionDict.
def filterSpriteIDs(condition):
    filteredSpriteIDs = []
    for spriteID in d.players.keys():
        if(evalCondition(condition=condition,spriteID=spriteID)):
            filteredSpriteIDs.append(spriteID)
    return filteredSpriteIDs

