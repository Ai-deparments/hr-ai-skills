"""Validate every skills/*/SKILL.md: frontmatter with name + description, name == folder."""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NAME_RE = re.compile(r"^[a-z0-9][a-z0-9-]{0,63}$")


def parse_frontmatter(text: str) -> dict | None:
    if not text.startswith("---"):
        return None
    end = text.find("\n---", 3)
    if end == -1:
        return None
    meta = {}
    for line in text[3:end].strip().splitlines():
        if ":" in line and not line.startswith(" "):
            key, _, value = line.partition(":")
            meta[key.strip()] = value.strip()
    return meta


def main() -> int:
    errors = []
    skills = sorted(p for p in (ROOT / "skills").iterdir() if p.is_dir())
    for folder in skills:
        f = folder / "SKILL.md"
        if not f.exists():
            errors.append(f"{folder.name}: missing SKILL.md")
            continue
        meta = parse_frontmatter(f.read_text(encoding="utf-8"))
        if meta is None:
            errors.append(f"{folder.name}: no YAML frontmatter")
            continue
        name, desc = meta.get("name", ""), meta.get("description", "")
        if name != folder.name:
            errors.append(f"{folder.name}: name '{name}' != folder name")
        if not NAME_RE.match(name):
            errors.append(f"{folder.name}: invalid name '{name}'")
        if len(desc) < 40:
            errors.append(f"{folder.name}: description too short")
        if len(desc) > 1024:
            errors.append(f"{folder.name}: description over 1024 chars")
    for e in errors:
        print("ERROR", e)
    print(f"{len(skills)} skills checked, {len(errors)} errors")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
