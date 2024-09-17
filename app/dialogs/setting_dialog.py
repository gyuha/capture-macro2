import sys

from PySide6.QtGui import QIntValidator, QScreen
from PySide6.QtWidgets import QApplication, QDialog, QFileDialog

from app.app_core import AppCore
from app.config.config import Config
from ui.setting_dialog_ui import Ui_SettingDialog


class SettingDialog(QDialog):
    def __init__(self, config: Config):
        super(SettingDialog, self).__init__()
        self.app_core = AppCore()
        self.ui = Ui_SettingDialog()
        self.ui.setupUi(self)
        self.config = config

        # 초기 설정 값 로드
        self.load_settings()

        # 신호를 슬롯에 연결
        self.connect_signals_slots()
        self.populate_monitor_combo()


    def load_settings(self):
        # Config 객체의 값을 UI에 설정
        self.ui.cbMonitorNum.setCurrentIndex(self.config.monitor)
        self.ui.sbMaxPage.setValue(self.config.max_page)
        self.ui.sbImageCompress.setValue(self.config.image_quality)
        self.ui.sbSameCount.setValue(self.config.same_count)
        self.ui.lbSameCount.setText(f"{self.config.same_count}")
        self.ui.leImagePath.setText(self.config.capture_path)
        self.ui.lePdfPath.setText(self.config.pdf_path)
        self.ui.sbImageSize.setValue(self.config.image_size)

    def connect_signals_slots(self):
        self.ui.btnCancel.clicked.connect(self.cancel)
        self.ui.btnOk.clicked.connect(self.ok)
        self.ui.cbMonitorNum.currentIndexChanged.connect(self.on_monitor_changed)
        self.ui.sbSameCount.valueChanged.connect(lambda value: self.ui.lbSameCount.setText(str(value)))

        self.ui.btnImagePath.clicked.connect(self.select_path)
        self.ui.btnPdfPath.clicked.connect(self.select_pdf_path)


    def cancel(self):
        # 다이얼로그를 변경 없이 닫기
        self.close()

    def ok(self):
        # 변경된 설정을 Config 객체에 저장
        self.config.capture_path = self.ui.leImagePath.text()
        self.config.image_quality = self.ui.sbImageCompress.value()
        self.config.image_size = self.ui.sbImageSize.value()
        self.config.max_page = self.ui.sbMaxPage.value()
        self.config.monitor = self.ui.cbMonitorNum.currentIndex()
        self.config.pdf_path = self.ui.lePdfPath.text()
        self.config.same_count = self.ui.sbSameCount.value()

        # 다이얼로그 닫기
        self.accept()

    def select_path(self):
        initial_path = self.ui.leImagePath.text() or "/"
        path = QFileDialog.getExistingDirectory(self, "Select Directory", initial_path)
        self.ui.leImagePath.setText(path)

    def select_pdf_path(self):
        initial_path = self.ui.leImagePath.text() or "/"
        path = QFileDialog.getExistingDirectory(self, "Select Directory", initial_path)
        self.ui.lePdfPath.setText(path)

    def populate_monitor_combo(self):
        screens = QApplication.screens()
        for i, screen in enumerate(screens):
            screen_geometry = screen.geometry()
            model_name = self.get_monitor_model(screen, i)

            display_text = f"Monitor {i+1}: {model_name} ({screen_geometry.width()}x{screen_geometry.height()})"
            self.ui.cbMonitorNum.addItem(display_text, i)

    def get_monitor_model(self, screen, index):
        if self.app_core.is_mac:
            return self.get_macos_monitor_model(screen)
        elif self.app_core.is_windows:
            return self.get_windows_monitor_model(index)
        else:
            return "Unknown"

    def get_windows_monitor_model(self, index):
        try:
            import win32api

            monitor_info = win32api.EnumDisplayDevices(None, index, 0)
            return monitor_info.DeviceString
        except ImportError:
            return "Unknown (win32api not available)"

    def get_macos_monitor_model(self, screen):
        try:
            name = screen.name()
            manufacturer = screen.manufacturer()
            model = screen.model()
            serial_number = screen.serialNumber()

            print(f"Screen info - Name: {name}, Manufacturer: {manufacturer}, Model: {model}, Serial: {serial_number}")

            return f"{manufacturer} {model}" if manufacturer and model else name
        except Exception as e:
            print(f"Error getting macOS monitor info: {e}")
            return f"Monitor {screen.name()}"

    def on_monitor_changed(self, index):
        # 선택된 모니터의 인덱스와 텍스트를 가져옵니다
        selected_monitor_index = self.ui.cbMonitorNum.itemData(index)
        selected_monitor_text = self.ui.cbMonitorNum.itemText(index)

        print(f"Selected monitor changed: Index = {selected_monitor_index}, Text = {selected_monitor_text}")

