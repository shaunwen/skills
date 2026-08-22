#!/usr/bin/env python3

import argparse
import json
import re
from collections import Counter
from pathlib import Path


FRONTMATTER_RE = re.compile(r"\A---\n(.*?)\n---\n?", re.DOTALL)
FRONTMATTER_KEY_RE = re.compile(r"^([A-Za-z0-9_-]+):", re.MULTILINE)
HEADING_RE = re.compile(r"^#\s+(.+)$", re.MULTILINE)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Inspect a notes folder and summarize local markdown note conventions."
    )
    parser.add_argument("folder", help="Notes folder to inspect.")
    parser.add_argument(
        "--limit",
        type=int,
        default=8,
        help="How many recent markdown files to sample.",
    )
    return parser.parse_args()


def list_recent_notes(folder: Path, limit: int) -> list[Path]:
    notes = [path for path in folder.glob("*.md") if path.is_file()]
    notes.sort(key=lambda path: path.stat().st_mtime, reverse=True)
    return notes[:limit]


def infer_tag_style(frontmatter: str) -> str | None:
    for line in frontmatter.splitlines():
        if not line.startswith("tags:"):
            continue
        stripped = line.strip()
        if stripped.endswith("]"):
            return "inline-list"
        value = stripped.partition(":")[2].strip()
        if value:
            return "scalar"
        return "block-list"
    return None


def inspect_note(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    frontmatter_match = FRONTMATTER_RE.match(text)
    frontmatter = frontmatter_match.group(1) if frontmatter_match else ""
    heading_match = HEADING_RE.search(text)

    timestamp_examples = {}
    for key in ("created", "updated", "date"):
        match = re.search(rf"^{key}:\s*(.+)$", frontmatter, re.MULTILINE)
        if match:
            timestamp_examples[key] = match.group(1).strip()

    return {
        "filename": path.name,
        "frontmatter_keys": FRONTMATTER_KEY_RE.findall(frontmatter),
        "tag_style": infer_tag_style(frontmatter),
        "timestamps": timestamp_examples,
        "heading": heading_match.group(1).strip() if heading_match else None,
    }


def main() -> int:
    args = parse_args()
    folder = Path(args.folder).expanduser().resolve()
    notes = list_recent_notes(folder, args.limit)

    if not folder.exists() or not folder.is_dir():
        raise SystemExit(f"Not a directory: {folder}")
    if not notes:
        raise SystemExit(f"No markdown notes found in: {folder}")

    inspected = [inspect_note(path) for path in notes]

    key_orders = Counter(tuple(item["frontmatter_keys"]) for item in inspected if item["frontmatter_keys"])
    key_counts = Counter(
        key for item in inspected for key in item["frontmatter_keys"]
    )
    tag_styles = Counter(item["tag_style"] for item in inspected if item["tag_style"])

    payload = {
        "folder": str(folder),
        "sample_size": len(inspected),
        "filename_examples": [item["filename"] for item in inspected[:5]],
        "common_frontmatter_key_orders": [
            {"keys": list(keys), "count": count}
            for keys, count in key_orders.most_common(3)
        ],
        "common_frontmatter_keys": [
            {"key": key, "count": count}
            for key, count in key_counts.most_common()
        ],
        "tag_styles": [
            {"style": style, "count": count}
            for style, count in tag_styles.most_common()
        ],
        "timestamp_examples": [
            {
                "filename": item["filename"],
                "timestamps": item["timestamps"],
            }
            for item in inspected
            if item["timestamps"]
        ][:5],
        "heading_examples": [
            {"filename": item["filename"], "heading": item["heading"]}
            for item in inspected
            if item["heading"]
        ][:5],
    }

    print(json.dumps(payload, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
