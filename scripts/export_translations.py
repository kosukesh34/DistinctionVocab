#!/usr/bin/env python3
"""Export vocabulary to TSV for manual Japanese translation."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CATALOG_PATH = ROOT / "DistinctionVocab" / "DistinctionVocab" / "Resources" / "vocabulary.json"
DEFAULT_OUTPUT = ROOT / "translations" / "manual_translations.tsv"

COLUMNS = [
    "book_id",
    "book_title",
    "number",
    "headword",
    "native_definition_en",
    "japanese_meaning",
    "etymology",
    "example_B_en",
    "example_B_ja",
    "example_C_en",
    "example_C_ja",
    "example_D_en",
    "example_D_ja",
]


def example_text(examples: list[dict], label: str) -> str:
    for example in examples:
        if example.get("label") == label:
            return (example.get("text") or "").strip()
    return ""


def example_translation(examples: list[dict], label: str) -> str:
    for example in examples:
        if example.get("label") == label:
            return (example.get("japaneseTranslation") or "").strip()
    return ""


def export_catalog(catalog: dict, output_path: Path, book_id: str | None, untranslated_only: bool) -> int:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    rows_written = 0

    with open(output_path, "w", encoding="utf-8", newline="") as output_file:
        writer = csv.DictWriter(output_file, fieldnames=COLUMNS, delimiter="\t")
        writer.writeheader()

        for book in catalog["books"]:
            if book_id and book["id"] != book_id:
                continue

            for word in book["words"]:
                examples = word.get("examples", [])
                japanese_meaning = (word.get("japaneseMeaning") or "").strip()

                if untranslated_only and japanese_meaning:
                    continue

                writer.writerow(
                    {
                        "book_id": book["id"],
                        "book_title": book["title"],
                        "number": word["number"],
                        "headword": word["headword"],
                        "native_definition_en": (word.get("nativeDefinition") or "").strip(),
                        "japanese_meaning": japanese_meaning,
                        "etymology": (word.get("etymology") or "").strip(),
                        "example_B_en": example_text(examples, "B"),
                        "example_B_ja": example_translation(examples, "B"),
                        "example_C_en": example_text(examples, "C"),
                        "example_C_ja": example_translation(examples, "C"),
                        "example_D_en": example_text(examples, "D"),
                        "example_D_ja": example_translation(examples, "D"),
                    }
                )
                rows_written += 1

    return rows_written


def main() -> None:
    parser = argparse.ArgumentParser(description="Export vocabulary for manual translation")
    parser.add_argument("--book-id", help="Export only one book (e.g. dist1)")
    parser.add_argument(
        "--untranslated-only",
        action="store_true",
        help="Export only entries without japanese_meaning",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help=f"Output TSV path (default: {DEFAULT_OUTPUT})",
    )
    args = parser.parse_args()

    with open(CATALOG_PATH, encoding="utf-8") as catalog_file:
        catalog = json.load(catalog_file)

    count = export_catalog(catalog, args.output, args.book_id, args.untranslated_only)
    print(f"Exported {count} rows to {args.output}")
    print("Edit japanese_meaning, etymology, and example_*_ja columns, then run:")
    print("  python3 scripts/import_manual_translations.py <path-to-tsv>")


if __name__ == "__main__":
    main()
