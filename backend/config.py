"""Configuration manager for Anki add-on."""
from typing import Any, Dict

_UNSET = object()

DEFAULT_CONFIG: Dict[str, Any] = {
    "modifier_key": "Shift",
    "theme": "auto",
    "popup_delay_ms": 30,
    "character_font_size": 24,
    "reading_font_size": 13,
    "bold_characters": False,
    "japanese_font": "Yu Gothic, Meiryo, 'Hiragino Sans', sans-serif",
    "chinese_font": "'Microsoft YaHei', 'PingFang SC', 'Source Han Sans CN', sans-serif",
    "popup_min_width": 220,
    "popup_max_width": 320,
    "show_pinyin": True,
    "show_readings": True,
}


class ConfigManager:
    """Reads and caches user settings from Anki addonManager."""

    def __init__(self, mw=None):
        self.mw = mw
        self._config = dict(DEFAULT_CONFIG)
        self.reload()

    def reload(self) -> None:
        if self.mw and hasattr(self.mw, "addonManager"):
            addon_name = __name__.split(".")[0]
            user_conf = self.mw.addonManager.getConfig(addon_name)
            if user_conf:
                self._config.update(user_conf)

    def get(self, key: str, default: Any = _UNSET) -> Any:
        if default is _UNSET:
            return self._config.get(key, DEFAULT_CONFIG.get(key))
        return self._config.get(key, default)

    def all(self) -> Dict[str, Any]:
        return dict(self._config)
