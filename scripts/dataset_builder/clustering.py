"""OpenCC parsing and character clustering."""
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Set, Tuple

CJK_RANGES = [
    (0x4E00, 0x9FFF),
    (0x3400, 0x4DBF),
    (0x20000, 0x2A6DF),
    (0x2A700, 0x2B73F),
    (0x2B740, 0x2B81F),
    (0x2B820, 0x2CEAF),
    (0x2CEB0, 0x2EBEF),
    (0x30000, 0x3134F),
    (0xF900, 0xFAFF),
    (0x2F800, 0x2FA1F),
]


class UnionFind:
    def __init__(self):
        self.parent: Dict[str, str] = {}
        self.rank: Dict[str, int] = {}

    def find(self, x: str) -> str:
        if x not in self.parent:
            self.parent[x] = x
            self.rank[x] = 0
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x: str, y: str) -> None:
        rx, ry = self.find(x), self.find(y)
        if rx == ry:
            return
        if self.rank[rx] < self.rank[ry]:
            rx, ry = ry, rx
        self.parent[ry] = rx
        if self.rank[rx] == self.rank[ry]:
            self.rank[rx] += 1

    def clusters(self) -> Dict[str, Set[str]]:
        groups: Dict[str, Set[str]] = defaultdict(set)
        for x in self.parent:
            groups[self.find(x)].add(x)
        return dict(groups)


def is_cjk(char: str) -> bool:
    cp = ord(char)
    return any(lo <= cp <= hi for lo, hi in CJK_RANGES)


def parse_opencc_file(path: Path) -> List[Tuple[str, List[str]]]:
    mappings = []
    if not path.exists():
        return mappings
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split("\t")
            if len(parts) < 2:
                continue
            source = parts[0].strip()
            targets = parts[1].strip().split()
            if len(source) == 1:
                single_targets = [t for t in targets if len(t) == 1]
                if single_targets:
                    mappings.append((source, single_targets))
    return mappings


def build_variant_graph(opencc_files: List[Path]) -> UnionFind:
    uf = UnionFind()
    for path in opencc_files:
        for source, targets in parse_opencc_file(path):
            for target in targets:
                uf.union(source, target)
    return uf


def classify_cluster(
    chars: Set[str],
    st_map: Dict[str, List[str]],
    ts_map: Dict[str, List[str]],
    jp_map: Dict[str, List[str]],
    readings: Dict[str, Dict[str, List[str]]] = None,
) -> Dict[str, List[str]]:
    valid_chars = {ch for ch in chars if is_cjk(ch)}
    if not valid_chars:
        return {"jp": [], "sc": [], "tc": []}

    st_sources = set(st_map.keys())
    st_targets = {t for targets in st_map.values() for t in targets}
    ts_sources = set(ts_map.keys())
    ts_targets = {t for targets in ts_map.values() for t in targets}
    jp_sources = set(jp_map.keys())
    jp_targets = {t for targets in jp_map.values() for t in targets}

    sc_chars = (valid_chars & st_sources) | (valid_chars & ts_targets)
    tc_chars = (valid_chars & ts_sources) | (valid_chars & st_targets) | (valid_chars & jp_targets)
    jp_chars = set(valid_chars & jp_sources)

    if not jp_chars:
        kun_chars = {ch for ch in valid_chars if readings and ch in readings and readings[ch].get("kJapaneseKun")}
        on_chars = {ch for ch in valid_chars if readings and ch in readings and readings[ch].get("kJapaneseOn")}
        if sc_chars & kun_chars:
            jp_chars = sc_chars & kun_chars
        elif sc_chars & on_chars:
            jp_chars = sc_chars & on_chars
        elif kun_chars:
            jp_chars = set(kun_chars)
        elif sc_chars:
            jp_chars = set(sc_chars)
        elif tc_chars:
            jp_chars = set(tc_chars)
        else:
            jp_chars = set(valid_chars)

    if not sc_chars:
        sc_chars = set(jp_chars) if jp_chars else set(valid_chars)
    if not tc_chars:
        tc_chars = set(jp_chars) if jp_chars else set(valid_chars)

    return {
        "jp": sorted(jp_chars),
        "sc": sorted(sc_chars),
        "tc": sorted(tc_chars),
    }
