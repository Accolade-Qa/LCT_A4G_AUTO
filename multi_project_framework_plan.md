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

# Root conftest.py

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
