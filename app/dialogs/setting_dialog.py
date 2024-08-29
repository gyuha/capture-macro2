from PySide6.QtWidgets import QDialog

from app.config.config import Config
from ui.setting_dialog_ui import Ui_SettingDialog


class SettingDialog(QDialog):
    def __init__(self, config: Config):
        super(SettingDialog, self).__init__()
        self.ui = Ui_SettingDialog()
        self.ui.setupUi(self)

        print(config.capture_path)

        # Connect signals to slots
        self.connect_signals_slots()

    def connect_signals_slots(self):
        self.ui.btnCancel.clicked.connect(self.cancel)
        self.ui.btnOk.clicked.connect(self.ok)

    def cancel(self):
        self.close()

    def ok(self):
        self.close()
