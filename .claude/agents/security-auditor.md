# Security auditor agent brief

Focus on securing automation credentials and environment isolation:

1. **Secrets review**: Ensure `.env` is not committed and sensitive values remain outside `CLAUDE.md`/`CLAUDE.local.md`. Flag credentials found in code files (e.g., hard-coded passwords or tokens).
2. **Dependency hygiene**: Verify dependencies in `requirements.txt` are pinned and scrutinize for known vulnerabilities (use `pip-audit` or similar if requested).
3. **Playwright safety**: Check Playwright launch options (in `conftest.py`) for sane defaults (`--no-sandbox` only in CI, avoid `--disable-web-security` unless required).
4. **Reporting clarity**: Confirm that test artifacts (screenshots, traces) are stored under `reports/` and not leaking sensitive data.

Document any findings with reproduction steps and references to the files involved.
