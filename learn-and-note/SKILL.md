---
name: learn-and-note
description: Learn from a resource (YouTube video, article or web URL, PDF or local file, or the current conversation) and write a concise zettelkasten note in the notes vault, matching its conventions and wiring it into the graph. Add the `visual` flag (e.g. `/learn-and-note visual <url>`) to also build a visual HTML page, store it in the vault's Files/ folder and link it from the note. Use when the user invokes /learn-and-note, or says "learn this", "take notes on", "make a note from this video/article/file", with or without asking for a visual.
---

# Learn and Note

Turn one resource into a durable note in the notes vault. By default create **only the note**. Create a visual HTML page **only when the user opts in**.

## 1. Parse the request

- **Resource**: a URL (YouTube or web page), a local file path (md, pdf, txt, html, code), or "this"/"the above" meaning the current conversation.
- **Visual opt-in**: true when the arguments contain the flag `visual` (also accepted: `v`, `-v`, `--visual`) as a standalone word anywhere, e.g. `/learn-and-note visual <url>` or `/learn-and-note <url> visual`. Also true when the user asks in plain words for a visual, visualisation, diagram or HTML page. Strip the flag before treating the rest as the resource. Otherwise do not create one and do not offer one unprompted beyond a single closing line.
- **Overrides**: an explicit target folder or extra tags from the user win over defaults.

## 2. Resolve the vault

Vault root = explicit folder from the user, else `$NOTES_DIR`, else `$ZK_NOTEBOOK_DIR`. Stop and ask if none is set or the folder does not exist.

- Notes go in `<vault>/zettelkasten/`.
- Visual pages go in `<vault>/Files/`.

If the vault uses different folders, follow what is there rather than creating a new layout.

## 3. Ingest the resource

| Resource | How |
|----------|-----|
| YouTube URL | `python3 <skill_dir>/scripts/youtube_transcript.py "<url>"` prints title, channel, upload date, duration and a deduplicated transcript. Needs `yt-dlp`. If YouTube rate-limits the subtitle download (HTTP 429), it falls back to `youtube-transcript-api` via `uvx`. If both fail, say so and stop. |
| Web article | WebFetch the URL. Capture the title, author, publish date and the full argument. |
| PDF | Read with the `pages` parameter, in chunks for long files. |
| Local file | Read it. |
| Conversation | Use the decisions, findings and commands from the current session. |

Read the whole source before writing. Do not summarise from the title or the first chunk.

## 4. Learn the vault's conventions

Before drafting, read 2-3 recent notes in `zettelkasten/` on a similar topic, preferring other notes made from external resources. Match:
- filename style (kebab-case slug, usually naming the topic and author)
- frontmatter keys and order. The current vault uses `title`, `created` (`YYYY-MM-DDTHH:MM`), `tags` (inline list), `status: seedling`
- section shape: H1 title, source line, Thesis, topic sections, Takeaways, Related

Find related notes to link: grep `zettelkasten/` for the key concepts and pick the 2-5 closest notes plus the best-fitting MOC (`moc-*.md`).

## 5. Write the note

`<vault>/zettelkasten/<slug>.md`, following this shape unless nearby notes show a different one:

```markdown
---
title: <Title> (<Author>)
created: <YYYY-MM-DDTHH:MM>
tags: [<3-6 tags>]
status: seedling
---

# <Title> (<Author>)

<Kind>: [<Original title>](<url>) (<author/channel>, <YYYY-MM-DD>, <length if video>).

## Thesis
<2-3 sentences: the core argument.>

## <Topic sections>
<Bullets. Keep frameworks, numbers, examples, commands and caveats. Cut filler, self-promotion and repetition.>

## Takeaways
<3-5 bullets the reader can act on.>

## Related
- [[<related-note>]]
- [[<moc>]]
```

Writing rules:
- Concise and reference-friendly. Write it as a reference, not a transcript retelling, and leave out phrases like "in this video he says".
- Keep the source's own terms and frameworks, and quote short memorable lines when they carry meaning.
- Use a markdown table for comparisons and timelines.
- Do not invent facts that are not in the source. Mark any of your own interpretation as such.
- Use a plain dash "-", never an em dash.

Then add one line to the chosen MOC, next to related entries:
`- [[<slug>]] - <one-line hook>`

## 6. Visual page (opt-in only)

1. Load the `visual-explainer` skill if it is available, for design guidance. Otherwise follow the rules below directly.
2. Write a single self-contained HTML file to `<vault>/Files/<slug>.html` (same slug as the note). If a tool generates the page elsewhere, copy it into `Files/` and use that copy.
3. Page requirements:
   - A `<title>` of 2-4 words, plus a favicon as an inline SVG data URI.
   - Colour tokens on `:root`, a dark-mode override under `@media (prefers-color-scheme: dark)`, and an explicit `body` background.
   - Google Fonts only for external CSS, and no external JS unless a chart truly needs it (use cdnjs).
   - Works at phone width with a 16px side gutter and no horizontal scroll.
   - Show the source's structure visually: the core model as an inline SVG diagram, frameworks as cards or steps, comparisons as split bars or tables, then a bottom-line card. Don't just paste the note's text into a page.
   - A header with the source link and the note's path.
4. Link the visual from the note directly under the source line:
   `- Visual page: [Files/<slug>.html](../Files/<slug>.html)`
5. Mention the visual in the MOC hook ("..., with a visual page").
6. Open it: `open <vault>/Files/<slug>.html`.

## 7. Respond

- The paths to the note (and the visual, if made) and the MOC that was updated.
- 4-6 bullets with the key ideas.
- Any assumptions or gaps (e.g. auto-generated captions, a paywalled article).
- Do not commit. The vault has its own backup flow.
