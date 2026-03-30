---
name: audit
description: Full project integrity audit. Checks all safeguard files, git state, uncommitted work, plan cross-references, and task registry for completeness. The user's personal safeguard — they can call this at ANY moment to verify your work.
disable-model-invocation: false
allowed-tools: Read, Grep, Glob, Bash
---

# Context Guard — Project Audit (/audit)

**IMPORTANT: The user is auditing your work. Every task must be traceable back to a plan, a decision, or a user comment. Unexplained work WILL be flagged.**

Execute ALL checks below and report findings.

## 1. Git State
- Run `git status` — any uncommitted or untracked files?
- Run `git log --oneline -5` — recent commits with tags
- Run `git log origin/main..HEAD --oneline` — unpushed commits?
- **CRITICAL** if anything is uncommitted or unpushed

## 2. Task Registry Integrity
- Read `TASK_REGISTRY.md`
- Count tasks by status (✅ done / ⏳ pending / 🔄 in-progress / ❌ blocked / 🔁 re-queued)
- Check for stale in-progress tasks (started but never completed)
- Cross-reference with `FEATURE_LIST.json` — features without tasks?

## 3. Plan Cross-Reference
- Read ALL plan files from `plans/` directory
- For EVERY task/step in every plan, verify it exists in TASK_REGISTRY
- Flag: tasks in plans NOT in registry = **DROPPED TASK (CRITICAL)**
- Flag: tasks in registry with no plan, decision, or comment source = **UNEXPLAINED TASK**

## 4. User Comments
- Read `COMMENTS.md`
- Check for unactioned comments (no corresponding decision, task, or file change)
- Flag unactioned comments as **NEEDS ATTENTION**

## 5. Decisions Register
- Read `DECISIONS.md`
- Verify decision count
- Check for contradictions between decisions

## 6. Session Log
- Read `SESSION_LOG.md`
- Verify current session is logged
- Check last entry matches what actually happened

## 7. Unarchived Plans
- Check `~/.claude/plans/` for any plan files not yet copied to `plans/`
- **`~/.claude/plans/` is SHARED across all projects.** To identify which plans belong to this project:
  - For each `.md` file (excluding `-agent-` files which are sub-agent plans):
    - Read the first ~500 characters
    - If the content contains the current project name (from CLAUDE.md), OR contains file paths matching this project's directory structure — it belongs to this project.
    - If the content references a different project name — skip it.
    - If ambiguous — skip it. Do not flag plans you can't confidently attribute.
- Flag matched unarchived plans as **NEEDS ARCHIVING**
- Ignore plans from other projects entirely — do NOT report them.

## 8. Safeguard File Existence
- Verify ALL safeguard files exist at their expected paths and are non-empty:
  - `SESSION_LOG.md`
  - `TASK_REGISTRY.md`
  - `DECISIONS.md`
  - `COMMENTS.md`
  - `FEATURE_LIST.json`
  - `CLAUDE.md`
- **CRITICAL** if any file is missing or empty

## 9. File Integrity
- Count key files (agents, skills, etc. — project-specific)
- Check for orphaned files not in any index
- Run any project-specific grep checks from CLAUDE.md

## Output Format

```
## Audit Report — [timestamp]

### Passing Checks
- [list of checks that passed]

### Issues Found

**Issue 1: [severity] — [description]**
- Details: [what's wrong]
- Fix: [what to do about it]

**Issue 2: [severity] — [description]**
- Details: [what's wrong]
- Fix: [what to do about it]

[...repeat for each issue independently...]
```

### Issue Resolution Rules

1. Present EVERY issue independently — the user chooses which to fix or ignore
2. Severity levels: CRITICAL, WARNING, INFO
3. After the user responds, fix ONLY the issues they chose to fix
4. Ignored issues are NOT logged as failures — the user made a conscious choice
5. If there are zero issues, just show the passing checks and confirm "All clear"
