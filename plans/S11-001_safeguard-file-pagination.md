# Plan: Safeguard File Pagination

## Context

Safeguard files grow indefinitely. Every /start reads ALL of them in full — SESSION_LOG.md, TASK_REGISTRY.md, DECISIONS.md, COMMENTS.md, FEATURE_LIST.json. Real-world sizes already proving the problem:

- Dev Base: SESSION_LOG 377 lines, TASK_REGISTRY 205 lines
- Waypoint AR: SESSION_LOG 196 lines, TASK_REGISTRY **603 lines**

That's 800+ lines of context consumed just reading safeguard files in one project. As projects age, this will only get worse — killing context window budget before any actual work begins.

**Solution:** Introduce automatic file pagination. When a safeguard file exceeds a line threshold, /save and /end archive older content into numbered page files. The agent has full context at save/end time, so it can make intelligent decisions about what to archive. /start then only reads the trimmed current files, with archive references for when deeper history is needed.

## Design

### Naming Convention
- `SESSION_LOG.md` — always the current/active file (most recent content)
- `SESSION_LOG_page1.md` — oldest archive
- `SESSION_LOG_page2.md` — next oldest archive
- Same pattern for TASK_REGISTRY, DECISIONS, COMMENTS

### Threshold: 300 lines
- Below 300 lines: no action needed
- Above 300 lines: rotate older content into a new page file

### Split Strategy (per file type)

**SESSION_LOG.md:**
- Split on `## Session N` headers
- Keep the **last 3 sessions** in the main file
- Move everything before → next numbered page file

**TASK_REGISTRY.md:**
- Split on `## Session N` headers
- Keep **all non-done tasks** (⏳ pending, 🔄 in-progress, ❌ blocked, 🔁 re-queued) regardless of age — these ALWAYS stay in the main file
- Keep **last 3 sessions of done tasks** for cross-referencing
- Archive older done tasks → next numbered page file

**DECISIONS.md:**
- Archive only **actioned decisions** — decisions that have been fully implemented and are no longer actively constraining current work
- Keep all **active/unactioned decisions** in the main file regardless of age
- The agent (which has full context at save/end time) decides which are actioned
- Move actioned decisions → page file

**COMMENTS.md:**
- Archive **actioned comments** — comments that have been turned into decisions, tasks, or file changes
- Archive **curiosity questions** — user questions that were just exploratory/informational, not directives about the project itself
- Keep all **unactioned project directives** in the main file regardless of age
- The agent (which has full context at save/end time) decides which fall into each category
- Move archived comments → page file

**FEATURE_LIST.json:**
- No pagination — stays compact by nature

### Archive File Header

Each archive gets a header noting its coverage:
```
# SESSION_LOG — Archive Page 1 (Sessions 1–15)
# Current sessions: see SESSION_LOG.md
# ---
[archived content]
```

### Main File Header Update

After rotation, the main file gets a reference line after the existing header:
```
# 📁 Archives: SESSION_LOG_page1.md, SESSION_LOG_page2.md
```

### When Pagination Runs

**During /save and /end** — after updating safeguard files (Step 2 in both skills), before git commit. This is the right time because:
- The agent has full session context and can make smart archival decisions
- It knows which comments/decisions are actioned vs still active
- /start then benefits from pre-trimmed files without needing to make those judgements with zero context

### Archive Referencing

/start, /audit, and any debugging workflow can reference archives when needed:
- /start Step 1 mentions archives exist: "📁 N archive pages available — read if historical context needed"
- /audit cross-references current-page tasks against recent plans; notes archives exist as INFO
- If something seems missing or confusing during any session, the agent should check the archive pages

## Files to Modify

### 1. `/save` SKILL.md — Add Step 2.5 "Rotate Safeguard Files"
After Step 2 (Update Safeguard Files), before Step 3 (Git Commit & Push):
- Count lines in each safeguard file
- If any exceeds 300 lines, execute the split strategy for that file type
- Create the page file with archived content + header
- Trim the main file to keep only recent content + add archive reference
- For DECISIONS.md and COMMENTS.md: use session context to identify actioned entries

### 2. `/end` SKILL.md — Add Step 2.5 "Rotate Safeguard Files"
Same logic as /save Step 2.5, placed after Step 2 (Update Safeguard Files), before Step 3 (Archive Plans).

### 3. `/start` SKILL.md — Add archive awareness to Step 1
- After reading each safeguard file, check for `_page*.md` files
- If archives exist, note them in the summary: "📁 N archive pages available for [file]"
- Do NOT read archives by default — only if cross-referencing reveals gaps
- Add a note in Step 3 (Cross-Reference Plans): if a task referenced in a plan isn't found in the current TASK_REGISTRY, check archive pages before flagging as DROPPED

### 4. `/audit` SKILL.md — Add archive awareness
- Check 8 (Safeguard File Existence): verify page files are well-formed if they exist
- Check 3 (Plan Cross-Reference): check archives for tasks before flagging DROPPED
- Add INFO note when archives exist

### 5. `/itemise` SKILL.md — No changes needed

### 6. `templates/CLAUDE.md` — Add pagination section
- Brief note under "CRITICAL: READ THESE FILES FIRST" about archive pages
- Note that archives are for reference, not auto-read

### 7. After CCG source of truth is updated:
- Push to public repo (main branch)
- Push to private backup (dev branch)
- Sync ALL consumer instances per the registry
- Commit/push each

## Verification

1. After implementation, manually check: Dev Base SESSION_LOG (377 lines) would trigger rotation on next /save or /end
2. Verify the rotation logic correctly identifies `## Session N` split points
3. Verify TASK_REGISTRY rotation preserves all non-done tasks in main file
4. Verify DECISIONS/COMMENTS rotation is context-aware (only archives actioned entries)
5. Verify /start reads trimmed files and notes archive existence
6. Verify /audit checks archives before flagging DROPPED tasks
