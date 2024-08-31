from functools import partial
from typing import List

from PySide6.QtCore import Qt, Signal, Slot
from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QPushButton,
    QTableWidgetItem,
    QWidget,
)

from app.config.config import Macro
from app.utils.rect.rect_check_overlay import RectCheckOverlay
from app.utils.rect.rect_overlay import RectOverlay
from app.utils.rect_value_utils import is_valid_rect_string_value, string_to_rect_value
from ui.command_widget_ui import Ui_CommandWidget

MACRO_ACTIONS = ["capture", "delay", "click", "key", "scroll"]
# TODO : 키 목록을 콤보박스에서 가져오도록 수가
KEY_ACTIONS = [
    "up",
    "down",
    "left",
    "right",
    "enter",
    "tab",
    "space",
    "backspace",
    "delete",
    "f1",
    "f2",
    "f3",
    "f4",
    "f5",
    "f6",
    "f7",
    "f8",
    "f9",
    "f10",
    "f11",
    "f12",
    "ctrl",
    "alt",
    "shift",
    "win",
    "pageup",
    "pagedown",
    "home",
    "end",
]


class CommandWidget(QWidget):
    signal_update_config = Signal(str, object)

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

        self.overlay = None

        # 액션을 실행 한 행
        self.action_row = -1

    def set_macro(self, main, macro_type: str = "macro", macro: List[Macro] = None):
        self.macro = macro
        self.main = main
        self.macro_type = macro_type
        self.ui.macroTable.setRowCount(len(macro))
        self.ui.macroTable.setAlternatingRowColors(True)
        for row, macro in enumerate(self.macro):
            self.set_macro_table_row(row, macro.action, macro.value)
        self.update_macro_actions()

        self.ui.macroTable.itemChanged.connect(self.update_macro_actions)

    def connect_signals_slots(self):
        # Macro buttons
        self.ui.btnCommandInsert.clicked.connect(self.on_macro_insert)
        self.ui.btnCommandAdd.clicked.connect(self.on_macro_add)
        self.ui.btnCommandRemove.clicked.connect(self.on_macro_remove)

    def add_row(self, row, action="capture", value=""):
        self.ui.macroTable.insertRow(row)
        self.set_macro_table_row(row, action, value)
        self.update_macro_actions()

    def on_macro_insert(self):
        self.add_row(self.ui.macroTable.currentRow())

    def on_macro_add(self):
        self.add_row(self.ui.macroTable.currentRow() + 1)

    def on_macro_remove(self):
        row = self.ui.macroTable.currentRow()
        self.ui.macroTable.removeRow(row)
        self.update_macro_actions()

    def set_macro_table_row(self, row, action, value):
        actionCombo = QComboBox()
        actionCombo.addItems(MACRO_ACTIONS)
        actionCombo.currentTextChanged.connect(self.update_macro_actions)
        index = actionCombo.findText(action)
        if index > -1:
            actionCombo.setCurrentIndex(index)
        self.ui.macroTable.setCellWidget(row, 0, actionCombo)

        item = QTableWidgetItem(value)
        # item.currentTextChanged.connect(self.updateMacroActions)
        self.ui.macroTable.setItem(row, 1, item)

    def update_macro_actions(self):
        self.ui.macroTable.blockSignals(True)
        macro: List[Macro] = []
        try:
            for row in range(self.ui.macroTable.rowCount()):
                action = self.ui.macroTable.cellWidget(row, 0).currentText()
                self.ui.macroTable.removeCellWidget(row, 2)
                self.ui.macroTable.removeCellWidget(row, 3)
                if action == "capture" or action == "click" or action == "scroll":
                    button = QPushButton()
                    button.setText("영역선택")
                    button.clicked.connect(partial(self.handle_screen_rect, row))
                    button2 = QPushButton()
                    button2.setText("확인")
                    button2.pressed.connect(partial(self.handle_rect_check_show, row))
                    button2.released.connect(self.handle_rect_check_hide)
                    self.ui.macroTable.setCellWidget(row, 2, button)
                    self.ui.macroTable.setCellWidget(row, 3, button2)
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

        except (AttributeError, KeyError, TypeError) as e:
            print(f"An error occurred: {e}")
        finally:
            self.signal_update_config.emit(self.macro_type, macro)
            self.ui.macroTable.blockSignals(False)

    def handle_screen_rect(self, row):
        # 스크린 영역 선택
        self.action_row = row
        screens = QApplication.screens()
        monitor_idx = int(self.main.config.monitor)
        if monitor_idx < len(screens):
            screen = screens[monitor_idx]
            self.overlay = RectOverlay(screen)
            self.overlay.rect_selected.connect(self.handle_rect_selected)
            self.overlay.show()

    @Slot(int, int, int, int)
    def handle_rect_selected(self, x, y, width, height):
        self.ui.macroTable.item(self.action_row, 1).setText(f"{x},{y},{width},{height}")
        self.update_macro_actions()
        self.overlay.close()

    def handle_rect_check_show(self, row):
        self.action_row = row
        screens = QApplication.screens()
        monitor_idx = int(self.main.config.monitor)
        if monitor_idx < len(screens):
            screen = screens[monitor_idx]
            self.overlay = RectCheckOverlay(screen)
            self.overlay.show()
            value = self.ui.macroTable.item(row, 1).text()
            if is_valid_rect_string_value(value):
                x, y, width, height = string_to_rect_value(value)
                self.overlay.display_rectangle(x, y, width, height)

    def handle_rect_check_hide(self):
        if hasattr(self, "overlay") and self.overlay.isVisible():
            self.overlay.close()

    def clickPointClick(self, row):
        pass
