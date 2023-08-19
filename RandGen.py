import BaseFunctions as b
import random
import os
import time
import chardet




# This method simply reads all races in Race.txt into the raceDict variable.
def readAllRaces(raceFile = f"{b.paths.randGen}\\Players\\Race.txt"):
    pass
class Race:

    def __init__(self,raceName):
        self.name = raceName
        self.skinColorRange = [0,5]
        self.CAPRanges = {"HParam1" : [-255,255],
                          "HParam2" : [-255,255],
                          "HdBrwHght" : [-255,255],
                          "HdBrwWdth" : [-255,255],
                          "HdBrwSlpd" : [-255,255],
                          "HdNkThck" : [-255,255],
                          "HdNkFat" : [-255,255],
                          "HdChnLen" : [-255,255],
                          "HdChnWdth" : [-255,255],
                          "HdChnProt" : [-255,255],
                          "HdJawSqr" : [-255,255],
                          "HdJawWdth" : [-255,255],
                          "HdChkHght" : [-255,255],
                          "HdChkWdth" : [-255,255],
                          "HdChkFull" : [-255,255],
                          "HdDefinit" : [-255,255],
                          "MtULCurve" : [-255,255],
                          "MtULThick" : [-255,255],
                          "MtULProtr" : [-255,255],
                          "MtLLCurve" : [-255,255],
                          "MtLLThick" : [-255,255],
                          "MtLLProtr" : [-255,255],
                          "MtSzHght" : [-255,255],
                          "MtSzWdth" : [-255,255],
                          "MtCrvCorn" : [-255,255],
                          "ErHeight" : [-255,255],
                          "ErWidth" : [-255,255],
                          "ErEarLobe" : [-255,255],
                          "ErTilt" : [-255,255],
                          "NsNsHght" : [-255,255],
                          "NsNsWdth" : [-255,255],
                          "NsNsProtr" : [-255,255],
                          "NsBnBridge" : [-255,255],
                          "NsBnDefin" : [-255,255],
                          "NsBnWdth" : [-255,255],
                          "NsTipHght" : [-255,255],
                          "NsTipWdth" : [-255,255],
                          "NsTipTip" : [-255,255],
                          "NsTipBnd" : [-255,255],
                          "NsNtHght" : [-255,255],
                          "NsNtWdth" : [-255,255],
                          "EsFrmOpen" : [-255,255],
                          "EsFrmSpac" : [-255,255],
                          "EsFrmLwEl" : [-255,255],
                          "EsFrmUpEl" : [-255,255],
                          "EsPlcHght" : [-255,255],
                          "EsPlcWdth" : [-255,255],
                          "EsPlcRot" : [-255,255],
                          "EsPlcProt" : [-255,255],
                          "EsShpOtEl" : [-255,255],
                          "EsShpInEl" : [-255,255]}

    # This function acc
    def convertFancyDict(self):
        pass


print(b.selectRandomFromList(filePath=f"{b.paths.randGen}/WordLists/Adjectives/Adjectives.txt",selectionCount = 200000,hatPick=True))
