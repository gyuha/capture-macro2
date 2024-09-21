from enum import Enum
from functools import partial
from typing import List

from PySide6.QtCore import Qt, Slot
from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QPushButton,
    QSpinBox,
    QTableWidgetItem,
    QWidget,
)

from app.config.config import Config, Macro
from app.utils.rect.rect_check_overlay import RectCheckOverlay
from app.utils.rect.rect_overlay import RectOverlay
from app.utils.rect_value_utils import is_valid_rect_string_value, string_to_rect_value
from ui.command_widget_ui import Ui_CommandWidget


class MacroActions(Enum):
    CAPTURE = "capture"
    DELAY = "delay"
    CLICK = "click"
    KEY = "key"
    SCROLL = "scroll"
    SWIPE = "Swipe"
    MOVE = "move"


MACRO_ACTIONS = [action.value for action in MacroActions]

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

DEFAULT_ACTION_VALUES = {
    "capture": "0,0,0,0",
    "click": "0,0,0,0",
    "scroll": "0,0,0,0",
    "move": "0,0,0,0",
    "delay": 500,
    "key": "right",
}


class CommandWidget(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_CommandWidget()
        self.ui.setupUi(self)
        self.connect_signals_slots()
        self.macro_type = ""
        self.main = None
        self.config = Config()

        self.ui.macroTable.setColumnWidth(0, 80)
        self.ui.macroTable.setColumnWidth(1, 110)
        self.ui.macroTable.setColumnWidth(2, 60)
        self.ui.macroTable.setColumnWidth(3, 60)

        self.action_row = None
        self.init_table = False
        # 마우스 선택 상자 오버레이
        self.overlay = None

    def set_macro(self, main, macro_type: str = "macro"):
        self.main = main
        self.macro_type = macro_type

        self.ui.macroTable.setRowCount(len(self.macros()))
        self.ui.macroTable.setAlternatingRowColors(True)

        self.init_table = False
        for row, macro in enumerate(self.macros()):
            self.set_macro_table_row(row, macro.action, macro.value)

        self.init_table = True
        self.button_enable_setting()

    def macros(self) -> List[Macro]:
        if self.macro_type == "macro":
            return self.config.macro
        elif self.macro_type == "pre_macro":
            return self.config.pre_macro
        else:
            return []

    def connect_signals_slots(self):
        # Macro buttons
        self.ui.btnCommandInsert.clicked.connect(self.on_macro_insert)
        self.ui.btnCommandAdd.clicked.connect(self.on_macro_add)
        self.ui.btnCommandRemove.clicked.connect(self.on_macro_remove)

    def add_row(self, row, action=MacroActions.CAPTURE.value, value=None):
        value = DEFAULT_ACTION_VALUES.get(action, value)
        new_macro = Macro(action, value)
        self.macros().insert(row, new_macro)

        self.ui.macroTable.insertRow(row)
        self.set_macro_table_row(row, action, value)
        self.config.save_to_settings()

    def on_macro_insert(self):
        self.add_row(self.ui.macroTable.currentRow())

    def on_macro_add(self):
        self.add_row(self.ui.macroTable.currentRow() + 1)

    def on_macro_remove(self):
        row = self.ui.macroTable.currentRow()
        self.macros().pop(row)
        self.ui.macroTable.removeRow(row)
        self.config.save_to_settings()
        self.button_enable_setting()

    def button_enable_setting(self):
        flag = self.ui.macroTable.rowCount() > 0
        self.ui.btnCommandRemove.setEnabled(flag)
        self.ui.btnCommandInsert.setEnabled(flag)

    def set_macro_table_row(self, row: int, action, value):
        actionCombo = QComboBox()
        actionCombo.addItems(MACRO_ACTIONS)
        actionCombo.currentTextChanged.connect(
            lambda action, r=row: self.on_action_combo_changed(r, action)
        )
        index = actionCombo.findText(action)
        if index > -1:
            actionCombo.setCurrentIndex(index)
        self.ui.macroTable.setCellWidget(row, 0, actionCombo)

        self.set_macro_row(row, action, value)

    def set_macro_row(self, row: int, action: str = None, value: str = None):
        self.ui.macroTable.removeCellWidget(row, 1)
        self.ui.macroTable.removeCellWidget(row, 2)
        self.ui.macroTable.removeCellWidget(row, 3)

        self.macros()[row].action = action

        if action in {
            MacroActions.CAPTURE.value,
            MacroActions.CLICK.value,
            MacroActions.SCROLL.value,
            MacroActions.MOVE.value,
        }:

            button = QPushButton()
            button.setText("영역선택")
            button.clicked.connect(partial(self.handle_screen_rect, row))

            button2 = QPushButton()
            button2.setText("확인")
            button2.pressed.connect(partial(self.handle_rect_check_show, row))
            button2.released.connect(self.handle_rect_check_hide)

            self.ui.macroTable.setCellWidget(row, 2, button)
            self.ui.macroTable.setCellWidget(row, 3, button2)

            input_item = QTableWidgetItem("")
            input_item.setText(value)
            input_item.setFlags(input_item.flags() & ~Qt.ItemIsEditable)
            self.ui.macroTable.setItem(row, 1, input_item)

        elif action == MacroActions.KEY.value:
            keyCombo = QComboBox()
            keyCombo.addItems(KEY_ACTIONS)
            current_value = value if value is not None else "right"
            keyCombo.currentTextChanged.connect(
                lambda text, r=row: self.set_macro_table_row_value(
                    r, MacroActions.KEY.value, text
                )
            )
            index = keyCombo.findText(current_value)
            if index > -1:
                keyCombo.setCurrentIndex(index)
            self.ui.macroTable.setCellWidget(row, 1, keyCombo)
        elif action == MacroActions.DELAY.value:
            delaySpin = QSpinBox()
            delaySpin.setRange(1, 20000)
            delaySpin.setSuffix("ms")
            delaySpin.setValue(
                int(value) if isinstance(value, str) and value.isdigit() else 500
            )  # 기본 값을 500으로 설정
            delaySpin.valueChanged.connect(
                lambda val, r=row: self.set_macro_table_row_value(
                    r, MacroActions.DELAY.value, val
                )
            )  # 수정된 부분
            self.ui.macroTable.setCellWidget(row, 1, delaySpin)

        if action in {MacroActions.DELAY.value, MacroActions.KEY.value}:
            # 2,3셀은 쓰지 않음
            self.set_disabled_cell(row, 2)
            self.set_disabled_cell(row, 3)

        self.set_macro_table_row_value(row, action, value)

    def on_action_combo_changed(self, row, action):
        value = DEFAULT_ACTION_VALUES.get(action)
        self.macros()[row].action = action
        self.macros()[row].value = value
        self.set_macro_row(row, action, value)
        self.config.save_to_settings()

    def set_disabled_cell(self, row: int, column: int):
        item = self.ui.macroTable.item(row, column)
        if item is not None:
            item.setFlags(item.flags() & ~Qt.ItemIsEditable)
            self.ui.macroTable.setItem(row, int, item)

    def set_macro_table_row_value(self, row: int, action: MacroActions, value):
        value_widget = self.ui.macroTable.cellWidget(row, 1)
        try:
            if action == MacroActions.DELAY.value:
                self.macros()[row].value = value
            elif action == MacroActions.KEY.value:
                index = value_widget.findText(value)  # 수정된 부분
                if index > -1:
                    value_widget.setCurrentIndex(index)
            elif action in {
                MacroActions.CAPTURE.value,
                MacroActions.CLICK.value,
                MacroActions.SCROLL.value,
                MacroActions.MOVE.value,
                MacroActions.SWIPE.value,
            }:
                self.ui.macroTable.item(row, 1).setText(value)
            self.macros()[row].value = value
            self.config.save_to_settings()
        except (AttributeError, KeyError, TypeError) as e:
            print(f"An error occurred: {e}")

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
        self.macros()[self.action_row].value = f"{x},{y},{width},{height}"
        self.config.save_to_settings()
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

    def set_row_colors(self, row, background_color, text_color):
        for column in range(self.ui.macroTable.columnCount()):
            item = self.ui.macroTable.item(row, column)
            if item is not None:
                item.setBackground(background_color)
                item.setForeground(text_color)
