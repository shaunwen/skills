# Skills

AI agent skills, packaged for compatibility with the `skills` CLI and `skills.sh` ecosystem.

## Installation

### Option 1: Install from local repository

```bash
npx skills add . --list
npx skills add . --skill sonarqube-new-code-warning-fixer -y
```

### Option 2: Install from GitHub (after publishing)

```bash
npx skills add https://github.com/shaunwen/skills --skill sonarqube-new-code-warning-fixer
```

## Available Skills

| Skill | Description |
|-------|-------------|
| [agent-note-capture](agent-note-capture/SKILL.md) | Capture durable markdown notes from active agent work into a configured notes folder, matching local conventions. |
| [book-file-naming](book-file-naming/SKILL.md) | Clean up ebook and document file names into short lowercase-hyphenated titles, as a text-only rename or a reviewed bulk rename of a library folder. |
| [distill-daily](distill-daily/SKILL.md) | Distill captured daily notes into atomic zettelkasten notes, merge a week's daily notes, produce weekly/monthly review summaries, and make a backup commit. |
| [learn-and-note](learn-and-note/SKILL.md) | Turn a YouTube video, article, PDF, local file or the current conversation into a zettelkasten note matching the vault's conventions, with an optional visual HTML page. |
| [notes-system-review](notes-system-review/SKILL.md) | Audit a notes vault (structure, links, staleness, secrets) and propose a plan-first set of improvements. |
| [sonarqube-new-code-warning-fixer](sonarqube-new-code-warning-fixer/SKILL.md) | Analyze newly updated code with SonarQube MCP, list warnings, fix all warnings, and fix broken tests. |

The notes skills resolve their target notes folder from the `NOTES_DIR` env var (falling back to `ZK_NOTEBOOK_DIR`) and assume a zk/Obsidian-style markdown vault.

## Skill Prerequisites

For `sonarqube-new-code-warning-fixer`, ensure:

1. SonarQube MCP server for SonarQube Server is configured for your AI agent environment.
2. A relatively recent `python3` is installed and available on `PATH`.

Reference setup example:
- SonarQube MCP quickstart (Codex CLI example): https://docs.sonarsource.com/sonarqube-mcp-server/quickstart-guide#setup-with-codex-cli
