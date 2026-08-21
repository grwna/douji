#!/usr/bin/env bash
set -euo pipefail

# Locate script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Build the .ankiaddon package using Python's zipfile for consistent cross-platform packaging & exclusions
python3 - << 'EOF'
import json
import os
import zipfile
from pathlib import Path

root_dir = Path.cwd()
manifest_path = root_dir / "manifest.json"

if not manifest_path.exists():
    raise FileNotFoundError(f"manifest.json not found at {manifest_path}")

with open(manifest_path, "r", encoding="utf-8") as f:
    manifest = json.load(f)

package_name = manifest.get("package", "addon")
version = manifest.get("version", "1.0.0")
output_filename = f"{package_name}-{version}.ankiaddon"
output_path = root_dir / output_filename

# Items to include in the addon zip root
included_top_level = [
    "__init__.py",
    "manifest.json",
    "config.json",
    "config.md",
    "backend",
    "web",
    "data",
]

excluded_patterns = {
    "__pycache__",
    ".pytest_cache",
    ".DS_Store",
    "Thumbs.db",
}

print(f"Packaging {manifest.get('name', package_name)} v{version}...")

with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as zip_file:
    for item_name in included_top_level:
        item_path = root_dir / item_name
        if not item_path.exists():
            print(f"Warning: '{item_name}' does not exist, skipping.")
            continue

        if item_path.is_file():
            zip_file.write(item_path, arcname=item_name)
            print(f"  + {item_name}")
        elif item_path.is_dir():
            for root, dirs, files in os.walk(item_path):
                # Filter out excluded directories in-place
                dirs[:] = [d for d in dirs if d not in excluded_patterns]
                
                for file in files:
                    if file.endswith((".pyc", ".pyo")) or file in excluded_patterns:
                        continue
                    file_path = Path(root) / file
                    rel_path = file_path.relative_to(root_dir)
                    zip_file.write(file_path, arcname=str(rel_path))
                    print(f"  + {rel_path}")

print(f"\nSuccessfully built: {output_filename} ({output_path.stat().st_size / 1024:.1f} KB)")
EOF
