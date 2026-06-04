---
paths:
  - pages/**/*.py
  - tests/**/*.py
  - utils/**/*.py
  - config/**/*.py
---
# Code Style

- Follow PEP 8 and pytest conventions (snake_case for functions/tests, PascalCase for page classes).
- Prefer descriptive helper methods in `pages/` and `utils/helpers.py` instead of raw Playwright commands inside tests.
- Keep assertions clear: use `expect` from Playwright or standard pytest assertions with helpful, descriptive messages.
- Document new helpers/tests with docstrings. Update the main project documentation when introducing new entry points or custom scripts.
