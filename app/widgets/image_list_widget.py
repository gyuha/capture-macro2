import glob
import io
import os
import re
from pathlib import Path

from PIL import Image
from PySide6.QtCore import Qt, QUrl, Slot
from PySide6.QtGui import QDesktopServices, QIcon, QImage, QPixmap
from PySide6.QtWidgets import (
    QFileDialog,
    QListWidgetItem,
    QMessageBox,
    QProgressDialog,
    QWidget,
)

from app.app_core import AppCore
from app.config.config import Config
from app.utils.file_util import remove_path_files
from app.utils.image_diff import ImageDiff
from app.utils.image_to_pdf_converter import ImageToPdfConverter
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

        self.image_to_pdf_converter = ImageToPdfConverter()

        self.load_capture_files()
        self.progress_dialog = None

        self.connect_signals_slots()

    def connect_signals_slots(self):
        self.ui.imageFiles.itemSelectionChanged.connect(
            self.handle_item_selection_changed
        )
        self.ui.btnDeleteAllFiles.clicked.connect(self.handle_delete_all_files)
        self.ui.btnDeleteFile.clicked.connect(self.handle_delete_file)
        self.ui.btnOpenFolder.clicked.connect(self.handle_open_folder)
        self.ui.btnToPdf.clicked.connect(self.handle_to_pdf)

        self.app_core.signal_add_image.connect(self.on_add_image)

        self.image_to_pdf_converter.signal_progress.connect(self.handle_progress)
        self.image_to_pdf_converter.signal_finished.connect(self.handle_finished)

    def handle_item_selection_changed(self):
        item = self.ui.imageFiles.selectedItems()
        if len(item) > 0:
            image_path = os.path.join(self.config.capture_path, item[0].text())
            self.app_core.signal_image_preview.emit(image_path)

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
                self.last_file_number()
                self.app_core.signal_image_clear.emit()
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
            item = self.ui.imageFiles.selectedItems()
            row = self.ui.imageFiles.currentRow()
            if len(item) > 0:
                os.remove(os.path.join(self.config.capture_path, item[0].text()))
                self.ui.imageFiles.takeItem(row)
            if self.ui.imageFiles.count() > row and row > 0:
                self.ui.imageFiles.setCurrentRow(row - 1)
            self.last_file_number()
            self.app_core.signal_image_clear.emit()
            self.handle_item_selection_changed()
        except Exception as e:
            print(e)

    # @Slot(str)
    def on_add_image(self, image_path: str):
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
        try:
            # or not (path.endswith(".jpg") and path.endswith(".png")):
            if os.path.isdir(image_path) or not image_path.lower().endswith(".jpg"):
                return
            picture = Image.open(image_path)
            picture.thumbnail((80, 80), Image.Resampling.NEAREST)

            icon = QIcon(self.pil2pixmap(picture))
            item = QListWidgetItem(os.path.basename(image_path), self.ui.imageFiles)
            item.setStatusTip(image_path)
            item.setIcon(icon)
            self.ui.lbImageNumber.setText(str(self.app_core.image_number))
        except Exception as e:  # pylint: disable=broad-exception-caught
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
        """
        마지막 파일 번호 가져오기
        """
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
        self.ui.lbImageNumber.setText(str(self.app_core.image_number))
        # self.leCurrentCount.setText(str(num))

    def handle_to_pdf(self):
        """
        이미지를 PDF로 변환
        """
        try:
            if self.app_core.is_windows:
                default_path = os.path.join(os.path.expanduser('~'), 'Desktop')
            else:  # macOS and other Unix-like systems
                default_path = os.path.join(os.path.expanduser('~/Desktop'))

            file_path, _ = QFileDialog.getSaveFileName(self, "Save file", default_path, "PDF Files (*.pdf)")
            if not file_path.endswith(".pdf"):
                file_path = file_path + ".pdf"

            self.progress_dialog = QProgressDialog(
                "Save to pdf", "Cancel", 0, 100, self
            )
            self.progress_dialog.setWindowTitle("Save to pdf")

            self.image_to_pdf_converter.setFile(self.config.capture_path, file_path)
            self.image_to_pdf_converter.start()

            self.progress_dialog.setWindowModality(Qt.WindowModal)
            self.progress_dialog.forceShow()

            print("PDF 생성 완료")
        except Exception as e:
            print(f"PDF 변환 중 오류 발생: {e}")

    @Slot(int)
    def handle_progress(self, value):
        if not self.progress_dialog.wasCanceled():
            self.progress_dialog.setValue(value)

    @Slot()
    def handle_finished(self):
        self.progress_dialog.close()
        print("PDF 생성 완료")
