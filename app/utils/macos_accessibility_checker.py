import ctypes
import ctypes.util
import subprocess
import sys

from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QApplication, QMessageBox


def _ax_is_process_trusted() -> bool:
    try:
        lib_path = ctypes.util.find_library("ApplicationServices")
        if not lib_path:
            return False
        lib = ctypes.cdll.LoadLibrary(lib_path)
        return bool(lib.AXIsProcessTrusted())
    except Exception:
        return False


class MacOSAccessibilityChecker:
    def __init__(self, app):
        self.app = app
        self.check_count = 0
        self.max_checks = 3

    def check_accessibility(self):
        if _ax_is_process_trusted():
            print("손쉬운 사용 권한이 허용되어 있습니다.")
            return True
        self.show_accessibility_dialog()
        return False

    def show_accessibility_dialog(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("이 앱은 '손쉬운 사용' 권한이 필요합니다.")
        msg.setInformativeText(
            "시스템 환경설정 > 보안 및 개인 정보 보호 > 개인 정보 보호 > 손쉬운 사용에서 이 앱을 추가해주세요."
        )
        msg.setWindowTitle("손쉬운 사용 권한 필요")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        result = msg.exec()

        if result == QMessageBox.Ok:
            self.open_accessibility_settings()
        else:
            print("사용자가 손쉬운 사용 설정을 취소했습니다.")
            self.terminate_app()

    def open_accessibility_settings(self):
        subprocess.run(["open", "x-apple.systempreferences:com.apple.preference.security?Privacy_Accessibility"])
        QTimer.singleShot(3000, self.recheck_accessibility)

    def recheck_accessibility(self):
        self.check_count += 1
        if self.check_accessibility():
            print("손쉬운 사용 권한이 성공적으로 부여되었습니다.")
        elif self.check_count < self.max_checks:
            print(f"손쉬운 사용 권한 확인 실패. 재시도 {self.check_count}/{self.max_checks}")
            QTimer.singleShot(3000, self.recheck_accessibility)
        else:
            print("최대 확인 횟수를 초과했습니다. 앱을 종료합니다.")
            self.terminate_app()

    def terminate_app(self):
        print("앱을 종료합니다.")
        self.app.quit()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    checker = MacOSAccessibilityChecker(app)
    if not checker.check_accessibility():
        pass
    else:
        pass

    sys.exit(app.exec())
