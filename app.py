import sys
from multiprocessing import freeze_support

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication

from app.main_window import MainWindow
from app.utils.macos_accessibility_checker import MacOSAccessibilityChecker
from app.utils.platform_util import is_macos

if __name__ == "__main__":
    freeze_support()

    app = QApplication(sys.argv)

    if is_macos():
        checker = MacOSAccessibilityChecker(app)
        if not checker.check_accessibility():
            exit(1)

    app_icon = QIcon("resources/icon.png")
    app.setWindowIcon(app_icon)

    window = MainWindow()
    window.show()
    sys.exit(app.exec())
