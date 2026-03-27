#!/bin/bash
# Claude Context Guard — Pre-Compaction Auto-Save Hook
# Fires before context compaction to remind Claude to save progress.
# Outputs JSON that injects a system message and additional context
# instructing Claude to run /save before compaction proceeds.

cat <<'EOF'
{
  "systemMessage": "🛡️ Context Guard — Auto-saving before compaction. Your project context is being preserved.",
  "hookSpecificOutput": {
    "hookEventName": "PreCompact",
    "additionalContext": "CONTEXT GUARD AUTO-SAVE: Context is about to be compacted. BEFORE compaction proceeds, you MUST update all safeguard files (SESSION_LOG.md, TASK_REGISTRY.md, COMMENTS.md, DECISIONS.md, FEATURE_LIST.json) with everything that has happened in this session so far. Follow the same steps as the /save skill: gather current context, update all safeguard files, and add a checkpoint marker to SESSION_LOG.md with the note '(auto-save before compaction)'. This is critical — after compaction, conversation history will be compressed and details may be lost. The safeguard files are the permanent record."
  }
}
EOF
