#!/usr/bin/env python3
"""Assemble vibe.json from translation parts."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "data" / "distinction_manual" / "vibe_source.json"
OUT = ROOT / "data" / "distinction_manual" / "vibe.json"
SCRIPTS = Path(__file__).resolve().parent


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main() -> None:
    base = load_module("vtd", SCRIPTS / "vibe_translations_data.py")
    p51 = load_module("p51", SCRIPTS / "_vibe_t51_120.py")
    p101 = load_module("p101", SCRIPTS / "_vibe_t101_200.py")
    p201 = load_module("p201", SCRIPTS / "_vibe_t201_300.py")
    p301 = load_module("p301", SCRIPTS / "_vibe_t301_400.py")

    translations: dict[int, dict] = {}
    translations.update(base.TRANSLATIONS)
    translations.update(p51.T51_120)
    translations.update(p101.T101_200)
    translations.update(p201.T201_300)
    translations.update(p301.T301_400)

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
        raise SystemExit(f"Missing: {missing}")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
        f.write("\n")

    print(f"Wrote {len(result)} words to {OUT}")


if __name__ == "__main__":
    main()
