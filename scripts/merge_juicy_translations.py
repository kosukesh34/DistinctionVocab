#!/usr/bin/env python3
"""Merge batch translation files into juicy_manual_translations.py and build juicy.json."""

from __future__ import annotations

import importlib.util
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TRANS_PATH = Path(__file__).resolve().parent / "juicy_manual_translations.py"
SOURCE = ROOT / "data" / "distinction_manual" / "juicy_source.json"
OUTPUT = ROOT / "data" / "distinction_manual" / "juicy.json"


def load_translations() -> dict[int, dict]:
    spec = importlib.util.spec_from_file_location("juicy_manual_translations", TRANS_PATH)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return dict(mod.TRANSLATIONS)


def load_batch(path: Path) -> dict[int, dict]:
    spec = importlib.util.spec_from_file_location(path.stem, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return dict(mod.BATCH)


def format_entry(n: int, t: dict) -> str:
    ex = t["examples"]
    return (
        f'{n}: {{"nativeDefinition": {json.dumps(t["nativeDefinition"], ensure_ascii=False)}, '
        f'"japaneseMeaning": {json.dumps(t["japaneseMeaning"], ensure_ascii=False)}, '
        f'"etymology": {json.dumps(t["etymology"], ensure_ascii=False)}, '
        f'"examples": {{"B": {json.dumps(ex["B"], ensure_ascii=False)}, '
        f'"C": {json.dumps(ex["C"], ensure_ascii=False)}, '
        f'"D": {json.dumps(ex["D"], ensure_ascii=False)}}}}},'
    )


def rewrite_translations_file(all_trans: dict[int, dict]) -> None:
    lines = ['# fmt: off', '"""Hand-crafted Japanese translations for Distinction III (juicy)."""', '', 'TRANSLATIONS: dict[int, dict] = {']
    for n in sorted(all_trans):
        lines.append(format_entry(n, all_trans[n]))
    lines.append("}")
    lines.append("")
    TRANS_PATH.write_text("\n".join(lines), encoding="utf-8")


def build_json(all_trans: dict[int, dict]) -> None:
    with open(SOURCE, encoding="utf-8") as f:
        source = json.load(f)
    result = []
    for word in source:
        n = word["number"]
        t = all_trans[n]
        result.append({
            "number": n,
            "headword": word["headword"],
            "nativeDefinition": t["nativeDefinition"],
            "japaneseMeaning": t["japaneseMeaning"],
            "etymology": t["etymology"],
            "examples": t["examples"],
        })
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(f"Wrote {len(result)} words to {OUTPUT}")


def main() -> None:
    all_trans = load_translations()
    for batch_file in sys.argv[1:]:
        batch = load_batch(Path(batch_file))
        all_trans.update(batch)
        print(f"Merged {len(batch)} entries from {batch_file}")

    expected = {n for n in range(1, 401) if n != 79}
    missing = sorted(expected - set(all_trans))
    if missing:
        print(f"Still missing {len(missing)}: {missing[:20]}{'...' if len(missing) > 20 else ''}")
        sys.exit(1)

    rewrite_translations_file(all_trans)
    build_json(all_trans)


if __name__ == "__main__":
    main()
