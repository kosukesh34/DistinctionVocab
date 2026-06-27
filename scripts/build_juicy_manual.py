#!/usr/bin/env python3
"""Generate juicy.json manual translations for Distinction III."""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "data" / "distinction_manual" / "juicy_source.json"
OUTPUT = ROOT / "data" / "distinction_manual" / "juicy.json"
MANUAL_DIR = ROOT / "data" / "distinction_manual"

PART_MODULES = [
    MANUAL_DIR / "juicy_trans_part2.py",
    MANUAL_DIR / "juicy_trans_part3.py",
    MANUAL_DIR / "juicy_trans_part4.py",
    MANUAL_DIR / "juicy_trans_part5.py",
    MANUAL_DIR / "juicy_trans_part6.py",
    MANUAL_DIR / "juicy_trans_part7.py",
    MANUAL_DIR / "juicy_trans_part8.py",
]


def load_translations() -> dict[int, dict]:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from juicy_manual_translations import TRANSLATIONS as part1  # noqa: E402

    merged = dict(part1)
    for path in PART_MODULES:
        spec = importlib.util.spec_from_file_location(path.stem, path)
        if spec is None or spec.loader is None:
            raise ImportError(f"Cannot load {path}")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        merged.update(module.TRANSLATIONS)
    return merged


def main() -> None:
    with open(SOURCE, encoding="utf-8") as f:
        source = json.load(f)

    translations = load_translations()
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

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
        f.write("\n")

    print(f"Wrote {len(result)} words to {OUTPUT}")


if __name__ == "__main__":
    main()
