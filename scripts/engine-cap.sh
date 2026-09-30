#!/usr/bin/env bash
# PreToolUse (Bash|PowerShell): warn, never block, when the number of running engine processes
# has reached the configured cap. Config: engine_process, max_engine_runs (plugin userConfig).
cat >/dev/null 2>&1   # drain the hook input; it is not needed
name="${CLAUDE_PLUGIN_OPTION_ENGINE_PROCESS-godot}"
cap="${CLAUDE_PLUGIN_OPTION_MAX_ENGINE_RUNS:-10}"
cap="${cap%%.*}"
[ -z "$name" ] && exit 0
case "$cap" in ''|*[!0-9]*|0) exit 0 ;; esac

count=0
case "$(uname -s 2>/dev/null)" in
  MINGW*|MSYS*|CYGWIN*)
    # Windows under Git Bash: image names from tasklist, substring match, case-insensitive.
    count=$(MSYS_NO_PATHCONV=1 tasklist.exe /FO CSV /NH 2>/dev/null | cut -d, -f1 | grep -ci -- "$name")
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
