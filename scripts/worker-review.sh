#!/usr/bin/env bash
# PostToolUse (Agent): fires at launch for background workers, so it reminds the coordinator to
# fill the remaining free slots. The review reminder on return is worker-return.sh.
# Also reminds when a launch above the role's default model carries no CHUNK MODEL reason.
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
model=$(printf '%s' "$flat" | sed -n 's/.*"model"[[:space:]]*:[[:space:]]*"\([a-z]*\)".*/\1/p')
# Role defaults (agents/*.md): is this launch above its role's default tier?
above=0
role=""
case "$agent" in game-studio:*) role="${agent#game-studio:}" ;; esac
case "$model:$role" in
  *:) ;;
  fable:designer) ;;
  fable:*) above=1 ;;
  opus:art-owner|opus:asset-gen|opus:audio-gen|opus:balance|opus:visual-review|opus:designer) ;;
  opus:*) above=1 ;;
  sonnet:knowledge-keeper|sonnet:surveyor) above=1 ;;
esac
reason=""
if [ "$above" = 1 ]; then
  case "$flat" in *'CHUNK MODEL'*) ;; *) reason=" This launch runs on $model, above the role default, with no CHUNK MODEL reason in its prompt: put the reason on the next brief, or relaunch on the default if there is none." ;; esac
fi
msg="game-studio: $agent launched. Tag its queue line as running (no new lines or notes).$reason If worker slots are still free and the queue has items that do not depend on a running worker, launch them now, within the caps."
printf '{"hookSpecificOutput":{"hookEventName":"PostToolUse","additionalContext":"%s"}}\n' "$msg"
exit 0
