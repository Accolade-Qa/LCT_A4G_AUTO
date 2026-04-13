# API conventions

- The automation suite exercises the LCT-A4G dashboard through the browser; there is no dedicated API client in this repo.
- When integrating with backend endpoints (e.g., for setup/cleanup), prefer the helpers inside `utils/helpers.py` so token refresh and retry logic stays centralized.
- Keep environment-specific URLs configurable through `.env` so the same scripts can run against staging or production with minimal edits.
