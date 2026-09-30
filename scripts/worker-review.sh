#!/usr/bin/env bash
# PostToolUse (Agent): remind the coordinator to review a studio worker's handoff and clean up
# after it. Runs in the launching session, so the reminder reaches the coordinator. (A SubagentStop
# hook would inject its context into the finishing worker instead, making it take another turn.)
# Only for game-studio role agents and general-purpose workers; other agent types stay silent.
input=$(cat 2>/dev/null)
flat=$(printf '%s' "$input" | tr -d '\n')
agent=$(printf '%s' "$flat" | sed -n 's/.*"subagent_type"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p')
agent=${agent:-general-purpose}
case "$agent" in
  game-studio:*|general-purpose) ;;
  *) exit 0 ;;
esac
agent=$(printf '%s' "$agent" | tr -d '\042\134')
msg="game-studio: when the $agent worker returns, review its handoff with templates/review-checklist.md (open the key images, grep logs for errors, check scope and caps) before accepting; record the verdict in the queue doc; stop its background shells and monitors; then launch the next task."
printf '{"hookSpecificOutput":{"hookEventName":"PostToolUse","additionalContext":"%s"}}\n' "$msg"
exit 0
