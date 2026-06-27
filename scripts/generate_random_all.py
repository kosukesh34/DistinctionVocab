#!/usr/bin/env python3
"""Generate complete random.json from source + translation chunks."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "data" / "distinction_manual" / "random_source.json"
OUT = ROOT / "data" / "distinction_manual" / "random.json"
CHUNK_DIR = Path(__file__).resolve().parent

def main():
    with open(SOURCE, encoding="utf-8") as f:
        source = json.load(f)

    merged = {}
    for chunk in sorted(CHUNK_DIR.glob("_random_t*.json")):
        merged.update({int(k): v for k, v in json.loads(chunk.read_text()).items()})

    result = []
    missing = []
    for word in source:
        n = word["number"]
        if n not in merged:
            missing.append(n)
            continue
        t = merged[n]
        result.append({
            "number": n,
            "headword": word["headword"],
            "nativeDefinition": t["nativeDefinition"],
            "japaneseMeaning": t["japaneseMeaning"],
            "etymology": t["etymology"],
            "examples": t["examples"],
        })

    if missing:
        raise SystemExit(f"Missing {len(missing)}: {missing[:30]}...")

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(f"Wrote {len(result)} words to {OUT}")

if __name__ == "__main__":
    main()
