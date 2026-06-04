---
name: deploy
description: Automate release verification, generate HTML/Excel report bundles, package test artifacts, and execute post-deploy smoke tests.
version: 1.0.0
author: Antigravity
tags:
  - deploy
  - verification
  - report-generation
  - release
---

# Deploy Skill

This skill automates pre-release and post-deployment validation. It executes test suites inside the virtual environment and bundles all verification reports (Allure, HTML, Excel) for release approval.

## When to Use
- Triggering pre-release verification checks before merging to master/develop.
- Generating test result reports (HTML, Excel, JSON) using custom project report generators.
- Performing live smoke tests against staging or production endpoints post-deployment.

## Deployment Verification Steps

### 1. Set Up Environment
Ensure the environment is ready for test execution:
- Activate the virtual environment (`.venv\Scripts\Activate.ps1` on Windows, or `source .venv/bin/activate` on Linux/macOS).
- Confirm dependencies match requirements: `pip install -r requirements.txt`.
- Install necessary browsers: `playwright install`.

### 2. Clean Up Cache & Caches
Before starting execution, clean up old runs to avoid reporting stale results:
- Clear standard pytest caches and report dirs.
- Delete old files inside `reports/` and `screenshots/`.

### 3. Execute Verification & Report Bundling
Run the verification suites and compile reporting formats:
- **Option A: Full Automated Report Generation**
  Run the central reports command:
  ```powershell
  python utils/generate_reports.py
  ```
  *Behind the scenes*: This command triggers `pytest` with the `--json-report` plugin to populate `reports/report.json`. It then parses results using `pandas` to output:
  - `reports/report.html` (Interactive web report with test execution timelines)
  - `reports/report.xlsx` (Color-coded Excel sheet mapping test names, expected, actual, duration, and error logs)

- **Option B: Manual Allure Collection**
  ```powershell
  pytest --alluredir=reports/allure-results
  ```
  Then build the Allure report:
  ```powershell
  allure generate reports/allure-results --clean -o reports/allure-report
  ```

### 4. Verify Generated Artifacts
Ensure report files exist and look complete:
- Check that [reports/report.html](file:///D:/AEPL_AUTOMATION/LCT_A4G_AUTO/reports/report.html) and [reports/report.xlsx](file:///D:/AEPL_AUTOMATION/LCT_A4G_AUTO/reports/report.xlsx) are created.
- Review any failure screenshots captured under `reports/screenshots/` (paths defined in `conftest.py`).

### 5. Run Post-Deployment Smoke Tests
Directly run smoke test cases against the newly deployed server URL:
- Modify `.env` variables `BASE_URL` and `DASHBOARD_URL` to point to the deployed target endpoint.
- Run targeted smoke tests:
  ```powershell
  pytest tests/test_login_page.py -k smoke
  pytest tests/test_dashboard_page.py -k smoke
  ```
- Re-run the report script `python utils/generate_reports.py` with `RUN_PYTEST=false` to package results without triggering a new test run, if necessary.
- Document any environment details or credential setups in [CLAUDE.local.md](file:///D:/AEPL_AUTOMATION/LCT_A4G_AUTO/CLAUDE.local.md).
