# Character Mapping Data

This document describes how `dataset.json` is built from open-source linguistic datasets, and how to rebuild it.

## Data Sources

The dataset is compiled from two open-source linguistic databases:

| Dataset | Source Name | Role |
| :--- | :--- | :--- |
| OpenCC | `STCharacters.txt`, `TSCharacters.txt`, `JPShinjitaiCharacters.txt` | Character equivalence mappings across Simplified Chinese, Traditional Chinese, and Japanese Shinjitai/Kyūjitai |
| Unihan | `Unihan_Readings.txt` | Core readings (Mandarin, Japanese On/Kun) and English definitions |

### OpenCC Tables

- **`STCharacters.txt`** — Simplified → Traditional character mappings. Each line maps one simplified character to one or more traditional equivalents.
- **`TSCharacters.txt`** — Traditional → Simplified character mappings. The reverse direction.
- **`JPShinjitaiCharacters.txt`** — Japanese Shinjitai → Traditional (Kyūjitai) mappings. Maps modern Japanese simplified kanji to their traditional forms.

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

Example: `気` → `氣` (from `JPShinjitaiCharacters.txt`) and `气` → `氣` (from `STCharacters.txt`) puts `{気, 气, 氣}` into one cluster.

### Step 2: Classify Characters (JP / SC / TC)

Each character in an OpenCC cluster is assigned regional roles using both source and target sides of the mapping dictionaries:

| Role | Classification Rule |
|---|---|
| **SC** (Simplified Chinese) | Sources in `STCharacters.txt` or Targets in `TSCharacters.txt` |
| **TC** (Traditional Chinese) | Sources in `TSCharacters.txt` or Targets in `STCharacters.txt` / `JPShinjitaiCharacters.txt` |
| **JP** (Japanese) | Sources in `JPShinjitaiCharacters.txt` |

**Japanese Role Disambiguation**:
When a cluster has no explicit entry in `JPShinjitaiCharacters.txt` (common when Simplified Chinese merged several traditional forms into a base glyph that Japanese also uses as standard Joyo kanji, e.g. `家`/`傢`, `私`/`俬`, `出`/`齣`):
1. The builder prioritizes characters that have native Japanese Kun'yomi (`kJapaneseKun`) or On'yomi (`kJapaneseOn`) in Unihan.
2. If `sc` characters have Kun'yomi readings, they are assigned to `jp`.
3. If still empty, it falls back to `sc`, then `tc`.

### Step 3: Enrich with Readings and Meanings

For every character in each cluster, `Unihan_Readings.txt` is queried for:
- Pinyin (from `kMandarin`)
- On'yomi (from `kJapaneseOn`, converted from romaji → Katakana)
- Kun'yomi (from `kJapaneseKun`, converted from romaji → Hiragana with okurigana dots preserved)
- English Meaning (from `kDefinition`)

**Definition Sanitization Pipeline**:
Raw Unihan definition strings undergo strict filtering to prevent tooltip overflow and remove noise:
1. Strip parentheticals (e.g., `(simplified form of...)`).
2. Split into tokens on `;` and `,`.
3. Filter out tokens containing uppercase letters (`[A-Z]`, e.g., proper names, dynasty trivia).
4. Filter out tokens containing raw CJK glyphs (`[\u4e00-\u9fff...]`).
5. Filter out tokens longer than 3 words.
6. Case-insensitively deduplicate and cap at 4 tokens joined by `"; "`.

### Step 4: Inject Invariant Singletons & Build Inverted Index

1. **Singleton Fallback**: Any character present in Unihan readings/definitions that was not involved in any OpenCC mapping table is added as a singleton cluster (`jp == sc == tc`, e.g. `表`, `作`, `感`).
2. **Precedence Protection**: OpenCC-derived multi-character clusters strictly take precedence during inverted index generation to prevent singleton collisions from overwriting valid variant clusters.
3. Every character appearing in any cluster's `jp`, `sc`, or `tc` list becomes a top-level key in the output JSON.

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
    "kunyomi": ["いき"],
    "meaning": "steam; vapor; air; gas"
  }
}
```

- `jp`, `sc`, `tc` — Lists of variant characters for each standard (usually 1 element, occasionally more)
- `pinyin` — Tone-marked Mandarin readings
- `onyomi` — Japanese On readings in Katakana
- `kunyomi` — Japanese Kun readings in Hiragana (with okurigana dots)
- `meaning` — Unified English definition string
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
| Total indexed characters (keys) | ~45,700 |
| Unique equivalence clusters | ~45,700 |
| Characters with Japanese readings | ~14,000 |
| Characters with Pinyin | ~45,000 |
| Three-way different characters (JP ≠ SC ≠ TC) | ~540 |
| All-identical characters (JP = SC = TC) | ~41,000 |
| Output file size | ~6.5 MB |

## Notes

- `mappings.json` is a read-only precompiled artifact. Modifying lookup behavior means rebuilding the file, not editing it in place.
- Multi-character compound words are not included; only single CJK ideographs are mapped.
- The `scripts/sources/` directory is gitignored since the source files can be re-downloaded at any time.
