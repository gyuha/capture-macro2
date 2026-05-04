# random_delay 매크로 액션 구현 계획

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 매크로 테이블에 `random_delay` 액션을 추가해 지정 범위(min~max ms) 내 무작위 대기를 지원한다.

**Architecture:** `MacroActions` enum에 새 항목을 추가하고, UI는 두 개의 SpinBox를 담은 컨테이너 위젯으로 구성한다. 실행 로직은 `ActionController.random_delay()`가 담당하며, `execute_macro()`의 `getattr` 디스패치가 자동으로 연결한다.

**Tech Stack:** Python 3.12, PySide6, pytest

---

## 파일 구조

| 파일 | 변경 내용 |
|------|-----------|
| `app/widgets/command_widget.py` | `RANDOM_DELAY` enum, 기본값, UI 위젯 추가 |
| `app/utils/action_controller.py` | `random_delay()` 메서드 추가 |
| `tests/test_random_delay.py` | 신규 — `random_delay()` 로직 단위 테스트 |

---

### Task 1: `random_delay()` 실행 로직 추가 (action_controller.py)

**Files:**
- Modify: `app/utils/action_controller.py`
- Test: `tests/test_random_delay.py`

- [ ] **Step 1: tests 디렉토리 및 테스트 파일 생성**

```bash
mkdir -p /Users/gyuha/workspace/capture-macro2/tests
touch /Users/gyuha/workspace/capture-macro2/tests/__init__.py
```

- [ ] **Step 2: 실패하는 테스트 작성**

`tests/test_random_delay.py` 생성:

```python
import time
from unittest.mock import MagicMock, patch


def make_controller():
    """ActionController를 GUI 없이 생성하기 위한 헬퍼."""
    from app.utils.action_controller import ActionController

    with patch("app.utils.action_controller.InputController"), \
         patch("app.utils.action_controller.QApplication"):
        ctrl = ActionController.__new__(ActionController)
        ctrl.app_core = MagicMock()
        ctrl.app_core.is_running = True
        return ctrl


def test_random_delay_waits_within_range():
    ctrl = make_controller()
    start = time.time()
    ctrl.random_delay("100,200")
    elapsed_ms = (time.time() - start) * 1000
    assert 90 <= elapsed_ms <= 500, f"elapsed {elapsed_ms:.0f}ms out of expected range"


def test_random_delay_stops_when_not_running():
    ctrl = make_controller()
    ctrl.app_core.is_running = False
    start = time.time()
    ctrl.random_delay("5000,6000")
    elapsed_ms = (time.time() - start) * 1000
    assert elapsed_ms < 200, f"should stop immediately but took {elapsed_ms:.0f}ms"


def test_random_delay_parses_value():
    ctrl = make_controller()
    delays = []
    original = __import__("random").randint

    import random
    with patch.object(random, "randint", side_effect=lambda a, b: delays.append((a, b)) or original(a, b)):
        ctrl.random_delay("300,800")

    assert len(delays) == 1
    assert delays[0] == (300, 800)
```

- [ ] **Step 3: 테스트 실행 — 실패 확인**

```bash
cd /Users/gyuha/workspace/capture-macro2 && python -m pytest tests/test_random_delay.py -v 2>&1 | head -30
```

Expected: `AttributeError: 'ActionController' object has no attribute 'random_delay'`

- [ ] **Step 4: `random_delay()` 메서드 구현**

`app/utils/action_controller.py`의 `delay()` 메서드(101행) 바로 아래에 추가:

```python
def random_delay(self, value):
    min_ms, max_ms = map(int, value.split(","))
    total_delay = random.randint(min_ms, max_ms)
    interval = 100
    for _ in range(0, total_delay, interval):
        if not self.app_core.is_running:
            return
        time.sleep(interval / 1000)
    remaining = total_delay % interval
    if remaining > 0 and self.app_core.is_running:
        time.sleep(remaining / 1000)
```

(`random` 모듈은 파일 상단에 이미 import되어 있음)

- [ ] **Step 5: 테스트 실행 — 통과 확인**

```bash
cd /Users/gyuha/workspace/capture-macro2 && python -m pytest tests/test_random_delay.py -v
```

Expected:
```
PASSED tests/test_random_delay.py::test_random_delay_waits_within_range
PASSED tests/test_random_delay.py::test_random_delay_stops_when_not_running
PASSED tests/test_random_delay.py::test_random_delay_parses_value
```

- [ ] **Step 6: 커밋**

```bash
git add app/utils/action_controller.py tests/test_random_delay.py tests/__init__.py
git commit -m "feat: ActionController에 random_delay() 메서드 추가"
```

---

### Task 2: UI 연동 (command_widget.py)

**Files:**
- Modify: `app/widgets/command_widget.py`

- [ ] **Step 1: `MacroActions` enum에 `RANDOM_DELAY` 추가**

`app/widgets/command_widget.py` 28행, `MOVE = "move"` 다음에 추가:

```python
RANDOM_DELAY = "random_delay"
```

- [ ] **Step 2: `DEFAULT_ACTION_VALUES`에 기본값 추가**

73행, `"key": "right"` 다음에 추가:

```python
"random_delay": "100,1000",
```

- [ ] **Step 3: `set_macro_row()`에 `random_delay` UI 분기 추가**

`app/widgets/command_widget.py` 파일 상단 import 블록에 `QHBoxLayout`, `QLabel` 추가:

```python
from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSpinBox,
    QTableWidgetItem,
    QWidget,
)
```

244행, `elif action == MacroActions.DELAY.value:` 블록 직후에 추가:

```python
elif action == MacroActions.RANDOM_DELAY.value:
    try:
        min_val, max_val = map(int, str(value).split(","))
    except (ValueError, AttributeError):
        min_val, max_val = 100, 1000

    container = QWidget()
    layout = QHBoxLayout(container)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(2)

    minSpin = QSpinBox()
    minSpin.setRange(1, 60000)
    minSpin.setSuffix("ms")
    minSpin.setValue(min_val)

    maxSpin = QSpinBox()
    maxSpin.setRange(1, 60000)
    maxSpin.setSuffix("ms")
    maxSpin.setValue(max_val)

    layout.addWidget(minSpin)
    layout.addWidget(QLabel("~"))
    layout.addWidget(maxSpin)

    def on_spin_changed(_, r=row, mn=minSpin, mx=maxSpin):
        self.set_macro_table_row_value(
            r, MacroActions.RANDOM_DELAY.value, f"{mn.value()},{mx.value()}"
        )

    minSpin.valueChanged.connect(on_spin_changed)
    maxSpin.valueChanged.connect(on_spin_changed)

    self.ui.macroTable.setCellWidget(row, 1, container)
```

- [ ] **Step 4: column 2, 3 비활성화 조건에 `RANDOM_DELAY` 추가**

246행의 조건을 수정:

```python
if action in {MacroActions.DELAY.value, MacroActions.KEY.value, MacroActions.RANDOM_DELAY.value}:
```

- [ ] **Step 5: `set_macro_table_row_value()`에 `RANDOM_DELAY` 처리 추가**

269행, `if action == MacroActions.DELAY.value:` 블록 직후에 추가:

```python
elif action == MacroActions.RANDOM_DELAY.value:
    self.macros()[row].value = value
```

- [ ] **Step 6: 앱 실행하여 UI 확인**

```bash
cd /Users/gyuha/workspace/capture-macro2 && python app.py
```

확인 항목:
1. 매크로 테이블에서 액션 콤보를 열면 `random_delay` 항목이 보임
2. `random_delay` 선택 시 두 개의 SpinBox(`~` 구분자 사이)가 column 1에 나타남
3. SpinBox 값 변경 후 저장/재실행 시 값이 유지됨
4. F1로 실행 시 지정 범위 내에서 딜레이 발생 (로그로 확인 가능)

- [ ] **Step 7: 커밋**

```bash
git add app/widgets/command_widget.py
git commit -m "feat: command_widget에 random_delay UI 추가"
```
