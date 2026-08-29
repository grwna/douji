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
) -> Dict[str, List[str]]:
    jp_chars = set()
    sc_chars = set()
    tc_chars = set()

    for ch in chars:
        if not is_cjk(ch):
            continue
        if ch in jp_map:
            jp_chars.add(ch)
        if ch in st_map:
            sc_chars.add(ch)
        if ch in ts_map:
            tc_chars.add(ch)

    unmapped = chars - jp_chars - sc_chars - tc_chars
    for ch in unmapped:
        if is_cjk(ch):
            if not jp_chars:
                jp_chars.add(ch)
            if not sc_chars:
                sc_chars.add(ch)
            if not tc_chars:
                tc_chars.add(ch)

    if not jp_chars and tc_chars:
        jp_chars = set(tc_chars)
    if not tc_chars and jp_chars:
        tc_chars = set(jp_chars)

    return {
        "jp": sorted(jp_chars),
        "sc": sorted(sc_chars),
        "tc": sorted(tc_chars),
    }
