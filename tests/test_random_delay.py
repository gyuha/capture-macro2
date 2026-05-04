import time
from unittest.mock import MagicMock, patch


def make_controller():
    """ActionController를 GUI 없이 생성하기 위한 헬퍼."""
    from app.utils.action_controller import ActionController

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
    import random
    original = random.randint

    with patch.object(random, "randint", side_effect=lambda a, b: delays.append((a, b)) or original(a, b)):
        ctrl.random_delay("300,800")

    assert len(delays) == 1
    assert delays[0] == (300, 800)
