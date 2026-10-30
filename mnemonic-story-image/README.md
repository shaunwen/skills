# mnemonic-story-image

An agent-agnostic skill (for Claude Code, Codex, or any agent that reads markdown skills) that turns a list of words into one vivid, funny, exaggerated mnemonic story, then into an image-model prompt that renders each word as legible text on the object that represents it.

## Usage

```
mnemonic-story-image aberration cacophony ephemeral gregarious obfuscate
```

Paste the resulting prompt into any image model (gpt-image-1, Midjourney, Imagen, ...). The skill itself never calls an image API.

## What it does

1. Picks a memory hook per word (sound-alike, meaning as action, exaggeration, color, emotion) and chains them into one absurd scene.
2. Builds a JSON bundle: the words, the story, a placement per word (object, exact text, where in the frame) and the image prompt.
3. Validates the bundle with `check.py`, which fails if any word is missing a placement, isn't spelled into the prompt, isn't used in the story, or if the prompt never tells the model to render text.
4. Shows the story and the prompt.

For long lists it splits the words into batches of 5-6, one scene per batch, because image models garble crowded text.

## Prerequisites

- `python3` 3.9 or newer, for `check.py` (standard library only).

## Files

- `SKILL.md` - the skill instructions the agent follows.
- `check.py` - validates a bundle; exit 0 means every word is covered.
- `examples/sat-5.json` - a verified bundle for five SAT words.
- `README.md` - this file, for humans.
