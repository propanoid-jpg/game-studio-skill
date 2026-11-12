#!/usr/bin/env bash
# PostToolUse (Agent): fires at launch for background workers, so it reminds the coordinator to
# fill the remaining free slots. The review reminder on return is worker-return.sh.
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
msg="game-studio: $agent launched. Record it in the queue doc. If worker slots are still free and the queue has items that do not depend on a running worker, launch them now, within the caps."
printf '{"hookSpecificOutput":{"hookEventName":"PostToolUse","additionalContext":"%s"}}\n' "$msg"
exit 0
