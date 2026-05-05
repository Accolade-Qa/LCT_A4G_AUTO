# Review command guidance

1. **Use-case**: Trigger this when reviewing pull requests, verifying test coverage, or analyzing potential regressions introduced by a change.
2. **Checkpoints**:
   - Confirm any new tests align with the page objects in `pages/` and use helpers from `utils/helpers.py`.
   - Run targeted pytest commands (e.g., `pytest tests/test_dashboard_page.py -k filter`) to ensure behavioral alignment.
   - Validate configuration changes in `config/config.py`, `.env`, and `commands.md`.
3. **Feedback**: Provide a concise summary of what passed, what failed, and recommended follow-up actions, referencing failing test names or configuration mismatches.
4. **Follow-up**: If more context is needed, ask for reproduction steps, expected vs actual behavior, or missing environment details noted in `CLAUDE.md`.
