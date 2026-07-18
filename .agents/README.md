# Portable Agent Skills

This directory is the canonical source for repository skills. Keep each skill
focused on one repeatable workflow and use only portable Agent Skills
frontmatter unless a vendor-specific copy has a documented reason to differ.

Run `python scripts/sync_agent_skills.py` after changing a skill. CI uses
`--check` to prevent drift from `.claude/skills/`.
