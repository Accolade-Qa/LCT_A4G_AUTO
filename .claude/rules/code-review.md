---
paths:
  - pages/**/*.py
  - tests/**/*.py
  - utils/**/*.py
  - .claude/**/*
---
# Code Review Guidance

- **Use-Case**: Trigger this when reviewing pull requests, verifying test coverage, or analyzing potential regressions introduced by a change.
- **Checkpoints**:
  - Confirm any new tests align with the page objects in `pages/` and use helpers from `utils/helpers.py`.
  - Run targeted pytest commands (e.g., `pytest tests/test_dashboard_page.py -k filter`) to ensure behavioral alignment.
  - Validate configuration changes in `config/config.py`, `.env`, and documentation.
- **Feedback**: Provide a concise summary of what passed, what failed, and recommended follow-up actions, referencing failing test names or configuration mismatches.
- **Follow-up**: If more context is needed, ask for reproduction steps, expected vs actual behavior, or missing environment details noted in `CLAUDE.md`.
