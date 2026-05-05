# Testing rulebook

- Always run the smallest failing test before triaging a bug to reduce noise (`pytest tests/test_login_page.py -k test_name`).
- Use `pytest -n auto` for faster suites but limit concurrency if the environment is resource constrained.
- Capture Allure results every time a regression is addressed; store artifacts under `reports/allure-results`.
- Toggle `VIDEO_RECORDING` or `SCREENSHOT_ON_FAILURE` in `.env` only if debugging, then revert to defaults.
