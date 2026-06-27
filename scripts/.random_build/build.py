#!/usr/bin/env python3
"""Merge translation parts and write random.json."""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "data" / "distinction_manual" / "random_source.json"
OUT = ROOT / "data" / "distinction_manual" / "random.json"
BUILD_DIR = Path(__file__).resolve().parent


def load_part(name: str) -> dict:
    path = BUILD_DIR / name
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    part_name = name.replace(".py", "").upper()
    return getattr(mod, part_name)


def main() -> None:
    translations = {}
    for part in ("part1.py", "part2.py", "part3.py", "part4.py"):
        translations.update(load_part(part))

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
        print(f"Missing: {missing}", file=sys.stderr)
        sys.exit(1)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
        f.write("\n")

    print(f"Wrote {len(result)} words to {OUT}")


if __name__ == "__main__":
    main()
