"""Configuration manager for Anki add-on."""
from typing import Any, Dict
from .constants import DEFAULT_CONFIG, ADDON_NAME

_UNSET = object()


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
