# Claude local notes

- **Purpose**: stash machine-specific details that should never be committed for other developers or agents.
- **Environment hints**: mirror the real `BASE_URL`, `DASHBOARD_URL`, and credential placeholders from `.env` when running locally. Keep values generic (e.g., `https://dashboard.staging.example`), then update the actual `.env` file outside source control.
- **Test data**: document any local test accounts, tokens, or fixtures that need to exist before Claude executes browser-heavy smoke suites.
- **Secrets**: avoid pasting API keys, passwords, or tokens here; instead, mention where the secure store lives (e.g., `Vault or 1Password entry "LCT A4G Playground"`).

Update this document only when new local setup context is created and you are confident it can stay private.
