import sys

from PySide6.QtCore import QPoint, QRect, Qt, QTimer, Signal
from PySide6.QtGui import QColor, QCursor, QPainter, QPen
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget


class RectOverlay(QWidget):
    # Define a custom signal to send the rectangle data
    rectSelected = Signal(int, int, int, int)

    def __init__(self, screen_geometry):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.start_point = QPoint()
        self.end_point = QPoint()
        self.is_drawing = False
        self.setGeometry(screen_geometry)

        # Initialize cursor position to the current mouse position
        self.cursor_position = QCursor.pos() - self.pos()

        # Set up a timer to update the cursor position
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_cursor_position)
        self.timer.start(16)  # Update approximately every 16ms (~60 FPS)

    def update_cursor_position(self):
        self.cursor_position = QCursor.pos() - self.pos()
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Fill the entire screen with semi-transparent black
        painter.fillRect(self.rect(), QColor(0, 0, 0, 127))

        if self.is_drawing:
            # Calculate the rectangle being drawn
            rect = QRect(self.start_point, self.end_point).normalized()

            # Clear the rectangle area to make it transparent
            painter.setCompositionMode(QPainter.CompositionMode_Clear)
            painter.fillRect(rect, QColor(0, 0, 0, 0))

        # Draw crosshair lines
        painter.setCompositionMode(QPainter.CompositionMode_SourceOver)
        pen = QPen(Qt.red, 0.5, Qt.DashLine)
        painter.setPen(pen)
        painter.drawLine(
            0, self.cursor_position.y(), self.width(), self.cursor_position.y()
        )  # Horizontal line
        painter.drawLine(
            self.cursor_position.x(), 0, self.cursor_position.x(), self.height()
        )  # Vertical line

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.start_point = event.pos()
            self.end_point = self.start_point
            self.is_drawing = True
            self.update()

    def mouseMoveEvent(self, event):
        if self.is_drawing:
            self.end_point = event.pos()
        self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.is_drawing = False
            self.update()
            rect = QRect(self.start_point, self.end_point).normalized()
            # Emit the signal with the rectangle's data
            self.rectSelected.emit(rect.x(), rect.y(), rect.width(), rect.height())
            self.close()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Overlay Example")
        self.setGeometry(100, 100, 800, 600)

        self.button = QPushButton("Show Overlay on Monitor 1", self)
        self.button.setGeometry(50, 50, 200, 50)
        self.button.clicked.connect(lambda: self.show_overlay(0))

        self.button2 = QPushButton("Show Overlay on Monitor 2", self)
        self.button2.setGeometry(50, 120, 200, 50)
        self.button2.clicked.connect(lambda: self.show_overlay(1))

    def show_overlay(self, monitor_index):
        screens = QApplication.screens()
        if monitor_index < len(screens):
            screen_geometry = screens[monitor_index].geometry()
            self.overlay = RectOverlay(screen_geometry)
            # Connect the signal to a slot in MainWindow
            self.overlay.rectSelected.connect(self.handle_rect_selected)
            self.overlay.show()
        else:
            print(f"Monitor {monitor_index + 1} is not available.")

    def handle_rect_selected(self, x, y, width, height):
        print(f"Rectangle selected: x={x}, y={y}, width={width}, height={height}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
