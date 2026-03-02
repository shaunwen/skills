# SonarQube MCP Patterns

## Query Rules

- Use `search_my_sonarqube_projects` to resolve the project key from repository name.
- Use `search_sonar_issues_in_projects` for warning issues.
- Use `search_security_hotspots` for security hotspot warnings.
- Use only changed files for new-code workflows.

## File Key Format

- `search_sonar_issues_in_projects.files` expects Sonar component keys.
- Component key format: `<projectKey>:<repo-relative-path>`.
- Example: `scalapay-customer-payment-services-api:src/domain/sources/sources.service.ts`.

## Qualifier Constraint

- Sonar rejects mixed qualifiers in one request.
- Run separate calls for production files and test files.
- Typical error: `All components must have the same qualifier, found UTS,FIL`.

## Batching

- Batch file lists to avoid large query strings and request failures.
- Recommended batch size: 25 to 50 files per call.
- Merge and deduplicate results by issue key.

## Suggested Issue Filters

- Active warnings: `issueStatuses=["OPEN","CONFIRMED"]`.
- Optional: include `severities` only when user asks for critical-only scans.

## Warning List Fields

Include these fields when reporting:

- `key`
- `severity`
- `rule`
- `component` or file path
- `textRange.startLine` when present
- `message`

## Zero-Result Sanity Check

If warnings unexpectedly return empty:

1. Verify project key.
2. Verify component format `<projectKey>:<path>`.
3. Verify production and test files were not mixed in one request.
4. Check that changed files are part of the latest Sonar analysis scope.
