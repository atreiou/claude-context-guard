#!/usr/bin/env python3
"""Publish Context Guard to JourneyKits.ai"""

import json
import os
import re
import sys
import urllib.request
import urllib.error

API_URL = "https://www.journeykits.ai/api/kits/import"
API_KEY = "akit_b25233eea12c_24954ecfdb0dd64c3037a3a62629b4a1aedf90f71b92cdd1"
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))


def read_file(rel_path):
    """Read a file relative to the project directory."""
    full = os.path.join(PROJECT_DIR, rel_path)
    with open(full, "r", encoding="utf-8") as f:
        return f.read()


def sanitize(content):
    """Remove personal info and rebrand to 'Context Guard'."""
    s = content
    # Rebrand: "Claude Context Guard" -> "Context Guard"
    s = s.replace("Claude Context Guard", "Context Guard")
    # Abbreviation
    s = s.replace("CCG", "Context Guard")
    # Personal paths
    s = re.sub(r'C:\\Users\\[^\\]+\\[^\s"\']+', '/path/to/project', s)
    s = re.sub(r'/Users/[^/]+/[^\s"\']+', '/path/to/project', s)
    # Personal emails
    s = re.sub(r'robgreensmail@gmail\.com', 'user@example.com', s)
    # Consumer project names (be careful not to replace in generic text)
    for name in ['AutoPoster', 'Audit for AI', 'Dev Base', 'My number picker']:
        s = s.replace(name, 'YourProject')
    # Don't replace "Lilu" in generic contexts - only in consumer lists
    s = re.sub(r'Lilu(?:\s*\(build-time \+ runtime\))?', 'YourProject', s)
    return s


def build_bundle():
    """Build the full kit bundle."""

    # Read kit.md
    kit_doc = read_file("kit.md")

    # Read skill files (keys must be flat names, not nested paths)
    skill_files = {}
    for skill in ["start", "end", "audit", "save", "itemise"]:
        content = read_file(f".claude/skills/{skill}/SKILL.md")
        skill_files[skill] = sanitize(content)

    # Read source files
    src_files = {}

    # Hooks
    for hook in ["pre-commit-check.sh", "pre-compact-save.sh", "check-slash-commands.sh"]:
        content = read_file(f".claude/hooks/{hook}")
        src_files[f".claude/hooks/{hook}"] = sanitize(content)

    # Settings
    src_files[".claude/settings.json"] = read_file(".claude/settings.json")

    # Install script
    src_files["install.sh"] = sanitize(read_file("install.sh"))

    # Templates
    for tmpl in ["CLAUDE.md", "SESSION_LOG.md", "TASK_REGISTRY.md",
                 "DECISIONS.md", "COMMENTS.md", "FEATURE_LIST.json"]:
        content = read_file(f"templates/{tmpl}")
        src_files[f"templates/{tmpl}"] = sanitize(content)

    # Build file manifest with required 'role' field
    file_manifest = []
    for path, content in {**skill_files, **src_files}.items():
        file_manifest.append({
            "path": path,
            "size": len(content.encode("utf-8")),
            "role": get_file_role(path),
            "description": get_file_description(path)
        })

    now = "2026-04-04T00:00:00Z"

    # Build manifest
    manifest = {
        "schemaVersion": "1.0.0",
        "slug": "context-guard",
        "title": "Context Guard",
        "description": "Persistent context protection for AI coding agents. External safeguard files (session logs, task registries, decisions, comments, feature lists) survive across sessions, rate limits, and context compaction. Five slash commands (/start, /end, /audit, /save, /itemise) provide session recovery, integrity checking, and mid-session checkpoints. The core principle — external state files that outlive context windows — is LLM-agnostic; the reference implementation targets Claude Code.",
        "summary": "Persistent context protection for AI coding agents — safeguard files survive sessions, rate limits, and compaction.",
        "version": "1.0.0",
        "license": "MIT",
        "tags": ["context", "memory", "persistence", "session-management", "agent-workflow"],
        "model": {
            "provider": "anthropic",
            "name": "claude-opus-4-6",
            "hosting": "cloud API — requires ANTHROPIC_API_KEY"
        },
        "selfContained": True,
        "environment": {
            "runtime": "Any AI coding agent with skill support",
            "os": "cross-platform (macOS, Linux, Windows via Git Bash)",
            "platforms": ["claude-code"],
            "adaptationNotes": "The reference implementation uses Claude Code and CLAUDE.md. To adapt for other agents, replace CLAUDE.md with your agent's instruction file and map the 5 skills to your agent's skill/command system. The core principle — external state files that survive context windows — is LLM-agnostic."
        },
        "tools": [
            "pre-commit-check — Pre-commit hook reminding the agent to update safeguard files before every git commit",
            "pre-compact-save — PreCompact hook that backs up safeguard files before context compaction",
            "check-slash-commands — UserPromptSubmit hook enforcing skill invocation for slash commands"
        ],
        "skills": [
            "start — Session recovery: reads all safeguard files, cross-references plans, flags dropped tasks",
            "end — Session save point: updates safeguard files, commits, pushes, reports summary",
            "audit — On-demand integrity check: verifies all files, plans, git state, task registry",
            "save — Mid-session checkpoint: updates safeguard files without git operations",
            "itemise — Itemisation Protocol: adds hierarchical section numbers to code files for targeted reading"
        ],
        "inputs": [
            {"name": "project-name", "description": "Name of the project to protect"},
            {"name": "project-description", "description": "Brief description of the project"}
        ],
        "outputs": [
            {"name": "safeguard-files", "description": "SESSION_LOG.md, TASK_REGISTRY.md, DECISIONS.md, COMMENTS.md, FEATURE_LIST.json — persistent state that survives across sessions"},
            {"name": "session-recovery", "description": "Full context recovery via /start at any session start"}
        ],
        "failuresOvercome": [
            {"problem": "Context lost after rate limits or session restarts — agent starts fresh with no memory", "resolution": "External safeguard files persist across sessions; /start recovers full context in one command", "scope": "general"},
            {"problem": "Tasks dropped between sessions — agent forgets what was pending", "resolution": "TASK_REGISTRY.md with cross-referencing ensures nothing is lost; /audit catches dropped tasks", "scope": "general"},
            {"problem": "Context compaction silently loses work mid-session", "resolution": "PreCompact hook backs up safeguard files automatically; auto-checkpoint protocol keeps files current throughout the session", "scope": "environment"}
        ],
        "prerequisites": [
            {"name": "git", "check": "git --version"}
        ],
        "verification": {
            "command": "ls .claude/skills/start/SKILL.md && echo 'Context Guard installed'"
        },
        "createdAt": now,
        "updatedAt": now,
        "fileManifest": file_manifest
    }

    # Assemble bundle
    bundle = {
        "manifest": manifest,
        "kitDoc": kit_doc,
        "skillFiles": skill_files,
        "toolFiles": {},
        "srcFiles": src_files,
        "examples": {},
        "assets": {}
    }

    return bundle


def get_file_role(path):
    """Return the role for each file in the manifest."""
    if path in ["start", "end", "audit", "save", "itemise"]:
        return "skill"
    if "hooks/" in path:
        return "hook"
    if path == ".claude/settings.json":
        return "config"
    if path == "install.sh":
        return "installer"
    if "templates/" in path:
        return "template"
    return "source"


def get_file_description(path):
    """Return a short description for each file."""
    descs = {
        "start": "Session recovery skill — reads safeguard files, cross-references plans, flags dropped tasks",
        "end": "Session end skill — updates safeguard files, commits, pushes, reports summary",
        "audit": "Integrity audit skill — verifies all files, plans, git state, task registry",
        "save": "Mid-session checkpoint skill — updates safeguard files without git operations",
        "itemise": "Code itemisation skill — adds hierarchical section numbers for targeted reading",
        ".claude/hooks/pre-commit-check.sh": "Pre-commit hook reminding agent to update safeguard files",
        ".claude/hooks/pre-compact-save.sh": "PreCompact hook backing up safeguard files before compaction",
        ".claude/hooks/check-slash-commands.sh": "UserPromptSubmit hook enforcing skill invocation for slash commands",
        ".claude/settings.json": "Claude Code settings with hook configuration",
        "install.sh": "One-command installer for Context Guard",
        "templates/CLAUDE.md": "Template for project instruction file with all protocols",
        "templates/SESSION_LOG.md": "Template for session history log",
        "templates/TASK_REGISTRY.md": "Template for permanent task registry",
        "templates/DECISIONS.md": "Template for architectural decisions register",
        "templates/COMMENTS.md": "Template for verbatim user comments log",
        "templates/FEATURE_LIST.json": "Template for feature pass/fail tracker (JSON)"
    }
    return descs.get(path, path)


def publish(bundle):
    """POST the bundle to JourneyKits API."""
    payload = json.dumps({
        "bundle": bundle,
        "author": "lilu",
        "visibility": "public",
        "skipRelease": False
    }, ensure_ascii=False)

    req = urllib.request.Request(
        API_URL,
        data=payload.encode("utf-8"),
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        },
        method="POST"
    )

    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            body = resp.read().decode("utf-8")
            print(f"Status: {resp.status}")
            print(f"Response: {body}")
            return json.loads(body)
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8")
        print(f"HTTP Error {e.code}: {e.reason}")
        print(f"Response: {body}")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None


if __name__ == "__main__":
    print("Building Context Guard kit bundle...")
    bundle = build_bundle()

    # Save bundle for inspection
    bundle_path = os.path.join(PROJECT_DIR, "kit_bundle.json")
    with open(bundle_path, "w", encoding="utf-8") as f:
        json.dump(bundle, f, indent=2, ensure_ascii=False)
    print(f"Bundle saved to kit_bundle.json ({os.path.getsize(bundle_path)} bytes)")

    print("\nPublishing to JourneyKits.ai...")
    result = publish(bundle)

    if result:
        print("\nPublish complete!")
    else:
        print("\nPublish failed. Check the response above.")
