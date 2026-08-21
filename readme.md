# Douji (同字)

**Douji (同字)** is an Anki add-on that instantly cross-references CJK characters across **Japanese (Kanji)**, **Simplified Chinese (Hanzi)**, and **Traditional Chinese (Hanzi)**. Hover over any character in the reviewer while holding a modifier key to view its regional variant forms alongside Mandarin Pinyin and Japanese Kana readings in a clean, Yomitan-inspired popup.

<!-- SCREENSHOT PLACEHOLDER -->
![Preview](assets/screenshot.png)

---

## Table of Contents

- [How to Use](#how-to-use)
- [Installation](#installation)
- [Configuration](#configuration)
- [Compatibility](#compatibility)
- [Troubleshooting & FAQ](#troubleshooting--faq)
- [Known Limitations](#known-limitations)
- [Future Plans](#future-plans)
- [License](#license)

---

## How to Use

Hold <kbd>Shift</kbd> (or your configured modifier key) and hover over any Hanzi or Kanji character on your cards. The tooltip will appear instantly with the cross-referenced forms and readings.

<!-- GIF PLACEHOLDER -->
![Hover Demo](assets/demo.gif)

- **Regional Variants**: Displays 🇯🇵 JP (Japanese), 🇨🇳 SC (Simplified Chinese), and 🇹🇼 TC (Traditional Chinese) forms.
- **Readings**: Displays tone-marked Pinyin (Mandarin) and On-yomi / Kun-yomi (Japanese Kana).
- **Target Scope**: Only CJK ideographs trigger lookups. Hovering over Kana (Hiragana/Katakana), Latin alphabet, numbers, or punctuation is automatically ignored with no popup.

---

## Installation

### Method 1: AnkiWeb (Recommended)
1. In Anki, go to **Tools** → **Add-ons** → **Get Add-ons...**
2. Paste the Add-on Code: `<!-- ANKIWEB CODE PLACEHOLDER -->`
3. Click **OK** and restart Anki.

Ankiweb page: []()

### Method 2: Manual (.ankiaddon)
1. Download the latest `.ankiaddon` file from the [Releases](https://github.com/USER/REPO/releases) page.
2. Double-click the downloaded file or drag and drop it into Anki.
3. Restart Anki.

---

## Configuration

Customize behavior, keys, fonts, and appearance via **Tools** → **Add-ons** → select this add-on → **Config**.

| Option | Type | Default | Description |
|---|---|---|---|
| `modifier_key` | string | `"Shift"` | Trigger key (`"Shift"`, `"Alt"`, `"Control"`, `"None"`). |
| `theme` | string | `"auto"` | Theme style (`"auto"`, `"light"`, `"dark"`). |
| `popup_delay_ms` | integer | `30` | Hover debounce delay in milliseconds. |
| `character_font_size` | integer | `24` | Font size (px) for main characters and variant glyphs. |
| `reading_font_size` | integer | `13` | Font size (px) for readings text. |
| `bold_characters` | boolean | `true` | Display variant characters in bold weight. |
| `japanese_font` | string | `"Yu Gothic, ..."` | CSS font family for Japanese Kanji (`JP`). |
| `chinese_font` | string | `"'Microsoft YaHei', ..."` | CSS font family for Chinese Hanzi (`SC`, `TC`). |
| `popup_min_width` | integer | `220` | Minimum tooltip width in pixels. |
| `popup_max_width` | integer | `320` | Maximum tooltip width in pixels. |
| `show_pinyin` | boolean | `true` | Toggle Mandarin Pinyin display. |
| `show_readings` | boolean | `true` | Toggle Japanese Kana readings display. |

> **Note:** `"None"` triggers on every hover without any key pressed, which may cause popup spam while reading.

For detailed explanations of all settings, see [`config.md`](config.md).


---

## Compatibility
- **Tested Version**: Anki 25.09+ (Qt6 / Python 3.13 / Chromium 122)
- **Operating Systems**: Windows, macOS, Linux
- **Platform**: Desktop Anki only (AnkiMobile for iOS, AnkiDroid for Android, and AnkiWeb are unsupported because Python add-ons run strictly in desktop Qt environments)

---

## Troubleshooting & FAQ

#### The popup doesn't appear when hovering over text
- Ensure you are holding down the configured `modifier_key` (default: <kbd>Shift</kbd>).
- Verify that your card template CSS does not have `user-select: none;` or `pointer-events: none;` on the text container, which prevents browser caret hit-testing.
- Confirm the character is a Hanzi/Kanji ideograph (Kana, Latin characters, and punctuation do not trigger popups).

#### The popup appears underneath card elements or other add-ons
- Check if your card styling or third-party add-ons set excessive `z-index` values on parent containers that trap the tooltip layer.

#### A character shows "No cross-reference found"
- The character is likely an unmapped rare variant or outside the 9,688 character cluster dataset.

---

## Known Limitations

- **Single-character lookup**: Cross-referencing operates on individual CJK ideographs rather than multi-character compound words.
- **Desktop Anki only**: Requires the desktop Qt webview reviewer.
- **Dataset coverage**: Covers 9,688 character clusters from common Japanese Joyo/Jinmeiyo and Chinese standard character sets; extremely rare or archaic historical variants may not be mapped.

---

## Future Plans

- **Dictionary & Definitions**: Direct integration with external dictionary providers (e.g., CEDICT, JMdict, Jitendex) for on-hover definitions and vocabulary breakdown.
- **Audio pronunciation**: Native audio playback support for Pinyin and Japanese readings.
- **Stroke order diagrams**: Visual stroke order diagrams for Kanji/Hanzi comparisons.

---

## License

This project is licensed under the [GNU General Public License v3.0](LICENSE).
