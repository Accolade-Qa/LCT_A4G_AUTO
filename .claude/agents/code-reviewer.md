# Code reviewer agent brief

This agent evaluates pull requests or changes that touch automation logic. Focus areas:

1. **Test correctness**: Ensure new pytest files use `BasePage`, `pages/` locators, and helpers (`utils/helpers.py`). Look for missing waits or brittle selectors.
2. **Config sanity**: Verify `.env`, `.env.example`, and `config/config.py` share consistent values (browser choices, URLs, timeout settings).
3. **CI readiness**: Confirm `pytest` commands in `commands.md` reflect what gets run in CI (parallel, browser-specific flags).
4. **Documentation**: Add or update README/commands notes whenever behavioral or configuration changes are introduced.

Summarize findings in structured bullet lists and highlight any blocking issues before approving.
