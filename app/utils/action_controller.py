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
        if self.config.max_page  < self.app_core.image_number:
            self.done()
            return

        x, y, width, height = map(int, value.split(","))
        file_path = f"{self.config.capture_path}/{self.app_core.image_number:04}.jpg"

        mouse_x = mouse_y = None
        try:
            if self.app_core.is_mac:
                # macOS: mss는 논리 해상도(포인트)로만 캡쳐해 Retina 픽셀을 버린다.
                # Quartz로 직접 캡쳐해 디스플레이의 전체 물리 해상도를 얻는다.
                mouse_x, mouse_y = self.input_controller.get_mouse_position()
                self.app_core.signal_mouse_event.emit(
                    "move",
                    self.app_core.monitor.left() + self.app_core.monitor.width(),
                    self.app_core.monitor.top() + self.app_core.monitor.height(),
                )

                img = self._grab_mac(x, y, width, height)
            else:
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

                    sct_img = sct.grab(monitor)
                    img = Image.frombytes(
                        "RGB", sct_img.size, sct_img.bgra, "raw", "BGRX"
                    )

            # 이미지 저장 하기
            jpg_image_optimize(img, file_path, quality=int(self.config.image_quality))

            self.app_core.image_number += 1
            self.app_core.signal_add_image.emit(file_path)

        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            # 캡쳐 중 구석으로 치워둔 커서를 grab 성공/실패와 무관하게 항상 복원
            if mouse_x is not None:
                self.app_core.signal_mouse_event.emit("move", mouse_x, mouse_y)

    def _grab_mac(self, x, y, width, height):
        """macOS에서 Quartz로 디스플레이 영역을 전체 물리(Retina) 해상도로 캡쳐한다.

        x, y, width, height는 rect_overlay가 저장한 디스플레이-로컬 물리 픽셀 좌표.
        CGDisplayCreateImageForRect는 디스플레이-로컬 '포인트' 좌표를 받으므로 DPR로
        나눠 포인트로 변환하면, 반환 이미지는 포인트 x DPR = 원래 물리 해상도가 된다.
        """
        import Quartz

        dpr = self.app_core.device_pixel_ratio or 1
        display_id = self._mac_display_id()
        rect = Quartz.CGRectMake(x / dpr, y / dpr, width / dpr, height / dpr)

        cg_img = Quartz.CGDisplayCreateImageForRect(display_id, rect)
        if cg_img is None:
            raise RuntimeError("CGDisplayCreateImageForRect가 None을 반환했습니다.")

        w = Quartz.CGImageGetWidth(cg_img)
        h = Quartz.CGImageGetHeight(cg_img)
        bytes_per_row = Quartz.CGImageGetBytesPerRow(cg_img)
        data = bytes(
            Quartz.CGDataProviderCopyData(Quartz.CGImageGetDataProvider(cg_img))
        )
        # CGDisplay 이미지는 little-endian BGRA(프리멀티플라이드). 행 패딩(stride) 처리.
        return Image.frombuffer(
            "RGBA", (w, h), data, "raw", "BGRA", bytes_per_row, 1
        ).convert("RGB")

    def _mac_display_id(self):
        """선택된 모니터의 전역 원점(포인트)을 CGDirectDisplayID로 매핑한다.

        Qt 화면 인덱스와 Quartz 디스플레이 목록 순서가 일치한다고 가정하지 않는다.
        """
        import Quartz

        origin = (self.app_core.monitor.x(), self.app_core.monitor.y())
        err, active, count = Quartz.CGGetActiveDisplayList(16, None, None)
        for display_id in active[:count]:
            bounds = Quartz.CGDisplayBounds(display_id)
            if (round(bounds.origin.x), round(bounds.origin.y)) == origin:
                return display_id
        return Quartz.CGMainDisplayID()

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

    def random_delay(self, value):
        try:
            min_ms, max_ms = map(int, str(value).split(","))
        except (ValueError, AttributeError, TypeError):
            return
        if min_ms > max_ms:
            min_ms, max_ms = max_ms, min_ms
        total_delay = random.randint(min_ms, max_ms)
        interval = 100
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

    def swipe(self, value):
        x, y, width, height = map(int, value.split(","))
        y = y + (height / 2)
        if self.app_core.is_mac:
            x = int(x / self.app_core.device_pixel_ratio)
            y = int(y / self.app_core.device_pixel_ratio)
            width = int(width / self.app_core.device_pixel_ratio)
        start = self.config.swipe_direction == "Left" and (x + width, y) or (x, y)
        end = self.config.swipe_direction == "Left" and (x, y) or (x + width, y)
        self.app_core.signal_mouse_swipe.emit(start, end, self.config.swipe_secs / 1000)

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
