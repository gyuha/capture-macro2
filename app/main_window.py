from PySide6.QtWidgets import QDialog, QMainWindow

from app.config.config import Config
from app.dialogs.setting_dialog import SettingDialog
from ui.main_window_ui import Ui_MainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.config = Config()

        self.pre_command_widget = None
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Connect signals to slots
        self.connect_signals_slots()
        self.set_macro()

    def connect_signals_slots(self):

        # Capture and control buttons
        self.ui.btnCapture.clicked.connect(self.on_capture)
        self.ui.btnStop.clicked.connect(self.on_stop)
        self.ui.btnStart.clicked.connect(self.on_start)

        # Menu actions
        self.ui.actionSettingDialog.triggered.connect(self.on_setting_dialog)
        self.ui.actionSave.triggered.connect(self.on_save)
        self.ui.actionExit_Q.triggered.connect(self.close)

    def set_macro(self):
        # 매크로 설정
        self.ui.pre_command_widget.ui.groupBox.setTitle("사전 수행")
        self.ui.command_widget.ui.groupBox.setTitle("수행")

        self.ui.pre_command_widget.set_macro(self, "pre_macro", self.config.pre_macro)
        self.ui.command_widget.set_macro(self, "macro", self.config.macro)

    def on_capture(self):
        # TODO: Implement capture logic
        pass

    def on_stop(self):
        # TODO: Implement stop logic
        pass

    def on_start(self):
        # TODO: Implement start logic
        pass

    def on_open(self):
        # TODO: Implement open file logic
        pass

    def on_save(self):
        self.config.save_to_file()
        self.ui.statusbar.showMessage("설정이 저장 되었습니다.", 2000)

    def on_setting_dialog(self):
        # 설정 다이얼로그
        dialog = SettingDialog(self.config)
        result = dialog.exec_()  # 다이얼로그 실행

        if result == QDialog.Accepted:
            self.config.save_to_file()
            print("Settings applied:", self.config)
        else:
            print("Settings dialog canceled")
