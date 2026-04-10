---
name: save
description: "Type /save to checkpoint progress mid-session. Updates all safeguard files without ending the session. Protects against context loss during long sessions."
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

## Step 2.5: Rotate Safeguard Files (Pagination)

**Always run this step.** You have full session context right now — use it to make smart archival decisions. Archive anything older than 5 sessions or fully actioned, regardless of file size. Don't wait for files to get large — keep them lean proactively.

### SESSION_LOG.md
1. Count `## Session` headers. Keep the **last 5 sessions** in the main file.
2. Everything above the 5th-from-last `## Session` header → move to archive.
3. Determine the next page number: check for existing `SESSION_LOG_page*.md` files. New page = highest existing + 1 (or 1 if none exist).
4. Create `SESSION_LOG_pageN.md` with header:
   ```
   # SESSION_LOG — Archive Page N (Sessions X–Y)
   # Current sessions: see SESSION_LOG.md
   ---
   [archived content]
   ```
5. Trim `SESSION_LOG.md`: keep the file header (lines before the first `## Session`) + the last 5 sessions.
6. Add/update an archive reference line after the file header: `# 📁 Archives: SESSION_LOG_page1.md, SESSION_LOG_page2.md, ...`
7. If 5 or fewer sessions exist, nothing to archive — skip.

### TASK_REGISTRY.md
1. Scan all task rows. Separate into:
   - **Keep:** All non-done tasks (⏳ 🔄 ❌ 🔁) regardless of session + done tasks (✅) from the last 5 sessions
   - **Archive:** Done tasks (✅) from sessions older than the last 5
2. Create `TASK_REGISTRY_pageN.md` with archived done tasks, preserving their session headers.
3. Trim the main file: keep file header + all non-done tasks + last 5 sessions of done tasks.
4. Add/update archive reference line.
5. If no done tasks older than 5 sessions, nothing to archive — skip.

### DECISIONS.md
1. Review each decision using your session context. Identify **actioned decisions** — those fully implemented and no longer actively constraining current work. Once the part of the build a decision relates to is complete and you've moved on, that decision is actioned.
2. Move actioned decisions → `DECISIONS_pageN.md`.
3. Keep all active/unactioned decisions in the main file.
4. Add/update archive reference line.

### COMMENTS.md
1. Review each comment using your session context. Identify:
   - **Actioned comments** — turned into decisions, tasks, or file changes
   - **Curiosity questions** — exploratory/informational, not project directives
2. Move both categories → `COMMENTS_pageN.md`.
3. Keep all unactioned project directives in the main file.
4. Add/update archive reference line.

**FEATURE_LIST.json** — skip, stays compact.

## Step 2.8: Verify Update Completion

Before proceeding to git, confirm every safeguard file was addressed. Output this checklist:

**Update verification:**
- SESSION_LOG.md — [updated / already current — reason]
- TASK_REGISTRY.md — [N tasks added/updated / no task changes — reason]
- COMMENTS.md — [N comments logged / no new comments this session]
- DECISIONS.md — [N decisions logged / no new decisions — checked: no architecture choices, algorithm choices, UI patterns, data model changes, naming conventions, or approach reversals this session]
- FEATURE_LIST.json — [N features updated / no feature status changes — checked: no features changed pass/fail, no new sub-features, no significant rework]

**Decision trigger check:** Were ANY of these made this session?
  Architecture choices, algorithm/approach selections, UI/UX pattern decisions,
  data model changes, naming conventions, technology selections, approach reversals,
  workflow changes, configuration decisions.
  If yes and DECISIONS.md wasn't updated → go back and update it now.

**Feature trigger check:** Did ANY feature change status this session?
  New features added, existing features passing/failing, sub-features created,
  significant feature rework.
  If yes and FEATURE_LIST.json wasn't updated → go back and update it now.

If any file shows 0 changes, the reason must be specific (not "no changes needed").
"No changes needed" without explanation is not acceptable — state what you checked.

## Step 3: Git Commit & Push

Check CLAUDE.md "Version Control" section:
- If mode is "none" → skip this entire step
- If mode is "local" → commit only, no push
- If mode is "remote" → commit and push (default behaviour if no Version Control section exists)

After updating safeguard files, commit everything to git so the save point is durable:

1. Run `git status` to see ALL modified and untracked files
2. Stage safeguard files AND any approved code changes since the last commit
3. Commit with a descriptive message: `"Checkpoint: [brief summary]"`
4. Push to remote: `git push`
5. If `git status` still shows uncommitted project files after the commit, something was missed — go back

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
