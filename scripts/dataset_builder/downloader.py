"""Download raw source datasets using sources.json configuration."""
import io
import json
import urllib.request
import zipfile
from pathlib import Path

PACKAGE_DIR = Path(__file__).resolve().parent
SOURCES_CONFIG = PACKAGE_DIR / "sources.json"


def load_sources_config(config_path: Path = SOURCES_CONFIG) -> dict:
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)


def download_file(url: str, dest: Path) -> None:
    print(f"  Downloading {url}")
    urllib.request.urlretrieve(url, dest)
    size_kb = dest.stat().st_size / 1024
    print(f"  Saved {dest.name} ({size_kb:.1f} KB)")


def fetch_all_sources(dest_dir: Path, config_path: Path = SOURCES_CONFIG) -> None:
    dest_dir.mkdir(parents=True, exist_ok=True)
    config = load_sources_config(config_path)

    opencc = config.get("opencc", {})
    base_url = opencc.get("base_url", "")
    for filename in opencc.get("files", {}).values():
        url = f"{base_url}/{filename}"
        download_file(url, dest_dir / filename)

    unihan = config.get("unihan", {})
    unihan_url = unihan.get("url")
    extract_files = unihan.get("extract_files", [])
    if unihan_url and extract_files:
        print(f"  Fetching {unihan_url}")
        resp = urllib.request.urlopen(unihan_url)
        with zipfile.ZipFile(io.BytesIO(resp.read())) as zf:
            for target in extract_files:
                if target in zf.namelist():
                    zf.extract(target, dest_dir)
                    size_kb = (dest_dir / target).stat().st_size / 1024
                    print(f"  Extracted {target} ({size_kb:.1f} KB)")


if __name__ == "__main__":
    target_dir = PACKAGE_DIR.parent / "sources"
    fetch_all_sources(target_dir)
