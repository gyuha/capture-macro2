import platform

from PySide6.QtCore import Signal

from app.utils.qt_singleton import QtSingleton


class AppCore(QtSingleton):
    signal_add_image = Signal(str)
    signal_macro_done = Signal()

    def __init__(self):
        super().__init__()

        self.total_image_count = 0
        self.image_number = 0  # 이미지 번호 저장용

        self.same_count = 0
        self.is_running = False
        self.macro_type = "pre_macro"
        self.macro_row = 0

        self.is_windows = platform.system() == "Windows"
        self.is_mac = platform.system() == "Darwin"
