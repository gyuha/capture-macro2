from typing import Any, Dict, List

import yaml


class Macro:
    def __init__(self, action: str, value: str):
        self.action = action
        self.value = value

    @classmethod
    def from_dict(cls, data: Dict[str, str]) -> "Macro":
        return cls(action=data["action"], value=data["value"])

    def to_dict(self) -> Dict[str, str]:
        return {"action": self.action, "value": self.value}


class Config:
    def __init__(self, filepath: str = "config.yml"):
        self.capture_path = ""
        self.window_name = ""
        self.monitor = 0
        self.same_count = 0
        self.click_point = ""
        self.screen_rect = ""
        self.image_quality = 0
        self.pre_macro: List[Macro] = []
        self.macro: List[Macro] = []

        self.load_from_file(filepath)

    def load_from_file(self, filepath: str) -> None:
        with open(filepath, "r", encoding="utf-8") as file:
            data = yaml.safe_load(file)

        self.capture_path = data["capture_path"]
        self.monitor = data["monitor"]
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

    def save_to_file(self, filepath: str = "config.yml") -> None:
        with open(filepath, "w", encoding="utf-8") as file:
            yaml.dump(self.to_dict(), file, default_flow_style=False)

    def __str__(self) -> str:
        pre_macro_str = "\n    ".join(str(macro) for macro in self.pre_macro)
        macro_str = "\n    ".join(str(macro) for macro in self.macro)
        return (
            f"Config(\n"
            f"  capture_path={self.capture_path},\n"
            f"  monitor={self.monitor},\n"
            f"  same_count={self.same_count},\n"
            f"  image_quality={self.image_quality},\n"
            f"  max_page={self.max_page},\n"
            f"  pre_macro=[\n    {pre_macro_str}\n  ],\n"
            f"  macro=[\n    {macro_str}\n  ]\n"
            f")"
        )


if __name__ == "__main__":
    config = Config()
    # config.save_to_file("config.yml")

    print(config)

    # 사용 예시:
    # 설정을 파일에서 읽어오기
    # config = Config.load_from_file("config.yml")

    # 변경 후 파일에 저장하기
    # config.save_to_file("new_config.yml")
