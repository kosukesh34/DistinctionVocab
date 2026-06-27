#!/usr/bin/env python3
"""Import vocabulary from Apple Numbers or TSV files into vocabulary.json."""

from __future__ import annotations

import csv
import json
import re
import shutil
import subprocess
import sys
from io import StringIO
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
AUDIO_DIR = ROOT / "DistinctionVocab" / "DistinctionVocab" / "Resources" / "Audio"
CATALOG_PATH = ROOT / "DistinctionVocab" / "DistinctionVocab" / "Resources" / "vocabulary.json"
PHONETIC_CACHE_PATH = ROOT / "scripts" / ".phonetic_cache.json"

BOOK_ID = "reibun"
BOOK_TITLE = "例文付き"

NUMBERS_DOCUMENTS_DIR = Path.home() / "Library/Mobile Documents/com~apple~Numbers/Documents"
DEFAULT_NUMBERS_PATH = NUMBERS_DOCUMENTS_DIR / "例文付き111.numbers"
DEFAULT_TSV_PATH = NUMBERS_DOCUMENTS_DIR / "例文付き　2 2.tsv"
DEFAULT_SOURCE_FILES = [
    NUMBERS_DOCUMENTS_DIR / "300まで.numbers",
    DEFAULT_NUMBERS_PATH,
    NUMBERS_DOCUMENTS_DIR / "例文付き 3.numbers",
    DEFAULT_TSV_PATH,
]

JP_RE = re.compile(r"[\u3040-\u30ff\u4e00-\u9fff]")
PLACEHOLDER_RE = re.compile(r"^[\d\s:]+$")
HEADWORD_FILE_RE = re.compile(r"[^\w\s\-'/.]", re.UNICODE)


def normalize_text(value: str) -> str:
    return value.replace("==", "'").replace("\xa0", " ").strip()


def is_placeholder(value: str) -> bool:
    value = normalize_text(value)
    return not value or value in {"1", ":"} or PLACEHOLDER_RE.match(value) is not None


def looks_english_example(value: str) -> bool:
    value = normalize_text(value)
    if is_placeholder(value) or len(value) < 4:
        return False
    if len(value) > 220:
        return False
    alpha = sum(1 for char in value if char.isalpha())
    if alpha < 3:
        return False
    return not JP_RE.search(value)


def looks_japanese_translation(value: str) -> bool:
    value = normalize_text(value)
    if is_placeholder(value):
        return False
    return bool(JP_RE.search(value))


def safe_audio_filename(number: int, label: str, text: str, extension: str = "mp3") -> str:
    if label == "headword":
        cleaned = HEADWORD_FILE_RE.sub("", text)
        cleaned = re.sub(r"\s+", " ", cleaned).strip()
        return f"{number:03d} {cleaned}.{extension}"
    return f"{number:03d}{label}.{extension}"


def parse_examples(parts: list[str]) -> list[dict[str, str | None]]:
    examples: list[dict[str, str | None]] = []
    labels = ("B", "C", "D", "E", "F")

    if len(parts) > 4:
        english = normalize_text(parts[3])
        japanese = normalize_text(parts[4])
        if looks_english_example(english):
            examples.append(
                {
                    "label": "B",
                    "text": english,
                    "japaneseTranslation": japanese if looks_japanese_translation(japanese) else None,
                }
            )

    label_index = 1
    index = 5
    while index < len(parts) - 1 and label_index < len(labels):
        english = normalize_text(parts[index])
        japanese = normalize_text(parts[index + 1])
        if looks_english_example(english) and looks_japanese_translation(japanese):
            examples.append(
                {
                    "label": labels[label_index],
                    "text": english,
                    "japaneseTranslation": japanese,
                }
            )
            label_index += 1
            index += 2
            continue
        index += 1

    return examples


def parse_tsv(path: Path) -> list[dict]:
    rows: list[dict] = []
    with open(path, encoding="utf-8") as file:
        reader = csv.reader(file, delimiter="\t")
        header = next(reader, None)
        if not header:
            return rows
        for raw in reader:
            if not raw or not raw[0].strip():
                continue
            number = raw[0].strip()
            if not number.isdigit():
                continue
            headword = raw[1].strip() if len(raw) > 1 else ""
            meaning = raw[2].strip() if len(raw) > 2 else ""
            padded = raw + [""] * (20 - len(raw))
            rows.append(
                {
                    "number": int(number),
                    "headword": headword,
                    "japaneseMeaning": meaning or None,
                    "examples": parse_examples(padded),
                }
            )
    return rows


def parse_numbers(path: Path) -> list[dict]:
    try:
        from numbers_parser import Document
    except ImportError as exc:
        raise SystemExit("numbers-parser is required. Install with: pip install numbers-parser") from exc

    document = Document(str(path))
    table = document.sheets[0].tables[0]
    rows: list[dict] = []

    for row_index in range(1, table.num_rows):
        raw = table.cell(row_index, 0).value
        if not raw:
            continue
        parts = next(csv.reader(StringIO(str(raw))))
        if len(parts) < 3 or not parts[0].strip().isdigit():
            continue
        rows.append(
            {
                "number": int(parts[0].strip()),
                "headword": parts[1].strip(),
                "japaneseMeaning": parts[2].strip() or None,
                "examples": parse_examples(parts),
            }
        )
    return rows


def merge_row(existing: dict, incoming: dict) -> dict:
    if len(incoming.get("examples", [])) > len(existing.get("examples", [])):
        merged = incoming.copy()
    elif incoming.get("examples") and not existing.get("examples"):
        merged = incoming.copy()
    else:
        merged = existing.copy()

    if not merged.get("japaneseMeaning") and incoming.get("japaneseMeaning"):
        merged["japaneseMeaning"] = incoming["japaneseMeaning"]
    if not merged.get("headword"):
        merged["headword"] = incoming.get("headword", "")
    return merged


def dedupe_rows(rows: list[dict]) -> list[dict]:
    by_number: dict[int, dict] = {}
    for row in rows:
        number = row["number"]
        if number in by_number:
            by_number[number] = merge_row(by_number[number], row)
        else:
            by_number[number] = row
    return [by_number[number] for number in sorted(by_number)]


def load_rows_from_source(path: Path) -> list[dict]:
    if not path.exists():
        return []
    if path.suffix.lower() == ".tsv":
        return parse_tsv(path)
    if path.suffix.lower() == ".numbers":
        return parse_numbers(path)
    raise SystemExit(f"Unsupported file type: {path}")


def load_merged_rows(source_paths: list[Path]) -> tuple[list[dict], list[str]]:
    rows: list[dict] = []
    loaded_sources: list[str] = []
    for path in source_paths:
        parsed = load_rows_from_source(path)
        if not parsed:
            continue
        rows.extend(parsed)
        loaded_sources.append(path.name)
    return dedupe_rows(rows), loaded_sources


def load_own_book_audio_index(catalog_path: Path) -> dict[int, dict]:
    """Reuse audio paths already stored for this book in vocabulary.json."""
    if not catalog_path.exists():
        return {}

    with open(catalog_path, encoding="utf-8") as file:
        catalog = json.load(file)

    own_book = next((book for book in catalog.get("books", []) if book.get("id") == BOOK_ID), None)
    if not own_book:
        return {}

    index: dict[int, dict] = {}
    for word in own_book.get("words", []):
        index[word["number"]] = {
            "headwordAudio": word.get("headwordAudio"),
            "examples": word.get("examples", []),
        }
    return index


def load_phonetic_cache() -> dict[str, str]:
    if PHONETIC_CACHE_PATH.exists():
        with open(PHONETIC_CACHE_PATH, encoding="utf-8") as file:
            return json.load(file)
    return {}


def generate_phonetic(headword: str, cache: dict[str, str]) -> str | None:
    if headword in cache:
        return cache[headword]
    try:
        import eng_to_ipa as ipa
    except ImportError:
        return None

    normalized = re.sub(
        r"\b(sb|sth|sb's|sth's)\b",
        lambda match: {"sb": "somebody", "sth": "something"}.get(match.group(1).lower(), match.group(1)),
        headword,
        flags=re.IGNORECASE,
    )
    converted = ipa.convert(normalized).replace("*", "")
    converted = re.sub(r"\s+", " ", converted).strip()
    return converted or None


def generate_tts_mp3(text: str, output_path: Path) -> bool:
    if output_path.exists():
        return True

    output_path.parent.mkdir(parents=True, exist_ok=True)
    aiff_path = output_path.with_suffix(".aiff")
    try:
        subprocess.run(
            ["say", "-v", "Samantha", text, "-o", str(aiff_path)],
            check=True,
            capture_output=True,
        )
        subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-i",
                str(aiff_path),
                "-ar",
                "44100",
                "-ac",
                "1",
                str(output_path),
            ],
            check=True,
            capture_output=True,
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False
    finally:
        if aiff_path.exists():
            aiff_path.unlink()


def copy_own_audio(source_relative: str, destination: Path) -> bool:
    if not source_relative.startswith(f"{BOOK_ID}/"):
        return False
    source = AUDIO_DIR / source_relative
    if not source.exists():
        return False
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists():
        return True
    shutil.copy2(source, destination)
    return True


def build_book(
    rows: list[dict],
    *,
    generate_audio: bool,
) -> tuple[dict, dict[str, int]]:
    own_audio_index = load_own_book_audio_index(CATALOG_PATH)
    phonetic_cache = load_phonetic_cache()
    book_dir = AUDIO_DIR / BOOK_ID

    stats = {
        "words": 0,
        "generated_headword_audio": 0,
        "reused_headword_audio": 0,
        "generated_example_audio": 0,
        "reused_example_audio": 0,
        "examples_with_text": 0,
    }

    words: list[dict] = []
    for row in rows:
        number = row["number"]
        headword = row["headword"]
        own_word = own_audio_index.get(number, {})

        headword_filename = safe_audio_filename(number, "headword", headword)
        headword_audio = f"{BOOK_ID}/{headword_filename}"
        headword_path = book_dir / headword_filename

        existing_headword_audio = own_word.get("headwordAudio")
        if existing_headword_audio and copy_own_audio(existing_headword_audio, headword_path):
            headword_audio = f"{BOOK_ID}/{headword_filename}"
            stats["reused_headword_audio"] += 1
        elif headword_path.exists():
            stats["reused_headword_audio"] += 1
        elif generate_audio and generate_tts_mp3(headword, headword_path):
            stats["generated_headword_audio"] += 1

        examples_out: list[dict] = []
        own_examples = {
            example.get("label"): example.get("audio")
            for example in own_word.get("examples", [])
            if example.get("label")
        }
        for example in row["examples"]:
            label = example["label"]
            text = example.get("text")
            if text:
                stats["examples_with_text"] += 1

            example_filename = safe_audio_filename(number, label, headword)
            example_audio = f"{BOOK_ID}/{example_filename}"
            example_path = book_dir / example_filename

            existing_example_audio = own_examples.get(label)
            if existing_example_audio and copy_own_audio(existing_example_audio, example_path):
                stats["reused_example_audio"] += 1
            elif example_path.exists():
                stats["reused_example_audio"] += 1
            elif generate_audio and text and generate_tts_mp3(text, example_path):
                stats["generated_example_audio"] += 1

            examples_out.append(
                {
                    "label": label,
                    "audio": example_audio,
                    "text": text,
                    "japaneseTranslation": example.get("japaneseTranslation"),
                }
            )

        phonetic = generate_phonetic(headword, phonetic_cache)
        words.append(
            {
                "number": number,
                "headword": headword,
                "headwordAudio": headword_audio,
                "phonetic": phonetic,
                "japaneseMeaning": row.get("japaneseMeaning"),
                "examples": examples_out,
            }
        )
        stats["words"] += 1

    book = {
        "id": BOOK_ID,
        "title": BOOK_TITLE,
        "wordCount": len(words),
        "words": words,
    }
    return book, stats


def merge_book_into_catalog(book: dict, catalog_path: Path) -> None:
    if catalog_path.exists():
        with open(catalog_path, encoding="utf-8") as file:
            catalog = json.load(file)
    else:
        catalog = {"books": []}

    catalog["books"] = [item for item in catalog.get("books", []) if item.get("id") != BOOK_ID]
    catalog["books"].append(book)

    catalog_path.parent.mkdir(parents=True, exist_ok=True)
    with open(catalog_path, "w", encoding="utf-8") as file:
        json.dump(catalog, file, ensure_ascii=False, indent=2)


def resolve_source_paths(path: Path | None) -> list[Path]:
    if path is not None:
        return [path]
    return [candidate for candidate in DEFAULT_SOURCE_FILES if candidate.exists()]


def main(argv: list[str] | None = None) -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Import 例文付き vocabulary as an independent book.")
    parser.add_argument("source", nargs="?", type=Path, help="Numbers or TSV file path")
    parser.add_argument("--no-audio", action="store_true", help="Skip TTS audio generation")
    args = parser.parse_args(argv)

    source_paths = resolve_source_paths(args.source)
    if not source_paths:
        raise SystemExit("No 例文付き source file found.")

    rows, loaded_sources = load_merged_rows(source_paths)
    print(f"Importing {', '.join(loaded_sources)} as independent book '{BOOK_TITLE}'...")
    book, stats = build_book(rows, generate_audio=not args.no_audio)
    merge_book_into_catalog(book, CATALOG_PATH)

    words_with_examples = sum(1 for row in rows if row.get("examples"))
    print(f"Wrote {len(rows)} words to {CATALOG_PATH}")
    print(f"  book id: {BOOK_ID}")
    print(f"  words with examples: {words_with_examples}")
    print(f"  reused headword audio: {stats['reused_headword_audio']}")
    print(f"  generated headword audio: {stats['generated_headword_audio']}")
    print(f"  reused example audio: {stats['reused_example_audio']}")
    print(f"  generated example audio: {stats['generated_example_audio']}")
    print(f"  example sentences: {stats['examples_with_text']}")


if __name__ == "__main__":
    main(sys.argv[1:])
