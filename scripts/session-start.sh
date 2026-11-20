#!/usr/bin/env bash
# SessionStart: one-line reminder to read the studio project.md and the queue doc, if they exist.
# Silent in projects that have neither, so the plugin stays quiet outside game projects.
input=$(cat 2>/dev/null)
root="${CLAUDE_PROJECT_DIR:-$PWD}"
queue="${CLAUDE_PLUGIN_OPTION_QUEUE_DOC:-docs/TODO.md}"
found=""
for p in .claude/game-studio/project.md .claude/skills/game-studio/project.md; do
  if [ -f "$root/$p" ]; then found="$p"; break; fi
done
[ -n "$queue" ] && [ -f "$root/$queue" ] && found="${found:+$found and }$queue"
[ -z "$found" ] && exit 0
# The instruction file rides in every call of every worker: flag it when it grows.
for f in AGENTS.md CLAUDE.md; do
  [ -f "$root/$f" ] || continue
  size=$(wc -c < "$root/$f" | tr -dc '0-9')
  [ "${size:-0}" -gt 10240 ] && echo "game-studio: $f is $((size / 1024)) KB and is loaded into every call of every worker. Brief a worker to cut it under 10 KB (rules only; reference material to the vault or docs)."
done
# The queue doc is read and edited all session: flag it when it has turned into a log.
if [ -n "$queue" ] && [ -f "$root/$queue" ]; then
  qsize=$(wc -c < "$root/$queue" | tr -dc '0-9')
  [ "${qsize:-0}" -gt 30720 ] && echo "game-studio: $queue is $((qsize / 1024)) KB. It holds open work only, one line per item: brief a coordinator-helper to archive finished and stale lines and cut it under 30 KB."
fi
echo "game-studio: before planning or delegating, read $found (top of the queue first: pauses, urgent items, latest user directions)."
# After a compaction the session is long: suggest a fresh one at the next quiet point.
case "$input" in *'"compact"'*)
  echo "game-studio: this session was compacted. Your memory of what ran is no longer reliable: before any launch, reconcile the queue doc with the workers actually running and check the item is not already done or live; keep the CHUNK MODEL line on every brief. Check the queue doc and decision log are current; at the next quiet point (goal done, or no workers running) tell the user once to start a fresh session with /game-studio:studio-resume; do not wait for a second compaction." ;;
esac
exit 0
