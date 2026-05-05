# CaptureMacro

화면 캡처와 마우스/키보드 자동화를 결합한 매크로 도구입니다. 반복적인 화면 캡처 작업을 매크로로 정의하고 자동으로 실행할 수 있습니다.

## 주요 기능

- **화면 캡처**: 지정한 영역을 반복 캡처하여 이미지로 저장
- **매크로 자동화**: 캡처 전/후에 실행할 마우스·키보드 액션 시퀀스 구성
- **PDF 변환**: 캡처된 이미지를 PDF로 일괄 변환
- **중복 감지**: 같은 화면이 반복 캡처되면 자동 중단 (same_count 설정)

### 지원 매크로 액션

| 액션 | 설명 |
|------|------|
| `capture` | 지정 영역 화면 캡처 |
| `click` | 지정 좌표 마우스 클릭 |
| `scroll` | 마우스 휠 스크롤 |
| `swipe` | 화면 스와이프 (터치 시뮬레이션) |
| `move` | 마우스 커서 이동 |
| `key` | 키보드 입력 (방향키, Enter, F1~F12 등) |
| `delay` | 고정 대기 (ms) |
| `random_delay` | 랜덤 범위 대기 (min,max ms) |

## 실행 방법

### 요구사항

- Python 3.12 이상
- [uv](https://docs.astral.sh/uv/) 패키지 매니저

### 설치 및 실행

```bash
# 의존성 설치
uv sync

# 앱 실행
uv run python app.py
```

### macOS 권한 설정

앱 최초 실행 전 두 가지 권한을 허용해야 합니다.

1. **마우스/키보드 제어** (pynput 사용)
   - `시스템 설정 > 개인정보 보호 및 보안 > 손쉬운 사용`에서 CaptureMacro 추가

2. **화면 캡처** (mss 사용)
   - `시스템 설정 > 개인정보 보호 및 보안 > 화면 및 시스템 오디오 녹음`에서 CaptureMacro 추가 후 권한 켜기

## 빌드

### macOS DMG

```bash
./build-mac.sh
```

빌드 결과물은 `dist/` 디렉터리에 생성됩니다. 버전은 `.version` 파일에서 읽습니다.

### Windows EXE

```powershell
.\build-win.ps1
```

## 버전 관리

`.version`과 `app/config/version.py` 두 파일을 항상 동기화해야 합니다. 직접 편집하지 말고 스크립트를 사용하세요.

```bash
python tools/update_version.py 1.0.0
```

버전 이력은 `version_history.txt`에 자동 기록됩니다.

## 개발

```bash
# 테스트 실행
python -m pytest tests/ -v

# UI 파일 재컴파일 (.ui → _ui.py)
./ui-compile.sh
```

### Windows 개발 환경

```bash
# 가상환경 생성
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 아이콘 업데이트 (macOS)

```bash
python ./app/utils/create_icon.py
```
