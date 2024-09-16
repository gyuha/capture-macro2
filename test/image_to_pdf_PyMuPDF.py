import io
import logging
import os
import sys
from concurrent.futures import ProcessPoolExecutor, as_completed

import fitz  # PyMuPDF
from PIL import Image
from PySide6.QtCore import QSettings, Qt, QThread, Signal
from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QSlider,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")


def process_image(image_path, target_dpi=50, quality=65, max_size=1500):
    try:
        with Image.open(image_path) as img:
            original_size = os.path.getsize(image_path)

            # 이미지 크기 조정 (작은 이미지는 확대하지 않음)
            if img.width > max_size or img.height > max_size:
                img.thumbnail((max_size, max_size), Image.LANCZOS)

            # 항상 JPEG로 변환 (투명도가 있는 이미지는 제외)
            if img.mode in ("RGBA", "LA") or (img.mode == "P" and "transparency" in img.info):
                img_format = "PNG"
            else:
                img_format = "JPEG"
                if img.mode != "RGB":
                    img = img.convert("RGB")

            img_bytes = io.BytesIO()
            if img_format == "JPEG":
                img.save(img_bytes, format="JPEG", quality=quality, optimize=True, dpi=(target_dpi, target_dpi))
            else:
                img.save(img_bytes, format="PNG", optimize=True, dpi=(target_dpi, target_dpi))

            compressed_size = img_bytes.tell()
            img_bytes.seek(0)

            return img_bytes.getvalue(), original_size, compressed_size
    except Exception as e:
        logging.error(f"Error processing image {image_path}: {str(e)}")
        return None, 0, 0


class ConverterThread(QThread):
    progress = Signal(int)
    finished = Signal(bool, str)

    def __init__(self, image_folder, pdf_filename, ocr_enabled, quality, max_size):
        super().__init__()
        self.image_folder = image_folder
        self.pdf_filename = pdf_filename
        self.ocr_enabled = ocr_enabled
        self.quality = quality
        self.max_size = max_size

    def run(self):
        try:
            doc = fitz.open()
            image_files = [
                os.path.join(self.image_folder, f)
                for f in sorted(os.listdir(self.image_folder))
                if f.lower().endswith((".png", ".jpg", ".jpeg", ".tiff", ".bmp", ".gif"))
            ]
            total_images = len(image_files)
            total_original_size = 0
            total_compressed_size = 0

            with ProcessPoolExecutor() as executor:
                futures = [
                    executor.submit(process_image, image_path, 72, self.quality, self.max_size)
                    for image_path in image_files
                ]
                for idx, future in enumerate(as_completed(futures)):
                    img_data, original_size, compressed_size = future.result()
                    if img_data:
                        total_original_size += original_size
                        total_compressed_size += compressed_size

                        pix = fitz.Pixmap(img_data)
                        page = doc.new_page()
                        page.insert_image(page.rect, pixmap=pix)

                        progress_percent = int((idx + 1) / total_images * 100)
                        self.progress.emit(progress_percent)

            # 메타데이터 제거
            doc.set_metadata({})

            # PDF 저장 (메타데이터 없이)
            doc.save(self.pdf_filename, garbage=4, deflate=True, clean=True, pretty=False, linear=True)

            pdf_size = os.path.getsize(self.pdf_filename)
            doc.close()

            logging.debug(f"Total original size: {total_original_size / (1024*1024):.2f} MB")
            logging.debug(f"Total compressed size: {total_compressed_size / (1024*1024):.2f} MB")
            logging.debug(f"Final PDF size: {pdf_size / (1024*1024):.2f} MB")

            self.finished.emit(True, f"Conversion completed. PDF size: {pdf_size / (1024*1024):.2f} MB")
        except Exception as e:
            logging.error(f"An error occurred: {str(e)}", exc_info=True)
            self.finished.emit(False, f"An error occurred: {str(e)}")


class ImageToPDFApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Image to PDF Converter")
        self.settings = QSettings("YourCompany", "ImageToPDFConverter")
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.folder_label = QLabel("Image folder path:")
        self.folder_edit = QLineEdit()
        self.folder_button = QPushButton("Select Folder")
        self.folder_button.clicked.connect(self.select_folder)

        self.pdf_label = QLabel("Output PDF filename:")
        self.pdf_edit = QLineEdit()

        self.ocr_checkbox = QCheckBox("Enable OCR")

        # 압축 품질 슬라이더
        quality_layout = QHBoxLayout()
        self.quality_label = QLabel("JPEG Quality:")
        self.quality_slider = QSlider(Qt.Horizontal)
        self.quality_slider.setRange(1, 100)
        self.quality_slider.setValue(85)
        self.quality_value = QLabel("85")
        self.quality_slider.valueChanged.connect(self.update_quality_label)
        quality_layout.addWidget(self.quality_label)
        quality_layout.addWidget(self.quality_slider)
        quality_layout.addWidget(self.quality_value)

        # 최대 이미지 크기 입력
        size_layout = QHBoxLayout()
        self.size_label = QLabel("Max Image Size:")
        self.size_input = QSpinBox()
        self.size_input.setRange(100, 10000)
        self.size_input.setValue(2000)
        self.size_input.setSuffix(" px")
        size_layout.addWidget(self.size_label)
        size_layout.addWidget(self.size_input)

        self.convert_button = QPushButton("Start Conversion")
        self.convert_button.clicked.connect(self.start_conversion)

        self.progress_label = QLabel("Progress: 0%")

        layout.addWidget(self.folder_label)
        layout.addWidget(self.folder_edit)
        layout.addWidget(self.folder_button)
        layout.addWidget(self.pdf_label)
        layout.addWidget(self.pdf_edit)
        layout.addWidget(self.ocr_checkbox)
        layout.addLayout(quality_layout)
        layout.addLayout(size_layout)
        layout.addWidget(self.convert_button)
        layout.addWidget(self.progress_label)

        self.setLayout(layout)

        self.load_settings()

    def update_quality_label(self, value):
        self.quality_value.setText(str(value))

    def select_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Image Folder")
        if folder:
            self.folder_edit.setText(folder)

    def start_conversion(self):
        image_folder = self.folder_edit.text()
        pdf_filename = self.pdf_edit.text()
        ocr_enabled = self.ocr_checkbox.isChecked()
        quality = self.quality_slider.value()
        max_size = self.size_input.value()

        if not image_folder or not os.path.isdir(image_folder):
            QMessageBox.warning(self, "Error", "Please select a valid image folder.")
            return

        if not pdf_filename:
            QMessageBox.warning(self, "Error", "Please enter an output PDF filename.")
            return

        self.convert_button.setEnabled(False)

        self.save_settings()

        self.thread = ConverterThread(image_folder, pdf_filename, ocr_enabled, quality, max_size)
        self.thread.progress.connect(self.update_progress)
        self.thread.finished.connect(self.conversion_finished)
        self.thread.start()

    def update_progress(self, value):
        self.progress_label.setText(f"Progress: {value}%")

    def conversion_finished(self, success, message):
        self.convert_button.setEnabled(True)
        QMessageBox.information(self, "Notification", message)

    def load_settings(self):
        self.folder_edit.setText(self.settings.value("last_folder", ""))
        self.pdf_edit.setText(self.settings.value("last_pdf", ""))
        self.ocr_checkbox.setChecked(self.settings.value("ocr_enabled", False, type=bool))
        self.quality_slider.setValue(self.settings.value("jpeg_quality", 85, type=int))
        self.size_input.setValue(self.settings.value("max_image_size", 2000, type=int))

    def save_settings(self):
        self.settings.setValue("last_folder", self.folder_edit.text())
        self.settings.setValue("last_pdf", self.pdf_edit.text())
        self.settings.setValue("ocr_enabled", self.ocr_checkbox.isChecked())
        self.settings.setValue("jpeg_quality", self.quality_slider.value())
        self.settings.setValue("max_image_size", self.size_input.value())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageToPDFApp()
    window.show()
    sys.exit(app.exec())
