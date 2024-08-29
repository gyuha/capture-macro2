from functools import partial
from typing import List

from PySide6.QtWidgets import QComboBox, QPushButton, QTableWidgetItem, QWidget

from app.config.config import Macro
from ui.command_widget_ui import Ui_CommandWidget

macroActions = ["capture", "delay", "click", "key", "scroll"]


class CommandWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_CommandWidget()
        self.ui.setupUi(self)
        self.connect_signals_slots()
        self.macro: List[Macro] = []

    def set_macro(self, macro: List[Macro]):
        self.macro = macro
        print("📢[command_widget.py:21]: ", macro)
        self.ui.macroTable.setRowCount(len(macro))
        for row, macro in enumerate(self.macro):
            self.setMacroTableRow(row, macro.action, macro.value)

    def connect_signals_slots(self):
        # Config buttons
        self.ui.btnConfigInsert.clicked.connect(self.on_config_insert)
        self.ui.btnConfigAdd.clicked.connect(self.on_config_add)
        self.ui.btnConfigRemove.clicked.connect(self.on_config_remove)

    def on_config_insert(self):
        print("Config insert")
        self.insert_macro("delay", "1000")  # Example action and value

    def on_config_add(self):
        print("Config add")
        self.add_macro("click", "x=100,y=200")  # Example action and value

    def on_config_remove(self):
        print("Config remove")
        self.remove_macro()  # Remove the last macro for demonstration

    def insert_macro(self, action, value):
        new_row = 0
        self.ui.macroTable.insertRow(new_row)  # Insert row at the top
        self.setMacroTableRow(new_row, action, value)
        self.macro.insert(new_row, Macro(action=action, value=value))
        self.updateMacroActions()

    def add_macro(self, action, value):
        new_row = self.ui.macroTable.rowCount()
        self.ui.macroTable.insertRow(new_row)  # Append row at the end
        self.setMacroTableRow(new_row, action, value)
        self.macro.append(Macro(action=action, value=value))
        self.updateMacroActions()

    def remove_macro(self):
        last_row = self.ui.macroTable.rowCount() - 1
        if last_row >= 0:
            self.ui.macroTable.removeRow(last_row)
            self.macro.pop()

    def setMacroTableRow(self, row, action, value):
        actionCombo = QComboBox()
        actionCombo.addItems(macroActions)
        index = actionCombo.findText(action)
        if index > -1:
            actionCombo.setCurrentIndex(index)
        # actionCombo.currentTextChanged.connect(self.updateMacroActions)

        self.ui.macroTable.setCellWidget(row, 0, actionCombo)

        item = QTableWidgetItem(value)
        self.ui.macroTable.setItem(row, 1, item)

    def updateMacroActions(self):
        try:
            for row in range(self.ui.macroTable.rowCount()):
                action = self.ui.macroTable.cellWidget(row, 0).currentText()
                self.ui.macroTable.removeCellWidget(row, 2)
                self.ui.macroTable.removeCellWidget(row, 3)
                if action == "capture":
                    button = QPushButton()
                    button.setText("영역선택")
                    button.clicked.connect(partial(self.clickScreenRect, row))
                    button2 = QPushButton()
                    button2.setText("확인")
                    button2.clicked.connect(partial(self.clickScreenRectCheck, row))
                    self.ui.macroTable.setCellWidget(row, 2, button)
                    self.ui.macroTable.setCellWidget(row, 3, button2)
                elif action == "click" or action == "scroll":
                    button = QPushButton()
                    button.setText("포인트")
                    button.clicked.connect(partial(self.clickPointClick, row))
                    self.ui.macroTable.setCellWidget(row, 2, button)
                else:
                    item = QTableWidgetItem()
                    # item.setFlags(item.flags() ^ Qt.ItemIsEditable)
                    self.ui.macroTable.setItem(row, 2, item)
                    self.ui.macroTable.setItem(row, 3, item)
        except Exception:
            pass
