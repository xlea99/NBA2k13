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
        self.rulesTable.setSelectionBehavior(QTableWidget.SelectRows)
        self.rulesTable.setSelectionMode(QTableWidget.NoSelection)
        self.rulesTable.setColumnCount(4)
        self.rulesTable.setHorizontalHeaderLabels(["","Field", "Condition", "Value"])

        # List of all rule rows, in the order they appear in the table.
        self.ruleRows = []

        # Header and "showOnly" combo box.
        self.headerContainer = QWidget()
        self.headerLayout = QHBoxLayout(self.headerContainer)
        self.showOnlyLabel = QLabel("Show Only: ")
        self.showOnlyComboBox = QComboBox()
        self.showOnlyComboBox.currentTextChanged.connect(self.applyFilter)
        #self.showOnlyComboBox.currentIndexChanged.connect(self.updateFieldFilter)
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
        self.ruleButtonsContainer = QWidget()
        self.ruleButtonsLayout = QHBoxLayout(self.ruleButtonsContainer)
        self.newRowButton = QPushButton("Add")
        self.newRowButton.clicked.connect(self.addRuleRow)
        self.deleteSelectedRowsButton = QPushButton("Remove")
        self.deleteSelectedRowsButton.clicked.connect(self.clearSelectedRuleRows)
        self.clearAllButton = QPushButton("Clear")
        self.clearAllButton.clicked.connect(self.clearAllRuleRows)
        self.ruleButtonsLayout.addWidget(self.newRowButton,stretch=2)
        self.ruleButtonsLayout.addWidget(self.deleteSelectedRowsButton,stretch=2)
        self.ruleButtonsLayout.addWidget(self.clearAllButton,stretch=1)

        # Add apply button, as well as separator.
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        separator.setStyleSheet("color: rgba(0, 0, 0, 50);")  # Adjust the color and opacity for faded effect
        self.applyButton = QPushButton("Apply Filters")
        self.applyButton.clicked.connect(self.onApplyClicked)

        self.layout.addWidget(self.headerContainer)
        self.layout.addWidget(self.rulesTable)
        self.layout.addWidget(self.ruleButtonsContainer)
        self.layout.addWidget(separator)
        self.layout.addWidget(self.applyButton)
        self.setLayout(self.layout)

        self.rulesTable.setColumnWidth(self.col_checkbox,self.checkboxColWidth)
        self.rulesTable.setColumnWidth(self.col_field,self.fieldColWidth)
        self.rulesTable.setColumnWidth(self.col_operator,self.operatorColWidth)
        self.rulesTable.setColumnWidth(self.col_value,self.valueColWidth)
        self.rulesTable.verticalHeader().setVisible(False)

        #self.updateRowSelectionButtons()

    #region === Filter Generation ===

    # Applies (returns) the condition dictionary created by the GUI and closes the filter.
    def onApplyClicked(self):
        self.currentFilterDict = self.getCurrentFilterDict()
        self.filterApplied.emit(self.currentFilterDict)
        self.accept()
    # This method converts the full rule table into a single player_filter dictionary.
    def getCurrentFilterDict(self):
        newRuleDict = {"type": "and","conditions": []}
        for ruleRow in self.ruleRows:
            thisFieldDict = ruleRow.getFieldVal()
            thisOperator = ruleRow.getOperatorVal()
            thisValue = ruleRow.getValueVal()

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

        return newRuleDict

    #endregion === Filter Generation ===

    #region === Table Manipulation ===

    # Methods for adding and removing rules visually from the rule table.
    def addRuleRow(self):
        rowPosition = self.rulesTable.rowCount()
        self.rulesTable.insertRow(rowPosition)

        newRuleRow = RuleRow(rowPosition=rowPosition,filterStr=self.currentFieldFilter)
        self.ruleRows.append(newRuleRow)

        self.rulesTable.setCellWidget(newRuleRow.rowPosition, self.col_checkbox, newRuleRow.checkBoxWidget)
        self.rulesTable.setCellWidget(newRuleRow.rowPosition, self.col_field, newRuleRow.fieldWidget)
        self.rulesTable.setCellWidget(newRuleRow.rowPosition, self.col_operator, newRuleRow.operatorWidget)
        self.rulesTable.setCellWidget(newRuleRow.rowPosition, self.col_value, newRuleRow.valueWidget)

        newRuleRow.checkboxStateChanged.connect(self.onCheckboxStateChanged)
        self.updateRowSelectionButtons()
    def removeRuleRow(self, rowPosition):
        self.rulesTable.removeRow(rowPosition)
        for ruleRowToUpdate in self.ruleRows[rowPosition:]:
            ruleRowToUpdate.rowPosition -= 1
        del self.ruleRows[rowPosition]
    def clearAllRuleRows(self):
        for row in range(self.rulesTable.rowCount()):
            self.removeRuleRow(0)
        self.updateRowSelectionButtons()
    def clearSelectedRuleRows(self):
        selectedRows = self.rulesTable.selectionModel().selectedRows()

        rowsToRemove = []
        for selectedRow in selectedRows:
            rowsToRemove.append(selectedRow.row())

        rowsToRemove.sort(reverse=True)
        for rowToRemove in rowsToRemove:
            self.removeRuleRow(rowPosition=rowToRemove)
        self.updateRowSelectionButtons()

    #endregion === Table Manipulation ===

    #region === Rule Row Updating ===

    # Applies the "show only" filter to all rule rows.
    def applyFilter(self,filterText):
        for ruleRow in self.ruleRows:
            ruleRow.setFieldFilter(filterText)

    # Method to handle row selection using the checkbox.
    def onCheckboxStateChanged(self, rowPosition,isChecked):
        selectionModel = self.rulesTable.selectionModel()
        if (isChecked):
            selectionModel.select(self.rulesTable.model().index(rowPosition, 0),QItemSelectionModel.Select | QItemSelectionModel.Rows)
        else:
            selectionModel.select(self.rulesTable.model().index(rowPosition, 0),QItemSelectionModel.Deselect | QItemSelectionModel.Rows)
        self.updateRowSelectionButtons()
    # Method to update all buttons that rely on row selection.
    def updateRowSelectionButtons(self):
        allSelectedRowIndices = []
        for selectedRow in self.rulesTable.selectionModel().selectedRows():
            allSelectedRowIndices.append(selectedRow.row())

        if(len(allSelectedRowIndices) == 0):
            self.deleteSelectedRowsButton.setText("Remove (0)")
            self.deleteSelectedRowsButton.setDisabled(True)
        else:
            self.deleteSelectedRowsButton.setText(f"Remove ({len(allSelectedRowIndices)})")
            self.deleteSelectedRowsButton.setDisabled(False)

    #endregion === Rule Row Updating ===


class RuleRow(QObject):

    checkboxStateChanged = Signal(int,bool)
    internalComboBoxStyle = """
            QComboBox {
                padding: 2px;  /* Reduce padding */
                margin: 1px;  /* Reduce margin */
                border: 1px solid gray;  /* Add a subtle border */
            }
        """

    # Setup for rule row
    def __init__(self,rowPosition,filterStr = "Any"):
        super().__init__()

        self.rowPosition = rowPosition
        self.__fieldFilter = filterStr

        # Checkbox setup
        self.checkBoxWidget = QWidget()
        self.__checkBox = QCheckBox()
        self.__checkBox.stateChanged.connect(self.__checkboxStateChanged)
        self.__checkBoxLayout = QHBoxLayout(self.checkBoxWidget)
        self.__checkBoxLayout.setAlignment(Qt.AlignCenter)
        self.__checkBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.__checkBoxLayout.addWidget(self.__checkBox)
        self.__isCheckBoxChecked = False

        # Field element setup
        self.fieldWidget = QWidget()
        self.__fieldLayout = QHBoxLayout(self.fieldWidget)
        self.__fieldLayout.setContentsMargins(0,0,0,0)
        self.__fieldComboBox = InputComboBox()
        self.__fieldComboBox.setStyleSheet(self.internalComboBoxStyle)
        self.__fieldComboBox.currentTextChanged.connect(self.__updateFieldRelationships)
        self.__fieldLayout.addWidget(self.__fieldComboBox)
        defaultField = FIELDS[0]
        if(self.__fieldFilter != "Any"):
            for field in FIELDS:
                if(field["Category"] == self.__fieldFilter):
                    defaultField = field
                    break
        self.__fieldComboBox.addItem("", defaultField)
        # Operator element setup
        self.operatorWidget = QWidget()
        self.__operatorLayout = QHBoxLayout(self.operatorWidget)
        self.__operatorLayout.setContentsMargins(0,0,0,0)
        self.__operatorComboBox = InputComboBox()
        self.__operatorComboBox.setStyleSheet(self.internalComboBoxStyle)
        self.__operatorLayout.addWidget(self.__operatorComboBox)
        # Value element setup
        self.valueWidget = QWidget()
        self.__valueLayout = QHBoxLayout(self.valueWidget)
        self.__valueLayout.setContentsMargins(0,0,0,0)
        self.__valueComboBox = InputComboBox()
        self.__valueComboBox.setStyleSheet(self.internalComboBoxStyle)
        self.__valueSimpleItem = QLineEdit()
        self.__valueLayout.addWidget(self.__valueComboBox)
        self.__valueLayout.addWidget(self.__valueSimpleItem)
        self.__isSimpleValue = True

        # Run setup updates
        self.__checkBox.isChecked()
        self.setFieldFilter(self.__fieldFilter)

    # Simply returns the values of each column of the rule row.
    def getCheckboxState(self):
        return self.__isCheckBoxChecked
    def getFieldVal(self):
        return self.__fieldComboBox.getCurrentItemData()
    def getOperatorVal(self):
        return self.__operatorComboBox.currentText()
    def getValueVal(self):
        if(self.__isSimpleValue):
            return self.__valueSimpleItem.text()
        else:
            return self.__valueComboBox.currentText()

    # Updates checkbox information.
    def __checkboxStateChanged(self,state):
        self.__isCheckBoxChecked = Qt.CheckState(state) == Qt.CheckState.Checked
        self.checkboxStateChanged.emit(self.rowPosition,self.__isCheckBoxChecked)

    # Updates the field filter, and the field selection combo box.
    def setFieldFilter(self,filterStr):
        self.__fieldFilter = filterStr
        if(self.__fieldFilter == "All"):
            self.__updateFieldComboBoxChoices(FIELDS)
        else:
            sortedFields = []
            for field in FIELDS:
                if(field["Category"] == self.__fieldFilter):
                    sortedFields.append(field)
            self.__updateFieldComboBoxChoices(sortedFields)
    def __updateFieldComboBoxChoices(self,choices : list):
        self.__fieldComboBox.currentTextChanged.disconnect()

        currentEntry = self.__fieldComboBox.getCurrentItemData()
        self.__fieldComboBox.clear()

        if(currentEntry != ""):
            retainCurrentEntry = True
            setCurrentEntry = True
            for choice in choices:
                if(choice.get("Value",None) == currentEntry["Value"]):
                    retainCurrentEntry = False
                    break
        else:
            retainCurrentEntry = False
            setCurrentEntry = False

        if(retainCurrentEntry):
            self.__fieldComboBox.addItem(icon=currentEntry["Icon"],text=currentEntry)

        for newFieldChoice in choices:
            self.__fieldComboBox.addItem(icon=newFieldChoice["Icon"],text=newFieldChoice)

        self.__fieldComboBox.currentTextChanged.connect(self.__updateFieldRelationships)

        if(setCurrentEntry):
            self.__fieldComboBox.setItemByDictKey(key="Value",value=currentEntry["Value"])
        self.__updateFieldRelationships(index=0)

    # Single method to handle all field relationship updates.
    def __updateFieldRelationships(self,index):
        currentFieldItem = self.__fieldComboBox.getCurrentItemData()
        if(currentFieldItem is None):
            currentFieldValue = ""
            currentFieldOperatorFilter = "Default"
        else:
            currentFieldValue = currentFieldItem["Value"]
            currentFieldOperatorFilter = currentFieldItem.get("Operators",None)
        self.__updateOperatorFilter(operatorFilter=currentFieldOperatorFilter)
        self.__updateValueFilter(currentFieldValue=currentFieldValue)
    # Updates an operator combo box with valid operators.
    def __updateOperatorFilter(self,operatorFilter):
        validOperators = OPERATOR_MAP.get(operatorFilter,OPERATOR_MAP["Default"])
        self.__updateOperatorComboBoxChoices(choices=validOperators)
    def __updateOperatorComboBoxChoices(self,choices : list):
        currentText = self.__operatorComboBox.currentText()

        self.__operatorComboBox.clear()
        for choice in choices:
            self.__operatorComboBox.addItem(icon=choice,text=choice)

        if(currentText in choices):
            self.__operatorComboBox.setCurrentText(currentText)
    # Updates a value box with a new element, dependent on whether it should be a combo box or not (based on field)
    def __updateValueFilter(self,currentFieldValue):
        allChoices = VALUE_COMBO_MAP.get(currentFieldValue,None)
        if(allChoices is None):
            self.__updateValueWidgetType(setAsComboBox=False)
        else:
            self.__updateValueWidgetType(setAsComboBox=True,choices=allChoices["Values"],isSorted=allChoices["Sorted"])
    def __updateValueWidgetType(self,setAsComboBox = False,choices : list = None,isSorted = True):
        if(setAsComboBox):
            if(isSorted):
                choices.sort()
            if(self.__isSimpleValue):
                self.__valueComboBox.clear()
                for choice in choices:
                    self.__valueComboBox.addItem(choice, choice)
                self.__valueSimpleItem.hide()
                self.__valueComboBox.show()
            else:
                existingValue = self.__valueComboBox.currentText()
                self.__valueComboBox.clear()
                for choice in choices:
                    self.__valueComboBox.addItem(choice,choice)
                if(existingValue in choices):
                    self.__valueComboBox.setCurrentText(existingValue)
            self.__isSimpleValue = False
        # Or we simply update it to a value element.
        else:
            # We don't need to change ANYTHING in this case, as it's already a simple QTableWidgetItem and
            # already contains the previous value.
            if(self.__isSimpleValue):
                pass
            else:
                self.__valueComboBox.hide()
                self.__valueSimpleItem.show()
            self.__isSimpleValue = True
