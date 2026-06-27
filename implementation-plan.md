# Comprehensive Implementation Plan: --project Flag with Project-Specific Test Data

**Date:** 2026-06-26  
**Status:** Ready for Implementation  
**Estimated Time:** 3-4 hours  
**Priority:** HIGH

---

## Table of Contents
1. [Overview](#overview)
2. [Current State Analysis](#current-state-analysis)
3. [Test Data Strategy](#test-data-strategy)
4. [Phase-by-Phase Implementation](#phase-by-phase-implementation)
5. [Code Changes Required](#code-changes-required)
6. [Testing the Implementation](#testing-the-implementation)
7. [Post-Implementation](#post-implementation)

---

## Overview

### What We're Building
A complete project-aware test automation framework that:
- ✅ Runs tests per project via `pytest --project lct -v`
- ✅ Loads project-specific configurations (URLs, credentials)
- ✅ Uses project-specific test data (JSON files, YAML configs)
- ✅ Auto-skips tests not meant for that project
- ✅ Validates configurations on startup

### Current State
- ✅ `--project` flag already implemented in conftest.py
- ✅ Project YAML configs exist (atcu.yaml, lct.yaml, etc.)
- ✅ Project test data folders exist
- ❌ Test folders not organized by project
- ❌ Test markers not applied
- ❌ Auto-skip logic missing
- ❌ Project validation missing

---

## Current State Analysis

### What Already Works
```
1. Flag Parsing (conftest.py lines 79-83)
   pytest --project lct -v  ✅ WORKS

2. Config Loading (config/config.py)
   Reads {project}.yaml dynamically ✅ WORKS

3. Test Data Loading (conftest.py lines 152-157)
   Loads test_data/{project}/login.json ✅ WORKS

4. project_config Fixture
   Returns 27 config values per project ✅ WORKS
```

### What's Missing
```
1. Test Folder Organization
   ❌ No tests/atcu/, tests/lct/, etc.

2. Project Markers
   ❌ @pytest.mark.atcu not used

3. Auto-Skip Logic
   ❌ No pytest_collection_modifyitems

4. Validation
   ❌ No --project value validation
   ❌ No config startup check

5. Documentation
   ❌ No usage guide for --project flag
```

---

## Test Data Strategy

### How Test Data Should Be Organized

#### **Option A: Separate JSON Files Per Project (Recommended)**
```
test_data/
├── atcu/
│   ├── login.json
│   ├── device_data.json
│   ├── user_data.json
│   └── customer_data.json
│
├── lct/
│   ├── login.json
│   ├── device_data.json
│   ├── user_data.json
│   └── customer_data.json
│
├── sampark/
│   ├── login.json
│   ├── device_data.json
│   └── ...
│
├── swaraj/ → ...
├── trio/ → ...
└── common/                    # (NEW) Shared test data
    ├── valid_imei_formats.json
    └── common_test_values.json
```

**Pros:**
- ✅ Clear separation per project
- ✅ Easy to manage project-specific test data
- ✅ Easy to maintain and update
- ✅ Fixture handles loading automatically
- ✅ No code duplication

**Cons:**
- Requires duplication if data is same

#### **Option B: Single JSON with Project Keys**
```json
{
  "atcu": {
    "login": { "valid_imei": "866677075606341" },
    "devices": [...]
  },
  "lct": {
    "login": { "valid_imei": "866677075606341" },
    "devices": [...]
  }
}
```

**Pros:**
- Centralized file
- Easier to see all projects at once

**Cons:**
- Large file
- Need custom loader logic

#### **Option C: YAML Config Files (Advanced)**
```
test_data/
├── atcu_test_data.yaml
├── lct_test_data.yaml
└── sampark_test_data.yaml
```

**Pros:**
- More readable than JSON
- Can include comments

**Cons:**
- Need YAML parser fixture

---

## Phase-by-Phase Implementation

### ⏱️ Phase 1: Project Folder Structure (30 minutes)

#### Step 1.1: Create Project Test Folders
```powershell
# Create folders
New-Item -ItemType Directory -Path "tests/common" -Force
New-Item -ItemType Directory -Path "tests/atcu" -Force
New-Item -ItemType Directory -Path "tests/lct" -Force
New-Item -ItemType Directory -Path "tests/sampark" -Force
New-Item -ItemType Directory -Path "tests/swaraj" -Force
New-Item -ItemType Directory -Path "tests/trio" -Force

# Create __init__.py files
@("common", "atcu", "lct", "sampark", "swaraj", "trio") | ForEach-Object {
    New-Item -ItemType File -Path "tests/$_/__init__.py" -Force
}
```

#### Step 1.2: Categorize Existing Tests
Move tests to appropriate folders:

**Tests to move to `tests/common/` (run for all projects):**
```
test_login_page.py          → tests/common/
test_dashboard_page.py      → tests/common/
test_profile_page.py        → tests/common/
```

**Tests to keep in respective project folders (or create project-specific versions):**
```
test_device_details_page.py → Keep as is for now (add markers later)
test_production_devices_page.py → Same
test_model_page.py → Same
... (others)
```

**Command to execute:**
```powershell
# Back up original tests first
Copy-Item tests tests.backup -Recurse

# Move common tests
Move-Item tests/test_login_page.py tests/common/
Move-Item tests/test_dashboard_page.py tests/common/
Move-Item tests/test_profile_page.py tests/common/
```

---

### ⏱️ Phase 2: Add Project Markers to pytest.ini (10 minutes)

#### Step 2.1: Update pytest.ini
Add project markers:

**File:** pytest.ini
```ini
[pytest]
addopts = --headed --browser chromium --video=retain-on-failure
testpaths = ./tests
python_files = test_*.py
pythonpath = .
markers =
    smoke: Quick sanity tests covering critical user flows (login, dashboard access)
    regression: Full suite of tests verifying all features
    sanity: Core functionality checks (subset of regression)
    critical: High-priority tests that must always pass
    auth: Authentication and authorization tests
    dashboard: Dashboard page tests
    device: Device-related tests
    production: Tests for production deployment
    staging: Tests for staging environment
    slow: Tests that take longer to execute
    ui: User interface specific tests
    api: API integration tests
    flaky: Known flaky tests to run independently
    atcu: ATCU project-specific tests
    lct: LCT project-specific tests
    sampark: Sampark project-specific tests
    swaraj: Swaraj project-specific tests
    trio: Trio project-specific tests
```

---

### ⏱️ Phase 3: Add Project Markers to Tests (20 minutes)

#### Step 3.1: Add Markers to Test Classes
Add project markers to any tests that are project-specific.

**Example: tests/test_model_page.py**
```python
import pytest
from pages.model_page import ModelPage
from utils.logger import get_logger

logger = get_logger(__name__)

@pytest.mark.regression
@pytest.mark.atcu          # ← ADD THIS if ATCU-specific
class TestModelPage:       # OR @pytest.mark.lct if LCT-specific
    """Model page tests"""
    ...
```

**Example: tests/test_production_devices_page.py**
```python
import pytest

@pytest.mark.regression
@pytest.mark.production
@pytest.mark.atcu          # ← ADD THIS if ATCU uses different UI
class TestProductionDevices:
    ...
```

---

### ⏱️ Phase 4: Add Auto-Skip Logic to conftest.py (30 minutes)

#### Step 4.1: Add pytest_collection_modifyitems Hook

**File:** conftest.py (Add after pytest_configure function)

```python
def pytest_collection_modifyitems(config, items):
    """
    Auto-skip tests that are marked for different projects.
    If PROJECT=atcu, skip all tests marked @pytest.mark.lct, etc.
    """
    current_project = os.getenv("PROJECT", "lct").lower()
    project_markers = ["atcu", "lct", "sampark", "swaraj", "trio"]
    
    for item in items:
        # Get all markers for this test
        item_markers = {marker.name for marker in item.iter_markers()}
        
        # Check if this test is marked for a specific project
        project_specific_markers = item_markers & set(project_markers)
        
        if project_specific_markers:
            # Test has a project marker - check if it matches current project
            test_project = list(project_specific_markers)[0]
            if test_project != current_project:
                # Skip this test - it's for a different project
                item.add_marker(
                    pytest.mark.skip(
                        reason=f"Test marked for {test_project}, "
                               f"running {current_project}"
                    )
                )
                logger.debug(
                    "Skipping %s (marked for %s, running %s)",
                    item.name, test_project, current_project
                )
```

---

### ⏱️ Phase 5: Add Configuration Validation (20 minutes)

#### Step 5.1: Add Validation in pytest_configure

**File:** conftest.py (Update pytest_configure function)

```python
def pytest_configure(config):
    project = config.getoption("--project", os.getenv("PROJECT", "lct")).lower()
    
    # Validate project value
    VALID_PROJECTS = ["atcu", "lct", "sampark", "swaraj", "trio"]
    if project not in VALID_PROJECTS:
        raise ValueError(
            f"Invalid project '{project}'. Must be one of: {', '.join(VALID_PROJECTS)}"
        )
    
    os.environ["PROJECT"] = project
    importlib.reload(config_module)
    
    # Validate required config values exist
    required_configs = ["BASE_URL", "USERNAME", "PASSWORD", "BROWSER"]
    missing = []
    
    for config_key in required_configs:
        config_value = getattr(config_module, config_key, None)
        if config_value is None or config_value == "":
            missing.append(config_key)
    
    if missing:
        raise ValueError(
            f"Missing required config values for project '{project}': {', '.join(missing)}. "
            f"Check config/{project}.yaml"
        )
    
    # Print startup message
    logger.info("=" * 60)
    logger.info("🚀 PYTEST STARTUP - Project Configuration")
    logger.info("=" * 60)
    logger.info("PROJECT: %s", project)
    logger.info("BASE_URL: %s", config_module.BASE_URL)
    logger.info("BROWSER: %s (headless=%s)", 
                config_module.BROWSER, config_module.HEADLESS)
    logger.info("=" * 60)
```

#### Step 5.2: Add Config Validator Fixture

**File:** conftest.py (Add new fixture)

```python
@pytest.fixture(scope="session", autouse=True)
def validate_project_config(project_config):
    """
    Automatically validate that all required config keys are loaded.
    Runs once per session before any tests.
    """
    required_keys = [
        "base_url", "username", "password", "browser",
        "api_base_url", "api_username", "api_password"
    ]
    
    missing_keys = [key for key in required_keys if not project_config.get(key)]
    
    if missing_keys:
        raise ValueError(
            f"Missing required config keys for project '{project_config['project']}': "
            f"{', '.join(missing_keys)}"
        )
    
    logger.info("✅ Project config validation passed for %s", 
                project_config["project"])
    yield
```

---

### ⏱️ Phase 6: Enhance Test Data Fixture (20 minutes)

#### Step 6.1: Update test_data Fixture (Optional Enhancement)

**File:** conftest.py (Replace existing test_data fixture)

```python
@pytest.fixture(scope="session")
def test_data(project_config):
    """
    Load project-specific test data from multiple JSON files.
    Supports: login.json, device_data.json, user_data.json, customer_data.json
    Falls back to common/ folder if project-specific file doesn't exist.
    """
    project = project_config["project"]
    test_data_root = Path(__file__).parent / "test_data"
    
    combined_data = {}
    
    # List of test data files to load (in order of priority)
    data_files = [
        "login.json",
        "device_data.json",
        "user_data.json",
        "customer_data.json"
    ]
    
    for data_file in data_files:
        # Try project-specific first
        project_path = test_data_root / project / data_file
        if project_path.exists():
            with project_path.open("r", encoding="utf-8") as f:
                file_data = json.load(f)
                # Use filename as key (without .json)
                key = data_file.replace(".json", "")
                combined_data[key] = file_data
                logger.debug(f"Loaded {project}/{data_file}")
        else:
            # Fall back to common/ if it exists
            common_path = test_data_root / "common" / data_file
            if common_path.exists():
                with common_path.open("r", encoding="utf-8") as f:
                    file_data = json.load(f)
                    key = data_file.replace(".json", "")
                    combined_data[key] = file_data
                    logger.debug(f"Loaded common/{data_file}")
    
    logger.info("✅ Loaded test data for project: %s (files: %s)", 
                project, list(combined_data.keys()))
    
    return combined_data
```

---

### ⏱️ Phase 7: Create Test Data Organization (15 minutes)

#### Step 7.1: Create Additional Test Data Files

For each project, create additional JSON files:

**File: test_data/atcu/device_data.json**
```json
{
    "valid_devices": [
        {
            "imei": "866677075606341",
            "device_name": "Device-ATCU-001",
            "model": "TCU4G"
        },
        {
            "imei": "866677075606342",
            "device_name": "Device-ATCU-002",
            "model": "TCU4G"
        }
    ],
    "invalid_imei": "123456",
    "imei_format_error": "ABCD1234567890"
}
```

**File: test_data/atcu/user_data.json**
```json
{
    "valid_users": [
        {
            "username": "user1@atcu.com",
            "password": "Password@123",
            "role": "admin"
        },
        {
            "username": "user2@atcu.com",
            "password": "Password@456",
            "role": "viewer"
        }
    ],
    "invalid_credentials": {
        "username": "invalid@atcu.com",
        "password": "WrongPassword"
    }
}
```

**File: test_data/lct/device_data.json**
```json
{
    "valid_devices": [
        {
            "imei": "866677075606341",
            "device_name": "Device-LCT-001",
            "model": "LCT-A4G"
        }
    ],
    "invalid_imei": "999999",
    "imei_format_error": "INVALID"
}
```

**Repeat for:** sampark/, swaraj/, trio/

---

### ⏱️ Phase 8: Create Comprehensive Documentation (20 minutes)

#### Step 8.1: Create README Section

**Add to README.md:**

```markdown
## Running Tests by Project

### Quick Start

#### Run all tests for a specific project:
```bash
pytest --project lct -v
pytest --project atcu -v
pytest --project sampark -v
```

#### Run only specific test types:
```bash
# Smoke tests for LCT project
pytest --project lct -m smoke -v

# Regression tests for ATCU project
pytest --project atcu -m regression -v

# Critical tests for all projects
pytest --project lct -m critical -v
```

#### Run specific test file or class:
```bash
# Run all tests in test_login_page.py for LCT
pytest --project lct tests/test_login_page.py -v

# Run specific test class for ATCU
pytest --project atcu tests/test_device_details_page.py::TestDeviceDetails -v

# Run single test method
pytest --project atcu tests/test_device_details_page.py::TestDeviceDetails::test_device_search -v
```

#### Run only common tests (all projects):
```bash
pytest tests/common/ -v
```

#### Run project-specific tests only:
```bash
# ATCU-specific tests
pytest -m atcu -v

# LCT-specific tests
pytest -m lct -v
```

### Valid Project Values
- `atcu` - ATCU project
- `lct` - LCT-A4G project
- `sampark` - Sampark project
- `swaraj` - Swaraj project
- `trio` - Trio project

### Default Behavior
- If `--project` flag is not provided, defaults to value in `.env` file
- If `.env` doesn't have PROJECT, defaults to `lct`

### Test Data
- Each project has its own test data in `test_data/{project}/`
- Common test data can be shared via `test_data/common/`
- Files: `login.json`, `device_data.json`, `user_data.json`, etc.

### Configuration
- Project-specific URLs and credentials: `config/{project}.yaml`
- Shared defaults: `.env` file

### Example Workflow
```bash
# Test ATCU project thoroughly
pytest --project atcu -m "smoke or regression" -v

# Test LCT project with specific markers
pytest --project lct -m critical -v

# Test across all browsers (requires setup)
pytest --project atcu --browser chromium --browser firefox -v
```
```

#### Step 8.2: Create Environment Setup Guide

**Create: Files/PROJECT_SETUP_GUIDE.md**

```markdown
# Project Setup Guide for Multi-Project Testing

## Prerequisites
- Python 3.8+
- Playwright installed: `playwright install`
- All dependencies: `pip install -r requirements.txt`

## Setup Steps

### 1. Activate Virtual Environment
```powershell
# PowerShell
.\.venv\Scripts\Activate.ps1

# CMD
.\.venv\Scripts\activate.bat

# Bash
source .venv/bin/activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
playwright install
```

### 3. Set Default Project (.env)
```
PROJECT=lct
BASE_URL=http://lct-a4g-qa.accoladeelectronics.com/login
USERNAME=your-username
PASSWORD=your-password
```

### 4. Verify Setup
```bash
# Test with LCT project (default)
pytest tests/common/test_login_page.py -v

# Test with ATCU project
pytest --project atcu tests/common/test_login_page.py -v
```

## Directory Structure
```
tests/
├── common/              ← Shared tests (all projects)
├── atcu/                ← ATCU-specific tests
├── lct/                 ← LCT-specific tests
├── sampark/             ← Sampark-specific tests
├── swaraj/              ← Swaraj-specific tests
└── trio/                ← Trio-specific tests

test_data/
├── common/              ← Shared test data
├── atcu/                ← ATCU test data
├── lct/                 ← LCT test data
├── sampark/             ← Sampark test data
├── swaraj/              ← Swaraj test data
└── trio/                ← Trio test data

config/
├── config.py            ← Dynamic loader
├── atcu.yaml            ← ATCU config
├── lct.yaml             ← LCT config
├── sampark.yaml         ← Sampark config
├── swaraj.yaml          ← Swaraj config
└── trio.yaml            ← Trio config
```

## Common Tasks

### Run All LCT Tests
```bash
pytest --project lct -v
```

### Run All ATCU Tests
```bash
pytest --project atcu -v
```

### Run Smoke Tests for All Projects
```bash
# LCT smoke tests
pytest --project lct -m smoke -v

# ATCU smoke tests
pytest --project atcu -m smoke -v
```

### Run Tests in Parallel
```bash
# Install pytest-xdist
pip install pytest-xdist

# Run with 4 workers
pytest --project lct -n 4 -v
```

### Debug Single Test
```bash
# Show print statements
pytest --project lct -s -v tests/common/test_login_page.py::TestLoginPage::test_login_with_valid_credentials

# With Playwright headed mode
pytest --project lct --headed -v
```

### Generate Reports
```bash
# HTML report
pytest --project lct --html=reports/report.html -v

# Allure report
pytest --project lct --alluredir=reports/allure-results -v
allure serve reports/allure-results
```
```

---

## Code Changes Required

### File 1: conftest.py

**Changes:**
1. Update `pytest_addoption` (already done ✅)
2. Update `pytest_configure` - add validation
3. Add `pytest_collection_modifyitems` - add auto-skip logic
4. Add `validate_project_config` fixture
5. Update `test_data` fixture - enhance

**Total lines to add: ~80 lines**

### File 2: pytest.ini

**Changes:**
1. Add project markers: `atcu`, `lct`, `sampark`, `swaraj`, `trio`

**Total lines to add: 5 lines**

### File 3: README.md

**Changes:**
1. Add "Running Tests by Project" section
2. Add examples

**Total lines to add: ~50 lines**

### File 4: New - Files/PROJECT_SETUP_GUIDE.md

**Content:**
- Setup instructions
- Directory structure
- Common tasks
- Troubleshooting

**Total lines: ~100 lines**

### File 5: New - Files/TEST_DATA_GUIDE.md

**Content:**
- Test data organization
- How to add new test data
- Loading test data in tests
- Best practices

**Total lines: ~80 lines**

---

## Testing the Implementation

### ⏱️ Test Phase 1: Basic Functionality (15 minutes)

```powershell
# Test 1: Default project (should be lct)
pytest tests/common/test_login_page.py -v

# Test 2: Explicit project flag
pytest --project lct tests/common/test_login_page.py -v

# Test 3: Different project
pytest --project atcu tests/common/test_login_page.py -v

# Test 4: Check config loaded
pytest --project atcu --collect-only -q  # Should show collection
```

### ⏱️ Test Phase 2: Auto-Skip Logic (10 minutes)

```powershell
# Test 5: Run with markers (should skip non-matching)
pytest --project lct -m lct -v

# Test 6: Run project-specific tests
pytest --project atcu -m atcu -v

# Test 7: Check skip summary
pytest --project lct -v --tb=short  # Should show skipped count
```

### ⏱️ Test Phase 3: Test Data Loading (10 minutes)

```powershell
# Test 8: Check test_data fixture loads
pytest --project lct -v -s tests/common/test_login_page.py

# Test 9: Verify different data per project
# (Add print statements to test to verify data)
pytest --project atcu -v -s tests/common/test_login_page.py

# Test 10: Fallback to common data
pytest --project sampark -v -s tests/common/test_login_page.py
```

### ⏱️ Test Phase 4: Validation (10 minutes)

```powershell
# Test 11: Invalid project name (should error)
pytest --project invalid_project tests/common/test_login_page.py 2>&1
# Should show: "Invalid project 'invalid_project'"

# Test 12: Missing config file (should warn)
pytest --project sampark tests/common/test_login_page.py -v
# Should show config validation results

# Test 13: Missing credentials (should error)
# (Temporarily remove BASE_URL from config, run, then restore)
```

### Expected Test Results
```
✅ Test 1: Common test runs with default project
✅ Test 2: Explicit --project flag works
✅ Test 3: Different project loads different config
✅ Test 4: Config values loaded correctly
✅ Test 5: Project markers work
✅ Test 6: Specific project tests run
✅ Test 7: Skip logic works
✅ Test 8-10: Test data loads per project
✅ Test 11: Validation rejects invalid projects
✅ Test 12-13: Config validation works
```

---

## Post-Implementation

### Checklist
- [ ] All test folders created with __init__.py
- [ ] Common tests moved to tests/common/
- [ ] Project markers added to tests
- [ ] pytest_collection_modifyitems added to conftest.py
- [ ] pytest_configure validation added
- [ ] validate_project_config fixture added
- [ ] test_data fixture enhanced
- [ ] Test data JSON files created for each project
- [ ] pytest.ini markers updated
- [ ] README.md updated
- [ ] PROJECT_SETUP_GUIDE.md created
- [ ] All tests run successfully with --project flag
- [ ] Documentation reviewed

### Verification Steps
```powershell
# 1. Verify folder structure
Get-Item tests/atcu/, tests/lct/, tests/common/ -ErrorAction SilentlyContinue

# 2. Run tests for each project
@("lct", "atcu", "sampark", "swaraj", "trio") | ForEach-Object {
    Write-Host "Testing project: $_"
    pytest --project $_ -v --tb=short
}

# 3. Verify marker filtering
pytest --project lct -m "not (atcu or sampark or swaraj or trio)" -v

# 4. Verify config loading
pytest --project atcu --co -q
```

### Future Enhancements
1. **GitHub Actions CI/CD**
   - Multi-project matrix testing
   - Parallel execution per project
   - Automatic report generation

2. **Test Data Management**
   - Excel to JSON converter
   - Test data versioning
   - Data validation schema

3. **Enhanced Reporting**
   - Per-project test reports
   - Cross-project comparison
   - Trend analysis

4. **Integration Tests**
   - Multi-project workflows
   - API contract testing
   - End-to-end scenarios

---

## Success Criteria

✅ **Phase 1 Complete** when:
- Folder structure created
- Tests organized by project
- No import errors

✅ **Phase 2 Complete** when:
- Markers added to pytest.ini
- Markers applied to tests
- pytest --co shows markers

✅ **Phase 3 Complete** when:
- pytest_collection_modifyitems works
- Tests auto-skip for wrong project
- Test count correct for each project

✅ **Phase 4 Complete** when:
- pytest_configure validates project
- Missing config raises error
- Config values printed on startup

✅ **Phase 5 Complete** when:
- test_data loads per project
- Fallback to common/ works
- Multiple JSON files load

✅ **Phase 6 Complete** when:
- README updated
- Documentation complete
- All examples work

✅ **Overall Complete** when:
- All 6 phases pass
- All verification steps pass
- User can run: `pytest --project atcu -v`

---

## Timeline Estimate

| Phase | Task | Time | Cumulative |
|-------|------|------|-----------|
| 1 | Create folder structure | 30 min | 30 min |
| 2 | Add pytest.ini markers | 10 min | 40 min |
| 3 | Add test markers | 20 min | 60 min |
| 4 | Add auto-skip logic | 30 min | 90 min |
| 5 | Add validation | 20 min | 110 min |
| 6 | Enhance test_data | 20 min | 130 min |
| 7 | Create test data files | 15 min | 145 min |
| 8 | Documentation | 20 min | 165 min |
| **Testing** | Run all tests | 30 min | **195 min (3.25 hrs)** |

---

## Troubleshooting

### Issue: `pytest: error: unrecognized arguments: --project`
**Solution:** Ensure conftest.py has `pytest_addoption` defined (already done)

### Issue: Tests not auto-skipping
**Solution:** Ensure `pytest_collection_modifyitems` added correctly to conftest.py

### Issue: Config values are None
**Solution:** Check if `config/{project}.yaml` file exists and has `base_url` key

### Issue: Test data not loading
**Solution:** Check `test_data/{project}/login.json` exists and has valid JSON

### Issue: Different results on different projects
**Solution:** Verify each project has different BASE_URL and credentials in YAML files

---

## Questions & Support

For implementation help:
1. Check existing conftest.py structure (lines 79-126)
2. Review existing YAML config files
3. Check test_data folder structure
4. Refer to pytest documentation: https://docs.pytest.org/

---

**End of Implementation Plan**
