#!/usr/bin/env python3
"""Import manually edited Japanese translations from TSV into vocabulary.json."""

from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CATALOG_PATH = ROOT / "DistinctionVocab" / "DistinctionVocab" / "Resources" / "vocabulary.json"

JP_RE = re.compile(r"[\u3040-\u30ff\u4e00-\u9fff]")


def has_japanese(text: str | None) -> bool:
    return bool(text and JP_RE.search(text))


def normalize(value: str | None) -> str:
    return (value or "").strip()


def word_key(book_id: str, number: int) -> str:
    return f"{book_id}:{number:04d}"


def build_word_index(catalog: dict) -> dict[str, tuple[dict, dict]]:
    index: dict[str, tuple[dict, dict]] = {}
    for book in catalog["books"]:
        for word in book["words"]:
            index[word_key(book["id"], word["number"])] = (book, word)
    return index


def apply_example_translation(word: dict, label: str, japanese: str) -> bool:
    if not has_japanese(japanese):
        return False

    for example in word.get("examples", []):
        if example.get("label") == label:
            example["japaneseTranslation"] = japanese
            return True
    return False


def apply_row(word: dict, row: dict[str, str], overwrite: bool) -> list[str]:
    updated_fields: list[str] = []

    meaning = normalize(row.get("japanese_meaning"))
    if has_japanese(meaning) and (overwrite or not has_japanese(word.get("japaneseMeaning"))):
        word["japaneseMeaning"] = meaning
        updated_fields.append("japanese_meaning")

    etymology = normalize(row.get("etymology"))
    if has_japanese(etymology) and (overwrite or not has_japanese(word.get("etymology"))):
        word["etymology"] = etymology
        updated_fields.append("etymology")

    native_definition = normalize(row.get("native_definition_en"))
    if native_definition and (overwrite or not word.get("nativeDefinition")):
        word["nativeDefinition"] = native_definition
        updated_fields.append("native_definition_en")

    for label, column in (("B", "example_B_ja"), ("C", "example_C_ja"), ("D", "example_D_ja")):
        translation = normalize(row.get(column))
        if not has_japanese(translation):
            continue
        if apply_example_translation(word, label, translation):
            updated_fields.append(column)

    return updated_fields


def write_catalog(catalog: dict) -> None:
    temp_path = CATALOG_PATH.with_suffix(".json.tmp")
    with open(temp_path, "w", encoding="utf-8") as catalog_file:
        json.dump(catalog, catalog_file, ensure_ascii=False, indent=2)
    temp_path.replace(CATALOG_PATH)


def import_tsv(path: Path, overwrite: bool) -> tuple[int, int, int]:
    with open(CATALOG_PATH, encoding="utf-8") as catalog_file:
        catalog = json.load(catalog_file)

    index = build_word_index(catalog)
    matched = 0
    updated = 0
    skipped = 0

    with open(path, encoding="utf-8", newline="") as tsv_file:
        reader = csv.DictReader(tsv_file, delimiter="\t")
        for row in reader:
            book_id = normalize(row.get("book_id"))
            number_text = normalize(row.get("number"))
            if not book_id or not number_text.isdigit():
                skipped += 1
                continue

            key = word_key(book_id, int(number_text))
            if key not in index:
                skipped += 1
                continue

            _, word = index[key]
            matched += 1
            if apply_row(word, row, overwrite):
                updated += 1

    write_catalog(catalog)
    return matched, updated, skipped


def main() -> None:
    parser = argparse.ArgumentParser(description="Import manual Japanese translations from TSV")
    parser.add_argument("tsv_path", type=Path, help="Path to edited TSV file")
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite existing Japanese fields (default: only fill empty fields)",
    )
    args = parser.parse_args()

    if not args.tsv_path.exists():
        raise SystemExit(f"File not found: {args.tsv_path}")

    matched, updated, skipped = import_tsv(args.tsv_path, args.overwrite)
    print(f"Matched rows: {matched}")
    print(f"Updated words: {updated}")
    print(f"Skipped rows: {skipped}")
    print(f"Saved to {CATALOG_PATH}")


if __name__ == "__main__":
    main()
