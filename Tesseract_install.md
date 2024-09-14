# Tesseract install for MacOS

Mac에서 Tesseract를 재설치하는 방법은 다음과 같습니다. Homebrew를 사용하여 설치하는 것이 가장 간단하고 권장되는 방법입니다.

1. Homebrew 설치 (이미 설치되어 있다면 이 단계는 건너뛰세요):

   터미널을 열고 다음 명령어를 실행합니다:

   ```
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```

2. 기존 Tesseract 제거 (이미 설치되어 있는 경우):

   ```
   brew uninstall tesseract
   ```

3. Tesseract 재설치:

   ```
   brew install tesseract
   ```

4. 한국어 언어 데이터 설치:

   ```
   brew install tesseract-lang
   ```

   이 명령어는 모든 언어 데이터를 설치합니다. 한국어만 필요하다면 다음 단계를 따르세요.

5. 한국어 데이터 파일 수동 설치 (선택적):

   a. Tesseract 언어 데이터 저장소에서 최신 한국어 데이터 파일을 다운로드합니다:
      https://github.com/tesseract-ocr/tessdata

   b. `kor.traineddata` 파일을 다운로드하고 Tesseract의 `tessdata` 디렉토리로 복사합니다:

      ```
      sudo cp ~/Downloads/kor.traineddata /usr/local/share/tessdata/
      ```

      M1 Mac의 경우 경로가 다를 수 있습니다:

      ```
      sudo cp ~/Downloads/kor.traineddata /opt/homebrew/share/tessdata/
      ```

6. 설치 확인:

   ```
   tesseract --version
   ```

   이 명령어로 Tesseract 버전과 지원 언어를 확인할 수 있습니다.

7. Python에서 사용하기 위해 pytesseract 설치 또는 업데이트:

   ```
   pip install --upgrade pytesseract
   ```

8. 설치 후 Python 스크립트에서 Tesseract 경로 설정:
```

import pytesseract

# Intel Mac
pytesseract.pytesseract.tesseract_cmd = r'/usr/local/bin/tesseract'

# M1 Mac
# pytesseract.pytesseract.tesseract_cmd = r'/opt/homebrew/bin/tesseract'

# OCR 실행 예시
# text = pytesseract.image_to_string(image, lang='kor+eng')

```
이 과정을 통해 Tesseract를 재설치하고 한국어 지원을 추가할 수 있습니다. 설치 후에도 한글 인식에 문제가 있다면, 이미지 품질 개선, 전처리 과정 최적화, 또는 다른 OCR 솔루션 고려 등의 추가적인 조치가 필요할 수 있습니다.
