#!/usr/bin/env python3
"""Merge translation parts and source into dist1.json."""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "data" / "distinction_manual" / "dist1_source.json"
OUT = ROOT / "data" / "distinction_manual" / "dist1.json"
PARTS_DIR = ROOT / "data" / "distinction_manual"
PART_FILES = [
    "dist1_trans_part1.py",
    "dist1_trans_part2.py",
    "dist1_trans_part3.py",
    "dist1_trans_part4.py",
]


def load_translations(path: Path) -> dict[int, dict]:
    spec = importlib.util.spec_from_file_location(path.stem, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[path.stem] = module
    spec.loader.exec_module(module)
    return module.TRANSLATIONS


def main() -> None:
    translations: dict[int, dict] = {}
    for name in PART_FILES:
        part = PARTS_DIR / name
        batch = load_translations(part)
        overlap = set(translations) & set(batch)
        if overlap:
            raise SystemExit(f"Duplicate keys in {name}: {sorted(overlap)[:10]}")
        translations.update(batch)

    with open(SOURCE, encoding="utf-8") as f:
        source = json.load(f)

    missing = [w["number"] for w in source if w["number"] not in translations]
    if missing:
        raise SystemExit(f"Missing translations: {missing[:20]}... ({len(missing)} total)")

    result = []
    for word in source:
        n = word["number"]
        t = translations[n]
        result.append({
            "number": n,
            "headword": word["headword"],
            "nativeDefinition": t["nativeDefinition"],
            "japaneseMeaning": t["japaneseMeaning"],
            "etymology": t["etymology"],
            "examples": t["examples"],
        })

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
        f.write("\n")

    print(f"Wrote {len(result)} words to {OUT}")


if __name__ == "__main__":
    main()
