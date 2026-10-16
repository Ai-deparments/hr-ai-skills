#!/usr/bin/env sh
# Copy skills into ~/.claude/skills (default) or ./.claude/skills (--project).
set -e
SRC="$(cd "$(dirname "$0")/.." && pwd)/skills"
if [ "$1" = "--project" ]; then DEST="$(pwd)/.claude/skills"; else DEST="$HOME/.claude/skills"; fi
mkdir -p "$DEST"
for d in "$SRC"/*/; do
  name="$(basename "$d")"
  rm -rf "$DEST/$name"
  cp -R "$d" "$DEST/$name"
  echo "installed $name -> $DEST/$name"
done
