import os
import random
import threading
import time
from typing import List

import mozjpeg_lossless_optimization
import mss
import mss.tools
import pyautogui
from PIL import Image
from PySide6.QtCore import QObject, Signal

from app.config.config import Config, Macro


class ActionController(QObject):
    signal_done = Signal()
    signal_add_image = Signal(int, str)
    signal_current_row = Signal(int)

    def __init__(self):
        super().__init__()
        self.is_running = False
        self._config = None
        self._action_type = "pre_macro"
        self._image_number = 0

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
    def config(self):
        return self._config

    @config.setter
    def config(self, value: Config):
        self._config = value

    @property
    def image_number(self):
        return self.image_number

    @image_number.setter
    def image_number(self, value):
        self._image_number = value

    def capture(self, value):
        x, y, width, height = map(int, value.split(","))
        file_path = f"{self.config.capture_path}/{self._image_number:04}.jpg"

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
            sct_img = sct.grab(monitor)
            img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")

            path = os.path.join(file_path)
            img.save(path, "JPEG", quality=int(self.config.image_quality))

        # JPG 추가 압축히기
        # https: // github.com/wanadev/mozjpeg-lossless-optimization
        with open(path, "rb") as input_jpeg_file:
            input_jpeg_bytes = input_jpeg_file.read()

        output_jpeg_bytes = mozjpeg_lossless_optimization.optimize(input_jpeg_bytes)

        with open(file_path, "wb") as output_jpeg_file:
            output_jpeg_file.write(output_jpeg_bytes)

        self._image_number += 1
        self.signal_add_image.emit(self._image_number, file_path)

    def key(self, value):
        pyautogui.press(value)

    def delay(self, value):
        total_delay = int(value)
        interval = 100  # 100ms 간격으로 체크
        for _ in range(0, total_delay, interval):
            if not self.is_running:
                return
            time.sleep(interval / 1000)
        remaining = total_delay % interval
        if remaining > 0 and self.is_running:
            time.sleep(remaining / 1000)

    def click(self, value):
        x, y, width, height = map(int, value.split(","))
        click_x = random.randint(x, x + width)
        click_y = random.randint(y, y + height)
        pyautogui.click(click_x, click_y)

    def execute_macro(self, macro_list: List[Macro]):
        for macro in macro_list:
            if not self.is_running:
                break
            action_method = getattr(self, macro.action, None)
            if action_method:
                print(f"Executing {macro.action} with value: {macro.value}")
                action_method(macro.value)
            else:
                print(f"Unknown action: {macro.action}")

    def start(self):
        self.is_running = True
        # self._config.capture의 경로가 없다면 생성
        if os.path.exists(self.config.capture_path) is False:
            os.makedirs(self.config.capture_path)

        threading.Thread(target=self.run_macros, daemon=True).start()

    def run_macros(self):
        if self._action_type == "pre_macro":
            self.execute_macro(self.config.pre_macro)
        else:
            while self.is_running:
                self.execute_macro(self.config.macro)

        self.signal_done.emit()

    def stop(self):
        self.is_running = False
