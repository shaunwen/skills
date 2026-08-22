---
name: notes-system-review
description: Audit the notes vault health (structure, links, orphans, MOC coverage, staleness, templates, duplicates, secrets) and propose improvements as a plan for the user to review before any changes are made. Use when the user invokes /notes-system-review or asks to review, audit, or improve their notes system.
---

# Notes System Review

Audit the notes vault and propose actions. **Read-only until the user approves a plan** - never modify, move, or delete anything during the audit.

## Vault root resolution

Resolve the vault root in this order:

1. An explicit folder named by the user in the invocation.
2. The `NOTES_DIR` environment variable, falling back to `ZK_NOTEBOOK_DIR` if unset (`echo "${NOTES_DIR:-$ZK_NOTEBOOK_DIR}"`).
3. If the current working directory looks like the vault (contains `.zk/` and `zettelkasten/`), use it.
4. Otherwise stop and ask the user for the vault path.

Validate the folder exists before proceeding.

## Step 1 - Audit

Delegate broad scanning to an Explore agent where useful. Cover:

1. **Structure**: folders, note counts per folder, stray root files, empty folders, single-file folders. Flag overlap (same topic living in multiple folders) against the intended layout: `zettelkasten/` (atomic notes + `moc-*`), `DailyNotes/` (daily captures, monthly-merged), `work/` (dated work logs), `reviews/` (weekly/monthly reviews), `design/`, `Personal/`, `Resources/`, `Files/`.
2. **Graph health**: share of zettel notes with outgoing `[[wikilinks]]`; true orphans (no inbound links); MOCs with zero outgoing links; whether `moc-home.md` lists all MOCs. Use `zk list --format ...`, or Grep.
3. **Dead links**: unresolved `[[targets]]`. IMPORTANT vault convention: dangling links are often intentional placeholders for unwritten notes. Only flag spelling-drift near-misses (a very similar filename exists) and false positives (code in unfenced blocks - verify fencing with an awk fence-state check before flagging; links inside fenced blocks or backticks are fine).
4. **Frontmatter and conventions**: notes missing frontmatter/tags; off-vocabulary `status:` values (valid: seedling, budding, evergreen); non-kebab-case filenames; empty `tags:` lines.
5. **Pipeline health**: status distribution (is promotion seedling->budding->evergreen happening?); daily notes with empty `## Extracted` sections (suggest `/distill-daily`); unchecked `- [ ]` accumulation and its age.
6. **Staleness**: mtime distribution per folder (git history is squashed, use mtime); dead folders.
7. **Hygiene**: near-empty stubs (<200 bytes); duplicate-topic pairs; large binaries committed; templates in `.zk/templates/` that no note actually uses; uncommitted changes and backup cadence (`git log --format=%ad --date=short | uniq -c`).
8. **Secrets**: Grep for tokens/passwords/api keys in notes (`token|secret|password|api[_-]?key|BEGIN.*PRIVATE`). Treat any hit as a top-priority finding; recommend revocation plus in-place redaction to an obvious example placeholder, and note that git history retains the original.

## Step 2 - Report findings

Present a concise findings summary: what's healthy first, then issues grouped by theme, each with concrete file paths and counts. No file dumps.

## Step 3 - Propose a plan and wait for approval

Produce a numbered action plan, ordered by value/effort. For each item: what will change, which files, and whether it's mechanical (safe) or judgment/destructive (moves, deletes, merges). Ask the user which items to execute (AskUserQuestion or plain text) and **do nothing until they approve**.

## Step 4 - Execute approved items only

Apply exactly the approved items. Rules:
- Verify a suspected problem before "fixing" it (e.g. confirm code blocks really are unfenced before adding fences).
- Preserve the intentional-placeholder link convention.
- When migrating notes into `zettelkasten/`: kebab-case slug, frontmatter with `created` (from mtime), `status: seedling`, a source tag; merge tags into existing frontmatter rather than duplicating it.
- Use `git mv`/`git rm` so history follows; stage but do not commit unless asked.
- Audit the result (e.g. every migrated file has its tag) and report what was done, what was skipped, and remind the user to run `zk index`.
