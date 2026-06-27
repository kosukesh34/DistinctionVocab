#!/usr/bin/env python3
"""Merge dist1 translation parts and write dist1.json."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "data" / "distinction_manual" / "dist1_source.json"
OUT = ROOT / "data" / "distinction_manual" / "dist1.json"
PARTS_DIR = Path(__file__).resolve().parent / "dist1_parts"

sys.path.insert(0, str(PARTS_DIR))
from part1 import PART1  # noqa: E402
from part2 import PART2  # noqa: E402
from part3 import PART3  # noqa: E402
from part4 import PART4  # noqa: E402

TRANSLATIONS = {**PART1, **PART2, **PART3, **PART4}


def main() -> None:
    with open(SOURCE, encoding="utf-8") as f:
        source = json.load(f)

    result = []
    missing = []
    for word in source:
        n = word["number"]
        if n not in TRANSLATIONS:
            missing.append(n)
            continue
        t = TRANSLATIONS[n]
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
