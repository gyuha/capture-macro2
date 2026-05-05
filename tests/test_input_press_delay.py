import pytest
from unittest.mock import patch, MagicMock


@pytest.fixture
def config():
    from app.utils.singleton_meta import SingletonMeta
    SingletonMeta._instances.clear()
    with patch("app.config.config.QSettings") as mock_qs, \
         patch("app.config.config.QApplication") as mock_app:
        mock_app.screens.return_value = [MagicMock()]
        mock_qs.return_value.value.side_effect = lambda key, default, **kw: default
        from app.config.config import Config
        yield Config()
    SingletonMeta._instances.clear()


def test_config_has_click_press_min_default(config):
    assert config.click_press_min == 10


def test_config_has_click_press_max_default(config):
    assert config.click_press_max == 150


def test_config_has_key_press_min_default(config):
    assert config.key_press_min == 10


def test_config_has_key_press_max_default(config):
    assert config.key_press_max == 150


def test_click_mouse_uses_config_delay():
    import random
    delays = []

    from app.utils.singleton_meta import SingletonMeta
    SingletonMeta._instances.clear()

    with patch("app.config.config.QSettings") as mock_qs, \
         patch("app.config.config.QApplication") as mock_app, \
         patch("pynput.mouse.Controller"), \
         patch("pynput.keyboard.Controller"), \
         patch("time.sleep"):

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

    SingletonMeta._instances.clear()
    assert any(d == (30, 80) for d in delays), f"expected (30,80) in {delays}"


def test_press_key_uses_config_delay():
    import random
    delays = []

    from app.utils.singleton_meta import SingletonMeta
    SingletonMeta._instances.clear()

    with patch("app.config.config.QSettings") as mock_qs, \
         patch("app.config.config.QApplication") as mock_app, \
         patch("pynput.mouse.Controller"), \
         patch("pynput.keyboard.Controller"), \
         patch("time.sleep"):

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

    SingletonMeta._instances.clear()
    assert any(d == (20, 60) for d in delays), f"expected (20,60) in {delays}"
