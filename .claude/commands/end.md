---
description: "Type /end to wrap up a session. Updates all safeguard files, rotates anything older than 5 sessions into the archives, commits, and leaves a clean handoff."
allowed-tools: Read, Grep, Glob, Bash, Edit, Write
---

# Context Guard — Session End (/end)

The user wants to wrap up this session cleanly. Your job is to create a save point so the next session can pick up seamlessly via `/start`.

**CRITICAL: /end is a SAVE-ONLY operation.** Do not start new work, execute plans, or make code changes beyond updating safeguard files. If a plan was approved this session but not yet executed, log it as ⏳ pending in TASK_REGISTRY.md and note it in the "Next session" field of the report. The next session will pick it up via /start.

**Date convention:** all dates written by this skill use **dd/mm/yy** (UK format). Do not retroactively rewrite older dates already in safeguard files; only new entries follow this rule.

## Step 0: Locate CCG Root

Safeguard files may not be in the current working directory — they could be in a subdirectory. Find them first.

0. **Check for a pointer file first:** if `CCG_LOCATION.md` exists at the working-directory root, it names CCG_ROOT directly. Trust it — skip the search below.
1. **Check the working directory:** Try to read `CLAUDE.md` in the current directory.
2. **If not found, search subdirectories:**
   ```bash
   find . -maxdepth 4 -name "CLAUDE.md" -type f 2>/dev/null | head -10
   ```
3. **Filter:** For each result, check it contains `TASK_REGISTRY.md` (confirms it's a Context Guard CLAUDE.md) and does NOT contain `{PROJECT_NAME}` (uninitialized template).
4. **Set CCG_ROOT:** Use the directory of the valid CLAUDE.md found. If multiple, ask the user. If none, warn: "No Context Guard files found. Run /start first."

**All safeguard file paths in subsequent steps are relative to CCG_ROOT.** Git operations should also run from CCG_ROOT if it differs from the working directory.

## Step 0.5: Completeness Check — never opt for brevity

Before saving, verify nothing from this session is missing. Log anything missing BEFORE proceeding to Step 1.

- Every user comment from this session → COMMENTS.md, verbatim, timestamped.
- Every task worked on → TASK_REGISTRY.md status updated.
- Every decision made → DECISIONS.md, with its `Category:` field.
- Every non-obvious gotcha, workaround, or >15-minute debug → LEARNED_BEHAVIOUR.md.
- **Did this session create or delete any credentials, accounts, or test fixtures?** If so, the FULL details — usernames, passwords, IDs, which are real identities and which are fixtures — must be recorded in the project's designated record (see CLAUDE.md; commonly `docs/TEST_USERS.md`) **and** in the session log **before this session counts as cleanly saved**. Not summarised, not deferred. A save that omits them blocks the next session outright: it cannot log in, and the information has to be recreated from scratch.

Brevity is not a virtue here. Trimming a detail because it feels secondary is a decision to withhold information nobody authorised you to withhold.

## Step 1: Gather Session Context

Review what was done this session:
- What tasks were worked on?
- What files were created or modified?
- What decisions were made?
- What user comments were given?

## Step 2: Update Safeguard Files

Check and update ALL of these:

### RESUME_STATE.md
- This is a SAVE-ONLY wipe. Overwrite RESUME_STATE.md with the clean template:
  ```
  # RESUME_STATE.md
  # Overwritten by /save. Wiped by /end. Read first by /start.
  # This file holds ONLY current in-flight state — not history. History lives in SESSION_LOG.md.

  **Session:** S[N+1]
  **Last updated:** dd/mm/yy HH:MM
  **Clean save:** true

  ## In-flight
  (No work in flight. This file is in its clean state.)

  ## Next step
  (Nothing pending.)
  ```
- `Clean save: true` tells the next `/start` that the previous session ended cleanly — no mid-flight recovery needed. The next-session intent still lives in SESSION_LOG.md's "Next step" field.
- **The "Next step" section is the next session's only plan pointer — make it precise.** `/start` no longer reads plan files, so whatever you write here is all the next agent gets. Name the exact task IDs, and if a plan governs the work, name the exact plan file *and the section within it* they should open. "Continue the migration" is useless. "Resume S12-004 at `plans/S11-002_auth-migration.md` §3 (session token rotation) — the schema change is done, the middleware is not" is a handoff.

### SESSION_LOG.md
- Add an entry for this session (or update the existing one)
- Include: what happened, commits made, tasks completed, tasks remaining
- **Next step:** Capture what the user wants done next, using their own words where possible. Not just a list of pending tasks — the actual direction, priority, and intent. This is what the next session's /start will read to understand where to pick up.
- **Errors encountered:** If any significant errors, blockers, or unexpected issues were hit during the session, log what happened and how it was resolved. Skip this if nothing notable occurred — don't force empty sections. This prevents future sessions from repeating the same mistakes.

### TASK_REGISTRY.md
- Log any new tasks created this session
- **When creating new tasks:** add `Governed by: D-xx, D-yy` to the Notes column for any decisions that constrain the task's implementation.
- Update status of tasks worked on (✅ done / ⏳ pending / 🔄 in-progress)
- **When marking a task ✅ done:** amend its Notes column with:
  - **Files:** 1–3 key paths touched
  - **Approach:** one sentence — the pattern or library used
  - **Governed by:** decision IDs that shaped the solution (if any)

  Example: `Files: widgets/favourite.php, blocks/fav-block.js | Approach: ACF flexible content with REST cache | Governed by: D-055`
- Ensure NO tasks are missing — cross-reference with what was actually done

### COMMENTS.md
- Verify all user comments from this session are logged verbatim
- If any are missing, add them now with timestamps

### DECISIONS.md
- If any architectural decisions were made this session, log them
- **Mandatory Category field** on every new entry: `forever-active`, `active-constraint`, `feature-specific`, or `superseded`. Default to `active-constraint` if uncertain.
- If a new decision supersedes an earlier one, mark the old `Category: superseded` with a pointer to the new D-number.

### LEARNED_BEHAVIOUR.md
- Log any non-obvious workaround, platform quirk, version-specific gotcha, or ">15 minutes debugging this" discovery from this session.
- Format:
  ```
  ## LB-NNN — [Short title] (Session N, dd/mm/yy)
  **Context:** Where this surfaces (platform, plugin, version)
  **Gotcha:** What fails and how
  **Workaround:** What actually works
  **Why:** Root cause if known
  **Related:** Tasks/decisions (optional)
  ```
- Do NOT log ordinary coding knowledge; only things a fresh agent would re-discover the hard way.

### FEATURE_LIST.json
- **Semantics:** FEATURE_LIST is a QA tracker, NOT a task-completion mirror. Only flip `passes: true` when the user has **manually verified** the feature works end-to-end. Task completion is tracked in TASK_REGISTRY.
- If the user reports a feature broken, flip `passes: false` with a `notes` description of the failing case.

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
   - **Keep:** All non-done tasks (⏳ 🔄 ❌ 🔁) + done tasks (✅) from the last 5 sessions
   - **Archive:** Done tasks (✅) from sessions older than the last 5
2. Create `TASK_REGISTRY_pageN.md` with archived done tasks, preserving their session headers.
3. Trim the main file: keep file header + all non-done tasks + last 5 sessions of done tasks.
4. **A pending row older than the window is NEVER silently dropped.** Over time the main file accumulates stale ⏳ rows that are still, technically, pending. Each one must get an explicit disposition — pick one and record it:
   - **Kept** — still genuinely actionable and owned by an agent. Move it into a `## Live backlog` section in the main file so it stays visible without pretending to belong to a recent session.
   - **Consolidated** — the work is now covered by another tracked item. Annotate the row `consolidated: <id of the thing that covers it>` and archive it. That counts as tracked, not dropped.
   - **Archived with its tag** — deferred or out-of-scope rows (post-MVP, deferred-to-user, blocked-on-third-party) keep their tag in the archive so a future search finds them.

   Deleting the row, or letting it vanish in a trim, is a project failure. If you cannot classify a row, keep it and flag it in the Step 6 report.
5. Add/update archive reference line.
6. If no done tasks older than 5 sessions and no stale pending rows, nothing to archive — skip.

### DECISIONS.md

Decisions rotate on the same 5-session window as everything else, but with one extra step that makes it safe: **the main file keeps a one-line index of every decision that has been archived.**

1. Move decisions older than the last 5 sessions into `DECISIONS_pageN.md`, full text intact.
2. For each one moved, add a line to the main file's `## Index of archived decisions` section:
   `D-042 — Sigil images are WebP-only [active-constraint] → DECISIONS_page3.md`
   ID, title, category, and which page holds it. Nothing more — the index has to stay cheap to read.
3. If a decision has no `Category:` field, treat it as `active-constraint` (safe default) and flag it for classification in your end report.
4. Mark `superseded` decisions as such (with a pointer to the D-number that replaced them) before archiving. They still archive — a superseded decision explains why the current one exists.
5. Add/update the archive reference line.

**Archiving does not revoke a decision.** `forever-active` and `active-constraint` decisions govern from the archive exactly as they did from the main file — the index is how future sessions find them. This is the whole reason the index exists: without it, the only way to keep a binding rule discoverable was to never archive it, and DECISIONS.md grew without limit until it swallowed the context window at every `/start`.

### LEARNED_BEHAVIOUR.md

Same mechanism as decisions.

1. Move entries older than the last 5 sessions into `LEARNED_BEHAVIOUR_pageN.md`, full text intact.
2. For each one moved, add a line to the main file's `## Index of archived LBs` section:
   `LB-017 — WPFC cache clear needs a fresh nonce → LEARNED_BEHAVIOUR_page2.md`
3. An entry whose underlying platform or library has been removed, or upgraded past the bug, can be marked `resolved` in the index — it stays findable but no longer needs reading.
4. Add/update the archive reference line.

An archived learned behaviour is still true. The index line is what stops a future session re-discovering it the hard way.

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
- RESUME_STATE.md — wiped to clean state (Clean save: true)
- SESSION_LOG.md — [updated / already current — reason]
- TASK_REGISTRY.md — [N tasks added/updated / no task changes — reason]
- COMMENTS.md — [N comments logged / no new comments this session]
- DECISIONS.md — [N decisions logged (all have Category field) / no new decisions — checked: no architecture choices, algorithm choices, UI patterns, data model changes, naming conventions, or approach reversals this session]
- LEARNED_BEHAVIOUR.md — [N entries logged / no new tactical knowledge — checked: no gotchas, workarounds, or >15min debugs this session]
- FEATURE_LIST.json — [N features verified / no QA updates — checked: user did not verify or report broken any features this session]

**Decision trigger check:** Were ANY of these made this session?
  Architecture choices, algorithm/approach selections, UI/UX pattern decisions,
  data model changes, naming conventions, technology selections, approach reversals,
  workflow changes, configuration decisions.
  If yes and DECISIONS.md wasn't updated → go back and update it now. Every new decision MUST have a `Category:` field.

**Learned behaviour trigger check:** Did the session surface any non-obvious workaround, platform quirk, version-specific gotcha, or ">15 minutes debugging this" discovery?
  If yes and LEARNED_BEHAVIOUR.md wasn't updated → update it now.

**Feature trigger check:** Did the user **manually verify** any feature working end-to-end this session, or report one broken? Task completion does NOT count — only human verification.
  If yes and FEATURE_LIST.json wasn't updated → go back and update it now.

If any file shows 0 changes, the reason must be specific (not "no changes needed").
"No changes needed" without explanation is not acceptable — state what you checked.

## Step 3: Archive Plans

- Check `~/.claude/plans/` for plans belonging to this project
- **`~/.claude/plans/` is SHARED across all Claude Code projects.** Plans from other projects will be in this folder — do not touch them. To identify which plans belong to this project:
  - For each `.md` file (excluding `-agent-` files which are sub-agent plans):
    - Read the first ~500 characters
    - If the content contains the current project name (from CLAUDE.md), OR contains file paths matching this project's directory structure — it belongs to this project. Archive it.
    - If the content clearly references a different project name — skip it.
    - If ambiguous (no project name found) — skip it. Do not archive plans you can't confidently attribute.
- Copy matched plans to `plans/S{session}-{seq}_{description}.md`
- **DO NOT EXECUTE archived plans.** /end is a save point, not an execution trigger. If a plan was approved but not yet implemented, mark its tasks as ⏳ pending in TASK_REGISTRY.md and record it in SESSION_LOG.md's "Next step" field so /start picks it up.

**Internal verification:** Check the **5 most recently modified** `.md` files in `~/.claude/plans/`. Read each file's first ~500 characters, match against the project name, and archive any that belong to this project. Do not output the verification details — just report the result: either "Archived N plans: [list]" or "No new project plans found to archive."

## Step 4: Git Commit & Push

Check CLAUDE.md "Version Control" section:
- If mode is "none" → skip this entire step
- If mode is "local" → commit and tag only, no push
- If mode is "remote" → commit, tag, push (default behaviour if no Version Control section exists)

**Stage explicit paths only. NEVER `git add -A` or `git add .`.** The working tree may be shared with other agents or with a paused lane of work, and a blanket stage sweeps their files into your commit. Name every path you stage.

1. Run `git status` to see ALL modified and untracked files
2. For EVERY modified file shown, cross-reference with the conversation to confirm the changes were approved (any positive acknowledgement counts — "looks good", "cool", accepting and moving on, etc.):
   - If approved this session → stage it by name
   - If from a prior session (orphaned work) → check SESSION_LOG/TASK_REGISTRY for approval context. If the work was part of a completed task, stage it AND note in the commit message: "Includes orphaned work from S[N]"
   - If unapproved or unclear → ask the user before staging
   - If it belongs to another agent's lane → leave it alone entirely and surface it in the report
   - If it should NOT be committed (temp files, diagnostics) → explicitly list it as excluded with reason
3. For EVERY untracked file shown:
   - If it's project code or safeguard files you can attribute to this session → stage it by name
   - If it's a temp/diagnostic file → add to .gitignore or explicitly exclude with reason
   - If you cannot attribute it → leave it, and say so
4. Commit with a descriptive message
5. Tag with the project's commit tagging convention
6. Run `git status` AFTER committing — it MUST show a clean tree, excluding gitignored files and any untracked lane you deliberately left alone
7. If the tree is NOT clean for any other reason → something was missed, go back
8. Push to remote: `git pull --rebase origin main && git push && git push --tags`. Rebasing first keeps a shared branch linear and surfaces a divergence as a conflict you resolve now, rather than as a merge commit nobody asked for or a rejected push at the end of a session.
- **Backup remote (CCG only):** This step applies only to the Context Guard source-of-truth repo, which uses a dual-remote setup: `origin` (public) + `backup` (private dev). Most projects have a single `origin` remote — that IS their backup. If you're on a project with only `origin`, skip this step. Do NOT flag a missing `backup` remote as an issue.
  If a `backup` remote exists: `git checkout dev && git merge main --no-edit && git push backup dev && git checkout main`

## Step 5: Verify Clean State

Run these checks:
- `git status` — should be clean (no uncommitted changes)
- `git log origin/main..HEAD --oneline` — should be empty (nothing unpushed)
- All safeguard files should be up to date

## Step 6: Report

Present the session summary in EXACTLY this format. Do not vary the structure, headings, or field names:

```
## Session [N] — Save Point

**What was done:** [1-2 sentence summary of the session's main accomplishments]

**Tasks:** [X] done, [Y] pending, [Z] in progress
- Pending: [list task IDs and names, or "None"]
- In progress: [list task IDs and names, or "None"]

**Commits:** [list of commit hashes, or "None — working tree clean"]

**Repos pushed:**
- [repo name]: [commit hash] ✅ (or ❌ if not pushed, with reason)

**Next session:** [What /start will find. User's stated intent for next session, or "No pending work."]
```

Do not add extra sections. Do not add "Files Modified" unless the session had no commits (uncommitted work needs visibility). Keep it scannable — this is a status report, not a narrative.
