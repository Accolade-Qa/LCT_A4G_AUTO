---
paths:
  - pages/api/**/*.py
  - tests/api_test/**/*.py
---
# API Conventions

- The automation suite exercises the LCT-A4G dashboard through both browser automation and dedicated backend API clients.
- Dedicated API clients reside under `pages/api/` (e.g., `api_client.py` and service-specific clients like `login_api.py` or `sim_batch_api.py`).
- API tests reside under `tests/api_test/` (e.g., `test_sim_batch_api.py`).
- When integrating with backend endpoints (e.g., for test setup or direct validation), prefer utilizing these existing API clients and the helpers inside `utils/helpers.py` so token refresh and retry logic stays centralized.
- Keep environment-specific URLs configurable through `.env` and load them via `config/config.py`.
