from PySide6.QtWidgets import QDialog

from app.config.config import Config
from ui.setting_dialog_ui import Ui_SettingDialog


class SettingDialog(QDialog):
    def __init__(self, config: Config):
        super(SettingDialog, self).__init__()
        self.ui = Ui_SettingDialog()
        self.ui.setupUi(self)
        self.config = config

        # 초기 설정 값 로드
        self.load_settings()

        # 신호를 슬롯에 연결
        self.connect_signals_slots()

    def load_settings(self):
        # Config 객체의 값을 UI에 설정
        self.ui.leMonitorNum.setText(str(self.config.monitor))
        self.ui.leSameCount.setText(str(self.config.same_count))
        self.ui.leMaxPage.setText(str(self.config.max_page))
        self.ui.leImageCompress.setText(str(self.config.image_quality))
        self.ui.leImagePath.setText(self.config.capture_path)

    def connect_signals_slots(self):
        self.ui.btnCancel.clicked.connect(self.cancel)
        self.ui.btnOk.clicked.connect(self.ok)

    def cancel(self):
        # 다이얼로그를 변경 없이 닫기
        self.close()

    def ok(self):
        # 변경된 설정을 Config 객체에 저장
        self.config.monitor = int(self.ui.leMonitorNum.text())
        self.config.same_count = int(self.ui.leSameCount.text())
        self.config.max_page = int(self.ui.leMaxPage.text())
        self.config.image_quality = int(self.ui.leImageCompress.text())
        self.config.capture_path = self.ui.leImagePath.text()

        # 다이얼로그 닫기
        self.accept()
