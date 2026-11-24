#!/usr/bin/env bash
# Counts one use of an adaptig-trainer command or skill, so Adaptig can see which
# ones trainers actually use. What is sent: the command or skill name, the app
# (Claude Code, Desktop or Cowork), the time, and a random ID made on this computer
# the first time and kept in ~/.adaptig/installer-id. Never your prompts, files,
# client names or anything you write.
#
# Switch it off: create the file ~/.adaptig/no-usage, or set ADAPTIG_TELEMETRY=0.
# Every message is also written, exactly as sent, to ~/.adaptig/trainer-usage.log.
#
# This script never blocks Claude and always exits 0.
set -u

PLUGIN="adaptig-trainer"
MARKETPLACE="adaptig"
URL="${ADAPTIG_USAGE_URL:-https://ymahkihjsjukzvdinoca.supabase.co/functions/v1/track-skill}"
DIR="$HOME/.adaptig"

[ "${ADAPTIG_TELEMETRY:-1}" = "0" ] && exit 0
[ -e "$DIR/no-usage" ] && exit 0

payload="$(head -c 262144 2>/dev/null || true)"

# Only this plugin's own commands and skills are counted. The name must match
# exactly, which also keeps anything else in the payload out of what is sent.
name="$(printf '%s' "$payload" \
  | grep -oE '"(command_name|skill)"[[:space:]]*:[[:space:]]*"adaptig-trainer:[a-z0-9-]{1,64}"' \
  | head -n 1 | grep -oE 'adaptig-trainer:[a-z0-9-]+' || true)"
[ -n "$name" ] || exit 0
skill="${name#adaptig-trainer:}"

case "${CLAUDE_CODE_ENTRYPOINT:-}" in
  *desktop*) agent="claude-desktop" ;;
  *cowork*|local-agent*) agent="cowork" ;;
  *) agent="claude-code" ;;
esac

mkdir -p "$DIR" 2>/dev/null || true
id="$(cat "$DIR/installer-id" 2>/dev/null | tr -cd 'a-f0-9-' | head -c 64)"
if [ -z "$id" ]; then
  id="$(uuidgen 2>/dev/null || cat /proc/sys/kernel/random/uuid 2>/dev/null || od -An -N16 -tx1 /dev/urandom 2>/dev/null)"
  id="$(printf '%s' "$id" | tr 'A-F' 'a-f' | tr -cd 'a-f0-9-' | head -c 64)"
  [ -n "$id" ] && printf '%s\n' "$id" > "$DIR/installer-id" 2>/dev/null
fi
[ -n "$id" ] || id="anonymous"

ts="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
# Every value is from a fixed character set, so plain string building is safe JSON.
body="{\"occurred_at\":\"$ts\",\"installer_id\":\"$id\",\"marketplace\":\"$MARKETPLACE\",\"plugin\":\"$PLUGIN\",\"skill\":\"$skill\",\"agent\":\"$agent\"}"
{ printf '%s\n' "$body" >> "$DIR/trainer-usage.log"; } 2>/dev/null || true

( curl -s -m 5 -X POST "$URL" -H 'Content-Type: application/json' -d "$body" >/dev/null 2>&1 & ) >/dev/null 2>&1
exit 0
