# Note Prompt Template

Use this as the base prompt when you want another agent to create a note from recent context.

```text
Turn `<SOURCE_CONTENT>` into a concise markdown note in the resolved target folder.

Folder rules:
- Prefer an explicit folder supplied in the request.
- Otherwise use the folder from `NOTES_DIR` (falling back to `ZK_NOTEBOOK_DIR`).
- Inspect nearby notes in that folder and follow the existing conventions for:
  - filename
  - frontmatter
  - metadata
  - timestamps
  - note structure

Constraints:
- required tags: `<REQUIRED_TAGS>`
- note goal: `<NOTE_GOAL>`
- audience/use: `<INTENDED_USE>`
- keep it concise, reference-friendly, and non-conversational
- infer local conventions from nearby notes instead of inventing new ones
- keep the durable information and remove filler, repetition, and transient chat phrasing

Preferred structure:
- title
- short summary
- key points
- examples / commands if relevant
- caveats / decisions if relevant

After creating the file, print only the final file path.
```

Recommended substitutions:
- `<SOURCE_CONTENT>`: the recent answers, findings, commands, or decisions that should be preserved
- `<REQUIRED_TAGS>`: one or more tags that must appear in the note
- `<NOTE_GOAL>`: reference note, dispute note, troubleshooting note, workflow note, decision note, and so on
- `<INTENDED_USE>`: future lookup, team handoff, personal recall, incident trail, runbook seed, and so on
