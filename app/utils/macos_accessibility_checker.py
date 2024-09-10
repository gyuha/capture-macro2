import sys
import subprocess
from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtCore import QTimer


class MacOSAccessibilityChecker:
    def __init__(self, app):
        self.app = app
        self.check_count = 0
        self.max_checks = 3  # 최대 확인 횟수

    def check_accessibility(self):
        # 손쉬운 사용 권한 확인
        result = subprocess.run(
            ["tccutil", "get", "com.apple.security.automation.apple-events"], capture_output=True, text=True
        )

        if "denied" in result.stdout.lower():
            self.show_accessibility_dialog()
        else:
            print("손쉬운 사용 권한이 허용되어 있습니다.")
            return True
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
        QTimer.singleShot(3000, self.recheck_accessibility)  # 3초 후 재확인

    def recheck_accessibility(self):
        self.check_count += 1
        if self.check_accessibility():
            print("손쉬운 사용 권한이 성공적으로 부여되었습니다.")
            # 여기에 앱의 메인 로직을 시작하는 코드를 추가할 수 있습니다.
        elif self.check_count < self.max_checks:
            print(f"손쉬운 사용 권한 확인 실패. 재시도 {self.check_count}/{self.max_checks}")
            QTimer.singleShot(3000, self.recheck_accessibility)  # 3초 후 다시 확인
        else:
            print("최대 확인 횟수를 초과했습니다. 앱을 종료합니다.")
            self.terminate_app()

    def terminate_app(self):
        print("앱을 종료합니다.")
        self.app.quit()


import sys
import subprocess
from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtCore import QTimer


class MacOSAccessibilityChecker:
    def __init__(self, app):
        self.app = app
        self.check_count = 0
        self.max_checks = 3  # 최대 확인 횟수

    def check_accessibility(self):
        # 손쉬운 사용 권한 확인
        result = subprocess.run(
            ["tccutil", "get", "com.apple.security.automation.apple-events"], capture_output=True, text=True
        )

        if "denied" in result.stdout.lower():
            self.show_accessibility_dialog()
        else:
            print("손쉬운 사용 권한이 허용되어 있습니다.")
            return True
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
        QTimer.singleShot(3000, self.recheck_accessibility)  # 3초 후 재확인

    def recheck_accessibility(self):
        self.check_count += 1
        if self.check_accessibility():
            print("손쉬운 사용 권한이 성공적으로 부여되었습니다.")
            # 여기에 앱의 메인 로직을 시작하는 코드를 추가할 수 있습니다.
        elif self.check_count < self.max_checks:
            print(f"손쉬운 사용 권한 확인 실패. 재시도 {self.check_count}/{self.max_checks}")
            QTimer.singleShot(3000, self.recheck_accessibility)  # 3초 후 다시 확인
        else:
            print("최대 확인 횟수를 초과했습니다. 앱을 종료합니다.")
            self.terminate_app()

    def terminate_app(self):
        print("앱을 종료합니다.")
        self.app.quit()


# 사용 예시
if __name__ == "__main__":
    app = QApplication(sys.argv)

    checker = MacOSAccessibilityChecker(app)
    if not checker.check_accessibility():
        # 초기 체크에 실패하면 앱이 계속 실행되며, 사용자에게 권한 설정 기회를 줍니다.
        # 이후의 프로세스는 recheck_accessibility에서 처리됩니다.
        pass
    else:
        # 권한이 이미 있는 경우, 여기에 앱의 메인 로직을 시작하는 코드를 추가하세요.
        pass

    sys.exit(app.exec())
