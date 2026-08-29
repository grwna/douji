# Character Mapping Data

This document describes how `dataset.json` is built from open-source linguistic datasets, and how to rebuild it.

## Data Sources

The dataset is compiled from three open-source linguistic databases:

| Source | Files Used | What It Provides |
|---|---|---|
| [OpenCC](https://github.com/BYVoid/OpenCC) | `STCharacters.txt`, `TSCharacters.txt`, `JPVariants.txt` | Character equivalence mappings across Simplified Chinese, Traditional Chinese, and Japanese Shinjitai/Kyūjitai |
| [Unicode Unihan](https://www.unicode.org/Public/UNIDATA/Unihan.zip) | `Unihan_Readings.txt` | Mandarin Pinyin (`kMandarin`), Japanese On'yomi (`kJapaneseOn`), Japanese Kun'yomi (`kJapaneseKun`) |

### OpenCC Tables

- **`STCharacters.txt`** — Simplified → Traditional character mappings. Each line maps one simplified character to one or more traditional equivalents.
- **`TSCharacters.txt`** — Traditional → Simplified character mappings. The reverse direction.
- **`JPVariants.txt`** — Japanese Shinjitai ↔ Traditional (Kyūjitai) mappings. Maps modern Japanese simplified kanji to their traditional forms.

Format: tab-separated, one mapping per line:
```
源	源字1 源字2
气	氣
```

### Unihan Readings

- **`Unihan_Readings.txt`** — Part of the Unicode Consortium's Unihan database. Contains per-character readings across languages.
- Properties used:
  - `kMandarin` — Tone-marked Pinyin readings (e.g., `qì`)
  - `kJapaneseOn` — On'yomi in uppercase romaji (e.g., `KI`, `KE`), converted to Katakana by the build script
  - `kJapaneseKun` — Kun'yomi in lowercase romaji with okurigana dots (e.g., `yasu.i`), converted to Hiragana by the build script

Format: tab-separated, one property per line:
```
U+6C17	kMandarin	qì
U+6C17	kJapaneseOn	KI KE
U+6C17	kJapaneseKun	iki
```

## Build Pipeline

The build process has 5 steps, implemented in [`scripts/build_dataset.py`](../../scripts/build_dataset.py):

### Step 1: Build Character Equivalence Clusters

All three OpenCC tables are parsed. Each source→target pair creates a bidirectional edge in a **union-find (disjoint set)** data structure. Characters connected through any chain of mappings end up in the same cluster.

Example: `気` → `氣` (from JPVariants) and `气` → `氣` (from STCharacters) puts `{気, 气, 氣}` into one cluster.

### Step 2: Classify Characters (JP / SC / TC)

Each character in a cluster is assigned regional roles based on which OpenCC table it appeared in as a **source**:

| Role | Classification Rule |
|---|---|
| **JP** (Japanese) | Source in `JPVariants.txt` (Shinjitai forms) |
| **SC** (Simplified Chinese) | Source in `STCharacters.txt` |
| **TC** (Traditional Chinese) | Source in `TSCharacters.txt` |

Characters not appearing in any table as a source are assigned to whichever roles are still empty (they're identical across standards).

### Step 3: Enrich with Readings

For every character in each cluster, `Unihan_Readings.txt` is queried for:
- Pinyin (from `kMandarin`)
- On'yomi (from `kJapaneseOn`, converted from romaji → Katakana)
- Kun'yomi (from `kJapaneseKun`, converted from romaji → Hiragana with okurigana dots preserved)

Readings from all characters in the cluster are merged and deduplicated.

### Step 4: Build Inverted Index

Every character appearing in any cluster's `jp`, `sc`, or `tc` list becomes a top-level key in the output JSON, pointing to the full cluster data. This enables O(1) lookup by any variant form.

### Step 5: Write Output

The result is written to `data/dataset.json` as a single-line minified JSON file.

## Output Format

Each top-level key is a single character. The value contains the full cluster:

```json
{
  "気": {
    "jp": ["気"],
    "sc": ["气"],
    "tc": ["氣"],
    "pinyin": ["qì", "qǐ"],
    "onyomi": ["キ", "ケ"],
    "kunyomi": ["いき"]
  }
}
```

- `jp`, `sc`, `tc` — Lists of variant characters for each standard (usually 1 element, occasionally more)
- `pinyin` — Tone-marked Mandarin readings
- `onyomi` — Japanese On readings in Katakana
- `kunyomi` — Japanese Kun readings in Hiragana (with okurigana dots)
- All list fields may be empty arrays

## How to Rebuild

### Prerequisites
- Python 3.8+
- Internet access (for downloading source files)

### Steps

```bash
# From the project root (douji/)

# Run full pipeline (downloads sources, builds dataset, cleans up temp files)
python3 scripts/build_dataset.py

# Optional: keep downloaded raw sources for debugging
python3 scripts/build_dataset.py --keep-sources
```

All source URLs and filenames are configured in [`scripts/dataset_builder/sources.json`](../../scripts/dataset_builder/sources.json).

### Output Stats (approximate)

| Metric | Value |
|---|---|
| Total indexed characters (keys) | ~9,700 |
| Unique equivalence clusters | ~5,500 |
| Characters with Japanese readings | ~3,200 |
| Characters with Pinyin | ~9,400 |
| Three-way different characters (JP ≠ SC ≠ TC) | ~540 |
| All-identical characters (JP = SC = TC) | ~3,200 |
| Output file size | ~980 KB |

## Notes

- `mappings.json` is a read-only precompiled artifact. Modifying lookup behavior means rebuilding the file, not editing it in place.
- Multi-character compound words are not included; only single CJK ideographs are mapped.
- The `scripts/sources/` directory is gitignored since the source files can be re-downloaded at any time.
