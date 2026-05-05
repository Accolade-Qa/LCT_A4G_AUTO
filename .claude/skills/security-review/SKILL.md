# Security-review skill

Use this skill whenever a request emphasizes dependency vulnerabilities, secrets, or configuration hardening.

Steps:
1. Scan `requirements.txt` for well-maintained libraries and note any outdated or unsafe versions.
2. Verify `.env` keys are not stored in version control and describe how to source them securely (e.g., mention `.env` template and Vault, if applicable).
3. Check `conftest.py` for launch flags that impact browser isolation and memory; ensure no insecure defaults are introduced.
4. Summarize any severe issues with file references so Claude agents can act on them.

Keep the skill focused on preventive reviews; refer to `security-auditor` agent guidance for deeper investigations.
