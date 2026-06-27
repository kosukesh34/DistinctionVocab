#!/usr/bin/env python3
"""Build complete earlybird.json from source + all translation batches."""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "data" / "distinction_manual" / "earlybird_source.json"
OUT = ROOT / "data" / "distinction_manual" / "earlybird.json"
SCRIPTS = Path(__file__).resolve().parent


def load_module(name: str):
    path = SCRIPTS / f"{name}.py"
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main() -> None:
    with open(SOURCE, encoding="utf-8") as f:
        source = json.load(f)

    merged: dict[int, dict] = {}

    for mod_name in (
        "_gen_earlybird_translations",
        "earlybird_translations_26_100",
        "earlybird_translations_101_200",
        "earlybird_translations_201_300",
        "earlybird_translations_301_400",
    ):
        mod = load_module(mod_name)
        merged.update(mod.TRANSLATIONS)

    result = []
    missing = []
    for word in source:
        n = word["number"]
        t = merged.get(n)
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
