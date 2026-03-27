---
name: end
description: Session save point. Updates all safeguard files, commits uncommitted work, and ensures a clean handoff for the next session. Optional — use when you want to cleanly wrap up before stopping.
disable-model-invocation: true
allowed-tools: Read, Grep, Glob, Bash, Edit, Write
---

# Context Guard — Session End (/end)

The user wants to wrap up this session cleanly. Your job is to create a save point so the next session can pick up seamlessly via `/start`.

## Step 0: Verify Completeness Before Saving

Before saving, verify nothing has been missed this session:
- Are there any user comments from this session NOT yet in COMMENTS.md?
- Are there any tasks worked on NOT yet updated in TASK_REGISTRY.md?
- Review the conversation for any decisions made but not logged in DECISIONS.md

If anything is missing, log it BEFORE proceeding to Step 1.

## Step 1: Gather Session Context

Review what was done this session:
- What tasks were worked on?
- What files were created or modified?
- What decisions were made?
- What user comments were given?

## Step 2: Update Safeguard Files

Check and update ALL of these:

### SESSION_LOG.md
- Add an entry for this session (or update the existing one)
- Include: what happened, commits made, tasks completed, tasks remaining

### TASK_REGISTRY.md
- Log any new tasks created this session
- Update status of tasks worked on (✅ done / ⏳ pending / 🔄 in-progress)
- Ensure NO tasks are missing — cross-reference with what was actually done

### COMMENTS.md
- Verify all user comments from this session are logged verbatim
- If any are missing, add them now with timestamps

### DECISIONS.md
- If any architectural decisions were made this session, log them

### FEATURE_LIST.json
- If any features changed status (passes: false → true), update them

## Step 3: Archive Plans

- Check `~/.claude/plans/` for any plans related to this project
- **IMPORTANT:** `~/.claude/plans/` is SHARED across all Claude Code projects. Only archive plans clearly related to THIS project.
- Copy relevant plans to `plans/S{session}-{seq}_{description}.md`

## Step 4: Git Commit & Push

- Run `git status` to see what's uncommitted
- Stage and commit all changes with a descriptive message
- Tag with the project's commit tagging convention
- Push to remote (including tags)

## Step 5: Verify Clean State

Run these checks:
- `git status` — should be clean (no uncommitted changes)
- `git log origin/main..HEAD --oneline` — should be empty (nothing unpushed)
- All safeguard files should be up to date

## Step 6: Report

Present a summary:

```
## Session [N] — Save Point

### What Was Done
- [bullet list of completed work]

### Tasks Status
- Done: [count]
- Pending: [count] — [list them]
- In Progress: [count] — [list them]

### Files Modified
- [list of files changed this session]

### Git State
- Last commit: [hash] [message]
- Pushed to remote: ✅

### Next Session Pickup
- [What /start will find when it runs next time]
- [Any pending work to continue]
```
