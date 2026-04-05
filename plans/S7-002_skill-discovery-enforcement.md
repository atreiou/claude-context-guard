# Plan: Fix CCG skill discovery, slash-command enforcement, and /end format standardisation

## Context

Four related issues with CCG skills:

1. **Skills don't show in "/" menu (parent directory)** — Claude Code is launched from `/Software/` (parent directory) but skills are installed in each project's `.claude/skills/`. Claude Code discovers skills from the working directory's `.claude/skills/` — since `/Software/.claude/skills/` doesn't exist, "/" shows nothing.

2. **`disable-model-invocation: true` hides skills from Claude** — All 5 skills have this flag set. Per Claude Code docs, this removes the skill description from Claude's context entirely. Claude doesn't know the skills exist. When the user types "/end" inside a message, Claude can't use the Skill tool (blocked by the flag) and doesn't even know it should. Fix: set to `false` — the risk of Claude auto-triggering `/end` is negligible compared to the cost of it not knowing skills exist.

3. **Slash commands not enforced** — Even when skills are discoverable, Claude sometimes treats `/end` as natural language and manually replicates steps (badly) instead of invoking the Skill tool. This caused a critical incident in Dev Base: 23 files left uncommitted, cross-device divergence, merge conflicts. Documented in `Dev Base/plans/S4-CCG-improvement_slash-command-enforcement.md`. Fix: UserPromptSubmit hook + CLAUDE.md enforcement section (defence in depth).

4. **Inconsistent /end summary format** — The Step 6 "Report" template in `/end` SKILL.md uses loose placeholders (`[bullet list]`, `[count]`) that different Claude instances interpret differently. Fix: tighten the template with exact formatting rules.

## Changes

### 0. Set `disable-model-invocation: false` on all 5 skills

Change the frontmatter in all SKILL.md files:
- `.claude/skills/start/SKILL.md` — `disable-model-invocation: false`
- `.claude/skills/end/SKILL.md` — `disable-model-invocation: false`
- `.claude/skills/audit/SKILL.md` — `disable-model-invocation: false`
- `.claude/skills/save/SKILL.md` — `disable-model-invocation: false`
- `.claude/skills/itemise/SKILL.md` — `disable-model-invocation: false`

This puts skill descriptions back into Claude's context so it knows they exist, and allows the Skill tool to invoke them. Combined with the CLAUDE.md enforcement section (Change 2), Claude will always use the Skill tool rather than manually replicating steps.

### 1. Install skills + hooks at parent `/Software/` level

Copy the 5 skills and 2 hooks from CCG source to `/Software/.claude/`:
- `/Software/.claude/skills/{start,end,audit,save,itemise}/SKILL.md`
- `/Software/.claude/hooks/{pre-commit-check.sh,pre-compact-save.sh}`
- `/Software/.claude/settings.json` (hook configuration)

This makes "/" work when Claude Code is launched from `/Software/`.

**Note:** This also means syncing CCG updates must include the parent level going forward. Update D-007 workflow.

### 2. Add UserPromptSubmit hook for slash-command enforcement

**New file: `.claude/hooks/check-slash-commands.sh`**

Bash script (not Node — keeps dependencies minimal) that:
1. Reads the user's prompt from stdin (JSON with `user_message` field)
2. Scans for `/word` patterns at start of message or after whitespace
3. Checks if the word matches an installed skill name in `.claude/skills/`
4. If match found, outputs a reminder to stderr:
   ```
   SLASH COMMAND DETECTED: /{skill}. You MUST invoke this via the Skill tool.
   Do NOT manually replicate the skill's steps. Use: Skill(skill="{skill}")
   ```

**Settings.json update:**
Add `UserPromptSubmit` hook entry pointing to the script.

**Templates/CLAUDE.md update:**
Add a `## SLASH COMMAND ENFORCEMENT` section (Option C from the Dev Base plan — defence in depth):
```markdown
## SLASH COMMAND ENFORCEMENT
When the user types a message containing `/word` where `word` matches a skill name in `.claude/skills/`,
you MUST invoke it via the Skill tool. NEVER manually replicate skill steps.
Skills exist because manual replication is error-prone and incomplete.
```

### 3. Tighten /end Step 6 "Report" format

Replace the loose template with strict formatting rules. Change from vague placeholders to explicit structure with a "copy this exactly" instruction:

```markdown
## Step 6: Report

Present the session summary in EXACTLY this format. Do not vary the structure, headings, or field names:

\`\`\`
## Session [N] — Save Point

**What was done:** [1-2 sentence summary of the session's main accomplishments]

**Tasks:** [X] done, [Y] pending, [Z] in progress
- Pending: [list task IDs and names, or "None"]
- In progress: [list task IDs and names, or "None"]

**Commits:** [list of commit hashes, or "None — working tree clean"]

**Repos pushed:**
- [repo name]: [commit hash] ✅ (or ❌ if not pushed, with reason)

**Next session:** [What /start will find. User's stated intent for next session, or "No pending work."]
\`\`\`

Do not add extra sections. Do not add "Files Modified" unless the session had no commits (uncommitted work needs visibility). Keep it scannable — this is a status report, not a narrative.
```

## Files to modify

| # | File | Action |
|---|------|--------|
| 1 | `Claude Context Guard/.claude/skills/*/SKILL.md` (all 5) | **EDIT** — set `disable-model-invocation: false` |
| 2 | `Claude Context Guard/.claude/hooks/check-slash-commands.sh` | **NEW** — slash command detection script |
| 3 | `Claude Context Guard/.claude/settings.json` | **EDIT** — add UserPromptSubmit hook |
| 4 | `Claude Context Guard/templates/CLAUDE.md` | **EDIT** — add SLASH COMMAND ENFORCEMENT section |
| 5 | `Claude Context Guard/.claude/skills/end/SKILL.md` | **EDIT** — tighten Step 6 Report format + remove no-narration rule (now redundant, enforcement handles it) |
| 6 | `Claude Context Guard/install.sh` | **REVIEW** — verify it already handles parent install (it does, no change needed) |

Then sync ALL changes to:
- `/Software/.claude/` (parent level — skills, hooks, settings)
- AutoPoster, Audit for AI, Dev Base, Lilu (build-time), Lilu (runtime) — skills, hooks, settings
- All 5 project CLAUDE.md files — add SLASH COMMAND ENFORCEMENT section to each

And update CCG's own CLAUDE.md (local, gitignored) to document the new workflow including parent-level syncing.

## Verification

1. Check `/Software/.claude/skills/` exists with all 5 skills
2. Type `/` in Claude Code launched from `/Software/` — should show skills
3. Read the UserPromptSubmit hook — confirm it detects `/end`, `/start`, etc.
4. Read updated /end SKILL.md — confirm Step 6 has strict format
5. Read updated templates/CLAUDE.md — confirm enforcement section present
6. All repos committed and pushed clean
