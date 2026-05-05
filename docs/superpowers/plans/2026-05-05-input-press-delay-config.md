# Input Press Delay Config Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 클릭/키 press~release 사이의 랜덤 딜레이 범위를 설정 다이얼로그에서 개별 조정할 수 있도록 한다.

**Architecture:** `Config` 싱글턴에 4개 필드(`click_press_min/max`, `key_press_min/max`)를 추가하고, `InputController`가 직접 `Config()`를 참조해 딜레이를 적용한다. 설정 다이얼로그 UI(`setting_dialog_ui.py`)에 SpinBox 2쌍을 추가하고 `setting_dialog.py`에서 연결한다.

**Tech Stack:** Python, PySide6 (QSettings, QSpinBox), pynput

---

## 파일 목록

| 파일 | 역할 |
|---|---|
| `app/config/config.py` | 새 딜레이 필드 4개 추가 |
| `app/utils/input_controller.py` | 하드코딩 제거, Config 참조 |
| `ui/setting_dialog_ui.py` | SpinBox UI 2쌍 추가 |
| `app/dialogs/setting_dialog.py` | 로드·저장·시그널 연결 |
| `tests/test_input_press_delay.py` | Config 필드 및 InputController 동작 테스트 |

---

### Task 1: Config에 딜레이 필드 추가

**Files:**
- Modify: `app/config/config.py`
- Test: `tests/test_input_press_delay.py`

- [ ] **Step 1: 실패하는 테스트 작성**

`tests/test_input_press_delay.py` 새로 생성:

```python
import pytest
from unittest.mock import patch, MagicMock


def make_config():
    """Config 싱글턴을 GUI 없이 생성하는 헬퍼."""
    from app.utils.singleton_meta import SingletonMeta
    SingletonMeta._instances.clear()

    with patch("app.config.config.QSettings") as mock_qs, \
         patch("app.config.config.QApplication") as mock_app:
        mock_app.screens.return_value = [MagicMock()]
        mock_qs.return_value.value.side_effect = lambda key, default, **kw: default
        from app.config.config import Config
        cfg = Config()
    return cfg


def test_config_has_click_press_min_default():
    cfg = make_config()
    assert cfg.click_press_min == 10


def test_config_has_click_press_max_default():
    cfg = make_config()
    assert cfg.click_press_max == 150


def test_config_has_key_press_min_default():
    cfg = make_config()
    assert cfg.key_press_min == 10


def test_config_has_key_press_max_default():
    cfg = make_config()
    assert cfg.key_press_max == 150
```

- [ ] **Step 2: 테스트 실패 확인**

```bash
cd /Users/gyuha/workspace/capture-macro2
python -m pytest tests/test_input_press_delay.py -v
```

Expected: `AttributeError: 'Config' object has no attribute 'click_press_min'` 류의 실패

- [ ] **Step 3: Config에 필드 추가**

`app/config/config.py`의 `__init__`에 추가 (기존 `self.swipe_secs = 800` 아래):

```python
self.click_press_min = 10
self.click_press_max = 150
self.key_press_min = 10
self.key_press_max = 150
```

`load_from_settings()`에 추가 (기존 `self.swipe_secs = ...` 아래):

```python
self.click_press_min = self.settings.value("click_press_min", 10, type=int)
self.click_press_max = self.settings.value("click_press_max", 150, type=int)
self.key_press_min = self.settings.value("key_press_min", 10, type=int)
self.key_press_max = self.settings.value("key_press_max", 150, type=int)
```

`save_to_settings()`에 추가 (기존 `self.settings.setValue("swipe_secs", ...)` 아래):

```python
self.settings.setValue("click_press_min", self.click_press_min)
self.settings.setValue("click_press_max", self.click_press_max)
self.settings.setValue("key_press_min", self.key_press_min)
self.settings.setValue("key_press_max", self.key_press_max)
```

- [ ] **Step 4: 테스트 통과 확인**

```bash
python -m pytest tests/test_input_press_delay.py::test_config_has_click_press_min_default tests/test_input_press_delay.py::test_config_has_click_press_max_default tests/test_input_press_delay.py::test_config_has_key_press_min_default tests/test_input_press_delay.py::test_config_has_key_press_max_default -v
```

Expected: 4개 PASS

- [ ] **Step 5: 커밋**

```bash
git add app/config/config.py tests/test_input_press_delay.py
git commit -m "feat: Config에 클릭/키 press 딜레이 필드 추가"
```

---

### Task 2: InputController에서 Config 참조

**Files:**
- Modify: `app/utils/input_controller.py`
- Test: `tests/test_input_press_delay.py`

- [ ] **Step 1: 실패하는 테스트 추가**

`tests/test_input_press_delay.py`에 추가:

```python
def make_input_controller(click_min=10, click_max=150, key_min=10, key_max=150):
    """InputController를 pynput 없이 생성하는 헬퍼."""
    from app.utils.singleton_meta import SingletonMeta
    SingletonMeta._instances.clear()

    with patch("app.config.config.QSettings") as mock_qs, \
         patch("app.config.config.QApplication") as mock_app, \
         patch("pynput.mouse.Controller"), \
         patch("pynput.keyboard.Controller"):
        mock_app.screens.return_value = [MagicMock()]

        def side_effect(key, default, **kw):
            mapping = {
                "click_press_min": click_min,
                "click_press_max": click_max,
                "key_press_min": key_min,
                "key_press_max": key_max,
            }
            return mapping.get(key, default)

        mock_qs.return_value.value.side_effect = side_effect
        from app.config.config import Config
        Config()  # 싱글턴 초기화

        from app.utils.input_controller import InputController
        ctrl = InputController()
    return ctrl


def test_click_mouse_uses_config_delay():
    import random
    delays = []
    original = random.randint

    with patch("app.config.config.QSettings") as mock_qs, \
         patch("app.config.config.QApplication") as mock_app, \
         patch("pynput.mouse.Controller") as mock_mouse_cls, \
         patch("pynput.keyboard.Controller"), \
         patch("time.sleep") as mock_sleep:
        from app.utils.singleton_meta import SingletonMeta
        SingletonMeta._instances.clear()

        mock_app.screens.return_value = [MagicMock()]

        def qs_value(key, default, **kw):
            return {"click_press_min": 30, "click_press_max": 80}.get(key, default)
        mock_qs.return_value.value.side_effect = qs_value

        from app.config.config import Config
        Config()

        with patch.object(random, "randint", side_effect=lambda a, b: delays.append((a, b)) or 50):
            from app.utils.input_controller import InputController
            ctrl = InputController()
            ctrl.click_mouse()

    assert any(d == (30, 80) for d in delays), f"expected (30,80) in {delays}"


def test_press_key_uses_config_delay():
    import random
    delays = []

    with patch("app.config.config.QSettings") as mock_qs, \
         patch("app.config.config.QApplication") as mock_app, \
         patch("pynput.mouse.Controller"), \
         patch("pynput.keyboard.Controller") as mock_kb_cls, \
         patch("time.sleep"):
        from app.utils.singleton_meta import SingletonMeta
        SingletonMeta._instances.clear()

        mock_app.screens.return_value = [MagicMock()]

        def qs_value(key, default, **kw):
            return {"key_press_min": 20, "key_press_max": 60}.get(key, default)
        mock_qs.return_value.value.side_effect = qs_value

        from app.config.config import Config
        Config()

        with patch.object(random, "randint", side_effect=lambda a, b: delays.append((a, b)) or 40):
            from app.utils.input_controller import InputController
            ctrl = InputController()
            ctrl.press_key("enter")

    assert any(d == (20, 60) for d in delays), f"expected (20,60) in {delays}"
```

- [ ] **Step 2: 테스트 실패 확인**

```bash
python -m pytest tests/test_input_press_delay.py::test_click_mouse_uses_config_delay tests/test_input_press_delay.py::test_press_key_uses_config_delay -v
```

Expected: FAIL — 현재 하드코딩 `(10, 150)` 사용 중이므로 assert 실패

- [ ] **Step 3: InputController 수정**

`app/utils/input_controller.py`에서 `from app.utils.pynput_keymap import get_key_from_string` 아래에 추가:

```python
from app.config.config import Config
```

`click_mouse()` 전체 교체:

```python
def click_mouse(self):
    cfg = Config()
    self.mouse.press(Button.left)
    time.sleep(random.randint(min(cfg.click_press_min, cfg.click_press_max),
                              max(cfg.click_press_min, cfg.click_press_max)) / 1000)
    self.mouse.release(Button.left)
```

`press_key()` 전체 교체:

```python
def press_key(self, key):
    cfg = Config()
    send_key = get_key_from_string(key)
    if send_key is None:
        print(f"Unknown key: {key}")
        return
    self.keyboard.press(send_key)
    time.sleep(random.randint(min(cfg.key_press_min, cfg.key_press_max),
                              max(cfg.key_press_min, cfg.key_press_max)) / 1000)
    self.keyboard.release(send_key)
```

- [ ] **Step 4: 테스트 통과 확인**

```bash
python -m pytest tests/test_input_press_delay.py -v
```

Expected: 전체 PASS

- [ ] **Step 5: 커밋**

```bash
git add app/utils/input_controller.py tests/test_input_press_delay.py
git commit -m "feat: InputController가 Config에서 press 딜레이 값 참조"
```

---

### Task 3: 설정 다이얼로그 UI에 SpinBox 추가

**Files:**
- Modify: `ui/setting_dialog_ui.py`

- [ ] **Step 1: setting_dialog_ui.py에 UI 요소 추가**

`setupUi()` 안에서 `self.sbSwipeSecs` 관련 블록(row 9) **이후**이자 `self.verticalLayout.addLayout(self.formLayout)` **이전**에 아래를 삽입:

```python
        # row 10 — 클릭 딜레이
        self.label_click_delay = QLabel(self.frame)
        self.label_click_delay.setObjectName(u"label_click_delay")
        self.formLayout.setWidget(10, QFormLayout.LabelRole, self.label_click_delay)

        self.horizontalLayout_click = QHBoxLayout()
        self.horizontalLayout_click.setObjectName(u"horizontalLayout_click")

        self.sbClickPressMin = QSpinBox(self.frame)
        self.sbClickPressMin.setObjectName(u"sbClickPressMin")
        self.sbClickPressMin.setMinimum(1)
        self.sbClickPressMin.setMaximum(2000)
        self.sbClickPressMin.setSuffix(u"ms")
        self.sbClickPressMin.setValue(10)
        self.horizontalLayout_click.addWidget(self.sbClickPressMin)

        self.label_click_tilde = QLabel(self.frame)
        self.label_click_tilde.setObjectName(u"label_click_tilde")
        self.label_click_tilde.setText(u"~")
        self.horizontalLayout_click.addWidget(self.label_click_tilde)

        self.sbClickPressMax = QSpinBox(self.frame)
        self.sbClickPressMax.setObjectName(u"sbClickPressMax")
        self.sbClickPressMax.setMinimum(1)
        self.sbClickPressMax.setMaximum(2000)
        self.sbClickPressMax.setSuffix(u"ms")
        self.sbClickPressMax.setValue(150)
        self.horizontalLayout_click.addWidget(self.sbClickPressMax)

        self.formLayout.setLayout(10, QFormLayout.FieldRole, self.horizontalLayout_click)

        # row 11 — 키 딜레이
        self.label_key_delay = QLabel(self.frame)
        self.label_key_delay.setObjectName(u"label_key_delay")
        self.formLayout.setWidget(11, QFormLayout.LabelRole, self.label_key_delay)

        self.horizontalLayout_key = QHBoxLayout()
        self.horizontalLayout_key.setObjectName(u"horizontalLayout_key")

        self.sbKeyPressMin = QSpinBox(self.frame)
        self.sbKeyPressMin.setObjectName(u"sbKeyPressMin")
        self.sbKeyPressMin.setMinimum(1)
        self.sbKeyPressMin.setMaximum(2000)
        self.sbKeyPressMin.setSuffix(u"ms")
        self.sbKeyPressMin.setValue(10)
        self.horizontalLayout_key.addWidget(self.sbKeyPressMin)

        self.label_key_tilde = QLabel(self.frame)
        self.label_key_tilde.setObjectName(u"label_key_tilde")
        self.label_key_tilde.setText(u"~")
        self.horizontalLayout_key.addWidget(self.label_key_tilde)

        self.sbKeyPressMax = QSpinBox(self.frame)
        self.sbKeyPressMax.setObjectName(u"sbKeyPressMax")
        self.sbKeyPressMax.setMinimum(1)
        self.sbKeyPressMax.setMaximum(2000)
        self.sbKeyPressMax.setSuffix(u"ms")
        self.sbKeyPressMax.setValue(150)
        self.horizontalLayout_key.addWidget(self.sbKeyPressMax)

        self.formLayout.setLayout(11, QFormLayout.FieldRole, self.horizontalLayout_key)
```

`retranslateUi()` 안에 레이블 텍스트 추가 (`self.sbSwipeSecs.setSuffix(...)` 줄 이후):

```python
        self.label_click_delay.setText(QCoreApplication.translate("SettingDialog", u"클릭 딜레이", None))
        self.label_key_delay.setText(QCoreApplication.translate("SettingDialog", u"키 딜레이", None))
```

또한 다이얼로그 최대 높이를 400 → 480으로 조정:

```python
        SettingDialog.setMaximumSize(QSize(500, 480))
```

- [ ] **Step 2: 커밋**

```bash
git add ui/setting_dialog_ui.py
git commit -m "feat: 설정 다이얼로그에 클릭/키 딜레이 SpinBox 추가"
```

---

### Task 4: SettingDialog 로드·저장·시그널 연결

**Files:**
- Modify: `app/dialogs/setting_dialog.py`

- [ ] **Step 1: load_settings()에 SpinBox 초기화 추가**

`app/dialogs/setting_dialog.py`의 `load_settings()` 맨 끝(버전 표시 블록 전)에 추가:

```python
        self.ui.sbClickPressMin.setValue(self.config.click_press_min)
        self.ui.sbClickPressMax.setValue(self.config.click_press_max)
        self.ui.sbKeyPressMin.setValue(self.config.key_press_min)
        self.ui.sbKeyPressMax.setValue(self.config.key_press_max)
```

- [ ] **Step 2: ok()에 저장 추가**

`ok()` 안의 마지막 `self.accept()` 직전에 추가:

```python
        self.config.click_press_min = self.ui.sbClickPressMin.value()
        self.config.click_press_max = self.ui.sbClickPressMax.value()
        self.config.key_press_min = self.ui.sbKeyPressMin.value()
        self.config.key_press_max = self.ui.sbKeyPressMax.value()
```

- [ ] **Step 3: 커밋**

```bash
git add app/dialogs/setting_dialog.py
git commit -m "feat: 설정 다이얼로그에서 클릭/키 딜레이 로드·저장 연결"
```

---

### Task 5: 전체 테스트 및 버전 업

- [ ] **Step 1: 전체 테스트 실행**

```bash
python -m pytest tests/ -v
```

Expected: 전체 PASS

- [ ] **Step 2: 버전 업**

`app/config/version.py`:

```python
VERSION = "0.2.3"
```

- [ ] **Step 3: 최종 커밋**

```bash
git add app/config/version.py
git commit -m "chore: 버전 0.2.3으로 업데이트"
```
