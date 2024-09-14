
import os
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from PySide6.QtCore import QThread, Signal
import pytesseract
from pytesseract import Output
import pandas as pd
from PyPDF2 import PdfWriter, PdfReader
from io import BytesIO

class ImageToPdfConverter(QThread):
    signal_progress = Signal(int)
    signal_finished = Signal()

    def __init__(self):
        super().__init__()
        self.image_folder = ""
        self.output_pdf = ""
        
        # 시스템 폰트 경로 (macOS)
        self.font_path = "/System/Library/Fonts/AppleSDGothicNeo.ttc"

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

    def create_pdf_with_text(self, image_path, ocr_data):
        img = Image.open(image_path).convert("RGBA")
        txt = Image.new("RGBA", img.size, (255, 255, 255, 0))
        draw = ImageDraw.Draw(txt)

        for _, row in ocr_data.iterrows():
            if pd.notna(row['text']) and row['conf'] > 10:
                x = row['left']
                y = row['top']
                text = row['text'].strip()
                if text and not all(char == '■' for char in text):
                    font = ImageFont.truetype(self.font_path, int(row['height']))
                    draw.text((x, y), text, font=font, fill=(0, 0, 0, 0))

        combined = Image.alpha_composite(img, txt)
        combined = combined.convert("RGB")
        
        img_byte_arr = BytesIO()
        combined.save(img_byte_arr, format='PDF')
        img_byte_arr.seek(0)
        
        return img_byte_arr

    def run(self):
        image_files = [f for f in os.listdir(self.image_folder) if f.lower().endswith(("png", "jpg", "jpeg"))]
        image_files.sort()

        output = PdfWriter()
        total_images = len(image_files)

        for i, image_file in enumerate(image_files):
            image_path = os.path.join(self.image_folder, image_file)
            img = Image.open(image_path)
            preprocessed_img = self.preprocess_image(img)

            custom_config = r'--oem 3 --psm 6 -l kor+eng'
            ocr_data = pytesseract.image_to_data(preprocessed_img, config=custom_config, output_type=Output.DATAFRAME)

            pdf_page_bytes = self.create_pdf_with_text(image_path, ocr_data)
            pdf_reader = PdfReader(pdf_page_bytes)
            output.add_page(pdf_reader.pages[0])

            self.signal_progress.emit(int((i + 1) / total_images * 100))

        with open(self.output_pdf, "wb") as output_file:
            output.write(output_file)

        self.signal_finished.emit()

if __name__ == "__main__":
    input_image_folder = "capture"
    output_pdf_file = "output.pdf"

    converter = ImageToPdfConverter()
    converter.setFile(input_image_folder, output_pdf_file)
    converter.start()
    converter.wait()
    print("PDF 생성 완료")
