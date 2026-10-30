# book-file-naming

An agent-agnostic skill (for Claude Code, Codex, or any agent that reads markdown skills) that turns messy ebook and document file names into short, lowercase, hyphenated titles, e.g. `Practical Widget Engineering Build and ship ... (Jane Doe) (Some-Site).pdf` -> `practical-widget-engineering.pdf`.

## Usage

```
book-file-naming <file name>          # text only: returns the cleaned name, touches nothing
book-file-naming <folder>             # bulk: plans renames for the whole folder, waits for approval
```

## What it does

- **Text mode:** applies the naming rules to a pasted name and replies with the result. It never searches the disk or renames anything.
- **Bulk mode:** lists every `.pdf`, `.epub` and `.chm` file under a folder, plans the new names, checks them (valid characters, unchanged extensions, no collisions in a folder), shows the full plan, and renames only after approval. It writes an undo log next to the library and checks that Finder aliases still resolve.

## Naming rules in short

- Lowercase, hyphen between words, main title only (subtitle dropped).
- Authors, download-site tags, publisher and series tags, and copy or version suffixes removed.
- Editions and volumes kept in a normal form: `-2nd-edition`, `-vol-2`.
- CJK titles (Chinese, Japanese, Korean) keep their characters.
- Unclear names (`Bonus_Pdf.pdf`, DOI names) are named from the PDF's title page.

## Prerequisites

- Bulk mode on unclear names uses `pdfinfo` and `pdftotext` (from poppler) to read title pages.
- The Finder alias check is macOS only.

## Files

- `SKILL.md` - the skill instructions the agent follows.
- `README.md` - this file, for humans.
