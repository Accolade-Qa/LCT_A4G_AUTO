# Deploy command guidance

1. **Scope**: Use this when the CI/CD pipeline is ready, smoke tests pass, and test artifacts (Allure) are generated.
2. **Checklist before deploying**:
   - Run `pytest --alluredir=reports/allure-results` and confirm there are no failures.
   - Confirm the `.env` file matches the target environment (staging/prod) and that the Playwright browsers targeted by the release are installed.
   - Update `commands.md` or `README.md` if new manual steps are required for deployment.
3. **Artifacts**: bundle `reports/allure-results` and any failure screenshots into the release notes.
4. **Post-deploy validation**: hit the same smoke tests used locally with `pytest tests/test_dashboard_page.py -k dashboard` to ensure the core flows still pass in the deployed endpoint.
