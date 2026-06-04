# Claude Agent Onboarding (CLAUDE.md)

This file serves as the onboarding guide and behavioral contract for Claude Code in the LCT-A4G Device Dashboard automation project.

## Project Snapshot
- **Domain**: LCT-A4G Device Dashboard automation tests (both UI and API).
- **Tech Stack**: Python 3.8+, Playwright, pytest, Allure, pandas (for Excel reporting).
- **Architecture**: Page Object Model (POM) for UI tests, API Client pattern for API tests.

## Key Developer Commands

### Environment Setup
- **Activate Venv (PowerShell)**: `.\.venv\Scripts\Activate.ps1`
- **Activate Venv (CMD)**: `.\.venv\Scripts\activate.bat`
- **Activate Venv (Bash)**: `source .venv/bin/activate`
- **Install Dependencies**: `pip install -r requirements.txt`
- **Install Playwright Browsers**: `playwright install`

### Run Tests
- **Run Full Suite**: `pytest`
- **Run Targeted File**: `pytest tests/test_login_page.py`
- **Run Specific Test**: `pytest tests/test_login_page.py::test_login`
- **Run in Parallel**: `pytest -n auto`
- **Target Browser**: `pytest --browser chromium` (options: `chromium`, `firefox`, `webkit`)
- **Headed Mode**: `pytest --headed` (default is headless based on `.env` configuration)

### Test Reporting
- **Generate Allure Results**: `pytest --alluredir=reports/allure-results`
- **Generate Custom Reports Bundle (HTML, JSON, Excel)**: `python utils/generate_reports.py`
  - Outputs: `reports/report.html`, `reports/report.xlsx`, `reports/report.json`

---

## Directory Structure
- [config/](file:///D:/AEPL_AUTOMATION/LCT_A4G_AUTO/config/) - Configuration handlers (`config.py`) and global variables (`global_var.py`). `.env` in the root is the source of truth.
- [pages/](file:///D:/AEPL_AUTOMATION/LCT_A4G_AUTO/pages/) - Page Object Model classes.
  - [pages/api/](file:///D:/AEPL_AUTOMATION/LCT_A4G_AUTO/pages/api/) - Dedicated API clients (e.g. `api_client.py`, `login_api.py`) for backend validation.
  - [pages/common/](file:///D:/AEPL_AUTOMATION/LCT_A4G_AUTO/pages/common/) - Reusable UI component handlers (e.g., search, pagination, tables).
- [tests/](file:///D:/AEPL_AUTOMATION/LCT_A4G_AUTO/tests/) - UI automation test suites.
  - [tests/api_test/](file:///D:/AEPL_AUTOMATION/LCT_A4G_AUTO/tests/api_test/) - API verification tests using the API client.
- [utils/](file:///D:/AEPL_AUTOMATION/LCT_A4G_AUTO/utils/) - Shared libraries: `helpers.py` (waits, screenshots), `logger.py` (logging), and `generate_reports.py`.

---

## Code Guidelines
- **Naming**: Use PEP 8 styling. Functions and tests use `snake_case`, Page classes use `PascalCase`.
- **UI Interaction**: Do not write raw Playwright selector statements inside test scripts. Utilize/extend page object helpers in `pages/` and `utils/helpers.py`.
- **Assertions**: Always use Playwright's `expect` assertions or pytest assertions with descriptive error messages.
- **Rules & Skills**: Custom instructions live in `.claude/rules/` and interactive workflows in `.claude/skills/`.
- **Local Overrides**: Use [CLAUDE.local.md](file:///D:/AEPL_AUTOMATION/LCT_A4G_AUTO/CLAUDE.local.md) for local dev overrides and credentials; do not commit secrets.
