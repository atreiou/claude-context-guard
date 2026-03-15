# Claude Context Guard

**Persistent context protection for Claude Code projects.**

Stop losing work to rate limits, session restarts, and context rot. Context Guard gives Claude Code a memory system that survives across sessions — so every restart picks up exactly where you left off.

## The Problem

Claude Code sessions get cut off by rate limits, context compaction, and crashes. Each new session starts fresh with no memory of what happened before. Tasks get dropped, decisions get forgotten, and you waste time re-explaining your project.

This is a known issue. [Anthropic's own engineering team](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) documented the same failure modes and recommended external state files as the solution.

> **Note:** Context Guard is NOT the same as Claude Code's built-in "context compaction." Compaction is Claude Code's automatic process that compresses your conversation when it gets too long — it happens whether or not you have Context Guard installed. What Context Guard does is ensure that when compaction happens (or when you start a fresh session), nothing important gets lost. The `/go` command reads your safeguard files and rebuilds full context from them, so compaction becomes a non-event instead of a disaster.

## My Solution

Context Guard creates a set of safeguard files that persist across sessions, plus three slash commands:

- **`/go`** — Type this at the start of every session. Claude reads all safeguard files, cross-references recent plans against the task registry, flags any dropped or unexplained tasks, and summarises the project state. One command, full recovery.

- **`/audit`** — Your personal safeguard. Call this at ANY moment to verify Claude's work. It runs a comprehensive integrity check across all files, plans, and git state.

- **`/end`** — Optional session save point. When you're done for the day, type `/end` and Claude will update all safeguard files, commit any uncommitted work, push to remote, and report a clean summary. Not required — `/go` handles recovery regardless — but useful when you want an explicit clean handoff.

## Installation

1. Copy the `.claude/` folder into your project root
2. Copy the `templates/` folder into your project root
3. Type `/go`

That's it. On first run, `/go` detects this is a new project and sets everything up — copies templates, asks for your project name, and initialises the safeguard files.

### What Gets Created

| File | Purpose |
|------|---------|
| `CLAUDE.md` | Auto-read every session. Project rules and pointers to other files |
| `SESSION_LOG.md` | Running history of what happened each session |
| `TASK_REGISTRY.md` | Every task ever created, with status. Nothing gets dropped |
| `DECISIONS.md` | Architectural decisions register. The "why" behind every choice |
| `COMMENTS.md` | Your verbatim comments logged as a safety net |
| `FEATURE_LIST.json` | Pass/fail feature tracker (JSON — harder for LLMs to accidentally overwrite) |
| `plans/` | Archived plans from every session, cross-referenced by /go and /audit |

### What Gets Configured

| Component | Purpose |
|-----------|---------|
| `/go` skill | Session recovery — one command to restore full context |
| `/audit` skill | On-demand integrity check — verify Claude's work at any moment |
| `/end` skill | Optional session save point — clean wrap-up with commit and push |
| Pre-commit hook | Reminds Claude to update safeguard files before every git commit |

## How It Works

### Session Start (`/go`)

1. Reads all safeguard files (session log, task registry, decisions, comments, features)
2. Reads the last 3 archived plans **in full**
3. Cross-references every plan item against the task registry
4. Flags dropped tasks (in plan but not in registry) and unexplained tasks (in registry but no source)
5. Checks git state for uncommitted or unpushed work
6. Summarises everything and waits for your confirmation

### On-Demand Audit (`/audit`)

Everything `/go` does, plus:
- Checks for stale in-progress tasks
- Verifies decisions aren't contradicted
- Checks for unarchived plans
- File integrity checks
- Reports passing, warnings, and critical issues

### Session End (`/end`) — Optional

When you're ready to stop working, type `/end`. Claude will:
1. Review everything done this session
2. Update all safeguard files (session log, task registry, comments, decisions, features)
3. Archive any unarchived plans
4. Commit and push all changes
5. Verify clean git state
6. Report a summary of the session and what's pending for next time

This is entirely optional — `/go` will recover context regardless. But `/end` gives you a guaranteed clean save point.

### Pre-Commit Safety

Before every git commit, a hook reminds Claude to update:
- COMMENTS.md (any new user feedback)
- TASK_REGISTRY.md (any new or completed tasks)
- SESSION_LOG.md (if significant milestone)
- FEATURE_LIST.json (if feature status changed)
- plans/ (any unarchived plans)

## Git Conventions

Context Guard uses a tagging convention for human-readable git history:

```
S{session}-{sequence}_{short-description}
```

Examples: `S5-001_install-deps`, `S5-002_add-auth`, `S6-001_fix-login-bug`

## Design Principles

I have been building (in practice,) this and another protocol which I am not sharing, for now, for quite some time. I am not a software engineer, just an avid AI user, but with Operational Analysis skills, I have over the last 3 years built what I consider the best context-rot defense out there, without even knowing why it works. I just had to figure out how to stop the problems all the LLMs kept making, without understanding why they are making them. Of course I have learneed all of that over the last year in partuclar now and it urns out I was right, and have been validated by the following, and genuinely hope the results of my 3 years of funmbling in the dark - that probably should be written into these models as standard - helps others like it now helps me:  [Anthropic's research](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) and the [Recursive Language Models paper](https://arxiv.org/abs/2512.24601) (MIT CSAIL):

1. **External state over in-context memory** — files survive, context windows don't
2. **JSON for structured data** — LLMs are less likely to accidentally overwrite JSON than markdown
3. **Cross-referencing over trust** — verify plans against registries, don't assume tasks were completed
4. **Minimal context loading** — read indexes first, fetch specifics only when needed
5. **User can audit at any time** — transparency and accountability built in

## License

MIT
