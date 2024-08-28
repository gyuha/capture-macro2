from PySide6.QtWidgets import QWidget

from ui.image_list_widget_ui import Ui_ImageListWidget


class ImageListWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_ImageListWidget()
        self.ui.setupUi(self)
        self.connect_signals_slots()

    def connect_signals_slots(self):
        pass
