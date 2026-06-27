#!/usr/bin/env python3
"""Export English source texts from vocabulary.json for manual translation work."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CATALOG_PATH = ROOT / "DistinctionVocab" / "DistinctionVocab" / "Resources" / "vocabulary.json"
MANUAL_DIR = ROOT / "data" / "distinction_manual"

BOOK_IDS = ("dist1", "earlybird", "juicy", "random", "sbslike", "vibe", "reibun")


def export_book(book: dict) -> list[dict]:
    entries: list[dict] = []
    for word in book["words"]:
        examples: dict[str, str] = {}
        for example in word.get("examples", []):
            label = example.get("label", "")
            text = example.get("text")
            if label and text:
                examples[label] = text

        entry = {
            "number": word["number"],
            "headword": word["headword"],
        }
        if examples:
            entry["examples"] = examples
        entries.append(entry)
    return entries


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--book-id", choices=BOOK_IDS, required=True)
    args = parser.parse_args()

    with open(CATALOG_PATH, encoding="utf-8") as catalog_file:
        catalog = json.load(catalog_file)

    book = next(book for book in catalog["books"] if book["id"] == args.book_id)
    entries = export_book(book)

    out_path = MANUAL_DIR / f"{args.book_id}_source.json"
    MANUAL_DIR.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as out_file:
        json.dump(entries, out_file, ensure_ascii=False, indent=2)
        out_file.write("\n")

    print(f"Exported {len(entries)} entries to {out_path}")


if __name__ == "__main__":
    main()
