import os
import random
import threading
import time
from typing import List

import mss
import mss.tools
from PIL import Image
from pynput.keyboard import Controller as KeyboardController
from pynput.mouse import Button
from pynput.mouse import Controller as MouseController
from PySide6.QtCore import QObject
from PySide6.QtWidgets import QApplication

from app.app_core import AppCore
from app.config.config import Config, Macro
from app.utils.jpg_image_optimize import jpg_image_optimize
from app.utils.pynput_keymap import get_key_from_string


class ActionController(QObject):

    def __init__(self):
        super().__init__()

        self.app_core = AppCore()
        self.app_core.macro_type = "pre_macro"
        self.app_core.is_running = False

        self.config = Config()
        self._action_macro = []
        self.device_pixel_ratio = 1
        self.mouse = MouseController()
        self.keyboard = KeyboardController()
        self.current_row = 0

    @property
    def action_macro(self):
        return self._action_macro

    @action_macro.setter
    def action_macro(self, value: List[Macro]):
        self._action_macro = value

    def capture(self, value):
        x, y, width, height = map(int, value.split(","))
        file_path = f"{self.config.capture_path}/{self.app_core.image_number:04}.jpg"

        with mss.mss() as sct:
            screen_num = int(self.config.monitor)
            mon = sct.monitors[screen_num + 1]

            monitor = {
                "top": mon["top"] + y,
                "left": mon["left"] + x,
                "width": width,
                "height": height,
                "mon": screen_num,
            }

            if self.app_core.is_mac:
                monitor["top"] = int(monitor["top"] / self.device_pixel_ratio)
                monitor["left"] = int(monitor["left"] / self.device_pixel_ratio)
                monitor["width"] = int(monitor["width"] / self.device_pixel_ratio)
                monitor["height"] = int(monitor["height"] / self.device_pixel_ratio)

            sct_img = sct.grab(monitor)
            img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")

            path = os.path.join(file_path)

            # 이미지 저장 하기
            jpg_image_optimize(img, path, quality=int(self.config.image_quality))

        self.app_core.image_number += 1
        self.app_core.signal_add_image.emit(file_path)

    def key(self, value):
        try:
            send_key = get_key_from_string(value)
            if send_key:
                self.keyboard.press(send_key)
                self.keyboard.release(send_key)
        except ValueError:
            print(f"Invalid key: {value}")

    def delay(self, value):
        total_delay = int(value)
        interval = 100  # 100ms 간격으로 체크
        for _ in range(0, total_delay, interval):
            if not self.app_core.is_running:
                return
            time.sleep(interval / 1000)
        remaining = total_delay % interval
        if remaining > 0 and self.app_core.is_running:
            time.sleep(remaining / 1000)

    def scroll(self, value):
        x, y, width, height = map(int, value.split(","))
        click_x = random.randint(x, x + width)
        click_y = random.randint(y, y + height)
        self.mouse.position = (click_x, click_y)
        self.mouse.scroll(0, -1)

    def click(self, value):
        x, y, width, height = map(int, value.split(","))
        click_x = random.randint(x, x + width)
        click_y = random.randint(y, y + height)
        self.mouse.position = (click_x, click_y)
        self.mouse.click(Button.left, 1)

    def execute_macro(self, macro_list: List[Macro]):
        for macro in macro_list:
            if not self.app_core.is_running:
                break
            # self.app_core.macro_row = index
            # print(index)
            action_method = getattr(self, macro.action, None)
            if action_method:
                print(f"Executing {macro.action} with value: {macro.value}")
                action_method(macro.value)
            else:
                print(f"Unknown action: {macro.action}")

    def done(self):
        self.app_core.is_running = False
        self.app_core.signal_macro_done.emit()

    def start(self):
        self.app_core.is_running = True

        # 화면 설정 가져 오기
        screens = QApplication.screens()
        if self.config.monitor > len(screens):
            self.done()
            return

        screen = screens[self.config.monitor]
        self.device_pixel_ratio = screen.devicePixelRatio()

        threading.Thread(target=self.run_macros, daemon=True).start()

    def run_macros(self):
        if self.app_core.macro_type == "pre_macro":
            self.execute_macro(self.config.pre_macro)
            self.app_core.is_running = False
            self.app_core.signal_macro_done.emit()
            return

        while self.app_core.is_running:
            self.execute_macro(self.config.macro)

    def stop(self):
        self.app_core.is_running = False
