#!/usr/bin/env python3
"""Translate headwords and example sentences to Japanese and update vocabulary.json."""

import argparse
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CATALOG_PATH = ROOT / "DistinctionVocab" / "DistinctionVocab" / "Resources" / "vocabulary.json"
HEADWORD_CACHE_PATH = ROOT / "scripts" / ".translation_headword_cache.json"
EXAMPLE_CACHE_PATH = ROOT / "scripts" / ".translation_example_cache.json"


def load_cache(path: Path) -> dict[str, str]:
    if path.exists():
        with open(path, encoding="utf-8") as cache_file:
            return json.load(cache_file)
    return {}


def save_cache(path: Path, cache: dict[str, str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as cache_file:
        json.dump(cache, cache_file, ensure_ascii=False, indent=2)


def write_catalog(catalog: dict) -> None:
    temp_path = CATALOG_PATH.with_suffix(".json.tmp")
    with open(temp_path, "w", encoding="utf-8") as catalog_file:
        json.dump(catalog, catalog_file, ensure_ascii=False, indent=2)
    temp_path.replace(CATALOG_PATH)


def translate_text(translator, text: str) -> str:
    normalized = text.strip()
    if not normalized:
        return ""
    return translator.translate(normalized)


def attach_translations(
    catalog: dict,
    headword_cache: dict[str, str],
    example_cache: dict[str, str],
) -> None:
    for book in catalog["books"]:
        for word in book["words"]:
            if not word.get("japaneseMeaning"):
                word["japaneseMeaning"] = headword_cache.get(word["headword"])

            for example in word["examples"]:
                english_text = example.get("text")
                if not example.get("japaneseTranslation") and english_text:
                    example["japaneseTranslation"] = example_cache.get(english_text)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--book-id", help="Translate only the specified book (e.g. dist1)")
    args = parser.parse_args()

    try:
        from deep_translator import GoogleTranslator
    except ImportError:
        print("Run: .venv/bin/pip install deep-translator", file=sys.stderr)
        sys.exit(1)

    with open(CATALOG_PATH, encoding="utf-8") as catalog_file:
        catalog = json.load(catalog_file)

    target_books = catalog["books"]
    if args.book_id:
        target_books = [book for book in catalog["books"] if book["id"] == args.book_id]
        if not target_books:
            print(f"Book not found: {args.book_id}", file=sys.stderr)
            sys.exit(1)

    headword_cache = load_cache(HEADWORD_CACHE_PATH)
    example_cache = load_cache(EXAMPLE_CACHE_PATH)
    translator = GoogleTranslator(source="en", target="ja")

    pending_headwords: list[tuple[str, str]] = []
    pending_examples: list[tuple[str, str]] = []

    for book in target_books:
        for word in book["words"]:
            headword = word["headword"]
            if not word.get("japaneseMeaning") and headword not in headword_cache:
                pending_headwords.append((headword, headword))

            for example in word["examples"]:
                english_text = example.get("text")
                if not english_text:
                    continue
                if example.get("japaneseTranslation") or english_text in example_cache:
                    continue
                pending_examples.append((english_text, english_text))

    print(f"Pending headword translations: {len(pending_headwords)}")
    print(f"Pending example translations: {len(pending_examples)}")

    total_headwords = len(pending_headwords)
    for index, (cache_key, headword) in enumerate(pending_headwords, start=1):
        try:
            headword_cache[cache_key] = translate_text(translator, headword)
        except Exception as error:
            print(f"  headword failed ({headword}): {error}", file=sys.stderr)
            time.sleep(1)
            continue

        if index % 100 == 0 or index == total_headwords:
            save_cache(HEADWORD_CACHE_PATH, headword_cache)
            print(f"  headwords {index}/{total_headwords}")
        time.sleep(0.1)

    total_examples = len(pending_examples)
    for index, (cache_key, english_text) in enumerate(pending_examples, start=1):
        try:
            example_cache[cache_key] = translate_text(translator, english_text)
        except Exception as error:
            print(f"  example failed ({english_text[:40]}...): {error}", file=sys.stderr)
            time.sleep(1)
            continue

        if index % 100 == 0 or index == total_examples:
            save_cache(EXAMPLE_CACHE_PATH, example_cache)
            print(f"  examples {index}/{total_examples}")
        time.sleep(0.1)

    save_cache(HEADWORD_CACHE_PATH, headword_cache)
    save_cache(EXAMPLE_CACHE_PATH, example_cache)
    attach_translations(catalog, headword_cache, example_cache)
    write_catalog(catalog)
    print("Done.")


if __name__ == "__main__":
    main()
