---
paths:
  - tests/**/*.py
  - pages/**/*.py
---
# Fix-Issue Guidance

- **Trigger**: Use these guidelines when resolving a failing test, flaky step, or user-reported bug.
- **Investigate**:
  - Run the relevant pytest suite (e.g., `pytest tests/test_login_page.py::test_login`) in isolation to confirm the failure and inspect the captured screenshot/video.
  - Check `config/config.py` and `utils/helpers.py` for shared helpers that might need adjustment.
- **Resolve**:
  - Update page objects under `pages/` if UI locators or interaction flows changed.
  - Add, adjust, or remove assertions in `tests/` to match expected behavior.
- **Verify**:
  - Re-run the full suite that touched the change to verify the fix.
  - Make sure `SCREENSHOT_ON_FAILURE` and `VIDEO_RECORDING` remain in their default states unless explicitly requested.
