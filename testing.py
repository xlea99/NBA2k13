from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QFontDatabase
import sys
import os
import csv
from spritopia.utilities.misc import getKeyFromValue
from spritopia.players.archetypes import MAPPED_ATTRIBUTES

specialMappedAttributes = MAPPED_ATTRIBUTES
specialMappedAttributes["SSht3PT"] = "Shoot 3 Pt."
specialMappedAttributes["SShtInT"] = "Shoot in Traffic"
specialMappedAttributes["SOffHDrib"] = "Off-hand Dribbling"
specialMappedAttributes["SShtOfD"] = "Shoot Off Dribble"
specialMappedAttributes["SOnBallD"] = "On-Ball Defense"
specialMappedAttributes["SLayUp"] = "Layup"
specialMappedAttributes["SPstFdaway"] = "Post-Fadeaway"
specialMappedAttributes["SPstHook"] = "Post-Hook"
specialMappedAttributes["SOLowPost"] = "Low-Post Offense"
specialMappedAttributes["SDLowPost"] = "Low-Post Defense"



with open("NEWDAYDATA.csv","r") as f:
    fullDataDict = list(csv.DictReader(f))



allRankingsDict = {"Slayer": {}, "Vigilante": {}, "Medic": {}, "Guardian": {}, "Engineer": {}, "Director": {}}
for thisAttribute in fullDataDict:
    for archetype, archetypeRankingsDict in allRankingsDict.items():
        if(thisAttribute["Stat"] == "Height"):
            continue
        archetypeRankingsDict[int(thisAttribute[archetype])] = thisAttribute["Stat"]


allRankingsList = {"Slayer": [], "Vigilante": [], "Medic": [], "Guardian": [], "Engineer": [], "Director": []}
for archetype, rankingList in allRankingsList.items():
    for i in range(1,32):
        thisStatID = getKeyFromValue(dictionary=specialMappedAttributes,targetValue=allRankingsDict[archetype][i])
        rankingList.append(thisStatID)


for archetype,rankingList in allRankingsList.items():
    print(f"ARCH_{archetype.upper()}.attributeImportance = {rankingList}")