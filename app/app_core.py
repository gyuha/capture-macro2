import platform

from PySide6.QtCore import Signal, Slot

from app.config.config import Config
from app.utils.pynput_keymap import get_key_from_string
from app.utils.qt_singleton import QtSingleton
from PySide6.QtWidgets import QApplication

from pynput.keyboard import Controller as KeyboardController
from pynput.mouse import Button
from pynput.mouse import Controller as MouseController


class AppCore(QtSingleton):
    signal_add_image = Signal(str)
    signal_macro_done = Signal()
    signal_image_preview = Signal(str)
    signal_image_clear = Signal()

    signal_mouse_event = Signal(str, int, int)
    signal_key_event = Signal(str)

    def __init__(self):
        super().__init__()

        self.total_image_count = 0
        self.image_number = 0  # 이미지 번호 저장용

        self.same_count = 0
        self.is_running = False
        self.macro_type = "pre_macro"
        self.macro_row = 0

        self.config = Config()

        self.is_windows = platform.system() == "Windows"
        self.is_mac = platform.system() == "Darwin"

        # 화면 설정 가져 오기
        self.screens = QApplication.screens()
        self.screen = self.screens[0]
        self.monitor = self.screen.geometry()
        self.device_pixel_ratio = 1

        self.mouse = MouseController()
        self.keyboard = KeyboardController()

        self.connect_signals_slots()

    def set_monitor(self):
        self.screens = QApplication.screens()
        if self.config.monitor > len(self.screens):
            return False
        self.screen = self.screens[self.config.monitor]
        self.monitor = self.screen.geometry()
        self.device_pixel_ratio = self.screen.devicePixelRatio()
        return True

    def connect_signals_slots(self):
        self.signal_mouse_event.connect(self.on_mouse_event)
        self.signal_key_event.connect(self.on_key_event)

    @Slot(str, int, int)
    def on_mouse_event(self, event, x, y):
        try:
            self.mouse.position = (x, y)
            if event == "scroll":
                self.mouse.scroll(Button.left, -1)
            elif event == "click":
                self.mouse.click(Button.left, 1)
        except AttributeError:
            print(f"Unknown event: {event}")

    @Slot(str)
    def on_key_event(self, key):
        try:
            send_key = get_key_from_string(key)
            self.keyboard.press(send_key)
            self.keyboard.release(send_key)
        except AttributeError:
            print(f"Unknown key: {key}")
