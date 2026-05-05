FROM mcr.microsoft.com/playwright/python:latest

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy repository files
COPY . .

# Install Playwright browser binaries and dependencies
RUN playwright install --with-deps

ENV PYTHONUNBUFFERED=1
ENV HEADLESS=true

CMD ["pytest", "--alluredir=reports/allure-results"]
