---
name: save
description: Mid-session checkpoint. Updates all safeguard files with current progress without git operations or plan archiving. A quick save point that protects against context loss during long sessions.
disable-model-invocation: false
allowed-tools: Read, Grep, Glob, Bash, Edit, Write
---

# Context Guard — Mid-Session Checkpoint (/save)

The user wants to save current progress without ending the session. This is a lightweight checkpoint — no plan archiving, no session wrap-up. Update safeguard files, commit, push, and confirm.

## Step 0: Locate CCG Root

Safeguard files may not be in the current working directory — they could be in a subdirectory. Find them first.

1. **Check the working directory:** Try to read `CLAUDE.md` in the current directory.
2. **If not found, search subdirectories:**
   ```bash
   find . -maxdepth 4 -name "CLAUDE.md" -type f 2>/dev/null | head -10
   ```
3. **Filter:** For each result, check it contains `TASK_REGISTRY.md` (confirms it's a Context Guard CLAUDE.md) and does NOT contain `{PROJECT_NAME}` (uninitialized template).
4. **Set CCG_ROOT:** Use the directory of the valid CLAUDE.md found. If multiple, ask the user. If none, warn: "No Context Guard files found. Run /start first."

**All safeguard file paths in subsequent steps are relative to CCG_ROOT.** Git operations should also run from CCG_ROOT if it differs from the working directory.

## Step 0.5: Verify Completeness

Before saving, check what might be missing:
- Are there any user comments from this session NOT yet in COMMENTS.md?
- Are there any tasks worked on NOT yet updated in TASK_REGISTRY.md?
- Review the recent conversation for any decisions made but not logged in DECISIONS.md

If anything is missing, log it BEFORE proceeding to Step 1.

## Step 1: Gather Current Context

Quickly review what has happened since the last checkpoint or session start:
- What tasks were worked on or completed?
- What files were created or modified?
- What decisions were made?
- What user comments were given?

## Step 2: Update Safeguard Files

Check and update ALL of these:

### SESSION_LOG.md
- If no entry exists for this session yet, create one
- If an entry already exists, append a checkpoint marker:
  ```
  **Checkpoint [HH:MM]:** [brief summary of progress since last save]
  **In flight:** [what is actively being worked on right now — the approach, current state, and next micro-step]
  ```
- The "In flight" line is critical — if context is lost after this save, this is what the next session reads to understand exactly where you were mid-thought. Write it like a handoff note to yourself.
- If any significant errors or blockers were hit since the last save, add: `**Error fixed:** [what happened and how it was resolved]`
- If the user has expressed what they want done next, add: `**Next step:** [user's intent in their own words]`
- Do NOT close out the session entry — work is continuing

### TASK_REGISTRY.md
- Log any new tasks created since the last save
- Update status of tasks worked on (✅ done / ⏳ pending / 🔄 in-progress)
- Ensure no tasks are missing

### COMMENTS.md
- Verify all user comments since the last save are logged verbatim
- If any are missing, add them now with timestamps

### DECISIONS.md
- If any architectural decisions were made since the last save, log them

### FEATURE_LIST.json
- If any features changed status (passes: false → true), update them

## Step 3: Git Commit & Push

After updating safeguard files, commit everything to git so the save point is durable:

1. **Stage all changes** — safeguard files AND any code changes since the last commit:
   ```
   git add [all modified and new files]
   ```
2. **Commit** with a descriptive message:
   ```
   git commit -m "Checkpoint: [brief summary of work since last commit]"
   ```
3. **Push** to remote: `git push`

If there are no changes to commit (everything is already committed), skip this step.

## Step 4: Confirm

Present a brief confirmation — keep it concise, not a full report:

```
## Checkpoint Saved

- SESSION_LOG.md — [updated/no changes needed]
- TASK_REGISTRY.md — [N tasks updated / no changes needed]
- COMMENTS.md — [N comments added / no changes needed]
- DECISIONS.md — [N decisions added / no changes needed]
- FEATURE_LIST.json — [N features updated / no changes needed]
- Git — [commit hash] pushed / no changes to commit

Progress is saved. Continue working — run /save again any time, or /end to wrap up.
```

Do NOT perform any of the following (these are /end responsibilities):
- Plan archiving
- Git state verification
- Full session summary report
