# Versioning

This project follows [Semantic Versioning](https://semver.org/) and [Keep a Changelog](https://keepachangelog.com/).

## Version Number Rules

```
MAJOR.MINOR.PATCH
```

| Bump | When |
|------|------|
| `PATCH` | Bug fixes, no behavior change for the user |
| `MINOR` | New config options, new features, backward compatible |
| `MAJOR` | Breaking changes — config key renames, removed behavior, anything requiring user action |

> [!NOTE]
> This addon targets individual users, not libraries. A "breaking change" means
> something that would silently break or require the user to manually update their
> config. When in doubt, bump `MINOR`.

## Release Checklist

**1. Bump version in `manifest.json`**
```json
{ "version": "1.2.0" }
```
This is the single source of truth. Anki reads it directly.

**2. Update `CHANGELOG.md`**

Move items from `[Unreleased]` into a new dated section:

```markdown
## [1.2.0] - 2025-03-15

### Added
- `show_readings` config toggle for Japanese kana readings.

### Fixed
- Tooltip not dismissing on scroll inside card iframe.
```

Add the comparison link at the bottom of the file:
```markdown
[1.2.0]: https://github.com/grwna/douji/compare/v1.1.0...v1.2.0
```

**3. Commit and tag**
```bash
git add manifest.json CHANGELOG.md
git commit -m "chore: release v1.2.0"
git tag v1.2.0
git push && git push --tags
```

**4. Package and publish**
```bash
bash package.sh   # produces douji-1.2.0.ankiaddon
```
- Upload `.ankiaddon` as the GitHub Release asset.

## Changelog Format

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.0] - 2025-01-01

### Added
- Initial release.

[unreleased]: https://github.com/grwna/douji/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/grwna/douji/releases/tag/v1.0.0
```

---

## Rules

- **Audience**: Write for users, not developers. "Tooltip now dismisses on scroll" not "fixed hideTooltip call in scroll handler."
- **Completeness**: Every released version must have an entry, even if it's just `- Minor internal changes.`
- **Chronology**: Latest version at the top. `[Unreleased]` is always the topmost section.
- **Dates**: `YYYY-MM-DD` format only — avoids regional ambiguity.
- **Linkability**: Every version header should be a hyperlink to its GitHub diff or tag (see format example above).
- **`[Unreleased]` as a staging area**: Document changes here as you make them — not retroactively before a release. When cutting a release, move its contents into the new version section and clear `[Unreleased]`.

## Change Type Labels

Use only these subsection headers — omit any that have no entries:

| Label | Use for |
|-------|---------|
| `Added` | New features |
| `Changed` | Changes to existing behavior |
| `Deprecated` | Features that will be removed in a future release |
| `Removed` | Features that have been removed |
| `Fixed` | Bug fixes |
| `Security` | Vulnerability fixes |

## Antipatterns

- **Dumping git log**: Commit messages make bad changelog entries — they're noisy, developer-centric, and often reference internal details. Summarize the user-visible delta.
- **Skipping deprecations**: Always document when a config key is renamed or behavior changes, so users know what to update.
- **Inconsistent updates**: Gaps in the changelog erode trust. If a version was released without a changelog entry, add one retroactively — even a brief one.
- **Yanked releases**: If a release is pulled due to a critical bug, still document it: `## [1.1.0] - 2025-01-10 [YANKED]` with a note explaining why.
