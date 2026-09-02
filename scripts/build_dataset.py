"""Orchestrate downloading, clustering, enrichment, and output generation."""
import argparse
import json
import shutil
from pathlib import Path

from dataset_builder import (
    build_variant_graph,
    classify_cluster,
    enrich_cluster,
    fetch_all_sources,
    load_sources_config,
    parse_opencc_file,
    parse_unihan_readings,
    parse_unihan_definitions,
)

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
OUTPUT_PATH = PROJECT_ROOT / "data" / "dataset.json"
SOURCES_DIR = SCRIPT_DIR / "sources"
CONFIG_PATH = SCRIPT_DIR / "dataset_builder" / "sources.json"


def main() -> None:
    parser = argparse.ArgumentParser(description="Build dataset.json")
    parser.add_argument("--keep-sources", action="store_true", help="Keep downloaded raw sources")
    args = parser.parse_args()

    print("--- 1. Fetching raw sources ---")
    config = load_sources_config(CONFIG_PATH)
    fetch_all_sources(SOURCES_DIR, CONFIG_PATH)

    opencc_cfg = config.get("opencc", {}).get("files", {})
    st_path = SOURCES_DIR / opencc_cfg.get("st_characters", "STCharacters.txt")
    ts_path = SOURCES_DIR / opencc_cfg.get("ts_characters", "TSCharacters.txt")
    jp_path = SOURCES_DIR / opencc_cfg.get("jp_variants", "JPShinjitaiCharacters.txt")
    unihan_path = SOURCES_DIR / "Unihan_Readings.txt"

    print("\n--- 2. Parsing readings and building variant clusters ---")
    readings = parse_unihan_readings(unihan_path)
    definitions = parse_unihan_definitions(unihan_path)

    uf = build_variant_graph([st_path, ts_path, jp_path])
    clusters = uf.clusters()

    st_map = dict(parse_opencc_file(st_path))
    ts_map = dict(parse_opencc_file(ts_path))
    jp_map = dict(parse_opencc_file(jp_path))

    classified_clusters = []
    for _root, chars in clusters.items():
        classified = classify_cluster(chars, st_map, ts_map, jp_map, readings=readings)
        if classified["jp"] or classified["sc"] or classified["tc"]:
            classified_clusters.append(classified)

    print(f"Total clusters: {len(classified_clusters)}")

    print("\n--- 3. Enriching with readings and definitions ---")
    
    opencc_assigned_chars = set(uf.parent.keys())
    for c in classified_clusters:
        opencc_assigned_chars.update(c.get("jp", []))
        opencc_assigned_chars.update(c.get("sc", []))
        opencc_assigned_chars.update(c.get("tc", []))
        
    all_unihan_chars = set(readings.keys()).union(set(definitions.keys()))
    for ch in all_unihan_chars:
        if ch not in opencc_assigned_chars:
            classified_clusters.append({
                "jp": [ch],
                "sc": [ch],
                "tc": [ch]
            })

    output = {}
    for cluster_data in classified_clusters:
        enriched = enrich_cluster(cluster_data, readings, definitions)
        all_chars = set(enriched["jp"] + enriched["sc"] + enriched["tc"])
        for ch in all_chars:
            if ch not in output:
                output[ch] = enriched

    print(f"Total indexed characters: {len(output)}")

    print("\n--- 4. Writing dataset ---")
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False)
    size_kb = OUTPUT_PATH.stat().st_size / 1024
    print(f"Saved: {OUTPUT_PATH} ({size_kb:.1f} KB)")

    if not args.keep_sources and SOURCES_DIR.exists():
        print("\n--- 5. Cleaning up temporary sources ---")
        shutil.rmtree(SOURCES_DIR)
        print(f"Removed {SOURCES_DIR}")

    print("\nBuild complete.")


if __name__ == "__main__":
    main()
