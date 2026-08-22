# agent-note-capture

An agent-agnostic skill (for Claude Code, Codex, or any agent that reads markdown skills) that captures durable markdown notes from active agent work into a configured notes folder, matching the folder's existing conventions instead of inventing a new note style.

## Target folder resolution

In order: an explicit user-supplied folder, the `NOTES_DIR` env var, then `ZK_NOTEBOOK_DIR` as fallback. If none is available the skill stops and asks. Confirm with:

```bash
python scripts/resolve_target_folder.py
```

## What it does

1. Resolves the target folder (above).
2. Infers local conventions from nearby notes (`python scripts/inspect_note_patterns.py "$TARGET_FOLDER"`): filename style, frontmatter keys, timestamp format, tags shape, section structure.
3. Condenses the source material - keeps decisions, commands, examples, caveats; drops filler and chat phrasing.
4. Writes a concise reference note matching the folder pattern.
5. Returns the final file path (only the path when that's all that was asked).

## Files

- `SKILL.md` - the skill instructions the agent follows.
- `scripts/` - folder resolution and note-pattern inspection helpers.
- `references/` - the note-generation prompt template.
- `README.md` - this file, for humans.
