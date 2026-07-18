# Claude Code Hooks

The enabled `PreToolUse` hooks are deterministic defense-in-depth checks:

- `guard_command.py` blocks a small set of clearly destructive shell commands.
- `protect_sensitive_files.py` blocks reads or edits of common secret and
  credential paths while allowing example files.

Hooks receive JSON on standard input and return Claude Code hook decision JSON.
They are intentionally small, standard-library-only, and fail closed on invalid
input. They do not attempt to parse every possible shell language or replace the
Claude sandbox and permission system.

Run their unit tests with:

```bash
python -m unittest tests.template_tools.test_claude_hooks -v
```
