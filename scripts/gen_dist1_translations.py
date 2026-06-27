#!/usr/bin/env python3
"""Generate dist1.json from source + embedded translations."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "data" / "distinction_manual" / "dist1_source.json"
OUT = ROOT / "data" / "distinction_manual" / "dist1.json"
PARTS = [
    ROOT / "scripts" / ".dist1_translations_part1.json",
    ROOT / "scripts" / ".dist1_translations_part2.json",
    ROOT / "scripts" / ".dist1_translations_part3.json",
    ROOT / "scripts" / ".dist1_translations_part4.json",
]


def main() -> None:
    translations: dict[int, dict] = {}
    for part in PARTS:
        with open(part, encoding="utf-8") as f:
            translations.update({int(k): v for k, v in json.load(f).items()})

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
        raise SystemExit(f"Missing: {missing[:20]}... ({len(missing)} total)")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
        f.write("\n")

    print(f"Wrote {len(result)} words to {OUT}")


if __name__ == "__main__":
    main()
