# LCT-A4G Automation Testing Framework

[![Playwright](https://img.shields.io/badge/Playwright-45ba4b?style=for-the-badge&logo=playwright&logoColor=white)](https://playwright.dev/)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![pytest](https://img.shields.io/badge/pytest-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white)](https://pytest.org/)
[![Allure](https://img.shields.io/badge/Allure-FF6B35?style=for-the-badge&logo=allure&logoColor=white)](https://docs.qameta.io/allure/)

A robust end-to-end automation testing framework built with **Playwright** and **pytest** for testing the LCT-A4G Device Dashboard application.

## 🚀 Features

- **Modern UI Automation**: Built with Playwright for reliable cross-browser testing
- **Page Object Model**: Well-structured page objects for maintainable test code
- **Comprehensive Reporting**: Allure reports with screenshots and video recordings
- **Parallel Execution**: pytest-xdist support for faster test execution
- **Configuration Management**: Environment-based configuration with .env support
- **Screenshot on Failure**: Automatic screenshot capture for failed tests
- **Cross-Browser Support**: Chromium, Firefox, and WebKit support
- **CI/CD Ready**: Optimized for continuous integration pipelines

## 📋 Prerequisites

- **Python 3.8+**
- **Git** (for cloning the repository)
- **Virtual Environment** (recommended)

## 🛠️ Installation & Setup

### 1. Clone the Repository
```bash
git clone <repository-url>
cd LCT_A4G_AUTO
```

### 2. Create Virtual Environment
```bash
# Windows
python -m venv .venv

# Linux/Mac
python3 -m venv venv
```

### 3. Activate Virtual Environment
```bash
# Windows (PowerShell)
.venv\Scripts\Activate.ps1

# Windows (Command Prompt)
.venv\Scripts\activate.bat

# Linux/Mac
source venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Install Playwright Browsers
```bash
playwright install
```

### 6. Environment Configuration
Create a `.env` file in the root directory:
```env
# Application URLs
BASE_URL=https://your-app-url.com
DASHBOARD_URL=https://your-app-url.com/device-dashboard-page

# Authentication
APP_USERNAME=your_username
APP_PASSWORD=your_password

# Browser Configuration
BROWSER=chromium
HEADLESS=false

# Test Configuration
SCREENSHOT_ON_FAILURE=true
LOG_LEVEL=INFO
VIDEO_RECORDING=false
```

## 📁 Project Structure

```
LCT_A4G_AUTO/
├── 📄 README.md                 # Project documentation
├── 📄 requirements.txt          # Python dependencies
├── 📄 pytest.ini               # pytest configuration
├── 📄 setup.sh                 # Setup script for Linux/Mac
├── 📄 commands.md              # Common commands reference
├── 📄 conftest.py              # pytest fixtures and configuration
├── 📁 config/                  # Configuration files
│   ├── 📄 config.py           # Environment configuration
│   └── 📄 global_var.py       # Global variables
├── 📁 pages/                   # Page Object Model classes
│   ├── 📄 base_page.py        # Base page class
│   ├── 📄 login_page.py       # Login page object
│   └── 📄 dashboard_page.py   # Dashboard page object
├── 📁 tests/                   # Test cases
│   ├── 📄 test_login_page.py  # Login tests
│   └── 📄 test_dashboard_page.py # Dashboard tests
├── 📁 utils/                   # Utility functions
│   └── 📄 helpers.py          # Helper methods
└── 📁 reports/                 # Test reports and artifacts
```

## ⚙️ Configuration

### Browser Options
- `BROWSER`: `chromium` (default), `firefox`, `webkit`
- `HEADLESS`: `true`/`false` - Run browser in headless mode

### Test Options
- `SCREENSHOT_ON_FAILURE`: `true`/`false` - Capture screenshots on test failure
- `VIDEO_RECORDING`: `true`/`false` - Record test videos
- `LOG_LEVEL`: `DEBUG`, `INFO`, `WARNING`, `ERROR`

### Browser Launch Parameters
The framework supports various browser launch arguments for enhanced testing:

```python
# In conftest.py, you can add:
args=[
    "--start-maximized",           # Maximize browser window
    "--disable-web-security",      # Disable CORS for testing
    "--no-sandbox",                # Useful in CI environments
    "--disable-dev-shm-usage",     # Fix resource issues
    "--disable-gpu",               # Disable GPU acceleration
]
```

## 🧪 Running Tests

### Basic Test Execution
```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_login_page.py

# Run specific test function
pytest tests/test_login_page.py::test_login

# Run tests with keyword filter
pytest -k "login"

# Run tests in verbose mode
pytest -v

# Stop on first failure
pytest -x

# Run with detailed output
pytest -s
```

### Parallel Execution
```bash
# Run tests in parallel (using all CPU cores)
pytest -n auto

# Run with specific number of workers
pytest -n 4
```

### Browser-Specific Tests
```bash
# Run on specific browser
pytest --browser chromium
pytest --browser firefox
pytest --browser webkit

# Run in headless mode
pytest --headed false
```

### Advanced Options
```bash
# Generate Allure reports
pytest --alluredir=reports/allure-results

# Run with video recording
pytest --video=retain-on-failure

# Run with tracing
pytest --tracing=retain-on-failure
```

## 📊 Reporting

### Allure Reports
```bash
# Generate and serve Allure report
allure generate reports/allure-results --clean
allure open reports/allure-results
```

### HTML Reports
```bash
# Generate HTML report
pytest --html=reports/report.html
```

### Screenshots & Videos
- **Screenshots**: Automatically captured on test failure in `screenshots/` directory
- **Videos**: Recorded when `VIDEO_RECORDING=true` in `.env`
- **Traces**: Available for debugging failed tests

## 🛠️ Development

### Adding New Tests
1. Create test file in `tests/` directory
2. Follow naming convention: `test_*.py`
3. Use page objects from `pages/` directory
4. Add appropriate assertions

### Adding New Page Objects
1. Create page class in `pages/` directory
2. Inherit from `BasePage`
3. Implement page-specific methods and locators

### Helper Methods
Common utility methods are available in `utils/helpers.py`:
- `maximize_browser()` - Maximize browser window
- `wait_for_element()` - Wait for element visibility
- `take_screenshot()` - Capture screenshot
- And more...

## 🔧 Common Commands

### Environment Management
```bash
# Activate virtual environment (Windows)
.venv\Scripts\Activate.ps1

# Activate virtual environment (Linux/Mac)
source venv/bin/activate

# Deactivate virtual environment
deactivate
```

### Cleanup
```bash
# Remove Python cache files
find . -type d -name "__pycache__" -exec rm -rf {} +
# or on Windows PowerShell:
Get-ChildItem -Recurse -Directory -Filter "__pycache__" | Remove-Item -Recurse -Force

# Clean all artifacts
rm -rf screenshots/ videos/ reports/ .pytest_cache/
```

### Dependency Management
```bash
# Update all packages
pip install --upgrade -r requirements.txt

# Add new dependency
pip install package-name
pip freeze > requirements.txt
```

## 🌐 Browser Support

| Browser | Version | Status |
|---------|---------|--------|
| Chromium | Latest | ✅ Supported |
| Firefox | Latest | ✅ Supported |
| WebKit (Safari) | Latest | ✅ Supported |

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Code Standards
- Follow PEP 8 style guidelines
- Use descriptive variable and function names
- Add docstrings to all functions and classes
- Write meaningful commit messages

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Troubleshooting

### Common Issues

**Browser not found error:**
```bash
playwright install
```

**Import errors:**
- Ensure virtual environment is activated
- Check Python path: `python -c "import sys; print(sys.path)"`

**Test discovery issues:**
- Ensure test files follow `test_*.py` naming convention
- Check `pytest.ini` configuration

**Environment variable issues:**
- Ensure `.env` file exists and is properly formatted
- Check variable names match those in `config/config.py`

### Getting Help

- Check existing issues on GitHub
- Review the [commands.md](commands.md) file for additional commands
- Enable debug logging by setting `LOG_LEVEL=DEBUG` in `.env`

---

## 📊 Auto-generated Reports

Use `python scripts/generate_reports.py` to run pytest with `--html`, `--self-contained-html`, and `--json-report` so that the HTML report lands at `reports/pytests/report.html`, the JSON payload resides in `reports/json/report.json`, and pandas converts that JSON into `reports/excel/pytest-results.xlsx`.

Install the reporting dependencies first (`pip install -r requirements.txt`). Set `SUITE_NAME` in the environment if you want the log file prefix (defaults to `LCT_A4G_AUTO`). Attach the generated HTML and Excel files when sending results to stakeholders.


**Happy Testing! 🚀**

## 📬 CI Reporting

A GitHub Actions workflow (`.github/workflows/reporting.yml`) now runs `scripts/generate_reports.py` on every push to `master` and every day at 10:00 UTC on `develop`. It emails the HTML/Excel reports via `dawidd6/action-send-mail`, so define the repository secrets `MAIL_USERNAME`, `MAIL_PASSWORD`, `MAIL_TO`, and `MAIL_FROM`. The emails use branch-specific subjects so recipients can distinguish the manual run from the scheduled one.
