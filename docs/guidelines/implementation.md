# Implementation

## Overview

**Douji (同字)** is an Anki addon that shows a floating popup when the user
hovers over a CJK character in the Anki reviewer while holding the modifier key
(default: Shift). The popup displays the Japanese (JP), Simplified Chinese (SC),
and Traditional Chinese (TC) variant forms of that character, plus Pinyin and
Kana readings.

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Anki Reviewer Webview                    │
│                                                             │
│  [User holds Shift + hovers over character]                 │
│         │                                                   │
│         ▼                                                   │
│  [tooltip.js: caretRangeFromPoint extracts char]            │
│         │                                                   │
│         ▼                                                   │
│  [pycmd("douji:lookup:{"char": "気", "req_id": "5"}")]     │
└──────────────────────────┬──────────────────────────────────┘
                           │  (Anki bridge)
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                    Python Backend                           │
│                                                             │
│  BridgeManager.on_js_message()                              │
│    └─► LookupEngine.lookup(char)                            │
│          └─► VariantMappingProvider  ◄── char_variants.json │
│                (O(1) in-memory dict lookup)                 │
│  BridgeManager._eval_js() → JS callback with result        │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                   Tooltip Render                            │
│                                                             │
│  • 3-row variant layout: JP / SC / TC                       │
│  • Highlight hovered variant row if all 3 forms differ      │
│  • Pinyin and Kana readings section                         │
│  • Viewport edge-flip positioning                           │
└─────────────────────────────────────────────────────────────┘
```

---

## Startup Sequence

**1. Addon loads** (`__init__.py`):
- Instantiates `ConfigManager`, `LookupEngine`, `BridgeManager`.
- `LookupEngine` creates a `VariantMappingProvider`, which immediately loads
  `char_variants.json` (~981 KB, 9,688 character clusters) into `self._data`.
- Registers three Anki hooks: `webview_will_set_content`, `webview_did_receive_js_message`,
  and two reviewer card-flip hooks.

**2. Reviewer opens** → `inject_assets` hook fires:
- `BridgeManager` reads `tooltip.css` and `tooltip.js` from disk (cached after
  first read in `_file_cache`).
- Injects them into the webview `<head>` as inline `<style>` and `<script>`
  tags, along with `window.DOUJI_INITIAL_CONFIG`.
- The IIFE executes: binds `mousemove`/`keyup` event listeners, applies config CSS vars.

**3. Card flip** → `on_card_shown` hook fires:
- Evals a lightweight guard script checking `window.DoujiBridge`. If it
  already exists, nothing is re-injected. If the webview was reset (e.g. deck
  change), the full JS + CSS is injected again.

---

## Key Components

### `ConfigManager` (`backend/config.py`)
- Merges `DEFAULT_CONFIG` with user values from Anki's `addonManager` on startup.
- `get(key)` uses a sentinel `_UNSET` default — distinguishes "no default
  provided" from an explicit `default=None` call.
- `all()` returns a plain dict safe to pass to `json.dumps`.

### `LookupEngine` (`backend/engine.py`)
- Holds an ordered list of `BaseLookupProvider` instances.
- `lookup(char)` calls each provider and merges results: the first provider to
  return a key wins; later providers only fill in missing keys.
- Designed to accept additional providers (e.g. CEDICT, Jitendex) via
  `register_provider()` without changing the bridge or JS.

### `VariantMappingProvider` (`backend/providers/variant_provider.py`)
- Loads `char_variants.json` once at startup into `self._data`.
- `lookup(char)` takes `char[0]`, looks it up, and returns a result dict with:
  - `jp`, `sc`, `tc` — variant form lists
  - `pinyin`, `onyomi`, `kunyomi` — readings (may be empty lists)
  - `all_identical` — `True` when `jp[0] == sc[0] == tc[0]`
  - `all_different` — `True` when all three primary forms differ
  - `hovered_variant` — which of `"jp"` / `"sc"` / `"tc"` the input char belongs to
- Returns `{"found": False, ...}` for characters not in the dataset.

### `BridgeManager` (`backend/bridge.py`)
- **`inject_assets`**: Called once per reviewer webview. Builds and appends the
  `<head>` injection string.
- **`on_js_message`**: Anki hook receiving all `pycmd()` calls from JS. Routes
  messages prefixed `douji:` — currently handles `lookup:` and `config:`.
- **`_eval_js(context, script)`**: Sends JS to the webview. Tries `context.eval()`,
  then `context.web.eval()`, then falls back to `mw.reviewer.web.eval()`.
- **`_read_web_file(filename)`**: Reads from `web/`, caches in `_file_cache` dict.
  No repeated disk reads after first load.

### `tooltip.js` (`web/tooltip.js`)
- Single self-contained IIFE, ES5-compatible.
- **State variables**: `container`, `highlightOverlay`, `hoverTimer`,
  `currentRequestId`, `activeChar`, `activeCharRect`, `lastMousePos`.
- **`isCJKIdeograph(char)`**: Validates code point against known CJK Unicode blocks.
  Only characters in these ranges trigger a lookup.
- **`getCharFromPoint(x, y)`**: Uses `caretRangeFromPoint` / `caretPositionFromPoint`
  to resolve the exact character under the cursor from a text node. Returns
  `{char, rect}` or `null`.
- **`onMouseMove`**: Debounces the lookup via `hoverTimer` (default 30ms). Sends
  `pycmd("douji:lookup:...")` with a monotonic `req_id` — stale responses
  are silently discarded by comparing `req_id` to `currentRequestId`.
- **`window.DoujiBridge`**: The public callback API the Python side calls
  into. `onResult(data, reqId, charRect)` is the primary entry point.

---

## Data Format (`char_variants.json`)

**Coverage**: 9,688 character clusters across common Japanese Kanji and Chinese Hanzi.

**Sources**: OpenCC tables (JP/SC/TC variants), Joyo Kanji dataset (onyomi/kunyomi),
Unicode Pinyin data (tone-marked Mandarin).

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

Keys are single Unicode characters. All list fields may be empty arrays.
`jp`/`sc`/`tc` can contain multiple variant forms, but the tooltip displays
only `[0]` of each.

---

## Display Rules

- **Highlight**: Applied to the hovered variant row only when all 3 forms differ
  (e.g. 気/气/氣). When forms are identical (e.g. 人/人/人), all rows are shown
  without highlight.
- **Readings**: Pinyin and Kana rows are only rendered if data is present and the
  respective config toggle is enabled (`show_pinyin`, `show_readings`).
- **Positioning**: Tooltip appears below the character rect. Flips above if it
  would overflow the bottom edge. Clamps to left/right viewport margins.
- **Theme**: CSS variables auto-switch on Anki's `.night_mode` / `.nightMode`
  body class. Explicit `douji-theme-light` / `douji-theme-dark` classes override auto.

---

## Constraints

| Constraint | Why |
|-----------|-----|
| No build step for JS | `tooltip.js` is read as a raw string and eval'd by Python — it must be a single self-contained file |
| ES5-only JS | Anki's QtWebEngine version varies; no optional chaining `?.`, no nullish coalescing `??`, no template literals |
| `aqt` not importable in tests | Root `__init__.py` imports Anki at module level; tests bypass it via `sys.path` insertion from `tests/` |
| `char_variants.json` is read-only | It's a precompiled dataset — modifying lookup behavior means replacing or augmenting the file, not editing in place |

---

## Configuration

User-configurable via **Tools → Add-ons → Config** in Anki. All options are defined in
`backend/config.py` (`DEFAULT_CONFIG`) and mirrored in `config.json` (Anki reads this for
the config editor UI). Documented for end users in `config.md`.

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| `modifier_key` | string | `"Shift"` | Key to hold while hovering. `"Shift"`, `"Alt"`, `"Control"`, or `"None"` |
| `theme` | string | `"auto"` | `"auto"` follows Anki night mode, `"light"` or `"dark"` force a theme |
| `popup_delay_ms` | int | `30` | Debounce delay in ms before triggering a lookup |
| `character_font_size` | int | `24` | Font size (px) for the main char and JP/SC/TC variant glyphs |
| `reading_font_size` | int | `13` | Font size (px) for Pinyin and Kana reading text |
| `bold_characters` | bool | `false` | Renders variant characters at weight 700 when true |
| `japanese_font` | string | `"Yu Gothic, ..."` | CSS font-family for the JP variant glyph |
| `chinese_font` | string | `"Microsoft YaHei, ..."` | CSS font-family for SC and TC variant glyphs |
| `popup_min_width` | int | `220` | Minimum tooltip width in px |
| `popup_max_width` | int | `320` | Maximum tooltip width in px |
| `show_pinyin` | bool | `true` | Show Mandarin Pinyin reading row |
| `show_readings` | bool | `true` | Show Japanese On-yomi / Kun-yomi reading row |

Config is passed to JS as `window.DOUJI_INITIAL_CONFIG` at injection time.
The JS `onConfig` bridge handler can update it at runtime without a page reload.

---

## Tests

Run from `tests/`: `python test_lookup.py -v`

| Test | What it verifies |
|------|-----------------|
| `test_all_different_characters` | `気`/`气`/`氣` — `all_different=True`, correct `jp`/`sc`/`tc` lists, `hovered_variant` set correctly |
| `test_all_identical_characters` | `人`/`人`/`人` — `all_identical=True`, `all_different=False` |
| `test_unmapped_character_empty_state` | `あ` — `found=False`, message field present, no crash |

The test suite covers the `LookupEngine` + `VariantMappingProvider` stack only — the bridge
and frontend have no automated tests (they require a live Anki webview).
