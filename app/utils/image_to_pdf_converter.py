import os

from PIL import Image
from PySide6.QtCore import QThread, Signal
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas


class ImageToPdfConverter(QThread):
    signal_progress = Signal(int)
    signal_finished = Signal()

    def __init__(self):
        super().__init__()
        self.image_folder = ""
        self.output_pdf = ""

    def setFile(self, image_folder, output_pdf):
        self.image_folder = image_folder
        self.output_pdf = output_pdf

    def run(self):
        image_files = [
            f
            for f in os.listdir(self.image_folder)
            if f.lower().endswith(("png", "jpg", "jpeg"))
        ]
        image_files.sort()

        c = canvas.Canvas(self.output_pdf)
        total_images = len(image_files)

        for i, image_file in enumerate(image_files):
            image_path = os.path.join(self.image_folder, image_file)
            img = Image.open(image_path)

            # 이미지 크기를 인치 단위로 변환 (72 DPI 기준)
            width_inch = img.width / 72.0
            height_inch = img.height / 72.0

            # 페이지 크기를 이미지 크기로 설정
            c.setPageSize((width_inch * inch, height_inch * inch))

            # 이미지를 페이지에 그리기
            c.drawImage(
                image_path, 0, 0, width=width_inch * inch, height=height_inch * inch
            )
            c.showPage()

            # 진행 상태 업데이트
            self.signal_progress.emit(int((i + 1) / total_images * 100))

        c.save()
        self.signal_finished.emit()


if __name__ == "__main__":
    input_image_folder = "capture"
    output_pdf_file = "output.pdf"

    converter = ImageToPdfConverter(input_image_folder, output_pdf_file)
    converter.start()
    converter.wait()
    print("PDF 생성 완료")
    print("PDF 생성 완료")
