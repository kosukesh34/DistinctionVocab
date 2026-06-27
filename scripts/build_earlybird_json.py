#!/usr/bin/env python3
"""Build complete earlybird.json from source + all translation batches."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "data" / "distinction_manual" / "earlybird_source.json"
OUT = ROOT / "data" / "distinction_manual" / "earlybird.json"

sys.path.insert(0, str(Path(__file__).resolve().parent))
from earlybird_manual_translations import TRANSLATIONS as T1  # noqa: E402
from earlybird_translations_41_100 import TRANSLATIONS as T2  # noqa: E402
from earlybird_translations_101_200 import TRANSLATIONS as T3  # noqa: E402
from earlybird_translations_201_300 import TRANSLATIONS as T4  # noqa: E402
from earlybird_translations_301_400 import TRANSLATIONS as T5  # noqa: E402


def main() -> None:
    translations: dict[int, dict] = {}
    for batch in (T1, T2, T3, T4, T5):
        translations.update(batch)

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
