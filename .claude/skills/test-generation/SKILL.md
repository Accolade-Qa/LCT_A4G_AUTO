# Test Generation Skill

This skill automates the creation of pytest test cases and supporting page objects from feature descriptions.

## When to use
- New feature requires test coverage
- Expanding existing test suite with new workflows
- Regression test generation from bug reports
- Batch test case generation from requirements

## Execution checklist

1. **Input**: Feature description or user story (e.g., "Test the device filter by status")
2. **Analyze existing patterns**:
   - Read one existing test file to understand fixture usage (e.g., `tests/test_dashboard_page.py`)
   - Read corresponding page object (e.g., `pages/dashboard_page.py`)
   - Extract locators, helper methods, assertion patterns
3. **Generate artifacts**:
   - Create/update `pages/<feature>_page.py` with Page Object Model
   - Create `tests/test_<feature>.py` with pytest test cases
   - Ensure fixtures from `conftest.py` are used correctly
4. **Apply standards**:
   - Follow PEP 8 and naming: `test_<action>_<scenario>` (e.g., `test_login_with_invalid_credentials`)
   - Use `@pytest.mark.smoke` or `@pytest.mark.regression` if appropriate
   - Include docstrings with test intent
   - Use page object helpers instead of inline Playwright commands
5. **Validation**:
   - Run `pytest tests/test_<feature>.py -v` to validate syntax
   - Verify imports resolve (pages, conftest fixtures)
   - Ensure all waits/assertions follow existing patterns

## Output structure

Example generated test file:
```python
import pytest
from pages.<feature>_page import <Feature>Page

class Test<Feature>:
    """Test suite for <feature> functionality."""
    
    @pytest.mark.smoke
    def test_<action>_<scenario>(self, <fixture_name>):
        """Test description: <behavior>."""
        # arrange
        <fixture_name>.<setup_action>()
        
        # act
        <fixture_name>.<user_action>()
        
        # assert
        assert <fixture_name>.<get_state>() == expected
```

## Integration with CI
After test generation:
1. Add test file to Git: `git add tests/test_<feature>.py`
2. Run locally: `pytest tests/test_<feature>.py -v`
3. Commit with message: `feat: add tests for <feature>`
4. GitHub Actions will pick it up and run it in CI
