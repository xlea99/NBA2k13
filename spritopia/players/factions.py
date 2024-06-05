import csv
import sqlite3
import os
import random
from spritopia.common.paths import paths
from spritopia.common.logger import log
from spritopia.utilities import rsuite

#region === Database Maintenance ===

# Helper dict for converting the names of race values on the Google sheet to RedMC values.
RACES_ATTRIBUTES = {
    "Skin Color" : "SkinTone",
    "Blackness" : "HParam1",
    "Asianness" : "HParam2",
    "Brow Height" : "HdBrwHght",
    "Brow Width" : "HdBrwWdth",
    "Brow Sloped" : "HdBrwSlpd",
    "Neck Thickness" : "HdNkThck",
    "Neck Fat" : "HdNkFat",
    "Chin Length" : "HdChnLen",
    "Chin Width" : "HdChnWdth",
    "Chin Protrusion" : "HdChnProt",
    "Jaw Squareness" : "HdJawSqr",
    "Jaw Width" : "HdJawWdth",
    "Cheek Height" : "HdChkHght",
    "Cheek Width" : "HdChkWdth",
    "Cheek Fullness" : "HdChkFull",
    "Head Definition" : "HdDefinit",
    "Upper Lip Curve" : "MtULCurve",
    "Upper Lip Thickness" : "MtULThick",
    "Upper Lip Protrusion" : "MtULProtr",
    "Lower Lip Curve" : "MtLLCurve",
    "Lower Lip Thickness" : "MtLLThick",
    "Lower Lip Protrusion" : "MtLLProtr",
    "Mouth Size Height" : "MtSzHght",
    "Mouth Size Width" : "MtSzWdth",
    "Mouth Corners Curve" : "MtCrvCorn",
    "Ear Height" : "ErHeight",
    "Ear Width" : "ErWidth",
    "Ear Lobe" : "ErEarLobe",
    "Ear Lobe Tilt" : "ErTilt",
    "Nose Height" : "NsNsHght",
    "Nose Width" : "NsNsWdth",
    "Nose Protrusion" : "NsNsProtr",
    "Nose Bone Bridge" : "NsBnBridge",
    "Nose Bone Definition" : "NsBnDefin",
    "Nose Bone Width" : "NsBnWdth",
    "Nose Tip Height" : "NsTipHght",
    "Nose Tip Width" : "NsTipWdth",
    "Nose Tip Size" : "NsTipTip",
    "Nose Tip Bend" : "NsTipBnd",
    "Nostrils Height" : "NsNtHght",
    "Nostrils Width" : "NsNtWdth",
    "Eyes Openness" : "EsFrmOpen",
    "Eyes Spacing" : "EsFrmSpac",
    "Lower Eyelid Shape" : "EsFrmLwEl",
    "Upper Eyelid Shape" : "EsFrmUpEl",
    "Eye Placement Height" : "EsPlcHght",
    "Eye Placement Width" : "EsPlcWdth",
    "Eye Rotation" : "EsPlcRot",
    "Eye Protrusion" : "EsPlcProt",
    "Eyelid Outer" : "EsShpOtEl",
    "Eyelid Inner" : "EsShpInEl"
}
# Helper dicts for correctly typing each table attribute
GEAR_TYPES_ATTRIBUTES = {"Symmetrical Type" : "Text"}
GEAR_ITEMS_ATTRIBUTES = {"ID" : "Integer"}
GEAR_SETS_ATTRIBUTES = {"Basic Gear Set" : "Integer", "Gear Items" : "Text", "Symmetry" : "Text", "Subsets" : "Text", "Subset Bucket" : "Text"}
FACTIONS_ATTRIBUTES = {"Race" : "Text",
                       "Backstory Modifier" : "Text",
                       "Buckets" : "Text",
                       "Description" : "Text",
                       "Generatable" : "Integer",
                       "Special Gear Sets" : "Text",
                       "Basic Gearset Chance" : "Real",
                       "Hair Style" : "Text",
                       "Hair Color" : "Text",
                       "Beard" : "Text",
                       "Goatee" : "Text",
                       "Moustache" : "Text",
                       "Facial Hair Probability" : "Real",
                       "Facial Hair Color" : "Text",
                       "Hair Color Match Prob" : "Real",
                       "Primary FN" : "Text",
                       "Secondary FN" : "Text",
                       "FN Ratio" : "Real",
                       "Primary LN" : "Text",
                       "Secondary LN" : "Text",
                       "LN Ratio" : "Real",
                       "Symmetrical Name Chance" : "Real",
                       "Tattoo Probability" : "Real",
                       "Tattoo Density" : "Text",
                       "Tattoo Symmetry" : "Integer",
                       "Icon" : "Text"}
NAME_LISTS_ATTRIBUTES = {"Value" : "Text","Symmetry" : "Text"}
HAIR_ATTRIBUTES = {"ID" : "Integer"}
TATTOO_ATTRIBUTES = {"Max ID" : "Integer","Symmetry" : "Integer"}
HAIR_COLOR_ATTRIBUTES = {"ID" : "Integer"}
GOATEE_ATTRIBUTES = {"ID" : "Integer"}
MOUSTACHE_ATTRIBUTES = {"ID" : "Integer"}
BEARD_ATTRIBUTES = {"ID" : "Integer"}
FACIAL_HAIR_COLOR_ATTRIBUTES = {"ID" : "Integer"}

# This function generates a new, empty Factions database with all appropriate tables.
# OVERWRITES EXISTING DB.
def genBlankFactionsDatabase(dbPath):
    if(os.path.exists(dbPath)):
        os.remove(dbPath)
    open(dbPath,"a").close()

    conn = sqlite3.connect(dbPath)
    cursor = conn.cursor()

    query = "CREATE TABLE 'Races' ('Race' TEXT NOT NULL UNIQUE,"
    for colName in RACES_ATTRIBUTES.values():
        query += f"'{colName}_Min' INTEGER,"
        query += f"'{colName}_Max' INTEGER,"
    query += "PRIMARY KEY('Race'));"
    cursor.execute(query)

    query = "CREATE TABLE 'GearTypes' ('Name' TEXT NOT NULL UNIQUE,"
    for colName,colType in GEAR_TYPES_ATTRIBUTES.items():
        query += f"'{colName}' {colType},"
    query += "PRIMARY KEY('Name'));"
    cursor.execute(query)

    query = "CREATE TABLE 'GearItems' ('Name' TEXT NOT NULL, 'Gear Type' TEXT NOT NULL, "
    for colName,colType in GEAR_ITEMS_ATTRIBUTES.items():
        query += f"'{colName}' {colType},"
    query += "PRIMARY KEY('Name','Gear Type'));"
    cursor.execute(query)

    query = "CREATE TABLE 'GearSets' ('Name' TEXT NOT NULL UNIQUE,"
    for colName,colType in GEAR_SETS_ATTRIBUTES.items():
        query += f"'{colName}' {colType},"
    query += "PRIMARY KEY('Name'));"
    cursor.execute(query)

    query = "CREATE TABLE 'Factions' ('Name' TEXT NOT NULL UNIQUE,"
    for colName,colType in FACTIONS_ATTRIBUTES.items():
        query += f"'{colName}' {colType},"
    query += "PRIMARY KEY('Name'));"
    cursor.execute(query)

    query = "CREATE TABLE 'NameLists' ('Name' TEXT NOT NULL UNIQUE,"
    for colName,colType in NAME_LISTS_ATTRIBUTES.items():
        query += f"'{colName}' {colType},"
    query += "PRIMARY KEY('Name'));"
    cursor.execute(query)

    query = "CREATE TABLE 'Hair' ('Name' TEXT NOT NULL UNIQUE,"
    for colName,colType in HAIR_ATTRIBUTES.items():
        query += f"'{colName}' {colType},"
    query += "PRIMARY KEY('Name'));"
    cursor.execute(query)

    query = "CREATE TABLE 'Tattoo' ('Name' TEXT NOT NULL UNIQUE,"
    for colName,colType in TATTOO_ATTRIBUTES.items():
        query += f"'{colName}' {colType},"
    query += "PRIMARY KEY('Name'));"
    cursor.execute(query)

    query = "CREATE TABLE 'HairColor' ('Name' TEXT NOT NULL UNIQUE,"
    for colName,colType in HAIR_COLOR_ATTRIBUTES.items():
        query += f"'{colName}' {colType},"
    query += "PRIMARY KEY('Name'));"
    cursor.execute(query)

    query = "CREATE TABLE 'Goatee' ('Name' TEXT NOT NULL UNIQUE,"
    for colName,colType in GOATEE_ATTRIBUTES.items():
        query += f"'{colName}' {colType},"
    query += "PRIMARY KEY('Name'));"
    cursor.execute(query)

    query = "CREATE TABLE 'Moustache' ('Name' TEXT NOT NULL UNIQUE,"
    for colName,colType in MOUSTACHE_ATTRIBUTES.items():
        query += f"'{colName}' {colType},"
    query += "PRIMARY KEY('Name'));"
    cursor.execute(query)

    query = "CREATE TABLE 'Beard' ('Name' TEXT NOT NULL UNIQUE,"
    for colName,colType in BEARD_ATTRIBUTES.items():
        query += f"'{colName}' {colType},"
    query += "PRIMARY KEY('Name'));"
    cursor.execute(query)

    query = "CREATE TABLE 'FacialHairColor' ('Name' TEXT NOT NULL UNIQUE,"
    for colName,colType in FACIAL_HAIR_COLOR_ATTRIBUTES.items():
        query += f"'{colName}' {colType},"
    query += "PRIMARY KEY('Name'));"
    cursor.execute(query)

    conn.commit()
    log.info("Built new Factions.db database")
# Helper methods for updating the Factions.db file with the CSV files stored at Factions/CSVs.
def updateRaces():
    with open(paths["factions"] / "CSVs/New Day of 2K - Races.csv") as f:
        reader = csv.DictReader(f)
        data = [row for row in reader]

    conn = sqlite3.connect(paths["factions"] / "Factions.db")
    cursor = conn.cursor()

    # Empty races table
    cursor.execute("DELETE FROM Races")

    uniqueRaces = []
    for race in data:
        raceName = race["Race"].split("_Max")[0].split("_Min")[0]
        if(raceName not in uniqueRaces):
            uniqueRaces.append(raceName)

    for raceName in uniqueRaces:
        cursor.execute("INSERT INTO Races (Race) VALUES (?)",(raceName,))

    for race in data:
        attributes = ""
        holders = ""
        vals = []

        if("_Max" in race["Race"]):
            isMax = "_Max"
        else:
            isMax = "_Min"

        for raceAttr,raceValue in race.items():
            if(raceAttr == "Race"):
                continue
            attributes += f", {RACES_ATTRIBUTES[raceAttr]}{isMax} = ?"
            holders += ", ?"
            vals.append(int(raceValue))

        fullQuery = f"UPDATE Races SET {attributes.lstrip(', ')} WHERE Race = '{race['Race'].split('_Max')[0].split('_Min')[0]}'"
        cursor.execute(fullQuery,tuple(vals))

    conn.commit()
    conn.close()
def updateGearTypes():
    with open(paths["factions"] / "CSVs/Gear Types-Grid view.csv","r",encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        data = [row for row in reader]

    conn = sqlite3.connect(paths["factions"] / "Factions.db")
    cursor = conn.cursor()

    # Empty and refill the table
    cursor.execute("DELETE FROM GearTypes")
    for entry in data:
        cursor.execute("INSERT INTO GearTypes (Name) VALUES (?)",(entry["Name"],))


    for entry in data:
        attributes = ""
        holders = ""
        vals = []

        for attr in GEAR_TYPES_ATTRIBUTES.keys():
            if(attr == "Name"):
                continue
            attributes += f", '{attr}' = ?"
            holders += ", ?"
            vals.append(entry[attr])

        fullQuery = f"UPDATE GearTypes SET {attributes.lstrip(', ')} WHERE Name = '{entry['Name']}'"
        cursor.execute(fullQuery,tuple(vals))

    conn.commit()
    conn.close()
def updateGearItems():
    with open(paths["factions"] / "CSVs/Gear Items-Grid view.csv","r",encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        data = [row for row in reader]

    conn = sqlite3.connect(paths["factions"] / "Factions.db")
    cursor = conn.cursor()

    # Empty and refill the table
    cursor.execute("DELETE FROM GearItems")
    for entry in data:
        cursor.execute("INSERT INTO GearItems (Name,'Gear Type') VALUES (?,?)",(entry["Name"],entry["Gear Type"]))


    for entry in data:
        attributes = ""
        holders = ""
        vals = []

        for attr in GEAR_ITEMS_ATTRIBUTES.keys():
            if(attr == "Name" or attr == "Gear Type"):
                continue
            attributes += f", '{attr}' = ?"
            holders += ", ?"
            vals.append(entry[attr])

        fullQuery = f"UPDATE GearItems SET {attributes.lstrip(', ')} WHERE Name = '{entry['Name']}'"
        cursor.execute(fullQuery,tuple(vals))

    conn.commit()
    conn.close()
def updateGearSets():
    with open(paths["factions"] / "CSVs/Gear Sets-Grid view.csv","r",encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        data = [row for row in reader]

    conn = sqlite3.connect(paths["factions"] / "Factions.db")
    cursor = conn.cursor()

    # Empty and refill the table
    cursor.execute("DELETE FROM GearSets")
    for entry in data:
        cursor.execute("INSERT INTO GearSets (Name) VALUES (?)",(entry["Name"],))


    for entry in data:
        attributes = ""
        holders = ""
        vals = []

        for attr in GEAR_SETS_ATTRIBUTES.keys():
            if(attr == "Name"):
                continue
            attributes += f", '{attr}' = ?"
            holders += ", ?"

            if(attr == "Basic Gear Set"):
                if(entry[attr] == "checked"):
                    finalVal = 1
                else:
                    finalVal = 0
            else:
                finalVal = entry[attr]
            vals.append(finalVal)

        fullQuery = f"UPDATE GearSets SET {attributes.lstrip(', ')} WHERE Name = '{entry['Name']}'"
        cursor.execute(fullQuery,tuple(vals))

    conn.commit()
    conn.close()
def updateFactions():
    with open(paths["factions"] / "CSVs/Factions-Grid view.csv","r",encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        data = [row for row in reader]

    conn = sqlite3.connect(paths["factions"] / f"Factions.db")
    cursor = conn.cursor()

    # Empty and refill the table
    cursor.execute("DELETE FROM Factions")
    for entry in data:
        if(entry["Name"] == "zAll"):
            continue
        cursor.execute("INSERT INTO Factions (Name) VALUES (?)",(entry["Name"],))


    for entry in data:
        if(entry["Name"] == "zAll"):
            continue
        attributes = ""
        holders = ""
        vals = []

        for attr in FACTIONS_ATTRIBUTES.keys():
            if(attr == "Name"):
                continue
            attributes += f", '{attr}' = ?"
            holders += ", ?"

            if(attr in ["Basic Gearset Chance","Facial Hair Probability","Hair Color Match Prob","FN Ratio","LN Ratio","Symmetrical Name Chance","Tattoo Probability"]):
                numValOnly = entry[attr].split("%")[0]
                if(numValOnly == ""):
                    finalVal = 0.0
                else:
                    finalVal = round(float(numValOnly)/100,2)
            elif(attr in ["Tattoo Symmetry","Generatable"]):
                if(entry[attr] == "checked"):
                    finalVal = 1
                else:
                    finalVal = 0
            else:
                finalVal = entry[attr]
            vals.append(finalVal)

        fullQuery = f"UPDATE Factions SET {attributes.lstrip(', ')} WHERE Name = \"{entry['Name']}\""
        cursor.execute(fullQuery,tuple(vals))

    conn.commit()
    conn.close()
def updateNameLists():
    with open(paths["factions"] / f"CSVs/Name Lists-Grid view.csv","r",encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        data = [row for row in reader]

    conn = sqlite3.connect(paths["factions"] / f"Factions.db")
    cursor = conn.cursor()

    # Empty and refill the table
    cursor.execute("DELETE FROM NameLists")
    for entry in data:
        cursor.execute("INSERT INTO NameLists (Name) VALUES (?)",(entry["Name"],))


    for entry in data:
        attributes = ""
        holders = ""
        vals = []

        for attr in NAME_LISTS_ATTRIBUTES.keys():
            if(attr == "Name"):
                continue
            attributes += f", '{attr}' = ?"
            holders += ", ?"

            finalVal = entry[attr]
            vals.append(finalVal)

        fullQuery = f"UPDATE NameLists SET {attributes.lstrip(', ')} WHERE Name = '{entry['Name']}'"
        if(len(vals) > 0):
            cursor.execute(fullQuery,tuple(vals))

    conn.commit()
    conn.close()
def updateHair():
    with open(paths["factions"] / "CSVs/Hair-Grid view.csv","r",encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        data = [row for row in reader]

    conn = sqlite3.connect(paths["factions"] / "Factions.db")
    cursor = conn.cursor()

    # Empty and refill the table
    cursor.execute("DELETE FROM Hair")
    for entry in data:
        cursor.execute("INSERT INTO Hair (Name) VALUES (?)",(entry["Name"],))


    for entry in data:
        attributes = ""
        holders = ""
        vals = []

        for attr in HAIR_ATTRIBUTES.keys():
            if(attr == "Name"):
                continue
            attributes += f", '{attr}' = ?"
            holders += ", ?"

            finalVal = entry[attr]
            vals.append(finalVal)

        fullQuery = f"UPDATE Hair SET {attributes.lstrip(', ')} WHERE Name = \"{entry['Name']}\""
        cursor.execute(fullQuery,tuple(vals))

    conn.commit()
    conn.close()
def updateTattoo():
    with open(paths["factions"] / f"CSVs/Tattoos-Grid view.csv","r",encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        data = [row for row in reader]

    conn = sqlite3.connect(paths["factions"] / "Factions.db")
    cursor = conn.cursor()

    # Empty and refill the table
    cursor.execute("DELETE FROM Tattoo")
    for entry in data:
        cursor.execute("INSERT INTO Tattoo (Name) VALUES (?)",(entry["Name"],))


    for entry in data:
        attributes = ""
        holders = ""
        vals = []

        for attr in TATTOO_ATTRIBUTES.keys():
            if(attr == "Name"):
                continue
            attributes += f", '{attr}' = ?"
            holders += ", ?"

            if(attr == "Symmetry"):
                if(entry[attr] == "checked"):
                    finalVal = 1
                else:
                    finalVal = 0
            finalVal = entry[attr]
            vals.append(finalVal)

        fullQuery = f"UPDATE Tattoo SET {attributes.lstrip(', ')} WHERE Name = \"{entry['Name']}\""
        cursor.execute(fullQuery,tuple(vals))

    conn.commit()
    conn.close()
def updateHairColor():
    with open(paths["factions"] / "CSVs/Hair Color-Grid view.csv","r",encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        data = [row for row in reader]

    conn = sqlite3.connect(paths["factions"] / "Factions.db")
    cursor = conn.cursor()

    # Empty and refill the table
    cursor.execute("DELETE FROM HairColor")
    for entry in data:
        cursor.execute("INSERT INTO HairColor (Name) VALUES (?)",(entry["Name"],))


    for entry in data:
        attributes = ""
        holders = ""
        vals = []

        for attr in HAIR_COLOR_ATTRIBUTES.keys():
            if(attr == "Name"):
                continue
            attributes += f", '{attr}' = ?"
            holders += ", ?"

            finalVal = entry[attr]
            vals.append(finalVal)

        fullQuery = f"UPDATE HairColor SET {attributes.lstrip(', ')} WHERE Name = \"{entry['Name']}\""
        cursor.execute(fullQuery,tuple(vals))

    conn.commit()
    conn.close()
def updateGoatee():
    with open(paths["factions"] / "CSVs/Goatee-Grid view.csv","r",encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        data = [row for row in reader]

    conn = sqlite3.connect(paths["factions"] / "Factions.db")
    cursor = conn.cursor()

    # Empty and refill the table
    cursor.execute("DELETE FROM Goatee")
    for entry in data:
        cursor.execute("INSERT INTO Goatee (Name) VALUES (?)",(entry["Name"],))


    for entry in data:
        attributes = ""
        holders = ""
        vals = []

        for attr in GOATEE_ATTRIBUTES.keys():
            if(attr == "Name"):
                continue
            attributes += f", '{attr}' = ?"
            holders += ", ?"

            finalVal = entry[attr]
            vals.append(finalVal)

        fullQuery = f"UPDATE Goatee SET {attributes.lstrip(', ')} WHERE Name = \"{entry['Name']}\""
        cursor.execute(fullQuery,tuple(vals))

    conn.commit()
    conn.close()
def updateMoustache():
    with open(paths["factions"] / "CSVs/Moustache-Grid view.csv","r",encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        data = [row for row in reader]

    conn = sqlite3.connect(paths["factions"] / "Factions.db")
    cursor = conn.cursor()

    # Empty and refill the table
    cursor.execute("DELETE FROM Moustache")
    for entry in data:
        cursor.execute("INSERT INTO Moustache (Name) VALUES (?)",(entry["Name"],))


    for entry in data:
        attributes = ""
        holders = ""
        vals = []

        for attr in MOUSTACHE_ATTRIBUTES.keys():
            if(attr == "Name"):
                continue
            attributes += f", '{attr}' = ?"
            holders += ", ?"

            finalVal = entry[attr]
            vals.append(finalVal)

        fullQuery = f"UPDATE Moustache SET {attributes.lstrip(', ')} WHERE Name = \"{entry['Name']}\""
        cursor.execute(fullQuery,tuple(vals))

    conn.commit()
    conn.close()
def updateBeard():
    with open(paths["factions"] / "CSVs/Beard-Grid view.csv","r",encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        data = [row for row in reader]

    conn = sqlite3.connect(paths["factions"] / "Factions.db")
    cursor = conn.cursor()

    # Empty and refill the table
    cursor.execute("DELETE FROM Beard")
    for entry in data:
        cursor.execute("INSERT INTO Beard (Name) VALUES (?)",(entry["Name"],))


    for entry in data:
        attributes = ""
        holders = ""
        vals = []

        for attr in BEARD_ATTRIBUTES.keys():
            if(attr == "Name"):
                continue
            attributes += f", '{attr}' = ?"
            holders += ", ?"

            finalVal = entry[attr]
            vals.append(finalVal)

        fullQuery = f"UPDATE Beard SET {attributes.lstrip(', ')} WHERE Name = \"{entry['Name']}\""
        cursor.execute(fullQuery,tuple(vals))

    conn.commit()
    conn.close()
def updateFacialHairColor():
    with open(paths["factions"] / "CSVs/Facial Hair Color-Grid view.csv","r",encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        data = [row for row in reader]

    conn = sqlite3.connect(paths["factions"] / "Factions.db")
    cursor = conn.cursor()

    # Empty and refill the table
    cursor.execute("DELETE FROM FacialHairColor")
    for entry in data:
        cursor.execute("INSERT INTO FacialHairColor (Name) VALUES (?)",(entry["Name"],))


    for entry in data:
        attributes = ""
        holders = ""
        vals = []

        for attr in FACIAL_HAIR_COLOR_ATTRIBUTES.keys():
            if(attr == "Name"):
                continue
            attributes += f", '{attr}' = ?"
            holders += ", ?"

            finalVal = entry[attr]
            vals.append(finalVal)

        fullQuery = f"UPDATE FacialHairColor SET {attributes.lstrip(', ')} WHERE Name = \"{entry['Name']}\""
        cursor.execute(fullQuery,tuple(vals))

    conn.commit()
    conn.close()

genBlankFactionsDatabase(paths["factions"] / "Factions.db")
updateRaces()
updateGearTypes()
updateGearItems()
updateGearSets()
updateNameLists()
updateHair()
updateTattoo()
updateHairColor()
updateGoatee()
updateMoustache()
updateBeard()
updateFacialHairColor()
updateFactions()
log.debug("Set up and updated all Faction info from Airtable CSVs")

#endregion === Database Maintenance ===

#region === Build DB Dict ===

# This method builds the entire Factions.db into a simple Python dict, for quick and easy
# access and to prevent a bunch of unnecessary SQL queries.
def buildDatabaseDict():
    conn = sqlite3.connect(paths["factions"] / "Factions.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    dbDict = {}

    # Select all faction rows as a list of dictionaries
    tableRows = cursor.execute("SELECT * FROM Factions").fetchall()
    if not tableRows:
        raise ValueError("No values found in the Factions table.")
    thisTableDict = {}
    for row in tableRows:
        singleRowDict = dict(row)
        thisTableDict[singleRowDict["Name"]] = singleRowDict
    dbDict["Factions"] = thisTableDict

    # Select all faction rows as a list of dictionaries
    tableRows = cursor.execute("SELECT * FROM Beard").fetchall()
    if not tableRows:
        raise ValueError("No values found in the Beard table.")
    thisTableDict = {}
    for row in tableRows:
        singleRowDict = dict(row)
        thisTableDict[singleRowDict["Name"]] = singleRowDict
    dbDict["Beard"] = thisTableDict

    # Select all faction rows as a list of dictionaries
    tableRows = cursor.execute("SELECT * FROM Beard").fetchall()
    if not tableRows:
        raise ValueError("No values found in the Beard table.")
    thisTableDict = {}
    for row in tableRows:
        singleRowDict = dict(row)
        thisTableDict[singleRowDict["Name"]] = singleRowDict
    dbDict["Beard"] = thisTableDict

    # Select all faction rows as a list of dictionaries
    tableRows = cursor.execute("SELECT * FROM FacialHairColor").fetchall()
    if not tableRows:
        raise ValueError("No values found in the FacialHairColor table.")
    thisTableDict = {}
    for row in tableRows:
        singleRowDict = dict(row)
        thisTableDict[singleRowDict["Name"]] = singleRowDict
    dbDict["FacialHairColor"] = thisTableDict

    # Select all faction rows as a list of dictionaries
    tableRows = cursor.execute("SELECT * FROM GearItems").fetchall()
    if not tableRows:
        raise ValueError("No values found in the GearItems table.")
    thisTableDict = {}
    for row in tableRows:
        singleRowDict = dict(row)
        thisTableDict[singleRowDict['Name']] = singleRowDict
    dbDict["GearItems"] = thisTableDict

    # Select all faction rows as a list of dictionaries
    tableRows = cursor.execute("SELECT * FROM GearSets").fetchall()
    if not tableRows:
        raise ValueError("No values found in the GearSets table.")
    thisTableDict = {}
    for row in tableRows:
        singleRowDict = dict(row)
        thisTableDict[singleRowDict["Name"]] = singleRowDict
    dbDict["GearSets"] = thisTableDict

    # Select all faction rows as a list of dictionaries
    tableRows = cursor.execute("SELECT * FROM GearTypes").fetchall()
    if not tableRows:
        raise ValueError("No values found in the GearTypes table.")
    thisTableDict = {}
    for row in tableRows:
        singleRowDict = dict(row)
        thisTableDict[singleRowDict["Name"]] = singleRowDict
    dbDict["GearTypes"] = thisTableDict

    # Select all faction rows as a list of dictionaries
    tableRows = cursor.execute("SELECT * FROM Goatee").fetchall()
    if not tableRows:
        raise ValueError("No values found in the Goatee table.")
    thisTableDict = {}
    for row in tableRows:
        singleRowDict = dict(row)
        thisTableDict[singleRowDict["Name"]] = singleRowDict
    dbDict["Goatee"] = thisTableDict

    # Select all faction rows as a list of dictionaries
    tableRows = cursor.execute("SELECT * FROM Hair").fetchall()
    if not tableRows:
        raise ValueError("No values found in the Hair table.")
    thisTableDict = {}
    for row in tableRows:
        singleRowDict = dict(row)
        thisTableDict[singleRowDict["Name"]] = singleRowDict
    dbDict["Hair"] = thisTableDict

    # Select all faction rows as a list of dictionaries
    tableRows = cursor.execute("SELECT * FROM HairColor").fetchall()
    if not tableRows:
        raise ValueError("No values found in the HairColor table.")
    thisTableDict = {}
    for row in tableRows:
        singleRowDict = dict(row)
        thisTableDict[singleRowDict["Name"]] = singleRowDict
    dbDict["HairColor"] = thisTableDict

    # Select all faction rows as a list of dictionaries
    tableRows = cursor.execute("SELECT * FROM Moustache").fetchall()
    if not tableRows:
        raise ValueError("No values found in the Moustache table.")
    thisTableDict = {}
    for row in tableRows:
        singleRowDict = dict(row)
        thisTableDict[singleRowDict["Name"]] = singleRowDict
    dbDict["Moustache"] = thisTableDict

    # Select all faction rows as a list of dictionaries
    tableRows = cursor.execute("SELECT * FROM NameLists").fetchall()
    if not tableRows:
        raise ValueError("No values found in the NameLists table.")
    thisTableDict = {}
    for row in tableRows:
        singleRowDict = dict(row)
        thisTableDict[singleRowDict["Name"]] = singleRowDict
    dbDict["NameLists"] = thisTableDict

    # Select all faction rows as a list of dictionaries
    tableRows = cursor.execute("SELECT * FROM Races").fetchall()
    if not tableRows:
        raise ValueError("No values found in the Races table.")
    thisTableDict = {}
    for row in tableRows:
        singleRowDict = dict(row)
        thisTableDict[singleRowDict["Race"]] = singleRowDict
    dbDict["Races"] = thisTableDict

    # Select all faction rows as a list of dictionaries
    tableRows = cursor.execute("SELECT * FROM Tattoo").fetchall()
    if not tableRows:
        raise ValueError("No values found in the Tattoo table.")
    thisTableDict = {}
    for row in tableRows:
        singleRowDict = dict(row)
        thisTableDict[singleRowDict["Name"]] = singleRowDict
    dbDict["Tattoo"] = thisTableDict

    conn.close()
    return dbDict
dbDict = buildDatabaseDict()

#endregion === Build DB Dict ===


# This method uses race information to generate all headshape information for a given player.
def genRaceHeadshape(raceName : str,player):
    if(raceName not in dbDict["Races"].keys()):
        raise ValueError(f"Invalid race name: '{raceName}'")

    valRanges = {}
    for key,value in dbDict["Races"][raceName].items():
        if(key.endswith("_Min")):
            valRanges[key.split("_Min")[0]] = [value]
        elif(key.endswith("_Max")):
            valRanges[key.split("_Max")[0]].append(value)

    for key,value in valRanges.items():
        player[key] = random.randrange(value[0],value[1] + 1)

    player["Race"] = raceName
    return player
# This method uses a given gearset to generate all gear information for a given player.
def genGearset(gearset : str,player):
    if(gearset not in dbDict["GearSets"].keys()):
        raise ValueError(f"Invalid gearset name: '{gearset}'")
    thisGearset = dbDict["GearSets"][gearset]

    # This helper method accepts a gearset name, and generates a "slotDict" of all entries
    # within it.
    def getGearsetSlotsDict(gearsetName,existingSlotDict = None):
        if(existingSlotDict is None):
            slotDict = {"Symmetry" : []}
        else:
            slotDict = existingSlotDict

        symmetryItems = dbDict["GearSets"][gearsetName]["Symmetry"].split(",") if dbDict["GearSets"][gearsetName]["Symmetry"] != "" else []
        for symmetryItem in symmetryItems:
            if(symmetryItem not in slotDict["Symmetry"]):
                slotDict["Symmetry"].append(symmetryItem)

        gearItems = dbDict["GearSets"][gearsetName]["Gear Items"].split(",") if dbDict["GearSets"][gearsetName]["Gear Items"] != "" else []
        for singleGearItem in gearItems:
            gearItemSplit = singleGearItem.split("|")
            if(gearItemSplit[1] in slotDict):
                slotDict[gearItemSplit[1]].append(gearItemSplit[0])
            else:
                slotDict[gearItemSplit[1]] = [gearItemSplit[0]]

        # Now, we divide subsets into ones that may be in conflict with each other (meaning
        # they have a bucket, and only one can win out) and ones that CAN'T come into conflict
        # with each other.
        bucketSubsets = {}
        finalSubsets = []
        rawSubsetList = dbDict["GearSets"][gearsetName]["Subsets"].split(",") if dbDict["GearSets"][gearsetName]["Subsets"] != "" else []
        for subset in rawSubsetList:
            if(dbDict["GearSets"][subset]["Subset Bucket"] == ""):
                finalSubsets.append(subset)
            else:
                if(dbDict["GearSets"][subset]["Subset Bucket"] in bucketSubsets.keys()):
                    bucketSubsets[dbDict["GearSets"][subset]["Subset Bucket"]].append(subset)
                else:
                    bucketSubsets[dbDict["GearSets"][subset]["Subset Bucket"]] = [subset]

        # We now take all conflicting subsets and resolve the conflicts, then add them to final
        # subsets.
        for conflictingSubsetList in bucketSubsets.values():
            finalSubsets.append(random.choice(conflictingSubsetList))

        # Finally, we recursively add the actual items of each final subset to our slotDict.
        for finalSubset in finalSubsets:
            getGearsetSlotsDict(gearsetName=finalSubset,existingSlotDict=slotDict)

        return slotDict
    thisSlotDict = getGearsetSlotsDict(gearsetName=gearset)

    # Now we resolve each slot present in the slotDict into the player object.
    for slot,choices in thisSlotDict.items():
        if(slot == "Symmetry"):
            continue
        player[slot] = dbDict["GearItems"][f"{random.choice(choices)}|{slot}"]["ID"]

    # Finally, we resolve any symmetry that was found in the slotDict.
    for symmetrySlot in thisSlotDict["Symmetry"]:
        symmetricalCounterpart = dbDict["GearTypes"][symmetrySlot]["Symmetrical Type"]
        player[symmetricalCounterpart] = player[symmetrySlot]

    return player

# Generates the race and headshape info, and applies it to the given player.
def genFactionRace(faction : str,player):
    if (faction not in dbDict["Factions"].keys()):
        raise ValueError(f"Invalid faction name: '{faction}'")
    thisFactionDict = dbDict["Factions"][faction]
    race = random.choice(thisFactionDict["Race"].split(",") if thisFactionDict["Race"] != "" else [])
    player = genRaceHeadshape(raceName=race,player=player)
# Generates the full Gearset based off the given faction, and applies it to the Player.
def genFactionGearset(faction : str,player):
    if(faction not in dbDict["Factions"].keys()):
        raise ValueError(f"Invalid faction name: '{faction}'")
    thisFactionDict = dbDict["Factions"][faction]

    gearsetChoices = []
    # Chance of getting a basic gearset
    if(thisFactionDict["Basic Gearset Chance"] > random.random()):
        for key,value in dbDict["GearSets"].items():
            if(value["Basic Gear Set"] == 1):
                gearsetChoices.append(key)
    # Otherwise, special gearset
    else:
        gearsetChoices = thisFactionDict["Special Gear Sets"].split(",") if thisFactionDict["Special Gear Sets"] != "" else []
    if(len(gearsetChoices) > 0):
        gearsetSelection = random.choice(gearsetChoices)
        genGearset(gearset=gearsetSelection,player=player)
# Generates all Hair, Facial Hair, and Eyebrow information based off the given faction, and applies it to the Player.
def genFactionHair(faction : str,player):
    if(faction not in dbDict["Factions"].keys()):
        raise ValueError(f"Invalid faction name: '{faction}'")
    thisFactionDict = dbDict["Factions"][faction]

    hairChoices = thisFactionDict["Hair Style"].split(",") if thisFactionDict["Hair Style"] != "" else []
    player["CAP_Hstl"] = dbDict["Hair"][random.choice(hairChoices)]["ID"]
    hairColorChoices = thisFactionDict["Hair Color"].split(",") if thisFactionDict["Hair Style"] != "" else []
    player["CAP_Hcol"] = dbDict["HairColor"][random.choice(hairColorChoices)]["ID"]

    # Now, we randomly roll to see which, if any, facial hair types will be present.
    validFacialHairTypes = []
    if(thisFactionDict["Beard"] != ""):
        validFacialHairTypes.append(("Beard","CAP_BStyle"))
    if(thisFactionDict["Moustache"] != ""):
        validFacialHairTypes.append(("Moustache","CAP_Moust"))
    if(thisFactionDict["Goatee"] != ""):
        validFacialHairTypes.append(("Goatee", "CAP_Goatee"))
    baseFacialHairChance = thisFactionDict["Facial Hair Probability"]
    for i in range(3):
        # TODO randomize hair length
        # TODO actually adhere to facial hair
        if((baseFacialHairChance * 0.333) > random.random() and len(validFacialHairTypes) > 0):
            # Halve the probability of subsequent facial hair
            baseFacialHairChance = baseFacialHairChance * 0.5
            chosenFacialHair = random.choice(validFacialHairTypes)
            validFacialHairTypes.remove(chosenFacialHair)
            facialHairOptions = thisFactionDict[chosenFacialHair[0]].split(",") if thisFactionDict[chosenFacialHair[0]] != "" else [0]
            player[chosenFacialHair[1]] = dbDict[chosenFacialHair[0]][random.choice(facialHairOptions)]["ID"]
    if(thisFactionDict["Hair Color Match Prob"] > random.random()):
        player["CAP_Fhcol"] = player["CAP_Hcol"]
    else:
        facialHairColorChoices = thisFactionDict["Facial Hair Color"].split(",") if thisFactionDict["Facial Hair Color"] != "" else [0]
        player["CAP_Fhcol"] = dbDict["HairColor"][random.choice(facialHairColorChoices)]["ID"]

    # Eyebrows are always randomly picked
    if(0.20 > random.random()):
        player["CAP_Eyebr"] = 1
    else:
        player["CAP_Eyebr"] = random.randrange(0,11)
# Generates all tattoos information based off the given faction, and applies it to the Player.
def genFactionTattoos(faction : str,player):
    if(faction not in dbDict["Factions"].keys()):
        raise ValueError(f"Invalid faction name: '{faction}'")
    thisFactionDict = dbDict["Factions"][faction]

    if(thisFactionDict["Tattoo Probability"] > random.random()):
        tattooDensity = thisFactionDict["Tattoo Density"]
        if(tattooDensity == "Light"):
            tattooCountChoices = [2]
        elif(tattooDensity == "Medium"):
            tattooCountChoices = [2,4]
        else:
            tattooCountChoices = [2,4,6]
        tattooCount = random.choice(tattooCountChoices)
        validTattooTypes = list(dbDict["Tattoo"].keys())
        #TODO real symmetry
        while tattooCount > 0:
            tattooCount -= 1
            tattooTypeChoice = random.choice(validTattooTypes)
            validTattooTypes.remove(tattooTypeChoice)
            player[tattooTypeChoice] = random.randrange(1,dbDict["Tattoo"][tattooTypeChoice]["Max ID"] + 1)
            if(thisFactionDict["Tattoo Symmetry"] == 1):
                tattooCount -= 1
                symmetricalTattoo = dbDict["Tattoo"][tattooTypeChoice]["Symmetry"]
                if(symmetricalTattoo != ""):
                    player[symmetricalTattoo] = random.randrange(1, dbDict["Tattoo"][symmetricalTattoo]["Max ID"] + 1)
# Generates a random name, based off the given faction, and applies it to the Player.
def genFactionName(faction : str,player):
    if(faction not in dbDict["Factions"].keys()):
        raise ValueError(f"Invalid faction name: '{faction}'")
    thisFactionDict = dbDict["Factions"][faction]

    if(thisFactionDict["Symmetrical Name Chance"] > random.random()):
        isSymmetricalName = True
    else:
        isSymmetricalName = False

    # First name
    if(thisFactionDict["FN Ratio"] > random.random()):
        firstNameListOptions = thisFactionDict["Primary FN"].split(",") if thisFactionDict["Primary FN"] != "" else []
    else:
        firstNameListOptions = thisFactionDict["Secondary FN"].split(",") if thisFactionDict["Secondary FN"] != "" else []
    chosenFirstNameList = random.choice(firstNameListOptions)
    if(isSymmetricalName and dbDict["NameLists"][chosenFirstNameList]["Symmetry"] != ""):
        symmetricalLastName = dbDict["NameLists"][chosenFirstNameList]["Symmetry"]
    else:
        symmetricalLastName = None

    # Last Name
    if(thisFactionDict["LN Ratio"] > random.random()):
        lastNameListOptions = thisFactionDict["Primary LN"].split(",") if thisFactionDict["Primary LN"] != "" else []
    else:
        lastNameListOptions = thisFactionDict["Secondary LN"].split(",") if thisFactionDict["Secondary LN"] != "" else []
    chosenLastNameList = random.choice(lastNameListOptions)
    if(isSymmetricalName and dbDict["NameLists"][chosenLastNameList]["Symmetry"] != ""):
        symmetricalFirstName = dbDict["NameLists"][chosenLastNameList]["Symmetry"]
    else:
        symmetricalFirstName = None
    # Now we finalize both first and last names.
    if(symmetricalLastName is not None):
        chosenLastNameList = symmetricalLastName
    elif(symmetricalFirstName is not None):
        chosenFirstNameList = symmetricalFirstName
    firstNameListPath = dbDict["NameLists"][chosenFirstNameList]["Value"].replace("$NL_PATH", "WordLists\\NameLists")
    lastNameListPath = dbDict["NameLists"][chosenLastNameList]["Value"].replace("$NL_PATH", "WordLists\\NameLists")
    player["First_Name"] = rsuite.rString(firstNameListPath,randListBasePath=paths["randGen"])
    player["Last_Name"] = rsuite.rString(lastNameListPath,randListBasePath=paths["randGen"])


# Helper method for randomly choosing a faction to generate based on all generatable factions.
def getRandomFaction():
    allGeneratableFactions = []

    for factionName,factionInfo in dbDict["Factions"].items():
        if(factionInfo["Generatable"] == 1):
            allGeneratableFactions.append(factionName)

    return random.choice(allGeneratableFactions)


# TODO FIX YOUR RSTRING IDIOT