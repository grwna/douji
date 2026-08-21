# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.0] - 2026-08-21

### Added
- Yomitan-style hover tooltip for CJK ideographs in the Anki reviewer.
- Cross-reference variant display for Japanese (JP), Simplified Chinese (SC), and Traditional Chinese (TC).
- Tone-marked Mandarin Pinyin readings.
- Japanese On-yomi and Kun-yomi Kana readings.
- Visual accent highlighting on hovered character row when all three regional forms differ.
- Precompiled database of 9,688 character clusters covering common Hanzi and Kanji (`char_variants.json`).
- Pluggable backend lookup engine architecture (`BaseLookupProvider`, `LookupEngine`, `VariantMappingProvider`).
- Configurable settings via Anki Add-on Manager:
  - `modifier_key` (Shift, Alt, Control, None)
  - `theme` (auto, light, dark)
  - `popup_delay_ms` debounce delay
  - `character_font_size` and `reading_font_size`
  - `bold_characters` toggle
  - `japanese_font` and `chinese_font` CSS font families
  - `popup_min_width` and `popup_max_width`
  - `show_pinyin` and `show_readings` display toggles
- Dark mode support automatically matching Anki's native night mode.
- Unit test suite for character resolution and variant matching.
- Automated packaging script (`package.sh`) producing `.ankiaddon` releases.

[unreleased]: https://github.com/USER/REPO/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/USER/REPO/releases/tag/v1.0.0
