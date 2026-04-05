# DECISIONS.md — Claude Context Guard Architectural Decisions Register
# NEVER CONTRADICT THESE DECISIONS WITHOUT EXPLICIT USER APPROVAL
# These are the "why" behind every major choice. Summaries lose the "why" — this file preserves it.

---

## D-001: External state over in-context memory (2026-03-14)
**Decision:** All project state lives in files (SESSION_LOG.md, TASK_REGISTRY.md, etc.), not in conversation context.
**Rationale:** Context windows are ephemeral. Files survive across sessions, compactions, and agent restarts.
**Source:** Initial design, inspired by Anthropic article on long-running agent harnesses.

## D-002: Itemisation Protocol uses Edit tool only (2026-03-20)
**Decision:** /itemise must use the Edit tool, never Write, to modify existing files.
**Rationale:** Write tool replaces entire file content, which destroyed existing comments during real-world testing on AutoPoster. Edit tool applies surgical diffs.
**Source:** Session 3 bug fix after comment destruction incident.

## D-003: 500-line threshold for sub-agent delegation (2026-03-20)
**Decision:** Files over 500 lines should use sub-agent delegation during itemisation.
**Rationale:** Large files exceed reliable single-pass editing. Battle-tested on AutoPoster.
**Source:** Session 3, enchanted-puzzling-ladybug plan.

## D-004: Consumer safeguard files are gitignored (2026-03-24)
**Decision:** CLAUDE.md, SESSION_LOG.md, TASK_REGISTRY.md, DECISIONS.md, COMMENTS.md, FEATURE_LIST.json, and plans/ are excluded from the public repo via .gitignore.
**Rationale:** These are consumer-generated content. The public repo must be clean and consumer-grade.
**Source:** Session 5, user decision.

## D-005: Public repo must be consumer-grade at all times (2026-03-27)
**Decision:** Never commit development plans, private info, internal notes, or session history to the public repo. Anyone checking out the codebase should see only clean, neutral, professional content.
**Rationale:** User explicitly stated including private/development content would be a "bad failure of professionalism."
**Source:** Session 6, user directive.

## D-006: Never use "gold standard" to describe CCG (2026-03-27)
**Decision:** Use "source of truth" instead. CCG is always improving; "gold standard" implies a finished benchmark.
**Rationale:** User flagged the term as misleading and asked for removal.
**Source:** Session 6, user correction.

## D-007: CCG update workflow is automatic (2026-03-27)
**Decision:** After any CCG improvement: fix in public repo → push → sync ALL consumer instances (AutoPoster, Audit for AI, Dev Base, Lilu build-time + runtime) → commit/push each. Do not wait to be asked.
**Rationale:** User got tired of repeatedly asking for instance syncing.
**Source:** Session 6, user directive.

## D-008: Standardised TASK_REGISTRY.md format (2026-03-27)
**Decision:** All TASK_REGISTRY.md files must use: `| ID | Timestamp | Task | Status | Notes |` with `S{session}-{seq}` IDs and emoji status (✅🔄⏳❌🔁).
**Rationale:** Three projects had invented three different column formats because the template never defined one. Standardised to prevent future divergence.
**Source:** Session 6, user-reported bug.

## D-009: Skills must be invokable — disable-model-invocation: false (2026-03-28)
**Decision:** All CCG skills use `disable-model-invocation: false`. A UserPromptSubmit hook (`check-slash-commands.sh`) and CLAUDE.md enforcement section ensure slash commands are always invoked via the Skill tool. Parent-level `/Software/.claude/` install ensures skills are discoverable regardless of launch directory.
**Rationale:** `disable-model-invocation: true` removed skill descriptions from Claude's context entirely, so Claude didn't know skills existed and couldn't invoke them. Skills also need to be at the working directory level to appear in "/". Defence in depth: hook + CLAUDE.md instruction + correct flag.
**Source:** Session 7, user-reported bug + Dev Base incident (S4-CCG-improvement_slash-command-enforcement.md).

## D-010: PreCompact hook backs up files directly, not via Claude instructions (2026-04-01)
**Decision:** The PreCompact hook script copies safeguard files to `compaction-backups/YYYY-MM-DD_HHMMSS/` as a direct side effect. It does NOT output JSON instructions for Claude. PreCompact hooks have no decision control — stdout goes nowhere useful.
**Rationale:** The original script output JSON with `systemMessage` and `hookSpecificOutput` trying to instruct Claude to save, but PreCompact hooks fire for side effects only. The JSON was silently ignored, giving false confidence.
**Source:** Session 9, bug report from Dev Base S8 where compaction occurred with no auto-save.

## D-011: /start and /save must commit and push to git (2026-04-04)
**Decision:** /start commits orphaned uncommitted work from crashed sessions (new Step 2.7). /save includes git commit & push (new Step 3) to create durable checkpoints. Only /end previously did git operations, which meant context overflows left work uncommitted indefinitely.
**Rationale:** Real-world usage showed 4 consecutive sessions overflowing before /end could run, accumulating 2,060+ lines of uncommitted changes. /save's whole point is creating a save point — without git, it wasn't durable.
**Source:** Session 10, bug report from seeko-child project.

## D-012: Kit files are local-only, never in public repo (2026-04-04)
**Decision:** kit.md, publish_kit.py, and kit_bundle.json are excluded via `.git/info/exclude` (local-only). They must never be added to .gitignore (which is tracked) or committed to the public repo.
**Rationale:** The public repo is for Context Guard as a standalone open-source project. JourneyKits is a separate distribution channel. Adding kit references to .gitignore would leak internal info.
**Source:** Session 10, user directive.

## D-013: Consumer instance list expanded (2026-04-04)
**Decision:** The D-007 sync workflow now covers: AutoPoster, Audit for AI, Dev Base, Waypoint AR, Lilu (runtime), Lilu/claude-context-guard (build-time, shares public remote), Socials.club (parent level, covers seeko-child), Socials.club/Claude Context Guard (shares public remote), /Software/ parent level. Lilu/CCG and Socials.club/CCG share the public remote — only pull from upstream, never commit divergent content.
**Rationale:** Two new projects added (seeko-child via Socials.club, Waypoint AR). A stale Lilu/CCG copy caused a merge that overwrote 4 public repo files during this session — shared-remote repos must be treated with care.
**Source:** Session 10, user directive + merge incident.
