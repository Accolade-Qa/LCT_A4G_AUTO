---
paths:
  - requirements.txt
  - .env*
  - conftest.py
  - .claude/**/*
---
# Security Reviewer Guidance

Focus on securing automation credentials and environment isolation:
- **Secrets Review**: Ensure `.env` is not committed and sensitive values remain outside `CLAUDE.md`/`CLAUDE.local.md`. Flag credentials found in code files (e.g., hard-coded passwords or tokens).
- **Dependency Hygiene**: Verify dependencies in `requirements.txt` are pinned and check for known vulnerabilities if requested.
- **Playwright Safety**: Check Playwright launch options in `conftest.py` for safe defaults (e.g., `--no-sandbox` only in CI, avoid `--disable-web-security` unless required).
- **Reporting Security**: Confirm that test artifacts (screenshots, traces, HTML/Excel reports) are stored under `reports/` and do not leak sensitive credentials or personal identifiable data.
- **Documentation**: Document any findings with reproduction steps and references to the files involved.
