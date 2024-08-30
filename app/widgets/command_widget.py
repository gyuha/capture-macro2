from functools import partial
from typing import List

from PySide6.QtCore import Qt
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
        self.macro_type = ""
        self.main = None
        self.macro: List[Macro] = []
        self.ui.macroTable.setColumnWidth(0, 80)
        self.ui.macroTable.setColumnWidth(1, 110)
        self.ui.macroTable.setColumnWidth(2, 60)
        self.ui.macroTable.setColumnWidth(3, 60)

    def set_macro(self, main, macro_type: str = "macro", macro: List[Macro] = None):
        self.macro = macro
        self.main = main
        self.macro_type = macro_type
        self.ui.macroTable.setRowCount(len(macro))
        self.ui.macroTable.setAlternatingRowColors(True)
        for row, macro in enumerate(self.macro):
            self.setMacroTableRow(row, macro.action, macro.value)
        self.updateMacroActions()

        self.ui.macroTable.itemChanged.connect(self.updateMacroActions)

    def connect_signals_slots(self):
        # Config buttons
        self.ui.btnConfigInsert.clicked.connect(self.on_config_insert)
        self.ui.btnConfigAdd.clicked.connect(self.on_config_add)
        self.ui.btnConfigRemove.clicked.connect(self.on_config_remove)

    def add_row(self, row, action="capture", value=""):
        self.ui.macroTable.insertRow(row)
        self.setMacroTableRow(row, action, value)

    def on_config_insert(self):
        self.add_row(self.ui.macroTable.currentRow())

    def on_config_add(self):
        self.add_row(self.ui.macroTable.currentRow() + 1)

    def on_config_remove(self):
        row = self.ui.macroTable.currentRow()
        self.ui.macroTable.removeRow(row)

    def setMacroTableRow(self, row, action, value):
        actionCombo = QComboBox()
        actionCombo.addItems(macroActions)
        actionCombo.currentTextChanged.connect(self.updateMacroActions)
        index = actionCombo.findText(action)
        if index > -1:
            actionCombo.setCurrentIndex(index)
        self.ui.macroTable.setCellWidget(row, 0, actionCombo)

        item = QTableWidgetItem(value)
        # item.currentTextChanged.connect(self.updateMacroActions)
        self.ui.macroTable.setItem(row, 1, item)

    def updateMacroActions(self):
        self.ui.macroTable.blockSignals(True)
        macro: List[Macro] = []
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
                    placeholder_item = QTableWidgetItem()
                    placeholder_item.setFlags(Qt.ItemIsEnabled)
                    self.ui.macroTable.setItem(row, 3, placeholder_item)
                else:
                    placeholder_item = QTableWidgetItem()
                    placeholder_item.setFlags(Qt.ItemIsEnabled)
                    self.ui.macroTable.setItem(row, 2, placeholder_item)

                    placeholder_item2 = QTableWidgetItem()
                    placeholder_item2.setFlags(Qt.ItemIsEnabled)
                    self.ui.macroTable.setItem(row, 3, placeholder_item2)
                macro.append(
                    Macro(action=action, value=self.ui.macroTable.item(row, 1).text())
                )
            if self.macro_type == "pre_macro":
                self.main.config.pre_macro = macro
            else:
                self.main.config.macro = macro

        except Exception as e:
            print(e)
        finally:
            self.ui.macroTable.blockSignals(False)

    def clickScreenRect(self, row):
        pass

    def clickScreenRectCheck(self, row):
        pass

    def clickPointClick(self, row):
        pass
