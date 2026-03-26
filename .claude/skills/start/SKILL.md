---
name: start
description: Session start and context recovery. Reads all safeguard files, cross-references plans against task registry, and summarises project state. On first run, sets up safeguard files from templates. Type /start at the start of every session.
disable-model-invocation: true
allowed-tools: Read, Grep, Glob, Bash, Write, Edit
---

# Context Guard — Session Recovery (/start)

You are starting or resuming a session. Follow these steps EXACTLY:

## Step 0: First-Run Detection

Before reading safeguard files, check whether they exist yet.

Try to read `CLAUDE.md` in the project root.

- If `CLAUDE.md` does **not exist**, or it **contains the placeholder text `{PROJECT_NAME}`** — this is a **first run**. Go to the First-Run Setup below.
- If `CLAUDE.md` exists and does NOT contain `{PROJECT_NAME}` — this is a normal session. Skip to Step 1.

### First-Run Setup

**IMPORTANT: First-run setup is procedural, not a design task. Do NOT enter plan mode. Proceed directly with creating safeguard files. If plan mode is active, exit it before continuing.**

1. **Check for templates:** Look for a `templates/` folder in the project root. If it doesn't exist, tell the user: "No templates/ folder found. Please run install.sh first or copy the templates/ folder from the Context Guard repo." Then stop.

2. **Ask for project details:**
   > "Welcome to Claude Context Guard! Let's set up your project."
   > "What is your **project name**?"

   Wait for their answer. Then ask:
   > "Brief description (one line, or say 'skip'):"

3. **Create safeguard files from templates:**
   - Copy `templates/CLAUDE.md` → `CLAUDE.md` (project root)
   - Copy `templates/SESSION_LOG.md` → `SESSION_LOG.md`
   - Copy `templates/TASK_REGISTRY.md` → `TASK_REGISTRY.md`
   - Copy `templates/DECISIONS.md` → `DECISIONS.md`
   - Copy `templates/COMMENTS.md` → `COMMENTS.md`
   - Copy `templates/FEATURE_LIST.json` → `FEATURE_LIST.json`
   - Create `plans/` directory if it doesn't exist

4. **Populate placeholders in CLAUDE.md:**
   - Replace `{PROJECT_NAME}` with the user's project name
   - Replace `{PROJECT_DESCRIPTION}` with their description (or "TODO" if skipped)
   - Replace `{DATE}` with today's date

5. **Initialise SESSION_LOG.md:**
   - Add a Session 1 entry:
   ```
   ## Session 1 — [today's date] (Project Setup)

   **What happened:**
   - Project initialised with Claude Context Guard
   - Safeguard files created from templates

   **Tasks completed:** Context Guard setup
   **Tasks remaining:** None yet
   ```

6. **Report to the user:**
   ```
   ## Context Guard — First-Run Setup Complete

   ### Files Created
   - CLAUDE.md — project instructions (auto-read every session)
   - SESSION_LOG.md — session history
   - TASK_REGISTRY.md — task tracker
   - DECISIONS.md — decisions register
   - COMMENTS.md — user comments log
   - FEATURE_LIST.json — feature tracker
   - plans/ — plan archive directory

   ### Next Steps
   - Type /start at the beginning of every session for full context recovery
   - Type /audit at any time to verify integrity
   - Type /end when you're done for the day (optional clean save point)

   ### Would you like to run /itemise?
   The Itemisation Protocol adds numbered section markers to your code files,
   making every block referenceable by address (e.g. "check section 2.3.1").
   It's optional — toggle it off in CLAUDE.md at any time.
   Type /itemise to run it now, or skip and come back to it later.
   ```

7. **Stop here.** Do NOT continue to Step 1. The user is starting fresh — there are no previous sessions to recover from.

---

## Step 1: Read Safeguard Files

Read ALL of these files in order:
1. `CLAUDE.md` — project rules and architecture
2. `SESSION_LOG.md` — what happened in every previous session
3. `TASK_REGISTRY.md` — every task ever created, find the PENDING ones
4. `DECISIONS.md` — architectural decisions, never contradict these
5. `COMMENTS.md` — user's verbatim comments, check for unactioned ones
6. `FEATURE_LIST.json` — feature pass/fail status

## Step 2: Check Git State

Run: `git log --oneline --decorate -10 && echo "===" && git status && echo "===" && git log origin/main..HEAD --oneline`

Report: any uncommitted files, any unpushed commits.

## Step 2.5: Detect Unlogged Sessions

After checking git state, detect potential orphaned work:

1. Get the date of the last session entry in SESSION_LOG.md
2. Get the date of the most recent git commit: `git log -1 --format=%ci`
3. If the last commit is AFTER the last session log date, warn:

> ⚠️ **ORPHANED SESSION DETECTED**
> Last session logged: S[N] on [date]
> Last git commit: [hash] on [date] — "[message]"
> Work was done after the last logged session. This may mean a session ended without /end.
> Recommend: Review git log and reconstruct the missing session entry.

If the dates match or the session log is current, continue normally.

## Step 3: Cross-Reference Plans

Read the **last 3 plan files** from the `plans/` directory IN FULL.

For each plan:
- Check every task/step mentioned against TASK_REGISTRY.md
- Flag any task that appears in a plan but NOT in the registry (DROPPED TASK — critical)
- Flag any task in the registry with no corresponding plan, decision, or user comment (UNEXPLAINED TASK)

## Step 4: Determine Session Number

The new session number = last session in SESSION_LOG.md + 1.

## Step 5: Summarise

Present a clear summary:

```
## Session [N] — Context Recovery

### Last Session ([N-1])
[What was done]

### Pending Tasks
[List from TASK_REGISTRY with pending status]

### Unactioned Comments
[Any user comments not yet turned into decisions/tasks/changes]

### Cross-Reference Results
[Any dropped or unexplained tasks found]

### Git State
[Clean / uncommitted files / unpushed commits]

### Ready to proceed?
```

## Step 6: Wait

Do NOT start any work until the user confirms. Wait for their go-ahead.
