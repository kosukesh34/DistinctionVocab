#!/usr/bin/env python3
"""Optional: fetch English reference data (nativeDefinition) for vocabulary.json.

Japanese translations (japaneseMeaning, etymology, example translations) should be
added manually via scripts/export_translations.py and scripts/import_manual_translations.py.
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
DEFINITION_CACHE_PATH = ROOT / "scripts" / ".enrichment_definition_cache.json"
ETYMOLOGY_CACHE_PATH = ROOT / "scripts" / ".enrichment_etymology_cache.json"
MEANING_CACHE_PATH = ROOT / "scripts" / ".enrichment_meaning_cache.json"
EXAMPLE_CACHE_PATH = ROOT / "scripts" / ".enrichment_example_cache.json"
ETYMOLOGY_JA_CACHE_PATH = ROOT / "scripts" / ".enrichment_etymology_ja_cache.json"

WIKTIONARY_API = "https://en.wiktionary.org/w/api.php"
DICTIONARY_API = "https://api.dictionaryapi.dev/api/v2/entries/en"
REQUEST_HEADERS = {"User-Agent": "DistinctionVocab/1.0 (educational app)"}

ANTONYM_PREFIXES = ("an ", "a ")


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


def clean_wikitext(text: str) -> str:
    text = re.sub(r"\[\[([^|\]]+\|)?([^\]]+)\]\]", r"\2", text)
    text = re.sub(r"\{\{[^}]+\}\}", "", text)
    text = re.sub(r"'''([^']+)'''", r"\1", text)
    text = re.sub(r"''([^']+)''", r"\1", text)
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def lookup_key_word(headword: str) -> str:
    normalized = headword.lower().strip()
    normalized = re.sub(r"\bsb\b|\bsth\b|\bsomebody\b|\bsomething\b", "", normalized)
    normalized = re.sub(r"[^\w\s-]", " ", normalized)
    normalized = re.sub(r"\s+", " ", normalized).strip()
    if not normalized:
        return headword.split()[0].lower()
    parts = normalized.split()
    return parts[0] if len(parts) == 1 else max(parts, key=len)


def normalize_for_wiktionary(headword: str) -> str:
    text = re.sub(r"\bsb\b", "someone", headword, flags=re.IGNORECASE)
    text = re.sub(r"\bsth\b", "something", text, flags=re.IGNORECASE)
    text = re.sub(r"\([^)]*\)", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def fetch_wiktionary_definition(headword: str) -> str | None:
    candidates = [normalize_for_wiktionary(headword), headword.lower()]
    seen: set[str] = set()
    for candidate in candidates:
        candidate = candidate.strip("- ")
        if not candidate or candidate in seen:
            continue
        seen.add(candidate)
        try:
            response = requests.get(
                WIKTIONARY_API,
                params={
                    "action": "query",
                    "titles": candidate,
                    "prop": "extracts",
                    "explaintext": "1",
                    "format": "json",
                },
                headers=REQUEST_HEADERS,
                timeout=12,
            )
            if response.status_code != 200:
                continue
            pages = response.json().get("query", {}).get("pages", {})
            for page in pages.values():
                extract = page.get("extract", "")
                match = re.search(
                    r"\(idiomatic\)\s*(.+?)(?:\n\n|\n====|\Z)",
                    extract,
                    re.DOTALL | re.IGNORECASE,
                )
                if match:
                    return clean_wikitext(match.group(1))
        except (requests.RequestException, json.JSONDecodeError, KeyError):
            continue
        time.sleep(0.05)
    return None


def is_phrase(headword: str) -> bool:
    lowered = headword.lower()
    return " " in lowered or "sb" in lowered or "sth" in lowered


def fetch_dictionary_definition(headword: str) -> str | None:
    if is_phrase(headword):
        return None

    candidates = [
        headword.lower(),
        normalize_for_wiktionary(headword).lower(),
    ]
    if not is_phrase(headword):
        candidates.append(lookup_key_word(headword))
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
            payload = response.json()
            if not payload:
                continue
            definitions: list[str] = []
            for meaning in payload[0].get("meanings", []):
                for definition in meaning.get("definitions", []):
                    text = definition.get("definition", "").strip()
                    if text and text not in definitions:
                        definitions.append(text)
                    if len(definitions) >= 2:
                        break
                if len(definitions) >= 2:
                    break
            if definitions:
                return "; ".join(definitions[:2])
        except requests.RequestException:
            continue
        time.sleep(0.05)
    return None


def fetch_etymology(headword: str) -> str | None:
    candidates = [
        headword.lower(),
        normalize_for_wiktionary(headword).lower(),
        lookup_key_word(headword),
    ]
    seen: set[str] = set()
    for candidate in candidates:
        candidate = candidate.strip("- ")
        if not candidate or candidate in seen:
            continue
        seen.add(candidate)
        try:
            response = requests.get(
                WIKTIONARY_API,
                params={
                    "action": "parse",
                    "page": candidate,
                    "prop": "wikitext",
                    "format": "json",
                },
                headers=REQUEST_HEADERS,
                timeout=12,
            )
            if response.status_code != 200:
                continue
            payload = response.json()
            if "parse" not in payload:
                continue
            wikitext = payload["parse"]["wikitext"]["*"]
            match = re.search(r"===\s*Etymology\s*===\s*(.*?)(?=\n===)", wikitext, re.DOTALL)
            if not match:
                continue
            cleaned = clean_wikitext(match.group(1))
            if cleaned:
                return cleaned[:280]
        except (requests.RequestException, json.JSONDecodeError, KeyError):
            continue
        time.sleep(0.05)
    return None


def example_by_label(examples: list[dict], label: str) -> str | None:
    for example in examples:
        if example.get("label") == label:
            text = example.get("text")
            if text and text.strip():
                return text.strip()
    return None


def normalize_definition_phrase(text: str) -> str:
    text = text.strip()
    if not text:
        return text
    if not text.endswith("."):
        text += "."
    return text[0].upper() + text[1:]


def is_antonym_hint(text: str) -> bool:
    lowered = text.strip().lower()
    return lowered.startswith(ANTONYM_PREFIXES)


def is_unreliable_d_definition(d_text: str) -> bool:
    lowered = d_text.strip().lower()
    return lowered.startswith("for somebody") or lowered.startswith("for someone")


def infer_phrasal_definition(headword: str, examples: list[dict]) -> str | None:
    lowered = headword.lower()
    if "kick" in lowered and "out" in lowered:
        return "To force someone to leave a place."
    if "figure" in lowered and "out" in lowered:
        return "To understand or solve something."
    if "watch out" in lowered:
        return "To be careful of someone or something."
    if "slack off" in lowered:
        return "To work less hard than usual."
    if "check" in lowered and "out" in lowered:
        return "To look at or investigate something."
    if "bring" in lowered and "up" in lowered:
        return "To mention or introduce a topic."
    if "cut" in lowered and "off" in lowered:
        return "To stop providing something or disconnect."
    if "hold" in lowered and "up" in lowered:
        return "To delay or rob."
    b_text = example_by_label(examples, "B")
    if b_text:
        return f"Used in contexts such as: \"{b_text}\""
    return None


def synonym_substitution(text: str, headword: str, d_text: str | None) -> str:
    if not d_text or is_antonym_hint(d_text) or is_unreliable_d_definition(d_text):
        return text

    synonym = d_text.strip().rstrip(".")
    synonym_me = re.sub(r"\bsomebody\b|\bsomeone\b", "me", synonym, flags=re.IGNORECASE)
    if synonym_me and synonym_me[0].isupper():
        synonym_me = synonym_me[0].lower() + synonym_me[1:]

    replacements = [
        (r"driving me up the wall", "driving me crazy"),
        (r"drives me up the wall", "drives me crazy"),
        (r"got kicked out of", "was forced to leave"),
        (r"get kicked out of", "be forced to leave"),
        (r"kicked out of", "forced to leave"),
    ]
    for pattern, replacement in replacements:
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)

    headword_patterns = [
        re.sub(r"\bsb\b", "me", headword, flags=re.IGNORECASE),
        re.sub(r"\bsb\b", "someone", headword, flags=re.IGNORECASE),
        headword,
    ]
    for pattern in headword_patterns:
        if pattern.lower() in text.lower():
            text = re.sub(re.escape(pattern), synonym_me, text, flags=re.IGNORECASE)
            break

    return text


def is_valid_etymology(text: str | None) -> bool:
    if not text:
        return False
    cleaned = text.strip()
    if len(cleaned) <= 18 or cleaned in {"From .", "From", "From 。"}:
        return False
    alpha = sum(1 for char in cleaned if char.isalpha())
    return alpha >= 12


def build_native_definition(headword: str, examples: list[dict], dictionary_def: str | None) -> str:
    d_text = example_by_label(examples, "D")
    if d_text and is_unreliable_d_definition(d_text):
        d_text = None

    if d_text and is_antonym_hint(d_text):
        if "black and white" in headword.lower():
            return "Clear-cut; involving only two opposing sides with no gray area."
        antonym = d_text.strip().rstrip(".").lower()
        return f"Distinct from being {antonym}; used in a specific idiomatic sense."

    if d_text:
        d_parts = [part.strip() for part in re.split(r"[.;]", d_text) if part.strip()]
        d_definition = "; ".join(normalize_definition_phrase(part).rstrip(".") for part in d_parts)
        return d_definition + ("" if d_definition.endswith(".") else ".")

    if not is_phrase(headword):
        wiktionary_def = fetch_wiktionary_definition(headword)
        if wiktionary_def:
            return normalize_definition_phrase(wiktionary_def)

    if dictionary_def and not is_phrase(headword):
        return dictionary_def if dictionary_def.endswith(".") else dictionary_def + "."

    inferred = infer_phrasal_definition(headword, examples)
    if inferred:
        return inferred if inferred.endswith(".") else inferred + "."

    b_text = example_by_label(examples, "B")
    if b_text:
        return f"A native expression used in contexts like: \"{b_text}\""

    return f"A common native English expression: {headword}."


def translate_text(translator, text: str, retries: int = 3) -> str:
    normalized = text.strip()
    if not normalized:
        return ""
    for attempt in range(retries):
        try:
            return translator.translate(normalized)
        except Exception:
            if attempt == retries - 1:
                raise
            time.sleep(0.8 * (attempt + 1))
    return ""


def normalize_for_translation(text: str, label: str) -> str:
    text = text.strip()
    if label == "D" and text and not text.lower().startswith("to "):
        lowered = text[0].lower() + text[1:]
        if lowered.endswith("."):
            lowered = lowered[:-1]
        return f"to {lowered}"
    return text


def refine_definition(definition: str, headword: str) -> str:
    parts = [part.strip() for part in definition.split(";") if part.strip()]
    if len(parts) <= 1:
        return definition

    preferred_keywords = (
        "restrained",
        "subtle",
        "idiomatic",
        "angry",
        "frustrat",
        "force",
        "clear",
        "careful",
        "messy",
        "exaggerat",
        "obvious",
        "native",
    )
    for part in reversed(parts):
        lowered = part.lower()
        if any(keyword in lowered for keyword in preferred_keywords):
            return part

    if "black and white" in headword.lower():
        for part in parts:
            if "police" not in part.lower():
                return part

    return parts[-1]


def translate_example(
    translator,
    english_text: str,
    headword: str,
    label: str,
    native_definition: str | None,
    examples: list[dict] | None = None,
) -> str:
    d_text = example_by_label(examples or [], "D") if examples else None
    if label == "D" and d_text and is_unreliable_d_definition(d_text) and native_definition:
        return translate_meaning(translator, native_definition, headword)
    source = normalize_for_translation(english_text, label)
    return translate_text(translator, source)


def translate_meaning(translator, native_definition: str, headword: str) -> str:
    _ = headword
    refined = refine_definition(native_definition, headword)
    return translate_text(translator, refined.rstrip("."))


def translate_etymology(translator, etymology: str, headword: str) -> str:
    _ = headword
    return translate_text(translator, etymology)


def enrich_catalog(
    catalog: dict,
    *,
    book_id: str | None,
    force: bool,
    skip_translate: bool,
) -> None:
    definition_cache = load_cache(DEFINITION_CACHE_PATH)
    etymology_cache = load_cache(ETYMOLOGY_CACHE_PATH)
    etymology_ja_cache = load_cache(ETYMOLOGY_JA_CACHE_PATH)
    meaning_cache = load_cache(MEANING_CACHE_PATH)
    example_cache = load_cache(EXAMPLE_CACHE_PATH)

    translator = None
    if not skip_translate:
        try:
            from deep_translator import GoogleTranslator
        except ImportError:
            print("Run: .venv/bin/pip install deep-translator", file=sys.stderr)
            sys.exit(1)
        translator = GoogleTranslator(source="en", target="ja")

    target_books = catalog["books"]
    if book_id:
        target_books = [book for book in catalog["books"] if book["id"] == book_id]
        if not target_books:
            print(f"Book not found: {book_id}", file=sys.stderr)
            sys.exit(1)

    total_words = sum(len(book["words"]) for book in target_books)
    processed_words = 0

    for book in target_books:
        for word in book["words"]:
            processed_words += 1
            headword = word["headword"]
            examples = word.get("examples", [])

            dict_cache_key = headword.lower()
            if force or dict_cache_key not in definition_cache:
                dictionary_def = fetch_dictionary_definition(headword)
                if dictionary_def:
                    dictionary_def = refine_definition(dictionary_def, headword)
                definition_cache[dict_cache_key] = build_native_definition(
                    headword, examples, dictionary_def
                )
                time.sleep(0.08)
            word["nativeDefinition"] = definition_cache[dict_cache_key]

            etym_cache_key = lookup_key_word(headword)
            if force or etym_cache_key not in etymology_cache:
                if is_phrase(headword):
                    etymology = fetch_etymology(normalize_for_wiktionary(headword))
                else:
                    etymology = fetch_etymology(headword)
                    if not etymology:
                        etymology = fetch_etymology(normalize_for_wiktionary(headword))
                if not etymology and is_phrase(headword):
                    etymology = (
                        f'Idiomatic expression built around "{etym_cache_key}".'
                    )
                etymology_cache[etym_cache_key] = etymology or ""
                time.sleep(0.08)

            raw_etymology = etymology_cache.get(etym_cache_key) or None
            if translator and raw_etymology and is_valid_etymology(raw_etymology):
                etymology_key = f"{headword}::{raw_etymology}"
                if force or etymology_key not in etymology_ja_cache:
                    etymology_ja_cache[etymology_key] = translate_etymology(
                        translator, raw_etymology, headword
                    )
                    time.sleep(0.12)
                word["etymology"] = etymology_ja_cache.get(etymology_key) or raw_etymology
            else:
                word["etymology"] = None

            if translator:
                meaning_key = f"{headword}::{word['nativeDefinition']}"
                if force or meaning_key not in meaning_cache:
                    meaning_cache[meaning_key] = translate_meaning(
                        translator, word["nativeDefinition"], headword
                    )
                    time.sleep(0.12)
                word["japaneseMeaning"] = meaning_cache[meaning_key]

                for example in examples:
                    english_text = example.get("text")
                    if not english_text:
                        continue
                    example_key = f"{headword}::{example['label']}::{english_text}"
                    if force or example_key not in example_cache:
                        example_cache[example_key] = translate_example(
                            translator,
                            english_text,
                            headword,
                            example.get("label", ""),
                            word.get("nativeDefinition"),
                            examples,
                        )
                        time.sleep(0.12)
                    example["japaneseTranslation"] = example_cache[example_key]

            if processed_words % 25 == 0 or processed_words == total_words:
                save_cache(DEFINITION_CACHE_PATH, definition_cache)
                save_cache(ETYMOLOGY_CACHE_PATH, etymology_cache)
                save_cache(ETYMOLOGY_JA_CACHE_PATH, etymology_ja_cache)
                save_cache(MEANING_CACHE_PATH, meaning_cache)
                save_cache(EXAMPLE_CACHE_PATH, example_cache)
                write_catalog(catalog)
                print(f"  words {processed_words}/{total_words}")

    save_cache(DEFINITION_CACHE_PATH, definition_cache)
    save_cache(ETYMOLOGY_CACHE_PATH, etymology_cache)
    save_cache(ETYMOLOGY_JA_CACHE_PATH, etymology_ja_cache)
    save_cache(MEANING_CACHE_PATH, meaning_cache)
    save_cache(EXAMPLE_CACHE_PATH, example_cache)
    write_catalog(catalog)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--book-id", help="Process only one book (e.g. dist1)")
    parser.add_argument("--force", action="store_true", help="Re-fetch and re-translate everything")
    parser.add_argument(
        "--skip-translate",
        action="store_true",
        help="Only fetch native definitions and etymology",
    )
    args = parser.parse_args()

    with open(CATALOG_PATH, encoding="utf-8") as catalog_file:
        catalog = json.load(catalog_file)

    enrich_catalog(
        catalog,
        book_id=args.book_id,
        force=args.force,
        skip_translate=args.skip_translate,
    )
    print("Done.")


if __name__ == "__main__":
    main()
