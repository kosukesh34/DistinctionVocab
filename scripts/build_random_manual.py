#!/usr/bin/env python3
"""Build random.json manual Japanese translations for Distinction IV."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "data" / "distinction_manual" / "random_source.json"
OUT = ROOT / "data" / "distinction_manual" / "random.json"
DATA = Path(__file__).with_name("random_manual_translations.py")


def main() -> None:
    with open(SOURCE, encoding="utf-8") as f:
        source = json.load(f)
    import importlib.util
    spec = importlib.util.spec_from_file_location("random_manual_translations", DATA)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    translations = mod.TRANSLATIONS

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
