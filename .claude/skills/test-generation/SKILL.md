---
name: test-generation
description: Automatically create modular Playwright UI/API page object classes and pytest test suites following the project's POM design pattern, logger fixtures, and reporting structures.
version: 1.0.0
author: Antigravity
tags:
  - test-generation
  - automation
  - playwright
  - pytest
---

# Test Generation Skill

This skill guides the creation of modular Playwright UI/API page object classes and pytest test suites. It strictly enforces the repository's custom Page Object Model (POM), logging practices, test markers, and excel reporting integrations.

## When to Use
- Implementing automated test coverage for a new UI page or API endpoint.
- Extending existing test suites with new scenarios (smoke or regression).
- Generating regression test cases derived from resolved bug reports.

## Detailed Coding Style Guidelines

### 1. Page Object Design (`pages/`)
- **Base Inheritance**: All UI page classes must inherit from `BasePage` (`from pages.base_page import BasePage`).
- **Locators Definition**: Declare page element locators inside the constructor (`__init__`).
  - Prefer Playwright's native locators: `get_by_placeholder()`, `get_by_role()`, `get_by_text()`, `get_by_label()`.
  - Use regex matching for flexible locators (e.g., `page.get_by_role("button", name=re.compile(r"Save", re.IGNORECASE))`).
- **Logger Setup**: Always initialize a class-specific standard logger inside `__init__`:
  ```python
  self.logger = logging.getLogger(self.__class__.__name__)
  ```
- **Encapsulated Actions**: Page methods should encapsulate actions and wait states. Always log key actions (e.g., `self.logger.info("Clicking submit button")`) and use explicit wait states (e.g., `self.page.wait_for_load_state("networkidle")`).
- **Return Values**: UI action methods that check errors or fetch text should clean and return values (e.g., `.inner_text().strip().lower()`).

### 2. Test Class Design (`tests/`)
- **Structure**: Group related tests inside a class prefixed with `Test` (e.g., `class TestDeviceDashboard:`) using `PascalCase`.
- **Pytest Markers**: Annotate classes and test methods with relevant pytest markers:
  - `@pytest.mark.smoke`, `@pytest.mark.regression`, `@pytest.mark.auth`, `@pytest.mark.critical`, etc.
- **Autouse Logging Fixture**: Every test class must include the standard autouse lifecycle logger fixture:
  ```python
  @pytest.fixture(autouse=True)
  def log_test_case(self, request):
      """Automatically log test lifecycle events"""
      test_name = request.node.name
      logger.info("Starting %s test: %s", self.__class__.__name__, test_name)
      yield
      report = getattr(request.node, "rep_call", None)
      if report is None:
          logger.debug("Test finished without call report: %s", test_name)
      elif report.passed:
          logger.info("Test passed: %s", test_name)
      elif report.failed:
          logger.error("Test failed: %s", test_name)
      elif report.skipped:
          logger.warning("Test skipped: %s", test_name)
  ```
- **Custom Reporting**: Inject the `report_case` fixture into every test method. Call it right before the assertion to record test metadata (expected, actual, and description):
  ```python
  report_case(
      expected=expected_value,
      actual=actual_value,
      message="Description of the test validation check",
  )
  ```
- **Assertions**: Always write descriptive assert failure messages showing expected vs. actual values:
  ```python
  assert actual_value == expected_value, (
      f"Expected '{expected_value}', but got '{actual_value}'"
  )
  ```
- **Logging Inside Tests**: Write high-signal log messages:
  - `logger.info()` for primary test blocks (starting validation, ending validation).
  - `logger.debug()` for parameters, URLs, values loaded, and wait states.

---

## Code Templates

### 1. Reference Page Object Class
```python
import logging
import re
from pages.base_page import BasePage

class DeviceDetailsPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.logger = logging.getLogger(self.__class__.__name__)
        
        # Locators
        self.imei_input = page.get_by_placeholder("Enter IMEI")
        self.search_btn = page.get_by_role("button", name=re.compile(r"Search", re.IGNORECASE))
        self.result_status = page.locator(".status-value")
        self.error_msg = page.locator("mat-error")

    def search_device(self, imei):
        self.logger.info(f"Searching for device IMEI: {imei}")
        self.imei_input.fill(imei)
        self.search_btn.click()
        self.page.wait_for_load_state("networkidle")

    def get_status_text(self):
        self.result_status.wait_for(state="visible", timeout=5000)
        status = self.result_status.inner_text().strip()
        self.logger.debug(f"Retrieved device status: {status}")
        return status
```

### 2. Reference Test Class
```python
import pytest
from pages.device_details_page import DeviceDetailsPage
from config.config import BASE_URL, IMEI
from utils.logger import get_logger

logger = get_logger(__name__)

@pytest.mark.regression
class TestDeviceDetails:
    @pytest.fixture(autouse=True)
    def log_test_case(self, request):
        """Automatically log test lifecycle events"""
        test_name = request.node.name
        logger.info("Starting Device Details test: %s", test_name)
        yield
        report = getattr(request.node, "rep_call", None)
        if report and report.passed:
            logger.info("Device Details test passed: %s", test_name)
        elif report and report.failed:
            logger.error("Device Details test failed: %s", test_name)

    @pytest.mark.smoke
    def test_search_and_validate_device_status(self, page, report_case):
        """Validate search result and status for a configured device IMEI"""
        logger.info("Starting validation of device search status")
        
        details_page = DeviceDetailsPage(page)
        details_page.load(BASE_URL)
        
        expected_status = "Active"
        details_page.search_device(IMEI)
        actual_status = details_page.get_status_text()
        
        logger.debug(
            "Status validation check | expected=%s | actual=%s",
            expected_status,
            actual_status,
        )
        
        report_case(
            expected=expected_status,
            actual=actual_status,
            message="Verify device search result status is Active",
        )
        
        assert actual_status == expected_status, (
            f"Expected device status to be '{expected_status}' but got '{actual_status}'"
        )
        logger.info("Device status validation completed successfully")
```
