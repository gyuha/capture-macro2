# random_delay 매크로 액션 설계

## 개요

반복 수행 매크로에 `random_delay` 액션을 추가한다. 사용자가 최솟값과 최댓값(ms)을 지정하면, 실행 시 해당 범위 내에서 무작위 시간만큼 대기한다.

## 요구사항

- 기존 `delay` 액션과 동일한 방식으로 매크로 테이블에 추가 가능
- 값은 `"min,max"` 형태 문자열로 저장 (예: `"100,1000"`)
- 실행 시 min 이상 max 이하의 무작위 ms만큼 대기
- 실행 중 중단(stop) 가능해야 함 (100ms 간격으로 is_running 체크)

## 변경 파일

### 1. `app/widgets/command_widget.py`

**MacroActions enum 추가:**
```python
RANDOM_DELAY = "random_delay"
```

**DEFAULT_ACTION_VALUES 추가:**
```python
"random_delay": "100,1000"
```

**set_macro_row() 분기 추가:**
`random_delay` 선택 시 column 1에 min/max 두 SpinBox를 담은 QWidget 배치.
column 2, 3은 `delay`와 동일하게 비활성화.

```
[ random_delay ▼ ] [ 100ms ↕  ~  1000ms ↕ ] [  -  ] [  -  ]
```

- SpinBox 범위: 1 ~ 60000ms
- 값 변경 시 `"min,max"` 형태로 `macro.value` 업데이트 및 저장

### 2. `app/utils/action_controller.py`

`random_delay()` 메서드 추가:

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

`random` 모듈은 이미 import되어 있어 추가 의존성 없음.

## 데이터 흐름

1. 사용자가 매크로 테이블에서 `random_delay` 선택
2. min/max SpinBox로 범위 입력 → `macro.value = "min,max"` 저장
3. 실행 시 `ActionController.random_delay("min,max")` 호출
4. `random.randint(min, max)` 로 실제 대기 시간 결정 후 대기

## 비고

- `Macro` 클래스의 `value` 필드는 `str` 타입이므로 변경 없음
- `execute_macro()`는 `getattr(self, macro.action)` 방식으로 디스패치하므로 자동 지원
