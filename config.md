# Configuration Options

### `modifier_key` (string)
- Key to hold while hovering.
- Values: `"Shift"`, `"Alt"`, `"Control"`, `"None"`. Default: `"Shift"`.

### `character_font_size` (integer)
- Font size in pixels for the main character and variant glyphs (`JP`, `SC`, `TC`).
- Default: `24`.

### `reading_font_size` (integer)
- Font size in pixels for smaller text (Pinyin, Kana readings).
- Default: `13`.

### `bold_characters` (boolean)
- Whether characters are displayed in bold weight (`700`) or normal weight (`400`).
- Default: `true`.

### `japanese_font` (string)
- Font family CSS string used to render Japanese Kanji (`JP`).
- Default: `"Yu Gothic, Meiryo, 'Hiragino Sans', sans-serif"`.

### `chinese_font` (string)
- Font family CSS string used to render Chinese Hanzi (`SC` and `TC`).
- Default: `"'Microsoft YaHei', 'PingFang SC', 'Source Han Sans CN', sans-serif"`.

### `popup_min_width` & `popup_max_width` (integer)
- Minimum and maximum width of the popup in pixels.
- Defaults: `220` and `320`.

### `theme` (string)
- Color scheme: `"auto"` (matches Anki night mode), `"dark"`, `"light"`. Default: `"auto"`.

### `popup_delay_ms` (integer)
- Hover debounce delay in milliseconds. Default: `30`.

### `show_pinyin` & `show_readings` (boolean)
- Toggles for displaying Pinyin and Japanese Kana readings. Defaults: `true`.
