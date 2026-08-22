---
name: distill-daily
description: Distill captured daily notes from the notes vault into atomic zettelkasten notes, fill each daily note's Extracted section, and produce a weekly or monthly summary review note. Use when the user invokes /distill-daily, or asks to distill/extract daily notes, run a weekly or monthly review, or turn a date range of daily notes into proper notes.
---

# Distill Daily Notes

Turn raw captures in `DailyNotes/` into atomic zettelkasten notes wired into the graph, then write a period summary.

## Vault root resolution

All paths below are relative to the vault root. Resolve it in this order:

1. An explicit folder named by the user in the invocation.
2. The `NOTES_DIR` environment variable, falling back to `ZK_NOTEBOOK_DIR` if unset (`echo "${NOTES_DIR:-$ZK_NOTEBOOK_DIR}"`).
3. If the current working directory looks like the vault (contains `.zk/` and `DailyNotes/`), use it.
4. Otherwise stop and ask the user for the vault path. Do not guess or create a layout.

Validate the resolved folder exists and contains `DailyNotes/` and `zettelkasten/` before proceeding.

## Arguments

Parse the invocation argument:

- `weekly` (default when no argument): period = the past 7 days ending today.
- `monthly`: period = the past calendar month-ish window (past 31 days ending today). Also include any weekly review notes in `reviews/` inside the period as source material.
- A date range: accept `YYYY-MM-DD..YYYY-MM-DD`, `from YYYY-MM-DD to YYYY-MM-DD`, or a single `YYYY-MM-DD` (that day only). Range mode produces a period summary too, typed by span: <=10 days -> weekly-style, otherwise monthly-style.

## Step 1 - Gather source notes

A daily note belongs to the period if either its filename date (`DailyNotes/YYYY-MM-DD.md`) or its frontmatter `created` date falls in range. Caveat: some files are monthly merges (title like `# 2026-08` with entries spanning the month) - include a monthly-merge file if its month overlaps the period, and only distill the entries that fall inside the period when entries are dated.

```bash
ls DailyNotes/           # filename dates
```

For `monthly`, also gather `reviews/*-weekly-review.md` in range.

Skip material already extracted: if an item is already linked from the note's `## Extracted` section, do not re-extract it (this makes reruns idempotent).

## Step 2 - Extract candidates

Read the gathered notes and identify distillable items:

- decisions made (and why)
- problem -> solution pairs (bugs fixed, root causes)
- reusable commands, queries, configuration
- insights, patterns, gotchas worth keeping
- open questions worth a `question_note`

Classify each candidate into a zk note type from `.zk/templates/`: `problem_solution`, `investigation`, `question_note`, `default` (fact/insight), `evergreen` (rare - only mature ideas). Ignore ephemeral chatter, completed-task noise with no durable lesson, and pure status updates.

## Step 3 - Dedupe against the vault

For every candidate, search before creating:

```bash
zk list --quiet --match "<keywords>"   # or Grep the zettelkasten/ folder
```

If a note on the topic exists, plan an **update** (append/merge into it) instead of a new note.

## Step 4 - Propose, then get approval

Present the extraction plan as a compact list: `[new|update] <slug> (<type>) - one-line summary - source: <daily note>`. Ask the user to approve/trim it (AskUserQuestion or plain text). Only proceed on approval. If the user asked to run non-interactively, proceed directly but say so.

## Step 5 - Write the zettels

For each approved item create `zettelkasten/<kebab-slug>.md` following the matching `.zk/templates/` template's structure, with frontmatter:

```yaml
---
title: <Title>
created: <now, YYYY-MM-DDTHH:MM>
tags: [<topic tags, e.g. payments, tech, devtools>]
status: seedling
---
```

Rules:
- kebab-case slug filenames, matching existing vault style.
- Concise, reference-friendly, non-conversational wording; preserve commands/SQL exactly.
- End each note with `## Related` linking relevant notes and the most relevant `moc-*` note (list MOCs with `ls zettelkasten/moc-*.md`).
- Add each new note to the relevant MOC's section as `- [[slug]] - one-liner`.
- Never include credentials/tokens - replace with placeholder values.

## Step 6 - Close the loop in the daily notes

In each source daily note, fill (or create) the `## Extracted` section with links to the notes created/updated from it:

```markdown
## Extracted
- [[slug-one]] - what was extracted
```

## Step 7 - Write the period summary

**Weekly** (`weekly` or short range): create `reviews/YYYY-MM-DD-weekly-review.md` (date = period end) using `.zk/templates/weekly_review.md` structure and frontmatter (`type: weekly_review`, `status: seedling`, `domain: meta`, `tags: [review]`). Fill the sections from what the period actually contained: problems solved (link the zettels), question triage, notes deserving distillation/evergreen promotion, repeated patterns, system improvements. Prepend a short `## Week in summary` paragraph: 3-6 sentences on what the week was about.

**Monthly** (`monthly` or long range): create `reviews/YYYY-MM-monthly-review.md` with the same frontmatter shape but `type: monthly_review` and `tags: [review, monthly]`. Sections:

```markdown
# Monthly review - YYYY-MM

## Month in summary
<one paragraph: main themes, biggest wins, biggest problems>

## Highlights
- ...

## Problems solved
- [[...]]

## Notes created/updated this month
- [[...]]

## Promotion candidates (seedling -> budding -> evergreen)
- [ ] [[...]]

## Carry-over / open threads
- ...
```

## Step 8 - Report

Remind the user to run `zk index` (or `:ZkIndex` in Neovim). Report: notes created (with paths), notes updated, MOCs touched, daily notes whose Extracted sections were filled, and the summary note path. End with the period summary paragraph inline so the user reads it without opening the file. Do not commit unless asked.
