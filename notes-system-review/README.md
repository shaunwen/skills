# notes-system-review

An agent-agnostic skill (for Claude Code, Codex, or any agent that reads markdown skills) that audits the notes vault and proposes improvements. The vault root is resolved from (in order): an explicit folder in the invocation, the `NOTES_DIR` env var (falling back to `ZK_NOTEBOOK_DIR`), or the current working directory if it looks like the vault; otherwise the skill asks. It is plan-first: the audit is read-only, findings and a numbered action plan are presented for review, and nothing is changed until specific items are approved. It assumes a zk + Obsidian vault layout (zettelkasten/ with moc-* notes, DailyNotes/, work/, reviews/, seedling/budding/evergreen statuses) - adjust folder names to your own vault.

## Usage

```
notes-system-review
```

## What it checks

- Folder structure, overlaps, stray files, empty/single-file folders
- Graph health: outgoing-link coverage, orphans, MOC completeness
- Dead links (respecting the vault's intentional-placeholder convention; verifies code fencing before flagging false positives)
- Frontmatter/convention drift: missing tags, off-vocabulary status values, non-kebab-case filenames
- Pipeline health: seedling->evergreen promotion, empty `## Extracted` sections, stale TODO accumulation
- Staleness per folder (mtime-based) and backup cadence
- Hygiene: stubs, duplicate topics, committed binaries, unused templates
- Secrets: token/password/key scanning (top-priority findings)

## Flow

1. **Audit** (read-only, may delegate scanning to a subagent)
2. **Report** findings - healthy parts first, then issues with paths and counts
3. **Plan** - numbered actions ordered by value/effort, marked safe vs destructive; waits for approval
4. **Execute** only approved items, verify results, remind to run `zk index`; stages but never commits unless asked

## Companion skill

`distill-daily` handles the extraction pipeline this review often recommends (daily notes -> zettels + weekly/monthly summaries).

## Files

- `SKILL.md` - the skill instructions the agent follows.
- `README.md` - this file, for humans.
