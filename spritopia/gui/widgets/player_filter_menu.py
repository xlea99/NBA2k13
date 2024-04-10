from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from functools import partial
from spritopia.data_storage.data_storage import d
from spritopia.gui.widgets.auto_resize_label import AutoResizeLabel
from spritopia.gui.widgets.input_combo_box import InputComboBox
from spritopia.players.players import Player
from spritopia.data_storage import player_filter
from spritopia.players.factions import dbDict as factions
from spritopia.common.localization import LOCALIZATION_PLAYERS, LOCALIZATION_STATS
from spritopia.utilities.misc import getMemorySizeOf


#region === Field Map Construction ===

FIELDS = []
# Load initial "top" vals
for specialVal in player_filter.specialConditionTypeDict.keys():
    FIELDS.append({"Icon": specialVal,
                   "Category": "Special",
                   "Domain": None,
                   "Subdomain": None,
                   "Value": specialVal})
for basicVal in Player.valCategories["Basic Info"]:
    FIELDS.append({"Icon": LOCALIZATION_PLAYERS[basicVal],
                   "Category": "Basic Info",
                   "Domain": "Players",
                   "Subdomain": None,
                   "Value": basicVal})
for attributeVal in Player.valCategories["Attributes"]:
    FIELDS.append({"Icon": LOCALIZATION_PLAYERS[attributeVal],
                   "Category": "Attributes",
                   "Domain": "Players",
                   "Subdomain": None,
                   "Value": attributeVal})

# Load all stat vals
for totalStatVal in LOCALIZATION_STATS["Totals"].keys():
    FIELDS.append({"Icon": LOCALIZATION_STATS["Totals"][totalStatVal],
                   "Category": "Stats",
                   "Domain": "Stats",
                   "Subdomain": "Totals",
                   "Value": totalStatVal})
for averageStatVal in LOCALIZATION_STATS["Averages"].keys():
    FIELDS.append({"Icon": LOCALIZATION_STATS["Averages"][averageStatVal],
                   "Category": "Stats",
                   "Domain": "Stats",
                   "Subdomain": "Averages",
                   "Value": averageStatVal})
for otherStatVal in LOCALIZATION_STATS["Other"].keys():
    FIELDS.append({"Icon": LOCALIZATION_STATS["Other"][otherStatVal],
                   "Category": "Stats",
                   "Domain": "Stats",
                   "Subdomain": "Other",
                   "Value": otherStatVal})

# Load rest of the player vals
for tendencyVal in Player.valCategories["Tendencies"]:
    FIELDS.append({"Icon": LOCALIZATION_PLAYERS[tendencyVal],
                   "Category": "Tendencies",
                   "Domain": "Players",
                   "Subdomain": None,
                   "Value": tendencyVal})
for hotspotVal in Player.valCategories["Hotspots"]:
    FIELDS.append({"Icon": LOCALIZATION_PLAYERS[hotspotVal],
                   "Category": "Hotspots",
                   "Domain": "Players",
                   "Subdomain": None,
                   "Value": hotspotVal})
for hotzoneVal in Player.valCategories["Hotzones"]:
    FIELDS.append({"Icon": LOCALIZATION_PLAYERS[hotzoneVal],
                   "Category": "Hotzones",
                   "Domain": "Players",
                   "Subdomain": None,
                   "Value": hotzoneVal})
for appearanceVal in Player.valCategories["Appearance"]:
    FIELDS.append({"Icon": LOCALIZATION_PLAYERS[appearanceVal],
                   "Category": "Appearance",
                   "Domain": "Players",
                   "Subdomain": None,
                   "Value": appearanceVal})
for animationVal in Player.valCategories["Animations"]:
    FIELDS.append({"Icon": LOCALIZATION_PLAYERS[animationVal],
                   "Category": "Animations",
                   "Domain": "Players",
                   "Subdomain": None,
                   "Value": animationVal})
for extraVal in Player.extraValuesMap.keys():
    FIELDS.append({"Icon": LOCALIZATION_PLAYERS[extraVal],
                   "Category": "Animations",
                   "Domain": "Players",
                   "Subdomain": None,
                   "Value": extraVal})

SORT_FIELDS = {
    "Basic Info" : {"IsBold" : True},
    "Attributes" : {"IsBold" : True},
    "Special" : {"IsBold" : True},
    "Stats" : {"IsBold" : True},
    "Tendencies" : {"IsBold" : False},
    "Hotspots" : {"IsBold" : False},
    "Hotzones" : {"IsBold" : False},
    "Appearance" : {"IsBold" : False},
    "Animations" : {"IsBold" : False},
    "Extra Values" : {"IsBold" : False},
}

#endregion === Field Map Construction ===

# Maps to which operators are available to which fields.
OPERATOR_MAP = {
    "Default" : ["==","!=",">",">=","<","<=","contains","does not contain"],
    "IsOnRoster": ["==","!="]
}
OPERATOR_LOCALIZED = {
    "==": "equals",
    "!=": "does_not_equal",
    ">": "greater_than",
    ">=": "greater_than_or_equal_to",
    "<": "less_than",
    "<=": "less_than_or_equal_to",
    "contains": "contains"
}
# A list of values to provide as a combo box, dependent on certain selected fields.
VALUE_COMBO_MAP = {
    "IsOnRoster": {"Values": list(d.rosters.keys()),"Sorted": True},
    "Archetype": {"Values": ["Slayer","Vigilante","Medic","Guardian","Engineer","Director","None"],"Sorted": False},
    "Rarity": {"Values": ["Common","Rare","Epic","Legendary","Godlike"],"Sorted": False},
    "Race": {"Values": list(factions["Races"].keys()),"Sorted": True},
    "Faction" : {"Values": list(factions["Factions"].keys()),"Sorted": True}
}




class PlayerFilterMenu(QDialog):
    # Signal for apply button.
    filterApplied = Signal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.currentFilterDict = {}
        self.currentFieldFilter = "All"

        self.setWindowTitle("Filter Preferences")
        self.setMinimumWidth(340)

        # Use QVBoxLayout for simple vertical layout
        self.layout = QVBoxLayout()

        # Setup actual rules table.
        self.rulesTable = QTableWidget()
        self.rulesTable.setMaximumWidth(313) #TODO adjust
        self.rulesTable.setColumnCount(3)
        self.rulesTable.setHorizontalHeaderLabels(['Field', 'Condition', 'Value'])

        # Header and "showOnly" combo box.
        self.headerContainer = QWidget()
        self.headerLayout = QHBoxLayout(self.headerContainer)
        self.showOnlyLabel = QLabel("Show Only: ")
        self.showOnlyComboBox = QComboBox()
        self.showOnlyComboBox.currentIndexChanged.connect(self.updateFieldFilter)
        showOnlyComboBoxItemModel = QStandardItemModel()
        # First, add the top "All" option.
        topItem = QStandardItem("All")
        font = topItem.font()
        font.setBold(True)
        font.setUnderline(True)
        topItem.setFont(font)
        showOnlyComboBoxItemModel.appendRow(topItem)
        # Now dynamically add all other field sort options.
        for fieldCategory,formattingOptions in SORT_FIELDS.items():
            thisItem = QStandardItem(fieldCategory)
            font = thisItem.font()
            font.setBold(formattingOptions["IsBold"])
            thisItem.setFont(font)
            showOnlyComboBoxItemModel.appendRow(thisItem)
        self.showOnlyComboBox.setModel(showOnlyComboBoxItemModel)
        self.headerLayout.addWidget(self.showOnlyLabel)
        self.headerLayout.addWidget(self.showOnlyComboBox)

        # Setup rule operator buttons
        self.ruleOperatorContainer = QWidget()
        self.ruleOperatorLayout = QHBoxLayout(self.ruleOperatorContainer)
        self.newRowButton = QPushButton("Add Rule")
        self.newRowButton.clicked.connect(self.addRuleRow)
        self.clearAllButton = QPushButton("Clear Rules")
        self.clearAllButton.clicked.connect(self.clearAllRuleRows)
        self.ruleOperatorLayout.addWidget(self.newRowButton)
        self.ruleOperatorLayout.addWidget(self.clearAllButton)

        # Add apply button, as well as separator.
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        separator.setStyleSheet("color: rgba(0, 0, 0, 50);")  # Adjust the color and opacity for faded effect
        self.applyButton = QPushButton("Apply Filters")
        self.applyButton.clicked.connect(self.apply)

        self.layout.addWidget(self.headerContainer)
        self.layout.addWidget(self.rulesTable)
        self.layout.addWidget(self.ruleOperatorContainer)
        self.layout.addWidget(separator)
        self.layout.addWidget(self.applyButton)
        self.setLayout(self.layout)

        self.applyButton.clicked.connect(self.onApplyClicked)

    #region === Filter Generation ===

    # Applies (returns) the condition dictionary created by the GUI and closes the filter.
    def apply(self):
        self.currentFilterDict = self.getCurrentFilterDict()
        self.accept()
    def onApplyClicked(self):
        self.filterApplied.emit(self.currentFilterDict)
    # This method converts the full rule table into a single player_filter dictionary.
    def getCurrentFilterDict(self):
        newRuleDict = {"type": "and","conditions": []}
        for row in range(self.rulesTable.rowCount()):
            thisFieldDict = self.rulesTable.cellWidget(row,0).getCurrentItemData()
            thisOperator = self.rulesTable.cellWidget(row,1).currentText()

            thisValueElement = self.rulesTable.cellWidget(row,2)
            if(thisValueElement):
                thisValue = thisValueElement.currentText()
            else:
                thisValue = self.rulesTable.item(row,2).text()

            thisCondition = {
                    "type": OPERATOR_LOCALIZED[thisOperator],
                    "domain": thisFieldDict["Domain"],
                    "subdomain": thisFieldDict["Subdomain"],
                    "field": thisFieldDict["Value"],
                    "value": thisValue
                }
            if(thisFieldDict["Value"] == "IsOnRoster"):
                thisCondition["type"] = "special"
                if(thisOperator == "!="):
                    newRuleDict["conditions"].append({"type": "not", "condition": thisCondition})
                else:
                    newRuleDict["conditions"].append(thisCondition)
            elif(thisOperator == "does not contain"):
                newRuleDict["conditions"].append({"type": "not","condition": thisCondition})
            else:
                newRuleDict["conditions"].append(thisCondition)

        print(newRuleDict)
        return newRuleDict

    #endregion === Filter Generation ===

    #region === Table Manipulation ===

    # Methods for adding and removing rules visually from the rule table.
    def addRuleRow(self):
        rowPosition = self.rulesTable.rowCount()
        self.rulesTable.insertRow(rowPosition)

        # Create InputComboBox instances for each cell that needs it
        fieldComboBox = InputComboBox()
        conditionComboBox = InputComboBox()
        valueComboBox = InputComboBox()


        # Get the first valid field for the currently set category.
        defaultField = FIELDS[0]
        if(self.currentFieldFilter != "Any"):
            for field in FIELDS:
                if(field["Category"] == self.currentFieldFilter):
                    defaultField = field
                    break
        # Default values.
        fieldComboBox.addItem("", defaultField)
        conditionComboBox.addItem("", "")
        valueComboBox.addItem("", "")

        # Connect each fieldComboBox to get valid operators.
        fieldComboBox.currentTextChanged.connect(partial(self.updateFieldRelationships,row=rowPosition))

        # Set combo boxes as cell widgets
        self.rulesTable.setCellWidget(rowPosition, 0, fieldComboBox)
        self.rulesTable.setCellWidget(rowPosition, 1, conditionComboBox)
        self.rulesTable.setItem(rowPosition, 2, QTableWidgetItem(""))

        self.updateFieldFilter(0)
    def removeRuleRow(self, rowPosition):
        # Check if the position is valid before attempting to remove
        if 0 <= rowPosition < self.rulesTable.rowCount():
            self.rulesTable.removeRow(rowPosition)
        else:
            print("Invalid row position: ", rowPosition)
    def clearAllRuleRows(self):
        for row in range(self.rulesTable.rowCount()):
            self.removeRuleRow(0)

    #endregion === Table Manipulation ===

    #region === Category Filtering ===

    # Updates the field filter, and the field selection combo box.
    def updateFieldFilter(self,index):
        self.currentFieldFilter = self.showOnlyComboBox.currentText()
        if(self.currentFieldFilter == "All"):
            self.updateFieldComboBoxChoices(FIELDS)
        else:
            sortedFields = []
            for field in FIELDS:
                if(field["Category"] == self.currentFieldFilter):
                    sortedFields.append(field)
            self.updateFieldComboBoxChoices(sortedFields)
    def updateFieldComboBoxChoices(self,choices : list):
        for row in range(self.rulesTable.rowCount()):
            thisFieldComboBox = self.rulesTable.cellWidget(row,0)
            thisFieldComboBox.currentTextChanged.disconnect()

            currentEntry = thisFieldComboBox.getCurrentItemData()
            thisFieldComboBox.clear()


            if(currentEntry != ""):
                retainCurrentEntry = True
                setCurrentEntry = True
                for choice in choices:
                    if(choice["Value"] == currentEntry["Value"]):
                        retainCurrentEntry = False
                        break
            else:
                retainCurrentEntry = False
                setCurrentEntry = False


            if(retainCurrentEntry):
                thisFieldComboBox.addItem(icon=currentEntry["Icon"],text=currentEntry)

            for newFieldChoice in choices:
                thisFieldComboBox.addItem(icon=newFieldChoice["Icon"],text=newFieldChoice)

            thisFieldComboBox.currentTextChanged.connect(partial(self.updateFieldRelationships,row=row))

            if(setCurrentEntry):
                thisFieldComboBox.setItemByDictKey(key="Value",value=currentEntry["Value"])
            self.updateFieldRelationships(index=0,row=row)

    #endregion === Category Filtering ===

    #region === Rule Row Updating ===

    # Single method to handle all field relationship updates.
    def updateFieldRelationships(self,index,row):
        currentFieldItem = self.rulesTable.cellWidget(row,0).getCurrentItemData()
        if(currentFieldItem is None):
            currentFieldValue = ""
        else:
            currentFieldValue = currentFieldItem["Value"]
        self.updateOperatorFilter(currentFieldValue=currentFieldValue,row=row)
        self.updateValueFilter(currentFieldValue=currentFieldValue,row=row)
    # Updates an operator combo box with valid operators.
    def updateOperatorFilter(self,currentFieldValue,row):
        validOperators = OPERATOR_MAP.get(currentFieldValue,OPERATOR_MAP["Default"])
        self.updateOperatorComboBoxChoices(row=row,choices=validOperators)
    def updateOperatorComboBoxChoices(self,row,choices : list):
        thisOperatorComboBox = self.rulesTable.cellWidget(row,1)
        currentText = thisOperatorComboBox.currentText()

        thisOperatorComboBox.clear()
        for choice in choices:
            thisOperatorComboBox.addItem(icon=choice,text=choice)

        if(currentText in choices):
            thisOperatorComboBox.setCurrentText(currentText)
    # Updates a value box with a new element, dependent on whether it should be a combo box or not (based on field)
    def updateValueFilter(self,currentFieldValue,row):
        allChoices = VALUE_COMBO_MAP.get(currentFieldValue,None)
        if(allChoices is None):
            self.updateValueCellType(row=row,setAsComboBox=False)
        else:
            self.updateValueCellType(row=row,setAsComboBox=True,choices=allChoices["Values"],isSorted=allChoices["Sorted"])
    def updateValueCellType(self,row,setAsComboBox = False,choices : list = None,isSorted = True):
        # First, test if the current element is a combo box or input value field.
        isExistingCellComboBox = True
        currentCellElement = self.rulesTable.cellWidget(row,2)
        if(not currentCellElement):
            isExistingCellComboBox = False
            currentCellElement = self.rulesTable.item(row,2)

        # Get existing value
        if(isExistingCellComboBox):
            existingCellValue = currentCellElement.currentText()
        else:
            existingCellValue = currentCellElement.text()

        # Now we can actually update the element if it's supposed to be a combo box.
        if(setAsComboBox):
            if(isSorted):
                choices.sort()
            if(isExistingCellComboBox):
                currentCellElement.clear()
                for choice in choices:
                    currentCellElement.addItem(choice,choice)
            else:
                newComboBox = InputComboBox()
                for choice in choices:
                    newComboBox.addItem(choice, choice)
                self.rulesTable.setCellWidget(row,2,newComboBox)
                del currentCellElement
        # Or we simply update it to a value element.
        else:
            if(isExistingCellComboBox):
                self.rulesTable.removeCellWidget(row,2)
                self.rulesTable.setItem(row, 2, QTableWidgetItem(""))
                del currentCellElement
            # We don't need to change ANYTHING in this case, as it's already a simple QTableWidgetItem and
            # already contains the previous value.
            else:
                pass

    #endregion === Rule Row Updating ===