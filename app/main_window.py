from pynput import keyboard
from PySide6 import QtCore
from PySide6.QtCore import Slot
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QDialog, QMainWindow

from app.app_core import AppCore
from app.config.config import Config
from app.dialogs.setting_dialog import SettingDialog
from app.utils.action_controller import ActionController
from app.utils.file_util import create_directory_path
from ui.main_window_ui import Ui_MainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.config = Config()
        self.app_core = AppCore()

        self.pre_command_widget = None
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.action_controller = ActionController()

        # Connect signals to slots
        self.connect_signals_slots()
        self.set_macro()

        self.ui.btnStop.setDisabled(True)

        # 전역 단축키 설정
        self.hotkeys = keyboard.GlobalHotKeys(
            {"<f1>": self.handle_start, "<f2>": self.handle_stop}
        )
        self.hotkeys.start()

        self.lb_preview_width = 100

    def connect_signals_slots(self):
        self.ui.btnCapture.clicked.connect(self.handle_capture)
        self.ui.btnStop.clicked.connect(self.handle_stop)
        self.ui.btnStart.clicked.connect(self.handle_start)

        # Menu actions
        self.ui.actionSettingDialog.triggered.connect(self.handle_setting_dialog)
        self.ui.actionSave.triggered.connect(self.handle_save)
        self.ui.actionExit_Q.triggered.connect(self.close)

        # Action controller signals
        self.app_core.signal_macro_done.connect(self.on_action_controller_done)

        # Image preview singals
        self.app_core.signal_image_preview.connect(self.on_image_preview)
        self.app_core.signal_image_clear.connect(self.on_image_clear)

        self.ui.pre_command_widget.signal_update_config.connect(self.on_update_config)
        self.ui.command_widget.signal_update_config.connect(self.on_update_config)

    def set_macro(self):
        # 매크로 설정
        self.ui.pre_command_widget.ui.groupBox.setTitle("사전 수행")
        self.ui.command_widget.ui.groupBox.setTitle("수행")

        self.ui.pre_command_widget.set_macro(self, "pre_macro", self.config.pre_macro)
        self.ui.command_widget.set_macro(self, "macro", self.config.macro)

    def handle_capture(self):
        self.app_core.set_monitor()
        table = self.ui.command_widget.ui.macroTable
        for row in range(table.rowCount()):
            if table.cellWidget(row, 0).currentText() == "capture":
                self.action_controller.capture(table.item(row, 1).text().strip())

    def set_action_status(self, status: bool):
        self.app_core.is_running = status
        self.ui.command_widget.setDisabled(status)
        self.ui.pre_command_widget.setDisabled(status)
        self.ui.btnStart.setDisabled(status)
        self.ui.btnStop.setDisabled(not status)
        self.ui.btnCapture.setDisabled(status)
        self.ui.image_list_widget.ui.btnToPdf.setDisabled(status)
        self.ui.image_list_widget.ui.btnDeleteAllFiles.setDisabled(status)
        self.ui.image_list_widget.ui.btnDeleteFile.setDisabled(status)

    def handle_stop(self):
        # 매크로 중지
        print("📢 Stop")
        self.action_controller.stop()
        self.set_action_status(False)

    def handle_start(self):
        if self.app_core.is_running:
            return

        if not create_directory_path(self.config.capture_path):
            self.ui.statusbar.showMessage("캡처 경로를 확인해주세요.", 2000)
            return

        self.set_action_status(True)
        # 매크로 시작
        self.app_core.same_count = 0
        self.app_core.macro_type = "pre_macro"
        self.action_controller.config = self.config
        self.action_controller.action_macro = self.config.pre_macro
        self.action_controller.monitor_index = int(self.config.monitor)

        self.action_controller.start()

    @Slot()
    def on_action_controller_done(self):
        # Action controller done
        if self.app_core.macro_type == "pre_macro":
            self.app_core.macro_type = "macro"
            self.action_controller.action_macro = self.config.macro
            self.action_controller.start()
        else:
            self.handle_stop()

    @Slot(str, object)
    def on_update_config(self, config_type, config):
        if config_type == "pre_macro":
            self.config.pre_macro = config
        else:
            self.config.macro = config

    def on_hotkey_activated(self, key):
        self.hotkeys.hot_keys[key]()
        self.activateWindow()
        self.raise_()

    def handle_save(self):
        self.config.save_to_file()
        self.ui.statusbar.showMessage("설정이 저장 되었습니다.", 2000)

    def handle_setting_dialog(self):
        # 설정 다이얼로그
        dialog = SettingDialog(self.config)
        result = dialog.exec_()  # 다이얼로그 실행

        if result == QDialog.Accepted:
            self.config.save_to_file()
            print("Settings applied:", self.config)
        else:
            print("Settings dialog canceled")

    @Slot(str)
    def on_image_preview(self, image_path):
        pix = QPixmap()
        pix.load(image_path)
        pix = pix.scaledToWidth(
            self.lb_preview_width, QtCore.Qt.TransformationMode.SmoothTransformation
        )
        self.ui.lbPreview.setPixmap(pix)

    @Slot()
    def on_image_clear(self):
        self.ui.lbPreview.clear()

    def showEvent(self, event):
        super().showEvent(event)
        self.lb_preview_width = self.ui.lbPreview.width()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.lb_preview_width = self.ui.lbPreview.width()
