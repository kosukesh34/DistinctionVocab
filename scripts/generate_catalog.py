#!/usr/bin/env python3
"""Extract vocabulary audio zips and generate vocabulary.json for the iOS app."""

import json
import re
import shutil
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
AUDIO_DIR = ROOT / "DistinctionVocab" / "DistinctionVocab" / "Resources" / "Audio"
CATALOG_PATH = ROOT / "DistinctionVocab" / "DistinctionVocab" / "Resources" / "vocabulary.json"
TRANSCRIPTION_CACHE_PATH = ROOT / "scripts" / ".transcription_cache.json"
HEADWORD_TRANSLATION_CACHE_PATH = ROOT / "scripts" / ".translation_headword_cache.json"
EXAMPLE_TRANSLATION_CACHE_PATH = ROOT / "scripts" / ".translation_example_cache.json"
PHONETIC_CACHE_PATH = ROOT / "scripts" / ".phonetic_cache.json"
DOWNLOADS = Path.home() / "Downloads"

BOOKS = [
    {"id": "dist1", "title": "Distinction I", "zip": "dist1.zip"},
    {"id": "earlybird", "title": "Distinction II", "zip": "earlybird.zip"},
    {"id": "juicy", "title": "Distinction III", "zip": "juicy.zip"},
    {"id": "random", "title": "Distinction IV", "zip": "random.zip"},
    {"id": "sbslike", "title": "Distinction V", "zip": "sbslike.zip"},
    {"id": "vibe", "title": "Distinction VI", "zip": "vibe.zip"},
]

HEADWORD_RE = re.compile(r"^(\d{3})(A)?\s+(.+)\.(mp3|wav)$", re.IGNORECASE)
EXAMPLE_RE = re.compile(r"^(\d{3})([BCDEF])\.(mp3|wav)$", re.IGNORECASE)


def normalize_name(name: str) -> str:
    return name.replace("_", "/")


def extract_zip(book_id: str, zip_path: Path, dest: Path) -> None:
    dest.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zip_path) as zf:
        for info in zf.infolist():
            if info.is_dir() or "__MACOSX" in info.filename or info.filename.startswith("."):
                continue
            filename = Path(info.filename).name
            if not filename.lower().endswith((".mp3", ".wav")):
                continue
            target = dest / filename
            if target.exists():
                continue
            with zf.open(info) as src, open(target, "wb") as out:
                shutil.copyfileobj(src, out)


def parse_book(book_id: str, title: str, book_dir: Path) -> dict:
    mp3_files = sorted(list(book_dir.glob("*.mp3")) + list(book_dir.glob("*.wav")))
    examples_by_number: dict[str, dict[str, str]] = {}
    headwords: dict[str, dict] = {}

    for path in mp3_files:
        name = path.name
        example_match = EXAMPLE_RE.match(name)
        if example_match:
            number, label, _ext = example_match.groups()
            examples_by_number.setdefault(number, {})[label.upper()] = f"{book_id}/{name}"
            continue

        headword_match = HEADWORD_RE.match(name)
        if headword_match:
            number, _suffix, text, _ext = headword_match.groups()
            headwords[number] = {
                "number": int(number),
                "headword": normalize_name(text.strip()),
                "headwordAudio": f"{book_id}/{name}",
                "phonetic": None,
                "nativeDefinition": None,
                "japaneseMeaning": None,
                "etymology": None,
            }

    words = []
    for number in sorted(headwords.keys(), key=int):
        entry = headwords[number]
        examples = []
        for label in ("B", "C", "D", "E", "F"):
            audio = examples_by_number.get(number, {}).get(label)
            if audio:
                examples.append({
                    "label": label,
                    "audio": audio,
                    "text": None,
                    "japaneseTranslation": None,
                })
        entry["examples"] = examples
        words.append(entry)

    return {"id": book_id, "title": title, "wordCount": len(words), "words": words}


def transcribe_example_sentences(catalog_books: list[dict]) -> dict[str, str]:
    """Load whisper transcription cache if available."""
    if TRANSCRIPTION_CACHE_PATH.exists():
        with open(TRANSCRIPTION_CACHE_PATH, encoding="utf-8") as cache_file:
            cached = json.load(cache_file)
        print(f"  loaded {len(cached)} cached transcriptions")
        return cached

    whisper_script = ROOT / "scripts" / "transcribe_catalog_whisper.py"
    venv_python = ROOT / ".venv" / "bin" / "python3"
    if whisper_script.exists() and venv_python.exists():
        print("  run scripts/transcribe_catalog_whisper.py to generate example text")

    return {}


def attach_transcribed_text(catalog_books: list[dict], transcriptions: dict[str, str]) -> None:
    for book in catalog_books:
        for word in book["words"]:
            for example in word["examples"]:
                example["text"] = transcriptions.get(example["audio"])


def load_translation_caches() -> tuple[dict[str, str], dict[str, str]]:
    headword_cache: dict[str, str] = {}
    example_cache: dict[str, str] = {}

    if HEADWORD_TRANSLATION_CACHE_PATH.exists():
        with open(HEADWORD_TRANSLATION_CACHE_PATH, encoding="utf-8") as cache_file:
            headword_cache = json.load(cache_file)

    if EXAMPLE_TRANSLATION_CACHE_PATH.exists():
        with open(EXAMPLE_TRANSLATION_CACHE_PATH, encoding="utf-8") as cache_file:
            example_cache = json.load(cache_file)

    return headword_cache, example_cache


def load_phonetic_cache() -> dict[str, str]:
    if PHONETIC_CACHE_PATH.exists():
        with open(PHONETIC_CACHE_PATH, encoding="utf-8") as cache_file:
            return json.load(cache_file)
    return {}


def attach_phonetics(catalog_books: list[dict], phonetic_cache: dict[str, str]) -> None:
    for book in catalog_books:
        for word in book["words"]:
            word["phonetic"] = phonetic_cache.get(word["headword"])


def attach_japanese_translations(
    catalog_books: list[dict],
    headword_cache: dict[str, str],
    example_cache: dict[str, str],
) -> None:
    for book in catalog_books:
        for word in book["words"]:
            word["japaneseMeaning"] = headword_cache.get(word["headword"])
            for example in word["examples"]:
                english_text = example.get("text")
                if english_text:
                    example["japaneseTranslation"] = example_cache.get(english_text)


def main() -> None:
    AUDIO_DIR.mkdir(parents=True, exist_ok=True)
    catalog_books = []

    for book in BOOKS:
        zip_path = DOWNLOADS / book["zip"]
        book_dir = AUDIO_DIR / book["id"]
        print(f"Processing {book['title']}...")
        if zip_path.exists():
            extract_zip(book["id"], zip_path, book_dir)
        elif not book_dir.exists():
            print(f"  Skipping {book['id']}: zip not found and no audio directory")
            continue
        catalog_books.append(parse_book(book["id"], book["title"], book_dir))
        print(f"  {catalog_books[-1]['wordCount']} words")

    transcriptions = transcribe_example_sentences(catalog_books)
    attach_transcribed_text(catalog_books, transcriptions)
    headword_cache, example_cache = load_translation_caches()
    phonetic_cache = load_phonetic_cache()
    attach_phonetics(catalog_books, phonetic_cache)
    attach_japanese_translations(catalog_books, headword_cache, example_cache)

    transcribed_count = sum(
        1
        for book in catalog_books
        for word in book["words"]
        for example in word["examples"]
        if example.get("text")
    )
    phonetic_count = sum(
        1 for book in catalog_books for word in book["words"] if word.get("phonetic")
    )
    translated_headwords = sum(
        1 for book in catalog_books for word in book["words"] if word.get("japaneseMeaning")
    )
    translated_examples = sum(
        1
        for book in catalog_books
        for word in book["words"]
        for example in word["examples"]
        if example.get("japaneseTranslation")
    )
    print(f"  {transcribed_count} example sentences with text")
    print(f"  {phonetic_count} headwords with phonetic transcription")
    print(f"  {translated_headwords} headwords with Japanese meaning")
    print(f"  {translated_examples} example sentences with Japanese translation")

    CATALOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(CATALOG_PATH, "w", encoding="utf-8") as f:
        json.dump({"books": catalog_books}, f, ensure_ascii=False, indent=2)
    print(f"Wrote {CATALOG_PATH}")

    import_script = ROOT / "scripts" / "import_custom_vocab.py"
    if import_script.exists():
        print("Merging custom vocabulary...")
        import importlib.util

        spec = importlib.util.spec_from_file_location("import_custom_vocab", import_script)
        if spec and spec.loader:
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            module.main([])


if __name__ == "__main__":
    main()
