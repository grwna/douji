"""Backend package initialization."""
from .config import ConfigManager
from .engine import LookupEngine
from .bridge import BridgeManager
from .constants import (
    ROOT_DIR,
    DATA_DIR,
    UI_DIR,
    CHAR_VARIANTS_PATH,
    TOOLTIP_CSS_PATH,
    TOOLTIP_JS_PATH,
    ADDON_NAME,
    BRIDGE_PREFIX,
    DEFAULT_CONFIG,
)

__all__ = [
    "ConfigManager",
    "LookupEngine",
    "BridgeManager",
    "ROOT_DIR",
    "DATA_DIR",
    "UI_DIR",
    "CHAR_VARIANTS_PATH",
    "TOOLTIP_CSS_PATH",
    "TOOLTIP_JS_PATH",
    "ADDON_NAME",
    "BRIDGE_PREFIX",
    "DEFAULT_CONFIG",
]
