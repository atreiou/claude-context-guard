#!/bin/bash
# Claude Context Guard — Installer
# Usage: ./install.sh [target-directory]
# If no target directory given, uses current working directory.

set -e

TARGET="${1:-.}"

# Resolve to absolute path
TARGET="$(cd "$TARGET" && pwd)"

# Get the directory where this script lives (the Context Guard repo)
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo ""
echo "  Claude Context Guard — Installer"
echo "  ================================="
echo ""
echo "  Installing into: $TARGET"
echo ""

# Check if .claude/ already exists
if [ -d "$TARGET/.claude" ]; then
    echo "  WARNING: $TARGET/.claude/ already exists."
    echo "  Context Guard files will be merged into your existing .claude/ folder."
    echo ""
    read -p "  Continue? (y/n) " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "  Aborted."
        exit 1
    fi
    echo ""
fi

# Copy skills
echo "  Copying skills..."
mkdir -p "$TARGET/.claude/skills"
cp -r "$SCRIPT_DIR/.claude/skills/start" "$TARGET/.claude/skills/"
cp -r "$SCRIPT_DIR/.claude/skills/end" "$TARGET/.claude/skills/"
cp -r "$SCRIPT_DIR/.claude/skills/audit" "$TARGET/.claude/skills/"
cp -r "$SCRIPT_DIR/.claude/skills/itemise" "$TARGET/.claude/skills/"

# Copy hooks
echo "  Copying hooks..."
mkdir -p "$TARGET/.claude/hooks"
cp "$SCRIPT_DIR/.claude/hooks/pre-commit-check.sh" "$TARGET/.claude/hooks/"

# Copy settings.json only if it doesn't already exist
if [ ! -f "$TARGET/.claude/settings.json" ]; then
    echo "  Copying settings.json..."
    cp "$SCRIPT_DIR/.claude/settings.json" "$TARGET/.claude/settings.json"
else
    echo "  Skipping settings.json (already exists)"
fi

# Copy templates
echo "  Copying templates..."
mkdir -p "$TARGET/templates"
cp "$SCRIPT_DIR/templates/"* "$TARGET/templates/"

echo ""
echo "  ✓ Context Guard installed successfully."
echo ""
echo "  Next step: Open Claude Code in your project and type /start"
echo "  On first run, /start will set up your safeguard files and offer to"
echo "  itemise your existing codebase."
echo ""
