.PHONY: help verify-template verify validate-blueprints sync-skills tree init-dry-run

help:
	@printf '%s\n' \
	  'verify-template    Validate template policy, skill sync, and unit tests' \
	  'verify             Validate the current repository state' \
	  'validate-blueprints Initialize and validate every stack blueprint' \
	  'sync-skills        Synchronize Claude skill copies from .agents/skills' \
	  'tree               Regenerate TREE.md' \
	  'init-dry-run       Preview generic initialization with example values'

verify-template:
	python scripts/verify_repository.py
	python scripts/sync_agent_skills.py --check
	python -m unittest discover -s tests/template_tools -v

verify:
	python scripts/verify_repository.py

validate-blueprints:
	python scripts/validate_blueprints.py

sync-skills:
	python scripts/sync_agent_skills.py

tree:
	python scripts/render_tree.py

init-dry-run:
	python scripts/template/init_project.py --name 'Example Project' --description 'Example project' --owner example --blueprint generic --license MIT --dry-run
