from PySide6.QtWidgets import QWidget

from ui.command_widget_ui import Ui_CommandWidget


class CommandWidget(QWidget):
    def __init__(self, title="수행", parent=None):
        super().__init__(parent)
        self.ui = Ui_CommandWidget()
        self.ui.setupUi(self)
        self.connect_signals_slots()

    def connect_signals_slots(self):
        # Config buttons
        self.ui.btnConfigInsert.clicked.connect(self.on_config_insert)
        self.ui.btnConfigAdd.clicked.connect(self.on_config_add)
        self.ui.btnConfigRemove.clicked.connect(self.on_config_remove)

    def on_config_insert(self):
        # TODO: Implement config insert logic
        print("Config insert")
        pass

    def on_config_add(self):
        # TODO: Implement config add logic
        pass

    def on_config_remove(self):
        # TODO: Implement config remove logic
        pass
