# Test Execution Commands

This document provides quick reference for running different test categories.

## Quick Commands

### Smoke Tests (Fast, Critical Path)
```bash
# Run all smoke tests
pytest -m smoke

# Run smoke tests with verbose output
pytest -m smoke -v

# Run smoke tests and generate Allure report
pytest -m smoke --alluredir=reports/allure-results
```

### Regression Tests (Full Suite)
```bash
# Run all regression tests
pytest -m regression

# Run regression tests with parallel execution
pytest -m regression -n auto

# Run regression tests with video recording on failure
pytest -m regression -v
```

### Sanity Tests (Core Functionality)
```bash
# Run sanity checks only
pytest -m sanity

# Sanity tests with live browser output
pytest -m sanity -v --headed
```

### Critical Tests (Must Always Pass)
```bash
# Run only critical priority tests
pytest -m critical

# Critical tests with extended timeout
pytest -m critical --timeout=60
```

## By Feature/Module

```bash
# Authentication tests only
pytest -m auth

# Dashboard tests only
pytest -m dashboard

# Device management tests only
pytest -m device

# Role management tests only
pytest -m role
```

## By Environment

```bash
# Staging environment tests
pytest -m staging

# Production deployment verification
pytest -m production
```

## Combined Markers

```bash
# Smoke tests that are also critical
pytest -m "smoke and critical"

# Regression excluding slow tests
pytest -m "regression and not slow"

# Dashboard tests excluding known flaky ones
pytest -m "dashboard and not flaky"

# Authentication tests for production
pytest -m "auth and production"
```

## Running Specific Test Files

```bash
# Run a single test file
pytest tests/test_login_page.py

# Run a specific test class
pytest tests/test_login_page.py::TestLoginPage

# Run a specific test method
pytest tests/test_login_page.py::TestLoginPage::test_login_with_valid_credentials

# Run tests matching a keyword
pytest -k "login" -v
```

## Parallel Execution

```bash
# Auto-detect CPU cores for parallel execution
pytest -m regression -n auto

# Use specific number of workers
pytest -m regression -n 4

# Parallel with verbose output
pytest -m regression -n auto -v
```

## Reporting & Artifacts

```bash
# Generate Allure report
pytest -m smoke --alluredir=reports/allure-results

# View Allure report (requires allure CLI)
allure serve reports/allure-results

# Generate HTML report
pytest -m regression --html=reports/report.html --self-contained-html

# Capture detailed logs
pytest -m regression -v --log-cli-level=DEBUG
```

## Browser & Display Options

```bash
# Run with Firefox browser
pytest -m smoke --browser firefox

# Run with WebKit browser
pytest -m smoke --browser webkit

# Run headless (no visual browser window)
pytest -m regression --headed=false

# Run with visual browser window
pytest -m regression --headed
```

## Debugging & Troubleshooting

```bash
# Stop on first failure
pytest -m regression -x

# Show prints and logging
pytest -m regression -s

# Run only failed tests from last run
pytest -m regression --lf

# Run failed tests + new tests
pytest -m regression --ff

# Drop into debugger on failure
pytest -m regression --pdb

# Show slowest tests
pytest -m regression --durations=10
```

## CI Pipeline Examples

```bash
# Quick smoke test run
pytest -m smoke --headless --browser chromium --alluredir=reports/allure-results

# Full regression suite
pytest -m regression -n auto --browser chromium --alluredir=reports/allure-results -v

# Critical path verification
pytest -m critical --browser chromium --alluredir=reports/allure-results
```

## Environment-Specific Setups

```bash
# Ensure .env is set correctly, then run
pytest -m smoke

# Override configuration via environment variables
BASE_URL=https://staging.app.com BROWSER=firefox pytest -m smoke

# Run against production (use with caution!)
DASHBOARD_URL=https://prod.app.com pytest -m "regression and production"
```

## Available Markers

| Marker | Purpose | Speed | Use Case |
|--------|---------|-------|----------|
| `smoke` | Critical path validation | Fast | Pre-deployment checks |
| `regression` | Full feature suite | Medium-Slow | Regular CI runs |
| `sanity` | Core functionality | Fast | Nightly builds |
| `critical` | Must-pass tests | Medium | Gating |
| `auth` | Login & permissions | Medium | Auth changes |
| `dashboard` | Dashboard features | Medium | Dashboard updates |
| `device` | Device management | Medium | Device-related changes |
| `slow` | Long-running tests | Slow | Nightly only |
| `flaky` | Known issues | Variable | Isolated runs |

---

## Quick Setup

If you're new to this repo:

1. **Install dependencies:**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   pip install -r requirements.txt
   playwright install
   ```

2. **Copy & configure `.env`:**
   ```bash
   BASE_URL=https://your-app.com
   DASHBOARD_URL=https://your-app.com/dashboard
   APP_USERNAME=testuser
   APP_PASSWORD=testpass
   BROWSER=chromium
   HEADLESS=false
   ```

3. **Run your first smoke test:**
   ```bash
   pytest -m smoke -v
   ```


## Running All Projects

   PowerShell — run sequentially (sets `PROJECT` per run):
   ```powershell
   $projects = 'lct','sampark','swaraj','trio'
   foreach ($p in $projects) {
      $env:PROJECT = $p
      python -m pytest tests -q --project $p
   }
   ```

   PowerShell — run in parallel using background jobs:
   ```powershell
   $projects = 'lct','sampark','swaraj','trio'
   $jobs = @()
   foreach ($p in $projects) {
      $jobs += Start-Job -ScriptBlock { param($proj) python -m pytest tests -q --project $proj } -ArgumentList $p
   }
   Wait-Job -Job $jobs
   $jobs | Receive-Job
   ```

   PowerShell — run with CPU affinity (use the provided runner):
   ```powershell
   # Launch one pytest process per project and bind to cores
   PowerShell -ExecutionPolicy Bypass -File run-parallel-projects.ps1
   ```

   Bash (Linux / WSL) — sequential:
   ```bash
   for p in lct sampark swaraj trio; do
      PROJECT=$p python -m pytest tests -q --project $p || exit 1
   done
   ```

   Bash — parallel with background processes (logs per project):
   ```bash
   for p in lct sampark swaraj trio; do
      PROJECT=$p python -m pytest tests -q --project $p > tests_$p.log 2>&1 &
   done
   wait
   ```

   Notes:
   - The `run-parallel-projects.ps1` script uses `start /affinity` to set CPU affinity per process. If you prefer `taskset` on Linux/WSL, I can add a bash runner.
   - Tune project list and pytest options (`-n auto`, markers, verbosity) to your CI needs.
