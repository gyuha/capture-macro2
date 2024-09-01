import glob
import os

from PySide6.QtWidgets import QWidget, QMessageBox

from app.utils.file_util import removePathFiles
from ui.image_list_widget_ui import Ui_ImageListWidget


class ImageListWidget(QWidget):
    """
    이미지 리스트 위젯
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_ImageListWidget()
        self.ui.setupUi(self)
        self.connect_signals_slots()

    def connect_signals_slots(self):
        self.ui.imageFiles.itemSelectionChanged.connect(self.on_item_selection_changed)
        self.ui.btnDeleteAllFiles.clicked.connect(self.on_delete_all_files)
        self.ui.btnDeleteFile.clicked.connect(self.on_delete_file)

    def on_item_selection_changed(self):
        pass
        # item = self.lsFiles.selectedItems()
        # if len(item) > 0:
        #     path = os.path.join(self.core.capturePath, item[0].text())
        #     # self.previewDisplay(path)

    def on_delete_all_files(self):
        """
        전체 파일 삭제
        """
        ret = QMessageBox.question(
            self,
            "경고",
            "정말 모든 파일을 지우시겠습니까?",
            QMessageBox.No | QMessageBox.Yes,
            QMessageBox.Yes,
            )

        if ret == QMessageBox.Yes:
            try:
                for file in ["*.png", "*.jpg"]:
                    path = os.path.join(self.config.capture_path, file)
                    files = glob.glob(path)
                    removePathFiles(files)
                self.lsFiles.clear()
                self.lbPreview.clear()
                self.startFileNumber()
            except Exception as e:
                print(e)

    def on_delete_file(self):
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
