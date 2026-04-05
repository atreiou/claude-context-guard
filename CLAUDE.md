# CLAUDE.md — Claude Context Guard Project Instructions
# This file is auto-read by Claude Code at every session start.
# Last updated: 2026-03-28

## CRITICAL: READ THESE FILES FIRST BEFORE ANY WORK

1. **`SESSION_LOG.md`** — What happened in every previous session. READ THIS FIRST.
2. **`TASK_REGISTRY.md`** — Every task ever created, with status. CHECK before creating new tasks. Column format: `| ID | Timestamp | Task | Status | Notes |`. IDs use `S{session}-{seq}` format. Status uses emoji: ✅ done, 🔄 in-progress, ⏳ pending, ❌ blocked, 🔁 re-queued.
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

## AUTO-CHECKPOINT PROTOCOL

Update safeguard files (SESSION_LOG.md, TASK_REGISTRY.md, COMMENTS.md) IMMEDIATELY after:
- Any task status change (completed/failed/blocked)
- Any new decision is made
- Every 3-4 user messages (batch update)
- Before any potentially long operation (testing, uploads, large code generation)
- When conversation is getting very long (approaching context limits)
- Or when the user runs `/save` to manually trigger a checkpoint

Do NOT wait for /end. Treat safeguard files as a running log, updated incrementally. When saving, capture not just what was completed but what is **in flight** — the current approach, state, and next micro-step. If context is lost, this is the handoff note.

## AUTOMATIC PRE-COMPACTION SAVE

A PreCompact hook automatically backs up all safeguard files before Claude Code compresses the conversation. Copies are saved to `compaction-backups/YYYY-MM-DD_HHMMSS/`. This is a safety net — if context is lost and safeguard files weren't fully up to date, the backup preserves the last known state. The hook runs automatically; no action is needed from you or the user.

For best results, also follow the AUTO-CHECKPOINT PROTOCOL above to keep safeguard files current throughout the session.

## RATE LIMIT AWARENESS

Rate limits pause the session but do NOT trigger compaction — context stays intact while waiting. The danger is when a rate limit hits **mid-operation** (e.g. halfway through a multi-file sync or large refactor). When the session resumes, you may lose track of which steps were completed. To protect against this:

1. **Before any multi-step operation** (syncing to multiple repos, batch edits, large refactors), update safeguard files FIRST
2. **After resuming from a rate limit**, re-read TASK_REGISTRY.md and SESSION_LOG.md to confirm where you left off
3. **Mark tasks as done individually** as you complete them, not in a batch at the end — a rate limit between step 3 and step 7 of a plan should not lose the record of steps 1-3

## CONTEXT OVERFLOW PROTOCOL

If the conversation is getting very long:
1. IMMEDIATELY update all safeguard files with current progress
2. Tell the user: "Context is getting large. I've saved all progress to safeguard files. You can run /save to force a checkpoint, or if I lose context, run /start to recover."
3. Continue working but update safeguard files after every significant action

## SAVE FREQUENCY

After every significant block of work (completing a task, fixing a bug, making a decision, receiving user feedback), append to SESSION_LOG.md and update TASK_REGISTRY.md. The /end command is a CLEAN save — but incremental saves should happen throughout the session. The user can also run /save at any time to trigger an explicit mid-session checkpoint. If context is lost mid-session, the safeguard files should contain 90%+ of what happened. When saving, always capture: (1) what was done, (2) what is in flight right now, (3) what the user wants next, and (4) any errors hit and how they were resolved. These four elements make the difference between a useful handoff and a stale status update.

## SLASH COMMAND ENFORCEMENT

When the user types a message containing `/word` where `word` matches a skill name in `.claude/skills/`, you MUST invoke it via the Skill tool. NEVER manually replicate skill steps — skills exist because manual replication is error-prone and incomplete. A `UserPromptSubmit` hook will remind you, but you should not need the reminder.

## IMPORTANT: PUBLIC REPO HYGIENE

This project has TWO copies:
- **Local working copy** (this directory) — has CCG tracking its own development. Safeguard files, plans, session history all live here but are gitignored.
- **Public GitHub repo** (`atreiou/claude-context-guard`) — clean, consumer-grade. No development history, no private info, no plans. Must look professional to anyone checking out the codebase.

The `.gitignore` handles this automatically. Never force-add gitignored files.

## IMPORTANT: UPDATE WORKFLOW

After any CCG improvement:
1. Make the change here in the CCG repo
2. Commit and push to GitHub
3. Sync to ALL consumer instances: AutoPoster, Audit for AI, Dev Base, Lilu (build-time + runtime)
4. Commit and push each project

Do NOT wait to be asked. This is automatic every time.

## Project Overview

**Project:** Claude Context Guard
**Description:** A task tracking and context protection system with slash commands for Claude Code. Open source at github.com/atreiou/claude-context-guard.
**Consumer projects:** AutoPoster, Audit for AI, Dev Base, Lilu (build-time + runtime)

## Git Conventions

- Every commit MUST be tagged with `S{session}-{sequence}_{short-description}`
  - Example: `S5-001_install-deps`, `S5-002_add-auth`
  - Session number from SESSION_LOG.md, sequence starts at 001 per session
  - Tag with: `git tag "S{session}-{sequence}_{short-description}" HEAD`
  - Push tags with: `git push --tags`
- Push to remote after every commit: `git push && git push --tags`

## Plan Archiving

After every approved plan is executed, archive it:
1. Copy from `~/.claude/plans/` to `plans/S{session}-{seq}_{description}.md`
2. Plans are cross-referenced by `/start` and `/audit` against the task registry

## Key Design Principles

1. External state over in-context memory — files survive, context windows don't
2. JSON for structured data — prevents accidental LLM overwrites
3. Cross-referencing over trust — verify plans against registries
4. Minimal context loading — read indexes first, fetch specifics only when needed
5. User can audit at any time — transparency and accountability
6. Referenceable code — Itemisation Protocol for direct addressing
