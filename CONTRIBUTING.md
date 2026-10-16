# Contributing

1. Put one skill in one folder: `skills/<kebab-name>/SKILL.md`, plus an optional `references/` folder.
2. The frontmatter needs `name` (the same as the folder) and `description`. Say what the skill does and when to trigger it, and add trigger phrases in the languages your users write in.
3. Keep the human-only rule: no skill may approve payroll, deduct, change contracts, hire, dismiss, broadcast or approve requests.
4. No real personal data, tokens, IDs or salaries in examples. Use fake names.
5. Run `python scripts/validate_skills.py` before you open a PR.
