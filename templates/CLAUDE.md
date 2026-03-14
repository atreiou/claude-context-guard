# CLAUDE.md — {PROJECT_NAME} Project Instructions
# This file is auto-read by Claude Code at every session start.
# Last updated: {DATE}

## CRITICAL: READ THESE FILES FIRST BEFORE ANY WORK

1. **`SESSION_LOG.md`** — What happened in every previous session. READ THIS FIRST.
2. **`TASK_REGISTRY.md`** — Every task ever created, with status. CHECK before creating new tasks.
3. **`DECISIONS.md`** — Every architectural decision made. NEVER contradict these without explicit approval.
4. **`FEATURE_LIST.json`** — All features with pass/fail status. The authoritative progress tracker.
5. **`COMMENTS.md`** — User's verbatim comments from every session. SACRED — never lose these.
6. **`plans/`** — Archived plans from every session. Read the last 3 in full to cross-reference with TASK_REGISTRY.

## DROPPING TASKS IS ABSOLUTELY UNACCEPTABLE

Dropping tasks will result in the **complete failure of this project**. Every task you create MUST be logged in `TASK_REGISTRY.md` with a timestamp. If a task cannot be completed in this session, it MUST remain in the registry as `pending`. If a background agent fails (rate limit, timeout, etc.), the tasks it was supposed to do MUST be re-logged as `pending` in the registry.

Before ending any session or hitting context limits, UPDATE the session log and task registry.

## PRESERVE USER COMMENTS — MANDATORY

Every comment the user makes in conversation MUST be logged verbatim in `COMMENTS.md` with timestamp and session ID. This includes directions, feedback, decisions, preferences, corrections — everything. Failure to preserve comments is as dangerous to the project as deleting core files. Comments can be removed once actioned (turned into decisions, tasks, or file changes).

## USER AUDITS YOUR WORK

The user can call `/audit` at ANY moment to verify your work. Every task must be traceable back to a plan, a decision, or a user comment. Unexplained work WILL be flagged. Be prepared for this at all times.

## Project Overview

**Project:** {PROJECT_NAME}
**Description:** {PROJECT_DESCRIPTION}

## Git Conventions

- Every commit MUST be tagged with `S{session}-{sequence}_{short-description}`
  - Example: `S5-001_install-deps`, `S5-002_add-auth`
  - Session number from SESSION_LOG.md, sequence starts at 001 per session
  - Tag with: `git tag "S{session}-{sequence}_{short-description}" HEAD`
  - Push tags with: `git push --tags`
- Push to remote after every commit: `git push && git push --tags`
- All amendment comments use format: `<!-- AMENDMENT vX.Y (YYYY-MM-DD): description -->`

## Plan Archiving

After every approved plan is executed, archive it:
1. Copy from `~/.claude/plans/` to `plans/S{session}-{seq}_{description}.md`
2. Plans are cross-referenced by `/go` and `/audit` against the task registry
