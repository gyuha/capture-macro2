
import os
from PIL import Image

def create_icns(png_path, icns_path):
    # 필요한 아이콘 크기들
    sizes = [16, 32, 64, 128, 256, 512, 1024]

    # 임시 iconset 디렉토리 생성
    iconset_path = os.path.splitext(icns_path)[0] + '.iconset'
    os.makedirs(iconset_path, exist_ok=True)

    # 원본 이미지 열기
    img = Image.open(png_path)

    # 각 크기별로 이미지 생성
    for size in sizes:
        icon_name = f'icon_{size}x{size}.png'
        if size <= 512:
            icon_name_2x = f'icon_{size}x{size}@2x.png'

        # 이미지 리사이즈
        img_resized = img.resize((size, size), Image.LANCZOS)
        img_resized.save(os.path.join(iconset_path, icon_name))

        if size <= 512:
            img_resized_2x = img.resize((size*2, size*2), Image.LANCZOS)
            img_resized_2x.save(os.path.join(iconset_path, icon_name_2x))

    # iconutil을 사용하여 icns 파일 생성
    os.system(f'iconutil -c icns {iconset_path}')

    # 임시 iconset 디렉토리 삭제
    for file in os.listdir(iconset_path):
        os.remove(os.path.join(iconset_path, file))
    os.rmdir(iconset_path)

    print(f"ICNS file created: {icns_path}")

# 스크립트 실행
if __name__ == "__main__":
    png_path = "./resources/icon.png"
    icns_path = "./resources/icon.icns"
    create_icns(png_path, icns_path)
