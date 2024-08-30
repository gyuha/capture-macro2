import sys

from PySide6.QtCore import QRect, Qt
from PySide6.QtGui import QColor, QPainter
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget


class RectCheckOverlay(QWidget):
    def __init__(self, screen_geometry):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setGeometry(screen_geometry)
        self.rect_to_display = None  # Store the rectangle to display

    def display_rectangle(self, x, y, width, height):
        # Set the rectangle to display
        self.rect_to_display = QRect(x, y, width, height)
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Fill the entire screen with semi-transparent black
        painter.fillRect(self.rect(), QColor(0, 0, 0, 127))

        if self.rect_to_display:
            # Clear the rectangle area to make it transparent
            painter.setCompositionMode(QPainter.CompositionMode_Clear)
            painter.fillRect(self.rect_to_display, QColor(0, 0, 0, 0))


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Overlay Example")
        self.setGeometry(100, 100, 800, 600)

        self.button = QPushButton("Show Overlay on Monitor 1", self)
        self.button.setGeometry(50, 50, 200, 50)
        self.button.pressed.connect(lambda: self.show_overlay(0))
        self.button.released.connect(self.hide_overlay)

        self.button2 = QPushButton("Show Overlay on Monitor 2", self)
        self.button2.setGeometry(50, 120, 200, 50)
        self.button2.pressed.connect(lambda: self.show_overlay(1))
        self.button2.released.connect(self.hide_overlay)

    def show_overlay(self, monitor_index):
        screens = QApplication.screens()
        if monitor_index < len(screens):
            screen_geometry = screens[monitor_index].geometry()
            self.overlay = RectCheckOverlay(screen_geometry)
            self.overlay.show()
            # Display a rectangle at a specific location
            self.overlay.display_rectangle(100, 100, 300, 200)
        else:
            print(f"Monitor {monitor_index + 1} is not available.")

    def hide_overlay(self):
        if hasattr(self, "overlay") and self.overlay.isVisible():
            self.overlay.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
