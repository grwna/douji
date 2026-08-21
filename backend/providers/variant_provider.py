"""Variant mapping lookup provider."""
import json
from pathlib import Path
from typing import Optional, Dict, Any
from .base import BaseLookupProvider


class VariantMappingProvider(BaseLookupProvider):
    """Provides cross-reference character variant data from precompiled JSON."""

    def __init__(self, data_path: Optional[str] = None):
        if data_path is None:
            data_path = str(Path(__file__).resolve().parents[2] / "data" / "char_variants.json")
        self.data_path = data_path
        self._data: Dict[str, Any] = {}
        self._load_data()

    def _load_data(self) -> None:
        path = Path(self.data_path)
        if path.exists():
            with open(path, "r", encoding="utf-8") as f:
                self._data = json.load(f)

    def lookup(self, char: str) -> Optional[Dict[str, Any]]:
        if not char:
            return None

        char = char[0]
        entry = self._data.get(char)

        if entry:
            jp_list = entry.get("jp", [char])
            sc_list = entry.get("sc", [char])
            tc_list = entry.get("tc", [char])
            jp_val = jp_list[0] if jp_list else char
            sc_val = sc_list[0] if sc_list else char
            tc_val = tc_list[0] if tc_list else char

            all_identical = (jp_val == sc_val == tc_val)
            all_different = (jp_val != sc_val and jp_val != tc_val and sc_val != tc_val)

            variants = {"jp": jp_list, "sc": sc_list, "tc": tc_list}
            hovered_variant = next((k for k, v in variants.items() if char in v), None)

            return {
                "found": True,
                "char": char,
                "jp": jp_list,
                "sc": sc_list,
                "tc": tc_list,
                "pinyin": entry.get("pinyin", []),
                "onyomi": entry.get("onyomi", []),
                "kunyomi": entry.get("kunyomi", []),
                "all_identical": all_identical,
                "all_different": all_different,
                "hovered_variant": hovered_variant,
            }

        # Else: character not in mapping -> empty state
        return {
            "found": False,
            "char": char,
            "message": "No character cross-reference found",
        }
