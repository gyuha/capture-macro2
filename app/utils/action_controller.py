import os
import random
import threading
import time
from typing import List

import mss
import mss.tools
from PIL import Image
from PySide6.QtCore import QObject
from PySide6.QtWidgets import QApplication

from app.app_core import AppCore
from app.config.config import Config, Macro
from app.utils.input_controller import InputController
from app.utils.jpg_image_optimize import jpg_image_optimize


class ActionController(QObject):

    def __init__(self):
        super().__init__()

        self.app_core = AppCore()
        self.app_core.macro_type = "pre_macro"
        self.app_core.is_running = False

        self.config = Config()
        self._action_macro = []
        self.current_row = 0

        self.input_controller = InputController()

        # 화면 설정 가져 오기
        self.screens = QApplication.screens()
        self.monitor = self.screens[0].geometry()

    @property
    def action_macro(self):
        return self._action_macro

    @action_macro.setter
    def action_macro(self, value: List[Macro]):
        self._action_macro = value

    def capture(self, value):
        x, y, width, height = map(int, value.split(","))
        file_path = f"{self.config.capture_path}/{self.app_core.image_number:04}.jpg"

        try:
            with mss.mss() as sct:
                screen_num = int(self.config.monitor)
                mon = sct.monitors[screen_num + 1]

                monitor = {
                    "left": mon["left"] + x,
                    "top": mon["top"] + y,
                    "width": width,
                    "height": height,
                    "mon": screen_num,
                }

                if self.app_core.is_mac:
                    device_pixel_ratio = self.app_core.device_pixel_ratio
                    monitor["top"] = int(monitor["top"] / device_pixel_ratio)
                    monitor["left"] = int(monitor["left"] / device_pixel_ratio)
                    monitor["width"] = int(monitor["width"] / device_pixel_ratio)
                    monitor["height"] = int(monitor["height"] / device_pixel_ratio)

                x, y = self.input_controller.get_mouse_position()
                if self.app_core.is_mac:
                    self.app_core.signal_mouse_event.emit(
                        "move", mon["left"] + mon["width"], mon["top"] + mon["height"]
                    )

                sct_img = sct.grab(monitor)
                img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")

                path = os.path.join(file_path)

                # 이미지 저장 하기
                jpg_image_optimize(img, path, quality=int(self.config.image_quality))

                if self.app_core.is_mac:
                    self.app_core.signal_mouse_event.emit("move", x, y)

            self.app_core.image_number += 1
            self.app_core.signal_add_image.emit(file_path)
        except Exception as e:
            print(f"An error occurred: {e}")

    def key(self, value):
        self.app_core.signal_key_event.emit(value)

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

    def mouse_move(self, value):
        x, y, width, height = map(int, value.split(","))
        move_x = random.randint(x, x + width)
        move_y = random.randint(y, y + height)

        move_x += self.app_core.monitor.left()
        move_y += self.app_core.monitor.top()

        if self.app_core.is_mac:
            move_x = int(move_x / self.app_core.device_pixel_ratio)
            move_y = int(move_y / self.app_core.device_pixel_ratio)
        return move_x, move_y

    def scroll(self, value):
        x, y = self.mouse_move(value)
        self.app_core.signal_mouse_event.emit("scroll", x, y)

    def click(self, value):
        x, y = self.mouse_move(value)
        self.app_core.signal_mouse_event.emit("click", x, y)

    def move(self, value):
        x, y = self.mouse_move(value)
        self.app_core.signal_mouse_event.emit("move", x, y)

    def execute_macro(self, macro_list: List[Macro]):
        for macro in macro_list:
            if not self.app_core.is_running:
                break
            # self.app_core.macro_row = index
            # print(index)
            action_method = getattr(self, macro.action, None)
            if action_method:
                action_method(macro.value)
            else:
                print(f"Unknown action: {macro.action}")

    def done(self):
        self.app_core.is_running = False
        self.app_core.signal_macro_done.emit()

    def start(self):
        self.app_core.is_running = True

        if not self.app_core.set_monitor():
            self.done()
            return

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
