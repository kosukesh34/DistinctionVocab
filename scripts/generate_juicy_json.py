#!/usr/bin/env python3
"""Generate juicy.json from source + hand-crafted translations."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "data" / "distinction_manual" / "juicy_source.json"
OUTPUT = ROOT / "data" / "distinction_manual" / "juicy.json"

sys.path.insert(0, str(ROOT))

from scripts.juicy_t_batch1 import B1
from scripts.juicy_t_batch2 import B2
from scripts.juicy_t_batch3 import B3
from scripts.juicy_t_batch4 import B4
from scripts.juicy_t_batch5 import B5
from scripts.juicy_t_batch6 import B6
from scripts.juicy_t_batch7 import B7

TRANSLATIONS: dict[int, dict] = {}
for batch in (B1, B2, B3, B4, B5, B6, B7):
    TRANSLATIONS.update(batch)


def main() -> None:
    with open(SOURCE, encoding="utf-8") as f:
        source = json.load(f)

    result = []
    missing = []
    for word in source:
        n = word["number"]
        if n not in TRANSLATIONS:
            missing.append(n)
            continue
        t = TRANSLATIONS[n]
        result.append({
            "number": n,
            "headword": word["headword"],
            "nativeDefinition": t["nativeDefinition"],
            "japaneseMeaning": t["japaneseMeaning"],
            "etymology": t["etymology"],
            "examples": t["examples"],
        })

    if missing:
        print(f"Missing {len(missing)}: {missing[:30]}{'...' if len(missing) > 30 else ''}", file=sys.stderr)
        raise SystemExit(1)

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(f"Wrote {len(result)} words to {OUTPUT}")


if __name__ == "__main__":
    main()
