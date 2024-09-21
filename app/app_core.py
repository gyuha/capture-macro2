import os
import platform
import time

from PySide6.QtCore import QObject, Signal
from PySide6.QtWidgets import QApplication

from app.config.config import Config
from app.utils.input_controller import InputController
from app.utils.singleton_meta import SingletonMeta

os.environ["PYNPUT_BACKEND"] = "darwin"


class AppCore(QObject, metaclass=SingletonMeta):
    signal_add_image = Signal(str)
    signal_macro_done = Signal()
    signal_image_preview = Signal(str)
    signal_image_clear = Signal()

    signal_mouse_event = Signal(str, int, int)
    signal_key_event = Signal(str)

    def __init__(self):
        super(AppCore, self).__init__()

        self.signals_connected = False

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

        self.input_controller = InputController()

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
        if not self.signals_connected:
            self.signal_mouse_event.connect(self.on_mouse_event)
            self.signal_key_event.connect(self.on_key_event)
            self.signals_connected = True

    # @Slot(str, int, int)
    def on_mouse_event(self, event, x, y):
        try:
            self.input_controller.move_mouse(x, y)
            time.sleep(0.01)
            if event == "scroll":
                self.input_controller.scroll_mouse(self.config.wheel)
            elif event == "click":
                self.input_controller.click_mouse()
        except AttributeError:
            print(f"Unknown event: {event}")

    # @Slot(str)
    def on_key_event(self, key):
        print("========> ", key)
        try:
            self.input_controller.press_key(key)
        except AttributeError:
            print(f"Unknown key: {key}")
