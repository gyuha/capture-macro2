import random

import sys

from PySide6.QtCore import QPoint, QRect, Qt, QTimer, Signal, Slot
from PySide6.QtGui import QColor, QCursor, QPainter, QPen
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget

from pynput.keyboard import Controller as KeyboardController
from pynput.mouse import Button
from pynput.mouse import Controller as MouseController

from PySide6.QtWidgets import QLineEdit, QVBoxLayout


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

    def move_mouse_to_coordinates(self):
        try:
            x = int(self.x_input.text())
            y = int(self.y_input.text())
            self.mouse.position = (x, y)
        except ValueError:
            print("Invalid input. Please enter valid integers for X and Y coordinates.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
