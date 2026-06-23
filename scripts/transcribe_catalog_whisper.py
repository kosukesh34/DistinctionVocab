#!/usr/bin/env python3
"""Transcribe example sentence audio and update vocabulary.json."""

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CATALOG_PATH = ROOT / "DistinctionVocab" / "DistinctionVocab" / "Resources" / "vocabulary.json"
AUDIO_ROOT = ROOT / "DistinctionVocab" / "DistinctionVocab" / "Resources" / "Audio"
CACHE_PATH = ROOT / "scripts" / ".transcription_cache.json"
EXAMPLE_TRANSLATION_CACHE_PATH = ROOT / "scripts" / ".translation_example_cache.json"
HEADWORD_TRANSLATION_CACHE_PATH = ROOT / "scripts" / ".translation_headword_cache.json"


def load_cache() -> dict[str, str]:
    if CACHE_PATH.exists():
        with open(CACHE_PATH, encoding="utf-8") as cache_file:
            return json.load(cache_file)
    return {}


def save_cache(cache: dict[str, str]) -> None:
    CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(CACHE_PATH, "w", encoding="utf-8") as cache_file:
        json.dump(cache, cache_file, ensure_ascii=False, indent=2)


def load_json(path: Path) -> dict[str, str]:
    if path.exists():
        with open(path, encoding="utf-8") as file:
            return json.load(file)
    return {}


def attach_all(catalog: dict, transcription_cache: dict[str, str]) -> None:
    example_translation_cache = load_json(EXAMPLE_TRANSLATION_CACHE_PATH)
    headword_translation_cache = load_json(HEADWORD_TRANSLATION_CACHE_PATH)

    for book in catalog["books"]:
        for word in book["words"]:
            if not word.get("japaneseMeaning"):
                word["japaneseMeaning"] = headword_translation_cache.get(word["headword"])

            for example in word["examples"]:
                if not example.get("text"):
                    example["text"] = transcription_cache.get(example["audio"])
                if not example.get("japaneseTranslation"):
                    english_text = example.get("text")
                    if english_text:
                        example["japaneseTranslation"] = example_translation_cache.get(english_text)


def write_catalog(catalog: dict) -> None:
    temp_path = CATALOG_PATH.with_suffix(".json.tmp")
    with open(temp_path, "w", encoding="utf-8") as catalog_file:
        json.dump(catalog, catalog_file, ensure_ascii=False, indent=2)
    temp_path.replace(CATALOG_PATH)


def collect_pending(catalog: dict, cache: dict[str, str], book_id: str | None) -> list[tuple[str, Path]]:
    pending: list[tuple[str, Path]] = []

    for book in catalog["books"]:
        if book_id and book["id"] != book_id:
            continue
        for word in book["words"]:
            for example in word["examples"]:
                audio_key = example["audio"]
                if example.get("text") or audio_key in cache:
                    continue
                audio_path = AUDIO_ROOT / audio_key
                if audio_path.exists():
                    pending.append((audio_key, audio_path))

    return pending


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--book-id", help="Transcribe only one book (e.g. earlybird)")
    args = parser.parse_args()

    try:
        import whisper
    except ImportError:
        print("Run: .venv/bin/pip install openai-whisper", file=sys.stderr)
        sys.exit(1)

    with open(CATALOG_PATH, encoding="utf-8") as catalog_file:
        catalog = json.load(catalog_file)

    cache = load_cache()
    pending = collect_pending(catalog, cache, args.book_id)

    print(f"Pending transcriptions: {len(pending)}")
    if not pending:
        attach_all(catalog, cache)
        write_catalog(catalog)
        print("Nothing to transcribe.")
        return

    model = whisper.load_model("tiny")
    total = len(pending)

    for index, (audio_key, audio_path) in enumerate(pending, start=1):
        result = model.transcribe(str(audio_path), language="en", fp16=False)
        cache[audio_key] = result["text"].strip()

        if index % 25 == 0 or index == total:
            save_cache(cache)
            print(f"  {index}/{total} transcribed", flush=True)

    save_cache(cache)
    attach_all(catalog, cache)
    write_catalog(catalog)
    print("Done.", flush=True)


if __name__ == "__main__":
    main()
