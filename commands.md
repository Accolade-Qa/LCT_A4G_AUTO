# Commands Reference

## pytest

Runs all tests:
```bash
pytest
```

Runs tests in specific folder:
```bash
pytest tests/
```

Runs specific test file:
```bash
pytest tests/test_example.py
```

Runs specific test class:
```bash
pytest tests/test_example.py::TestClassName
```

Runs specific test function:
```bash
pytest tests/test_example.py::test_function_name
```

Runs multiple folders test cases:
```bash
pytest tests/unit tests/integration
```

Runs test with matching keyword:
```bash
pytest -k "login"
```

Runs test by marker:
```bash
pytest -m smoke
```

Stop on first failure:
```bash
pytest -x
```

Real world command usage:
```bash
pytest tests/unit -v -k "api" -x
```

## Common Commands

Remove the `__pycache__` folders:
```powershell
Get-ChildItem -Recurse -Directory -Filter "__pycache__" | Remove-Item -Recurse -Force
```

Set env variable to not have the `__pycache__` folder everywhere in the project:
```powershell
$env:PYTHONDONTWRITEBYTECODE=1
```

Generate the `.venv` in the project:
```bash
python -m venv .venv
```

Activate the virtual environment:
```powershell
.venv\Scripts\Activate.ps1
```

Upgrade pip:
```bash
python.exe -m pip install --upgrade pip
```

Install dependencies from requirements.txt file:
```bash
pip install -r .\requirements.txt
```

Hide `.xyz` folders from VS Code — add this line to settings.json file:
```json
"files.exclude": {
    "**/.xyz": true,
    "**/__pycache__": true,
    "**/.pytest_cache": true,
    "**/.venv": true
}
```