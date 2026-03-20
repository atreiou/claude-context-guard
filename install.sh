#!/bin/bash
# Claude Context Guard — Installer
# Usage: ./install.sh [target-directory]
# If no target directory given, uses current working directory.

set -e

# 1. SECTION: Configuration
TARGET="${1:-.}"

# Resolve to absolute path
TARGET="$(cd "$TARGET" && pwd)"

# Get the directory where this script lives (the Context Guard repo)
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
# end of 1

# 2. SECTION: Welcome banner
echo ""
echo "  Claude Context Guard — Installer"
echo "  ================================="
echo ""
echo "  Installing into: $TARGET"
echo ""
# end of 2

# 3. SECTION: Pre-flight checks
# 3.1 Check if .claude/ already exists
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
# end of 3.1
# end of 3

# 4. SECTION: File installation
# 4.1 Copy skills
# Copy skills
echo "  Copying skills..."
mkdir -p "$TARGET/.claude/skills"
cp -r "$SCRIPT_DIR/.claude/skills/start" "$TARGET/.claude/skills/"
cp -r "$SCRIPT_DIR/.claude/skills/end" "$TARGET/.claude/skills/"
cp -r "$SCRIPT_DIR/.claude/skills/audit" "$TARGET/.claude/skills/"
cp -r "$SCRIPT_DIR/.claude/skills/itemise" "$TARGET/.claude/skills/"
# end of 4.1

# 4.2 Copy hooks
# Copy hooks
echo "  Copying hooks..."
mkdir -p "$TARGET/.claude/hooks"
cp "$SCRIPT_DIR/.claude/hooks/pre-commit-check.sh" "$TARGET/.claude/hooks/"
# end of 4.2

# 4.3 Copy settings (conditional)
# Copy settings.json only if it doesn't already exist
if [ ! -f "$TARGET/.claude/settings.json" ]; then
    echo "  Copying settings.json..."
    cp "$SCRIPT_DIR/.claude/settings.json" "$TARGET/.claude/settings.json"
else
    echo "  Skipping settings.json (already exists)"
fi
# end of 4.3

# 4.4 Copy templates
# Copy templates
echo "  Copying templates..."
mkdir -p "$TARGET/templates"
cp "$SCRIPT_DIR/templates/"* "$TARGET/templates/"
# end of 4.4
# end of 4

# 5. SECTION: Success output
echo ""
echo "  ✓ Context Guard installed successfully."
echo ""
echo "  Next step: Open Claude Code in your project and type /start"
echo "  On first run, /start will set up your safeguard files and offer to"
echo "  itemise your existing codebase."
echo ""
# end of 5
