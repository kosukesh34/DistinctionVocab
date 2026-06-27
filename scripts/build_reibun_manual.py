#!/usr/bin/env python3
"""Build reibun manual JSON from TSV meanings and hand-crafted example translations."""

from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CATALOG_PATH = ROOT / "DistinctionVocab" / "DistinctionVocab" / "Resources" / "vocabulary.json"
MANUAL_DIR = ROOT / "data" / "distinction_manual"
TSV_PATH = Path.home() / "Library/Mobile Documents/com~apple~Numbers/Documents/例文付き　2 2.tsv"
EXAMPLE_TRANSLATIONS_PATH = MANUAL_DIR / "reibun_example_translations.json"

MEANING_FIXES: dict[int, str] = {
    28: "お世辞を言う",
    675: "批判する",
}


def load_tsv_meanings() -> dict[int, str]:
    meanings: dict[int, str] = {}
    with open(TSV_PATH, encoding="utf-8") as file:
        reader = csv.reader(file, delimiter="\t")
        next(reader, None)
        for row in reader:
            if not row or not row[0].strip().isdigit():
                continue
            number = int(row[0].strip())
            meaning = row[2].strip() if len(row) > 2 else ""
            if meaning:
                meanings[number] = meaning
    return meanings


def load_example_translations() -> dict[str, dict[str, str]]:
    if not EXAMPLE_TRANSLATIONS_PATH.exists():
        return {}
    with open(EXAMPLE_TRANSLATIONS_PATH, encoding="utf-8") as file:
        return json.load(file)


def main() -> None:
    with open(CATALOG_PATH, encoding="utf-8") as catalog_file:
        catalog = json.load(catalog_file)

    reibun = next(book for book in catalog["books"] if book["id"] == "reibun")
    tsv_meanings = load_tsv_meanings()
    example_translations = load_example_translations()

    entries = []
    missing_examples = []
    for word in reibun["words"]:
        number = word["number"]
        key = str(number)
        examples: dict[str, str] = {}

        if key in example_translations:
            examples = dict(example_translations[key])
        else:
            for example in word.get("examples", []):
                label = example.get("label", "")
                if example.get("text"):
                    missing_examples.append((number, word["headword"], label, example["text"]))

        entry = {
            "number": number,
            "headword": word["headword"],
            "japaneseMeaning": MEANING_FIXES.get(number) or tsv_meanings.get(number) or word.get("japaneseMeaning"),
        }
        if examples:
            entry["examples"] = examples
        entries.append(entry)

    out_path = MANUAL_DIR / "reibun.json"
    with open(out_path, "w", encoding="utf-8") as out_file:
        json.dump(entries, out_file, ensure_ascii=False, indent=2)
        out_file.write("\n")

    print(f"Wrote {len(entries)} entries to {out_path}")
    print(f"Missing hand translations for {len(missing_examples)} examples")
    if missing_examples[:10]:
        for item in missing_examples[:10]:
            print(f"  #{item[0]} {item[1]} [{item[2]}] {item[3][:60]}")


if __name__ == "__main__":
    main()
