#!/usr/bin/env python3
"""Merge translation batches and build earlybird.json."""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "data" / "distinction_manual" / "earlybird_source.json"
OUT = ROOT / "data" / "distinction_manual" / "earlybird.json"
SCRIPTS = Path(__file__).resolve().parent

BATCH_MODULES = [
    "earlybird_manual_translations",
    "earlybird_t_51_100",
    "earlybird_t_101_150",
    "earlybird_t_151_200",
    "earlybird_t_201_250",
    "earlybird_t_251_300",
    "earlybird_t_301_350",
    "earlybird_t_351_400",
]


def load_module(name: str):
    path = SCRIPTS / f"{name}.py"
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main() -> None:
    translations: dict[int, dict] = {}
    for batch in BATCH_MODULES:
        path = SCRIPTS / f"{batch}.py"
        if not path.exists():
            print(f"Missing batch: {path.name}", file=sys.stderr)
            continue
        mod = load_module(batch)
        translations.update(mod.TRANSLATIONS)

    with open(SOURCE, encoding="utf-8") as f:
        source = json.load(f)

    missing = [w["number"] for w in source if w["number"] not in translations]
    if missing:
        raise SystemExit(f"Missing {len(missing)} translations: {missing[:10]}...{missing[-3:]}")

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
