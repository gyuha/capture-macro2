from typing import List

from PySide6.QtCore import QObject, Signal

from app.config.config import Macro


class ActionController(QObject):
    signal_done = Signal()
    signal_add_image = Signal(str)
    signal_current_row = Signal(int)

    def __init__(self):
        super().__init__()
        self.is_running = False
        self._action_type = "pre_macro"
        self._action_macro = []
        self._monitor_index = 0
        self.current_row = 0

    @property
    def action_type(self):
        return self._action_type

    @action_type.setter
    def action_type(self, value):
        if value not in ["pre_macro", "macro"]:
            raise ValueError("action_type must be 'pre_macro' or 'macro'")
        self._action_type = value

    @property
    def action_macro(self):
        return self._action_macro

    @action_macro.setter
    def action_macro(self, value: List[Macro]):
        self._action_macro = value

    @property
    def monitor_index(self):
        return self._monitor_index

    @monitor_index.setter
    def monitor_index(self, value):
        self._monitor_index = value

    def start(self):
        self.is_running = True
        self.current_row = 0
        self.signal_current_row.emit(self.current_row)
        # for macro in self.action_macro:
        #     print(macro.action, macro.value)
        # self.signal_done.emit()

    def stop(self):
        self.is_running = False
