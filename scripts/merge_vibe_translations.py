#!/usr/bin/env python3
"""Merge vibe translation batches and build vibe.json."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "data" / "distinction_manual" / "vibe_source.json"
OUT = ROOT / "data" / "distinction_manual" / "vibe.json"
SCRIPTS = Path(__file__).resolve().parent

BATCH_FILES = sorted(SCRIPTS.glob("vibe_t_part*.json"))


def main() -> None:
    translations: dict[int, dict] = {}
    for path in BATCH_FILES:
        if not path.exists():
            raise FileNotFoundError(f"Missing batch file: {path}")
        with open(path, encoding="utf-8") as f:
            batch = json.load(f)
        for k, v in batch.items():
            translations[int(k)] = v

    with open(SOURCE, encoding="utf-8") as f:
        source = json.load(f)

    missing = [w["number"] for w in source if w["number"] not in translations]
    if missing:
        raise SystemExit(f"Missing {len(missing)} translations: {missing[:20]}...")

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

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
        f.write("\n")

    print(f"Wrote {len(result)} words to {OUT}")


if __name__ == "__main__":
    main()
