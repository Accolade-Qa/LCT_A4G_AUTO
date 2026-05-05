# Commands Reference

## pytest

Run all tests:
```bash
pytest
```

Run specific test file:
```bash
pytest tests/test_login_page.py
```

Run test with keyword match:
```bash
pytest -k "login"
```

Run tests with verbose output:
```bash
pytest -v
```

Run tests and stop on first failure:
```bash
pytest -x
```

Run tests in parallel (auto workers):
```bash
pytest -n auto
```

Run tests with Allure reporting:
```bash
pytest --alluredir=reports/allure-results
```

Run tests with HTML report:
```bash
pytest --html=reports/report.html --self-contained-html
```

## Setup & Environment

Create virtual environment:
```bash
python -m venv .venv
```

Activate virtual environment (PowerShell):
```powershell
.venv\Scripts\Activate.ps1
```

Install dependencies:
```bash
pip install -r requirements.txt
```

Install Playwright browsers:
```bash
playwright install
```

## Docker

Build Docker image:
```bash
docker build -t lct-a4g-automation .
```

Run all tests in container:
```bash
docker run --rm lct-a4g-automation
```

Run tests with .env file:
```bash
docker run --rm --env-file .env lct-a4g-automation
```

Run specific test in container:
```bash
docker run --rm lct-a4g-automation pytest tests/test_login_page.py
```

Run tests with volume mount for reports:
```bash
docker run --rm -v %cd%\reports:/app/reports lct-a4g-automation pytest --alluredir=reports/allure-results
```

Run tests in parallel inside container:
```bash
docker run --rm lct-a4g-automation pytest -n auto
```

View running containers:
```bash
docker ps
```

View container logs:
```bash
docker logs <container_id>
```

Stop container:
```bash
docker stop <container_id>
```