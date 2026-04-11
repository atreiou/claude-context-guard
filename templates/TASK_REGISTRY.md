# TASK_REGISTRY.md — {PROJECT_NAME} Permanent Task Log
# EVERY TASK EVER CREATED MUST BE LOGGED HERE WITH A TIMESTAMP
# DROPPING TASKS IS ABSOLUTELY UNACCEPTABLE AND WILL RESULT IN PROJECT FAILURE
# CHECK THIS FILE BEFORE CREATING NEW TASKS — DO NOT DUPLICATE
#
# Status: ✅ done | 🔄 in-progress | ⏳ pending | ❌ blocked | 🔁 re-queued (failed, needs retry)
#
# Column format: | ID | Timestamp | Task | Status | Notes |
# ID = S{session}-{seq} (e.g. S1-001, S2-003). Timestamp = YYYY-MM-DD.
#
# Notes may include:
#   - `Governed by: D-xx, D-yy`  — decisions that constrain this task's implementation (strongly recommended for architectural work)
#   - `Blocked on: T-zz`         — other tasks this depends on
#   - On completion, amend with: `Files: path1, path2 | Approach: one-sentence pattern/library | Governed by: D-xx`
#   This makes the archived registry a queryable knowledge base, not dead rows.
#
# When a background agent fails (rate limit, timeout, etc.), its tasks MUST be re-logged as pending
# When a session ends, ALL incomplete tasks MUST remain here with their current status

---

## Session 1 — {DATE}

| ID | Timestamp | Task | Status | Notes |
|----|-----------|------|--------|-------|
