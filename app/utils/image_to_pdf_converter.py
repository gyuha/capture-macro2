import os

from PIL import Image
from PySide6.QtCore import QThread, Signal
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


class ImageToPdfConverter(QThread):
    progress = Signal(int)
    finished = Signal()

    def __init__(self, image_folder, output_pdf):
        super().__init__()
        self.image_folder = image_folder
        self.output_pdf = output_pdf

    def run(self):
        image_files = [
            f
            for f in os.listdir(self.image_folder)
            if f.endswith(("png", "jpg", "jpeg"))
        ]
        image_files.sort()

        c = canvas.Canvas(self.output_pdf, pagesize=letter)
        width, height = letter

        total_images = len(image_files)
        for i, image_file in enumerate(image_files):
            image_path = os.path.join(self.image_folder, image_file)
            img = Image.open(image_path)

            img_width, img_height = img.size
            aspect = img_height / float(img_width)
            img = img.resize(
                (int(width), int(width * aspect)), Image.Resampling.LANCZOS
            )

            c.drawImage(
                image_path, 0, height - img.height, width=img.width, height=img.height
            )
            c.showPage()

            # 진행 상태 업데이트
            self.progress.emit(int((i + 1) / total_images * 100))

        c.save()
        self.finished.emit()


if __name__ == "__main__":
    input_image_folder = "images"
    output_pdf_file = "output.pdf"

    converter = ImageToPdfConverter(input_image_folder, output_pdf_file)
    converter.start()
    converter.wait()
    print("PDF 생성 완료")
