#!/usr/bin/env python3
"""Generate chapter audio and sentence timings from content/stories.json.

Each sentence is synthesized on its own with edge-tts and the MP3 bytes are
concatenated into one file per chapter. edge-tts returns constant 48 kbps MP3,
so a sentence's start time is simply (bytes before it) / bytes-per-second,
which keeps the on-screen highlight exactly in sync with the audio.

Usage:
    .venv/bin/python tools/generate_audio.py              # only changed chapters
    .venv/bin/python tools/generate_audio.py --force      # regenerate everything
    .venv/bin/python tools/generate_audio.py --book pip   # a single book
"""

import argparse
import asyncio
import hashlib
import json
import re
import sys
from pathlib import Path

import edge_tts
import edge_tts.communicate as _communicate
from edge_tts.constants import TRUSTED_CLIENT_TOKEN

ROOT = Path(__file__).resolve().parent.parent
STORIES = ROOT / "content" / "stories.json"
CACHE = ROOT / "content" / "audio-cache.json"
DATA_JS = ROOT / "js" / "data.js"

BYTES_PER_SECOND = 48_000 / 8  # MP3 CBR 48 kbps, 24 kHz mono
CONCURRENCY = 4
RETRIES = 4

# Workaround (Oct 2026): speech.platform.bing.com answers 403 to synthesis.
# Edge 155 synthesizes through api.msedgeservices.com with the same token.
# See https://github.com/rany2/edge-tts/issues/490 — remove this once a fixed
# edge-tts release is out.
_communicate.WSS_URL = (
    "wss://api.msedgeservices.com/tts/cognitiveservices/websocket/v1"
    f"?Ocp-Apim-Subscription-Key={TRUSTED_CLIENT_TOKEN}"
)

SENTENCE_BREAK = re.compile(r"(?<=[.!?])\s+(?=[A-Z“\"])")


def split_sentences(text):
    return [s.strip() for s in SENTENCE_BREAK.split(text) if s.strip()]


def voice_settings(cfg):
    return {
        "voice": cfg["voice"],
        "rate": cfg.get("rate", "+0%"),
        "pitch": cfg.get("pitch", "+0Hz"),
    }


def chapter_units(book, chapter):
    """Paragraphs as lists of (sentence, voice settings)."""
    narrator = voice_settings(book["narrator"])
    characters = {k: voice_settings(v) for k, v in book.get("characters", {}).items()}
    paragraphs = []
    for paragraph in chapter["paragraphs"]:
        units = []
        for segment in paragraph:
            if isinstance(segment, str):
                cfg, text = narrator, segment
            else:
                ((name, text),) = segment.items()
                if name not in characters:
                    sys.exit(f"Unknown character {name!r} in {book['id']}: {chapter['title']}")
                cfg = characters[name]
            units.extend((sentence, cfg) for sentence in split_sentences(text))
        paragraphs.append(units)
    return paragraphs


async def synthesize(text, cfg, semaphore):
    async with semaphore:
        for attempt in range(1, RETRIES + 1):
            try:
                audio = bytearray()
                communicate = edge_tts.Communicate(text, cfg["voice"], rate=cfg["rate"], pitch=cfg["pitch"])
                async for chunk in communicate.stream():
                    if chunk["type"] == "audio":
                        audio += chunk["data"]
                if not audio:
                    raise RuntimeError("no audio received")
                return bytes(audio)
            except Exception as exc:  # network hiccups, throttling
                if attempt == RETRIES:
                    raise RuntimeError(f"Failed to synthesize {text!r}: {exc}") from exc
                await asyncio.sleep(2 * attempt)


async def build_chapter(book, number, chapter, cache, force, semaphore):
    key = f"{book['id']}/ch{number}"
    units = chapter_units(book, chapter)
    digest = hashlib.sha256(json.dumps(units, sort_keys=True).encode()).hexdigest()[:16]
    mp3 = ROOT / "audio" / book["id"] / f"ch{number}.mp3"

    cached = cache.get(key)
    if not force and cached and cached["hash"] == digest and mp3.exists():
        print(f"  = {key} (unchanged)")
        return cached

    flat = [unit for paragraph in units for unit in paragraph]
    clips = await asyncio.gather(*(synthesize(text, cfg, semaphore) for text, cfg in flat))

    audio = bytearray()
    clip_iter = iter(clips)
    paragraphs = []
    for paragraph in units:
        sentences = []
        for text, _ in paragraph:
            sentences.append({"text": text, "start": round(len(audio) / BYTES_PER_SECOND, 3)})
            audio += next(clip_iter)
        paragraphs.append(sentences)

    mp3.parent.mkdir(parents=True, exist_ok=True)
    mp3.write_bytes(audio)
    entry = {
        "hash": digest,
        "duration": round(len(audio) / BYTES_PER_SECOND, 3),
        "paragraphs": paragraphs,
    }
    cache[key] = entry
    CACHE.write_text(json.dumps(cache, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"  ✓ {key}: {len(flat)} sentences, {entry['duration']:.1f}s")
    return entry


def write_data_js(books, cache):
    out = []
    for book in books:
        chapters = []
        for number, chapter in enumerate(book["chapters"], start=1):
            entry = cache[f"{book['id']}/ch{number}"]
            chapters.append({
                "number": number,
                "title": chapter["title"],
                "image": f"images/{book['id']}/ch{number}.svg",
                "audio": f"audio/{book['id']}/ch{number}.mp3",
                "duration": entry["duration"],
                "paragraphs": entry["paragraphs"],
            })
        out.append({
            "id": book["id"],
            "title": book["title"],
            "theme": book["theme"],
            "summary": book["summary"],
            "cover": f"images/{book['id']}/cover.svg",
            "chapters": chapters,
        })
    DATA_JS.write_text(
        "// Generated by tools/generate_audio.py from content/stories.json. Do not edit by hand.\n"
        f"window.BOOKS = {json.dumps(out, indent=2, ensure_ascii=False)};\n",
        encoding="utf-8",
    )


async def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--force", action="store_true", help="regenerate audio even if the text did not change")
    parser.add_argument("--book", help="only (re)generate this book id")
    args = parser.parse_args()

    books = json.loads(STORIES.read_text(encoding="utf-8"))["books"]
    cache = json.loads(CACHE.read_text(encoding="utf-8")) if CACHE.exists() else {}
    semaphore = asyncio.Semaphore(CONCURRENCY)

    for book in books:
        if args.book and book["id"] != args.book:
            continue
        print(f"{book['title']}")
        for number, chapter in enumerate(book["chapters"], start=1):
            await build_chapter(book, number, chapter, cache, args.force, semaphore)

    missing = [f"{b['id']}/ch{n}" for b in books for n in range(1, len(b["chapters"]) + 1)
               if f"{b['id']}/ch{n}" not in cache]
    if missing:
        sys.exit(f"Missing audio for {', '.join(missing)}; run without --book to generate it.")
    write_data_js(books, cache)
    print(f"Wrote {DATA_JS.relative_to(ROOT)}")


if __name__ == "__main__":
    asyncio.run(main())
