import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

import pandas as pd
from jinja2 import Template

# ================= CONFIG =================
ROOT = Path.cwd()
REPORT_DIR = ROOT / "reports"

JSON_PATH = REPORT_DIR / "report.json"
HTML_PATH = REPORT_DIR / "report.html"
EXCEL_PATH = REPORT_DIR / "report.xlsx"

# ================= HTML TEMPLATE =================
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Test Report</title>
<style>
body {
    font-family: system-ui;
    background: #0f172a;
    color: #e2e8f0;
    padding: 20px;
}
.cards {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 15px;
}
.card {
    padding: 15px;
    border-radius: 10px;
    background: #1e293b;
}
.pass { border-left: 5px solid #22c55e; }
.fail { border-left: 5px solid #ef4444; }
.skip { border-left: 5px solid #f59e0b; }

.value { font-size: 26px; }

table {
    width: 100%;
    margin-top: 20px;
    border-collapse: collapse;
}
td, th {
    padding: 10px;
    border-bottom: 1px solid #334155;
}
.status-pass { color: #22c55e; }
.status-fail { color: #ef4444; }
.status-skipped { color: #f59e0b; }
</style>
</head>

<body>

<h1>Test Report</h1>
<p>{{ time }}</p>

<div class="cards">
<div class="card"><div>Total</div><div class="value">{{ total }}</div></div>
<div class="card pass"><div>Passed</div><div class="value">{{ passed }}</div></div>
<div class="card fail"><div>Failed</div><div class="value">{{ failed }}</div></div>
<div class="card skip"><div>Skipped</div><div class="value">{{ skipped }}</div></div>
</div>

<table>
<tr><th>Test</th><th>Status</th><th>Time</th><th>Message</th></tr>

{% for t in tests %}
<tr>
<td>{{ t.name }}</td>
<td class="status-{{ t.status }}">{{ t.status }}</td>
<td>{{ t.duration }}</td>
<td>{{ t.message }}</td>
</tr>
{% endfor %}

</table>

</body>
</html>
"""


# ================= STEP 1: RUN PYTEST =================
def run_pytest():
    REPORT_DIR.mkdir(exist_ok=True)

    cmd = [
        sys.executable,
        "-m",
        "pytest",
        "--json-report",
        f"--json-report-file={JSON_PATH}",
    ]

    print("Running pytest...")
    result = subprocess.run(cmd, cwd=ROOT)
    return result.returncode


# ================= STEP 2: PROCESS JSON =================
def process_json():
    with open(JSON_PATH) as f:
        data = json.load(f)

    tests = []
    counts = {"passed": 0, "failed": 0, "skipped": 0}

    for t in data.get("tests", []):
        outcome = t.get("outcome", "")

        if outcome in ["passed", "pass"]:
            status = "pass"
            counts["passed"] += 1
        elif outcome in ["failed", "fail"]:
            status = "fail"
            counts["failed"] += 1
        else:
            status = "skipped"
            counts["skipped"] += 1

        tests.append(
            {
                "name": t.get("nodeid"),
                "status": status,
                "duration": round(t.get("duration", 0), 2),
                "message": (t.get("longrepr") or "")[:150],
            }
        )

    total = len(tests)
    return tests, counts, total, data


# ================= STEP 3: HTML =================
def generate_html(tests, counts, total):
    template = Template(HTML_TEMPLATE)

    html = template.render(
        time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        total=total,
        passed=counts["passed"],
        failed=counts["failed"],
        skipped=counts["skipped"],
        tests=tests,
    )

    HTML_PATH.write_text(html, encoding="utf-8")
    print("HTML generated:", HTML_PATH)


# ================= STEP 4: EXCEL =================
def generate_excel(data):
    rows = []

    for t in data.get("tests", []):
        rows.append(
            {
                "Test Case": t.get("nodeid"),
                "Result": t.get("outcome").upper(),
                "Duration": t.get("duration"),
                "Message": t.get("longrepr", ""),
            }
        )

    df = pd.DataFrame(rows)
    df.to_excel(EXCEL_PATH, index=False)

    print("Excel generated:", EXCEL_PATH)


# ================= MAIN =================
def main():
    exit_code = run_pytest()

    tests, counts, total, data = process_json()

    generate_html(tests, counts, total)
    generate_excel(data)

    if exit_code != 0:
        print("Some tests failed")

    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
