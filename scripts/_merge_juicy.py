#!/usr/bin/env python3
"""Merge all juicy translation parts and write juicy.json."""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "data" / "distinction_manual" / "juicy_source.json"
OUT = ROOT / "data" / "distinction_manual" / "juicy.json"
SCRIPTS = Path(__file__).resolve().parent


def load_module(name: str):
    path = SCRIPTS / f"{name}.py"
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main() -> None:
    translations: dict[int, dict] = {}

    for mod_name, attr in [
        ("_gen_juicy_part1", "PART1"),
        ("_juicy_trans_21_200", "PART"),
        ("_juicy_trans_201_400", "PART"),
    ]:
        mod = load_module(mod_name)
        part = getattr(mod, attr)
        translations.update(part)
        print(f"Loaded {mod_name}: {len(part)} entries")

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
