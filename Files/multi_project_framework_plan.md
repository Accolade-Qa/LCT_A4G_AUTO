# Multi-Project Playwright + Pytest Framework Plan

## Goal

Support multiple projects/environments using:

- One framework
- One set of page objects
- One test suite
- Multiple config files
- Multiple test-data folders

---

# Proposed Structure

```text
automation-framework/

├── config/
│   ├── lct.yaml
│   ├── sampark.yaml
│   ├── swaraj.yaml
│   └── trio.yaml
│
├── testdata/
│   ├── lct/
│   │   └── login.json
│   │
│   ├── sampark/
│   │   └── login.json
│   │
│   ├── swaraj/
│   │   └── login.json
│   │
│   └── trio/
│       └── login.json
│
├── pages/
│   ├── base_page.py
│   ├── login_page.py
│   ├── dashboard_page.py
│   └── ...
│
├── api/
│   ├── api_client.py
│   ├── login_api.py
│   └── ...
│
├── utils/
│   ├── logger.py
│   └── helpers.py
│
├── tests/
│   ├── test_login.py
│   ├── test_dashboard.py
│   └── ...
│
├── conftest.py
├── pytest.ini
└── requirements.txt
```

---

# Config Files

## config/lct.yaml

```yaml
project: lct

base_url: "https://lct-qa.com"

username: "admin"
password: "admin123"

browser: "chromium"
```

## config/sampark.yaml

```yaml
project: sampark

base_url: "https://sampark-qa.com"

username: "sampark_admin"
password: "pass123"

browser: "chromium"
```

---

# Test Data Example

## testdata/lct/login.json

```json
{
  "expected_dashboard_title": "LCT Dashboard"
}
```

## testdata/sampark/login.json

```json
{
  "expected_dashboard_title": "Sampark Dashboard"
}
```

---

# Actual Configuration & Loading Implementation

The project implements a dynamic, centralized configuration approach combining YAML files and environment variables, handled by a dedicated `config/config.py` module and reloaded at runtime via `conftest.py`.

## 1. Centralized Config Module (`config/config.py`)
Rather than parsing YAML manually inside test fixtures, configuration values are centralized in `config/config.py`. Key behaviors include:
- **Project Selection:** Determines the project to run by reading the `PROJECT` environment variable (defaults to `lct`).
- **YAML Loading:** Looks for a config file named `config/{PROJECT}.yaml` and parses it into a dictionary (`_PROJECT_CONFIG`).
- **Resolution Precedence:** Configuration constants (e.g., `BASE_URL`, `USERNAME`, `PASSWORD`) are resolved using helper functions `_get()` and `_get_bool()` which prioritize settings in the project's YAML configuration, falling back to environment variables or defaults if not set.

```python
import os
from pathlib import Path
import yaml
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent
load_dotenv(dotenv_path=ROOT.parent / ".env")

PROJECT = os.getenv("PROJECT", "lct").lower()
PROJECT_CONFIG_PATH = ROOT / f"{PROJECT}.yaml"

_PROJECT_CONFIG = {}
if PROJECT_CONFIG_PATH.exists():
    with PROJECT_CONFIG_PATH.open("r", encoding="utf-8") as config_file:
        _PROJECT_CONFIG = yaml.safe_load(config_file) or {}

def _get(key, default=None):
    project_value = _PROJECT_CONFIG.get(key.lower())
    if project_value is not None:
        return project_value
    return os.getenv(key, default)

def _get_bool(key, default=False):
    project_value = _PROJECT_CONFIG.get(key.lower())
    if isinstance(project_value, bool):
        return project_value
    if project_value is not None:
        return str(project_value).lower() == "true"
    env_value = os.getenv(key)
    if env_value is not None:
        return str(env_value).lower() == "true"
    return default

# Example variable mappings
BASE_URL = _get("BASE_URL")
USERNAME = _get("USERNAME", _get("APP_USERNAME"))
PASSWORD = _get("PASSWORD", _get("APP_PASSWORD"))
# ...
```

## 2. Dynamic Reloading via Pytest (`conftest.py`)
To support switching projects at test execution time via CLI command (`--project=project_name`), `conftest.py` configures pytest to update the environment variables and dynamically reload the configuration module:
- **CLI Registration:** Adds the `--project` option to pytest (falling back to the `PROJECT` env variable).
- **Reload on Initialization:** In `pytest_configure`, the chosen project name is injected into `os.environ["PROJECT"]`, and the `config.config` module is reloaded via `importlib.reload`. This forces the module to re-evaluate and load the correct `{PROJECT}.yaml` configuration file.

```python
import importlib
import os
import config.config as config_module

def pytest_addoption(parser):
    parser.addoption(
        "--project",
        action="store",
        default=os.getenv("PROJECT", "lct"),
        help="Project name to select the configuration",
    )

def pytest_configure(config):
    project = config.getoption("--project", os.getenv("PROJECT", "lct")).lower()
    os.environ["PROJECT"] = project
    # Dynamically reload config to load the selected project yaml file
    importlib.reload(config_module)
```

## 3. Project Configuration & Test Data Fixtures (`conftest.py`)
The reloaded configurations are exposed to test functions via `pytest` fixtures:
- `project_config` gathers configuration properties from the reloaded `config_module`.
- `test_data` loads corresponding JSON test data from `test_data/{project}/login.json`.

```python
@pytest.fixture(scope="session")
def project_config():
    return {
        "project": os.getenv("PROJECT", "lct").lower(),
        "base_url": config_module.BASE_URL,
        "username": config_module.USERNAME,
        "password": config_module.PASSWORD,
        # ... maps other loaded configurations ...
    }

@pytest.fixture(scope="session")
def test_data(project_config):
    project = project_config["project"]
    path = Path(__file__).parent / "test_data" / project / "login.json"
    if path.exists():
        with path.open("r", encoding="utf-8") as json_file:
            return json.load(json_file)
    return {}
```

---

# Root conftest.py (Proposed)

## Add Project Option

```python
def pytest_addoption(parser):
    parser.addoption(
        "--project",
        action="store",
        default="lct",
        help="Project Name"
    )
```

---

## Load YAML Configuration

```python
import yaml
import pytest

@pytest.fixture(scope="session")
def project_config(request):

    project = request.config.getoption("--project")

    config_path = f"config/{project}.yaml"

    with open(config_path, "r") as file:
        config = yaml.safe_load(file)

    return config
```

---

## Load Project Test Data

```python
import json
from pathlib import Path

@pytest.fixture(scope="session")
def test_data(project_config):

    project = project_config["project"]

    file_path = Path(
        f"testdata/{project}/login.json"
    )

    with open(file_path) as file:
        return json.load(file)
```

---

# Playwright Browser Fixture

```python
import pytest
from playwright.sync_api import sync_playwright

@pytest.fixture(scope="session")
def browser(project_config):

    with sync_playwright() as p:

        browser_name = project_config["browser"]

        if browser_name == "firefox":
            browser = p.firefox.launch(headless=False)

        elif browser_name == "webkit":
            browser = p.webkit.launch(headless=False)

        else:
            browser = p.chromium.launch(headless=False)

        yield browser

        browser.close()
```

---

# Context Fixture

```python
@pytest.fixture
def context(browser):

    context = browser.new_context()

    yield context

    context.close()
```

---

# Page Fixture

```python
@pytest.fixture
def page(context):

    page = context.new_page()

    yield page

    page.close()
```

---

# Login Page Example

## pages/login_page.py

```python
class LoginPage:

    def __init__(self, page):
        self.page = page

    def open(self, url):
        self.page.goto(url)

    def login(self, username, password):

        self.page.fill("#username", username)
        self.page.fill("#password", password)

        self.page.click("#login-btn")

    def is_logged_in(self):

        return self.page.locator(
            "text=Dashboard"
        ).is_visible()
```

---

# Login Page Fixture

```python
from pages.login_page import LoginPage

@pytest.fixture
def login_page(page):

    return LoginPage(page)
```

---

# Example Test

## tests/test_login.py

```python
def test_login(
    login_page,
    project_config,
    test_data
):

    login_page.open(
        project_config["base_url"]
    )

    login_page.login(
        project_config["username"],
        project_config["password"]
    )

    assert login_page.is_logged_in()

    expected_title = (
        test_data["expected_dashboard_title"]
    )

    assert expected_title is not None
```

---

# Running Commands

## Run LCT

```bash
pytest --project=lct
```

## Run Sampark

```bash
pytest --project=sampark
```

## Run Swaraj

```bash
pytest --project=swaraj
```

## Run Trio

```bash
pytest --project=trio
```

---

# Run Single Test

```bash
pytest tests/test_login.py --project=lct
```

---

# Run Smoke Tests

```bash
pytest -m smoke --project=lct
```

---

# Future Improvements

1. Add Allure Reporting
2. Add Environment Selection (QA/UAT/PROD)
3. Add API Fixtures
4. Add Database Fixtures
5. Add Parallel Execution (pytest-xdist)
6. Add Jenkins/GitHub Actions Pipeline
7. Add Retry Logic
8. Add Screenshot on Failure
9. Add Video Recording
10. Add Centralized Logging

---

# Migration Strategy

Step 1:
Move all common page objects into one pages folder.

Step 2:
Move all common tests into one tests folder.

Step 3:
Create one YAML per project.

Step 4:
Create one testdata folder per project.

Step 5:
Replace hardcoded URLs, usernames and passwords with project_config fixture.

Step 6:
Execute using:

pytest --project=lct
pytest --project=sampark
pytest --project=swaraj
pytest --project=trio

Result:

- One framework
- One maintenance point
- Unlimited projects/environments
- No duplicated tests
