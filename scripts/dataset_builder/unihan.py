"""Unihan readings parser and cluster enricher."""
from collections import defaultdict
from pathlib import Path
from typing import Dict, List
from .kana import romaji_to_katakana, romaji_to_hiragana


def parse_unihan_readings(path: Path) -> Dict[str, Dict[str, List[str]]]:
    readings: Dict[str, Dict[str, List[str]]] = defaultdict(lambda: defaultdict(list))
    target_props = {"kMandarin", "kJapaneseOn", "kJapaneseKun"}

    if not path.exists():
        return dict(readings)

    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split("\t")
            if len(parts) < 3:
                continue
            codepoint_str, prop, value = parts[0], parts[1], parts[2]
            if prop not in target_props:
                continue

            try:
                cp = int(codepoint_str.replace("U+", ""), 16)
                char = chr(cp)
            except (ValueError, OverflowError):
                continue

            values = value.strip().split()
            readings[char][prop].extend(values)

    return dict(readings)


def enrich_cluster(
    cluster_data: Dict[str, List[str]],
    readings: Dict[str, Dict[str, List[str]]],
) -> Dict[str, object]:
    all_chars = set(cluster_data.get("jp", []) + cluster_data.get("sc", []) + cluster_data.get("tc", []))

    pinyin_set = []
    onyomi_set = []
    kunyomi_set = []

    for ch in all_chars:
        if ch in readings:
            r = readings[ch]
            for py in r.get("kMandarin", []):
                if py not in pinyin_set:
                    pinyin_set.append(py)
            for on_reading in r.get("kJapaneseOn", []):
                converted = romaji_to_katakana(on_reading)
                if converted and converted not in onyomi_set:
                    onyomi_set.append(converted)
            for kun_reading in r.get("kJapaneseKun", []):
                converted = romaji_to_hiragana(kun_reading)
                if converted and converted not in kunyomi_set:
                    kunyomi_set.append(converted)

    return {
        **cluster_data,
        "pinyin": pinyin_set,
        "onyomi": onyomi_set,
        "kunyomi": kunyomi_set,
    }
