---
name: security-review
description: Perform dependency checks, check for committed credentials/secrets, and verify browser execution sandbox options.
version: 1.0.0
author: Antigravity
tags:
  - security
  - code-audit
  - configuration-hardening
---

# Security-Review Skill

This skill guides the auditing of the repository's security posture, focusing on secrets management, dependency pinning, and secure Playwright configurations.

## When to Use
- Validating a pull request or code change that introduces new packages or environment configurations.
- Auditing the repository for committed secrets, credentials, or API keys.
- Reviewing browser capabilities and launch arguments to prevent vulnerability exposure during automated runs.

## Security Audit Steps

### 1. Secrets & Credentials Scan
Ensure no sensitive data is leaked or committed to version control:
- **Scan Local Files**: Verify `.env` is NOT checked in (confirm `.gitignore` excludes it).
- **Hard-coded Secrets check**: Scan code files, configuration files (`config/config.py`), test data directories, and instructions (`CLAUDE.md`, `CLAUDE.local.md`) for hard-coded values:
  - Look for keywords: `APP_PASSWORD`, `PASSWORD`, `token`, `secret`, `key`.
  - Stash credentials safely or write instructions for storing them in secure systems (Vault, 1Password, or Github Secrets).
- **Report Validation**: Verify that screenshots captured during failures (under `reports/screenshots/`) or trace videos do not leak passwords or authentication headers.

### 2. Dependency Audit
Ensure package dependencies are safe and pinned:
- **Pinning check**: Verify that dependencies listed in `requirements.txt` are explicitly pinned to specific versions (e.g., `pytest==7.4.0`) to prevent supply chain updates from breaking or compromising builds.
- **Dependency checks**: Run vulnerability scanners if requested (e.g., `pip-audit` or `safety`):
  ```powershell
  pip-audit -r requirements.txt
  ```

### 3. Browser Launch Configuration Hardening
Review `conftest.py` for Playwright launch arguments:
- **Sandbox Isolation**: Ensure options like `--no-sandbox` or `--disable-setuid-sandbox` are only enabled in headless CI environments where they are strictly required. They must not be configured globally for local headed runs.
- **Web Security**: Avoid using arguments like `--disable-web-security` (which bypasses Same-Origin Policy) unless testing specific cross-origin endpoints.
- **Zoom & Execution policies**: Check that scripts injected into page contexts (such as zoom injection or execution policies) do not run unchecked code or evaluate unverified inputs.
