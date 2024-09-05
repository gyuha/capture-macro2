import sys
import time

from pynput.mouse import Controller as MouseController
from pynput.mouse import Listener as MouseListener
from PySide6.QtWidgets import (
    QApplication,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mouse Example")
        self.setGeometry(100, 100, 800, 600)

        # 화면 설정 가져 오기
        self.screens = QApplication.screens()
        self.monitor = self.screens[0].geometry()
        self.device_pixel_ratio = 1

        # Create input fields and button
        self.x_input = QLineEdit(self)
        self.x_input.setPlaceholderText("Enter X coordinate")
        self.y_input = QLineEdit(self)
        self.y_input.setPlaceholderText("Enter Y coordinate")
        self.move_button = QPushButton("Move Mouse", self)
        self.move_button.clicked.connect(self.move_mouse_to_coordinates)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.x_input)
        layout.addWidget(self.y_input)
        layout.addWidget(self.move_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Initialize mouse controller
        self.mouse = MouseController()

        # Initialize mouse listener
        self.listener = MouseListener(
            on_move=self.on_move, on_click=self.on_click, on_scroll=self.on_scroll
        )
        self.listener.start()

    def on_move(self, x, y):
        print("Position : x:%s, y:%s" % (x, y))

    def on_click(self, x, y, button, pressed):
        print("Button: %s, Position: (%s, %s), Pressed: %s " % (button, x, y, pressed))

    def on_scroll(self, x, y, dx, dy):
        print("Scroll: (%s, %s) (%s, %s)." % (x, y, dx, dy))

    def move_mouse_to_coordinates(self):
        try:
            x = int(self.x_input.text())
            y = int(self.y_input.text())
            self.mouse.position = (x, y)
            time.sleep(0.5)  # 0.5초 대기
            self.mouse.click(MouseController.left, 1)  # 클릭 이벤트 발생
        except ValueError:
            print("Invalid input. Please enter valid integers for X and Y coordinates.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
