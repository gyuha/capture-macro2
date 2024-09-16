
import sys
import os
from PySide6.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout,
    QLabel, QLineEdit, QFileDialog, QCheckBox, QMessageBox
)
from PySide6.QtCore import Qt, QThread, Signal
import fitz  # PyMuPDF
from PIL import Image
import io

class ConverterThread(QThread):
    progress = Signal(int)
    finished = Signal(bool, str)

    def __init__(self, image_folder, pdf_filename, ocr_enabled):
        super().__init__()
        self.image_folder = image_folder
        self.pdf_filename = pdf_filename
        self.ocr_enabled = ocr_enabled

    def run(self):
        try:
            doc = fitz.open()
            image_files = [
                f for f in sorted(os.listdir(self.image_folder))
                if f.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif'))
            ]
            total_images = len(image_files)

            for idx, image_file in enumerate(image_files):
                image_path = os.path.join(self.image_folder, image_file)
                img = Image.open(image_path)
                
                # Convert image to RGB if it's not
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                
                # Compress image
                img_bytes = io.BytesIO()
                img.save(img_bytes, format='JPEG', quality=85, optimize=True)
                img_bytes.seek(0)
                
                # Insert compressed image
                img_xref = doc.add_file_annot(img_bytes, filename=image_file)
                page = doc.new_page()
                page.insert_image(page.rect, stream=img_xref)

                progress_percent = int((idx + 1) / total_images * 100)
                self.progress.emit(progress_percent)

            # Optimize PDF
            doc.save(self.pdf_filename, garbage=4, deflate=True, clean=True)
            doc.close()
            self.finished.emit(True, "Conversion completed successfully.")
        except Exception as e:
            self.finished.emit(False, f"An error occurred: {str(e)}")

class ImageToPDFApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Image to PDF Converter")
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

        self.convert_button = QPushButton("Start Conversion")
        self.convert_button.clicked.connect(self.start_conversion)

        self.progress_label = QLabel("Progress: 0%")

        layout.addWidget(self.folder_label)
        layout.addWidget(self.folder_edit)
        layout.addWidget(self.folder_button)
        layout.addWidget(self.pdf_label)
        layout.addWidget(self.pdf_edit)
        layout.addWidget(self.ocr_checkbox)
        layout.addWidget(self.convert_button)
        layout.addWidget(self.progress_label)

        self.setLayout(layout)

    def select_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Image Folder")
        if folder:
            self.folder_edit.setText(folder)

    def start_conversion(self):
        image_folder = self.folder_edit.text()
        pdf_filename = self.pdf_edit.text()
        ocr_enabled = self.ocr_checkbox.isChecked()

        if not image_folder or not os.path.isdir(image_folder):
            QMessageBox.warning(self, "Error", "Please select a valid image folder.")
            return

        if not pdf_filename:
            QMessageBox.warning(self, "Error", "Please enter an output PDF filename.")
            return

        self.convert_button.setEnabled(False)

        self.thread = ConverterThread(image_folder, pdf_filename, ocr_enabled)
        self.thread.progress.connect(self.update_progress)
        self.thread.finished.connect(self.conversion_finished)
        self.thread.start()

    def update_progress(self, value):
        self.progress_label.setText(f"Progress: {value}%")

    def conversion_finished(self, success, message):
        self.convert_button.setEnabled(True)
        QMessageBox.information(self, "Notification", message)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageToPDFApp()
    window.show()
    sys.exit(app.exec())
