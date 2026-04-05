# Plan: Fix /end skill executing plans instead of archiving them

## Context

When `/end` runs and encounters an approved plan in `~/.claude/plans/`, the agent treats the plan approval as a signal to start coding — instead of just archiving the plan and wrapping up. This happened in a real session: the user ran `/end`, the agent found an approved plan, executed it, and kept working when it should have stopped.

The root cause is that Step 3 ("Archive Plans") says to copy plans to `plans/` but doesn't explicitly say **stop — do not execute them**. The agent's default behaviour on seeing an approved plan is to implement it, and nothing in the skill overrides that instinct.

## Fix

**File:** `Claude Context Guard/.claude/skills/end/SKILL.md` — Step 3

Add an explicit rule at the top of the /end skill AND in Step 3:

**Top of skill (after the opening paragraph):**
```
**CRITICAL: /end is a SAVE-ONLY operation.** Do not start new work, execute plans, or make code changes beyond updating safeguard files. If a plan was approved this session but not yet executed, log it as ⏳ pending in TASK_REGISTRY.md and note it in the "Next session" field of the report. The next session will pick it up via /start.
```

**Step 3 update — replace current text with:**
```
## Step 3: Archive Plans

- Check `~/.claude/plans/` for any plans related to this project
- **IMPORTANT:** `~/.claude/plans/` is SHARED across all Claude Code projects. Only archive plans clearly related to THIS project.
- Copy relevant plans to `plans/S{session}-{seq}_{description}.md`
- **DO NOT EXECUTE archived plans.** /end is a save point, not an execution trigger. If a plan was approved but not yet implemented, mark its tasks as ⏳ pending in TASK_REGISTRY.md and record it in SESSION_LOG.md's "Next step" field so /start picks it up.
```

Then sync to all instances per D-007. **Scan `/Software/` dynamically** to find all projects with CCG installed — don't hardcode project names, as new projects may have been added.

## Files to modify

| # | File | Action |
|---|------|--------|
| 1 | `Claude Context Guard/.claude/skills/end/SKILL.md` | **EDIT** — add save-only rule + no-execute warning in Step 3 |

Then sync by scanning for all directories in `/Software/` that contain `.claude/skills/end/SKILL.md`, plus:
- `/Software/.claude/skills/end/SKILL.md` (parent level)
- Any nested CCG instances (e.g. Lilu runtime at `Lilu/claude-context-guard/`)

## Verification

1. Read updated /end SKILL.md — confirm both the top-level rule and Step 3 warning are present
2. All repos committed and pushed clean
