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


def parse_unihan_definitions(path: Path) -> Dict[str, str]:
    definitions: Dict[str, str] = {}
    if not path.exists():
        return definitions

    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split("\t")
            if len(parts) < 3:
                continue
            codepoint_str, prop, value = parts[0], parts[1], parts[2]
            if prop != "kDefinition":
                continue

            try:
                cp = int(codepoint_str.replace("U+", ""), 16)
                char = chr(cp)
            except (ValueError, OverflowError):
                continue

            definitions[char] = value.strip()

    return definitions


import re

def clean_definition(raw_text: str, max_tokens: int = 4, max_words: int = 3) -> str:
    if not raw_text:
        return ""
    cleaned = re.sub(r'\(.*?\)', '', raw_text)
    raw_tokens = re.split(r'[;,]', cleaned)
    seen = set()
    out = []
    for t in raw_tokens:
        tok = t.strip()
        if not tok:
            continue
        # 1. Reject if contains any uppercase letters
        if re.search(r'[A-Z]', tok):
            continue
        # 2. Reject if contains CJK characters
        if re.search(r'[\u4e00-\u9fff\u3400-\u4dbf\uf900-\ufaff]', tok):
            continue
        # 3. Reject if phrase contains more than max_words
        words = tok.split()
        if len(words) > max_words:
            continue
        key = tok.lower()
        if key not in seen:
            seen.add(key)
            out.append(tok)
            if len(out) == max_tokens:
                break
    return "; ".join(out)

def enrich_cluster(
    cluster_data: Dict[str, List[str]],
    readings: Dict[str, Dict[str, List[str]]],
    definitions: Dict[str, str],
) -> Dict[str, object]:
    all_chars = set(cluster_data.get("jp", []) + cluster_data.get("sc", []) + cluster_data.get("tc", []))

    pinyin_set = []
    onyomi_set = []
    kunyomi_set = []
    meanings_set = []

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
        if ch in definitions:
            m = definitions[ch]
            # definitions might be slightly different or duplicate, collect them
            if m not in meanings_set:
                meanings_set.append(m)

    # Join multiple different meanings if they exist 
    meaning_str = clean_definition("; ".join(meanings_set))

    return {
        **cluster_data,
        "pinyin": pinyin_set,
        "onyomi": onyomi_set,
        "kunyomi": kunyomi_set,
        "meaning": meaning_str,
    }
