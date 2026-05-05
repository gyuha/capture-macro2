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
