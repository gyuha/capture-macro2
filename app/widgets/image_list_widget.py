import glob
import os

from PySide6.QtCore import QUrl
from PySide6.QtGui import QDesktopServices

from PySide6.QtWidgets import QWidget, QMessageBox

from app.app_core import AppCore
from app.config.config import Config
from app.utils.file_util import remove_path_files
from ui.image_list_widget_ui import Ui_ImageListWidget


class ImageListWidget(QWidget):
    """
    이미지 리스트 위젯
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.app_core = AppCore()
        self.config = Config()

        self.ui = Ui_ImageListWidget()
        self.ui.setupUi(self)
        self.connect_signals_slots()

    def connect_signals_slots(self):
        self.ui.imageFiles.itemSelectionChanged.connect(self.handle_item_selection_changed)
        self.ui.btnDeleteAllFiles.clicked.connect(self.handle_delete_all_files)
        self.ui.btnDeleteFile.clicked.connect(self.handle_delete_file)
        self.ui.btnOpenFolder.clicked.connect(self.handle_open_folder)


    def handle_item_selection_changed(self):
        pass
        # item = self.lsFiles.selectedItems()
        # if len(item) > 0:
        #     path = os.path.join(self.core.capturePath, item[0].text())
        #     # self.previewDisplay(path)

    def handle_delete_all_files(self):
        """
        전체 파일 삭제
        """
        ret = QMessageBox.question(
            self,
            "경고",
            "정말 모든 파일을 지우시겠습니까?",
            QMessageBox.StandardButton.No | QMessageBox.StandardButton.Yes,
            QMessageBox.StandardButton.Yes,
        )

        if ret == QMessageBox.StandardButton.Yes:
            try:
                for file_ext in ["*.png", "*.jpg"]:
                    path = os.path.join(self.config.capture_path, file_ext)
                    files = glob.glob(path)
                    remove_path_files(files)

                self.ui.imageFiles.clear()
                # self.label_preview.clear()
                self.start_file_number()
            except Exception as e:
                print(f"파일 삭제 중 오류 발생: {e}")

    def handle_open_folder(self):
        """
         탐색기에서 config.capture_path 폴더 열기
         """
        try:
            # 상대 경로를 절대 경로로 변환
            abs_path = os.path.abspath(self.config.capture_path)

            # 경로가 존재하는지 확인
            if not os.path.exists(abs_path):
                print(f"경로가 존재하지 않습니다: {abs_path}")
                return

            folder_path = QUrl.fromLocalFile(abs_path)
            if QDesktopServices.openUrl(folder_path):
                print(f"폴더가 성공적으로 열렸습니다: {abs_path}")
            else:
                print(f"폴더를 열 수 없습니다: {abs_path}")
        except Exception as e:
            print(f"폴더를 여는 중 오류 발생: {e}")

    def handle_delete_file(self):
        """
        선택된 파일 삭제
        """
        try:
            item = self.lsFiles.selectedItems()
            row = self.lsFiles.currentRow()
            if len(item) > 0:
                os.remove(os.path.join(self.Config, item[0].text()))
                self.lsFiles.takeItem(row)
        except Exception as e:
            print(e)

    def add_image(self, path):
        self.ui.imageFiles.addItem(path)
