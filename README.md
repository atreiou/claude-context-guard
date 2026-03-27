# Claude Context Guard

**Persistent context protection for Claude Code projects.**

Stop losing work to rate limits, session restarts, and context rot. Context Guard gives Claude Code a memory system that survives across sessions — so every restart picks up exactly where you left off.

## The Problem

Claude Code sessions get cut off by rate limits, context compaction, and crashes. Each new session starts fresh with no memory of what happened before. Tasks get dropped, decisions get forgotten, and you waste time re-explaining your project.

This is a known issue. [Anthropic's own engineering team](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) documented the same failure modes and recommended external state files as the solution.

> **Note:** Context Guard is NOT the same as Claude Code's built-in "context compaction." Compaction is Claude Code's automatic process that compresses your conversation when it gets too long — it happens whether or not you have Context Guard installed. What Context Guard does is ensure that when compaction happens (or when you start a fresh session), nothing important gets lost. The `/start` command reads your safeguard files and rebuilds full context from them, so compaction becomes a non-event instead of a disaster. There should now be an option to stop their auto-compaction as it just happends randomly and is annoyingand no longer needed. To be fair though, all the LLMs should now just have thie Context Guard or similar, built in. I'm actually quite surprised that they still haven't figured this out and rely on compaction. I guess that's what happens when you let an Operational Analyst near AI, not a coder. ;p

## My Solution

Context Guard creates a set of safeguard files that persist across sessions, plus five slash commands:

- **`/start`** — Type this at the start of every session. Claude reads all safeguard files, cross-references recent plans against the task registry, flags any dropped or unexplained tasks, and summarises the project state. One command, full recovery.

- **`/audit`** — Your personal safeguard. Call this at ANY moment to verify Claude's work. It runs a comprehensive integrity check across all files, plans, and git state.

- **`/save`** — Mid-session checkpoint. Saves all progress to safeguard files without git operations. Use during long sessions or any time you want an explicit save point.

- **`/end`** — Optional session save point. When you're done for the day, type `/end` and Claude will update all safeguard files, commit any uncommitted work, push to remote, and report a clean summary. Not required — `/start` handles recovery regardless — but useful when you want an explicit clean handoff.

- **`/itemise`** — Apply the Itemisation Protocol to your code files. Numbers sections, functions, and meaningful blocks so every part of the code is referenceable by address. Backs up files first, verifies nothing changed except the added numbers, then removes backups. Can be toggled off in `CLAUDE.md` for projects that don't want it.

## Installation

### Option 1: One-Command Install

```bash
git clone https://github.com/atreiou/claude-context-guard.git
cd claude-context-guard
./install.sh /path/to/your/project
```

> **Windows users:** Run this in Git Bash or WSL, not PowerShell or CMD.

### Option 2: Manual Install

1. Copy the `.claude/` folder into your project root
2. Copy the `templates/` folder into your project root

### First Run

Open Claude Code in your project and type `/start`. On first run, it will:
1. Detect this is a new project (no safeguard files yet)
2. Ask for your project name and description
3. Create all safeguard files from the templates
4. Offer to run `/itemise` for numbered code addressing (optional)

From then on, `/start` reads your existing safeguard files and recovers full context — one command, full recovery.

### What Gets Created

| File | Purpose |
|------|---------|
| `CLAUDE.md` | Auto-read every session. Project rules and pointers to other files |
| `SESSION_LOG.md` | Running history of what happened each session |
| `TASK_REGISTRY.md` | Every task ever created, with status. Nothing gets dropped |
| `DECISIONS.md` | Architectural decisions register. The "why" behind every choice |
| `COMMENTS.md` | Your verbatim comments logged as a safety net |
| `FEATURE_LIST.json` | Pass/fail feature tracker (JSON — harder for LLMs to accidentally overwrite) |
| `plans/` | Archived plans from every session, cross-referenced by /start and /audit |

### What Gets Configured

| Component | Purpose |
|-----------|---------|
| `/start` skill | Session recovery — one command to restore full context |
| `/audit` skill | On-demand integrity check — verify Claude's work at any moment |
| `/save` skill | Mid-session checkpoint — update safeguard files without git operations |
| `/end` skill | Optional session save point — clean wrap-up with commit and push |
| `/itemise` skill | Itemisation Protocol — numbered code addressing with backup and integrity verification |
| Pre-commit hook | Reminds Claude to update safeguard files before every git commit |
| Pre-compaction hook | Automatically saves all progress before context compression — no data loss |

## How It Works

### Session Start (`/start`)

1. Reads all safeguard files (session log, task registry, decisions, comments, features)
2. Reads the last 3 archived plans **in full**
3. Cross-references every plan item against the task registry
4. Flags dropped tasks (in plan but not in registry) and unexplained tasks (in registry but no source)
5. Checks git state for uncommitted or unpushed work
6. Summarises everything and waits for your confirmation

### On-Demand Audit (`/audit`)

Everything `/start` does, plus:
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

This is entirely optional — `/start` will recover context regardless. But `/end` gives you a guaranteed clean save point.

### Mid-Session Checkpoint (`/save`)

A lightweight save point you can run at any time during a session. Claude will:
1. Check for any unlogged comments, tasks, or decisions
2. Update all safeguard files with current progress
3. Add a checkpoint marker to the session log
4. Confirm what was saved

No git operations, no plan archiving — just a quick save. Use it when a session is running long, before a risky operation, or any time you want peace of mind.

### Itemisation Protocol (`/itemise`)

The Itemisation Protocol adds hierarchical section numbers to code files, making every block referenceable by address. Instead of loading an entire file into context, you can say "check section 2.3.1" and point directly to the relevant code.

Numbers are added as comments using the correct syntax for each language:

```php
// 1. SECTION: Enqueue Scripts and Styles

// 1.1 Enqueue parent theme stylesheet
add_action('wp_enqueue_scripts', function() {
    wp_enqueue_style('parent-style', get_template_directory_uri() . '/style.css');
});
// end of 1.1

// 1.2 Conditional enqueue for calendar assets
add_action('wp_enqueue_scripts', function() {
    if (is_page('book-now') || is_page('booking-confirmation')) {
        wp_enqueue_style('app-calendar', get_stylesheet_directory_uri() . '/app-calendar.css');
        wp_enqueue_script('app-calendar-js', get_stylesheet_directory_uri() . '/app-calendar.js', [], null, true);

        // 1.2.1 Localise script with AJAX URL, nonce, and slot config
        wp_localize_script('app-calendar-js', 'appData', array(
            'ajaxUrl'    => admin_url('admin-ajax.php'),
            'nonce'      => wp_create_nonce('app_booking_nonce'),
            // 1.2.1.1 Slot config: array of {label, start_h, start_m, end_h, end_m} objects
            'slotConfig' => get_slot_config(),
        ));
    }
});
// end of 1.2

// end of 1
```

**What gets numbered:** sections, functions, significant conditionals, important loops, key config objects.
**What doesn't:** variable declarations, single-line assignments, imports, trivial boilerplate.
**Depth:** aim for 3 levels (`1.2.3`) in most cases, 4 only for genuinely complex nested config.

**To disable:** set `ITEMISATION: disabled` in your project's `CLAUDE.md`. The `/itemise` command will halt before making any changes. Many developers won't want or need this protocol — the toggle is prominently placed at the top of the Itemisation Protocol section in `CLAUDE.md`.

**Safety:** `/itemise` creates `{filename}.itemise-backup` copies before touching anything, verifies integrity after (strips added comment-numbers and diffs against the backup to confirm no code changed), and restores from backup on any failure.

### Automatic Pre-Compaction Save

When Claude Code is about to compress your conversation (context compaction), a `PreCompact` hook fires automatically. You'll see a notification: **"Context Guard — Auto-saving before compaction."** Claude is then instructed to update all safeguard files before compaction proceeds — capturing everything from the session that would otherwise be lost to compression.

This means you never have to worry about a long session being silently compacted without your progress being saved. Context Guard catches it for you.

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

I have been building (in practice,) this and another protocol which I am not sharing, for now, for quite some time. I am not a software engineer, just an avid AI user, but with Operational Analysis skills, I have over the last 3 years built what I consider the best context-rot defense out there, without even knowing why it works. I just had to figure out how to stop the problems all the LLMs kept making, without understanding why they are making them. Of course I have learneed all of that over the last year in particular now and it turns out I was right, and have been validated by the following, and genuinely hope the results of my 3 years of funmbling in the dark - that probably should be written into these models as standard - helps others like it now helps me: [Anthropic's research](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) and the [Recursive Language Models paper](https://arxiv.org/abs/2512.24601) (MIT CSAIL):

1. **External state over in-context memory** — files survive, context windows don't
2. **JSON for structured data** — LLMs are less likely to accidentally overwrite JSON than markdown
3. **Cross-referencing over trust** — verify plans against registries, don't assume tasks were completed
4. **Minimal context loading** — read indexes first, fetch specifics only when needed
5. **User can audit at any time** — transparency and accountability built in
6. **Referenceable code** — every block has an address, LLMs don't need full file context to find it

## License

MIT
