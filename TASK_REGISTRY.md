# TASK_REGISTRY.md — Claude Context Guard Permanent Task Log
# EVERY TASK EVER CREATED MUST BE LOGGED HERE WITH A TIMESTAMP
# DROPPING TASKS IS ABSOLUTELY UNACCEPTABLE AND WILL RESULT IN PROJECT FAILURE
# CHECK THIS FILE BEFORE CREATING NEW TASKS — DO NOT DUPLICATE
#
# Status: ✅ done | 🔄 in-progress | ⏳ pending | ❌ blocked | 🔁 re-queued (failed, needs retry)
#
# Column format: | ID | Timestamp | Task | Status | Notes |
# ID = S{session}-{seq} (e.g. S1-001, S2-003). Timestamp = YYYY-MM-DD.
#
# When a background agent fails (rate limit, timeout, etc.), its tasks MUST be re-logged as ⏳ pending
# When a session ends, ALL incomplete tasks MUST remain here with their current status

---

## Session 1 — 2026-03-14

| ID | Timestamp | Task | Status | Notes |
|----|-----------|------|--------|-------|
| S1-001 | 2026-03-14 | Initial release — templates, /go, /audit, pre-commit hook | ✅ done | `1ced32c` |
| S1-002 | 2026-03-14 | Write README with design principles | ✅ done | `31ba431`, `63018e3` |

---

## Session 2 — 2026-03-15

| ID | Timestamp | Task | Status | Notes |
|----|-----------|------|--------|-------|
| S2-001 | 2026-03-15 | Add safeguard file existence check to /audit | ✅ done | `b21bf6b` |
| S2-002 | 2026-03-15 | Add .gitignore | ✅ done | `b21bf6b` |
| S2-003 | 2026-03-15 | Create /end skill for session wrap-up | ✅ done | `865be8f` |
| S2-004 | 2026-03-15 | Polish README wording | ✅ done | `8791521`, `6af19af`, `86fadc7` |
| S2-005 | 2026-03-15 | Rename /go to /start | ✅ done | `8663b3f` |
| S2-006 | 2026-03-15 | Update README with feedback and details | ✅ done | `a4b4f51` |
| S2-007 | 2026-03-15 | Add Itemisation Protocol — /itemise skill, CLAUDE.md toggle, README | ✅ done | `4a8adad` |

---

## Session 3 — 2026-03-20

| ID | Timestamp | Task | Status | Notes |
|----|-----------|------|--------|-------|
| S3-001 | 2026-03-20 | Create install.sh for easy setup | ✅ done | `e4ad3ce` |
| S3-002 | 2026-03-20 | Add first-run detection to /start | ✅ done | `e4ad3ce` |
| S3-003 | 2026-03-20 | Remove personal identifiers from all files | ✅ done | `e4ad3ce` |
| S3-004 | 2026-03-20 | Harden /itemise: preserve existing comments, fix CRLF verification | ✅ done | `14845db` |
| S3-005 | 2026-03-20 | Enforce Edit-only itemisation to prevent comment destruction | ✅ done | `a5586ca` |
| S3-006 | 2026-03-20 | Add cross-references, section lookup, impact advisories to /itemise | ✅ done | `aa969b5` |

---

## Session 4 — 2026-03-23

| ID | Timestamp | Task | Status | Notes |
|----|-----------|------|--------|-------|
| S4-001 | 2026-03-23 | Merge all /itemise bug fixes into canonical version | ✅ done | `f86ba82` |

---

## Session 5 — 2026-03-24

| ID | Timestamp | Task | Status | Notes |
|----|-----------|------|--------|-------|
| S5-001 | 2026-03-24 | Add consumer-generated safeguard files to .gitignore | ✅ done | `0feebea` |

---

## Session 6 — 2026-03-26/27

| ID | Timestamp | Task | Status | Notes |
|----|-----------|------|--------|-------|
| S6-001 | 2026-03-26 | Add auto-checkpoint, context overflow, save frequency protocols | ✅ done | `722e0da` |
| S6-002 | 2026-03-27 | Create /save skill for mid-session checkpoints | ✅ done | `0164267` |
| S6-003 | 2026-03-27 | Add PreCompact hook for auto-save before compaction | ✅ done | `8e7b24e` |
| S6-004 | 2026-03-27 | Clean up README for public-facing professionalism | ✅ done | `5956266` |
| S6-005 | 2026-03-27 | Add working directory mismatch detection | ✅ done | `224d71e` |
| S6-006 | 2026-03-27 | Add comparison asset images (CCG vs /init, CCG vs Auto-Memory) | ✅ done | `8811cad` |
| S6-007 | 2026-03-27 | Standardise TASK_REGISTRY.md column format + emoji status | ✅ done | `c9c8aca` — all instances synced |
| S6-008 | 2026-03-27 | Improve session handoff: Next Step, In Flight, Errors | ✅ done | `5add11b` — all instances synced |
| S6-009 | 2026-03-27 | Move Lilu safeguard files to project root | ✅ done | Standardised Lilu to match all other projects |
| S6-010 | 2026-03-27 | Remove Dev Base safeguardPath override for Lilu | ✅ done | No longer needed |
| S6-011 | 2026-03-28 | Set up CCG to track its own development | ✅ done | Safeguard files created, history reconstructed |

---

## Session 7 — 2026-03-28

| ID | Timestamp | Task | Status | Notes |
|----|-----------|------|--------|-------|
| S7-001 | 2026-03-28 | Add no-narration rule to /end skill and sync all instances | ✅ done | `22a9bc6` — synced to all 5 projects |
| S7-002 | 2026-03-28 | Fix skill discovery + slash-command enforcement + /end format | ✅ done | `825c6a1` — disable-model-invocation false, UserPromptSubmit hook, strict /end format, parent-level install, all synced |
| S7-003 | 2026-03-28 | Fix Dev Base safeguardPath for CCG (templates → root) | ✅ done | `df4bdba` — removed safeguardPath: "templates" override |
| S7-004 | 2026-03-28 | Set defaultMode: acceptEdits in /Software/ settings.local.json | ✅ done | Reduces permission prompts for file operations |

---

## Session 8 — 2026-03-30

| ID | Timestamp | Task | Status | Notes |
|----|-----------|------|--------|-------|
| S8-001 | 2026-03-30 | Fix /end executing plans instead of archiving them | ✅ done | `670227e` — save-only rule + Step 3 no-execute warning, synced to all instances |
| S8-002 | 2026-03-30 | Clean up /Software/ permissions (settings.local.json) | ✅ done | Replaced 80 specific rules with Bash(*) + acceptEdits |
| S8-003 | 2026-03-31 | Fix plan leaking between projects — content-matching in /end and /audit | ✅ done | `ef431a9` — match plans by project name in first ~500 chars, synced to all instances |
| S8-004 | 2026-03-31 | Persist /audit results to timestamped files in audits/ | ✅ done | `00c765f` — Step 10 added, audits/ gitignored, synced to all instances |

---

## Session 9 — 2026-04-01

| ID | Timestamp | Task | Status | Notes |
|----|-----------|------|--------|-------|
| S9-001 | 2026-04-01 | Fix PreCompact hook to directly back up safeguard files | ✅ done | `3723c96` — rewritten from JSON output to direct file copy |
| S9-002 | 2026-04-01 | Add rate limit awareness section to CLAUDE.md template | ✅ done | `7e37f55` — new section before CONTEXT OVERFLOW PROTOCOL |
| S9-003 | 2026-04-01 | Sync PreCompact fix to all consumer instances | ✅ done | AutoPoster, Audit for AI, Dev Base, Lilu, My number picker |
| S9-004 | 2026-04-01 | Sync rate limit awareness to all consumer instances | ✅ done | All 5 projects + parent level |
| S9-005 | 2026-04-01 | Fix missed Lilu templates/CLAUDE.md sync | ✅ done | `1809aff` — added RATE LIMIT AWARENESS + SLASH COMMAND ENFORCEMENT |

---

## Session 10 — 2026-04-04

| ID | Timestamp | Task | Status | Notes |
|----|-----------|------|--------|-------|
| S10-001 | 2026-04-04 | Create kit.md and publish bundle for JourneyKits.ai | ✅ done | kit.md created, bundle built (72KB), 24h cooldown — scheduled task for 2026-04-05 18:45 UTC |
| S10-002 | 2026-04-04 | Isolate kit files from public repo | ✅ done | .git/info/exclude, memory note saved, .gitignore reverted |
| S10-003 | 2026-04-04 | Add git commit/push to /start and /save skills | ✅ done | `1d570c3` — /start Step 2.7 commits orphaned work, /save Step 3 commits & pushes |
| S10-004 | 2026-04-04 | Sync /start and /save updates to all consumer instances | ✅ done | AutoPoster `57f308e`, Audit for AI `5fea447`, Dev Base `bc3862a`, Lilu `e7c9687`, + all other instances |
| S10-005 | 2026-04-04 | Fix merge damage from stale Lilu/CCG copy | ✅ done | `583020c` — restored install.sh, README.md, templates/CLAUDE.md, pre-compact-save.sh |
| S10-006 | 2026-04-04 | Rebuild kit bundle with updated skills | ✅ done | 72,799 bytes, includes /start and /save git commit changes |
| S10-007 | 2026-04-04 | Schedule JourneyKits publish task | ✅ done | `publish-context-guard` scheduled for 2026-04-05 18:45 UTC |
| S10-008 | 2026-04-04 | Add Waypoint AR and seeko-child to consumer instance list | ✅ done | Memory updated, D-013 logged |
