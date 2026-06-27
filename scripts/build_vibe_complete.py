#!/usr/bin/env python3
"""Build complete vibe.json from all translation modules."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "data" / "distinction_manual" / "vibe_source.json"
OUT = ROOT / "data" / "distinction_manual" / "vibe.json"

sys.path.insert(0, str(Path(__file__).resolve().parent))
from vibe_translations_data import TRANSLATIONS  # noqa: E402
from vibe_translations_251_400 import TRANSLATIONS_251_400  # noqa: E402


def main() -> None:
    with open(SOURCE, encoding="utf-8") as f:
        source = json.load(f)

    all_translations = {**TRANSLATIONS, **TRANSLATIONS_251_400}

    result = []
    missing = []
    for word in source:
        n = word["number"]
        if n not in all_translations:
            missing.append(n)
            continue
        t = all_translations[n]
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

    # Also write merged data file for build_vibe_manual.py compatibility
    data_out = ROOT / "scripts" / ".vibe_translations_data.json"
    with open(data_out, "w", encoding="utf-8") as f:
        json.dump({str(k): v for k, v in sorted(all_translations.items())}, f, ensure_ascii=False, indent=2)
        f.write("\n")

    print(f"Wrote {len(result)} words to {OUT}")
    print(f"Numbers: {result[0]['number']}-{result[-1]['number']} (missing 78 in source)")


if __name__ == "__main__":
    main()
