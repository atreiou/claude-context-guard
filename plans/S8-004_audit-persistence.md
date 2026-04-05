# Plan: Persist /audit results to file

## Context

Audit reports are only shown in conversation and lost when context compresses or the session ends. There's no history of audit results over time. Saving them to a file creates an audit trail and would let tools like Dev Base display audit health trends.

## Fix

### 1. `/audit` SKILL.md — Add Step 10: Save Report

After the output format section, add a new step that saves the audit report to a timestamped file:

```
## 10. Save Report

Save the full audit report (exactly as displayed above) to:
`audits/YYYY-MM-DD_HHMMSS.md`

Create the `audits/` directory if it doesn't exist. The timestamp uses the current date/time. This creates a persistent audit trail that survives context loss and can be read by external tools.
```

Also update `allowed-tools` in the frontmatter to include `Write` (currently only has `Read, Grep, Glob, Bash`).

### 2. `.gitignore` — Add `audits/`

Audit results are consumer-generated local content (like safeguard files). They must not be in the public repo.

### 3. `templates/CLAUDE.md` — Add audits/ to the safeguard files list

Add `audits/` to the "CRITICAL: READ THESE FILES FIRST" section so new sessions know it exists:
```
7. **`audits/`** — Saved audit reports with timestamps. Read the latest to check project health.
```

## Files to modify

| # | File | Action |
|---|------|--------|
| 1 | `.claude/skills/audit/SKILL.md` | **EDIT** — add allowed-tools Write, add Step 10 save report |
| 2 | `.gitignore` | **EDIT** — add `audits/` |
| 3 | `templates/CLAUDE.md` | **EDIT** — add audits/ to safeguard files list |

Then sync to all instances (scan /Software/ dynamically) + parent level.

## Verification

1. Read updated /audit skill — confirm Step 10 and Write in allowed-tools
2. Check .gitignore includes audits/
3. All repos committed and pushed clean
