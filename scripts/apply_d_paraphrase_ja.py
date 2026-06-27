#!/usr/bin/env python3
"""Apply hand-crafted D (言い換え) Japanese paraphrases to manual JSON and vocabulary.json."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CATALOG_PATH = ROOT / "DistinctionVocab" / "DistinctionVocab" / "Resources" / "vocabulary.json"
MANUAL_DIR = ROOT / "data" / "distinction_manual"
PARAPHRASE_DIR = MANUAL_DIR / "d_paraphrase_ja"

BOOK_IDS = ("dist1", "earlybird", "juicy", "random", "sbslike", "vibe")


def load_paraphrases(book_id: str) -> dict[str, str]:
    path = PARAPHRASE_DIR / f"{book_id}.json"
    if not path.exists():
        raise FileNotFoundError(f"Paraphrase file not found: {path}")
    with open(path, encoding="utf-8") as paraphrase_file:
        return json.load(paraphrase_file)


def apply_to_manual(book_id: str, paraphrases: dict[str, str]) -> int:
    manual_path = MANUAL_DIR / f"{book_id}.json"
    with open(manual_path, encoding="utf-8") as manual_file:
        entries = json.load(manual_file)

    applied = 0
    for entry in entries:
        key = str(entry["number"])
        if key not in paraphrases:
            print(f"  missing paraphrase: {book_id} #{entry['number']} {entry['headword']}")
            continue
        entry.setdefault("examples", {})["D"] = paraphrases[key]
        applied += 1

    with open(manual_path, "w", encoding="utf-8") as manual_file:
        json.dump(entries, manual_file, ensure_ascii=False, indent=2)
        manual_file.write("\n")

    return applied


def apply_to_catalog(book_ids: list[str], paraphrases_by_book: dict[str, dict[str, str]]) -> int:
    with open(CATALOG_PATH, encoding="utf-8") as catalog_file:
        catalog = json.load(catalog_file)

    applied = 0
    for book in catalog["books"]:
        if book["id"] not in book_ids:
            continue

        paraphrases = paraphrases_by_book[book["id"]]
        for word in book["words"]:
            key = str(word["number"])
            if key not in paraphrases:
                continue
            for example in word.get("examples", []):
                if example.get("label") == "D":
                    example["japaneseTranslation"] = paraphrases[key]
                    applied += 1
                    break

    temp_path = CATALOG_PATH.with_suffix(".json.tmp")
    with open(temp_path, "w", encoding="utf-8") as catalog_file:
        json.dump(catalog, catalog_file, ensure_ascii=False, indent=2)
    temp_path.replace(CATALOG_PATH)
    return applied


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--book-id", choices=BOOK_IDS, help="Apply one book only")
    args = parser.parse_args()

    book_ids = [args.book_id] if args.book_id else list(BOOK_IDS)
    paraphrases_by_book: dict[str, dict[str, str]] = {}

    for book_id in book_ids:
        paraphrases = load_paraphrases(book_id)
        manual_applied = apply_to_manual(book_id, paraphrases)
        paraphrases_by_book[book_id] = paraphrases
        print(f"{book_id}: updated {manual_applied} manual entries")

    catalog_applied = apply_to_catalog(book_ids, paraphrases_by_book)
    print(f"Updated {catalog_applied} D translations in {CATALOG_PATH}")


if __name__ == "__main__":
    main()
