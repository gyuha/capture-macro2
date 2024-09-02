import glob
import io
import os
import re
from pathlib import Path

from PIL import Image
from PySide6.QtCore import QUrl, Slot
from PySide6.QtGui import QDesktopServices, QIcon, QImage, QPixmap
from PySide6.QtWidgets import QListWidgetItem, QMessageBox, QWidget

from app.app_core import AppCore
from app.config.config import Config
from app.utils.file_util import remove_path_files
from app.utils.image_diff import ImageDiff
from ui.image_list_widget_ui import Ui_ImageListWidget


class ImageListWidget(QWidget):
    """
    이미지 리스트 위젯
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.app_core = AppCore()
        self.config = Config()

        self.image_diff = ImageDiff()

        self.ui = Ui_ImageListWidget()
        self.ui.setupUi(self)
        self.connect_signals_slots()

        self.load_capture_files()

    def connect_signals_slots(self):
        self.ui.imageFiles.itemSelectionChanged.connect(
            self.handle_item_selection_changed
        )
        self.ui.btnDeleteAllFiles.clicked.connect(self.handle_delete_all_files)
        self.ui.btnDeleteFile.clicked.connect(self.handle_delete_file)
        self.ui.btnOpenFolder.clicked.connect(self.handle_open_folder)

        self.app_core.signal_add_image.connect(self.on_add_image)

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

    @Slot(str)
    def on_add_image(self, image_path):
        print("📢[image_list_widget.py:110]: ", image_path)
        self.add_image_item(image_path)
        self.last_file_select()
        if self.image_diff.diff(image_path):
            self.app_core.same_count += 1
            if self.app_core.same_count >= self.config.same_count:
                self.app_core.signal_macro_done.emit()
                # for i in range(self.config.same_count):
                #     self.clickDeleteSelectFile()
                #     self.lastLsFileSelect()
        else:
            self.app_core.same_count = 0

    def pil2pixmap(self, image):
        bytesImg = io.BytesIO()
        image.save(bytesImg, format="JPEG")

        qImg = QImage()
        qImg.loadFromData(bytesImg.getvalue())

        return QPixmap.fromImage(qImg)

    def add_image_item(self, image_path):
        print("📢[image_list_widget.py:106]: ", image_path)
        # self.ui.imageFiles.addItem(path)
        try:
            # or not (path.endswith(".jpg") and path.endswith(".png")):
            if os.path.isdir(image_path) or not (image_path.endswith(".jpg")):
                return
            picture = Image.open(image_path)
            picture.thumbnail((80, 120), Image.Resampling.NEAREST)

            icon = QIcon(self.pil2pixmap(picture))
            item = QListWidgetItem(os.path.basename(image_path), self.ui.imageFiles)
            item.setStatusTip(image_path)
            item.setIcon(icon)
        except Exception as e:
            print(e)

    def last_file_select(self):
        self.ui.imageFiles.setCurrentRow(self.ui.imageFiles.count() - 1)

    def load_capture_files(self):
        self.ui.imageFiles.clear()
        Path(self.config.capture_path).mkdir(parents=True, exist_ok=True)
        files = os.listdir(self.config.capture_path)
        for file in files:
            path = os.path.join(self.config.capture_path, file)
            self.add_image_item(path)
        self.last_file_number()

    def last_file_number(self):
        files = os.listdir(self.config.capture_path)
        p = re.compile(r"^\d+.jpg$")
        files = [s for s in files if p.match(s)]
        if len(files) == 0:
            self.app_core.image_number = 0
            return
        basename = os.path.basename(files[-1])
        num = int(os.path.splitext(basename)[0])
        self.app_core.image_number = num
        self.app_core.image_number += 1
        print("📢[image_list_widget.py:177]: ", self.app_core.image_number)
        # self.leCurrentCount.setText(str(num))
