# learn-and-note

An agent-agnostic skill (for Claude Code, Codex, or any agent that reads markdown skills) that turns one resource into a concise zettelkasten note in the notes vault, matching the vault's existing conventions and linking it into the graph. The vault root is resolved from (in order): an explicit folder in the invocation, the `NOTES_DIR` env var, or `ZK_NOTEBOOK_DIR`; otherwise the skill asks.

## Usage

```
learn-and-note <youtube-url | article-url | file-path | "this">
learn-and-note visual <resource>       # also build a visual HTML page
```

Use `this` (or "the above") to turn the current conversation into a note. The `visual` flag (also `v`, `-v`, `--visual`) can go anywhere in the arguments.

## What it does

1. Ingests the whole resource: YouTube transcripts via `scripts/youtube_transcript.py`, web articles, PDFs, local files, or the current conversation.
2. Reads 2-3 similar notes to match filename style, frontmatter and section shape, and finds related notes and the best-fitting `moc-*` note.
3. Writes `zettelkasten/<slug>.md`: source line, Thesis, topic sections, Takeaways, Related.
4. Adds a one-line entry to the chosen MOC.
5. With `visual`: writes a self-contained `Files/<slug>.html` page (light and dark mode, phone-friendly), links it from the note and opens it. Uses the `visual-explainer` skill for design guidance if it's installed.

## Prerequisites

- `python3` 3.7 or newer.
- For YouTube: [`yt-dlp`](https://github.com/yt-dlp/yt-dlp). If YouTube rate-limits subtitle downloads (HTTP 429), the script falls back to `youtube-transcript-api` through [`uvx`](https://docs.astral.sh/uv/) when it's available.

## Guarantees

- Creates only the note unless a visual page is asked for.
- Never invents facts that aren't in the source; marks its own interpretation as such.
- Never commits; run your usual notes backup afterwards.

## Files

- `SKILL.md` - the skill instructions the agent follows.
- `scripts/youtube_transcript.py` - prints a video's title, channel, upload date, duration and a deduplicated transcript.
- `README.md` - this file, for humans.
