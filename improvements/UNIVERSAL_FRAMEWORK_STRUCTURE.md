# 🏗️ Universal Automation Framework - Folder Structure

## 📁 Complete Directory Layout

```
automation-framework/
│
├── core/                                    # ← SHARED CODE (ALL PROJECTS USE THIS)
│   ├── config/
│   │   ├── __init__.py
│   │   ├── base_config.py                  # Base configuration with env vars
│   │   └── global_var.py                   # Global paths and constants
│   │
│   ├── pages/                              # Reusable Page Objects
│   │   ├── __init__.py
│   │   ├── base_page.py                    # Base class for all pages
│   │   ├── login_page.py                   # Generic login page
│   │   ├── dashboard_page.py               # Generic dashboard
│   │   ├── device_details_page.py
│   │   ├── role_management_page.py
│   │   ├── ota_page.py
│   │   ├── model_page.py
│   │   └── api/
│   │       ├── __init__.py
│   │       ├── dashboard_api.py
│   │       └── sim_batch_details.py
│   │
│   ├── utils/                              # Reusable Helpers
│   │   ├── __init__.py
│   │   ├── helpers.py                      # Utility functions
│   │   ├── logger.py                       # Logging configuration
│   │   └── excel_report.py
│   │
│   ├── conftest_base.py                    # Base pytest fixtures
│   └── requirements.txt                    # Core dependencies
│
│
├── projects/
│   │
│   ├── lct-a4g-qa/                         # ← PROJECT 1 (QA ENVIRONMENT)
│   │   ├── .env                            # Project-specific credentials & URLs
│   │   ├── .env.example                    # Template for .env (commit to git)
│   │   ├── conftest.py                     # Project-specific fixture overrides
│   │   ├── pytest.ini                      # Project-specific pytest config
│   │   │
│   │   ├── tests/
│   │   │   ├── __init__.py
│   │   │   ├── test_login_page.py
│   │   │   ├── test_dashboard_page.py
│   │   │   ├── test_device_details_page.py
│   │   │   ├── test_role_management_page.py
│   │   │   ├── test_role_group_page.py
│   │   │   ├── test_ota_page.py
│   │   │   ├── test_model_page.py
│   │   │   ├── test_govt_server_page.py
│   │   │   └── test_sim_batch_data_details.py
│   │   │
│   │   ├── test_data/                      # Project-specific test data
│   │   │   ├── login_packet.json           # QA login data
│   │   │   ├── devices.json                # QA device data
│   │   │   └── roles.json                  # QA role data
│   │   │
│   │   ├── pages/                          # Project-specific page overrides (if any)
│   │   │   └── (Usually empty - uses core/pages)
│   │   │
│   │   └── Artifacts/                      # Test outputs (ignored in git)
│   │       ├── Screenshots/
│   │       ├── Logs/
│   │       ├── Videos/
│   │       └── Reports/
│   │
│   │
│   ├── lct-a4g-prod/                       # ← PROJECT 2 (PRODUCTION ENVIRONMENT)
│   │   ├── .env                            # Prod credentials & URLs
│   │   ├── .env.example
│   │   ├── conftest.py                     # Can override for prod-specific setup
│   │   ├── pytest.ini
│   │   │
│   │   ├── tests/
│   │   │   ├── __init__.py
│   │   │   ├── test_login_page.py
│   │   │   ├── test_dashboard_page.py
│   │   │   └── ... (same as QA)
│   │   │
│   │   ├── test_data/                      # Prod-specific test data
│   │   │   ├── login_packet.json           # Prod login data
│   │   │   ├── devices.json                # Prod device data
│   │   │   └── roles.json
│   │   │
│   │   └── Artifacts/                      # Prod test outputs
│   │       ├── Screenshots/
│   │       ├── Logs/
│   │       ├── Videos/
│   │       └── Reports/
│   │
│   │
│   └── another-project/                    # ← PROJECT 3 (ANOTHER ENVIRONMENT)
│       ├── .env
│       ├── .env.example
│       ├── conftest.py
│       ├── pytest.ini
│       ├── tests/
│       ├── test_data/
│       ├── pages/
│       └── Artifacts/
│
│
├── scripts/                                 # Utility scripts
│   ├── generate_reports.py
│   └── cleanup.py
│
├── .github/
│   └── workflows/
│       ├── reporting.yml
│       └── ci.yml
│
├── .gitignore                              # Ignore projects/.env, Artifacts/, .venv
├── README.md                               # Main documentation
└── requirements-dev.txt                    # For framework development

```

---

## 📝 What Goes in Each Folder

### 🔷 `core/` - SHARED ACROSS ALL PROJECTS

**Purpose:** Reusable code that doesn't change between projects

| Folder | Content | Example |
|--------|---------|---------|
| `core/config/` | Base configuration & paths | URLs patterns, browser settings |
| `core/pages/` | Generic page objects | Login, Dashboard, Device pages |
| `core/utils/` | Helper functions | Logger, random data generators |
| `core/conftest_base.py` | Base fixtures (fixtures all projects inherit) | Browser setup, auth fixtures |
| `core/requirements.txt` | Core dependencies | playwright, pytest, pandas |

**These files NEVER change per project.**

---

### 🟢 `projects/lct-a4g-qa/` - PROJECT-SPECIFIC

**Purpose:** QA Environment with specific credentials and test data

| File/Folder | Content | What It Looks Like |
|-------------|---------|------------------|
| `.env` | QA credentials & URLs | `BASE_URL=http://lct-a4g-qa.company.com` |
| `.env.example` | Template (safe to commit) | `BASE_URL=YOUR_URL_HERE` |
| `conftest.py` | QA-specific fixtures | Inherits from `core/conftest_base.py` |
| `tests/` | Same tests as other projects | `test_login_page.py`, `test_dashboard_page.py` |
| `test_data/` | QA-specific data | QA device IDs, QA user credentials |
| `pages/` | Overrides (usually empty) | Only if QA has different page behavior |
| `Artifacts/` | Test outputs (git-ignored) | Screenshots, logs, videos |

---

### 🟠 `projects/lct-a4g-prod/` - ANOTHER PROJECT

**Identical structure to lct-a4g-qa but with:**
- Different `.env` values (prod credentials, prod URLs)
- Different `test_data/` (prod devices, prod users)
- Same `tests/` (code is reused)
- Same page objects (from core)

---

## 📄 Detailed File Examples

### Example 1: `core/config/base_config.py`
```python
import os
from dotenv import load_dotenv

load_dotenv()

# URLs - can be overridden by .env in each project
BASE_URL = os.getenv("BASE_URL", "http://localhost:3000")

# Build URLs from BASE_URL if not explicitly set
DASHBOARD_URL = os.getenv(
    "DASHBOARD_URL", 
    f"{BASE_URL}/device-dashboard-page"
)
ROLE_MANAGEMENT_URL = os.getenv(
    "ROLE_MANAGEMENT_URL", 
    f"{BASE_URL}/user-role"
)
OTA_URL = os.getenv("OTA_URL", f"{BASE_URL}/ota-batch-page")

# Credentials - each project has its own
USERNAME = os.getenv("APP_USERNAME")
PASSWORD = os.getenv("APP_PASSWORD")

# Browser settings
BROWSER = os.getenv("BROWSER", "chromium")
HEADLESS = os.getenv("HEADLESS", "false").lower() == "true"

# Project identifier for logging
SUITE_NAME = os.getenv("SUITE_NAME", "AUTOMATION")

# API settings
API_BASE_URL = os.getenv("API_BASE_URL", f"{BASE_URL}:9090")
```

---

### Example 2: `projects/lct-a4g-qa/.env`
```env
# QA Environment
SUITE_NAME=LCT_A4G_QA
BASE_URL=http://lct-a4g-qa.accoladeelectronics.com

# QA Credentials
APP_USERNAME=qa_admin
APP_PASSWORD=qa_password_123

# QA URLs (will use defaults from base_config.py)
DASHBOARD_URL=http://lct-a4g-qa.accoladeelectronics.com/device-dashboard-page
ROLE_MANAGEMENT_URL=http://lct-a4g-qa.accoladeelectronics.com/user-role
OTA_URL=http://lct-a4g-qa.accoladeelectronics.com/ota-batch-page

# Browser
BROWSER=chromium
HEADLESS=false
SCREENSHOT_ON_FAILURE=true
LOG_LEVEL=INFO
```

---

### Example 3: `projects/lct-a4g-prod/.env`
```env
# PRODUCTION Environment
SUITE_NAME=LCT_A4G_PROD
BASE_URL=http://lct-a4g-prod.accoladeelectronics.com

# PROD Credentials (different user)
APP_USERNAME=prod_admin
APP_PASSWORD=prod_password_999

# PROD URLs
DASHBOARD_URL=http://lct-a4g-prod.accoladeelectronics.com/device-dashboard-page
ROLE_MANAGEMENT_URL=http://lct-a4g-prod.accoladeelectronics.com/user-role
OTA_URL=http://lct-a4g-prod.accoladeelectronics.com/ota-batch-page

# Browser
BROWSER=chromium
HEADLESS=true
SCREENSHOT_ON_FAILURE=true
LOG_LEVEL=WARNING
```

---

### Example 4: `projects/lct-a4g-qa/conftest.py`
```python
import sys
from pathlib import Path

# Add core to Python path
CORE_DIR = Path(__file__).parent.parent.parent / "core"
sys.path.insert(0, str(CORE_DIR))

# Import base fixtures from core
from conftest_base import *

# Optional: Override if QA needs custom setup
# (Most projects won't need this)
```

---

### Example 5: `projects/lct-a4g-qa/pytest.ini`
```ini
[pytest]
# Project-specific pytest configuration
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*

# QA-specific markers
markers =
    smoke: Quick smoke tests
    regression: Full regression suite
    qa: QA environment only

addopts = 
    -v
    --tb=short
```

---

### Example 6: `projects/lct-a4g-qa/test_data/devices.json`
```json
{
  "devices": [
    {
      "id": "QA-DEVICE-001",
      "name": "QA Test Device 1",
      "imei": "351234567890123",
      "model": "Model-A"
    },
    {
      "id": "QA-DEVICE-002",
      "name": "QA Test Device 2",
      "imei": "351234567890124",
      "model": "Model-B"
    }
  ]
}
```

---

### Example 7: `projects/lct-a4g-prod/test_data/devices.json`
```json
{
  "devices": [
    {
      "id": "PROD-DEVICE-101",
      "name": "Production Device 1",
      "imei": "351111111111111",
      "model": "Model-A"
    },
    {
      "id": "PROD-DEVICE-102",
      "name": "Production Device 2",
      "imei": "351111111111112",
      "model": "Model-B"
    }
  ]
}
```

---

### Example 8: `projects/lct-a4g-qa/tests/test_dashboard_page.py`
```python
from pages.dashboard_page import DashboardPage
from utils.helpers import Helpers

class TestDashboardPage:
    def test_dashboard_loads(self, page):
        """Test dashboard page loads correctly"""
        dashboard = DashboardPage(page)
        assert dashboard.is_page_loaded()
        
    def test_device_list_visible(self, page):
        """Test device list is visible"""
        dashboard = DashboardPage(page)
        assert dashboard.is_device_list_visible()
```

---

## 🎯 Comparison: Same Test in Both Projects

### In `projects/lct-a4g-qa/tests/test_login_page.py`
```python
def test_valid_login(self, page):
    """Test QA login"""
    login = LoginPage(page)
    # Uses QA credentials from projects/lct-a4g-qa/.env
    assert login.is_page_loaded()
```

### In `projects/lct-a4g-prod/tests/test_login_page.py`
```python
def test_valid_login(self, page):
    """Test Production login"""
    login = LoginPage(page)
    # Uses PROD credentials from projects/lct-a4g-prod/.env
    # EXACT SAME CODE - Different credentials via .env!
    assert login.is_page_loaded()
```

**Key Point:** Test code is 100% identical. Only `.env` changes!

---

## 🚀 How to Run Tests

```bash
# Run QA tests
cd projects/lct-a4g-qa
pytest tests/

# Run PROD tests
cd projects/lct-a4g-prod
pytest tests/

# Run all projects
pytest projects/*/tests/

# Run specific test in QA
cd projects/lct-a4g-qa
pytest tests/test_login_page.py::test_valid_login
```

---

## 📋 Summary: What Changes Per Project

| Item | Changes? | Where |
|------|----------|-------|
| Test code (test_login_page.py) | ❌ NO | Same in all projects |
| Page objects (login_page.py) | ❌ NO | Shared in `core/pages/` |
| Credentials | ✅ YES | Each project's `.env` |
| URLs | ✅ YES | Each project's `.env` |
| Test data (devices.json) | ✅ YES | `projects/xxx/test_data/` |
| Fixtures | ❌ NO (mostly) | Base in core, only override if needed |

---

## 📌 .gitignore Configuration

```
# Root .gitignore
.venv/
*.pyc
__pycache__/

# Project-specific (never commit)
projects/**/.env
projects/**/Artifacts/
projects/**/reports/

# IDE
.vscode/
.idea/
*.swp
```

---

## ✅ Folder Creation Checklist

```
☐ Create core/config/
☐ Create core/pages/
☐ Create core/utils/
☐ Create core/conftest_base.py
☐ Create core/requirements.txt

☐ Create projects/lct-a4g-qa/tests/
☐ Create projects/lct-a4g-qa/test_data/
☐ Create projects/lct-a4g-qa/.env
☐ Create projects/lct-a4g-qa/conftest.py
☐ Create projects/lct-a4g-qa/Artifacts/

☐ Create projects/lct-a4g-prod/tests/
☐ Create projects/lct-a4g-prod/test_data/
☐ Create projects/lct-a4g-prod/.env
☐ Create projects/lct-a4g-prod/conftest.py
☐ Create projects/lct-a4g-prod/Artifacts/

☐ Update .gitignore
☐ Create README.md
```

---

This is the complete structure! Ready to set it up? 🎯
