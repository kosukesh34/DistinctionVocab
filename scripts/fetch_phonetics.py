#!/usr/bin/env python3
"""Generate IPA phonetic transcriptions for vocabulary headwords."""

import json
import re
from pathlib import Path

import eng_to_ipa as ipa

ROOT = Path(__file__).resolve().parent.parent
CATALOG_PATH = ROOT / "DistinctionVocab" / "DistinctionVocab" / "Resources" / "vocabulary.json"
CACHE_PATH = ROOT / "scripts" / ".phonetic_cache.json"

PLACEHOLDER_RE = re.compile(r"\b(sb|sth|sb's|sth's)\b", re.IGNORECASE)


def normalize_headword_for_ipa(headword: str) -> str:
    return PLACEHOLDER_RE.sub(
        lambda match: {"sb": "somebody", "sth": "something"}.get(match.group(1).lower(), match.group(1)),
        headword,
    )


def convert_to_ipa(headword: str) -> str:
    normalized = normalize_headword_for_ipa(headword)
    converted = ipa.convert(normalized)
    converted = converted.replace("*", "")
    converted = re.sub(r"\s+", " ", converted).strip()
    return converted


def main() -> None:
    cache: dict[str, str] = {}
    if CACHE_PATH.exists():
        with open(CACHE_PATH, encoding="utf-8") as cache_file:
            cache = json.load(cache_file)

    if not CATALOG_PATH.exists():
        raise SystemExit(f"Catalog not found: {CATALOG_PATH}")

    with open(CATALOG_PATH, encoding="utf-8") as catalog_file:
        catalog = json.load(catalog_file)

    pending = []
    for book in catalog["books"]:
        for word in book["words"]:
            headword = word["headword"]
            if headword not in cache:
                pending.append(headword)

    print(f"Pending phonetics: {len(pending)}")
    for index, headword in enumerate(pending, start=1):
        cache[headword] = convert_to_ipa(headword)
        if index % 100 == 0 or index == len(pending):
            print(f"  {index}/{len(pending)} converted")
            with open(CACHE_PATH, "w", encoding="utf-8") as cache_file:
                json.dump(cache, cache_file, ensure_ascii=False, indent=2)

    if pending:
        with open(CACHE_PATH, "w", encoding="utf-8") as cache_file:
            json.dump(cache, cache_file, ensure_ascii=False, indent=2)

    print(f"Cached phonetics: {len(cache)}")
    print("Run generate_catalog.py to attach phonetics to vocabulary.json")


if __name__ == "__main__":
    main()
