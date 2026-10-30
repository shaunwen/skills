---
name: mnemonic-story-image
description: Turn a list of words into one vivid, funny, exaggerated mnemonic story that helps you memorize them, then convert that story into an image-model prompt that renders each word as legible text embedded in the scene. Use when asked to memorize vocabulary, make a mnemonic story, create a memory image, study SAT/English words, remember a word list, or generate an image prompt that spells out words in place.
---

# Mnemonic Story + Image Prompt

Given a list of words, produce two things:

1. **One short story** that weaves in *every* word - vivid, funny, exaggerated,
   color-soaked, emotionally charged. Exaggeration and emotion are what make it
   stick.
2. **An image-model prompt** that turns the story into a single scene and tells
   the image model to render *each target word as legible text* on/near the
   object that represents it ("embed the words properly in place").

This is a **prompt-only** skill - it does not call any image API. It emits a
copy-paste prompt you paste into any image model (gpt-image-1, Midjourney,
Imagen, etc.). The deliverable is validated by a script so no word is silently
dropped.

`<skill_dir>` below is this skill's own folder (wherever it is installed).

## Run (agent path)

1. **Build the bundle.** Produce a JSON bundle (schema below) in your head and
   write it to a temp file, e.g. `/tmp/bundle.json`. Use
   [examples/sat-5.json](examples/sat-5.json) as the exact shape to copy.

2. **Validate it** - this is mandatory, it's what guarantees every word lands:

   ```bash
   python3 <skill_dir>/check.py /tmp/bundle.json
   ```

   Exit 0 = every word is placed, spelled into the prompt, and used in the
   story. Non-zero = fix the listed problems and re-run before showing the user.

3. **Show the user** the story and the `image_prompt`. Mention they paste the
   prompt into any image model.

### Bundle schema

```json
{
  "words": ["aberration", "..."],
  "story": "one paragraph weaving in EVERY word, vivid and exaggerated",
  "placements": [
    {"word": "aberration",
     "object": "tilted neon banner above the party",
     "rendered_text": "ABERRATION",
     "where": "top of frame, hot-pink glowing letters"}
  ],
  "image_prompt": "full scene description that names every word as literal text to render, plus a 'render every word as large legible correctly-spelled text' instruction and a vivid style line"
}
```

## How to write a story that sticks

For each word, pick a memory hook before writing prose:

- **Sound-alike / sub-word** - "obfuscate" → an *octopus* that *fogs* things.
- **Meaning as action** - "ephemeral" (short-lived) → a bubble that pops after
  one second.
- **Exaggerate** - never "loud," always "200 kazoos shook the cake."
- **Color** - give each element a saturated, named color; color anchors memory.
- **Emotion** - joy, heartbreak, absurdity. A boring image is forgotten.

Then chain all the hooks into **one** absurd scene (a party, a heist, a
zoo-gone-wrong) so the words recall each other in order.

## How to write the image prompt

- Describe **one coherent scene**, not a list of disconnected words.
- For each word, name the **object** it lives on and the **exact text** to
  render and **where** in the frame (mirror the `placements` table).
- End with an explicit instruction: *"Render every word as large, legible,
  correctly-spelled text exactly as given, integrated naturally into each
  object."* Image models drop or misspell text without this.
- Add a **style line**: vivid/exaggerated cartoon, hyper-saturated colors,
  thick outlines, dramatic emotion. This matches the mnemonic's energy.

## Verified example

[examples/sat-5.json](examples/sat-5.json) - 5 SAT words
(aberration, cacophony, ephemeral, gregarious, obfuscate) woven into one
loudest-birthday-party scene. Passes `check.py`. Run:

```bash
python3 <skill_dir>/check.py <skill_dir>/examples/sat-5.json
# -> OK: all 5 words placed, spelled into the prompt, and used in the story.
```

## Gotchas

- **Image models silently drop text.** A word in your scene description is not
  the same as a word the model is *told to render as text*. The `check.py` rule
  that the prompt must contain a `text`/`spell`/`label` instruction guards this.
- **More than ~6-8 words per image gets crowded** and the model garbles the
  text. For long lists, split into batches of 5-6 and make one scene per batch.
- **Embedded text must be the word itself**, not a synonym. `check.py` fails a
  placement whose `rendered_text` doesn't contain the actual word - so a
  rendered "LOUD" for the word "cacophony" is caught.
- **The story is the index, the image is the recall cue.** Both must contain
  every word; `check.py` enforces both, which is why a word present in the
  prompt but missing from the story still fails.

## Troubleshooting

- `FAIL: word 'X': no placement entry` - you forgot to give word X an object in
  the scene. Add a `placements` row for it.
- `FAIL: word 'X': not spelled into image_prompt` - X is in your story/placements
  but you never wrote it into the prompt string the model reads. Add it.
- `FAIL: image_prompt never tells the model to render TEXT` - add the explicit
  "render every word as legible text" instruction.
- `python3: command not found` - install Python 3.9 or newer, or call it by its
  full path. The script uses only the standard library.
