#!/usr/bin/env python3

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from urllib.parse import parse_qs, urlparse

TIMING_LINE = re.compile(r"^\d{2}:\d{2}[:.\d]* --> ")
INLINE_TAG = re.compile(r"<[^>]+>")
HEADER_PREFIXES = ("WEBVTT", "Kind:", "Language:")
METADATA_TEMPLATE = "TITLE: %(title)s\nCHANNEL: %(channel)s\nUPLOADED: %(upload_date)s\nDURATION: %(duration_string)s"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Print YouTube metadata and a deduplicated plain-text transcript."
    )
    parser.add_argument("url")
    parser.add_argument("--lang", default="en", help="Subtitle language code (default: en)")
    return parser.parse_args()


def video_id(url: str) -> str:
    parsed = urlparse(url)
    if parsed.hostname and parsed.hostname.endswith("youtu.be"):
        return parsed.path.lstrip("/")
    return parse_qs(parsed.query).get("v", [url])[0]


def vtt_to_text(vtt: str) -> str:
    seen = set()
    lines = []
    for raw in vtt.splitlines():
        line = INLINE_TAG.sub("", raw).strip()
        if not line or line.startswith(HEADER_PREFIXES) or TIMING_LINE.match(line):
            continue
        if line in seen:
            continue
        seen.add(line)
        lines.append(line)
    return " ".join(lines)


def fetch_metadata(url: str) -> str:
    result = subprocess.run(
        ["yt-dlp", "--skip-download", "--print", METADATA_TEMPLATE, url],
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def transcript_via_ytdlp(url: str, lang: str) -> str | None:
    with tempfile.TemporaryDirectory() as tmp:
        subprocess.run(
            [
                "yt-dlp", "--skip-download",
                "--write-subs", "--write-auto-subs",
                "--sub-langs", lang, "--sub-format", "vtt",
                "-o", str(Path(tmp) / "video"),
                url,
            ],
            capture_output=True,
            text=True,
        )
        subtitles = sorted(Path(tmp).glob("*.vtt"), key=lambda p: p.stat().st_size)
        return vtt_to_text(subtitles[0].read_text()) if subtitles else None


def transcript_via_transcript_api(url: str, lang: str) -> str | None:
    # yt-dlp's subtitle endpoint is often rate-limited (HTTP 429); this API uses a different one.
    if not shutil.which("uvx"):
        return None
    result = subprocess.run(
        [
            "uvx", "--from", "youtube-transcript-api", "youtube_transcript_api",
            video_id(url), "--languages", lang, "--format", "text",
        ],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0 or not result.stdout.strip():
        return None
    return " ".join(result.stdout.split())


def main() -> int:
    args = parse_args()
    if not shutil.which("yt-dlp"):
        print("yt-dlp is not installed.", file=sys.stderr)
        return 1
    transcript = transcript_via_ytdlp(args.url, args.lang) or transcript_via_transcript_api(args.url, args.lang)
    if not transcript:
        print("No transcript available (no subtitles, or YouTube is rate-limiting).", file=sys.stderr)
        return 1
    print(fetch_metadata(args.url))
    print()
    print(transcript)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
