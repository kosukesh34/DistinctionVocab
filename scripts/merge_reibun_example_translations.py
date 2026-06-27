#!/usr/bin/env python3
"""Merge reibun example translation parts into a single file."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MANUAL_DIR = ROOT / "data" / "distinction_manual"
PARTS = (
    MANUAL_DIR / "reibun_example_translations_part1.json",
    MANUAL_DIR / "reibun_example_translations_part2.json",
    MANUAL_DIR / "reibun_example_translations_part3.json",
)
OUT = MANUAL_DIR / "reibun_example_translations.json"


def main() -> None:
    merged: dict[str, dict[str, str]] = {}
    for path in PARTS:
        if not path.exists():
            raise FileNotFoundError(path)
        with open(path, encoding="utf-8") as part_file:
            merged.update(json.load(part_file))

    manual_overrides = {
        "435": {
            "B": "彼はこの支店のトップ（リーダー）になろうとしてるんだ。",
            "C": "もちろん",
        },
        "507": {
            "B": "でもよく考えたら、行かないことにした。",
        },
        "546": {
            "B": "ついにメアリーが秘密をばらしちゃった。",
        },
        "630": {
            "B": "気をつけて。でしゃばりすぎだよ。",
        },
    }
    for key, examples in manual_overrides.items():
        merged.setdefault(key, {}).update(examples)

    with open(OUT, "w", encoding="utf-8") as out_file:
        json.dump(merged, out_file, ensure_ascii=False, indent=2)
        out_file.write("\n")

    print(f"Merged {len(merged)} entries to {OUT}")


if __name__ == "__main__":
    main()
