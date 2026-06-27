#!/usr/bin/env python3
"""Research translations from internet sources and update manual JSON (safe mode).

Uses:
- Free Dictionary API + Wiktionary for English definitions / etymology
- Jisho.org for single-word Japanese glosses (not idioms)
- Sentence-level translation for example B/C only

Does NOT overwrite:
- D paraphrases (use apply_d_paraphrase_ja.py)
- reibun japaneseMeaning (TSV source)
- existing manual fields unless --overwrite

Run:
  .venv/bin/python scripts/research_translations.py --book-id dist1
  .venv/bin/python scripts/apply_distinction_manual.py
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parent.parent
CATALOG_PATH = ROOT / "DistinctionVocab" / "DistinctionVocab" / "Resources" / "vocabulary.json"
MANUAL_DIR = ROOT / "data" / "distinction_manual"
CACHE_DIR = ROOT / "data" / "distinction_manual" / "research_cache"

BOOK_IDS = ("dist1", "earlybird", "juicy", "random", "sbslike", "vibe", "reibun")
JISHO_API = "https://jisho.org/api/v1/search/words"
DICTIONARY_API = "https://api.dictionaryapi.dev/api/v2/entries/en"
REQUEST_HEADERS = {"User-Agent": "DistinctionVocab/1.0 (educational research)"}

sys.path.insert(0, str(ROOT / "scripts"))
from enrich_vocabulary import (  # noqa: E402
    clean_wikitext,
    example_by_label,
    fetch_etymology,
    fetch_wiktionary_definition,
    is_phrase,
    is_valid_etymology,
    lookup_key_word,
    normalize_for_wiktionary,
    refine_definition,
)


def load_json(path: Path, default):
    if path.exists():
        with open(path, encoding="utf-8") as file:
            return json.load(file)
    return default


def save_json(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)
        file.write("\n")


def fetch_dictionary_definition(headword: str) -> str | None:
    candidates = [lookup_key_word(headword), normalize_for_wiktionary(headword).lower(), headword.lower()]
    seen: set[str] = set()
    for candidate in candidates:
        candidate = candidate.strip("- ")
        if not candidate or candidate in seen:
            continue
        seen.add(candidate)
        try:
            response = requests.get(
                f"{DICTIONARY_API}/{requests.utils.quote(candidate)}",
                headers=REQUEST_HEADERS,
                timeout=12,
            )
            if response.status_code != 200:
                continue
            for entry in response.json():
                for meaning in entry.get("meanings", []):
                    for definition in meaning.get("definitions", []):
                        text = (definition.get("definition") or "").strip()
                        if len(text) > 10:
                            return text
        except (requests.RequestException, json.JSONDecodeError):
            continue
    return None


def build_native_definition(headword: str, examples: list[dict]) -> str:
    dictionary_def = fetch_dictionary_definition(headword)
    if dictionary_def:
        return refine_definition(dictionary_def, headword).rstrip(".") + "."

    if not is_phrase(headword):
        wiktionary_def = fetch_wiktionary_definition(headword)
        if wiktionary_def:
            return wiktionary_def if wiktionary_def.endswith(".") else wiktionary_def + "."

    b_text = example_by_label(examples, "B")
    if b_text:
        return f"A native expression used in contexts like: \"{b_text}\""
    return f"A common native English expression: {headword}."


def jisho_search(keyword: str) -> list[dict]:
    try:
        response = requests.get(JISHO_API, params={"keyword": keyword}, headers=REQUEST_HEADERS, timeout=12)
        if response.status_code == 200:
            return response.json().get("data", [])
    except requests.RequestException:
        pass
    return []


def pick_jisho_meaning(headword: str, native_definition: str) -> str | None:
    if is_phrase(headword):
        return None

    query = lookup_key_word(headword)
    items = jisho_search(query)
    if not items:
        return None

    hint_words = set(re.findall(r"[a-z]{4,}", native_definition.lower()))
    scored: list[tuple[float, str]] = []

    for item in items[:6]:
        for japanese in item.get("japanese", []):
            word = japanese.get("word") or japanese.get("reading")
            if not word:
                continue
            score = 0.0
            for sense in item.get("senses", []):
                for gloss in sense.get("english_definitions", []):
                    gloss_lower = gloss.lower()
                    score += sum(2 for token in hint_words if token in gloss_lower)
            if score > 0:
                scored.append((score, word))

    if not scored:
        return None
    scored.sort(reverse=True)
    unique: list[str] = []
    for _, word in scored:
        if word not in unique:
            unique.append(word)
        if len(unique) >= 3:
            break
    return "、".join(unique)


def bad_japanese_for_idiom(headword: str, japanese: str) -> bool:
    if not is_phrase(headword):
        return False
    head_tokens = set(re.findall(r"[a-z]{3,}", headword.lower()))
    ja = japanese.lower()
    false_friends = {
        "drive": ("ドライブ", "運転"),
        "black": ("黒",),
        "white": ("白", "白字"),
    }
    for token in head_tokens:
        if token in false_friends:
            for bad in false_friends[token]:
                if bad in japanese:
                    return True
    return False


def research_entry(
    word: dict,
    book_id: str,
    translator,
    overwrite: bool,
) -> dict:
    headword = word["headword"]
    examples = word.get("examples", [])

    native_definition = build_native_definition(headword, examples)
    time.sleep(0.1)

    raw_etymology = fetch_etymology(normalize_for_wiktionary(headword)) or fetch_etymology(headword)
    time.sleep(0.08)

    japanese_meaning = None
    if book_id == "reibun":
        japanese_meaning = word.get("japaneseMeaning")
    elif is_phrase(headword) and translator:
        try:
            japanese_meaning = translator.translate(refine_definition(native_definition, headword).rstrip("."))
        except Exception:
            japanese_meaning = None
    else:
        japanese_meaning = pick_jisho_meaning(headword, native_definition)
        if not japanese_meaning and translator:
            try:
                japanese_meaning = translator.translate(refine_definition(native_definition, headword).rstrip("."))
            except Exception:
                japanese_meaning = None

    if japanese_meaning and bad_japanese_for_idiom(headword, japanese_meaning):
        japanese_meaning = None

    etymology_ja = None
    if translator and raw_etymology and is_valid_etymology(raw_etymology):
        cleaned = clean_wikitext(raw_etymology)
        if len(cleaned) > 220:
            cleaned = cleaned[:217] + "..."
        try:
            etymology_ja = translator.translate(cleaned)
        except Exception:
            etymology_ja = None

    example_translations: dict[str, str] = {}
    if translator:
        for example in examples:
            label = example.get("label", "")
            english = example.get("text")
            if not english or label in {"D", "F"}:
                continue
            if book_id != "reibun" and label == "D":
                continue
            try:
                example_translations[label] = translator.translate(english)
            except Exception:
                pass
            time.sleep(0.08)

    return {
        "nativeDefinition": native_definition,
        "japaneseMeaning": japanese_meaning,
        "etymology": etymology_ja,
        "examples": example_translations,
    }


def merge_entry(entry: dict, researched: dict, overwrite: bool) -> None:
    if researched.get("nativeDefinition") and (overwrite or not entry.get("nativeDefinition")):
        entry["nativeDefinition"] = researched["nativeDefinition"]

    meaning = researched.get("japaneseMeaning")
    if meaning and (overwrite or not entry.get("japaneseMeaning")):
        if not bad_japanese_for_idiom(entry["headword"], meaning):
            entry["japaneseMeaning"] = meaning

    if researched.get("etymology") and (overwrite or not entry.get("etymology")):
        entry["etymology"] = researched["etymology"]

    entry.setdefault("examples", {})
    for label, translation in researched.get("examples", {}).items():
        if translation and (overwrite or not entry["examples"].get(label)):
            entry["examples"][label] = translation


def process_book(book: dict, translator, overwrite: bool) -> int:
    book_id = book["id"]
    manual_path = MANUAL_DIR / f"{book_id}.json"
    entries = load_json(manual_path, [])
    by_number = {entry["number"]: entry for entry in entries}

    for index, word in enumerate(book["words"], start=1):
        number = word["number"]
        entry = by_number.get(number)
        if not entry:
            entry = {"number": number, "headword": word["headword"]}
            by_number[number] = entry

        researched = research_entry(word, book_id, translator, overwrite)
        merge_entry(entry, researched, overwrite)

        if index % 25 == 0:
            save_json(manual_path, sorted(by_number.values(), key=lambda item: item["number"]))
            print(f"  {book_id}: {index}/{len(book['words'])}")

    save_json(manual_path, sorted(by_number.values(), key=lambda item: item["number"]))
    return len(book["words"])


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--book-id", choices=BOOK_IDS)
    parser.add_argument("--overwrite", action="store_true")
    parser.add_argument("--skip-translate", action="store_true", help="Only refresh English definitions")
    args = parser.parse_args()

    translator = None
    if not args.skip_translate:
        try:
            from deep_translator import GoogleTranslator

            translator = GoogleTranslator(source="en", target="ja")
        except ImportError:
            print("Run: .venv/bin/pip install deep-translator", file=sys.stderr)
            sys.exit(1)

    with open(CATALOG_PATH, encoding="utf-8") as file:
        catalog = json.load(file)

    books = catalog["books"]
    if args.book_id:
        books = [book for book in books if book["id"] == args.book_id]

    for book in books:
        print(f"Researching {book['title']} ({book['id']})...")
        process_book(book, translator, args.overwrite)

    print("Done. Run: python3 scripts/apply_distinction_manual.py")


if __name__ == "__main__":
    main()
