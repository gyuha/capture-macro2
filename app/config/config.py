import os
import platform
from typing import Any, Dict, List

import yaml
from PySide6.QtCore import QObject
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
        self.use_ocr = False
        self.window_name = ""

        self.load_from_file(self.get_config_path())

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

    def make_default_config(self, config_path: str):
        config = {
            "capture_path": self.get_default_data_folder("CaptureMacro"),
            "pdf_path": self.get_default_pdf_folder(),
            "use_ocr": False,
            "image_quality": 88,
            "max_page": 1500,
            "monitor": 0,
            "same_count": 3,
            "pre_macro": [],
            "macro": [],
        }
        with open(config_path, "w", encoding="utf-8") as file:
            yaml.dump(config, file, default_flow_style=False)

    def get_config_path(self):
        app_name = "CaptureMacro"
        config_dir = os.path.expanduser(f"~/.{app_name}")
        config_path = os.path.join(config_dir, "config.yml")
        if not os.path.exists(config_dir):
            os.makedirs(config_dir)
            self.make_default_config(config_path)
        return config_path

    def load_from_file(self, filepath: str) -> None:
        if not os.path.exists(filepath):
            self.make_default_config(filepath)
        
        with open(filepath, "r", encoding="utf-8") as file:
            data = yaml.safe_load(file)

        self.capture_path = (
            data["capture_path"] if "capture_path" in data else self.get_default_data_folder("CaptureMacro")
        )
        self.pdf_path = data["pdf_path"] if "pdf_path" in data else self.get_default_pdf_folder()
        self.use_ocr = data["use_ocr"] if "use_ocr" in data else False
        if platform.system() == "Windows":
            self.use_ocr = False
        self.monitor = data["monitor"]
        # 모니터 수 확인
        num_monitors = len(QApplication.screens())
        # self.monitor 값이 모니터 수보다 크면 0으로 설정
        if self.monitor >= num_monitors:
            self.monitor = 0

        self.same_count = data["same_count"]
        self.image_quality = data["image_quality"]
        self.max_page = data["max_page"]
        self.pre_macro = [Macro.from_dict(macro) for macro in data["pre_macro"]]
        self.macro = [Macro.from_dict(macro) for macro in data["macro"]]

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

    def save_to_file(self) -> None:
        with open(self.get_config_path(), "w", encoding="utf-8") as file:
            yaml.dump(self.to_dict(), file, default_flow_style=False)

    def __str__(self) -> str:
        pre_macro_str = "\n    ".join(str(macro) for macro in self.pre_macro)
        macro_str = "\n    ".join(str(macro) for macro in self.macro)
        return (
            f"Config(\n"
            f"  capture_path={self.capture_path},\n"
            f"  image_quality={self.image_quality},\n"
            f"  macro=[\n    {macro_str}\n  ],\n"
            f"  pdf_path=[\n    {self.pdf_path}\n  ],\n"
            f"  use_ocr={self.use_ocr},\n"
            f"  max_page={self.max_page},\n"
            f"  monitor={self.monitor},\n"
            f"  pre_macro=[\n    {pre_macro_str}\n  ],\n"
            f"  same_count={self.same_count}\n"
            f")"
        )
