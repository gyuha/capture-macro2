import json
import os
import platform
from typing import Any, Dict, List

from PySide6.QtCore import QObject, QSettings
from PySide6.QtWidgets import QApplication

from app.utils.singleton_meta import SingletonMeta


class Macro:
    def __init__(self, action: str, value: str):
        self.action = action
        self.value = value

    @classmethod
    def from_dict(cls, data: Dict[str, str]) -> "Macro":
        return cls(action=data["action"], value=data["value"])

    def to_dict(self) -> Dict[str, str]:
        return {"action": self.action, "value": self.value}


class Config(QObject, metaclass=SingletonMeta):
    def __init__(self):
        super().__init__()

        # 저장용 설정 값
        self.capture_path = ""
        self.click_point = ""
        self.image_quality = 0
        self.macro: List[Macro] = []
        self.monitor = 0
        self.pdf_path = ""
        self.pre_macro: List[Macro] = []
        self.same_count = 0
        self.screen_rect = ""
        self.window_name = ""
        self.image_size = 2000
        self.max_page = 1500
        self.wheel = -1

        self.settings = QSettings("CaptureMacro", "Settings")
        print(self.settings.fileName())
        self.load_from_settings()

    def get_default_pdf_folder(self):
        system = platform.system()
        base_dir = ""
        if system in ["Windows", "Darwin"]:  # Windows or macOS
            base_dir = os.path.join(os.path.expanduser("~"), "Desktop")
        else:
            base_dir = os.path.expanduser("~")
        return base_dir

    def get_default_data_folder(self, app_name):
        # 운영 체제 감지
        system = platform.system()

        if system in ["Windows", "Darwin"]:  # Windows or macOS
            base_dir = os.path.expanduser("~/Documents")
        else:
            # 기타 운영 체제의 경우 (기본적으로 홈 디렉토리 사용)
            base_dir = os.path.expanduser("~")

        # 어플리케이션 전용 폴더 경로 생성
        app_data_folder = os.path.join(base_dir, app_name)

        # 폴더가 존재하지 않으면 생성
        if not os.path.exists(app_data_folder):
            os.makedirs(app_data_folder)

        return app_data_folder

    def load_from_settings(self) -> None:
        self.capture_path = self.settings.value(
            "capture_path", self.get_default_data_folder("CaptureMacro")
        )
        self.pdf_path = self.settings.value("pdf_path", self.get_default_pdf_folder())
        self.monitor = self.settings.value("monitor", 0, type=int)
        num_monitors = len(QApplication.screens())
        if self.monitor >= num_monitors:
            self.monitor = 0
        self.same_count = self.settings.value("same_count", 3, type=int)
        self.image_quality = self.settings.value("image_quality", 88, type=int)
        self.max_page = self.settings.value("max_page", 1500, type=int)
        self.wheel = self.settings.value("wheel", -1, type=int)

        pre_macro_json = self.settings.value("pre_macro", "[]")
        self.pre_macro = [
            Macro.from_dict(macro) for macro in json.loads(pre_macro_json)
        ]

        macro_json = self.settings.value("macro", "[]")
        self.macro = [Macro.from_dict(macro) for macro in json.loads(macro_json)]

    def save_to_settings(self) -> None:
        self.settings.setValue("capture_path", self.capture_path)
        self.settings.setValue("pdf_path", self.pdf_path)
        self.settings.setValue("monitor", self.monitor)
        self.settings.setValue("same_count", self.same_count)
        self.settings.setValue("image_quality", self.image_quality)
        self.settings.setValue("max_page", self.max_page)
        self.settings.setValue("wheel", self.wheel)

        pre_macro_json = json.dumps([macro.to_dict() for macro in self.pre_macro])
        self.settings.setValue("pre_macro", pre_macro_json)

        macro_json = json.dumps([macro.to_dict() for macro in self.macro])
        self.settings.setValue("macro", macro_json)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "capture_path": self.capture_path,
            "monitor": self.monitor,
            "same_count": self.same_count,
            "image_quality": self.image_quality,
            "max_page": self.max_page,
            "pre_macro": [macro.to_dict() for macro in self.pre_macro],
            "macro": [macro.to_dict() for macro in self.macro],
        }

    def __str__(self) -> str:
        pre_macro_str = "\n    ".join(str(macro) for macro in self.pre_macro)
        macro_str = "\n    ".join(str(macro) for macro in self.macro)
        return (
            f"Config(\n"
            f"  capture_path={self.capture_path},\n"
            f"  image_quality={self.image_quality},\n"
            f"  macro=[\n    {macro_str}\n  ],\n"
            f"  pdf_path=[\n    {self.pdf_path}\n  ],\n"
            f"  max_page={self.max_page},\n"
            f"  monitor={self.monitor},\n"
            f"  pre_macro=[\n    {pre_macro_str}\n  ],\n"
            f"  same_count={self.same_count}\n"
            f")"
        )
