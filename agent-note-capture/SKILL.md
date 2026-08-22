---
name: agent-note-capture
description: Capture durable markdown notes from active AI-agent work into a user-configured notes folder. Use when Codex or another agent should turn recent conversation, findings, commands, decisions, or troubleshooting into a concise note that matches local folder conventions, especially when the destination folder comes from an env var and the agent must infer filename, frontmatter, metadata, timestamp, and structure patterns from nearby notes.
---

# Agent Note Capture

## Overview

Create concise markdown notes from recent agent context without inventing a new note style. Resolve the destination folder from an env var or explicit override, inspect nearby notes to infer the local pattern, then write a compact reference note and return the final path when the user only wants file creation.

## Quick Start

1. Resolve the target folder.
   - Prefer an explicit user-supplied folder when present.
   - Otherwise use `NOTES_DIR` (falling back to `ZK_NOTEBOOK_DIR`).
   - Run `python scripts/resolve_target_folder.py` to confirm the effective folder.
2. Inspect nearby notes before drafting.
   - Run `python scripts/inspect_note_patterns.py "$TARGET_FOLDER"` for a compact summary.
   - If the summary is insufficient, manually inspect 2-4 nearby notes in the same folder.
3. Condense the source material.
   - Keep decisions, commands, examples, and caveats.
   - Remove filler, repetition, and chatty wording.
4. Create the note.
   - Match the folder's existing filename style, frontmatter keys, metadata shape, timestamp format, and section structure.
   - Add required tags from the request, plus a small number of inferred tags if they fit the local pattern.
5. Respond appropriately.
   - If the user asked only for note creation, print only the final file path.
   - Otherwise summarize what was created and call out any assumptions.

## Folder Resolution

- Default env var: `NOTES_DIR` (falling back to `ZK_NOTEBOOK_DIR`)
- Override rule: if the user explicitly names a folder, use that instead of the env var.
- Failure rule: if neither an explicit folder nor `NOTES_DIR` (falling back to `ZK_NOTEBOOK_DIR`) is available, stop and ask for one.
- Validate that the folder exists before writing. Do not create a new note system layout unless the user asked for that.

Use the resolver script:

```bash
python scripts/resolve_target_folder.py
python scripts/resolve_target_folder.py --target-folder ~/notes/zettelkasten
python scripts/resolve_target_folder.py --env-var MY_AGENT_NOTES_DIR
```

## Convention Inference

Infer the local note pattern from the destination folder instead of copying a generic template.

Check for:
- filename slug style
- frontmatter presence and key order
- timestamp field names and formats
- common tags shape
- title conventions
- recurring sections such as summary, key points, commands, caveats, or links

Use the inspector first:

```bash
python scripts/inspect_note_patterns.py "$TARGET_FOLDER"
```

If the folder contains mixed note types, bias toward the notes that are closest in topic and location to the requested note.

## Writing Rules

- Keep the note concise, reference-friendly, and non-conversational.
- Prefer durable wording over chat transcript phrasing.
- Preserve important commands exactly.
- Avoid copying long raw conversation blocks unless the user explicitly wants archival notes.
- Do not invent metadata fields that do not exist in the folder pattern.
- Do not broaden the note scope beyond the supplied source material.

## Default Prompt Template

Use the template in `references/note-prompt-template.md` as the base prompt when you need to create or refine a note-generation request for another agent.

## Minimal Workflow

```text
Turn source material into a concise markdown note in the resolved target folder.
Infer local conventions from nearby notes.
Keep only the durable information.
Create the file.
Return the final path.
```
