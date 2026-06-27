#!/usr/bin/env python3
"""Merge translation parts and write random.json."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "data" / "distinction_manual" / "random_source.json"
OUT = ROOT / "data" / "distinction_manual" / "random.json"
PARTS_DIR = Path(__file__).resolve().parent

PART_FILES = [
    PARTS_DIR / "random_manual_translations_p1.json",
    PARTS_DIR / "random_trans_51_100.json",
    PARTS_DIR / "random_trans_101_150.json",
    PARTS_DIR / "random_trans_151_200.json",
    PARTS_DIR / "random_trans_201_250.json",
    PARTS_DIR / "random_trans_251_300.json",
    PARTS_DIR / "random_trans_301_350.json",
    PARTS_DIR / "random_trans_351_400.json",
]


def main() -> None:
    translations: dict[int, dict] = {}
    for path in PART_FILES:
        if not path.exists():
            raise SystemExit(f"Missing part file: {path}")
        data = json.load(open(path, encoding="utf-8"))
        for k, v in data.items():
            translations[int(k)] = v

    with open(SOURCE, encoding="utf-8") as f:
        source = json.load(f)

    result = []
    missing = []
    for word in source:
        n = word["number"]
        if n not in translations:
            missing.append(n)
            continue
        t = translations[n]
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
