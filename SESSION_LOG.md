# SESSION_LOG.md — Claude Context Guard Session History

---

## Session 1 — 2026-03-14 (Project Creation)

**What happened:**
- CCG born as a standalone project, extracted from Lilu's safeguard system
- Initial release v1.0: templates (CLAUDE.md, SESSION_LOG, TASK_REGISTRY, DECISIONS, COMMENTS, FEATURE_LIST), /start (then called /go), /audit skills, pre-commit hook
- README written with design principles
- Several README polish commits (wording, design principles section)

**Commits:** `1ced32c`, `31ba431`, `63018e3`
**Tasks completed:** 3 (initial release, README, design principles)
**Tasks remaining:** None

---

## Session 2 — 2026-03-15 (Skills Expansion + Itemise)

**What happened:**
- Added safeguard file existence check to /audit
- Added .gitignore
- Created /end skill for session wrap-up
- Renamed /go → /start across all instances
- Added Itemisation Protocol: /itemise skill, CLAUDE.md toggle, full README documentation
- Multiple README polish passes

**Commits:** `b21bf6b`, `865be8f`, `8791521`, `6af19af`, `86fadc7`, `8663b3f`, `a4b4f51`, `4a8adad`
**Tasks completed:** 8
**Tasks remaining:** None

---

## Session 3 — 2026-03-20 (Install Script + Itemise Hardening)

**What happened:**
- Created install.sh for easy setup
- Added first-run detection to /start (checks for {PROJECT_NAME} placeholder)
- Removed personal identifiers from all files
- Hardened /itemise: preserve existing comments, fix Windows CRLF verification
- Enforced Edit-only itemisation to prevent comment destruction
- Added cross-references, section lookup, and impact advisories to itemise

**Commits:** `e4ad3ce`, `14845db`, `a5586ca`, `aa969b5`
**Tasks completed:** 6
**Errors encountered:** Real-world testing on AutoPoster found 4 critical /itemise bugs (comment destruction, code reorganisation, verification false positives, CRLF false failures). All fixed.
**Tasks remaining:** Sync fixes to all consumer instances

---

## Session 4 — 2026-03-23 (Bug Fix Sync)

**What happened:**
- Merged all /itemise bug fixes from AutoPoster and CCG into single canonical version
- Synced to all consumer instances

**Commits:** `f86ba82`
**Tasks completed:** 1
**Tasks remaining:** None

---

## Session 5 — 2026-03-24 (Gitignore + Consumer Setup)

**What happened:**
- Added consumer-generated safeguard files to .gitignore (CLAUDE.md, SESSION_LOG, TASK_REGISTRY, DECISIONS, COMMENTS, FEATURE_LIST, plans/)
- This ensures the public repo stays clean and consumer-grade
- Installed CCG into Audit for AI project

**Commits:** `0feebea`
**Tasks completed:** 2
**Tasks remaining:** None

---

## Session 6 — 2026-03-26/27 (Major Feature Sprint)

**What happened:**
- Added auto-checkpoint, context overflow, and save frequency protocols to CLAUDE.md template
- Created /save skill for mid-session checkpoints
- Added PreCompact hook for automatic save before context compaction
- Cleaned up README for public-facing professionalism
- Added working directory mismatch detection
- Added comparison asset images (CCG vs /init, CCG vs Auto-Memory)
- Standardised TASK_REGISTRY.md column format across all instances: `| ID | Timestamp | Task | Status | Notes |` with emoji status
- Improved session handoff quality: added Next Step, In Flight, Errors to /end and /save
- Moved Lilu safeguard files from nested path to project root (standardisation)
- Set up CCG to track its own development (this file!)
- Synced all changes to all 4 consumer projects + Lilu runtime

**Commits:** `722e0da`, `0164267`, `8e7b24e`, `5956266`, `224d71e`, `8811cad`, `c9c8aca`, `5add11b`
**Tasks completed:** 11
**Errors encountered:** AutoPoster remote had new commits from GitHub Actions, causing push rejections. Fixed with `git pull --rebase` before pushing.
**Decisions made:** D-005 (public repo hygiene), D-006 (no "gold standard" term), D-007 (CCG update workflow), D-008 (standardised task registry format)
**Next step:** User considers CCG mostly complete for now. Future work is bug fixes and improvements as they come up from real-world usage.

---

## Session 7 — 2026-03-28 (Skill Discovery + Enforcement)

**What happened:**
- Added no-narration rule to /end skill (later superseded by enforcement)
- Fixed `disable-model-invocation: true` → `false` on all 5 skills — this was hiding skills from Claude's context entirely
- Created UserPromptSubmit hook (`check-slash-commands.sh`) for slash-command enforcement
- Added SLASH COMMAND ENFORCEMENT section to CLAUDE.md template and all project CLAUDE.md files
- Tightened /end Step 6 Report to exact standardised format
- Installed skills, hooks, and settings at parent `/Software/.claude/` level so "/" works from parent directory
- Synced all changes to all 5 consumer instances

**Commits:** `22a9bc6`, `825c6a1` (CCG), `26d04e3` (AutoPoster), `1eaa0f5` (Audit for AI), `65c7153`, `df4bdba` (Dev Base), `aa78566` (Lilu)
**Tasks completed:** 4 (S7-001 through S7-004)
**Errors encountered:** Skill tool returned "cannot be used due to disable-model-invocation" even after changing to false — skills are cached at conversation start and don't reload mid-session. The `/` menu also doesn't update mid-session. Both will work in the next conversation.
**Next step:** CCG is stable. User confirmed "/" menu shows all 5 skills in new conversation. No pending work.

---

## Session 8 — 2026-03-30 (Bug Fixes)

**What happened:**
- Fixed /end skill executing plans instead of archiving them — added CRITICAL save-only rule and Step 3 no-execute warning
- Synced /end fix to all instances (scanned /Software/ dynamically)
- Cleaned up /Software/ settings.local.json — replaced 80 hyper-specific permission rules with `Bash(*)` + `acceptEdits`
- Established that /Software/ working dir is for access, CCG is the home project (memory saved)

- Fixed plan leaking between projects — added content-matching (first ~500 chars) to /end and /audit
- Persisted /audit results to timestamped files in audits/ directory

**Commits:** `670227e`, `ef431a9`, `00c765f` (CCG), `e04bf83`, `309469e`, `707d9b6` (AutoPoster), `ec91cbf`, `a14105b`, `37bd021` (Audit for AI), `3d232c5`, `21d01e9`, `3a6669b` (Dev Base), `3301de9`, `cd10a4a`, `2275e53` (Lilu)
**Tasks completed:** 4 (S8-001 through S8-004)
**Next step:** CCG is stable. No pending work.

---

## Session 9 — 2026-04-01 (PreCompact Hook Fix + Rate Limit Awareness)

**What happened:**
- Investigated bug report claiming PreCompact hook doesn't fire. Found the bug report's root cause was WRONG — PreCompact IS a valid Claude Code hook event (confirmed by schema). The actual issue: PreCompact hooks have no decision control, so the script's JSON output (systemMessage/hookSpecificOutput) went nowhere.
- Rewrote `pre-compact-save.sh` to directly back up safeguard files to `compaction-backups/YYYY-MM-DD_HHMMSS/` as a side effect instead of trying to instruct Claude
- Added RATE LIMIT AWARENESS section to CLAUDE.md template — protects against mid-operation rate limit disruptions
- Synced all changes to all 5 consumer instances + parent level
- Found and fixed Lilu `templates/CLAUDE.md` being out of sync (missing SLASH COMMAND ENFORCEMENT and RATE LIMIT AWARENESS)
- Verified public repo is clean of all private info

**Commits:** `3723c96` (hook fix), `7e37f55` (rate limit awareness)
**Consumer syncs:** AutoPoster, Audit for AI, Dev Base, Lilu (`ae434c0`, `1809aff`), My number picker (local only)
**Tasks completed:** 5 (S9-001 through S9-005)
**Errors encountered:** Initial plan was to remove PreCompact entirely based on bug report. Schema validation revealed PreCompact IS valid — reverted all changes before committing and investigated the real cause instead.
**Decisions made:** D-010 (PreCompact hook backs up files directly, not via Claude instructions)
**Next step:** CCG is stable. No pending work.

---

## Session 10 — 2026-04-04 (JourneyKits Publish + /start & /save Git Fix)

**What happened:**
- Continued JourneyKits.ai publishing from Session 9 (context compaction). kit.md was already created. Built the publish bundle JSON (72KB), hit 24h email verification cooldown — scheduled task for 2026-04-05 18:45 UTC
- User directed that kit files (kit.md, publish_kit.py, kit_bundle.json) are local-only — must never touch the public repo. Moved from .gitignore (tracked!) to .git/info/exclude (local-only). Memory note saved.
- Implemented /start and /save git commit/push per bug report from seeko-child: /start now commits orphaned work from crashed sessions (Step 2.7); /save now commits & pushes as Step 3
- Synced to all consumer instances: AutoPoster, Audit for AI, Dev Base, Waypoint AR, Lilu (runtime + build-time), Socials.club (parent + CCG copy), /Software/ parent
- Fixed merge damage: Lilu/claude-context-guard had stale versions that overwrote 4 public repo files (install.sh, README.md, templates/CLAUDE.md, pre-compact-save.sh) via a merge. Restored from correct commit and pushed fix.
- Rebuilt kit bundle with updated /start and /save skills
- Added Waypoint AR and seeko-child (via Socials.club parent) to permanent consumer instance list

**Commits:** `1d570c3` (skill updates), `583020c` (merge fix)
**Consumer syncs:** AutoPoster `57f308e`, Audit for AI `5fea447`, Dev Base `bc3862a`, Lilu `e7c9687`, all other instances via copy
**Tasks completed:** 8 (S10-001 through S10-008)
**Errors encountered:** Lilu/claude-context-guard shares the public remote (atreiou/claude-context-guard). An automated sync agent committed and merged there, pulling in stale file versions that overwrote rate limit awareness, slash command enforcement, parent-dir detection, and more. Fixed by restoring from the correct commit. Memory updated with warning about shared-remote repos.
**Decisions made:** D-011 (/start and /save must commit/push), D-012 (kit files local-only), D-013 (expanded consumer instance list)
**Next step:** JourneyKits publish scheduled for 2026-04-05 18:45 UTC. CCG is otherwise stable. No pending work.
