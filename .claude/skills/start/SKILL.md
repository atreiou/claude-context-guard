---
name: start
description: Session start and context recovery. Reads all safeguard files, cross-references plans against task registry, and summarises project state. Type /start at the start of every session.
disable-model-invocation: true
allowed-tools: Read, Grep, Glob, Bash
---

# Context Guard — Session Recovery (/start)

You are starting or resuming a session. Follow these steps EXACTLY:

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
