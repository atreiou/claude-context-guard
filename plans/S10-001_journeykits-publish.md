# Plan: Publish Context Guard as a Journey Kit

## Context

The user wants to publish Context Guard to [journeykits.ai](https://www.journeykits.ai). API key provided with agent name "lilu", `kits:write` scope, email verified.

**CRITICAL branding:** The kit is called **"Context Guard"** — NOT "Claude Context Guard" or "CCG". The principle works with ANY LLM agent, not just Claude. The current implementation uses Claude Code and CLAUDE.md as an example, but any agent that can use skills can use Context Guard. The kit description must make this LLM-agnostic positioning clear.

## What a Journey Kit requires

A kit is a JSON **bundle** with these parts:
- **manifest** — structured metadata (slug, title, summary, version, model, tags, tools, skills, inputs, outputs, failuresOvercome, fileManifest, etc.)
- **kitDoc** — a `kit.md` markdown file with YAML frontmatter + required sections (Goal, When to Use, Setup, Steps, Constraints, Safety Notes)
- **skillFiles** — reusable agent instructions (our 5 SKILL.md files)
- **toolFiles** — setup notes, operational guidance
- **srcFiles** — tested source code (hooks, settings.json, install.sh, templates)
- **examples** — sanitized example usage

Publishing flow: `POST /api/kits/import` with the bundle → auto-creates a release if quality scores pass (security ≥ 6, completeness ≥ 5).

## Implementation

### Step 1: Create kit.md

Write `Claude Context Guard/kit.md` with YAML frontmatter and required body sections:

**Frontmatter:**
```yaml
schema: "kit/1.0"
slug: "context-guard"
title: "Context Guard"
summary: "Persistent context protection for AI coding agents — safeguard files survive sessions, rate limits, and compaction."
version: "1.0.0"
license: "MIT"
tags: ["context", "memory", "persistence", "session-management", "agent-workflow"]
model:
  provider: anthropic
  name: claude-opus-4-6
  hosting: "cloud API — requires ANTHROPIC_API_KEY"
selfContained: true
environment:
  runtime: "Any AI coding agent with skill support"
  os: "cross-platform (macOS, Linux, Windows via Git Bash)"
  platforms: ["claude-code"]
  adaptationNotes: "The reference implementation uses Claude Code and CLAUDE.md. To adapt for other agents, replace CLAUDE.md with your agent's instruction file and map the 5 skills to your agent's skill/command system."
tools:
  - name: "pre-commit-check"
    description: "Pre-commit hook reminding the agent to update safeguard files"
  - name: "pre-compact-save"
    description: "PreCompact hook backing up safeguard files before context compaction"
  - name: "check-slash-commands"
    description: "UserPromptSubmit hook enforcing skill invocation for slash commands"
skills:
  - name: "start"
    description: "Session recovery — reads all safeguard files, cross-references plans, flags dropped tasks"
  - name: "end"
    description: "Session save point — updates safeguard files, commits, pushes, reports summary"
  - name: "audit"
    description: "On-demand integrity check — verifies all files, plans, git state, task registry"
  - name: "save"
    description: "Mid-session checkpoint — updates safeguard files without git operations"
  - name: "itemise"
    description: "Itemisation Protocol — adds hierarchical section numbers to code files"
inputs:
  - name: "project-name"
    description: "Name of the project to protect"
  - name: "project-description"
    description: "Brief description of the project"
outputs:
  - name: "safeguard-files"
    description: "SESSION_LOG.md, TASK_REGISTRY.md, DECISIONS.md, COMMENTS.md, FEATURE_LIST.json"
  - name: "session-recovery"
    description: "Full context recovery via /start at any session start"
failures:
  - problem: "Context lost after rate limits or session restarts"
    resolution: "External safeguard files persist across sessions; /start recovers full context"
    scope: "core"
  - problem: "Tasks dropped between sessions"
    resolution: "TASK_REGISTRY.md with cross-referencing ensures nothing is lost"
    scope: "core"
  - problem: "Context compaction loses work mid-session"
    resolution: "PreCompact hook backs up safeguard files; auto-checkpoint protocol keeps files current"
    scope: "core"
prerequisites:
  - name: "git"
    check: "git --version"
verification:
  command: "ls .claude/skills/start/SKILL.md && echo 'Context Guard installed'"
```

**Body sections:**
- **Goal:** Prevent data loss across AI agent sessions. The principle — external state files that survive context windows — works with any LLM. The reference implementation targets Claude Code.
- **When to Use:** Any project where an AI coding agent works across multiple sessions and you need continuity.
- **Setup:** install.sh or manual copy.
- **Steps:** The 5 slash commands (/start, /end, /audit, /save, /itemise).
- **Constraints:** Reference implementation uses Claude Code; adaptable to any agent with skill support.
- **Safety Notes:** No credentials in safeguard files; consumer-generated files are gitignored.

### Step 2: Build the publish bundle JSON

Construct the bundle with:
- `manifest` — from the frontmatter fields above, plus `fileManifest` entries for every srcFile
- `kitDoc` — the kit.md content
- `skillFiles` — the 5 SKILL.md files (`start/SKILL.md`, `end/SKILL.md`, `audit/SKILL.md`, `save/SKILL.md`, `itemise/SKILL.md`)
- `toolFiles` — empty (no separate ops guides needed)
- `srcFiles` — hooks (3 .sh files), settings.json, install.sh, all template files
- `examples` — empty or a brief example session
- `assets` — empty

### Step 3: Sanitize

Before publishing, scrub ALL content for:
- No personal paths (`C:\Users\robgr\...`)
- No personal email/usernames
- No consumer project names (AutoPoster, Dev Base, Lilu, etc.)
- No API keys or tokens
- Templates use `{PROJECT_NAME}` placeholders (already clean)
- No "Claude Context Guard" or "CCG" in the kit — use "Context Guard" throughout
- Make it clear the principle is LLM-agnostic; Claude Code is just the reference implementation

### Step 4: Publish via API

```
POST https://www.journeykits.ai/api/kits/import
Authorization: Bearer <api-key>
Content-Type: application/json

{
  "bundle": { <bundle object> },
  "author": "lilu",
  "visibility": "public",
  "skipRelease": false
}
```

### Step 5: Verify

```
GET https://www.journeykits.ai/api/kits/search?q=context-guard
```

Confirm the kit is discoverable and installable.

## Files to create/modify

| # | File | Action |
|---|------|--------|
| 1 | `Claude Context Guard/kit.md` | **CREATE** — kit.md with frontmatter + body |
| 2 | (none on disk) | **API call** — build bundle JSON in memory, POST to /api/kits/import |

The kit.md file will also be committed to the CCG repo so it lives alongside the project.

## Verification

1. API returns `revisionId` and `release` with status
2. `GET /api/kits/search?q=context-guard` returns the kit
3. Kit is visible at `https://www.journeykits.ai/browse/lilu/context-guard`
