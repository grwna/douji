# Release Workflow

This document provides a concise step-by-step guide to cutting an official release for **Douji (同字)** across Git, GitHub Actions, GitHub Releases, and AnkiWeb.

---

## TL;DR Quick Checklist

1. Bump `"version"` in `manifest.json` and move items from `[Unreleased]` into a dated release section in `CHANGELOG.md`.
2. Commit release metadata and create an annotated tag (`git tag -a vX.Y.Z`).
3. Push both the branch and tag to GitHub (`git push origin main && git push origin vX.Y.Z`).
4. **GitHub Actions automatically builds and publishes the GitHub Release** with the `.ankiaddon` artifact attached via [`.github/workflows/release.yaml`](../../.github/workflows/release.yaml).
5. Upload the generated `.ankiaddon` file (from local `./package.sh` or downloaded from the GitHub Release) to [AnkiWeb Shared Add-ons](https://ankiweb.net/shared/addons/).

---

## CI/CD Automation (`.github/workflows/release.yaml`)

This repository includes an automated GitHub Actions workflow for releases:

```
git push origin v1.0.0
       │
       ▼
GitHub Actions triggers (.github/workflows/release.yaml)
       │
       ├─► 1. Checks out repository
       ├─► 2. Sets up Python 3.13
       ├─► 3. Runs ./package.sh to build douji-<version>.ankiaddon
       └─► 4. Uses softprops/action-gh-release@v2 to:
             • Create official GitHub Release
             • Attach *.ankiaddon binary asset
             • Auto-generate release notes from commits/tags
```

> [!TIP]
> You do **not** need to manually draft a release or upload binaries on GitHub. Pushing the `v*` tag triggers the full build & publish pipeline automatically.

---

## Step-by-Step Release Process

### 1. Version Preparation & Changelog

1. Increment `"version"` in `manifest.json` following [Semantic Versioning](https://semver.org/):
   ```json
   {
     "name": "Douji",
     "package": "douji",
     "version": "1.0.0"
   }
   ```
2. Move staged items in `CHANGELOG.md` from `## [Unreleased]` into the target version header with the ISO 8601 release date (`YYYY-MM-DD`):
   ```markdown
   ## [1.0.0] - 2026-08-21

   ### Added
   - Initial public release of Douji (同字) tooltip inspector.
   ```

---

### 2. Optional: Local Verification & Artifact Build

You can verify the package locally before pushing:

```bash
chmod +x package.sh
./package.sh
```

**Output:** `douji-<version>.ankiaddon` at the project root.

---

### 3. Commit and Tag

Tagging marks a specific, immutable point in Git history. Pushing the tag triggers the CI release workflow.

```bash
# 1. Stage metadata and changelog
git add manifest.json CHANGELOG.md

# 2. Commit release preparation
git commit -m "chore(release): bump version to v1.0.0"

# 3. Create an annotated tag with release summary
git tag -a v1.0.0 -m "Release v1.0.0"

# 4. Push commit and tag to GitHub (Triggers GitHub Actions)
git push origin main
git push origin v1.0.0
```

---

### 4. Automated GitHub Release

Once you run `git push origin v1.0.0`:
1. Check the **Actions** tab on GitHub to monitor the `Publish GitHub Release` workflow.
2. Within ~1 minute, the workflow will complete and publish the release under **Releases** with `douji-1.0.0.ankiaddon` attached as a downloadable asset.

---

### 5. Publish to AnkiWeb

AnkiWeb currently does not offer an official upload API, so uploading to AnkiWeb is performed manually:

1. Log in to [AnkiWeb Shared Add-ons](https://ankiweb.net/shared/addons/).
2. **First Release:**
   - Click **Share an Add-on**.
   - Upload `douji-1.0.0.ankiaddon` (either generated locally from `./package.sh` or downloaded from the GitHub Release).
   - Fill in title, description, and save to obtain your numeric add-on code.
   - Update the code placeholder in `README.md`.
3. **Subsequent Releases:**
   - Click **Edit** on your existing add-on listing.
   - Upload the updated `.ankiaddon` file.
   - Update description and release notes as needed.

---

## Git Tag Management Cheat Sheet

| Action | Command |
|---|---|
| **List existing tags** | `git tag -n` |
| **Inspect tag details** (hash, author, date, message) | `git show v1.0.0` |
| **Delete a tag locally** (mistaken tag) | `git tag -d v1.0.0` |
| **Delete a remote tag on GitHub** | `git push origin --delete v1.0.0` |
| **Push all local tags at once** | `git push origin --tags` |
