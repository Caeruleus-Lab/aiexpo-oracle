#!/usr/bin/env bash
# After onboarding: make sure the ego-browser skill is visible to Claude Code, omx (Codex) and omp.
# Only adds missing symlinks to the onboarding copy; never overwrites an existing entry.
set -u
SRC="$HOME/.local/share/ego/ego-skills"
[ -f "$SRC/SKILL.md" ] || { echo "No onboarding copy at $SRC — open ego(lite) and finish onboarding first."; exit 1; }
for d in "$HOME/.claude/skills" "$HOME/.agents/skills" "$HOME/.codex/skills"; do
  mkdir -p "$d"
  if [ -e "$d/ego-browser" ] || [ -L "$d/ego-browser" ]; then
    echo "keep    ${d/#$HOME/\~}/ego-browser -> $(readlink "$d/ego-browser" 2>/dev/null || echo '(directory)')"
  else
    ln -s "$SRC" "$d/ego-browser" && echo "linked  ${d/#$HOME/\~}/ego-browser -> ${SRC/#$HOME/\~}"
  fi
done
