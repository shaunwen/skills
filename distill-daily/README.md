# distill-daily

An agent-agnostic skill (for Claude Code, Codex, or any agent that reads markdown skills) that turns raw captures in `DailyNotes/` of the notes vault into atomic zettelkasten notes, then writes a weekly or monthly review summary.

The vault root is resolved from (in order): an explicit folder in the invocation, the `NOTES_DIR` env var (falling back to `ZK_NOTEBOOK_DIR`), or the current working directory if it looks like the vault; otherwise the skill asks.

## Why

Capture is strong, extraction rarely happens: daily notes pile up with decisions, fixes, and commands buried in raw logs, and their `## Extracted` sections stay empty. This skill closes that loop.

## Usage

```
distill-daily                          # (or /distill-daily in Claude Code) default: past 7 days + weekly review
distill-daily weekly                   # same as default
distill-daily monthly                  # past 31 days (incl. weekly reviews) + monthly review
distill-daily 2026-07-01..2026-07-15   # explicit range (also "from X to Y" or a single date)
```

Range spans of 10 days or less get a weekly-style summary; longer spans get a monthly-style one.

## What it does

1. Gathers daily notes in the period, by filename date or frontmatter `created` (handles monthly-merge files that span a whole month).
2. Extracts distillable items: decisions, problem/solution pairs, reusable commands, insights, open questions.
3. Classifies each into a zk note type (`problem_solution`, `investigation`, `question_note`, `default`, `evergreen`).
4. Dedupes against the existing vault - updates existing notes instead of duplicating.
5. Proposes the extraction plan and waits for approval.
6. Writes seedling zettels in `zettelkasten/` following `.zk/templates/` conventions, and wires them into the relevant `moc-*` notes.
7. Fills each source daily note's `## Extracted` section with links - this makes reruns idempotent.
8. For a weekly run, merges the week's daily notes into the latest one and deletes the rest, repointing any backlinks.
9. Writes the summary note in `reviews/` (`YYYY-MM-DD-weekly-review.md` or `YYYY-MM-monthly-review.md`) and shows the summary paragraph inline.
10. Commits the result as `notes backup: YYYY-MM-DD-HH:MM`, with system/config changes in a separate scoped commit. Never pushes.

## Guarantees

- Never copies credentials or tokens into notes (placeholders only).
- Makes a backup commit before deleting any daily note that isn't committed yet, so nothing is lost if the merge goes wrong.
- Reruns skip anything already linked from an `## Extracted` section.
- Reminds you to run `zk index` (or `:ZkIndex` in Neovim) when done.

## Files

- `SKILL.md` - the skill instructions the agent follows.
- `README.md` - this file, for humans.
