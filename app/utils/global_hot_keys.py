import sys

import keyboard
from PySide6.QtCore import QObject, Qt, QTimer, Signal
from PySide6.QtWidgets import QApplication, QLabel, QMainWindow, QVBoxLayout, QWidget


class GlobalHotKeys(QObject):
    activated = Signal(str)

    def __init__(self, hot_keys):
        super().__init__()
        self.hot_keys = hot_keys
        for key, _ in self.hot_keys.items():
            keyboard.add_hotkey(key, self.on_activated, args=(key,))

    def on_activated(self, key):
        self.activated.emit(key)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Multiple Global Shortcuts Example")
        self.setGeometry(100, 100, 400, 300)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        self.label = QLabel(
            "Press any of the following shortcuts:\n"
            "Ctrl+Alt+H: Say Hello\n"
            "Ctrl+Alt+W: Say Welcome\n"
            "Ctrl+Alt+Q: Quit Application"
        )
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)

        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.status_label)

        # 여러 전역 단축키 설정
        self.hotkeys = GlobalHotKeys(
            {
                "ctrl+alt+h": self.say_hello,
                "ctrl+alt+w": self.say_welcome,
                "ctrl+alt+q": self.quit_app,
            }
        )
        self.hotkeys.activated.connect(self.on_hotkey_activated)

        # 주기적으로 이벤트 처리
        self.timer = QTimer(self)
        self.timer.timeout.connect(lambda: None)
        self.timer.start(100)

    def on_hotkey_activated(self, key):
        self.hotkeys.hot_keys[key]()
        self.activateWindow()
        self.raise_()

    def say_hello(self):
        self.status_label.setText("Hello! You pressed Ctrl+Alt+H")

    def say_welcome(self):
        self.status_label.setText("Welcome! You pressed Ctrl+Alt+W")

    def quit_app(self):
        self.status_label.setText("Quitting application...")
        QTimer.singleShot(1000, QApplication.instance().quit)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
    window.show()
    sys.exit(app.exec())
