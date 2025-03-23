#!/usr/bin/env python3
"""
버전 업데이트 기능 테스트
"""
import os
import sys

# 현재 디렉토리를 추가하여 모듈을 임포트할 수 있게 합니다
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools.update_version import update_dot_version_file, update_windows_installer

# 테스트 버전으로 업데이트
TEST_VERSION = "1.0.0"

def main():
    """
    버전 업데이트 기능을 테스트합니다.
    """
    print(f"버전을 {TEST_VERSION}(으)로 업데이트합니다.")
    
    # Windows 인스톨러 스크립트 업데이트 테스트
    print("\n1. Windows 인스톨러 스크립트 테스트:")
    update_windows_installer(TEST_VERSION)
    
    # .version 파일 업데이트 테스트
    print("\n2. .version 파일 테스트:")
    update_dot_version_file(TEST_VERSION)
    
    print("\n테스트 완료")

if __name__ == "__main__":
    main() 