#!/usr/bin/env bash
# UserPromptSubmit: fires in the main session when a background worker reports back (as well as
# on typed prompts, which pass silently). Reminds the coordinator to review the handoff, refill
# every free slot and check the other workers for stalls. Silent outside studio projects.
input=$(cat 2>/dev/null)
case "$input" in *'"agent_id"'*) exit 0 ;; esac
case "$input" in *'task-notification'*|*'agent-message from='*) ;; *) exit 0 ;; esac
root="${CLAUDE_PROJECT_DIR:-$PWD}"
[ -f "$root/.claude/game-studio/project.md" ] || [ -f "$root/.claude/skills/game-studio/project.md" ] || exit 0
msg="game-studio: a worker reported back. Review its handoff with the checklist (open the key images, grep logs, check scope, caps and coverage) before accepting; delete the accepted item from the queue doc; stop its shells and monitors. Then, unless the studio is paused or the user said to hold launches, check load and disk and fill EVERY free slot within the caps with queue items that do not depend on a running worker, and relaunch any running worker with no new evidence for the stall limit."
printf '{"hookSpecificOutput":{"hookEventName":"UserPromptSubmit","additionalContext":"%s"}}
' "$msg"
exit 0
