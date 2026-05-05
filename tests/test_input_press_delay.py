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
