#!/usr/bin/env bash
# Copy skills into ~/.claude/skills (default) or ./.claude/skills (--project).
# Also installs Cloudflare's security-audit skill (MIT) as "cloudflare-security-audit" unless --no-third-party.
set -euo pipefail
root="$(cd "$(dirname "$0")/.." && pwd)"
dest="$HOME/.claude/skills"
third=1
for a in "$@"; do
  case "$a" in
    --project) dest="$(pwd)/.claude/skills" ;;
    --no-third-party) third=0 ;;
  esac
done
mkdir -p "$dest"
for d in "$root"/skills/*/; do
  name="$(basename "$d")"
  rm -rf "${dest:?}/$name"
  cp -R "$d" "$dest/$name"
  echo "installed $name -> $dest/$name"
done
if [ "$third" = 1 ]; then
  t="$dest/cloudflare-security-audit"
  rm -rf "$t"
  cp -R "$root/third_party/cloudflare-security-audit/security-audit" "$t"
  sed -i.bak 's/^name:[[:space:]]*security-audit[[:space:]]*$/name: cloudflare-security-audit/' "$t/SKILL.md" && rm -f "$t/SKILL.md.bak"
  echo "installed cloudflare-security-audit -> $t"
  for s in playwright-skill task-observer; do
    rm -rf "${dest:?}/$s"
    cp -R "$root/third_party/$s/$s" "$dest/$s"
    echo "installed $s -> $dest/$s"
  done
  echo "playwright-skill needs: (cd $dest/playwright-skill && npm install && npx playwright install chromium)"
fi
