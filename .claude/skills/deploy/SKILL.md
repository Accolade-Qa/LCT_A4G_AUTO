# Deploy skill

This skill helps automate deployment-related actions. Use when:

1. You need to generate deployment artifacts (Allure reports, video captures).
2. You want to verify `pytest` suites against production/staging URLs before tagging a release.

Typical flow:
- Install dependencies (`pip install -r requirements.txt`) and Playwright browsers.
- Run smoke tests with `pytest --alluredir=reports/allure-results` and ensure the `reports/` directory is clean before new output.
- Package screenshots/videos under `Artifacts/` if required.

Update `commands.md` when additional deploy steps are introduced so operators know how to trigger them manually.
