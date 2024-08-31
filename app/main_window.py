from PySide6.QtCore import Slot
from PySide6.QtWidgets import QDialog, QMainWindow

from app.config.config import Config
from app.dialogs.setting_dialog import SettingDialog
from app.utils.action_controller import ActionController
from ui.main_window_ui import Ui_MainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.config = Config()

        self.pre_command_widget = None
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.action_controller = ActionController()

        # Connect signals to slots
        self.connect_signals_slots()
        self.set_macro()

        self.ui.btnStop.setDisabled(True)

        self.image_number = 0

    def connect_signals_slots(self):

        # Capture and control buttons
        self.ui.btnCapture.clicked.connect(self.on_capture)
        self.ui.btnStop.clicked.connect(self.on_stop)
        self.ui.btnStart.clicked.connect(self.on_start)

        # Menu actions
        self.ui.actionSettingDialog.triggered.connect(self.on_setting_dialog)
        self.ui.actionSave.triggered.connect(self.on_save)
        self.ui.actionExit_Q.triggered.connect(self.close)

        self.action_controller.signal_done.connect(self.on_action_controller_done)
        self.action_controller.signal_add_image.connect(
            self.on_action_controller_add_image
        )

        self.ui.pre_command_widget.signal_update_config.connect(self.on_update_config)
        self.ui.command_widget.signal_update_config.connect(self.on_update_config)

    def set_macro(self):
        # 매크로 설정
        self.ui.pre_command_widget.ui.groupBox.setTitle("사전 수행")
        self.ui.command_widget.ui.groupBox.setTitle("수행")

        self.ui.pre_command_widget.set_macro(self, "pre_macro", self.config.pre_macro)
        self.ui.command_widget.set_macro(self, "macro", self.config.macro)

    def on_capture(self):
        # TODO: Implement capture logic
        pass

    def set_action_status(self, status: bool):
        self.action_controller.is_running = status
        self.ui.command_widget.setDisabled(status)
        self.ui.pre_command_widget.setDisabled(status)
        self.ui.btnStart.setDisabled(status)
        self.ui.btnStop.setDisabled(not status)
        self.ui.btnCapture.setDisabled(status)
        self.ui.image_list_widget.ui.btnToPdf.setDisabled(status)
        self.ui.image_list_widget.ui.btnDeleteAllFiles.setDisabled(status)
        self.ui.image_list_widget.ui.btnDeleteFile.setDisabled(status)

    def on_stop(self):
        # 매크로 중지
        self.set_action_status(False)

    def on_start(self):
        self.set_action_status(True)
        # 매크로 시작
        self.action_controller.action_type = "pre_macro"
        self.action_controller.config = self.config
        self.action_controller.action_macro = self.config.pre_macro
        self.action_controller.monitor_index = int(self.config.monitor)

        self.action_controller.start()

    @Slot()
    def on_action_controller_done(self):
        # Action controller done
        if self.action_controller.action_type == "pre_macro":
            self.action_controller.action_type = "macro"
            self.action_controller.action_macro = self.config.macro
            self.action_controller.start()
        else:
            self.on_stop()
            self.action_controller.stop()

    @Slot(int, str)
    def on_action_controller_add_image(self, image_number, image_name):
        # Add image to the list
        self.image_number = image_number
        print("Adding image:", image_number)
        print("Adding image:", image_name)

    @Slot(int)
    def on_action_controller_current_row(self, row):
        if self.action_controller.action_type == "pre_macro":
            self.ui.pre_command_widget.ui.macroTable.selectRow(row)
        else:
            self.ui.command_widget.ui.macroTable.selectRow(row)

    @Slot(str, object)
    def on_update_config(self, config_type, config):
        if config_type == "pre_macro":
            self.config.pre_macro = config
        else:
            self.config.macro = config

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
            print("Settings dialog canceled")
            print("Settings dialog canceled")
