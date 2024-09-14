
import os
import cv2
import numpy as np
from PIL import Image
from PySide6.QtCore import QThread, Signal
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
import pytesseract
from pytesseract import Output
import pandas as pd
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

class ImageToPdfConverter(QThread):
    signal_progress = Signal(int)
    signal_finished = Signal()

    def __init__(self):
        super().__init__()
        self.image_folder = ""
        self.output_pdf = ""
        
        # 한글 폰트 등록 (폰트 파일의 경로는 실제 경로로 변경해야 합니다)
        pdfmetrics.registerFont(TTFont('NanumGothic', 'NanumGothic.ttf'))

    def setFile(self, image_folder, output_pdf):
        self.image_folder = image_folder
        self.output_pdf = output_pdf

    def preprocess_image(self, image):
        gray = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)
        denoised = cv2.fastNlMeansDenoising(gray)
        _, binary = cv2.threshold(denoised, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        kernel = np.ones((1, 1), np.uint8)
        morphed = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
        return Image.fromarray(morphed)

    def run(self):
        image_files = [f for f in os.listdir(self.image_folder) if f.lower().endswith(("png", "jpg", "jpeg"))]
        image_files.sort()

        c = canvas.Canvas(self.output_pdf)
        total_images = len(image_files)

        for i, image_file in enumerate(image_files):
            image_path = os.path.join(self.image_folder, image_file)
            img = Image.open(image_path)

            preprocessed_img = self.preprocess_image(img)

            width_inch = img.width / 72.0
            height_inch = img.height / 72.0

            c.setPageSize((width_inch * inch, height_inch * inch))
            c.drawImage(image_path, 0, 0, width=width_inch * inch, height=height_inch * inch)

            custom_config = r'--oem 3 --psm 6 -l kor+eng'
            ocr_data = pytesseract.image_to_data(preprocessed_img, config=custom_config, output_type=Output.DATAFRAME)

            for _, row in ocr_data.iterrows():
                if pd.notna(row['text']) and row['conf'] > 10:
                    x = row['left'] / 72.0 * inch
                    y = height_inch * inch - (row['top'] + row['height']) / 72.0 * inch
                    font_size = row['height'] / 72.0 * 72

                    # UTF-8로 명시적 디코딩
                    text = row['text'].encode('utf-8').decode('utf-8').strip()
                    if text and not all(char == '■' for char in text):
                        c.setFont("NanumGothic", font_size)  # 한글 폰트 사용
                        c.setFillColorRGB(0, 0, 1)
                        c.drawString(x, y, text)

            c.showPage()
            self.signal_progress.emit(int((i + 1) / total_images * 100))

        c.save()
        self.signal_finished.emit()

if __name__ == "__main__":
    input_image_folder = "capture"
    output_pdf_file = "output.pdf"

    converter = ImageToPdfConverter()
    converter.setFile(input_image_folder, output_pdf_file)
    converter.start()
    converter.wait()
    print("PDF 생성 완료")
