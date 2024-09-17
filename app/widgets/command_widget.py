from functools import partial
from typing import List

from PySide6.QtCore import Signal, Slot
from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QPushButton,
    QTableWidgetItem,
    QWidget,
    QSpinBox,
)

from app.config.config import Config, Macro
from app.utils.rect.rect_check_overlay import RectCheckOverlay
from app.utils.rect.rect_overlay import RectOverlay
from app.utils.rect_value_utils import is_valid_rect_string_value, string_to_rect_value
from ui.command_widget_ui import Ui_CommandWidget

MACRO_ACTIONS = ["capture", "delay", "click", "key", "scroll", "move"]
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

        # 마우스 선택 상자 오버레이
        self.overlay = None

    def set_macro(self, main, macro_type: str = "macro"):
        self.main = main
        self.macro_type = macro_type

        self.ui.macroTable.setRowCount(len(self.macros()))
        self.ui.macroTable.setAlternatingRowColors(True)

        for row, macro in enumerate(self.macros()):
            self.set_macro_table_row(row, macro.action, macro.value)
        self.update_macro_actions()

        self.button_enable_setting()

        self.ui.macroTable.itemChanged.connect(self.update_macro_actions)

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

    def add_row(self, row, action="capture", value=None):
        new_macro = Macro(action, value)
        self.macros().insert(row, new_macro)

        self.ui.macroTable.insertRow(row)
        self.set_macro_table_row(row, action, value)

        self.update_macro_actions()

    def on_macro_insert(self):
        self.add_row(self.ui.macroTable.currentRow())

    def on_macro_add(self):
        self.add_row(self.ui.macroTable.currentRow() + 1)

    def on_macro_remove(self):
        row = self.ui.macroTable.currentRow()
        self.macros.pop(row)
        self.ui.macroTable.removeRow(row)
        self.update_macro_actions()
        self.button_enable_setting()

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
        self.button_enable_setting()

    def button_enable_setting(self):
        flag = self.ui.macroTable.rowCount() > 0
        self.ui.btnCommandRemove.setEnabled(flag)
        self.ui.btnCommandInsert.setEnabled(flag)

    def update_macro_actions(self):
        self.ui.macroTable.blockSignals(True)
        try:
            for row in range(self.ui.macroTable.rowCount()):
                value = self.macros()[row].value
                cell_widget = self.ui.macroTable.cellWidget(row, 0)
                action = (
                    cell_widget.currentText()
                    if cell_widget
                    and hasattr(cell_widget, "currentText")
                    and callable(cell_widget.currentText)
                    else ""
                )
                self.ui.macroTable.removeCellWidget(row, 1)
                self.ui.macroTable.removeCellWidget(row, 2)
                self.ui.macroTable.removeCellWidget(row, 3)
                if (
                    action == "capture"
                    or action == "click"
                    or action == "scroll"
                    or action == "move"
                ):
                    button = QPushButton()
                    button.setText("영역선택")
                    button.clicked.connect(partial(self.handle_screen_rect, row))
                    button2 = QPushButton()
                    button2.setText("확인")
                    button2.pressed.connect(partial(self.handle_rect_check_show, row))
                    button2.released.connect(self.handle_rect_check_hide)
                    self.ui.macroTable.setCellWidget(row, 2, button)
                    self.ui.macroTable.setCellWidget(row, 3, button2)

                    # 1번째 cell을 입력 상자로 설정
                    input_item = QTableWidgetItem("")
                    input_item.setText(value)
                    self.ui.macroTable.setItem(row, 1, input_item)  # 입력 상자로 설정
                elif action == "key":
                    keyCombo = QComboBox()
                    keyCombo.addItems(KEY_ACTIONS)
                    current_value = value if value is not None else "right"
                    keyCombo.currentTextChanged.connect(
                        lambda text, r=row: self.update_macro_value(r, text)
                    )
                    index = keyCombo.findText(current_value)  # 수정된 부분
                    if index > -1:
                        keyCombo.setCurrentIndex(index)
                    self.ui.macroTable.setCellWidget(row, 1, keyCombo)
                elif action == "delay":
                    delaySpin = QSpinBox()
                    delaySpin.setRange(1, 20000)
                    delaySpin.setSuffix("ms")
                    delaySpin.setValue(
                        int(value) if value.isdigit() else 500
                    )  # 기본 값을 500으로 설정
                    delaySpin.valueChanged.connect(
                        lambda val, r=row: self.update_macro_delay(r, val)
                    )  # 수정된 부분
                    self.ui.macroTable.setCellWidget(row, 1, delaySpin)

                if action == "key" or action == "delay":
                    item2 = QTableWidgetItem("")
                    item3 = QTableWidgetItem("")
                    self.ui.macroTable.setItem(row, 2, item2)
                    self.ui.macroTable.setItem(row, 3, item3)

        except (AttributeError, KeyError, TypeError) as e:
            print(f"An error occurred: {e}")
        finally:
            self.config.save_to_settings()
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

    def set_row_colors(self, row, background_color, text_color):
        for column in range(self.ui.macroTable.columnCount()):
            item = self.ui.macroTable.item(row, column)
            if item is not None:
                item.setBackground(background_color)
                item.setForeground(text_color)

    def update_macro_value(self, row, action):
        if row < len(self.macros()):
            self.macros()[row].value = action  # macro의 값을 업데이트
            # self.update_macro_actions()  # 매크로 액션 업데이트 호출

    def update_macro_delay(self, row, value):
        if row < len(self.macros()):
            self.macros()[row].value = str(value)  # macro의 값을 업데이트
            # self.update_macro_actions()  # 매크로 액션 업데이트 호출
