# capture-macro2
Capture macro 2

## MacOS에서 설정
1. 마우스, 키보드 컨트롤
     - `시스템설정 > 개인정보 보호 및 보안 > 손쉬운 사용`에 CaptureMacro 앱을 추가 권한을 추가 합니다.
2. 캡쳐 컨트롤
     - `시스템설정 > 개인정보 보호 및 보안 > 화면 및 시스템 오디오 녹음`에 CaptureMacro 앱을 추가 하고 권한을 켜 줍니다.

## Todo
- [x] init ui design
    -  [x] in widget
- [x] configure file save/load
  - [x] config file structure
    - [x] save path
    - [x] compress level
- [x] macro process
    - [x] macro type
      - [x] wheel scroll
      - [x] click
      - [x] key press
      - [x] image capture
    - [x] Setting up the event area
    - [x] insert, delete, move
    - [x] save/load
- [x] image capture
  - [x] image save path
  - [x] compress level
  - [x] image preview
- [x] Execute the capture command in the action list.
- [x] If the selected image is deleted, preview the image that is in focus.
- [x] image to pdf
  - [ ] image ocr
- [x] Application icon
- [x] Creating an executable file
  - [x] for MacOS
  - [x] for Windows
- [x] macro list selected cursor when action doing
- [x] settings save to QSettings
  - [x] image compress level widget change to spinnerbox
  - [ ] start, end global hot-key change

## 개발 환경 설정
### Windows

#### Required
- pyenv-win
  - python 3.12.12
- vscode

### Etc
#### mac용 아이콘 업데이트 하기
```bash
python ./app/utils/create_icon.py
```

### 빌드 옵션
```bash
pyinstaller --icon=resources/icon.png \
            --name=CaptureMacro \
            --noconsole \
            --windowed \
            --noupx \
            app.py
```


