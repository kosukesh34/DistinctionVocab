#!/usr/bin/env python3
"""Verify and enrich manual translations using internet dictionary sources.

Sources:
- Free Dictionary API + Wiktionary (English definitions, etymology)
- Weblio EJJE (idiom glosses from example dictionary)
- Jisho.org (single-word Japanese)
- deep-translator (idiom meaning + example B/C when missing)

Safe defaults: only fills empty fields. Use --apply-fixes to update mismatches
when web confidence is high.

Usage:
  .venv/bin/python scripts/verify_translations_online.py --book-id dist1 --report-only
  .venv/bin/python scripts/verify_translations_online.py --apply-fixes
  .venv/bin/python scripts/apply_distinction_manual.py
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
import urllib.parse
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parent.parent
CATALOG_PATH = ROOT / "DistinctionVocab" / "DistinctionVocab" / "Resources" / "vocabulary.json"
MANUAL_DIR = ROOT / "data" / "distinction_manual"
REPORT_DIR = ROOT / "data" / "distinction_manual" / "verification_reports"

BOOK_IDS = ("dist1", "earlybird", "juicy", "random", "sbslike", "vibe", "reibun")
REQUEST_HEADERS = {"User-Agent": "DistinctionVocab/1.0 (educational verification)"}

sys.path.insert(0, str(ROOT / "scripts"))
from enrich_vocabulary import (  # noqa: E402
    is_phrase,
    refine_definition,
)
from research_translations import (  # noqa: E402
    bad_japanese_for_idiom,
    build_native_definition,
    pick_jisho_meaning,
)

JISHO_API = "https://jisho.org/api/v1/search/words"


def load_json(path: Path, default=None):
    if path.exists():
        with open(path, encoding="utf-8") as file:
            return json.load(file)
    return default if default is not None else {}


def save_json(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)
        file.write("\n")


def weblio_query(headword: str) -> str:
    text = re.sub(r"\bsb\b", "someone", headword, flags=re.IGNORECASE)
    text = re.sub(r"\bsth\b", "something", text, flags=re.IGNORECASE)
    return urllib.parse.quote(text.replace(" ", "+"))


def fetch_weblio_idiom_gloss(headword: str) -> str | None:
    if not is_phrase(headword):
        return None
    url = f"https://ejje.weblio.jp/content/{weblio_query(headword)}"
    try:
        response = requests.get(url, headers=REQUEST_HEADERS, timeout=15)
        if response.status_code != 200:
            return None
        html = response.text
        marker = "Weblio例文辞書での"
        start = html.find(marker)
        if start == -1:
            return None
        chunk = html[start : start + 12000]
        match = re.search(
            r'class="werbjJ"[^>]*>.*?<p><a[^>]*>([^<]{2,40})</a></p>',
            chunk,
            re.DOTALL,
        )
        if match:
            gloss = match.group(1).strip()
            if re.search(r"[\u3040-\u9fff]", gloss) and "辞典" not in gloss:
                return gloss
    except requests.RequestException:
        return None
    return None


NAV_JA = frozenset(
    {
        "英語",
        "英和",
        "和英",
        "英韓",
        "英西",
        "西英",
        "日本語",
        "英和辞典・和英辞典",
        "ロングマン現代英英辞典",
    }
)


def is_valid_gloss(text: str) -> bool:
    if not text or text in NAV_JA:
        return False
    if any(marker in text for marker in ("辞典", "クイズ", "トピック", "ログイン", "Weblio")):
        return False
    return bool(re.search(r"[\u3040-\u9fff]", text))


def research_japanese_meaning(headword: str, native_definition: str, translator) -> tuple[str | None, str]:
    refined = refine_definition(native_definition, headword).rstrip(".")

    if is_phrase(headword):
        weblio = fetch_weblio_idiom_gloss(headword)
        time.sleep(0.15)
        if weblio and is_valid_gloss(weblio) and not bad_japanese_for_idiom(headword, weblio):
            return weblio, "weblio"

        if translator:
            try:
                gloss = translator.translate(refined)
                if gloss and is_valid_gloss(gloss) and not bad_japanese_for_idiom(headword, gloss):
                    return gloss, "translate_idiom"
            except Exception:
                pass
        return None, "none"

    jisho = pick_jisho_meaning(headword, native_definition)
    if jisho and is_valid_gloss(jisho):
        return jisho, "jisho"

    if translator:
        try:
            gloss = translator.translate(refined)
            if gloss and is_valid_gloss(gloss):
                return gloss, "translate"
        except Exception:
            pass
    return None, "none"


def normalize_ja(text: str) -> str:
    text = text.replace("；", "、").replace(";", "、")
    text = re.sub(r"\s+", "", text)
    return text


def meanings_similar(current: str, proposed: str) -> bool:
    if not current or not proposed:
        return False
    if normalize_ja(current) == normalize_ja(proposed):
        return True
    current_parts = set(re.split(r"[、；;・]", current))
    proposed_parts = set(re.split(r"[、；;・]", proposed))
    current_parts = {part.strip() for part in current_parts if part.strip()}
    proposed_parts = {part.strip() for part in proposed_parts if part.strip()}
    if not current_parts or not proposed_parts:
        return False
    overlap = current_parts & proposed_parts
    return len(overlap) >= min(len(current_parts), len(proposed_parts)) * 0.5


def verify_word(word: dict, manual_entry: dict | None, book_id: str, translator) -> dict:
    headword = word["headword"]
    number = word["number"]
    examples = word.get("examples", [])

    current_meaning = (manual_entry or {}).get("japaneseMeaning") or word.get("japaneseMeaning", "")
    current_native = (manual_entry or {}).get("nativeDefinition") or word.get("nativeDefinition", "")
    current_etymology = (manual_entry or {}).get("etymology") or word.get("etymology", "")

    native = current_native or build_native_definition(headword, examples)

    proposed_meaning = None
    meaning_source = "skip_reibun"
    if book_id != "reibun" and native:
        proposed_meaning, meaning_source = research_japanese_meaning(headword, native, translator)

    example_fixes: dict[str, str] = {}
    manual_examples = (manual_entry or {}).get("examples", {})
    if translator and book_id != "reibun":
        for example in examples:
            label = example.get("label", "")
            if label in {"D", "F"}:
                continue
            english = example.get("text", "")
            current_ja = manual_examples.get(label) or example.get("japaneseTranslation", "")
            if english and not current_ja:
                try:
                    example_fixes[label] = translator.translate(english)
                except Exception:
                    pass
                time.sleep(0.06)

    issue = None
    if (
        book_id != "reibun"
        and proposed_meaning
        and current_meaning
        and is_valid_gloss(proposed_meaning)
        and not bad_japanese_for_idiom(headword, proposed_meaning)
        and not meanings_similar(current_meaning, proposed_meaning)
    ):
        issue = "meaning_mismatch"

    return {
        "number": number,
        "headword": headword,
        "issue": issue,
        "currentMeaning": current_meaning,
        "proposedMeaning": proposed_meaning,
        "meaningSource": meaning_source,
        "exampleFixes": example_fixes,
        "fixes": {
            "japaneseMeaning": proposed_meaning if issue == "meaning_mismatch" else None,
            "examples": example_fixes or None,
        },
    }


def apply_fixes(manual_entries: dict[int, dict], result: dict, mode: str) -> bool:
    number = result["number"]
    entry = manual_entries.get(number)
    if not entry:
        entry = {"number": number, "headword": result["headword"]}
        manual_entries[number] = entry

    changed = False
    fixes = result["fixes"]

    if mode == "apply_fixes":
        if fixes.get("japaneseMeaning"):
            entry["japaneseMeaning"] = fixes["japaneseMeaning"]
            changed = True

    if fixes.get("examples"):
        entry.setdefault("examples", {})
        for label, translation in fixes["examples"].items():
            if translation and not entry["examples"].get(label):
                entry["examples"][label] = translation
                changed = True

    return changed


def process_book(book: dict, translator, mode: str) -> list[dict]:
    book_id = book["id"]
    manual_path = MANUAL_DIR / f"{book_id}.json"
    manual_list = load_json(manual_path, [])
    manual_by_number = {entry["number"]: entry for entry in manual_list}

    results: list[dict] = []
    changed = 0

    for index, word in enumerate(book["words"], start=1):
        result = verify_word(word, manual_by_number.get(word["number"]), book_id, translator)
        results.append(result)

        if apply_fixes(manual_by_number, result, mode):
            changed += 1

        if index % 50 == 0:
            print(f"  {book_id}: verified {index}/{len(book['words'])}")

    if mode == "apply_fixes" and changed:
        save_json(manual_path, sorted(manual_by_number.values(), key=lambda item: item["number"]))
        print(f"  {book_id}: applied fixes to {changed} entries")

    mismatches = [item for item in results if item.get("issue")]
    report_path = REPORT_DIR / f"{book_id}_report.json"
    save_json(report_path, {"bookId": book_id, "mismatches": mismatches, "total": len(results)})
    print(f"  {book_id}: {len(mismatches)} potential mismatches -> {report_path}")

    return results


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--book-id", choices=BOOK_IDS)
    parser.add_argument("--report-only", action="store_true", help="Only write mismatch reports")
    parser.add_argument("--apply-fixes", action="store_true", help="Apply high-confidence meaning fixes")
    parser.add_argument("--limit", type=int, default=0)
    args = parser.parse_args()

    mode = "report_only" if args.report_only or not args.apply_fixes else "apply_fixes"

    try:
        from deep_translator import GoogleTranslator

        translator = GoogleTranslator(source="en", target="ja")
    except ImportError:
        print("Run: .venv/bin/pip install beautifulsoup4 deep-translator", file=sys.stderr)
        sys.exit(1)

    with open(CATALOG_PATH, encoding="utf-8") as file:
        catalog = json.load(file)

    books = catalog["books"]
    if args.book_id:
        books = [book for book in books if book["id"] == args.book_id]

    for book in books:
        if args.limit:
            book = {**book, "words": book["words"][: args.limit]}
        print(f"Verifying {book['title']} ({book['id']})...")
        process_book(book, translator, mode)

    if mode == "apply_fixes":
        print("Run: .venv/bin/python scripts/apply_d_paraphrase_ja.py && .venv/bin/python scripts/apply_distinction_manual.py")


if __name__ == "__main__":
    main()
