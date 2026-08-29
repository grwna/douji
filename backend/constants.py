from pathlib import Path
from typing import Any, Dict

# Addon Root 
ROOT_DIR = Path(__file__).resolve().parent.parent

# Core Directories
DATA_DIR = ROOT_DIR / "data"
UI_DIR = ROOT_DIR / "ui"

# Core File Paths
DATASET_PATH = DATA_DIR / "dataset.json"
TOOLTIP_CSS_PATH = UI_DIR / "tooltip.css"
TOOLTIP_JS_PATH = UI_DIR / "tooltip.js"

# Addon Identity 
ADDON_NAME = "douji"
BRIDGE_PREFIX = "douji:"

# Default Addon Configuration
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
