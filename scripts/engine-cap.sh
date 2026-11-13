#!/usr/bin/env bash
# PreToolUse (Bash|PowerShell): warn, never block, when the number of running engine processes
# has reached the configured cap. Config: engine_process, max_engine_runs (plugin userConfig).
# Also warns on a wait that wastes tokens: a bare sleep over 270 s (the prompt cache lives 5
# minutes, so the next call re-bills the whole context) or an idle echo used as a poll.
input=$(cat 2>/dev/null)
cmd=$(printf '%s' "$input" | tr -d '\n' | sed -n 's/.*"command"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p')
secs=$(printf '%s' "$cmd" | sed -n -E 's/^[[:space:]]*(sleep|Start-Sleep( -Seconds| -s)?)[[:space:]]+([0-9]+)[[:space:]]*$/\3/p')
case "$cmd" in "echo idle"|"echo w"|"echo waiting"|"echo wait") secs=999 ;; esac
if [ -n "$secs" ] && [ "$secs" -gt 270 ]; then
  msg="game-studio: wasteful wait. Wait in one blocking command of at most 270 s that returns on a done-condition (timeout 270 bash -c 'until <done>; do sleep 5; done'), repeat it until done, and do not poll with echo, sleep or status reads in between."
  printf '{"systemMessage":"%s","hookSpecificOutput":{"hookEventName":"PreToolUse","additionalContext":"%s"}}\n' "$msg" "$msg"
  exit 0
fi
name="${CLAUDE_PLUGIN_OPTION_ENGINE_PROCESS-godot}"
cap="${CLAUDE_PLUGIN_OPTION_MAX_ENGINE_RUNS:-10}"
cap="${cap%%.*}"
[ -z "$name" ] && exit 0
case "$cap" in ''|*[!0-9]*|0) exit 0 ;; esac

count=0
case "$(uname -s 2>/dev/null)" in
  MINGW*|MSYS*|CYGWIN*)
    # Windows under Git Bash: image names from tasklist, substring match, case-insensitive.
    # Skip *_console launchers: each Windows engine run is a console launcher plus its real child.
    count=$(MSYS_NO_PATHCONV=1 tasklist.exe /FO CSV /NH 2>/dev/null | cut -d, -f1 | grep -i -- "$name" | grep -vci -- "_console")
    ;;
  *)
    if command -v pgrep >/dev/null 2>&1; then
      count=$(pgrep -i -- "$name" 2>/dev/null | wc -l)
    else
      count=$(ps -A -o comm= 2>/dev/null | grep -ci -- "$name")
    fi
    ;;
esac
count=$(printf '%s' "$count" | tr -dc '0-9')
count=${count:-0}
[ "$count" -lt "$cap" ] && exit 0

# Keep the message free of quotes and backslashes so it is valid JSON as-is.
safe_name=$(printf '%s' "$name" | tr -d '\042\134')
msg="game-studio: $count $safe_name processes are running (cap $cap across all workers). Do not start another engine run now; queue it or wait for runs to finish. Never kill processes you did not start."
printf '{"systemMessage":"%s","hookSpecificOutput":{"hookEventName":"PreToolUse","additionalContext":"%s"}}\n' "$msg" "$msg"
exit 0
