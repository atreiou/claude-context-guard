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

## AUTO-CHECKPOINT PROTOCOL

Update safeguard files (SESSION_LOG.md, TASK_REGISTRY.md, COMMENTS.md) IMMEDIATELY after:
- Any task status change (completed/failed/blocked)
- Any new decision is made
- Every 3-4 user messages (batch update)
- Before any potentially long operation (testing, uploads, large code generation)
- When conversation is getting very long (approaching context limits)
- Or when the user runs `/save` to manually trigger a checkpoint

Do NOT wait for /end. Treat safeguard files as a running log, updated incrementally.

## AUTOMATIC PRE-COMPACTION SAVE

A PreCompact hook is installed that fires BEFORE Claude Code compresses the conversation. When it fires, you will see a notification: "Context Guard — Auto-saving before compaction." When this triggers, you MUST update all safeguard files with current progress BEFORE compaction proceeds. This is your last chance to preserve details that will be lost to compression. Follow the /save steps: update SESSION_LOG.md (with checkpoint marker noting "auto-save before compaction"), TASK_REGISTRY.md, COMMENTS.md, DECISIONS.md, and FEATURE_LIST.json.

## CONTEXT OVERFLOW PROTOCOL

If the conversation is getting very long:
1. IMMEDIATELY update all safeguard files with current progress
2. Tell the user: "Context is getting large. I've saved all progress to safeguard files. You can run /save to force a checkpoint, or if I lose context, run /start to recover."
3. Continue working but update safeguard files after every significant action

## SAVE FREQUENCY

After every significant block of work (completing a task, fixing a bug, making a decision, receiving user feedback), append to SESSION_LOG.md and update TASK_REGISTRY.md. The /end command is a CLEAN save — but incremental saves should happen throughout the session. The user can also run /save at any time to trigger an explicit mid-session checkpoint. If context is lost mid-session, the safeguard files should contain 90%+ of what happened.

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
2. Plans are cross-referenced by `/start` and `/audit` against the task registry

## Itemisation Protocol

ITEMISATION: enabled

The Itemisation Protocol adds hierarchical section numbers to code blocks so every part of the codebase is referenceable by address (e.g. "check section 2.3.1"). This reduces the context an LLM needs to load — instead of reading an entire file, you can point directly to the relevant block.

**To disable:** change `ITEMISATION: enabled` to `ITEMISATION: disabled` above. The `/itemise` command will halt before making any changes.

### What Gets Numbered

Number logical **blocks** that serve as identifiable, referenceable units — not individual lines.

- **Sections** — top-level logical groups: `// 1. SECTION: Name` ... `// end of 1`
- **Functions and methods**: `// 1.1 functionName()` ... `// end of 1.1`
- **Significant conditionals** — if/else/switch with meaningful business logic: `// 1.1.1 Description`
- **Important loops** — for/while/foreach with non-trivial bodies: `// 1.1.2 Description`
- **Key configuration objects** — complex arrays/objects passed to important calls: `// 1.2.1 Description`
- **Notable parameters** within those, when the parameter itself calls a function or is complex: `// 1.2.1.1 Description`

### What Does NOT Get Numbered

- Individual variable declarations
- Single-line assignments
- Simple imports, requires, or use statements
- Closing braces and trivial boilerplate
- Anything already explained by its parent block's label

### Comment Syntax by Language

| Language | Format |
|----------|--------|
| JS, TS, PHP, Java, C#, Go | `// 1.1 Description` |
| Python, Ruby, Shell, YAML | `# 1.1 Description` |
| HTML, XML, Vue templates | `<!-- 1.1 Description -->` |
| CSS, SCSS, Less | `/* 1.1 Description */` |
| SQL | `-- 1.1 Description` |

### Applying Itemisation to Existing Code

Run `/itemise` to apply the protocol to existing files. The command will:
1. Confirm the list of files before touching anything
2. Create `{filename}.itemise-backup` copies
3. Rewrite each file with numbering applied
4. Verify integrity (strips added comment-numbers, diffs against backup — confirms no code changed)
5. Delete backups on success; restore on failure

### Cross-References

When a section calls a function or method defined in another numbered section of the same file, the marker includes a `[calls: N.M]` tag:

```
// 3.2 handlePayment() [calls: 1.1, 2.3]
```

- Only track function/method calls, not shared variables or implicit dependencies
- Multiple calls are comma-separated: `[calls: 1.1, 2.3, 5.1]`
- Cross-references are scoped to the same file — cross-file dependencies are out of scope
- References are refreshed automatically when `/itemise` is re-run

### Reading Specific Sections

For itemised files over ~100 lines, prefer targeted section reads over loading the full file. The section markers are grep-friendly anchors that cannot go stale.

**To read a specific section (e.g. section 4.2):**

1. Grep for the start marker to get its line number
2. Grep for the end marker (`end of 4.2`) to get its line number
3. Use `Read(file_path, offset=START_LINE, limit=END_LINE - START_LINE + 1)` to load just that section

**If no end marker exists** (short blocks skip them per the protocol), read 20 lines from the start marker and look for the next numbered marker to determine the boundary.

**Nested sections:** Reading a parent section (e.g. `4`) via its start/end markers includes all children (`4.1`, `4.2`, etc.). To read only the parent's preamble, read from the `4` marker to the `4.1` marker.

### Impact Advisories

When modifying a section, grep the file for `[calls: N.M]` references pointing to it. If other sections depend on the one being changed, flag this to the user:

- "Section 4.2 calls this function — check if it needs updating too"
- "This feature is linked with section 3.1 — consider adding a task to update it"

This is advisory, not blocking — mention it and move on. The agent may already be aware of the dependency; that's fine. The check costs nothing and occasionally prevents a missed update.
