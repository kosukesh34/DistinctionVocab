#!/usr/bin/env python3
"""Generate earlybird.json from source + embedded translations."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "data" / "distinction_manual" / "earlybird_source.json"
OUT = ROOT / "data" / "distinction_manual" / "earlybird.json"
PARTS_DIR = ROOT / "data" / "distinction_manual" / "_parts"


def load_translations() -> dict[int, dict]:
    merged: dict[int, dict] = {}
    for part_file in sorted(PARTS_DIR.glob("part_*.json")):
        with open(part_file, encoding="utf-8") as f:
            chunk = json.load(f)
        for entry in chunk:
            merged[entry["number"]] = entry
    return merged


def main() -> None:
    with open(SOURCE, encoding="utf-8") as f:
        source = json.load(f)

    translations = load_translations()
    result = []
    missing = []

    for word in source:
        n = word["number"]
        t = translations.get(n)
        if not t:
            missing.append(n)
            continue
        result.append({
            "number": n,
            "headword": word["headword"],
            "nativeDefinition": t["nativeDefinition"],
            "japaneseMeaning": t["japaneseMeaning"],
            "etymology": t["etymology"],
            "examples": t["examples"],
        })

    if missing:
        raise SystemExit(
            f"Missing translations for: {missing[:20]}{'...' if len(missing) > 20 else ''} ({len(missing)} total)"
        )

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
        f.write("\n")

    print(f"Wrote {len(result)} words to {OUT}")


if __name__ == "__main__":
    main()
