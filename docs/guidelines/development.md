# Development Guide

## Project Layout

```
project/
├── __init__.py              # Addon entry point — registers Anki hooks
├── manifest.json            # Anki metadata + version number
├── config.json              # User-facing default config (Anki reads this)
├── backend/
│   ├── config.py            # ConfigManager — reads Anki addonManager settings
│   ├── engine.py            # LookupEngine — coordinates providers
│   ├── bridge.py            # BridgeManager — JS↔Python bridge + asset injection
│   └── providers/
│       ├── base.py          # BaseLookupProvider (ABC)
│       └── variant_provider.py  # Reads char_variants.json, does lookups
├── web/
│   ├── tooltip.js           # Frontend IIFE — all tooltip logic
│   └── tooltip.css          # Tooltip styles
├── data/
│   └── char_variants.json   # Precompiled character variant data (~1MB)
├── tests/
│   └── test_lookup.py       # Unit tests (run via `python test_lookup.py`)
└── docs/
    └── guidelines/          # You are here
```

## Running Tests

Tests do not require Anki installed. Run from the `tests/` directory:

```bash
cd tests && python test_lookup.py -v
```

> [!WARNING]
> Do **not** run `pytest` from the project root — the root `__init__.py` imports
> `aqt` (Anki's Qt layer) which is unavailable outside Anki.

## Development Loop

Install the addon into Anki by placing (or symlinking) this directory into
Anki's addons folder:

- **Linux/macOS**: `~/.local/share/Anki2/addons21/<package_name>/`
- **Windows**: `%APPDATA%\Anki2\addons21\<package_name>\`

After editing Python files, reload via **Tools → Check Database**, or restart
Anki. After editing `tooltip.js` or `tooltip.css`, the next card render picks
up changes automatically — no restart needed, as assets are read from disk on
each injection.

## Adding a Feature

### New config option

**1. Add to `DEFAULT_CONFIG` in `backend/config.py`:**
```python
DEFAULT_CONFIG = {
    ...
    "my_new_option": True,
}
```

**2. Add to `config.json` (user-visible defaults):**
```json
{ "my_new_option": true }
```

**3. Document in `config.md`.**

**4. Consume in `tooltip.js`** — `config` is populated from
`window.DOUJI_INITIAL_CONFIG` at startup. No other wiring needed.

### New lookup data field

**1. Add to `VariantMappingProvider.lookup()` return dict** in `variant_provider.py`.

**2. Consume in `renderTooltip()` in `tooltip.js`.**

No engine changes needed unless you need a second provider (see below).

### New data provider

Create a new file in `backend/providers/` inheriting `BaseLookupProvider`:

```python
from .base import BaseLookupProvider

class MyProvider(BaseLookupProvider):
    def lookup(self, char: str) -> dict | None:
        ...
```

Register it in `__init__.py`:
```python
lookup_engine = LookupEngine(providers=[VariantMappingProvider(), MyProvider()])
```

The engine merges results — later providers fill in missing keys, never
overwrite keys set by earlier providers.

### New JS↔Python message type

**1. Add a handler in `BridgeManager.on_js_message()` in `bridge.py`:**
```python
if subcommand.startswith("mycommand:"):
    ...
    self._eval_js(context, callback_script)
    return (True, result)
```

**2. Send from JS using `pycmd`:**
```javascript
pycmd("douji:mycommand:" + payload);
```

**3. Handle the response via `window.DoujiBridge.myCallback()`** —
register it in the `window.DoujiBridge` object in `tooltip.js`.

## Style Rules

- **Python**: Type-annotate all function
  signatures. No bare `except:`, always `except Exception:`.
- **JavaScript**: ES5-compatible (Anki's webview is QtWebEngine / older Chromium —
  avoid optional chaining, nullish coalescing, or template literals in
  injected code). Keep within the existing IIFE — no module system.
- **No build step**: `tooltip.js` is read as a raw string and eval'd. It must be
  a single self-contained file.
