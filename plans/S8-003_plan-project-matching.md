# Plan: Fix plan leaking between projects due to global ~/.claude/plans/

## Context

`~/.claude/plans/` is a single shared directory — all Claude Code sessions across all projects write plans there with random filenames (e.g., `foamy-launching-puppy.md`). There's no project scoping. This caused AutoPoster to display Dev Base's plan because it was the newest file globally.

CCG's `/end` and `/audit` skills both read from this directory and say "only archive/flag plans clearly related to THIS project" — but provide no concrete method for determining which project a plan belongs to.

## Fix

Add explicit project-matching instructions to the three skills that interact with `~/.claude/plans/`. The matching method: **read the first ~500 chars of each plan file and check if the project name appears in the content** (title, context section, or file paths). This is the same approach Dev Base already implemented in its parser.

### 1. `/end` SKILL.md — Step 3: Archive Plans

Replace the current "only archive plans clearly related to THIS project" instruction with concrete matching:

```
- For each `.md` file in `~/.claude/plans/` (excluding `-agent-` files which are sub-agent plans):
  - Read the first ~500 characters
  - If the content contains the current project name (from CLAUDE.md), OR contains file paths matching this project's directory structure — it belongs to this project. Archive it.
  - If the content clearly references a different project name — skip it. It belongs to another project.
  - If ambiguous (no project name found) — skip it. Do not archive plans you can't confidently attribute.
```

### 2. `/audit` SKILL.md — Section 7: Unarchived Plans

Same matching logic. Replace the vague "clearly related to THIS project" with the concrete content-matching instruction above.

### 3. `/start` SKILL.md — No change needed

`/start` Step 3 reads from `plans/` (the local archive), not from `~/.claude/plans/`. Plans are already project-scoped by the time they're in `plans/`. No fix needed here.

### 4. `templates/CLAUDE.md` — Plan Archiving section

Add a note about the shared directory:

```
## Plan Archiving

After every approved plan is executed, archive it:
1. Copy from `~/.claude/plans/` to `plans/S{session}-{seq}_{description}.md`
2. Plans are cross-referenced by `/start` and `/audit` against the task registry
3. **`~/.claude/plans/` is shared across all projects.** Only archive plans whose content references this project by name or file paths. Skip plans belonging to other projects.
```

## Files to modify

| # | File | Action |
|---|------|--------|
| 1 | `Claude Context Guard/.claude/skills/end/SKILL.md` | **EDIT** — Step 3, add content-matching logic |
| 2 | `Claude Context Guard/.claude/skills/audit/SKILL.md` | **EDIT** — Section 7, add content-matching logic |
| 3 | `Claude Context Guard/templates/CLAUDE.md` | **EDIT** — Plan Archiving section, add shared directory note |

Then sync to all instances (scan /Software/ dynamically) + parent level.

## Verification

1. Read updated /end and /audit skills — confirm content-matching instructions are present
2. Read updated templates/CLAUDE.md — confirm shared directory note
3. All repos committed and pushed clean
