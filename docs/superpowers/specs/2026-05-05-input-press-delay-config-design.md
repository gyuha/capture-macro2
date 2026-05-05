# 입력 딜레이 설정 기능 설계

## 목표

클릭과 키 입력 시 press~release 사이의 랜덤 딜레이를 설정 다이얼로그에서 조정할 수 있도록 한다.  
현재 `input_controller.py`에 하드코딩된 `random.randint(10, 150)` 값을 Config 기반으로 교체한다.

---

## 아키텍처

### 접근 방식

`InputController`가 `Config` 싱글턴을 직접 참조하는 방식(방법 A) 채택.  
- 이미 앱 전체에서 `Config()` 싱글턴을 직접 참조하는 패턴 사용 중
- 설정 변경 시 재시작 없이 즉시 반영

---

## 변경 파일

### 1. `app/config/config.py`

새 필드 4개 추가:

| 필드명 | 타입 | 기본값 | 설명 |
|---|---|---|---|
| `click_press_min` | int | 10 | 클릭 press~release 최소 딜레이 (ms) |
| `click_press_max` | int | 150 | 클릭 press~release 최대 딜레이 (ms) |
| `key_press_min` | int | 10 | 키 press~release 최소 딜레이 (ms) |
| `key_press_max` | int | 150 | 키 press~release 최대 딜레이 (ms) |

`load_from_settings()`, `save_to_settings()` 양쪽에 추가.

### 2. `app/utils/input_controller.py`

`Config` 임포트 추가. `click_mouse()`와 `press_key()`에서 하드코딩 값 제거 후 Config 참조:

```python
def click_mouse(self):
    cfg = Config()
    self.mouse.press(Button.left)
    time.sleep(random.randint(cfg.click_press_min, cfg.click_press_max) / 1000)
    self.mouse.release(Button.left)

def press_key(self, key):
    cfg = Config()
    send_key = get_key_from_string(key)
    if send_key is None:
        print(f"Unknown key: {key}")
        return
    self.keyboard.press(send_key)
    time.sleep(random.randint(cfg.key_press_min, cfg.key_press_max) / 1000)
    self.keyboard.release(send_key)
```

### 3. `ui/setting_dialog_ui.py`

기존 `sbSwipeSecs` 행(row 9) 아래에 2개 행 추가 (row 10, 11):

**row 10 — 클릭 딜레이:**
- 레이블: `label_click_delay` ("클릭 딜레이")
- 필드: `QHBoxLayout` → `sbClickPressMin`(ms) + `QLabel("~")` + `sbClickPressMax`(ms)
- 범위: 1~2000ms

**row 11 — 키 딜레이:**
- 레이블: `label_key_delay` ("키 딜레이")
- 필드: `QHBoxLayout` → `sbKeyPressMin`(ms) + `QLabel("~")` + `sbKeyPressMax`(ms)
- 범위: 1~2000ms

### 4. `app/dialogs/setting_dialog.py`

- `load_settings()`: 4개 SpinBox에 config 값 세팅
- `connect_signals_slots()`: `valueChanged` 시그널 연결
- `ok()`: config에 4개 값 저장

---

## 데이터 흐름

```
설정 다이얼로그 (SpinBox)
    → Config.click_press_min/max, key_press_min/max 저장
    → QSettings 영속화

매크로 실행 시
    → InputController.click_mouse() / press_key()
    → Config() 싱글턴 읽기
    → random.randint(min, max) / 1000 딜레이 적용
```

---

## 제약 사항

- min > max 방어: `InputController`에서 min/max 순서를 보장 (`min(a,b)`, `max(a,b)` 사용)
- `.ui` 파일은 수동 편집하지 않고 `setting_dialog_ui.py`에 직접 추가 (재컴파일 없음)
