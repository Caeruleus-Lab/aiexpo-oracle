#!/usr/bin/env bash
# Install THIS skill (ego-lite-install) for Claude Code, omx (Codex) and omp.
# Copies it to a stable home (so a deleted worktree cannot break it), then symlinks:
#   ~/.claude/skills  -> Claude Code (omp reads it too)
#   ~/.agents/skills  -> Codex / omx and omp
#   ~/.codex/skills   -> Codex / omx (older path)
set -u
HERE=$(cd "$(dirname "$0")" && pwd)
HOME_DIR="$HOME/.local/share/oracle-skills/ego-lite-install"
mkdir -p "$HOME_DIR" && rsync -a --delete --exclude install-skill.sh "$HERE/" "$HOME_DIR/" && cp "$HERE/install-skill.sh" "$HOME_DIR/"
echo "copied  ${HOME_DIR/#$HOME/\~}"
for d in "$HOME/.claude/skills" "$HOME/.agents/skills" "$HOME/.codex/skills"; do
  mkdir -p "$d"; T="$d/ego-lite-install"
  if [ -L "$T" ] && [ "$(readlink "$T")" = "$HOME_DIR" ]; then echo "already ${T/#$HOME/\~}"
  elif [ -e "$T" ] || [ -L "$T" ]; then echo "SKIP    ${T/#$HOME/\~} exists and points elsewhere: $(readlink "$T" 2>/dev/null || echo directory)"
  else ln -s "$HOME_DIR" "$T" && echo "linked  ${T/#$HOME/\~} -> ${HOME_DIR/#$HOME/\~}"; fi
done
