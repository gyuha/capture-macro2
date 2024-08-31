import sys

from PySide6.QtCore import QPoint, QRect, Qt, QTimer, Signal, Slot
from PySide6.QtGui import QColor, QCursor, QPainter, QPen
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget


class RectOverlay(QWidget):
    rect_selected = Signal(int, int, int, int)

    def __init__(self, screen):
        super().__init__()
        self.screen = screen
        self.device_pixel_ratio = screen.devicePixelRatio()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.start_point = QPoint()
        self.end_point = QPoint()
        self.is_drawing = False
        self.setGeometry(screen.geometry())

        self.cursor_position = QCursor.pos() - self.pos()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_cursor_position)
        self.timer.start(16)

    def update_cursor_position(self):
        self.cursor_position = QCursor.pos() - self.pos()
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        painter.fillRect(self.rect(), QColor(0, 0, 0, 127))

        if self.is_drawing:
            rect = QRect(self.start_point, self.end_point).normalized()

            painter.setCompositionMode(QPainter.CompositionMode_Clear)
            painter.fillRect(rect, QColor(0, 0, 0, 0))

        painter.setCompositionMode(QPainter.CompositionMode_SourceOver)
        pen = QPen(Qt.red, 0.5, Qt.DashLine)
        painter.setPen(pen)
        painter.drawLine(
            0, self.cursor_position.y(), self.width(), self.cursor_position.y()
        )
        painter.drawLine(
            self.cursor_position.x(), 0, self.cursor_position.x(), self.height()
        )

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
            # Scale the rectangle coordinates
            scaled_rect = QRect(
                int(rect.x() * self.device_pixel_ratio),
                int(rect.y() * self.device_pixel_ratio),
                int(rect.width() * self.device_pixel_ratio),
                int(rect.height() * self.device_pixel_ratio),
            )
            self.rect_selected.emit(
                scaled_rect.x(),
                scaled_rect.y(),
                scaled_rect.width(),
                scaled_rect.height(),
            )
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
            screen = screens[monitor_index]
            self.overlay = RectOverlay(screen)
            self.overlay.rect_selected.connect(self.handle_rect_selected)
            self.overlay.show()
        else:
            print(f"Monitor {monitor_index + 1} is not available.")

    @Slot(int, int, int, int)
    def handle_rect_selected(self, x, y, width, height):
        print(f"Rectangle selected: x={x}, y={y}, width={width}, height={height}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
