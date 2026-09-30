#!/usr/bin/env bash
# PreToolUse (file-writing tools, write-like MCP tools): the coordinator delegates. When the MAIN
# session (not a subagent) writes a file other than the queue doc, the decision log, project.md or
# its memory/plan files, or calls a write-like MCP tool, add a warning; with the plugin option
# enforce_delegation=block, deny the call instead. Subagent calls carry agent_id and pass silently.
input=$(cat 2>/dev/null)
flat=$(printf '%s' "$input" | tr -d '\n\r')

# Subagent (worker) calls carry "agent_id"; the main session never does, even when run as an agent.
case "$flat" in *'"agent_id"'*) exit 0 ;; esac

field() { printf '%s' "$flat" | sed -n "s/.*\"$1\"[[:space:]]*:[[:space:]]*\"\\([^\"]*\\)\".*/\\1/p"; }
tool=$(field tool_name)
path=$(field file_path)
[ -z "$path" ] && path=$(field notebook_path)

# Normalise: JSON-escaped backslashes and plain backslashes to '/', lower case (advisory match).
norm() { printf '%s' "$1" | sed 's/\\\\/\//g; s/\\/\//g' | tr '[:upper:]' '[:lower:]'; }
p=$(norm "$path")

allowed=0
if [ -n "$p" ]; then
  queue=$(norm "${CLAUDE_PLUGIN_OPTION_QUEUE_DOC:-docs/TODO.md}")
  dlog=$(norm "${CLAUDE_PLUGIN_OPTION_DECISION_LOG-}")
  for suffix in "$queue" "$dlog" ".claude/game-studio/project.md" ".claude/skills/game-studio/project.md"; do
    suffix=${suffix#./}
    [ -z "$suffix" ] && continue
    case "$p" in "$suffix"|*/"$suffix") allowed=1 ;; esac
  done
  case "$p" in
    */.claude/projects/*/memory/*|*/.claude/plans/*) allowed=1 ;;
  esac
fi
[ "$allowed" = 1 ] && exit 0

# Keep messages free of quotes and backslashes so they are valid JSON as-is.
tool=$(printf '%s' "$tool" | tr -d '\042\134')
what="$tool"
[ -n "$path" ] && what="$tool on $(printf '%s' "$path" | sed 's/\\\\/\//g; s/\\/\//g' | tr -d '\042\134')"
msg="Coordinator: delegate this to a worker. The main session only edits the queue doc, the decision log, project.md and its memory; $what is a worker task (launch a game-studio role agent with a brief)."

mode=$(printf '%s' "${CLAUDE_PLUGIN_OPTION_ENFORCE_DELEGATION:-warn}" | tr '[:upper:]' '[:lower:]')
if [ "$mode" = "block" ]; then
  printf '{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"deny","permissionDecisionReason":"%s"}}\n' "$msg"
else
  printf '{"systemMessage":"%s","hookSpecificOutput":{"hookEventName":"PreToolUse","additionalContext":"%s"}}\n' "$msg" "$msg"
fi
exit 0
