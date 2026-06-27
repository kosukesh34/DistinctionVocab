#!/usr/bin/env python3
"""Apply hand-crafted Distinction manual translations to vocabulary.json."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CATALOG_PATH = ROOT / "DistinctionVocab" / "DistinctionVocab" / "Resources" / "vocabulary.json"
MANUAL_DIR = ROOT / "data" / "distinction_manual"

DISTINCTION_BOOK_IDS = ("dist1", "earlybird", "juicy", "random", "sbslike", "vibe", "reibun")


def load_manual_translations(book_id: str) -> dict[int, dict]:
    path = MANUAL_DIR / f"{book_id}.json"
    if not path.exists():
        raise FileNotFoundError(f"Manual translation file not found: {path}")

    with open(path, encoding="utf-8") as manual_file:
        entries = json.load(manual_file)

    return {entry["number"]: entry for entry in entries}


def apply_entry(word: dict, entry: dict, source_entry: dict | None = None, book_id: str = "") -> None:
    if entry.get("nativeDefinition"):
        word["nativeDefinition"] = entry["nativeDefinition"]
    if entry.get("japaneseMeaning"):
        word["japaneseMeaning"] = entry["japaneseMeaning"]
    if entry.get("etymology"):
        word["etymology"] = entry["etymology"]

    example_translations = entry.get("examples", {})
    for example in word.get("examples", []):
        label = example.get("label", "")
        if label in example_translations and example_translations[label]:
            example["japaneseTranslation"] = example_translations[label]

    if source_entry:
        source_examples = source_entry.get("examples", {})
        for example in word.get("examples", []):
            label = example.get("label", "")
            if label in source_examples and source_examples[label]:
                text = source_examples[label]
            elif label == "D" and source_examples.get("F") and book_id == "sbslike":
                text = source_examples["F"]
            else:
                continue
            if label == "D":
                text = normalize_d_english_text(text)
            example["text"] = text


def normalize_d_english_text(text: str) -> str:
    text = text.strip()
    fixes = {
        "An ambiguous.": "Unambiguous.",
        "an ambiguous.": "Unambiguous.",
    }
    return fixes.get(text, text)


def load_source_entries(book_id: str) -> dict[int, dict]:
    path = MANUAL_DIR / f"{book_id}_source.json"
    if not path.exists():
        return {}
    with open(path, encoding="utf-8") as source_file:
        entries = json.load(source_file)
    return {entry["number"]: entry for entry in entries}


def write_catalog(catalog: dict) -> None:
    temp_path = CATALOG_PATH.with_suffix(".json.tmp")
    with open(temp_path, "w", encoding="utf-8") as catalog_file:
        json.dump(catalog, catalog_file, ensure_ascii=False, indent=2)
    temp_path.replace(CATALOG_PATH)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--book-id", choices=DISTINCTION_BOOK_IDS, help="Apply one book only")
    args = parser.parse_args()

    with open(CATALOG_PATH, encoding="utf-8") as catalog_file:
        catalog = json.load(catalog_file)

    book_ids = [args.book_id] if args.book_id else list(DISTINCTION_BOOK_IDS)
    total_applied = 0

    for book in catalog["books"]:
        if book["id"] not in book_ids:
            continue

        manual = load_manual_translations(book["id"])
        source = load_source_entries(book["id"])
        applied = 0
        for word in book["words"]:
            entry = manual.get(word["number"])
            if not entry:
                print(f"  missing: {book['id']} #{word['number']} {word['headword']}")
                continue
            apply_entry(word, entry, source.get(word["number"]), book["id"])
            applied += 1

        total_applied += applied
        print(f"{book['title']} ({book['id']}): {applied}/{len(book['words'])} words applied")

    write_catalog(catalog)
    print(f"Done. Applied {total_applied} words to {CATALOG_PATH}")


if __name__ == "__main__":
    main()
