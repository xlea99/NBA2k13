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
from spritopia.utilities.misc import isNumber


#region === Field Map Construction ===

FIELDS = []
# Load initial "top" vals manually
FIELDS.append({"Icon": "Roster",
               "Category": "Special",
               "Domain": None,
               "Subdomain": None,
               "Value": "IsOnRoster",
               "Operators": "EqualityOnly"})
for basicVal in Player.valCategories["Basic Info"]:
    thisDict = {"Icon": LOCALIZATION_PLAYERS[basicVal],
                   "Category": "Basic Info",
                   "Domain": "Players",
                   "Subdomain": None,
                   "Value": basicVal}
    if(basicVal in ["Hand","Height","Weight","NmOrder"]):
        thisDict["Operators"] = "Default"
    else:
        thisDict["Operators"] = "TextOnly"
    FIELDS.append(thisDict)
for attributeVal in Player.valCategories["Attributes"]:
    FIELDS.append({"Icon": LOCALIZATION_PLAYERS[attributeVal],
                   "Category": "Attributes",
                   "Domain": "Players",
                   "Subdomain": None,
                   "Value": attributeVal,
                   "Operators": "NumericOnly"})

# Load all stat vals
for otherStatVal in LOCALIZATION_STATS["Other"].keys():
    FIELDS.append({"Icon": LOCALIZATION_STATS["Other"][otherStatVal],
                   "Category": "Stats",
                   "Domain": "Stats",
                   "Subdomain": "Other",
                   "Value": otherStatVal,
                   "Operators": "NumericOnly"})
for totalStatVal in LOCALIZATION_STATS["Totals"].keys():
    FIELDS.append({"Icon": LOCALIZATION_STATS["Totals"][totalStatVal],
                   "Category": "Stats",
                   "Domain": "Stats",
                   "Subdomain": "Totals",
                   "Value": totalStatVal,
                   "Operators": "NumericOnly"})
for averageStatVal in LOCALIZATION_STATS["Averages"].keys():
    FIELDS.append({"Icon": LOCALIZATION_STATS["Averages"][averageStatVal],
                   "Category": "Stats",
                   "Domain": "Stats",
                   "Subdomain": "Averages",
                   "Value": averageStatVal,
                   "Operators": "NumericOnly"})

# Load rest of the player vals
for tendencyVal in Player.valCategories["Tendencies"]:
    FIELDS.append({"Icon": LOCALIZATION_PLAYERS[tendencyVal],
                   "Category": "Tendencies",
                   "Domain": "Players",
                   "Subdomain": None,
                   "Value": tendencyVal,
                   "Operators": "NumericOnly"})
for hotspotVal in Player.valCategories["Hotspots"]:
    FIELDS.append({"Icon": LOCALIZATION_PLAYERS[hotspotVal],
                   "Category": "Hotspots",
                   "Domain": "Players",
                   "Subdomain": None,
                   "Value": hotspotVal,
                   "Operators": "NumericOnly"})
for hotzoneVal in Player.valCategories["Hotzones"]:
    FIELDS.append({"Icon": LOCALIZATION_PLAYERS[hotzoneVal],
                   "Category": "Hotzones",
                   "Domain": "Players",
                   "Subdomain": None,
                   "Value": hotzoneVal,
                   "Operators": "NumericOnly"})
for appearanceVal in Player.valCategories["Appearance"]:
    FIELDS.append({"Icon": LOCALIZATION_PLAYERS[appearanceVal],
                   "Category": "Appearance",
                   "Domain": "Players",
                   "Subdomain": None,
                   "Value": appearanceVal,
                   "Operators": "NumericOnly"})
for animationVal in Player.valCategories["Animations"]:
    FIELDS.append({"Icon": LOCALIZATION_PLAYERS[animationVal],
                   "Category": "Animations",
                   "Domain": "Players",
                   "Subdomain": None,
                   "Value": animationVal,
                   "Operators": "NumericOnly"})
for extraVal in Player.extraValuesMap.keys():
    FIELDS.append({"Icon": LOCALIZATION_PLAYERS[extraVal],
                   "Category": "Animations",
                   "Domain": "Players",
                   "Subdomain": None,
                   "Value": extraVal,
                   "Operators": "Default"})

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
    "NumericOnly" : ["==","!=",">",">=","<","<="],
    "TextOnly": ["==","!=","contains","does not contain"],
    "EqualityOnly": ["==","!="]
}
OPERATOR_LOCALIZED = {
    "==": "equals",
    "!=": "does_not_equal",
    ">": "greater_than",
    ">=": "greater_than_or_equal_to",
    "<": "less_than",
    "<=": "less_than_or_equal_to",
    "contains": "contains",
    "does not contain": "does not contain",
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

    checkboxColWidth = 30
    fieldColWidth = 120
    operatorColWidth = 60
    valueColWidth = 120
    col_checkbox = 0
    col_field = 1
    col_operator = 2
    col_value = 3

    internalComboBoxStyle = """
        QComboBox {
            padding: 2px;  /* Reduce padding */
            margin: 1px;  /* Reduce margin */
            border: 1px solid gray;  /* Add a subtle border */
        }
    """

    removeRuleButtonWidth = 40


    def __init__(self, parent=None):
        super().__init__(parent)

        self.currentFilterDict = {}
        self.currentFieldFilter = "All"

        self.setWindowTitle("Filter Preferences")
        self.setMinimumWidth(self.checkboxColWidth + self.fieldColWidth + self.operatorColWidth + self.valueColWidth + 24)

        # Use QVBoxLayout for simple vertical layout
        self.layout = QVBoxLayout()

        # Setup actual rules table.
        self.rulesTable = QTableWidget()
        self.rulesTable.setStyleSheet("""
            QHeaderView::section:selected {
                background-color: #b0c4de;  /* Light Steel Blue */
            }
        """)
        self.rulesTable.setSelectionBehavior(QTableWidget.SelectRows)  # or QTableWidget.SelectColumns
        self.rulesTable.setSelectionMode(QTableWidget.MultiSelection)  # or QTableWidget.MultiSelection
        #self.rulesTable.setMaximumWidth(313) #TODO adjust
        self.rulesTable.setColumnCount(4)
        self.rulesTable.setHorizontalHeaderLabels(["","Field", "Condition", "Value"])

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
        self.newRowButton = QPushButton("Add")
        self.newRowButton.clicked.connect(self.addRuleRow)
        self.deleteSelectedRowsButton = QPushButton("Remove")
        self.deleteSelectedRowsButton.clicked.connect(self.clearSelectedRuleRows)
        self.clearAllButton = QPushButton("Clear")
        self.clearAllButton.clicked.connect(self.clearAllRuleRows)
        self.ruleOperatorLayout.addWidget(self.newRowButton,stretch=2)
        self.ruleOperatorLayout.addWidget(self.deleteSelectedRowsButton,stretch=2)
        self.ruleOperatorLayout.addWidget(self.clearAllButton,stretch=1)

        # Add apply button, as well as separator.
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        separator.setStyleSheet("color: rgba(0, 0, 0, 50);")  # Adjust the color and opacity for faded effect
        self.applyButton = QPushButton("Apply Filters")
        self.applyButton.clicked.connect(self.onApplyClicked)

        self.layout.addWidget(self.headerContainer)
        self.layout.addWidget(self.rulesTable)
        self.layout.addWidget(self.ruleOperatorContainer)
        self.layout.addWidget(separator)
        self.layout.addWidget(self.applyButton)
        self.setLayout(self.layout)

        self.rulesTable.setColumnWidth(self.col_checkbox,self.checkboxColWidth)
        self.rulesTable.setColumnWidth(self.col_field,self.fieldColWidth)
        self.rulesTable.setColumnWidth(self.col_operator,self.operatorColWidth)
        self.rulesTable.setColumnWidth(self.col_value,self.valueColWidth)
        self.rulesTable.verticalHeader().setVisible(False)

    #region === Filter Generation ===

    # Applies (returns) the condition dictionary created by the GUI and closes the filter.
    def onApplyClicked(self):
        self.currentFilterDict = self.getCurrentFilterDict()
        self.filterApplied.emit(self.currentFilterDict)
        self.accept()
    # This method converts the full rule table into a single player_filter dictionary.
    def getCurrentFilterDict(self):
        newRuleDict = {"type": "and","conditions": []}
        for row in range(self.rulesTable.rowCount()):
            thisFieldDict = self.rulesTable.cellWidget(row,self.col_field).getCurrentItemData()
            thisOperator = self.rulesTable.cellWidget(row,self.col_operator).currentText()

            thisValueElement = self.rulesTable.cellWidget(row,self.col_value)
            if(thisValueElement):
                thisValue = thisValueElement.currentText()
            else:
                thisValue = self.rulesTable.item(row,self.col_value).text()

            thisCondition = {
                    "type": OPERATOR_LOCALIZED[thisOperator],
                    "domain": thisFieldDict["Domain"],
                    "subdomain": thisFieldDict["Subdomain"],
                    "field": thisFieldDict["Value"]
                }

            # Converting the value to its actual type, if needed.
            if(isNumber(thisValue)):
                if("." in thisValue):
                    thisCondition["value"] = float(thisValue)
                else:
                    thisCondition["value"] = int(thisValue)
            else:
                thisCondition["value"] = thisValue

            # Dealing with special logic cases
            if(thisFieldDict["Value"] == "IsOnRoster"):
                thisCondition["type"] = "special"
                if(thisOperator == "!="):
                    newRuleDict["conditions"].append({"type": "not", "condition": thisCondition})
                else:
                    newRuleDict["conditions"].append(thisCondition)
            elif(thisOperator == "does not contain"):
                thisCondition["type"] = "contains"
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

        # Create a checkbox widget
        checkBoxWidget = QWidget()
        checkBox = QCheckBox()
        checkBoxLayout = QHBoxLayout(checkBoxWidget)
        checkBoxLayout.addWidget(checkBox)
        checkBoxLayout.setAlignment(Qt.AlignCenter)
        checkBoxLayout.setContentsMargins(0, 0, 0, 0)
        checkBoxWidget.setLayout(checkBoxLayout)


        # Create InputComboBox instances for each cell that needs it
        fieldComboBox = InputComboBox()
        fieldComboBox.setStyleSheet(self.internalComboBoxStyle)
        operatorComboBox = InputComboBox()
        operatorComboBox.setStyleSheet(self.internalComboBoxStyle)
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
        operatorComboBox.addItem("", "")
        valueComboBox.addItem("", "")



        # Connect each fieldComboBox to get valid operators.
        fieldComboBox.currentTextChanged.connect(partial(self.updateFieldRelationships,row=rowPosition))

        # Set combo boxes as cell widgets
        self.rulesTable.setCellWidget(rowPosition,self.col_checkbox,checkBoxWidget)
        self.rulesTable.setCellWidget(rowPosition, self.col_field, fieldComboBox)
        self.rulesTable.setCellWidget(rowPosition, self.col_operator, operatorComboBox)
        self.rulesTable.setItem(rowPosition, self.col_value, QTableWidgetItem(""))

        self.updateFieldFilter(0)
        checkBox.stateChanged.connect(lambda state, row=rowPosition: self.onCheckboxStateChanged(state, row))

        print(f"Checkbox: {self.rulesTable.columnWidth(0)}")
        print(f"Field: {self.rulesTable.columnWidth(1)}")
        print(f"Operator: {self.rulesTable.columnWidth(2)}")
        print(f"Value: {self.rulesTable.columnWidth(3)}")
    def removeRuleRow(self, rowPosition):
        # Check if the position is valid before attempting to remove
        if 0 <= rowPosition < self.rulesTable.rowCount():
            self.rulesTable.removeRow(rowPosition)
        else:
            print("Invalid row position: ", rowPosition)
    def clearAllRuleRows(self):
        for row in range(self.rulesTable.rowCount()):
            self.removeRuleRow(0)
    def clearSelectedRuleRows(self):
        selectedRows = self.rulesTable.selectionModel().selectedRows()

        rowsToRemove = []
        for selectedRow in selectedRows:
            rowsToRemove.append(selectedRow.row())

        rowsToRemove.sort(reverse=True)
        for rowToRemove in rowsToRemove:
            self.removeRuleRow(rowPosition=rowToRemove)

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
            thisFieldComboBox = self.rulesTable.cellWidget(row,self.col_field)
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

    # Method to handle row selection using the checkbox.
    def onCheckboxStateChanged(self, state, row):
        selectionModel = self.rulesTable.selectionModel()
        checkbox_state = Qt.CheckState(state)  # Convert integer to Qt.CheckState enum

        print(f"Converted State: {checkbox_state}, Expected: {Qt.CheckState.Checked}")

        if checkbox_state == Qt.CheckState.Checked:
            print("Selection: CHECKED")
            selectionModel.select(self.rulesTable.model().index(row, 0),
                                  QItemSelectionModel.Select | QItemSelectionModel.Rows)
        else:
            print("Selection: UNCHECKED")
            selectionModel.select(self.rulesTable.model().index(row, 0),
                                  QItemSelectionModel.Deselect | QItemSelectionModel.Rows)
    # Single method to handle all field relationship updates.
    def updateFieldRelationships(self,index,row):
        currentFieldItem = self.rulesTable.cellWidget(row,self.col_field).getCurrentItemData()
        if(currentFieldItem is None):
            currentFieldValue = ""
            currentFieldOperatorFilter = "Default"
        else:
            currentFieldValue = currentFieldItem["Value"]
            currentFieldOperatorFilter = currentFieldItem.get("Operators",None)
        self.updateOperatorFilter(currentFieldValue=currentFieldValue,row=row,operatorFilter=currentFieldOperatorFilter)
        self.updateValueFilter(currentFieldValue=currentFieldValue,row=row)
    # Updates an operator combo box with valid operators.
    def updateOperatorFilter(self,currentFieldValue,row,operatorFilter):
        validOperators = OPERATOR_MAP.get(operatorFilter,OPERATOR_MAP["Default"])
        self.updateOperatorComboBoxChoices(row=row,choices=validOperators)
    def updateOperatorComboBoxChoices(self,row,choices : list):
        thisOperatorComboBox = self.rulesTable.cellWidget(row,self.col_operator)
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
        currentCellElement = self.rulesTable.cellWidget(row,self.col_value)
        if(not currentCellElement):
            isExistingCellComboBox = False
            currentCellElement = self.rulesTable.item(row,self.col_value)

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
                if(existingCellValue in choices):
                    currentCellElement.setCurrentText(existingCellValue)
            else:
                newComboBox = InputComboBox()
                newComboBox.setStyleSheet(self.internalComboBoxStyle)
                for choice in choices:
                    newComboBox.addItem(choice, choice)
                self.rulesTable.setCellWidget(row,self.col_value,newComboBox)
                del currentCellElement
        # Or we simply update it to a value element.
        else:
            if(isExistingCellComboBox):
                self.rulesTable.removeCellWidget(row,self.col_value)
                self.rulesTable.setItem(row, self.col_value, QTableWidgetItem(""))
                del currentCellElement
            # We don't need to change ANYTHING in this case, as it's already a simple QTableWidgetItem and
            # already contains the previous value.
            else:
                pass

    #endregion === Rule Row Updating ===