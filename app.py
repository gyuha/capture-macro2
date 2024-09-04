import sys
from PySide6.QtWidgets import QApplication
from app.main_window import MainWindow
from multiprocessing import freeze_support
from PySide6.QtGui import QIcon

import qdarktheme

if __name__ == "__main__":
    freeze_support()

    qdarktheme.enable_hi_dpi()
    app = QApplication(sys.argv)
    qdarktheme.setup_theme("auto")

    app_icon = QIcon("resources/icon.png")
    app.setWindowIcon(app_icon)

    window = MainWindow()
    window.show()
    sys.exit(app.exec())
