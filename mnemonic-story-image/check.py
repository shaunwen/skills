#!/usr/bin/env python3
"""
check.py - validate a mnemonic-story-image output bundle.

The skill produces a JSON bundle with: the target words, a vivid story, a
per-word placement table, and the final image-model prompt. This script
enforces the one requirement an LLM most easily fudges: EVERY target word must
(a) get its own visual placement, and (b) be spelled into the final image
prompt as literal text to render. If any word is missing, the image model will
silently drop it and the mnemonic fails.

Usage:
    python3 check.py bundle.json
    cat bundle.json | python3 check.py -

Exit code 0 = all words covered. Non-zero = something is missing (details on
stderr), so the agent knows to fix the bundle before showing the user.

Bundle schema (see examples/sat-5.json):
{
  "words": ["aberration", ...],
  "story": "one paragraph weaving in every word ...",
  "placements": [
    {"word": "aberration", "object": "tilted neon banner",
     "rendered_text": "ABERRATION", "where": "top of frame"}
  ],
  "image_prompt": "full prompt string that names every word as text to render"
}
"""
import json
import re
import sys


def norm(s: str) -> str:
    return re.sub(r"[^a-z0-9]", "", s.lower())


def load(path: str) -> dict:
    raw = sys.stdin.read() if path == "-" else open(path, encoding="utf-8").read()
    return json.loads(raw)


def check(bundle: dict) -> list[str]:
    errors: list[str] = []
    words = bundle.get("words") or []
    if not words:
        return ["bundle has no 'words'"]

    story = bundle.get("story", "")
    prompt = bundle.get("image_prompt", "")
    placements = bundle.get("placements") or []

    if len(norm(story)) < 60:
        errors.append("story is too short to be a real mnemonic (need a vivid paragraph)")

    placed = {norm(p.get("word", "")): p for p in placements}
    nprompt = norm(prompt)

    for w in words:
        nw = norm(w)
        # 1. every word needs a placement entry
        p = placed.get(nw)
        if p is None:
            errors.append(f"word '{w}': no placement entry")
            continue
        # 2. the rendered_text label must actually contain the word
        if nw not in norm(p.get("rendered_text", "")):
            errors.append(
                f"word '{w}': rendered_text '{p.get('rendered_text')}' does not contain the word"
            )
        # 3. the placement must say WHERE and on WHAT
        if not p.get("object") or not p.get("where"):
            errors.append(f"word '{w}': placement missing 'object' or 'where'")
        # 4. the final image prompt must name the word as literal text
        if nw not in nprompt:
            errors.append(f"word '{w}': not spelled into image_prompt (image model will drop it)")
        # 5. the story should use the word too (that's the memory hook)
        if nw not in norm(story):
            errors.append(f"word '{w}': not used in the story")

    # the prompt must instruct the model to render text legibly & exactly
    if not re.search(r"\b(text|letter|word|label|spell|typograph)", prompt, re.I):
        errors.append("image_prompt never tells the model to render TEXT - words won't appear")

    return errors


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    bundle = load(sys.argv[1])
    errors = check(bundle)
    n = len(bundle.get("words") or [])
    if errors:
        print(f"FAIL: {len(errors)} problem(s) across {n} word(s):", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 1
    print(f"OK: all {n} words placed, spelled into the prompt, and used in the story.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
