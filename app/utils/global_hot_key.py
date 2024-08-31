import sys

import keyboard
from PySide6.QtCore import QObject, Qt, QTimer, Signal
from PySide6.QtWidgets import QApplication, QLabel, QMainWindow


class GlobalHotKey(QObject):
    activated = Signal()

    def __init__(self, hot_key):
        super().__init__()
        self.hot_key = hot_key
        keyboard.add_hotkey(self.hot_key, self.on_activated)

    def on_activated(self):
        self.activated.emit()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cross-Platform Global Shortcut Example")
        self.setGeometry(100, 100, 400, 200)

        self.label = QLabel("Press Ctrl+Alt+H anywhere to say hello", self)
        self.label.setAlignment(Qt.AlignCenter)
        self.setCentralWidget(self.label)

        # 전역 단축키 설정
        self.hotkey = GlobalHotKey("ctrl+alt+h")
        self.hotkey.activated.connect(self.say_hello)

        self.hotkey = GlobalHotKey("ctrl+q")
        self.hotkey.activated.connect(self.close)

        # 주기적으로 이벤트 처리
        self.timer = QTimer(self)
        self.timer.timeout.connect(lambda: None)
        self.timer.start(100)

    def say_hello(self):
        self.label.setText("Hello! You pressed Ctrl+Alt+H")
        self.activateWindow()
        self.raise_()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
