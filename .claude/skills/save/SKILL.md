---
name: save
description: Mid-session checkpoint. Updates all safeguard files with current progress without git operations or plan archiving. A quick save point that protects against context loss during long sessions.
disable-model-invocation: true
allowed-tools: Read, Grep, Glob, Bash, Edit, Write
---

# Context Guard — Mid-Session Checkpoint (/save)

The user wants to save current progress without ending the session. This is a lightweight checkpoint — no git operations, no plan archiving, no session wrap-up. Just update the safeguard files and confirm.

## Step 0: Verify Completeness

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
  ```
- Do NOT close out the session entry — work is continuing

### TASK_REGISTRY.md
- Log any new tasks created since the last save
- Update status of tasks worked on (done/pending/in-progress)
- Ensure no tasks are missing

### COMMENTS.md
- Verify all user comments since the last save are logged verbatim
- If any are missing, add them now with timestamps

### DECISIONS.md
- If any architectural decisions were made since the last save, log them

### FEATURE_LIST.json
- If any features changed status (passes: false → true), update them

## Step 3: Confirm

Present a brief confirmation — keep it concise, not a full report:

```
## Checkpoint Saved

- SESSION_LOG.md — [updated/no changes needed]
- TASK_REGISTRY.md — [N tasks updated / no changes needed]
- COMMENTS.md — [N comments added / no changes needed]
- DECISIONS.md — [N decisions added / no changes needed]
- FEATURE_LIST.json — [N features updated / no changes needed]

Progress is saved. Continue working — run /save again any time, or /end to wrap up.
```

Do NOT perform any of the following (these are /end responsibilities):
- Git commit, push, or tagging
- Plan archiving
- Git state verification
- Full session summary report
