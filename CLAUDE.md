# Claude agent summary

## Project snapshot
- **Domain**: LCT-A4G Device Dashboard automation tests.
- **Stack**: Python 3.8+, Playwright, pytest, Allure for reporting.
- **Purpose for Claude**: help author or validate tests, configuration updates, and release prep guided by the instructions below.

## Key actions the agent can take
1. **Understand the structure**: `config/` holds env helpers, `pages/` implements Playwright page objects, `tests/` contains pytest cases, and `utils/helpers.py` exposes reusable helpers. Use `README.md` for a full overview when uncertain.
2. **Set up**: run `python -m venv .venv`, activate it, install via `pip install -r requirements.txt`, and install Playwright browsers with `playwright install`.
3. **Run tests**: use `pytest` (with `-n auto` for parallel execution, `--browser` to pick Chromium/Firefox/WebKit, `--alluredir` to collect results). Capture screenshots/videos automatically via `.env` flags (`SCREENSHOT_ON_FAILURE=true`, `VIDEO_RECORDING` toggles).
4. **Check configs**: `.env` in root is the source of truth. Mirror values referenced in `config/config.py` before editing tests or fixtures.
5. **Deliverables**: when asked to add new tests, create `tests/test_<feature>.py` and complement with page objects under `pages/`. Add documentation or commands in `commands.md` as needed.

## Notes for Claude workflows
- **Deploy/Review/Fix** commands live in `.claude/commands/`; follow each file’s guidance before acting.
- **Agents** describe specialized roles for code review or security auditing—refer to `.claude/agents/` for their scope.
- **Local overrides** belong in `CLAUDE.local.md` for sensitive or environment-specific notes; avoid committing secrets or real credentials.
- **Skills and rules** (inside `.claude/skills/` and `.claude/rules/`) define reusable workflows. Add new steps there if you automate repeated tasks.

Use this file as the canonical summary of how Claude should reason about the repo before running commands or making changes.
