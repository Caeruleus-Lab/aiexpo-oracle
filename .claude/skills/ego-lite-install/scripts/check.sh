#!/usr/bin/env bash
# Read-only status of ego(lite) + the ego-browser skill for Claude Code, omx (Codex) and omp.
# Exit 0 = ready, 1 = something to do (the report says what).
set -u
ok=0
line() { printf '%-28s %s\n' "$1" "$2"; }
line "machine" "$(uname -s) $(uname -m)"
APP="/Applications/ego lite.app"
if [ -d "$APP" ]; then
  line "ego(lite) app" "$(defaults read "$APP/Contents/Info.plist" CFBundleShortVersionString 2>/dev/null) ($APP)"
else
  line "ego(lite) app" "MISSING — run fetch-verify.sh, then install by hand"; ok=1
fi
if command -v ego-browser >/dev/null 2>&1; then
  line "ego-browser CLI" "$(ego-browser --version 2>&1 | head -1)"
else
  line "ego-browser CLI" "MISSING — finish onboarding in ego(lite)"; ok=1
fi
for d in "$HOME/.claude/skills" "$HOME/.agents/skills" "$HOME/.codex/skills"; do
  if [ -e "$d/ego-browser/SKILL.md" ]; then line "skill in ${d/#$HOME/\~}" "ok"; else line "skill in ${d/#$HOME/\~}" "missing"; [ "$d" = "$HOME/.codex/skills" ] || ok=1; fi
done
for a in claude codex omx omp; do
  if command -v "$a" >/dev/null 2>&1; then line "agent $a" "$(command -v "$a")"; else line "agent $a" "not installed"; fi
done
echo
if [ $ok -eq 0 ]; then echo "VERDICT: ready — type /ego-browser <task> in your agent"; else echo "VERDICT: not ready — see the lines marked MISSING/missing"; fi
exit $ok
