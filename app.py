import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from src.main_window_ui import Ui_MainWindow  # main_window_ui.py 파일에서 Ui_MainWindow 클래스를 임포트


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
