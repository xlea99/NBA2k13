import csv
import os
import Player
import BaseFunctions as b
import sqlite3 as sql
from datetime import date
import random
import json
import StatsProcessing

# This dictionary stores relevant values for each possible Jersey that can be selected.
JERSEY_DICT = {
"SixersHome" : {'Texture': 'uh000', 'Logo': 'logo000', 'Name': 'B7E8E31A', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '4', 'SocksCol': '0', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': 'EBEBEB', 'TColor2': '0068B3', 'TColor3': 'DE2739', 'TColor4': 'DE2739', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"SixersAway" : {'Texture': 'ua000', 'Logo': 'logo000', 'Name': 'F45673DE', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '4', 'SocksCol': '1', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': '141414', 'TColor2': 'DE2739', 'TColor3': '0068B3', 'TColor4': 'DE2739', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"SixersClassicAwayI" : {'Texture': 'r1a000', 'Logo': 'logo000', 'Name': '5897FDC4', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '0', 'SocksCol': '1', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': '141414', 'TColor2': 'EA2750', 'TColor3': '1B3A60', 'TColor4': 'EA2750', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"SixersClassicHomeII" : {'Texture': 'r2h000', 'Logo': 'logo000', 'Name': '2BDE5EAA', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '1', 'SocksCol': '0', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': 'EBEBEB', 'TColor2': 'ED174C', 'TColor3': '005A9C', 'TColor4': 'ED174C', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"SixersClassicAwayIII" : {'Texture': 'r3a000', 'Logo': 'logo000', 'Name': 'DB3623A5', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '0', 'SocksCol': '1', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': '141414', 'TColor2': '005596', 'TColor3': 'ED174F', 'TColor4': '005596', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"SixersClassicAwayIV" : {'Texture': 'r4a000', 'Logo': 'logo000', 'Name': 'C151ECC2', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '1', 'SocksCol': '1', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': '141414', 'TColor2': 'FA002C', 'TColor3': '093A80', 'TColor4': 'FA002C', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"SixersClassicAwayV" : {'Texture': 'r5a000', 'Logo': 'logo000', 'Name': '792665E2', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '0', 'SocksCol': '1', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': '141414', 'TColor2': '005596', 'TColor3': 'F51031', 'TColor4': '005596', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"SixersClassicHomeVI" : {'Texture': 'r6h000', 'Logo': 'logo000', 'Name': 'F9F26ACF', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '3', 'SocksCol': '0', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': 'EBEBEB', 'TColor2': 'ED174C', 'TColor3': 'D7D7D7', 'TColor4': 'ED174C', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"SixersClassicAwayVI" : {'Texture': 'r6a000', 'Logo': 'logo000', 'Name': '32CC4081', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '3', 'SocksCol': '1', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': '141414', 'TColor2': 'ED174C', 'TColor3': '141414', 'TColor4': 'ED174C', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"SixersClassicAwayVIAlt" : {'Texture': 'r6x000', 'Logo': 'logo000', 'Name': '9D160E5D', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '3', 'SocksCol': '1', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': '141414', 'TColor2': '1860AB', 'TColor3': 'ED174C', 'TColor4': '1860AB', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"SixersClassicHomeVII" : {'Texture': 'r7h000', 'Logo': 'logo000', 'Name': '7793C8FB', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '3', 'SocksCol': '0', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': 'EBEBEB', 'TColor2': 'ED174C', 'TColor3': 'D7D7D7', 'TColor4': 'ED174C', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"SixersClassicAwayVII" : {'Texture': 'r7a000', 'Logo': 'logo000', 'Name': 'E63C9A46', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '3', 'SocksCol': '1', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': '141414', 'TColor2': 'ED174C', 'TColor3': '141414', 'TColor4': 'ED174C', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"BobcatsHome" : {'Texture': 'uh031', 'Logo': 'logo031', 'Name': 'B7E8E31A', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '1', 'SocksCol': '0', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': 'EBEBEB', 'TColor2': '0A2B5C', 'TColor3': 'A1A1A5', 'TColor4': '0A2B5C', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"BobcatsAway" : {'Texture': 'ua031', 'Logo': 'logo031', 'Name': 'F45673DE', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '1', 'SocksCol': '1', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': '141414', 'TColor2': 'A1A1A5', 'TColor3': '0A2B5C', 'TColor4': 'A1A1A5', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"BobcatsRacing" : {'Texture': 'uax031', 'Logo': 'logo031', 'Name': '97CC5AB6', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '1', 'SocksCol': '1', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': '141414', 'TColor2': '3D6185', 'TColor3': 'F26631', 'TColor4': '141414', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"BobcatsNBAGreen" : {'Texture': 'uay031', 'Logo': 'logo031', 'Name': 'BDFBD6EE', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '1', 'SocksCol': '1', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': '141414', 'TColor2': '004812', 'TColor3': 'F47B20', 'TColor4': '004812', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"BobcatsClassicHomeI" : {'Texture': 'r1h031', 'Logo': 'logo031', 'Name': '070E3F74', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '2', 'SocksCol': '0', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': 'EBEBEB', 'TColor2': 'F16530', 'TColor3': '305A8B', 'TColor4': 'F16530', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"BobcatsClassicAwayI" : {'Texture': 'r1a031', 'Logo': 'logo031', 'Name': '5897FDC4', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '2', 'SocksCol': '1', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': '141414', 'TColor2': 'F16530', 'TColor3': '305A8B', 'TColor4': '141414', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"BobcatsClassicAwayIAlt" : {'Texture': 'r1x031', 'Logo': 'logo031', 'Name': '0872C7C8', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '2', 'SocksCol': '1', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': '141414', 'TColor2': '2E5B8D', 'TColor3': 'F26532', 'TColor4': '141414', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"BobcatsClassicHomeII" : {'Texture': 'r2h031', 'Logo': 'logo031', 'Name': '2BDE5EAA', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '0', 'SocksCol': '0', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': 'EBEBEB', 'TColor2': 'D21034', 'TColor3': '5998C8', 'TColor4': 'EBEBEB', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"BucksHome" : {'Texture': 'uh001', 'Logo': 'logo001', 'Name': 'B7E8E31A', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '4', 'SocksCol': '0', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': 'EBEBEB', 'TColor2': '0A653F', 'TColor3': 'C41130', 'TColor4': '0A653F', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"BucksAway" : {'Texture': 'ua001', 'Logo': 'logo001', 'Name': 'F45673DE', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '4', 'SocksCol': '0', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': 'EBEBEB', 'TColor2': '0A653F', 'TColor3': 'C41130', 'TColor4': '0A653F', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"BucksAlternate" : {'Texture': 'ux001', 'Logo': 'logo001', 'Name': '39976E3D', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '0', 'SocksCol': '0', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': 'EBEBEB', 'TColor2': 'C41130', 'TColor3': '0A653F', 'TColor4': 'C41130', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"BucksClassicHomeI" : {'Texture': 'r1h001', 'Logo': 'logo001', 'Name': '070E3F74', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '0', 'SocksCol': '1', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': '141414', 'TColor2': 'BC1E2C', 'TColor3': '245224', 'TColor4': 'BC1E2C', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"BucksClassicAwayI" : {'Texture': 'r1a001', 'Logo': 'logo001', 'Name': '5897FDC4', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '0', 'SocksCol': '0', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': 'EBEBEB', 'TColor2': '0D2710', 'TColor3': 'FA002C', 'TColor4': '0D2710', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"BucksClassicHomeII" : {'Texture': 'r2h001', 'Logo': 'logo001', 'Name': '2BDE5EAA', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '1', 'SocksCol': '0', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': 'EBEBEB', 'TColor2': 'B0132A', 'TColor3': '5C7E39', 'TColor4': 'B0132A', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"BucksClassicAwayII" : {'Texture': 'r2a001', 'Logo': 'logo001', 'Name': 'E0E074E4', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '1', 'SocksCol': '0', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': 'EBEBEB', 'TColor2': '2D5E58', 'TColor3': 'B0132A', 'TColor4': '2D5E58', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"BucksClassicHomeIII" : {'Texture': 'r3h001', 'Logo': 'logo001', 'Name': '4A997118', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '0', 'SocksCol': '0', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': 'EBEBEB', 'TColor2': '004812', 'TColor3': 'E51837', 'TColor4': '004812', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"BucksClassicAwayIV" : {'Texture': 'r4a001', 'Logo': 'logo001', 'Name': 'C151ECC2', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '1', 'SocksCol': '0', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': 'EBEBEB', 'TColor2': '0A461B', 'TColor3': '5E398A', 'TColor4': '0A461B', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"BullsHome" : {'Texture': 'uh003', 'Logo': 'logo003', 'Name': 'B7E8E31A', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '0', 'SocksCol': '0', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': 'EBEBEB', 'TColor2': 'CE1043', 'TColor3': 'D7D7D7', 'TColor4': 'CE1043', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"BullsAway" : {'Texture': 'ua003', 'Logo': 'logo003', 'Name': 'F45673DE', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '0', 'SocksCol': '1', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': '141414', 'TColor2': 'CE1043', 'TColor3': '141414', 'TColor4': 'CE1043', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"BullsAlternate" : {'Texture': 'ux003', 'Logo': 'logo003', 'Name': '39976E3D', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '0', 'SocksCol': '1', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': '141414', 'TColor2': 'DA203D', 'TColor3': '141414', 'TColor4': 'DA203D', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"BullsLatinNights" : {'Texture': 'uhx003', 'Logo': 'logo003', 'Name': '893F3614', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '0', 'SocksCol': '0', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': 'EBEBEB', 'TColor2': 'CE1043', 'TColor3': '141414', 'TColor4': 'CE1043', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"BullsStPatricks" : {'Texture': 'uax003', 'Logo': 'logo003', 'Name': '39A2D4A5', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '0', 'SocksCol': '1', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': '141414', 'TColor2': '008348', 'TColor3': '141414', 'TColor4': '008348', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"BullsNBAGreen" : {'Texture': 'uay003', 'Logo': 'logo003', 'Name': 'BDFBD6EE', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '0', 'SocksCol': '1', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': '141414', 'TColor2': '004812', 'TColor3': 'DA203D', 'TColor4': '004812', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"BullsClassicAwayI" : {'Texture': 'r1a003', 'Logo': 'logo003', 'Name': '5897FDC4', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '0', 'SocksCol': '1', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': '141414', 'TColor2': 'C71444', 'TColor3': '141414', 'TColor4': 'C71444', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"BullsClassicAwayII" : {'Texture': 'r2a003', 'Logo': 'logo003', 'Name': 'E0E074E4', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '0', 'SocksCol': '1', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': '141414', 'TColor2': '141414', 'TColor3': 'CD1043', 'TColor4': '141414', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"CavaliersHome" : {'Texture': 'uh004', 'Logo': 'logo004', 'Name': 'B7E8E31A', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '0', 'SocksCol': '0', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': 'EBEBEB', 'TColor2': '860038', 'TColor3': 'FCB034', 'TColor4': 'EBEBEB', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"CavaliersAway" : {'Texture': 'ua004', 'Logo': 'logo004', 'Name': 'F45673DE', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '0', 'SocksCol': '1', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': '141414', 'TColor2': '860038', 'TColor3': 'FCB034', 'TColor4': '860038', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"CavaliersCavfanatic" : {'Texture': 'uax004', 'Logo': 'logo004', 'Name': 'C7939431', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '0', 'SocksCol': '0', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': 'EBEBEB', 'TColor2': '860038', 'TColor3': 'FDBA31', 'TColor4': 'FDBA31', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"CavaliersClassicHomeI" : {'Texture': 'r1h004', 'Logo': 'logo004', 'Name': '070E3F74', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '1', 'SocksCol': '0', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': 'EBEBEB', 'TColor2': '6071C4', 'TColor3': 'FF870E', 'TColor4': '6071C4', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"CavaliersClassicAwayI" : {'Texture': 'r1a004', 'Logo': 'logo004', 'Name': '5897FDC4', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '1', 'SocksCol': '0', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': 'EBEBEB', 'TColor2': '6071C4', 'TColor3': 'FF870E', 'TColor4': '6071C4', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"CavaliersClassicHomeII" : {'Texture': 'r2h004', 'Logo': 'logo004', 'Name': '2BDE5EAA', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '0', 'SocksCol': '0', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': 'EBEBEB', 'TColor2': 'FEC31D', 'TColor3': '921026', 'TColor4': 'FEC31D', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"CavaliersClassicAwayII" : {'Texture': 'r2a004', 'Logo': 'logo004', 'Name': 'E0E074E4', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '0', 'SocksCol': '0', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': 'EBEBEB', 'TColor2': '970B1E', 'TColor3': 'DEC52D', 'TColor4': '970B1E', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"CavaliersClassicHomeIII" : {'Texture': 'r3h004', 'Logo': 'logo004', 'Name': '4A997118', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '0', 'SocksCol': '0', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': 'EBEBEB', 'TColor2': 'F15C22', 'TColor3': '013C7E', 'TColor4': 'F15C22', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"CavaliersClassicAwayIII" : {'Texture': 'r3a004', 'Logo': 'logo004', 'Name': 'DB3623A5', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '0', 'SocksCol': '0', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': 'EBEBEB', 'TColor2': 'F15C22', 'TColor3': '013C7E', 'TColor4': 'F15C22', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"CavaliersClassicHomeIV" : {'Texture': 'r4h004', 'Logo': 'logo004', 'Name': '0A6FC68C', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '0', 'SocksCol': '0', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': 'EBEBEB', 'TColor2': 'FCB034', 'TColor3': '8B0B04', 'TColor4': '8B0B04', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"CavaliersClassicAwayIV" : {'Texture': 'r4a004', 'Logo': 'logo004', 'Name': 'C151ECC2', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '0', 'SocksCol': '0', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': 'EBEBEB', 'TColor2': '8B0B04', 'TColor3': 'FCB034', 'TColor4': '8B0B04', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"CavaliersClassicAwayIVAlt" : {'Texture': 'r4x004', 'Logo': 'logo004', 'Name': '248E0A7B', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '0', 'SocksCol': '0', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': 'EBEBEB', 'TColor2': '0068B0', 'TColor3': 'FCB034', 'TColor4': 'FCB034', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"CavaliersClassicHomeV" : {'Texture': 'r5h004', 'Logo': 'logo004', 'Name': '26BFA752', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '3', 'SocksCol': '0', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': 'EBEBEB', 'TColor2': 'A90533', 'TColor3': '987C4D', 'TColor4': 'EBEBEB', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"CavaliersClassicAwayV" : {'Texture': 'r5a004', 'Logo': 'logo004', 'Name': '792665E2', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '3', 'SocksCol': '1', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': '141414', 'TColor2': 'A90533', 'TColor3': '987C4D', 'TColor4': 'A90533', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"CavaliersClassicAwayVAlt" : {'Texture': 'r5x004', 'Logo': 'logo004', 'Name': 'CF9C51C5', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '3', 'SocksCol': '0', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': 'EBEBEB', 'TColor2': '002B60', 'TColor3': 'A90533', 'TColor4': '002B60', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"CelticsHome" : {'Texture': 'uh005', 'Logo': 'logo005', 'Name': 'B7E8E31A', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '0', 'SocksCol': '0', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': 'EBEBEB', 'TColor2': '008853', 'TColor3': 'D7D7D7', 'TColor4': 'EBEBEB', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"CelticsAway" : {'Texture': 'ua005', 'Logo': 'logo005', 'Name': 'F45673DE', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '0', 'SocksCol': '1', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': '141414', 'TColor2': '008853', 'TColor3': 'D7D7D7', 'TColor4': '008853', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"CelticsAlternate" : {'Texture': 'ux005', 'Logo': 'logo005', 'Name': '39976E3D', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '0', 'SocksCol': '1', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': '141414', 'TColor2': '008853', 'TColor3': '141414', 'TColor4': '008853', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"CelticsStPatricks" : {'Texture': 'uax005', 'Logo': 'logo005', 'Name': '39A2D4A5', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '0', 'SocksCol': '1', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': '141414', 'TColor2': '008853', 'TColor3': 'BA9754', 'TColor4': '008853', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"CelticsClassicHomeI" : {'Texture': 'r1h005', 'Logo': 'logo005', 'Name': '070E3F74', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '0', 'SocksCol': '0', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': 'EBEBEB', 'TColor2': '00853E', 'TColor3': 'D7D7D7', 'TColor4': 'EBEBEB', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"ClippersHome" : {'Texture': 'uh006', 'Logo': 'logo006', 'Name': 'B7E8E31A', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '1', 'SocksCol': '0', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': 'EBEBEB', 'TColor2': '0068B3', 'TColor3': 'EE174F', 'TColor4': 'EBEBEB', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"ClippersAway" : {'Texture': 'ua006', 'Logo': 'logo006', 'Name': 'F45673DE', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '1', 'SocksCol': '1', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': '141414', 'TColor2': 'EE174F', 'TColor3': '0068B3', 'TColor4': 'EE174F', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"ClippersClassicAwayI" : {'Texture': 'r1a006', 'Logo': 'logo006', 'Name': '5897FDC4', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '0', 'SocksCol': '1', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': '141414', 'TColor2': 'F47B20', 'TColor3': '141414', 'TColor4': 'F47B20', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"ClippersClassicHomeII" : {'Texture': 'r2h006', 'Logo': 'logo006', 'Name': '2BDE5EAA', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '3', 'SocksCol': '0', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': 'EBEBEB', 'TColor2': 'E0001D', 'TColor3': '006BB6', 'TColor4': 'EBEBEB', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"ClippersClassicAwayII" : {'Texture': 'r2a006', 'Logo': 'logo006', 'Name': 'E0E074E4', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '3', 'SocksCol': '1', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': '141414', 'TColor2': 'E0001D', 'TColor3': '006BB6', 'TColor4': 'E0001D', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"ClippersClassicAwayIIAlt" : {'Texture': 'r2x006', 'Logo': 'logo006', 'Name': 'E3609C76', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '3', 'SocksCol': '1', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': '141414', 'TColor2': '006BB6', 'TColor3': 'E0001D', 'TColor4': '006BB6', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"ClippersClassicAwayIII" : {'Texture': 'r3a006', 'Logo': 'logo006', 'Name': 'DB3623A5', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '0', 'SocksCol': '1', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': '141414', 'TColor2': '4F91CD', 'TColor3': 'ED174F', 'TColor4': 'EBEBEB', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"GrizzliesHome" : {'Texture': 'uh008', 'Logo': 'logo008', 'Name': 'B7E8E31A', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '3', 'SocksCol': '0', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': 'EBEBEB', 'TColor2': '1A385B', 'TColor3': '7299C6', 'TColor4': 'EBEBEB', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"GrizzliesAway" : {'Texture': 'ua008', 'Logo': 'logo008', 'Name': 'F45673DE', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '3', 'SocksCol': '0', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': 'EBEBEB', 'TColor2': '1A385B', 'TColor3': '7299C6', 'TColor4': '1A385B', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"GrizzliesAlternate" : {'Texture': 'ux008', 'Logo': 'logo008', 'Name': '39976E3D', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '1', 'SocksCol': '0', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': 'EBEBEB', 'TColor2': '7299C6', 'TColor3': '1A385B', 'TColor4': '7299C6', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"GrizzliesClassicHomeI" : {'Texture': 'r1h008', 'Logo': 'logo008', 'Name': '070E3F74', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '3', 'SocksCol': '0', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': 'EBEBEB', 'TColor2': '00ADA8', 'TColor3': 'E03A3E', 'TColor4': '00ADA8', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"GrizzliesClassicAwayI" : {'Texture': 'r1a008', 'Logo': 'logo008', 'Name': '5897FDC4', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '3', 'SocksCol': '0', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': 'EBEBEB', 'TColor2': '00ADA8', 'TColor3': 'E03A3E', 'TColor4': '00ADA8', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"GrizzliesClassicAwayII" : {'Texture': 'r2a008', 'Logo': 'logo008', 'Name': 'E0E074E4', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '0', 'SocksCol': '0', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': 'EBEBEB', 'TColor2': 'FDBA31', 'TColor3': '0B8743', 'TColor4': 'EBEBEB', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"HawksHome" : {'Texture': 'uh009', 'Logo': 'logo009', 'Name': 'B7E8E31A', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '4', 'SocksCol': '0', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': 'EBEBEB', 'TColor2': '00234C', 'TColor3': 'D21034', 'TColor4': 'EBEBEB', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"HawksAway" : {'Texture': 'ua009', 'Logo': 'logo009', 'Name': 'F45673DE', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '4', 'SocksCol': '1', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': '141414', 'TColor2': '00234C', 'TColor3': 'D21034', 'TColor4': '141414', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"HawksAlternate" : {'Texture': 'ux009', 'Logo': 'logo009', 'Name': '39976E3D', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '4', 'SocksCol': '1', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': '141414', 'TColor2': 'D21034', 'TColor3': '00234C', 'TColor4': 'D21034', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"HawksClassicHomeI" : {'Texture': 'r1h009', 'Logo': 'logo009', 'Name': '070E3F74', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '0', 'SocksCol': '0', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': 'EBEBEB', 'TColor2': '1A357B', 'TColor3': '669F51', 'TColor4': 'EBEBEB', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"HawksClassicAwayI" : {'Texture': 'r1a009', 'Logo': 'logo009', 'Name': '5897FDC4', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '0', 'SocksCol': '1', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': '141414', 'TColor2': '1A357B', 'TColor3': '669F51', 'TColor4': '1A357B', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"HawksClassicHomeII" : {'Texture': 'r2h009', 'Logo': 'logo009', 'Name': '2BDE5EAA', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '0', 'SocksCol': '0', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': 'EBEBEB', 'TColor2': 'E2373E', 'TColor3': 'FFC323', 'TColor4': 'EBEBEB', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"HawksClassicAwayII" : {'Texture': 'r2a009', 'Logo': 'logo009', 'Name': 'E0E074E4', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '0', 'SocksCol': '1', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': '141414', 'TColor2': 'E2373E', 'TColor3': 'FFC323', 'TColor4': 'E2373E', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"HawksClassicHomeIII" : {'Texture': 'r3h009', 'Logo': 'logo009', 'Name': '4A997118', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '0', 'SocksCol': '0', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': 'EBEBEB', 'TColor2': 'FF3A3E', 'TColor3': 'FFC425', 'TColor4': 'EBEBEB', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"HawksClassicAwayIII" : {'Texture': 'r3a009', 'Logo': 'logo009', 'Name': 'DB3623A5', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '0', 'SocksCol': '1', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': '141414', 'TColor2': 'FF3A3E', 'TColor3': 'FFC425', 'TColor4': 'FF3A3E', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"HawksClassicAwayIIIAlt" : {'Texture': 'r3x009', 'Logo': 'logo009', 'Name': 'CF5210A6', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '3', 'SocksCol': '1', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': '141414', 'TColor2': 'FFC425', 'TColor3': 'FF3A3E', 'TColor4': 'FFC425', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"HawksClassicAwayIV" : {'Texture': 'r4a009', 'Logo': 'logo009', 'Name': 'C151ECC2', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '0', 'SocksCol': '1', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': '141414', 'TColor2': 'E2383F', 'TColor3': 'FFE91E', 'TColor4': 'E2383F', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"HeatHome" : {'Texture': 'uh010', 'Logo': 'logo010', 'Name': 'B7E8E31A', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '4', 'SocksCol': '0', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': 'EBEBEB', 'TColor2': '98012E', 'TColor3': 'EBEBEB', 'TColor4': 'EBEBEB', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"HeatAway" : {'Texture': 'ua010', 'Logo': 'logo010', 'Name': 'F45673DE', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '4', 'SocksCol': '0', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': '141414', 'TColor2': '98012E', 'TColor3': '141414', 'TColor4': '141414', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"HeatAlternate" : {'Texture': 'ux010', 'Logo': 'logo010', 'Name': '39976E3D', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '4', 'SocksCol': '0', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': '141414', 'TColor2': '98012E', 'TColor3': 'EBEBEB', 'TColor4': '141414', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"HeatBackInBlack" : {'Texture': 'uax010', 'Logo': 'logo010', 'Name': '758B36E8', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '4', 'SocksCol': '0', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': '141414', 'TColor2': '141414', 'TColor3': 'EBEBEB', 'TColor4': '141414', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"HeatLatinNights" : {'Texture': 'r3h010', 'Logo': 'logo010', 'Name': '893F3614', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '4', 'SocksCol': '0', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': 'EBEBEB', 'TColor2': '98012E', 'TColor3': '141414', 'TColor4': '141414', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"HeatClassicHomeI" : {'Texture': 'r1h010', 'Logo': 'logo010', 'Name': '070E3F74', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '0', 'SocksCol': '0', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': 'EBEBEB', 'TColor2': 'E01A2C', 'TColor3': 'EBEBEB', 'TColor4': 'EBEBEB', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"HeatClassicAwayI" : {'Texture': 'r1a010', 'Logo': 'logo010', 'Name': '5897FDC4', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '0', 'SocksCol': '0', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': '141414', 'TColor2': 'E01A2C', 'TColor3': '141414', 'TColor4': '141414', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"HeatClassicAwayIAlt" : {'Texture': 'r1x010', 'Logo': 'logo010', 'Name': '0872C7C8', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '0', 'SocksCol': '0', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': '141414', 'TColor2': 'E01A2C', 'TColor3': '141414', 'TColor4': '141414', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"HeatClassicHomeII" : {'Texture': 'r2h010', 'Logo': 'logo010', 'Name': '2BDE5EAA', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '0', 'SocksCol': '0', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': 'EBEBEB', 'TColor2': 'F0037F', 'TColor3': 'F47A20', 'TColor4': 'EBEBEB', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"HornetsHome" : {'Texture': 'uh011', 'Logo': 'logo011', 'Name': 'B7E8E31A', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '4', 'SocksCol': '0', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': 'EBEBEB', 'TColor2': '008FC5', 'TColor3': 'FDC221', 'TColor4': 'EBEBEB', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"HornetsAway" : {'Texture': 'ua011', 'Logo': 'logo011', 'Name': 'F45673DE', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '4', 'SocksCol': '1', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': '141414', 'TColor2': '008FC5', 'TColor3': 'FDC221', 'TColor4': 'FDC221', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"HornetsAlternate" : {'Texture': 'ux011', 'Logo': 'logo011', 'Name': '39976E3D', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '4', 'SocksCol': '1', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': '141414', 'TColor2': 'FDB827', 'TColor3': '008FC5', 'TColor4': '272967', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"HornetsMardisGras" : {'Texture': 'uhx011', 'Logo': 'logo011', 'Name': '6A3F34A4', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '4', 'SocksCol': '0', 'UseCusClrs': '0', 'CusClrs4Nm': '1', 'TColor1': 'EBEBEB', 'TColor2': '1D1060', 'TColor3': 'FDBA31', 'TColor4': 'FDBA31', 'TColor5': '00853E', 'TColor6': '000000', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '6', 'FrNumCol2': '4', 'BkNumCol1': '6', 'BkNumCol2': '4', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"HornetsClassicHomeI" : {'Texture': 'r1h011', 'Logo': 'logo011', 'Name': '070E3F74', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '1', 'SocksCol': '0', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': 'EBEBEB', 'TColor2': '0093B2', 'TColor3': '0060AA', 'TColor4': 'EBEBEB', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"HornetsClassicAwayI" : {'Texture': 'r1a011', 'Logo': 'logo011', 'Name': '5897FDC4', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '1', 'SocksCol': '1', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': '141414', 'TColor2': '0093B2', 'TColor3': '0364AD', 'TColor4': '0093B2', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"HornetsClassicAwayIAlt" : {'Texture': 'r1x011', 'Logo': 'logo011', 'Name': '0872C7C8', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '1', 'SocksCol': '1', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': '141414', 'TColor2': '263997', 'TColor3': '40AEC5', 'TColor4': '263997', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"HornetsClassicHomeII" : {'Texture': 'r2h011', 'Logo': 'logo011', 'Name': '2BDE5EAA', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '1', 'SocksCol': '0', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': 'EBEBEB', 'TColor2': '0093B2', 'TColor3': '0B52AC', 'TColor4': 'EBEBEB', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"HornetsClassicAwayII" : {'Texture': 'r2a011', 'Logo': 'logo011', 'Name': 'E0E074E4', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '1', 'SocksCol': '1', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': '141414', 'TColor2': '00788A', 'TColor3': '061368', 'TColor4': '00788A', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"HornetsClassicHomeIII" : {'Texture': 'r3h011', 'Logo': 'logo011', 'Name': '4A997118', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '3', 'SocksCol': '0', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': 'EBEBEB', 'TColor2': '0093B1', 'TColor3': 'FCB116', 'TColor4': 'EBEBEB', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"HornetsClassicAwayIII" : {'Texture': 'r3a011', 'Logo': 'logo011', 'Name': 'DB3623A5', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '3', 'SocksCol': '1', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': '141414', 'TColor2': '0093B1', 'TColor3': 'FCB116', 'TColor4': '0093B1', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"HornetsClassicAwayIIIAlt" : {'Texture': 'r3x011', 'Logo': 'logo011', 'Name': 'CF5210A6', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '3', 'SocksCol': '1', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': '141414', 'TColor2': 'FDB827', 'TColor3': '0093B1', 'TColor4': 'FDB827', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"JazzHome" : {'Texture': 'uh012', 'Logo': 'logo012', 'Name': 'B7E8E31A', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '1', 'SocksCol': '0', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': 'EBEBEB', 'TColor2': '002A5C', 'TColor3': 'FCB034', 'TColor4': '004812', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"JazzAway" : {'Texture': 'ua012', 'Logo': 'logo012', 'Name': 'F45673DE', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '1', 'SocksCol': '1', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': '141414', 'TColor2': '002A5C', 'TColor3': 'FCB034', 'TColor4': '004812', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"JazzAlternate" : {'Texture': 'ux012', 'Logo': 'logo012', 'Name': '39976E3D', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '1', 'SocksCol': '1', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': '141414', 'TColor2': '004812', 'TColor3': '002A5C', 'TColor4': 'FCB034', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"JazzClassicHomeI" : {'Texture': 'r1h012', 'Logo': 'logo012', 'Name': '070E3F74', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '1', 'SocksCol': '0', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': 'EBEBEB', 'TColor2': '532F64', 'TColor3': 'F5B82B', 'TColor4': '532F64', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"JazzClassicAwayI" : {'Texture': 'r1a012', 'Logo': 'logo012', 'Name': '5897FDC4', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '1', 'SocksCol': '1', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': '141414', 'TColor2': '441F81', 'TColor3': 'FBC013', 'TColor4': '441F81', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"JazzClassicHomeII" : {'Texture': 'r2h012', 'Logo': 'logo012', 'Name': '2BDE5EAA', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '1', 'SocksCol': '0', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': 'EBEBEB', 'TColor2': '421F7D', 'TColor3': '00A5E0', 'TColor4': '421F7D', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"JazzClassicAwayII" : {'Texture': 'r2a012', 'Logo': 'logo012', 'Name': 'E0E074E4', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '1', 'SocksCol': '1', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': '141414', 'TColor2': '421F7D', 'TColor3': '00A5E0', 'TColor4': '421F7D', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"JazzClassicAwayIII" : {'Texture': 'r3a012', 'Logo': 'logo012', 'Name': 'DB3623A5', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '1', 'SocksCol': '1', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': '141414', 'TColor2': '31744E', 'TColor3': 'FBC013', 'TColor4': '31744E', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"JazzClassicHomeIV" : {'Texture': 'r4h012', 'Logo': 'logo012', 'Name': '0A6FC68C', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '1', 'SocksCol': '0', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': 'EBEBEB', 'TColor2': '002B5C', 'TColor3': '4C90CC', 'TColor4': '002B5C', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"JazzClassicAwayIV" : {'Texture': 'r4a012', 'Logo': 'logo012', 'Name': 'C151ECC2', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '1', 'SocksCol': '1', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': '141414', 'TColor2': '002B5C', 'TColor3': '4C90CC', 'TColor4': '002B5C', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"JazzClassicAwayIVAlt" : {'Texture': 'r4x012', 'Logo': 'logo012', 'Name': '248E0A7B', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '1', 'SocksCol': '1', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': '141414', 'TColor2': '4C90CC', 'TColor3': '002B5C', 'TColor4': '4C90CC', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"KingsHome" : {'Texture': 'uh013', 'Logo': 'logo013', 'Name': 'B7E8E31A', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '4', 'SocksCol': '1', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': '141414', 'TColor2': '253D96', 'TColor3': 'D7D7D7', 'TColor4': 'EBEBEB', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"KingsAway" : {'Texture': 'ua013', 'Logo': 'logo013', 'Name': 'F45673DE', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '4', 'SocksCol': '1', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': '141414', 'TColor2': '253D96', 'TColor3': '141414', 'TColor4': '141414', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"KingsAlternate" : {'Texture': 'ux013', 'Logo': 'logo013', 'Name': '39976E3D', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '4', 'SocksCol': '1', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': '141414', 'TColor2': '393996', 'TColor3': 'A6A8AB', 'TColor4': '141414', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"KingsClassicAwayI" : {'Texture': 'r1a013', 'Logo': 'logo013', 'Name': '5897FDC4', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '1', 'SocksCol': '1', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': '141414', 'TColor2': '567EB9', 'TColor3': 'F90030', 'TColor4': '567EB9', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"KingsClassicHomeII" : {'Texture': 'r2h013', 'Logo': 'logo013', 'Name': '2BDE5EAA', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '0', 'SocksCol': '1', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': '141414', 'TColor2': '393996', 'TColor3': 'D7D7D7', 'TColor4': '393996', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"KingsClassicAwayII" : {'Texture': 'r2a013', 'Logo': 'logo013', 'Name': 'E0E074E4', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '0', 'SocksCol': '1', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': '141414', 'TColor2': '393996', 'TColor3': '141414', 'TColor4': '393996', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"KingsClassicHomeIII" : {'Texture': 'r3h013', 'Logo': 'logo013', 'Name': '4A997118', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '1', 'SocksCol': '1', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': '141414', 'TColor2': '393A97', 'TColor3': 'D7D7D7', 'TColor4': '393A97', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"KingsClassicAwayIII" : {'Texture': 'r3a013', 'Logo': 'logo013', 'Name': 'DB3623A5', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '1', 'SocksCol': '1', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': '141414', 'TColor2': '393A97', 'TColor3': '141414', 'TColor4': '393A97', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"KingsClassicAwayIIIAlt" : {'Texture': 'r3x013', 'Logo': 'logo013', 'Name': 'CF5210A6', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '1', 'SocksCol': '1', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': '141414', 'TColor2': 'B79C6E', 'TColor3': '5A3F93', 'TColor4': 'B79C6E', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"KingsClassicHomeIV" : {'Texture': 'r4h013', 'Logo': 'logo013', 'Name': '0A6FC68C', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '0', 'SocksCol': '1', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': '141414', 'TColor2': 'E51837', 'TColor3': '0869B0', 'TColor4': 'EBEBEB', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"KingsClassicAwayV" : {'Texture': 'r5a013', 'Logo': 'logo013', 'Name': '792665E2', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '0', 'SocksCol': '1', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': '141414', 'TColor2': '393996', 'TColor3': '141414', 'TColor4': '393996', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"KnicksHome" : {'Texture': 'uh014', 'Logo': 'logo014', 'Name': 'B7E8E31A', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '1', 'SocksCol': '0', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': 'EBEBEB', 'TColor2': '007AC0', 'TColor3': 'F37021', 'TColor4': 'EBEBEB', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"KnicksAway" : {'Texture': 'ua014', 'Logo': 'logo014', 'Name': 'F45673DE', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '1', 'SocksCol': '1', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': '141414', 'TColor2': '007AC0', 'TColor3': 'F37021', 'TColor4': 'F37021', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"KnicksLatinNights" : {'Texture': 'uhx014', 'Logo': 'logo014', 'Name': '893F3614', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '1', 'SocksCol': '1', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': '141414', 'TColor2': 'F37021', 'TColor3': '00539F', 'TColor4': 'F37021', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"KnicksStPatricks" : {'Texture': 'uax014', 'Logo': 'logo014', 'Name': '39A2D4A5', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '1', 'SocksCol': '1', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': '141414', 'TColor2': '008348', 'TColor3': 'F37021', 'TColor4': '008348', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"KnicksClassicHomeI" : {'Texture': 'r1h014', 'Logo': 'logo014', 'Name': '070E3F74', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '1', 'SocksCol': '0', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': 'EBEBEB', 'TColor2': 'F37021', 'TColor3': '007AC1', 'TColor4': 'F37021', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"KnicksClassicAwayI" : {'Texture': 'r1a014', 'Logo': 'logo014', 'Name': '5897FDC4', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '1', 'SocksCol': '1', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': '141414', 'TColor2': '007AC1', 'TColor3': 'F37021', 'TColor4': '007AC1', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"KnicksClassicHomeII" : {'Texture': 'r2h014', 'Logo': 'logo014', 'Name': '2BDE5EAA', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '0', 'SocksCol': '0', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': 'EBEBEB', 'TColor2': '0B4499', 'TColor3': 'FF5C00', 'TColor4': '0B4499', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"KnicksClassicAwayII" : {'Texture': 'r2a014', 'Logo': 'logo014', 'Name': 'E0E074E4', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '0', 'SocksCol': '1', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': '141414', 'TColor2': '0B4499', 'TColor3': 'FF5C00', 'TColor4': '0B4499', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"KnicksClassicAwayIII" : {'Texture': 'r3a014', 'Logo': 'logo014', 'Name': 'DB3623A5', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '0', 'SocksCol': '1', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': '141414', 'TColor2': '0B4499', 'TColor3': 'FF5C00', 'TColor4': '0B4499', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"LakersHome" : {'Texture': 'uh015', 'Logo': 'logo015', 'Name': 'B7E8E31A', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '4', 'SocksCol': '0', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': 'EBEBEB', 'TColor2': 'FDB827', 'TColor3': '552582', 'TColor4': 'FDB827', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"LakersAlternate" : {'Texture': 'ux015', 'Logo': 'logo015', 'Name': '39976E3D', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '4', 'SocksCol': '0', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': 'EBEBEB', 'TColor2': '552582', 'TColor3': 'FDB827', 'TColor4': '552582', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"LakersAway" : {'Texture': 'ua015', 'Logo': 'logo015', 'Name': 'F45673DE', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '4', 'SocksCol': '1', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': '141414', 'TColor2': '552582', 'TColor3': 'FDB827', 'TColor4': '552582', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"LakersLatinNights" : {'Texture': 'uhx015', 'Logo': 'logo015', 'Name': '893F3614', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '4', 'SocksCol': '0', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': 'EBEBEB', 'TColor2': '552582', 'TColor3': 'FDB827', 'TColor4': '552582', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"LakersClassicHomeI" : {'Texture': 'r1h015', 'Logo': 'logo015', 'Name': '070E3F74', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '0', 'SocksCol': '0', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': 'EBEBEB', 'TColor2': 'FDB827', 'TColor3': '552582', 'TColor4': 'FDB827', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"LakersClassicAwayI" : {'Texture': 'r1a015', 'Logo': 'logo015', 'Name': '5897FDC4', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '0', 'SocksCol': '1', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': '141414', 'TColor2': '552582', 'TColor3': 'FDB827', 'TColor4': '552582', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"LakersClassicHomeII" : {'Texture': 'r2h015', 'Logo': 'logo015', 'Name': '2BDE5EAA', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '0', 'SocksCol': '0', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': 'EBEBEB', 'TColor2': '739DD3', 'TColor3': 'FDB827', 'TColor4': '739DD3', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"LakersClassicAwayII" : {'Texture': 'r2a015', 'Logo': 'logo015', 'Name': 'E0E074E4', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '0', 'SocksCol': '1', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': '141414', 'TColor2': '739DD3', 'TColor3': 'FDB827', 'TColor4': '739DD3', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"LakersClassicHomeIII" : {'Texture': 'r3h015', 'Logo': 'logo015', 'Name': '4A997118', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '0', 'SocksCol': '0', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': 'EBEBEB', 'TColor2': '0053A0', 'TColor3': '4B90CD', 'TColor4': '0053A0', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"LakersClassicAwayIII" : {'Texture': 'r3a015', 'Logo': 'logo015', 'Name': 'DB3623A5', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '0', 'SocksCol': '1', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': '141414', 'TColor2': '0053A0', 'TColor3': '4B90CD', 'TColor4': '0053A0', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"LakersClassicHomeIV" : {'Texture': 'r4h015', 'Logo': 'logo015', 'Name': '0A6FC68C', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '0', 'SocksCol': '0', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': 'EBEBEB', 'TColor2': 'FDB827', 'TColor3': '552583', 'TColor4': 'FDB827', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"MagicHome" : {'Texture': 'uh016', 'Logo': 'logo016', 'Name': 'B7E8E31A', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '4', 'SocksCol': '0', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': 'EBEBEB', 'TColor2': '0077C0', 'TColor3': 'D7D7D7', 'TColor4': '0077C0', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"MagicAway" : {'Texture': 'ua016', 'Logo': 'logo016', 'Name': 'F45673DE', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '4', 'SocksCol': '1', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': '141414', 'TColor2': '0077C0', 'TColor3': '141414', 'TColor4': '0077C0', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"MagicAlternate" : {'Texture': 'ux016', 'Logo': 'logo016', 'Name': '39976E3D', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '4', 'SocksCol': '1', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': '141414', 'TColor2': '0077C0', 'TColor3': '141414', 'TColor4': '0077C0', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"MagicLatinNights" : {'Texture': 'uhx016', 'Logo': 'logo016', 'Name': '893F3614', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '4', 'SocksCol': '0', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': 'EBEBEB', 'TColor2': '0077C0', 'TColor3': 'A7A9AC', 'TColor4': '0077C0', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"MagicClassicHomeI" : {'Texture': 'r1h016', 'Logo': 'logo016', 'Name': '070E3F74', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '0', 'SocksCol': '0', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': 'EBEBEB', 'TColor2': '0077C0', 'TColor3': 'D7D7D7', 'TColor4': '0077C0', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"MagicClassicAwayI" : {'Texture': 'r1a016', 'Logo': 'logo016', 'Name': '5897FDC4', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '0', 'SocksCol': '1', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': '141414', 'TColor2': '0077C0', 'TColor3': '141414', 'TColor4': '0077C0', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"MagicClassicAwayIAlt" : {'Texture': 'r1x016', 'Logo': 'logo016', 'Name': '0872C7C8', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '0', 'SocksCol': '1', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': '141414', 'TColor2': '0077C0', 'TColor3': 'D7D7D7', 'TColor4': '0077C0', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"MagicClassicHomeII" : {'Texture': 'r2h016', 'Logo': 'logo016', 'Name': '2BDE5EAA', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '3', 'SocksCol': '0', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': 'EBEBEB', 'TColor2': '0075BF', 'TColor3': 'D7D7D7', 'TColor4': '0075BF', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"MagicClassicAwayII" : {'Texture': 'r2a016', 'Logo': 'logo016', 'Name': 'E0E074E4', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '3', 'SocksCol': '1', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': '141414', 'TColor2': '0075BF', 'TColor3': '141414', 'TColor4': '0075BF', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"MavericksHome" : {'Texture': 'uh017', 'Logo': 'logo017', 'Name': 'B7E8E31A', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '4', 'SocksCol': '0', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': 'EBEBEB', 'TColor2': '00285D', 'TColor3': '006BB6', 'TColor4': 'EBEBEB', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"MavericksAway" : {'Texture': 'ua017', 'Logo': 'logo017', 'Name': 'F45673DE', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '4', 'SocksCol': '0', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': 'EBEBEB', 'TColor2': '00285D', 'TColor3': '006BB6', 'TColor4': '00285D', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"MavericksAlternate" : {'Texture': 'ux017', 'Logo': 'logo017', 'Name': '39976E3D', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '3', 'SocksCol': '0', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': 'EBEBEB', 'TColor2': '002A5C', 'TColor3': '0077C0', 'TColor4': 'EBEBEB', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"MavericksLatinNights" : {'Texture': 'uhx017', 'Logo': 'logo017', 'Name': '893F3614', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '3', 'SocksCol': '0', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': 'EBEBEB', 'TColor2': '0077C0', 'TColor3': '002D62', 'TColor4': '0077C0', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"MavericksClassicHomeI" : {'Texture': 'r1h017', 'Logo': 'logo017', 'Name': '070E3F74', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '0', 'SocksCol': '0', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': 'EBEBEB', 'TColor2': '00285E', 'TColor3': '007959', 'TColor4': '00285E', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"MavericksClassicAwayI" : {'Texture': 'r1a017', 'Logo': 'logo017', 'Name': '5897FDC4', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '0', 'SocksCol': '0', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': 'EBEBEB', 'TColor2': '00285E', 'TColor3': '007959', 'TColor4': '00285E', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"NetsHome" : {'Texture': 'uh018', 'Logo': 'logo018', 'Name': 'B7E8E31A', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '0', 'SocksCol': '0', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': 'EBEBEB', 'TColor2': 'EBEBEB', 'TColor3': '141414', 'TColor4': 'EBEBEB', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"NetsAway" : {'Texture': 'ua018', 'Logo': 'logo018', 'Name': 'F45673DE', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '0', 'SocksCol': '1', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': '141414', 'TColor2': '141414', 'TColor3': 'EBEBEB', 'TColor4': '141414', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"NetsClassicAwayI" : {'Texture': 'r1a018', 'Logo': 'logo018', 'Name': '5897FDC4', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '0', 'SocksCol': '0', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': 'EBEBEB', 'TColor2': '0068B3', 'TColor3': 'FA002C', 'TColor4': 'EBEBEB', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"NetsClassicHomeII" : {'Texture': 'r2h018', 'Logo': 'logo018', 'Name': '2BDE5EAA', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '1', 'SocksCol': '0', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': 'EBEBEB', 'TColor2': 'DF0C2B', 'TColor3': '00285D', 'TColor4': 'EBEBEB', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"NetsClassicAwayII" : {'Texture': 'r2a018', 'Logo': 'logo018', 'Name': 'E0E074E4', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '1', 'SocksCol': '0', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': 'EBEBEB', 'TColor2': '00285D', 'TColor3': 'DF0C2B', 'TColor4': 'DF0C2B', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"NuggetsHome" : {'Texture': 'uh019', 'Logo': 'logo019', 'Name': 'B7E8E31A', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '1', 'SocksCol': '0', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': 'EBEBEB', 'TColor2': '4D90CD', 'TColor3': 'FDB927', 'TColor4': 'EBEBEB', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"NuggetsAway" : {'Texture': 'ua019', 'Logo': 'logo019', 'Name': 'F45673DE', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '1', 'SocksCol': '0', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': 'EBEBEB', 'TColor2': '4D90CD', 'TColor3': 'FDB927', 'TColor4': '4D90CD', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"NuggetsNBAGreen" : {'Texture': 'uax019', 'Logo': 'logo019', 'Name': 'BDFBD6EE', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '3', 'SocksCol': '0', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': 'EBEBEB', 'TColor2': '0F5A49', 'TColor3': 'FDB927', 'TColor4': '0F5A49', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"NuggetsClassicHomeI" : {'Texture': 'r1h019', 'Logo': 'logo019', 'Name': '070E3F74', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '0', 'SocksCol': '0', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': 'EBEBEB', 'TColor2': 'FDE545', 'TColor3': '0B3D91', 'TColor4': 'FDE545', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"NuggetsClassicAwayI" : {'Texture': 'r1a019', 'Logo': 'logo019', 'Name': '5897FDC4', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '0', 'SocksCol': '0', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': 'EBEBEB', 'TColor2': '0061AA', 'TColor3': 'FFD520', 'TColor4': '0061AA', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"NuggetsClassicHomeII" : {'Texture': 'r2h019', 'Logo': 'logo019', 'Name': '2BDE5EAA', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '0', 'SocksCol': '0', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': 'EBEBEB', 'TColor2': 'F15C22', 'TColor3': '292A2C', 'TColor4': 'F15C22', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"NuggetsClassicHomeIII" : {'Texture': 'r3h019', 'Logo': 'logo019', 'Name': '4A997118', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '0', 'SocksCol': '0', 'UseCusClrs': '0', 'CusClrs4Nm': '1', 'TColor1': 'EBEBEB', 'TColor2': '0068B3', 'TColor3': 'ED174F', 'TColor4': 'EBEBEB', 'TColor5': '0068B3', 'TColor6': 'FFC423', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '5', 'FrNumCol2': '6', 'BkNumCol1': '5', 'BkNumCol2': '5', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"PacersHome" : {'Texture': 'uh020', 'Logo': 'logo020', 'Name': 'B7E8E31A', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '4', 'SocksCol': '0', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': 'EBEBEB', 'TColor2': '002D62', 'TColor3': 'FFC425', 'TColor4': '002D62', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"PacersAway" : {'Texture': 'ua020', 'Logo': 'logo020', 'Name': 'F45673DE', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '4', 'SocksCol': '0', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': 'EBEBEB', 'TColor2': '002D62', 'TColor3': 'FFC425', 'TColor4': '002D62', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"PacersAlternate" : {'Texture': 'ux020', 'Logo': 'logo020', 'Name': '39976E3D', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '4', 'SocksCol': '1', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': '141414', 'TColor2': 'F8C42A', 'TColor3': '1B3A60', 'TColor4': 'F8C42A', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"PacersClassicAwayI" : {'Texture': 'r1a020', 'Logo': 'logo020', 'Name': '5897FDC4', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '0', 'SocksCol': '1', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': '141414', 'TColor2': '1F3B69', 'TColor3': 'DBC516', 'TColor4': '1F3B69', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"PacersClassicHomeII" : {'Texture': 'r2h020', 'Logo': 'logo020', 'Name': '2BDE5EAA', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '1', 'SocksCol': '0', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': 'EBEBEB', 'TColor2': 'F7DC0A', 'TColor3': '14224F', 'TColor4': 'F7DC0A', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"PacersClassicAwayII" : {'Texture': 'r2a020', 'Logo': 'logo020', 'Name': 'E0E074E4', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '1', 'SocksCol': '0', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': 'EBEBEB', 'TColor2': '14224F', 'TColor3': 'F7DC01', 'TColor4': '14224F', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"PacersClassicAwayIIAlt" : {'Texture': 'r2x020', 'Logo': 'logo020', 'Name': 'E3609C76', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '1', 'SocksCol': '1', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': '141414', 'TColor2': 'FFD520', 'TColor3': '00285D', 'TColor4': 'FFD520', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"PacersClassicHomeIII" : {'Texture': 'r3h020', 'Logo': 'logo020', 'Name': '4A997118', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '0', 'SocksCol': '0', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': 'EBEBEB', 'TColor2': '006CB7', 'TColor3': 'FFD51E', 'TColor4': '006CB7', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"PacersClassicAwayIV" : {'Texture': 'r4a020', 'Logo': 'logo020', 'Name': 'C151ECC2', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '0', 'SocksCol': '0', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': 'EBEBEB', 'TColor2': '0068B3', 'TColor3': 'FAD529', 'TColor4': 'EBEBEB', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"PistonsHome" : {'Texture': 'uh021', 'Logo': 'logo021', 'Name': 'B7E8E31A', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '4', 'SocksCol': '0', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': 'EBEBEB', 'TColor2': 'DE0D2F', 'TColor3': '006BB6', 'TColor4': 'DE0D2F', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"PistonsAway" : {'Texture': 'ua021', 'Logo': 'logo021', 'Name': 'F45673DE', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '4', 'SocksCol': '0', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': 'EBEBEB', 'TColor2': '006BB6', 'TColor3': 'ED174B', 'TColor4': '006BB6', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"PistonsAlternate" : {'Texture': 'ux021', 'Logo': 'logo021', 'Name': '39976E3D', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '4', 'SocksCol': '0', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': 'EBEBEB', 'TColor2': 'DE0D2F', 'TColor3': '006BB6', 'TColor4': 'DE0D2F', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"PistonsClassicHomeI" : {'Texture': 'r1h021', 'Logo': 'logo021', 'Name': '070E3F74', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '0', 'SocksCol': '0', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': 'EBEBEB', 'TColor2': 'DE0D2F', 'TColor3': '006BB6', 'TColor4': 'DE0D2F', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"PistonsClassicAwayI" : {'Texture': 'r1a021', 'Logo': 'logo021', 'Name': '5897FDC4', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '0', 'SocksCol': '0', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': 'EBEBEB', 'TColor2': '006BB6', 'TColor3': 'DE0D2F', 'TColor4': '006BB6', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"PistonsClassicHomeII" : {'Texture': 'r2h021', 'Logo': 'logo021', 'Name': '2BDE5EAA', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '0', 'SocksCol': '0', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': 'EBEBEB', 'TColor2': '238B99', 'TColor3': 'E21B03', 'TColor4': '238B99', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"PistonsClassicAwayII" : {'Texture': 'r2a021', 'Logo': 'logo021', 'Name': 'E0E074E4', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '0', 'SocksCol': '0', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': 'EBEBEB', 'TColor2': '238B99', 'TColor3': 'E21B03', 'TColor4': '238B99', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"PistonsClassicHomeIII" : {'Texture': 'r3h021', 'Logo': 'logo021', 'Name': '4A997118', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '1', 'SocksCol': '0', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': 'EBEBEB', 'TColor2': 'DE0D2F', 'TColor3': '0869B0', 'TColor4': 'DE0D2F', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"RaptorsHome" : {'Texture': 'uh022', 'Logo': 'logo022', 'Name': 'B7E8E31A', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '4', 'SocksCol': '0', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': 'EBEBEB', 'TColor2': 'CE1723', 'TColor3': '141414', 'TColor4': 'C4CED3', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"RaptorsAway" : {'Texture': 'ua022', 'Logo': 'logo022', 'Name': 'F45673DE', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '4', 'SocksCol': '1', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': '141414', 'TColor2': 'CE1723', 'TColor3': '141414', 'TColor4': 'C4CED3', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"RaptorsAlternate" : {'Texture': 'ux022', 'Logo': 'logo022', 'Name': '39976E3D', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '4', 'SocksCol': '1', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': '141414', 'TColor2': 'CE1723', 'TColor3': 'C4CED3', 'TColor4': '141414', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"RaptorsMilitaryNight" : {'Texture': 'uhx022', 'Logo': 'logo022', 'Name': 'DD7BE75B', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '4', 'SocksCol': '0', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': 'EBEBEB', 'TColor2': '3A4B01', 'TColor3': '141414', 'TColor4': '886632', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"RaptorsStPatricks" : {'Texture': 'uax022', 'Logo': 'logo022', 'Name': '39A2D4A5', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '4', 'SocksCol': '1', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': '141414', 'TColor2': '008349', 'TColor3': '141414', 'TColor4': '008349', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"RaptorsClassicHomeI" : {'Texture': 'r1h022', 'Logo': 'logo022', 'Name': '070E3F74', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '4', 'SocksCol': '0', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': 'EBEBEB', 'TColor2': 'D01040', 'TColor3': '393A96', 'TColor4': 'D01040', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"RaptorsClassicAwayI" : {'Texture': 'r1a022', 'Logo': 'logo022', 'Name': '5897FDC4', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '4', 'SocksCol': '1', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': '141414', 'TColor2': '393A96', 'TColor3': 'D01040', 'TColor4': '393A96', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"RaptorsClassicHomeII" : {'Texture': 'r2h022', 'Logo': 'logo022', 'Name': '2BDE5EAA', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '0', 'SocksCol': '0', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': 'EBEBEB', 'TColor2': '5569B0', 'TColor3': 'D7D7D7', 'TColor4': '5569B0', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"RocketsHome" : {'Texture': 'uh023', 'Logo': 'logo023', 'Name': 'B7E8E31A', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '1', 'SocksCol': '0', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': 'EBEBEB', 'TColor2': 'CE1141', 'TColor3': 'D7D7D7', 'TColor4': 'CE1141', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"RocketsAway" : {'Texture': 'ua023', 'Logo': 'logo023', 'Name': 'F45673DE', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '1', 'SocksCol': '1', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': '141414', 'TColor2': 'CE1141', 'TColor3': 'D7D7D7', 'TColor4': 'CE1141', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"RocketsAlternate" : {'Texture': 'ux023', 'Logo': 'logo023', 'Name': '39976E3D', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '3', 'SocksCol': '1', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': '141414', 'TColor2': 'D03548', 'TColor3': 'F8C42A', 'TColor4': 'D03548', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"RocketsLatinNights" : {'Texture': 'uhx023', 'Logo': 'logo023', 'Name': '893F3614', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '1', 'SocksCol': '0', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': 'EBEBEB', 'TColor2': 'CE1141', 'TColor3': 'D7D7D7', 'TColor4': 'CE1141', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"RocketsClassicHomeI" : {'Texture': 'r1h023', 'Logo': 'logo023', 'Name': '070E3F74', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '0', 'SocksCol': '0', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': 'EBEBEB', 'TColor2': 'CE3747', 'TColor3': 'F7C325', 'TColor4': 'CE3747', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"RocketsClassicAwayI" : {'Texture': 'r1a023', 'Logo': 'logo023', 'Name': '5897FDC4', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '0', 'SocksCol': '1', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': '141414', 'TColor2': 'D40026', 'TColor3': 'FFC400', 'TColor4': 'D40026', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"RocketsClassicHomeII" : {'Texture': 'r2h023', 'Logo': 'logo023', 'Name': '2BDE5EAA', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '1', 'SocksCol': '0', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': 'EBEBEB', 'TColor2': '14214E', 'TColor3': 'CE1141', 'TColor4': '14214E', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"RocketsClassicAwayII" : {'Texture': 'r2a023', 'Logo': 'logo023', 'Name': 'E0E074E4', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '1', 'SocksCol': '1', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': '141414', 'TColor2': '14214E', 'TColor3': 'CE1141', 'TColor4': '14214E', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"SpursHome" : {'Texture': 'uh025', 'Logo': 'logo025', 'Name': 'B7E8E31A', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '1', 'SocksCol': '0', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': 'EBEBEB', 'TColor2': 'D7D7D7', 'TColor3': '141414', 'TColor4': 'EBEBEB', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"SpursAway" : {'Texture': 'ua025', 'Logo': 'logo025', 'Name': 'F45673DE', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '1', 'SocksCol': '1', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': '141414', 'TColor2': '141414', 'TColor3': 'D7D7D7', 'TColor4': '141414', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"SpursLatinNights" : {'Texture': 'uhx025', 'Logo': 'logo025', 'Name': '893F3614', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '0', 'SocksCol': '0', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': 'EBEBEB', 'TColor2': 'D7D7D7', 'TColor3': '141414', 'TColor4': 'EBEBEB', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"SpursClassicHomeI" : {'Texture': 'r1h025', 'Logo': 'logo025', 'Name': '070E3F74', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '0', 'SocksCol': '0', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': 'EBEBEB', 'TColor2': 'C6CDD3', 'TColor3': '141414', 'TColor4': 'C6CDD3', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"SpursClassicHomeII" : {'Texture': 'r2h025', 'Logo': 'logo025', 'Name': '2BDE5EAA', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '0', 'SocksCol': '0', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': 'EBEBEB', 'TColor2': 'ED174F', 'TColor3': '0068B3', 'TColor4': 'EBEBEB', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"SunsHome" : {'Texture': 'uh026', 'Logo': 'logo026', 'Name': 'B7E8E31A', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '4', 'SocksCol': '0', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': 'EBEBEB', 'TColor2': '4A207E', 'TColor3': 'CD5806', 'TColor4': 'EBEBEB', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"SunsAway" : {'Texture': 'ua026', 'Logo': 'logo026', 'Name': 'F45673DE', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '4', 'SocksCol': '1', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': '141414', 'TColor2': '4A207E', 'TColor3': 'CD5806', 'TColor4': '141414', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"SunsAlternate" : {'Texture': 'ux026', 'Logo': 'logo026', 'Name': '39976E3D', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '4', 'SocksCol': '1', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': '141414', 'TColor2': 'CD5806', 'TColor3': '4A207E', 'TColor4': 'CD5806', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"SunsLatinNights" : {'Texture': 'uhx026', 'Logo': 'logo026', 'Name': '893F3614', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '1', 'SocksCol': '0', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': 'EBEBEB', 'TColor2': 'CD5806', 'TColor3': '4A207E', 'TColor4': 'CD5806', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"SunsClassicHomeI" : {'Texture': 'r1h026', 'Logo': 'logo026', 'Name': '070E3F74', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '0', 'SocksCol': '0', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': 'EBEBEB', 'TColor2': 'F47D30', 'TColor3': '4F2683', 'TColor4': 'F47D30', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"SunsClassicAwayI" : {'Texture': 'r1a026', 'Logo': 'logo026', 'Name': '5897FDC4', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '0', 'SocksCol': '1', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': '141414', 'TColor2': '4F2683', 'TColor3': 'F47D30', 'TColor4': '4F2683', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"SunsClassicAwayII" : {'Texture': 'r2a026', 'Logo': 'logo026', 'Name': 'E0E074E4', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '0', 'SocksCol': '1', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': '141414', 'TColor2': '141414', 'TColor3': 'F37736', 'TColor4': '141414', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"ThunderHome" : {'Texture': 'uh024', 'Logo': 'logo024', 'Name': 'B7E8E31A', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '1', 'SocksCol': '0', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': 'EBEBEB', 'TColor2': '007DC3', 'TColor3': 'F05033', 'TColor4': '141414', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"ThunderAway" : {'Texture': 'ua024', 'Logo': 'logo024', 'Name': 'F45673DE', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '1', 'SocksCol': '0', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': 'EBEBEB', 'TColor2': '007DC3', 'TColor3': 'F05033', 'TColor4': '141414', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"TimberwolvesHome" : {'Texture': 'uh027', 'Logo': 'logo027', 'Name': 'B7E8E31A', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '4', 'SocksCol': '0', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': 'EBEBEB', 'TColor2': '005595', 'TColor3': '141414', 'TColor4': 'A7A9AC', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"TimberwolvesAway" : {'Texture': 'ua027', 'Logo': 'logo027', 'Name': 'F45673DE', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '4', 'SocksCol': '1', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': '141414', 'TColor2': '005595', 'TColor3': '141414', 'TColor4': 'A7A9AC', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"TimberwolvesAlternate" : {'Texture': 'ux027', 'Logo': 'logo027', 'Name': '39976E3D', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '4', 'SocksCol': '1', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': '141414', 'TColor2': '005595', 'TColor3': '141414', 'TColor4': '141414', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"TimberwolvesClassicHomeI" : {'Texture': 'r1h027', 'Logo': 'logo027', 'Name': '070E3F74', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '0', 'SocksCol': '0', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': 'EBEBEB', 'TColor2': '005083', 'TColor3': '00A261', 'TColor4': 'EBEBEB', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"TimberwolvesClassicAwayI" : {'Texture': 'r1a027', 'Logo': 'logo027', 'Name': '5897FDC4', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '0', 'SocksCol': '1', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': '141414', 'TColor2': '005083', 'TColor3': '00A261', 'TColor4': '141414', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"TimberwolvesClassicHomeII" : {'Texture': 'r2h027', 'Logo': 'logo027', 'Name': '2BDE5EAA', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '0', 'SocksCol': '0', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': 'EBEBEB', 'TColor2': '005083', 'TColor3': '008756', 'TColor4': 'EBEBEB', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"TimberwolvesClassicAwayII" : {'Texture': 'r2a027', 'Logo': 'logo027', 'Name': 'E0E074E4', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '0', 'SocksCol': '1', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': '141414', 'TColor2': '005083', 'TColor3': '008756', 'TColor4': '141414', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"TimberwolvesClassicAwayIIAlt" : {'Texture': 'r2x027', 'Logo': 'logo027', 'Name': 'E3609C76', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '0', 'SocksCol': '1', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': '141414', 'TColor2': '005083', 'TColor3': '008756', 'TColor4': '141414', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"TimberwolvesClassicHomeIII" : {'Texture': 'r3h027', 'Logo': 'logo027', 'Name': '4A997118', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '0', 'SocksCol': '0', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': 'EBEBEB', 'TColor2': '0068B3', 'TColor3': 'BC9B6A', 'TColor4': 'EBEBEB', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"TrailblazersHome" : {'Texture': 'uh028', 'Logo': 'logo028', 'Name': 'B7E8E31A', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '0', 'SocksCol': '0', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': 'EBEBEB', 'TColor2': 'E0393E', 'TColor3': 'D7D7D7', 'TColor4': 'E0393E', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"TrailblazersAway" : {'Texture': 'ua028', 'Logo': 'logo028', 'Name': 'F45673DE', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '0', 'SocksCol': '1', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': '141414', 'TColor2': 'E0393E', 'TColor3': '141414', 'TColor4': 'E0393E', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"TrailblazersRipCity" : {'Texture': 'uhx028', 'Logo': 'logo028', 'Name': '846A3685', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '3', 'SocksCol': '0', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': 'EBEBEB', 'TColor2': 'E0393E', 'TColor3': '141414', 'TColor4': 'E0393E', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"TrailblazersClassicHomeI" : {'Texture': 'r1h028', 'Logo': 'logo028', 'Name': '070E3F74', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '0', 'SocksCol': '0', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': 'EBEBEB', 'TColor2': 'D31145', 'TColor3': 'D7D7D7', 'TColor4': 'D31145', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"TrailblazersClassicAwayI" : {'Texture': 'r1a028', 'Logo': 'logo028', 'Name': '5897FDC4', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '0', 'SocksCol': '1', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': '141414', 'TColor2': 'D31145', 'TColor3': '141414', 'TColor4': 'D31145', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"TrailblazersClassicHomeII" : {'Texture': 'r2h028', 'Logo': 'logo028', 'Name': '2BDE5EAA', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '0', 'SocksCol': '0', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': 'EBEBEB', 'TColor2': 'B6050E', 'TColor3': 'D7D7D7', 'TColor4': 'B6050E', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"TrailblazersClassicAwayII" : {'Texture': 'r2a028', 'Logo': 'logo028', 'Name': 'E0E074E4', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '0', 'SocksCol': '1', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': '141414', 'TColor2': 'B6050E', 'TColor3': '141414', 'TColor4': 'B6050E', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"WarriorsHome" : {'Texture': 'uh029', 'Logo': 'logo029', 'Name': 'B7E8E31A', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '4', 'SocksCol': '0', 'UseCusClrs': '0', 'CusClrs4Nm': '1', 'TColor1': 'EBEBEB', 'TColor2': '0068B3', 'TColor3': 'FFC423', 'TColor4': '0068B3', 'TColor5': '0068B3', 'TColor6': 'FFC423', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '6', 'FrNumCol2': '6', 'BkNumCol1': '5', 'BkNumCol2': '5', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"WarriorsAway" : {'Texture': 'ua029', 'Logo': 'logo029', 'Name': 'F45673DE', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '4', 'SocksCol': '1', 'UseCusClrs': '0', 'CusClrs4Nm': '1', 'TColor1': '141414', 'TColor2': '0068B3', 'TColor3': 'FFC423', 'TColor4': '0068B3', 'TColor5': 'FFC423', 'TColor6': '0068B3', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '6', 'FrNumCol2': '6', 'BkNumCol1': '5', 'BkNumCol2': '5', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"WarriorsClassicHomeI" : {'Texture': 'r1h029', 'Logo': 'logo029', 'Name': '070E3F74', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '0', 'SocksCol': '0', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': 'EBEBEB', 'TColor2': '2C3294', 'TColor3': 'FBD227', 'TColor4': '2C3294', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"WarriorsClassicAwayI" : {'Texture': 'r1a029', 'Logo': 'logo029', 'Name': '5897FDC4', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '0', 'SocksCol': '1', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': '141414', 'TColor2': '2C3294', 'TColor3': 'FBD227', 'TColor4': '2C3294', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"WarriorsClassicHomeII" : {'Texture': 'r2h029', 'Logo': 'logo029', 'Name': '2BDE5EAA', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '0', 'SocksCol': '0', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': 'EBEBEB', 'TColor2': 'FFC423', 'TColor3': '005696', 'TColor4': 'CB073E', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"WarriorsClassicHomeIII" : {'Texture': 'r3h029', 'Logo': 'logo029', 'Name': '4A997118', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '0', 'SocksCol': '0', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': 'EBEBEB', 'TColor2': 'F7B928', 'TColor3': '14214E', 'TColor4': 'F7B928', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"WarriorsClassicAwayIII" : {'Texture': 'r3a029', 'Logo': 'logo029', 'Name': 'DB3623A5', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '0', 'SocksCol': '1', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': '141414', 'TColor2': '005696', 'TColor3': 'FFC431', 'TColor4': '005696', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"WarriorsClassicHomeIV" : {'Texture': 'r4h029', 'Logo': 'logo029', 'Name': '0A6FC68C', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '3', 'SocksCol': '0', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': 'EBEBEB', 'TColor2': '00275D', 'TColor3': 'DB5833', 'TColor4': 'DB5833', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"WarriorsClassicAwayIV" : {'Texture': 'r4a029', 'Logo': 'logo029', 'Name': 'C151ECC2', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '3', 'SocksCol': '1', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': '141414', 'TColor2': '00275D', 'TColor3': 'F9A01B', 'TColor4': 'DB5833', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"WarriorsClassicAwayIVAlt" : {'Texture': 'r4x029', 'Logo': 'logo029', 'Name': '248E0A7B', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '3', 'SocksCol': '1', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': '141414', 'TColor2': 'DB5833', 'TColor3': '00275D', 'TColor4': '00275D', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"WarriorsClassicHomeV" : {'Texture': 'r5h029', 'Logo': 'logo029', 'Name': '26BFA752', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '0', 'SocksCol': '0', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': 'EBEBEB', 'TColor2': 'FFC423', 'TColor3': '0068B3', 'TColor4': 'FFC423', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"WizardsHome" : {'Texture': 'uh002', 'Logo': 'logo002', 'Name': 'B7E8E31A', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '1', 'SocksCol': '0', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': 'EBEBEB', 'TColor2': 'E31837', 'TColor3': '002B5C', 'TColor4': 'EBEBEB', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"WizardsAway" : {'Texture': 'ua002', 'Logo': 'logo002', 'Name': 'F45673DE', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '1', 'SocksCol': '1', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': '141414', 'TColor2': 'E31837', 'TColor3': '002B5C', 'TColor4': '141414', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"WizardsClassicHomeI" : {'Texture': 'r1h002', 'Logo': 'logo002', 'Name': '070E3F74', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '0', 'SocksCol': '0', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': 'EBEBEB', 'TColor2': '0B3D91', 'TColor3': 'E90012', 'TColor4': 'EBEBEB', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"WizardsClassicAwayI" : {'Texture': 'r1a002', 'Logo': 'logo002', 'Name': '5897FDC4', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '0', 'SocksCol': '1', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': '141414', 'TColor2': '0B3D91', 'TColor3': 'E90012', 'TColor4': '0B3D91', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"WizardsClassicHomeII" : {'Texture': 'r2h002', 'Logo': 'logo002', 'Name': '2BDE5EAA', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '1', 'SocksCol': '0', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': 'EBEBEB', 'TColor2': 'EE7B31', 'TColor3': '1E3B60', 'TColor4': 'EBEBEB', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"WizardsClassicHomeIII" : {'Texture': 'r3h002', 'Logo': 'logo002', 'Name': '4A997118', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '0', 'SocksCol': '0', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': 'EBEBEB', 'TColor2': 'BC9B6A', 'TColor3': '002D62', 'TColor4': 'EBEBEB', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"WizardsClassicHomeIV" : {'Texture': 'r4h002', 'Logo': 'logo002', 'Name': '0A6FC68C', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '1', 'SocksCol': '0', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': 'EBEBEB', 'TColor2': '005083', 'TColor3': 'BC9B6A', 'TColor4': 'EBEBEB', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"WizardsClassicAwayIV" : {'Texture': 'r4a002', 'Logo': 'logo002', 'Name': 'C151ECC2', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '1', 'SocksCol': '1', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': '141414', 'TColor2': '005083', 'TColor3': 'BC9B6A', 'TColor4': '141414', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'},
"WizardsClassicAwayIVAlt" : {'Texture': 'r4x002', 'Logo': 'logo002', 'Name': '248E0A7B', 'CATTmplNm': '00000000', 'ShortsStl': '0', 'JModel': '1', 'SocksCol': '1', 'UseCusClrs': '0', 'CusClrs4Nm': '0', 'TColor1': '141414', 'TColor2': 'BC9B6A', 'TColor3': '191919', 'TColor4': '141414', 'TColor5': 'FFFFFF', 'TColor6': '323232', 'JColor1': '0', 'JColor2': '0', 'JColor3': '0', 'LColor1': '0', 'LColor2': '0', 'LColor3': '0', 'NameColor': '0', 'FrNumCol1': '0', 'FrNumCol2': '0', 'BkNumCol1': '0', 'BkNumCol2': '0', 'ShsColor1': '0', 'ShsColor2': '1', 'ShsColor3': '2'}}

# This class handles all communications with Databases and CSV sets.
class DataStorage:

    # Init method defaults to opening the players, stats, and all roster files. Options exist
    # to manually disable these, as well as manually set the paths to databases.
    def __init__(self, openCSVFiles=True, openPlayers=True, openStats = True,
                 playersPathOverride: str = None, statsPathOverride: str = None):

        if(playersPathOverride is None):
            self.__playersDBPath = f"{b.paths.databases}\\Players.db" # Default PlayersDB path
        else:
            self.__playersDBPath = playersPathOverride

        if(statsPathOverride is None):
            self.__statsDBPath = f"{b.paths.databases}\\Stats.db" # Default StatsDB path
        else:
            self.__statsDBPath = statsPathOverride

        self.rosters = {}
        self.__csvDBDict = {}
        self.__csvCursorDict = {}
        if (openCSVFiles):
            savedRosters = self.csv_GetSavedRosterList()
            for roster in savedRosters:
                self.csv_ImportCSVs(roster)

        self.players = {}
        self.__playersDB = None
        self.__playersCursor = None
        if (openPlayers):
            self.playersDB_Open()
            self.playersDB_DownloadPlayers()

        self.stats = {}
        self.__statsDB = None
        self.__statsCursor = None
        if(openStats):
            self.statsDB_Open()
            self.statsDB_DownloadRaw()

    # region === CSV/Roster Management ===

    # This method simply returns an array of all managed and saved roster directories.
    @staticmethod
    def csv_GetSavedRosterList():
        returnArray = []
        for item in os.listdir(b.paths.rosterCSVs):
            if (os.path.isdir(os.path.join(b.paths.rosterCSVs, item))):
                returnArray.append(item)
        return returnArray

    # This method updates a single RosterID's SpriteID in the RosterVals.db database.
    def __csv_UpdateSpriteID(self, rosterName, rosterID, spriteID):
        query = f'UPDATE SpriteIDs SET SpriteID = {spriteID} WHERE RosterID = {rosterID};'
        self.__csvCursorDict[rosterName].execute(query)
        self.__csvDBDict[rosterName].commit()
    # This method adds a valid height adjustment (between 0.00 and 2.53) for the given RosterID, applies it,
    # stores it in RosterVals.db, and returns True if the Roster isn't yet full. realHeight should be in inches.
    def __csv_AdjustHeight(self, rosterName, rosterID, realHeight):
        if (realHeight == -1):
            query = f"UPDATE HeightMap SET RealHeight = {realHeight}, HeightAdjustment = 0 WHERE RosterID = {rosterID}"
            self.__csvCursorDict[rosterName].execute(query)
            self.__csvDBDict[rosterName].commit()
        else:
            query = f"SELECT HeightAdjustment FROM HeightMap WHERE RealHeight = {realHeight}"
            self.__csvCursorDict[rosterName].execute(query)
            records = self.__csvCursorDict[rosterName].fetchall()
            allCurrentAdjustments = [record[0] for record in records]

            validAdjustments = []
            for i in range(254):
                if (i in allCurrentAdjustments):
                    continue
                else:
                    validAdjustments.append(i)

            if (len(validAdjustments) == 0):
                raise ValueError(
                    f"UH OH HOMIE! You got WAY too many players with this height: {realHeight}. Can't add any more to this roster!")
            thisAdjustment = random.choice(validAdjustments)

            query = f"UPDATE HeightMap SET RealHeight = {realHeight}, HeightAdjustment = {thisAdjustment} WHERE RosterID = {rosterID}"
            self.__csvCursorDict[rosterName].execute(query)
            self.__csvDBDict[rosterName].commit()

            self.rosters[rosterName]["Players"][rosterID]["Height"] = str(
                round((realHeight * 2.54) + (thisAdjustment * 0.01), 2))
    # This method uses the RosterVals.db database present alongside each exported Roster csv set to generate
    # a dictionary that matches each ID of the Players tab of the rosterName roster to a SpriteID.
    def csv_GenSpriteIDDict(self, rosterName):
        allUsedPlayerIDs = self.csv_FindAllUsedPlayerIDs(rosterName)
        query = f'SELECT SpriteID FROM SpriteIDs WHERE RosterID IN ({str(allUsedPlayerIDs).strip("[]")})'

        self.__csvCursorDict[rosterName].execute(query)
        spriteIDList = self.__csvCursorDict[rosterName].fetchall()

        spriteIDDict = {}
        for i in range(len(allUsedPlayerIDs)):
            spriteIDDict[allUsedPlayerIDs[i]] = spriteIDList[i][0]

        self.rosters[rosterName]["SpriteIDs"] = spriteIDDict
    # This method uses the RosterVals.db database present alongside each exported Roster csv set to generate
    # a dictionary that matches each RosterID with the player's height adjustment.
    def csv_GenHeightAdjustmentDict(self,rosterName):
        allUsedPlayerIDs = self.csv_FindAllUsedPlayerIDs(rosterName)
        query = f'SELECT * FROM HeightMap WHERE RosterID IN ({str(allUsedPlayerIDs).strip("[]")})'

        self.__csvCursorDict[rosterName].execute(query)
        heightAdjustmentRows = self.__csvCursorDict[rosterName].fetchall()

        heightMap = {}
        for row in heightAdjustmentRows:
            heightMap[row[0]] = {"RealHeight" : row[1], "HeightAdjustment" : row[2]}

        self.rosters[rosterName]["HeightMap"] = heightMap
    # This method uses the RosterVals.db database present alongside each exported Roster csv set to generate
    # a dictionary of Jersey config values.
    def csv_GenJerseyConfigDict(self,rosterName):
        query = f'SELECT * FROM JerseyConfig'

        self.__csvCursorDict[rosterName].execute(query)
        jerseyConfigRows = self.__csvCursorDict[rosterName].fetchall()

        jerseyConfig = {}
        for row in jerseyConfigRows:
            jerseyConfig[row[0]] = row[1]

        self.rosters[rosterName]["JerseyConfig"] = jerseyConfig
    # This method simply returns the SpriteID of a player on a roster, given RosterID.
    def csv_GetSpriteIDFromRosterID(self, rosterName, rosterID):
        return self.rosters[rosterName]["SpriteIDs"].get(rosterID,None)
    # This method simply returns the RosterID if a player exists on a roster with given SpriteID.
    def csv_GetRosterIDFromSpriteID(self, rosterName, spriteID):
        for rosterID in self.rosters[rosterName]["SpriteIDs"]:
            if (str(self.rosters[rosterName]["SpriteIDs"][rosterID]) == str(spriteID)):
                return rosterID

    # This helper method loads all aspects of CSV and SpriteID.db information into this local DataStorage
    # object for use.
    def csv_ImportCSVs(self, rosterName):
        # This method looks for the associated rosterName folder in b.paths.rosterCSVs path to read (import) the 4
        # exported CSV files into self.rosters = {}, overwriting whatever was there under
        # rosterName previously.
        def readBaseCSVs():
            def readCSVFileToDict(filePath):
                with open(filePath, "r", encoding="utf16") as f:
                    reader = csv.DictReader(f, delimiter=",")
                    return [row for row in reader]

            self.rosters[rosterName] = {
                "Players": readCSVFileToDict(f"{b.paths.rosterCSVs}\\{rosterName}\\Players.csv"),
                "Headshapes": readCSVFileToDict(f"{b.paths.rosterCSVs}\\{rosterName}\\Headshapes.csv"),
                "Teams": readCSVFileToDict(f"{b.paths.rosterCSVs}\\{rosterName}\\Teams.csv"),
                "Jerseys": readCSVFileToDict(f"{b.paths.rosterCSVs}\\{rosterName}\\Jerseys.csv"),
            }

        readBaseCSVs()

        # This simply generates necessary db connection and cursor objects to hook into this rosterName's
        # RosterVals.db data file. If the db doesn't exist for this roster yet, it creates it.
        def genRosterValsDBConnection():
            rosterValsDBPath = f"{b.paths.rosterCSVs}\\{rosterName}\\RosterVals.db"
            if (not os.path.exists(rosterValsDBPath)):
                needsTableBuilt = True
            else:
                needsTableBuilt = False
            if (rosterName not in self.__csvDBDict):
                self.__csvDBDict[rosterName] = sql.connect(rosterValsDBPath)
                self.__csvCursorDict[rosterName] = self.__csvDBDict[rosterName].cursor()
                if (needsTableBuilt):
                    spriteIDTableQuery = '''CREATE TABLE "SpriteIDs" ("RosterID" INTEGER UNIQUE, "SpriteID" INTEGER, PRIMARY KEY("RosterID"));'''
                    self.__csvCursorDict[rosterName].execute(spriteIDTableQuery)
                    # Insert 1000 entries with a SpriteID of -1
                    for i in range(1, 1001):
                        self.__csvCursorDict[rosterName].execute(
                            '''INSERT INTO "SpriteIDs" ("RosterID", "SpriteID") VALUES (?, -1);''', (i,))

                    heightMapTableQuery = '''CREATE TABLE "HeightMap" ("RosterID" INTEGER,"RealHeight" INTEGER,"HeightAdjustment" INTEGER,PRIMARY KEY("RosterID"));'''
                    self.__csvCursorDict[rosterName].execute(heightMapTableQuery)
                    for i in range(1, 1001):
                        self.__csvCursorDict[rosterName].execute(
                            '''INSERT INTO "HeightMap" ("RosterID","RealHeight","HeightAdjustment") VALUES (?,-1,0);''',
                            (i,))

                    jerseyConfigTableQuery = '''CREATE TABLE "JerseyConfig" ("JerseyOption" TEXT UNIQUE, "JerseyValue"	TEXT, PRIMARY KEY("JerseyOption"));'''
                    self.__csvCursorDict[rosterName].execute(jerseyConfigTableQuery)
                    jerseyConfigQuery = '''INSERT INTO JerseyConfig (JerseyOption, JerseyValue) VALUES (?,?)'''
                    jerseyConfigOptions = ["BallerzSlayer","BallerzVigilante","BallerzMedic","BallerzGuardian","BallerzEngineer","BallerzDirector","RingersSlayer","RingersVigilante","RingersMedic","RingersGuardian","RingersEngineer","RingersDirector",]
                    for jerseyConfigOption in jerseyConfigOptions:
                        self.__csvCursorDict[rosterName].execute(jerseyConfigQuery,(jerseyConfigOption,"GrizzliesHome"))

                    self.__csvDBDict[rosterName].commit()

        genRosterValsDBConnection()

        self.csv_GenSpriteIDDict(rosterName)
        self.csv_GenHeightAdjustmentDict(rosterName)
        self.csv_GenJerseyConfigDict(rosterName)
    # This method turns a CSV dictionary into four files, saves them to the rosterName csv folder for
    # RedMC import, and overwrites any existing files there.
    def csv_ExportCSVs(self, rosterName):
        if (not os.path.exists(f"{b.paths.rosterCSVs}\\{rosterName}")):
            os.mkdir(f"{b.paths.rosterCSVs}\\{rosterName}")

        # Helper function to write a single CSV file from a csvData set.
        def writeCSVDictToFile(filePath: str, csvData: list):
            with open(filePath, "w", newline="", encoding="UTF-16") as f:
                writer = csv.DictWriter(f, fieldnames=csvData[0].keys(), quoting=csv.QUOTE_NONNUMERIC)
                writer.writeheader()
                writer.writerows(csvData)

        # WriteCSVDictToFile for all 4 relevant files.
        writeCSVDictToFile(filePath=f"{b.paths.rosterCSVs}\\{rosterName}\\Players.csv",
                           csvData=self.rosters[rosterName]["Players"])
        writeCSVDictToFile(filePath=f"{b.paths.rosterCSVs}\\{rosterName}\\Headshapes.csv",
                           csvData=self.rosters[rosterName]["Headshapes"])
        writeCSVDictToFile(filePath=f"{b.paths.rosterCSVs}\\{rosterName}\\Teams.csv",
                           csvData=self.rosters[rosterName]["Teams"])
        writeCSVDictToFile(filePath=f"{b.paths.rosterCSVs}\\{rosterName}\\Jerseys.csv",
                           csvData=self.rosters[rosterName]["Jerseys"])

    # This method overwrites the given RosterID in the Players tab of rosterName with the given
    # Player object. If no Player is given, the player will instead be 'removed', which
    # essentially means the RosterID is set to inactive and their name is reset.
    def csv_UpdatePlayer(self, rosterName, rosterID, player: Player.Player = None):
        rosterID = int(rosterID)
        if(rosterID > 999):
            raise ValueError(f"ERROR: RosterID must be <= 999, given value is {rosterID}")
        if (player is None):
            self.rosters[rosterName]["Players"][rosterID]["IsRegNBA"] = "0"
            self.rosters[rosterName]["Players"][rosterID]["First_Name"] = f"*{b.alphaBase26(decimalNumber=rosterID,maxPlaces=15)}"
            self.rosters[rosterName]["Players"][rosterID]["Last_Name"] = f"*{b.alphaBase26(decimalNumber=-1 * rosterID - 1,maxPlaces=15)}"
            self.rosters[rosterName]["Players"][rosterID]["NickName"] = "**************"
            self.__csv_UpdateSpriteID(rosterName, rosterID, -1)
            self.csv_GenSpriteIDDict(rosterName)
            self.__csv_AdjustHeight(rosterName=rosterName, rosterID=rosterID, realHeight=-1)
            self.csv_GenHeightAdjustmentDict(rosterName)
            self.csv_GenJerseyConfigDict(rosterName)
        else:
            player["HS_ID"] = rosterID
            player["PortrID"] = str(rosterID + 9999)
            player["NickName"] = ""
            player["ASA_ID"] = "0"
            # Check if this player is not a normal archetype
            if (player["Archetype"] is None):
                player["TeamID1"] = "7"
                player["TeamID2"] = "7"

            # Update all Players tab values
            for key in self.rosters[rosterName]["Players"][0].keys():
                if (key == "Height"):  # Skip height for now, as we need to set it specially later
                    finalVal = "0"
                elif (key in ["ID"] or key == ""):  # Skip bad keys
                    continue
                else:
                    finalVal = str(player[key])
                self.rosters[rosterName]["Players"][rosterID][key] = finalVal

            # Update all Headshapes tab values
            for key in self.rosters[rosterName]["Headshapes"][0].keys():
                if (key in ["HS_ID", "ID"] or key == ""):
                    continue
                else:
                    self.rosters[rosterName]["Headshapes"][rosterID][key] = str(player[key])

            # Final clean up, adjusting height properly and updating SpriteID db
            self.__csv_AdjustHeight(rosterName=rosterName, rosterID=rosterID, realHeight=player["HeightIn"])
            self.__csv_UpdateSpriteID(rosterName, rosterID, player["SpriteID"])
            self.csv_GenSpriteIDDict(rosterName)
            self.csv_GenHeightAdjustmentDict(rosterName)
            self.csv_GenJerseyConfigDict(rosterName)
    # This method uses exported CSVs (specifically, headshapes and players csvs) to generate a Player object.
    # Assumes rosterName CSVs are already exported and up to date. It uses rosterID to target a single player.
    def csv_ExtractPlayer(self, rosterName, rosterID):
        player = Player.Player()
        for key, value in self.rosters[rosterName]['Players'][rosterID]:
            if (key not in ["ID", "HS_ID", "Height"] and key != ""):
                player[key] = value

        # True height needs to be extracted from RosterVals.db
        query = f"SELECT RealHeight FROM HeightMap WHERE RosterID = {rosterID}"
        self.__csvCursorDict[rosterName].execute(query)
        realHeight = self.__csvCursorDict[rosterName].fetchone()[0]
        player["Height"] = realHeight

        # Grab HS_ID for future use
        HS_ID = int(self.rosters[rosterName]["Players"][rosterID]["HS_ID"])

        for key, value in self.rosters[rosterName]['Headshapes'][HS_ID]:
            if (key != "HS_ID"):
                player[key] = value
        return player

    # This method simply returns the first unused RosterID on the "Players" tab of a CSV dict
    # TODO Max rosterID error handling
    def csv_FindFirstUnusedRosterID(self, rosterName):
        for singlePlayer in self.rosters[rosterName]["Players"][1:]:
            if (singlePlayer["IsRegNBA"] == "1"):
                continue
            else:
                return singlePlayer["ID"]
    # This method simply returns a list of all used RosterIDs on the "Players" tab of a CSV dict
    def csv_FindAllUsedPlayerIDs(self, rosterName):
        returnList = []
        for singlePlayer in self.rosters[rosterName]["Players"][1:]:
            if (singlePlayer["IsRegNBA"] == "1"):
                returnList.append(int(singlePlayer["ID"]))
        return returnList
    # This method uses the HeightMap table of RosterVals.db to determine, given a list of SpriteIDs,
    # the mapped Ball Handling IDs for that team.
    def csv_FindBallHandlingMap(self, rosterName, rosterIDs: list):
        query = f"SELECT * FROM HeightMap WHERE RosterID IN {tuple(rosterIDs)} ORDER BY RealHeight DESC,HeightAdjustment DESC"
        self.__csvCursorDict[rosterName].execute(query)
        results = self.__csvCursorDict[rosterName].fetchall()

        resultList = []
        for row in results:
            resultList.append(row[0])
        return resultList

    # This function updates the given rosterName with Jersey information as defined in this roster's
    # JerseyConfig.
    def csv_UpdateAllJerseys(self, rosterName):
        # This dict stores the constant values we will be editing, based on what config value
        # we're updating.
        translationDict = {"BallerzSlayer": 61,
                           "BallerzVigilante": 74,
                           "BallerzMedic": 82,
                           "BallerzGuardian": 91,
                           "BallerzEngineer": 100,
                           "BallerzDirector": 116,
                           "RingersSlayer": 60,
                           "RingersVigilante": 73,
                           "RingersMedic": 81,
                           "RingersGuardian": 90,
                           "RingersEngineer": 99,
                           "RingersDirector": 115}

        for configVal, jerseyPosition in translationDict.items():
            thisJerseyVal = self.rosters[rosterName]["JerseyConfig"][configVal]
            jerseyContent = JERSEY_DICT[thisJerseyVal]

            # Now we loop through each value in the Jerseys tab of RedMC.
            counter = 0

            for elementName in jerseyContent.keys():
                self.rosters[rosterName]["Jerseys"][jerseyPosition][elementName] = jerseyContent[elementName]
                counter += 1

        self.csv_ExportCSVs(rosterName)

        # Finally, we ensure that the Jersey configurations are now saved in the actualy RosterVals.db.
        updateJerseyConfigQuery = "UPDATE JerseyConfig SET JerseyValue = ? WHERE JerseyOption = ?"
        for jerseyOption,jerseyValue in self.rosters[rosterName]["JerseyConfig"].items():
            self.__csvCursorDict[rosterName].execute(updateJerseyConfigQuery,(jerseyValue,jerseyOption))
        self.__csvDBDict[rosterName].commit()

    # endregion === CSV/Roster Management ===

    # region === Players Table Management ===

    # Simple open function forms connection to Players.db
    def playersDB_Open(self):
        self.__playersDB = sql.connect(self.__playersDBPath)
        self.__playersDB.row_factory = sql.Row
        self.__playersCursor = self.__playersDB.cursor()

    # This method simply returns the count of Players currently in the players table.
    def playersDB_GetPlayerCount(self):
        countQuery = "SELECT COUNT(*) FROM Players;"
        self.__playersCursor.execute(countQuery)
        rowCount = self.__playersCursor.fetchone()[0]
        return rowCount
    # This function simply returns the first unused SpriteID from the players table.
    def playersDB_GetFirstUnusedSpriteID(self):
        if(self.playersDB_GetPlayerCount() == 0):
            return 0
        else:
            spriteQuery = "SELECT MAX(SpriteID) FROM Players;"
            self.__playersCursor.execute(spriteQuery)
            maxSpriteID = self.__playersCursor.fetchone()[0]
            return maxSpriteID + 1

    # This method downloads the full Players.db into this object's self.players member.
    def playersDB_DownloadPlayers(self):
        query = "SELECT * FROM Players;"
        self.__playersCursor.execute(query)
        results = self.__playersCursor.fetchall()

        allPlayers = {}
        for row in results:
            thisPlayer = Player.Player()
            thisPlayer["SpriteID"] = row["SpriteID"]
            for key in thisPlayer.vals.keys():
                thisPlayer[key] = row[key]
            if(row["PMods"] is not None):
                thisPlayer.pmods = json.loads(row["PMods"])
            allPlayers[thisPlayer["SpriteID"]] = thisPlayer

        self.players = allPlayers
    # This method uploads any changed Players in the self.players dict to the Players.db file.
    # It also handles insertion of new Players as well as SpriteID assignment.
    def playersDB_UploadPlayers(self):
        nextNewSpriteID = self.playersDB_GetFirstUnusedSpriteID()

        pendingQueries = []
        for spriteID,thisPlayer in self.players.items():
            # We only want to update/insert this Player if its marked as updated.
            if(thisPlayer.hasPendingUpdates):
                # Declare initial values for queries/value tuple
                columnNameQuery = "INSERT OR REPLACE INTO Players ("
                valuesQuery = "VALUES ("
                values = []

                # First we build the info part of the query
                for key in thisPlayer.vals.keys():
                    columnNameQuery += f"{key}, "
                    valuesQuery += "?, "
                    if (key == "Archetype"):
                        finalVal = thisPlayer["Archetype_Name"]
                    else:
                        finalVal = thisPlayer[key]
                    values.append(finalVal)
                # We also handle serializing potential PMods for this Player.
                columnNameQuery += "PMods, "
                valuesQuery += "?, "
                if(len(thisPlayer.pmods) > 0):
                    values.append(json.dumps(thisPlayer.pmods))
                else:
                    values.append(None)
                # Now, we append the SpriteID to actually replace/insert into the
                # correct SpriteID.
                columnNameQuery += "SpriteID)"
                valuesQuery += "?)"
                # A negative SpriteID means this Player object hasn't yet been assigned
                # an actual SpriteID, and needs one.
                if(spriteID < 0):
                    thisPlayer["SpriteID"] = nextNewSpriteID
                    values.append(nextNewSpriteID)
                    nextNewSpriteID += 1
                else:
                    values.append(spriteID)
                # Now we append the actual query for eventual execution.
                pendingQueries.append((f"{columnNameQuery} {valuesQuery}",values))

                # We finally mark this Player object as no longer having pending updates.
                thisPlayer.hasPendingUpdates = False

        for query in pendingQueries:
            self.__playersCursor.execute(query[0], query[1])
        self.__playersDB.commit()

    # Helper method for adding a new player to the self.players dict. To save this player,
    # UploadPlayers MUST BE RUN or the player will be lost after program closes.
    def playersDB_AddPlayer(self,player : Player.Player):
        tempSpriteID = min(self.players.keys()) - 1 if len(self.players.keys()) > 0 else -1
        player["SpriteID"] = tempSpriteID
        self.players[tempSpriteID] = player

    # endregion === Players Table Management ===

    # region === Stats Table Management ===

    # Simply opens a single, maintained connection with the Stats.db database.
    def statsDB_Open(self):
        self.__statsDB = sql.connect(self.__statsDBPath)
        self.__statsDB.row_factory = sql.Row
        self.__statsCursor = self.__statsDB.cursor()

    # Downloads the full Stats database in the stats member of this object.
    def statsDB_DownloadRaw(self):
        # Fetch all games
        self.__statsCursor.execute("SELECT * FROM Games")
        games = self.__statsCursor.fetchall()

        gamesDict = {}
        for game in games:
            gameId = game['GameID']
            gameDict = dict(game)

            # Fetch player slots for this game
            self.__statsCursor.execute("SELECT * FROM PlayerSlots WHERE GameID = ?", (gameId,))
            playerSlots = self.__statsCursor.fetchall()

            gameDict["DataState"] = "Committed"
            gameDict["PlayerSlots"] = {}
            for playerSlot in playerSlots:
                playerSlotDict = dict(playerSlot)
                playerSlotDict["DataState"] = "Committed"
                slotID = playerSlotDict["PlayerSlot"]
                gameDict["PlayerSlots"][slotID] = playerSlotDict

            # Add this game's dictionary to the main dictionary
            gamesDict[gameId] = gameDict

        self.stats["Raw"] = gamesDict
    # Uploads all changes made to the Stats dict to the actual stats database.
    def statsDB_UploadRaw(self):
        updateQueries = []
        insertQueries = []
        # Iterate through each game in the dictionary
        for gameId, gameInfo in self.stats["Raw"].items():
            # Check if the game is marked as updated.
            if(gameInfo["DataState"] == "Updated"):
                # Prepare an UPDATE statement for the Games table
                updateGameQuery = """
                    UPDATE Games SET
                    LoadedRoster = ?,
                    Mode = ?,
                    PlayDate = ?,
                    GameDuration = ?,
                    BallerzScore = ?,
                    RingersScore = ?,
                    ExtraValue1 = ?, ExtraValue2 = ?, ExtraValue3 = ?,
                    ExtraValue4 = ?, ExtraValue5 = ?, ExtraValue6 = ?,
                    ExtraValue7 = ?, ExtraValue8 = ?, ExtraValue9 = ?,
                    ExtraValue10 = ?
                    WHERE GameID = ?
                """
                gameVals = (
                    gameInfo["LoadedRoster"],
                    gameInfo["Mode"],
                    gameInfo["PlayDate"],
                    gameInfo["GameDuration"],
                    gameInfo["BallerzScore"],
                    gameInfo["RingersScore"],
                    gameInfo["ExtraValue1"],
                    gameInfo["ExtraValue2"],
                    gameInfo["ExtraValue3"],
                    gameInfo["ExtraValue4"],
                    gameInfo["ExtraValue5"],
                    gameInfo["ExtraValue6"],
                    gameInfo["ExtraValue7"],
                    gameInfo["ExtraValue8"],
                    gameInfo["ExtraValue9"],
                    gameInfo["ExtraValue10"],
                    gameId
                )
                updateQueries.append((updateGameQuery,gameVals))
            # Check if the game is marked as new.
            elif(gameInfo["DataState"] == "New"):
                # Prepare an INSERT statement for the Games table
                insertGameQuery = """
                    INSERT INTO Games (
                        GameID, LoadedRoster, Mode, PlayDate, GameDuration, BallerzScore, RingersScore,
                        ExtraValue1, ExtraValue2, ExtraValue3, ExtraValue4, ExtraValue5,
                        ExtraValue6, ExtraValue7, ExtraValue8, ExtraValue9, ExtraValue10
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """
                gameVals = (
                    gameId,
                    gameInfo["LoadedRoster"],
                    gameInfo["Mode"],
                    gameInfo["PlayDate"],
                    gameInfo["GameDuration"],
                    gameInfo["BallerzScore"],
                    gameInfo["RingersScore"],
                    gameInfo["ExtraValue1"],
                    gameInfo["ExtraValue2"],
                    gameInfo["ExtraValue3"],
                    gameInfo["ExtraValue4"],
                    gameInfo["ExtraValue5"],
                    gameInfo["ExtraValue6"],
                    gameInfo["ExtraValue7"],
                    gameInfo["ExtraValue8"],
                    gameInfo["ExtraValue9"],
                    gameInfo["ExtraValue10"]
                )
                insertQueries.append((insertGameQuery, gameVals))

            # Iterate through each player slot in the game
            for slotId, slotInfo in gameInfo["PlayerSlots"].items():
                # Check if the player slot is marked as "Dirty"
                if(slotInfo["DataState"] == "Updated"):
                    # Prepare an UPDATE statement for the PlayerSlots table
                    updateSlotQuery = """
                        UPDATE PlayerSlots SET
                        IsActive = ?, SpriteID = ?, RosterID = ?, Points = ?,
                        DefensiveRebounds = ?, OffensiveRebounds = ?, PointsPerAssist = ?,
                        AssistCount = ?, Steals = ?, Blocks = ?, Turnovers = ?,
                        InsidesMade = ?, InsidesAttempted = ?, ThreesMade = ?,
                        ThreesAttempted = ?, Fouls = ?, Dunks = ?, Layups = ?,
                        Unknown1 = ?, Unknown2 = ?
                        WHERE GameID = ? AND PlayerSlot = ?
                    """
                    slotVals = (
                        slotInfo["IsActive"],
                        slotInfo["SpriteID"],
                        slotInfo["RosterID"],
                        slotInfo["Points"],
                        slotInfo["DefensiveRebounds"],
                        slotInfo["OffensiveRebounds"],
                        slotInfo["PointsPerAssist"],
                        slotInfo["AssistCount"],
                        slotInfo["Steals"],
                        slotInfo["Blocks"],
                        slotInfo["Turnovers"],
                        slotInfo["InsidesMade"],
                        slotInfo["InsidesAttempted"],
                        slotInfo["ThreesMade"],
                        slotInfo["ThreesAttempted"],
                        slotInfo["Fouls"],
                        slotInfo["Dunks"],
                        slotInfo["Layups"],
                        slotInfo["Unknown1"],
                        slotInfo["Unknown2"],
                        gameId,
                        slotId
                    )
                    updateQueries.append((updateSlotQuery,slotVals))
                elif(slotInfo["DataState"] == "New"):
                    # Prepare an INSERT statement for the PlayerSlots table
                    insertSlotQuery = """
                        INSERT INTO PlayerSlots (
                            GameID, PlayerSlot, IsActive, SpriteID, RosterID, Points,
                            DefensiveRebounds, OffensiveRebounds, PointsPerAssist, AssistCount, Steals,
                            Blocks, Turnovers, InsidesMade, InsidesAttempted, ThreesMade,
                            ThreesAttempted, Fouls, Dunks, Layups, Unknown1, Unknown2
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """
                    slotVals = (
                        gameId,
                        slotInfo["PlayerSlot"],
                        slotInfo["IsActive"],
                        slotInfo["SpriteID"],
                        slotInfo["RosterID"],
                        slotInfo["Points"],
                        slotInfo["DefensiveRebounds"],
                        slotInfo["OffensiveRebounds"],
                        slotInfo["PointsPerAssist"],
                        slotInfo["AssistCount"],
                        slotInfo["Steals"],
                        slotInfo["Blocks"],
                        slotInfo["Turnovers"],
                        slotInfo["InsidesMade"],
                        slotInfo["InsidesAttempted"],
                        slotInfo["ThreesMade"],
                        slotInfo["ThreesAttempted"],
                        slotInfo["Fouls"],
                        slotInfo["Dunks"],
                        slotInfo["Layups"],
                        slotInfo["Unknown1"],
                        slotInfo["Unknown2"]
                    )
                    insertQueries.append((insertSlotQuery, slotVals))

        # Finally, we actually execute all statements.
        for query, vals in updateQueries:
            self.__statsCursor.execute(query, vals)
        for query, vals in insertQueries:
            self.__statsCursor.execute(query, vals)

        # Commit the changes
        self.__statsCursor.commit()

        self.statsDB_DownloadRaw()

    # This method uses a stats object, which is assumed to have a full ripped game in it, and adds it as a new game row
    # to the stats.db. It also returns the GameID of the saved game.
    def statsDB_AddRippedGame(self, statsObject, extraValues=None):
        newGameID = max(self.stats["Raw"].keys()) + 1
        newGame = {"DataState" : "New",
                   "GameID" : newGameID,
                   "LoadedRoster" : statsObject.loadedRoster,
                   "Mode" : statsObject.gameMode,
                   "PlayDate" : date.today().strftime("%Y-%m-%d"),
                   "GameDuration" : None, #TODO
                   "BallerzScore" : statsObject.ballerzScore,
                   "RingersScore" : statsObject.ringersScore}
        if(type(extraValues) is not list): # TODO maybe make these kwargs instead?
            extraValues = []

        for i in range(1,11):
            if(len(extraValues) >= i):
                newGame[f"ExtraValue{i}"] = extraValues[i-1]
            else:
                newGame[f"ExtraValue{i}"] = None


        playerSlots = {}
        for slotName,slotInfo in statsObject.slotStats["slotStats"].items():
            slotId = int(slotName.split("Slot")[1])
            thisPlayerSlot = {"DataState" : "New",
                              "GameID" : newGameID,
                              "PlayerSlot" : slotId,
                              "IsActive" : slotInfo["IsActive"],
                              "SpriteID" : self.csv_GetSpriteIDFromRosterID(statsObject.loadedRoster.split(".ROS")[0], slotInfo['RosterID']),
                              "RosterID" : slotInfo['RosterID'],
                              "Points" : slotInfo["Points"],
                              "DefensiveRebounds" : slotInfo["DefensiveRebounds"],
                              "OffensiveRebounds" : slotInfo["OffensiveRebounds"],
                              "PointsPerAssist" : slotInfo["PointsPerAssist"],
                              "AssistCount" : slotInfo["AssistCount"],
                              "Steals" : slotInfo["Steals"],
                              "Blocks" : slotInfo["Blocks"],
                              "Turnovers" : slotInfo["Turnovers"],
                              "InsidesMade" : slotInfo["InsidesMade"],
                              "InsidesAttempted" : slotInfo["InsidesAttempted"],
                              "ThreesMade" : slotInfo["ThreesMade"],
                              "ThreesAttempted" : slotInfo["ThreesAttempted"],
                              "Fouls" : slotInfo["Fouls"],
                              "Dunks" : slotInfo["Dunks"],
                              "Layups" : slotInfo["Layups"],
                              "Unknown1" : slotInfo["Unknown1"],
                              "Unknown2" : slotInfo["Unknown2"]
                              }
            playerSlots[slotId] = thisPlayerSlot
        newGame["PlayerSlots"] = playerSlots

        self.stats["Raw"][newGameID] = newGame

        return newGameID

    # endregion === Stats Table Management ===

    #region === Helpers ===

    # This method uses CAP information from a Roster CSV set to overwrite the given Player with.
    # with. This method assumes that the roster set is already exported and up to date. Should
    # be used after we make changes to Player's faces in game to save them permanently on Players.db.
    def updatePlayerCAPInfoFromRoster(self,rosterName,spriteID):
        rosterID = self.csv_GetRosterIDFromSpriteID(rosterName, spriteID)

        capVals = ["CAP_FaceT",
                     "CAP_Hstl",
                     "CAP_Hcol",
                     "CAP_Hlen",
                     "CAP_BStyle",
                     "CAP_Moust",
                     "CAP_Goatee",
                     "CAP_Fhcol",
                     "CAP_Eyebr",
                     "CAP_T_LftN",
                     "CAP_T_LftS",
                     "CAP_T_RgtS",
                     "CAP_T_LftB",
                     "CAP_T_RgtB",
                     "CAP_T_LftF",
                     "CAP_T_RgtF",
                     "GHeadband",
                    "GHdbndLg",
                    "GUndrshrt",
                    "GUndrsCol",
                    "GLeftArm",
                    "GLArmCol",
                    "GLeftElb",
                    "GLElbCol",
                    "GLeftWrst",
                    "GLWrstC1",
                    "GLWrstC2",
                    "GLeftFngr",
                    "GLFngrCol",
                    "GRghtArm",
                    "GRArmCol",
                    "GRghtElb",
                    "GRElbCol",
                    "GRghtWrst",
                    "GRWrstC1",
                    "GRWrstC2",
                    "GRghtFngr",
                    "GRFngrCol",
                    "GPresShrt",
                    "GPrsShCol",
                    "GLeftLeg",
                    "GLLegCol",
                    "GLeftKnee",
                    "GLKneeCol",
                    "GLeftAnkl",
                    "GLAnklCol",
                    "GRghtLeg",
                    "GRLegCol",
                    "GRghtKnee",
                    "GRKneeCol",
                    "GRghtAnkl",
                    "GRAnklCol",
                    "GSockLngh",
                    "GShsBrLck",
                    "GShsBrand",
                    "GShsModel",
                    "GShsUCusC",
                    "GShsTHC1",
                    "GShsTHC2",
                    "GShsTAC1",
                    "GShsTAC2",
                    "GShsHCol1",
                    "GShsHCol2",
                    "GShsHCol3",
                    "GShsACol1",
                    "GShsACol2",
                    "GShsACol3",
                    "Weight",
                    "SkinTone",
                    "Muscles",
                    "EyeColor",
                    "Bodytype",
                    "Clothes",
                    "Number"]
        headshapeVals = ["HParam1",
                         "HParam2",
                         "HdBrwHght",
                         "HdBrwWdth",
                         "HdBrwSlpd",
                         "HdNkThck",
                         "HdNkFat",
                         "HdChnLen",
                         "HdChnWdth",
                         "HdChnProt",
                         "HdJawSqr",
                         "HdJawWdth",
                         "HdChkHght",
                         "HdChkWdth",
                         "HdChkFull",
                         "HdDefinit",
                         "MtULCurve",
                         "MtULThick",
                         "MtULProtr",
                         "MtLLCurve",
                         "MtLLThick",
                         "MtLLProtr",
                         "MtSzHght",
                         "MtSzWdth",
                         "MtCrvCorn",
                         "ErHeight",
                         "ErWidth",
                         "ErEarLobe",
                         "ErTilt",
                         "NsNsHght",
                         "NsNsWdth",
                         "NsNsProtr",
                         "NsBnBridge",
                         "NsBnDefin",
                         "NsBnWdth",
                         "NsTipHght",
                         "NsTipWdth",
                         "NsTipTip",
                         "NsTipBnd",
                         "NsNtHght",
                         "NsNtWdth",
                         "EsFrmOpen",
                         "EsFrmSpac",
                         "EsFrmLwEl",
                         "EsFrmUpEl",
                         "EsPlcHght",
                         "EsPlcWdth",
                         "EsPlcRot",
                         "EsPlcProt",
                         "EsShpOtEl",
                         "EsShpInEl"]

        for capVal in capVals:
            self.players[spriteID][capVal] = self.rosters[rosterName]["Players"][rosterID][capVal]
        for headshapeVal in headshapeVals:
            self.players[spriteID][headshapeVal] = self.rosters[rosterName]["Headshapes"][rosterID][headshapeVal]

    #endregion === Helpers ===

# The actual, global DataStorage object used.
d = DataStorage()
StatsProcessing.generatePlayerGamesDict(d)
StatsProcessing.calculatePlayerAverages(d)


'''
# Use this code to test the size of each important part of a dataStorageObject, as
# well as the general size of non-data members.

print(f"Players Size: {b.getMemorySizeOf(d.players)}")
print(f"Stats Size: {b.getMemorySizeOf(d.stats)}")
print(f"Rosters Size: {b.getMemorySizeOf(d.rosters)}")
d.players,d.stats,d.rosters = {},{},{}
print(f"(Other) Size: {b.getMemorySizeOf(d)}")
'''