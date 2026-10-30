---
name: book-file-naming
description: Clean up book and document file names (pdf, epub, chm) into short lowercase-hyphenated titles, either as a pure text transformation of a name the user pastes, or as a reviewed bulk rename of a library folder. Use when the user asks to rename a book or ebook file name, tidy downloaded ebook names, or normalize file names across a books folder.
---

# Book File Naming

Turn messy ebook names like
`Practical Widget Engineering Build and ship reliable widgets ... (Jane Doe, John Roe) (Some-Site).pdf`
into `practical-widget-engineering.pdf`.

## Two modes - pick the right one

1. **Text only.** The user pastes a file name and asks to "rename" it. Reply with the cleaned name only. Never search the disk or rename any file in this mode.
2. **Bulk rename.** The user names a folder and asks for a plan. Follow the workflow below. Never rename anything before the user approves the plan.

## Naming rules

1. Lowercase only.
2. Hyphen `-` between words. No spaces, underscores, `+`, dots, brackets or punctuation in the base name.
3. Concise and accurate: keep the **main title**, drop the subtitle.
   - The subtitle usually starts where the title ends without a colon, e.g. `Deep Focus A Practical Guide to...` -> `deep-focus`.
   - Keep words that are part of the real title, e.g. `the-art-of-clear-writing`, `a-short-guide-to-testing`, `data-pipelines-the-practical-parts`.
4. Strip all unnecessary details:
   - authors (`by X`, `(X, Y)`, `[X]`, `X - Title`)
   - download-site and source tags, e.g. `(Some-Site)`, `(site.example)`, `(site-a.example, site-b.example)`, `( SiteName )`, `@mirror.example`
   - publisher, series and exam tags: `[Publisher]`, `(Some Science Library)`, `(Early Access V06)`, `Exam AB-123`
   - version and copy suffixes: `_v7`, `v260615`, `(1)`, `(3)`, `_compact` only if there is no sibling it must be told apart from
   - double extensions: `.epub.pdf` -> `.pdf`, `.pptx.pdf` -> `.pdf`
5. Keep meaningful qualifiers in a normalized form:
   - edition: `-2nd-edition`, `-3rd-edition` (from `2nd ed`, `Second Edition`, `3rd`, `(2nd Edition)`)
   - volume: `-vol-1`, `-vol-2` (from `Volume II`, `Vol 2`)
   - anniversary or year editions when they identify the book: `-20th-anniversary-edition`, `-2024`
6. Normalize symbols: `&` -> `and`, `++` -> `plus`, `Node.js` -> `node-js`, curly apostrophes and `'` removed (`programmers`, `dont`, `cant`), fullwidth brackets `（）` become a hyphen-separated word.
7. Lowercase the extension. Never change the real file type.
8. CJK titles (Chinese, Japanese, Korean): keep the characters, drop author and source tags, lowercase any Latin letters, e.g. `示例书名（第二版） (某作者) (Some-Site).pdf` -> `示例书名-第二版.pdf`. For bilingual names keep the original-language title only.
9. If a name already satisfies all rules (lowercase, hyphenated, concise), leave it unchanged. A compliant but long name with a subtitle is NOT compliant: shorten it.

## Decisions that need judgment

- **Uninformative names** (`Bonus_Pdf.pdf`, `fileCDocuments20and....pdf`, `notes2.pdf`, `scan_2007.pdf`, DOI names like `j.example.2018.09.001.pdf`): read the real title with `pdfinfo` (Title) and `pdftotext -f 1 -l 3 file - | head`, then name it from the cover/title page. Examples: `Bonus_Pdf.pdf` -> `widget-patterns-bonus.pdf`, `fileCDocuments...pdf` -> `the-example-book.pdf`, `Lang-manual-v1.pdf` (one-page cheat sheet) -> `lang-cheat-sheet.pdf`.
- **Collisions in the same folder** (different files that would get the same name): add the shortest distinguishing suffix from the original name or content, e.g. `widget-guide-site-a.pdf` / `widget-guide-site-b.pdf`, `example-patterns-3rd-edition.pdf` / `-4th-edition.pdf` (confirm the edition from the front matter), `example-statistics-german.pdf`, `learning-example-tool-early-release.epub`. If two files are near-identical copies (same size, different checksum), use `-alt` and tell the user. Never delete duplicates unless asked.
- **Same title, different extension** (`x.epub` and `x.pdf`) is fine and needs no suffix.
- **Academic papers** in a numbered reading list (`1_Sparse_Widgets_Scale_Well_..._2401.00001.pdf`): keep the order number zero-padded so files sort (`01-`), drop the arXiv ID, and use the paper's short name (usually the part before the colon): `01-sparse-widgets.pdf`, `09-tree-search.pdf`, `11-self-critique.pdf`. Keep the full title only when there is no short name.
- **Course material** (slides, recaps, practice exercises): clean the name but keep what identifies the lesson, e.g. `PracticeExercises-CaseStatements.pdf` -> `practice-exercises-case-statements.pdf`, `Unit+Testing+Recap+.pdf` -> `unit-testing-recap.pdf`. Drop course codes like `12345_07_`.
- **CamelCase names** split into words: `PracticalNotesForEngineers` -> `practical-notes-for-engineers`.
- **Fix obvious typos** in the original name (`Pyhton` -> `python`, `managment` -> `management`, `embeddigns` -> `embeddings`).

## Bulk rename workflow

1. **Scope.** By default rename only `.pdf`, `.epub`, `.chm` (ask before including other types). Do not rename folders. Prune `node_modules`, `.git`, `target`. Check the size first: book folders often hide code projects with tens of thousands of files.
   ```bash
   find . \( -name node_modules -o -name .git -o -name target \) -prune -o -type f \( -iname "*.pdf" -o -iname "*.epub" -o -iname "*.chm" \) -print | sort > books.txt
   ```
2. **Plan.** Write the new names in a scratch file aligned with `books.txt` (`=` for unchanged). Build a `dir<TAB>old<TAB>new` TSV with a script that:
   - checks every new name matches `^[a-z0-9ぁ-ヿ一-鿿가-힯-]+\.(pdf|epub|chm)$` (kana, CJK ideographs and Hangul allowed)
   - checks the extension did not change
   - checks there are no collisions per folder (counting files that are kept unchanged)
   Spot-check alignment around skipped or unchanged lines.
3. **Review.** Show the user the full list grouped by folder (`old -> new`, long old names truncated), the list of unchanged files, and a short section of the judgment calls (uninformative names, collisions, duplicates, aliases). Wait for approval.
4. **Execute.** Use `mv -n` and write an undo log (`dir<TAB>new<TAB>old`) into the library root as a hidden file, e.g. `.rename-undo-YYYY-MM-DD.tsv`.
   - macOS is case-insensitive: case-only renames (`Example.pdf` -> `example.pdf`) look like "already exists". Rename them in two steps through a temporary name: `mv a .tmp-b && mv .tmp-b b`.
5. **Verify.** Confirm every planned new name exists (`ls dir | grep -Fx`, which is case-exact). Check that Finder aliases pointing at renamed books still resolve:
   ```bash
   osascript -e 'tell application "Finder" to get POSIX path of (original item of (POSIX file "/path/x alias" as alias) as alias)'
   ```
6. **Report.** Give counts (renamed, unchanged, skipped), any failures, and where the undo log is.

## Undo

```bash
cd <library root> && while IFS=$'\t' read -r d n o; do mv -n "$d/$n" "$d/$o"; done < .rename-undo-YYYY-MM-DD.tsv
```
