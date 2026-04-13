# Code style

- Follow PEP 8 and pytest conventions (snake_case for functions/tests, PascalCase for page classes).
- Prefer descriptive helper methods in `pages/` and `utils/helpers.py` instead of inline Playwright commands inside tests.
- Keep assertions clear: use `expect` from Playwright or pytest assertions with helpful messages.
- Document new helpers/tests with docstrings and update `commands.md` when introducing new entry points or scripts.
