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
| [sonarqube-new-code-warning-fixer](sonarqube-new-code-warning-fixer/SKILL.md) | Analyze newly updated code with SonarQube MCP, list warnings, fix all warnings, and fix broken tests. |

## Skill Prerequisites

For `sonarqube-new-code-warning-fixer`, ensure:

1. SonarQube MCP server for SonarQube Server is configured for your AI agent environment.
2. A relatively recent `python3` is installed and available on `PATH`.

Reference setup example:
- SonarQube MCP quickstart (Codex CLI example): https://docs.sonarsource.com/sonarqube-mcp-server/quickstart-guide#setup-with-codex-cli
