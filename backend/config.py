"""Configuration manager for Anki add-on."""
from typing import Any, Dict

DEFAULT_CONFIG: Dict[str, Any] = {
    "modifier_key": "Shift",
    "theme": "auto",
    "show_pinyin": True,
    "show_readings": True,
    "popup_delay_ms": 60,
    "font_size": 14,
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

    def get(self, key: str, default: Any = None) -> Any:
        return self._config.get(key, default if default is not None else DEFAULT_CONFIG.get(key))

    def all(self) -> Dict[str, Any]:
        return dict(self._config)
