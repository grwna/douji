# AnkiWeb Listing Information

---

### Title
```text
Douji (同字) - Instant Hanzi & Kanji Cross-Reference Tooltip
```

---

### Tags
```text
japanese chinese kanji hanzi yomitan lookup cross-reference pinyin kana
```

---

### Support Page
```text
https://github.com/grwna/douji/issues
```

---

### Description

```markdown
# Douji (同字)

**Douji (同字)** is an Anki add-on that instantly cross-references CJK characters across **Japanese (Kanji)**, **Simplified Chinese (Hanzi)**, and **Traditional Chinese (Hanzi)**.

Hover over any character in the reviewer while holding a modifier key to view its regional variant forms alongside Mandarin Pinyin and Japanese Kana readings in a clean, Yomitan-inspired popup.

<p align="center">
  <img src="https://raw.githubusercontent.com/grwna/douji/main/docs/assets/screenshot.png" width="560" alt="Douji Preview">
</p>

---

### Key Features

- **Regional Variants**: Shows 🇯🇵 **JP** (Japanese Kanji), 🇨🇳 **SC** (Simplified Chinese), and 🇹🇼 **TC** (Traditional Chinese) forms side-by-side.
- **Dynamic Accent Highlighting**: If all three regional forms differ (e.g. `気` vs `气` vs `氣` or `発` vs `发` vs `發`), the hovered variant row is automatically highlighted with an accent border.
- **Tone-Marked Readings**: Displays Mandarin Pinyin with tone marks and Japanese On-yomi / Kun-yomi readings in Kana.
- **Extensive Coverage**: Bundled with a precompiled database of **9,688 character clusters** covering all standard Joyo/Jinmeiyo Kanji and Chinese Hanzi.
- **Instant & Responsive**: Pure local in-memory lookup (<1ms), debounced hover detection, and automatic viewport edge-flipping.
- **Dark Mode**: Native palette adaptation matching Anki's dark / night mode.

---

### How to Use

1. Hold <kbd>Shift</kbd> (or your configured trigger key) while reviewing cards.
2. Hover the mouse over any Hanzi or Kanji character.
3. The cross-reference popup will appear instantly.

<p align="center">
  <img src="https://raw.githubusercontent.com/grwna/douji/main/docs/assets/demo.gif" width="560" alt="Hover Demo">
</p>

*Note: Kana (Hiragana/Katakana), Latin letters, numbers, and punctuation are automatically ignored.*

---

### Configuration

Customize options via **Tools** → **Add-ons** → select **Douji** → **Config**:

- `modifier_key`: Trigger key (`"Shift"`, `"Alt"`, `"Control"`, or `"None"`).
- `theme`: Color theme (`"auto"`, `"light"`, `"dark"`).
- `popup_delay_ms`: Hover delay in milliseconds (default: `30`).
- `character_font_size` & `reading_font_size`: Font sizes in pixels.
- `japanese_font` & `chinese_font`: Custom CSS font-family strings for regional glyphs.
- `show_pinyin` & `show_readings`: Toggle Pinyin / Kana readings display.

---

### Compatibility

- **Anki Version**: Anki 2.1.20+ (Qt5 and Qt6 supported, tested on Anki 25.09+).
- **Platform**: Desktop Anki only (Windows, macOS, Linux).

---

### Source Code & Support

- **GitHub Repository**: [github.com/grwna/douji](https://github.com/grwna/douji)
- **Bug Tracker / Report**: [github.com/grwna/douji/issues](https://github.com/grwna/douji/issues)
- **License**: GNU General Public License v3.0 (GPL-3.0)
```
