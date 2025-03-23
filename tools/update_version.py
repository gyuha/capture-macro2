#!/usr/bin/env python3
"""
버전 업데이트 스크립트

이 스크립트는 새 버전을 배포할 때 버전 번호를 업데이트하는 데 사용됩니다.
사용법: python update_version.py <버전>
예: python update_version.py 1.0.1
"""
import os
import re
import sys
from datetime import datetime


def update_version(new_version):
    """
    version.py 파일의 버전을 업데이트합니다.

    Args:
        new_version (str): 새 버전 문자열 (예: "1.0.1")

    Returns:
        bool: 성공 여부
    """
    version_file = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "app",
        "config",
        "version.py",
    )

    if not os.path.exists(version_file):
        print(f"오류: 버전 파일을 찾을 수 없습니다: {version_file}")
        return False

    with open(version_file, "r", encoding="utf-8") as f:
        content = f.read()

    # 버전 문자열만 업데이트하고 다른 import 문은 유지
    new_content = re.sub(r'VERSION = "[^"]+"', f'VERSION = "{new_version}"', content)

    # __future__ import 제거 (만약 있다면)
    new_content = re.sub(r"from __future__ import annotations\n", "", new_content)

    with open(version_file, "w", encoding="utf-8") as f:
        f.write(new_content)

    print(f"버전이 {new_version}(으)로 업데이트되었습니다.")

    # 버전 이력 로그 업데이트
    update_version_history(new_version)

    return True


def update_version_history(version):
    """
    버전 이력을 기록합니다.

    Args:
        version (str): 버전 문자열
    """
    history_file = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "version_history.txt",
    )

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(history_file, "a+", encoding="utf-8") as f:
        f.seek(0)
        if not f.read().strip():
            f.write("# 버전 이력\n\n")
        f.write(f"## 버전 {version} - {now}\n\n")


def main():
    if len(sys.argv) != 2:
        print(f"사용법: {sys.argv[0]} <버전>")
        print(f"예: {sys.argv[0]} 1.0.1")
        return 1

    new_version = sys.argv[1]

    # 버전 형식 확인 (예: 1.0.0)
    if not re.match(r"^\d+\.\d+\.\d+$", new_version):
        print("오류: 버전은 X.Y.Z 형식이어야 합니다 (예: 1.0.0)")
        return 1

    if update_version(new_version):
        return 0
    else:
        return 1


if __name__ == "__main__":
    sys.exit(main())
