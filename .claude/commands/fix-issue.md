# Fix-issue guidance

1. **Trigger**: Use this when you are asked to resolve a failing test, flaky step, or user-reported bug.
2. **Investigate**:
   - Run the relevant pytest suite (e.g., `pytest tests/test_login_page.py::test_login`) in isolation to confirm the failure and inspect the captured screenshot/video.
   - Check `config/config.py` and `utils/helpers.py` for shared helpers that might need adjustment.
3. **Resolve**:
   - Update page objects under `pages/` if locators or flows changed.
   - Add, adjust, or remove asserts in `tests/` to match expected behavior.
4. **Verify**:
   - Re-run the full suite that touched the change.
   - Make sure `SCREENSHOT_ON_FAILURE` and `VIDEO_RECORDING` remain in their current default states unless there is a reason to toggle them.
5. **Document**: Note the issue number/description and root cause in `commands.md` or `README.md` if the fix requires manual instructions for future troubleshooting.
