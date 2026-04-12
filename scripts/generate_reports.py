import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from config.global_var import REPORT_PATH, ROOT_DIR as CONFIG_ROOT
import pandas as pd

REPORT_TEMPLATE = """
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Automation Test Report</title>
    <link rel="stylesheet" href="report.css" />
  </head>
  <body>
    <header>
      <h1>Automation Test Report</h1>
      <p>Generated at {{ generated_at }} &middot; Duration {{ duration }}</p>
    </header>

    <section class="summary-grid">
      <div class="card card-total">
        <div class="label">Total tests</div>
        <div class="value">{{ summary.total }}</div>
        <div class="subtext">Passed: {{ counts.passed }} · Failed: {{ counts.failed }} · Skipped: {{ counts.skipped }}</div>
      </div>
      <div class="card card-pass">
        <div class="label">Passed</div>
        <div class="value">{{ counts.passed }}</div>
        <div class="subtext">Success rate {{ counts.pass_rate }}%</div>
      </div>
      <div class="card card-fail">
        <div class="label">Failed</div>
        <div class="value">{{ counts.failed }}</div>
        <div class="subtext">{{ failure_ratio }} failures</div>
      </div>
      <div class="card card-skipped">
        <div class="label">Skipped</div>
        <div class="value">{{ counts.skipped }}</div>
        <div class="subtext">{{ counts.skipped }} skipped by suite</div>
      </div>
    </section>

    <h2>Test details</h2>
    <table class="status-table">
      <thead>
        <tr>
          <th>Module</th>
          <th>Test</th>
          <th>Outcome</th>
          <th>Duration (s)</th>
          <th>Message</th>
        </tr>
      </thead>
      <tbody>
        {% for test in tests %}
        <tr>
          <td>{{ test.module }}</td>
          <td>{{ test.short_name }}</td>
          <td class="status-{{ test.outcome_class }}">{{ test.outcome | capitalize }}</td>
          <td>{{ "%.2f"|format(test.duration) }}</td>
          <td>
            {% if test.longrepr %}
            <details>
              <summary>View failure info</summary>
              <div class="fail-details">{{ test.longrepr }}</div>
            </details>
            {% else %}
              {{ test.message or "—" }}
            {% endif %}
          </td>
        </tr>
        {% endfor %}
      </tbody>
    </table>
  </body>
</html>
"""

REPORT_CSS = """
:root {
  font-family: 'Inter', Arial, sans-serif;
  color: #1e1e1e;
  background-color: #f4f6fb;
}
body {
  margin: 0;
  padding: 2rem;
  background: #f4f6fb;
}
h1 {
  margin-bottom: 0.25rem;
}
h2 {
  margin-top: 2rem;
  border-bottom: 2px solid #e0e7ff;
  padding-bottom: 0.25rem;
}
.summary-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 1rem;
  margin-bottom: 1.5rem;
}
.card {
  padding: 1rem 1.25rem;
  border-radius: 0.75rem;
  box-shadow: 0 8px 16px rgba(15, 23, 42, 0.06);
  background: white;
}
.card .label {
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: #475569;
}
.card .value {
  margin-top: 0.35rem;
  font-size: 1.8rem;
  font-weight: 600;
}
.card .subtext {
  margin-top: 0.15rem;
  color: #64748b;
  font-size: 0.85rem;
}
.card-total {
  background: linear-gradient(135deg, #eef2ff, #f8fafc);
}
.card-pass {
  border-left: 4px solid #22c55e;
  background: linear-gradient(135deg, #ecfdf3, #f7fee7);
}
.card-fail {
  border-left: 4px solid #dc2626;
  background: linear-gradient(135deg, #fee2e2, #fff1f2);
}
.card-skipped {
  border-left: 4px solid #ea580c;
  background: linear-gradient(135deg, #fff7ed, #fff4e6);
}
.status-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 1rem;
}
.status-table th,
.status-table td {
  border-bottom: 1px solid #e2e8f0;
  padding: 0.75rem;
  text-align: left;
}
.status-table th {
  font-size: 0.85rem;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  color: #475569;
  background: #f8fafc;
}
.status-pass {
  color: #16a34a;
  font-weight: 600;
}
.status-fail {
  color: #dc2626;
  font-weight: 600;
}
.status-skipped {
  color: #ea580c;
  font-weight: 600;
}
.status-other {
  color: #475569;
  font-weight: 600;
}
.fail-details {
  font-family: 'Courier New', monospace;
  background: #111827;
  color: #e2e8f0;
  padding: 0.75rem;
  border-radius: 0.5rem;
  margin-top: 0.5rem;
  max-height: 220px;
  overflow: auto;
}
details {
  margin-top: 0.5rem;
}
details summary {
  cursor: pointer;
  font-weight: 600;
  color: #1d4ed8;
}
"""


def _prepare_directories() -> dict[str, Path]:
    reports_root = Path(REPORT_PATH)
    paths = {
        "html": reports_root / "pytests" / "report.html",
        "json": reports_root / "json" / "report.json",
        "excel": reports_root / "excel" / "pytest-results.xlsx",
        "css": reports_root / "pytests" / "report.css",
    }
    for path in paths.values():
        path.parent.mkdir(parents=True, exist_ok=True)
    return paths


def _build_test_context(tests: list[dict]) -> tuple[list[dict], float]:
    entries = []
    total_duration = 0.0
    for item in tests:
        nodeid = item.get("nodeid", "")
        outcome = item.get("outcome", "unknown")
        duration = item.get("duration", 0.0) or 0.0
        module = nodeid.split("::")[0]
        short_name = nodeid.split("::")[-1]
        longrepr = item.get("longrepr") or item.get("longreprtext") or ""
        if isinstance(longrepr, list):
            longrepr = "".join(longrepr)
        outcome_class = (
            "pass"
            if outcome in {"pass", "passed"}
            else (
                "fail"
                if outcome in {"fail", "failed"}
                else "skipped" if outcome == "skipped" else "other"
            )
        )
        message = (
            item.get("message") or (longrepr.splitlines()[0] if longrepr else "") or "—"
        )
        entries.append(
            {
                "module": module,
                "short_name": short_name,
                "outcome": outcome,
                "duration": duration,
                "longrepr": longrepr,
                "message": message,
                "outcome_class": outcome_class,
            }
        )
        total_duration += duration
    return entries, total_duration


def _summarize(data: dict) -> tuple[dict[str, int], dict]:
    tests = data.get("tests", [])
    counts = {"passed": 0, "failed": 0, "skipped": 0, "other": 0}
    for test in tests:
        outcome = test.get("outcome", "").lower()
        if outcome in {"pass", "passed"}:
            counts["passed"] += 1
        elif outcome in {"fail", "failed"}:
            counts["failed"] += 1
        elif outcome == "skipped":
            counts["skipped"] += 1
        else:
            counts["other"] += 1
    total = len(tests)
    pass_rate = round((counts["passed"] / total * 100) if total else 0, 1)
    return counts, {"total": total, "pass_rate": pass_rate}


def _render_html_report(json_path: Path, html_path: Path, css_path: Path) -> None:
    if not json_path.exists():
        raise FileNotFoundError(f"Pytest JSON report not found: {json_path}")

    with json_path.open() as handle:
        payload = json.load(handle)

    summary = payload.get("summary", {})
    counts, base = _summarize(payload)
    tests_context, total_duration = _build_test_context(payload.get("tests", []))
    summary_context = {
        "total": base["total"],
        "pass_rate": base["pass_rate"],
        "duration": f"{total_duration:.2f}s",
    }
    failure_ratio = f"{counts['failed']}/{base['total'] or 1}"

    env = Environment(
        loader=FileSystemLoader(searchpath=str(Path(__file__).parent)),
        autoescape=select_autoescape(["html", "xml"]),
    )
    template = env.from_string(REPORT_TEMPLATE)
    _write_css(css_path)
    html_content = template.render(
        generated_at=datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC"),
        duration=summary_context["duration"],
        summary=summary_context,
        counts={
            "passed": counts["passed"],
            "failed": counts["failed"],
            "skipped": counts["skipped"],
            "pass_rate": summary_context["pass_rate"],
        },
        failure_ratio=failure_ratio,
        tests=tests_context,
    )

    html_path.write_text(html_content, encoding="utf-8")


def _write_css(css_path: Path) -> None:
    css_path.write_text(REPORT_CSS, encoding="utf-8")


def _run_pytest_with_reports(paths: dict[str, Path], root: Path) -> int:
    cmd = [
        sys.executable,
        "-m",
        "pytest",
        "--html",
        str(paths["html"]),
        "--self-contained-html",
        "--json-report",
        "--json-report-file",
        str(paths["json"]),
        "tests",
    ]
    print("Running:", " ".join(cmd))
    result = subprocess.run(cmd, cwd=root)
    return result.returncode


def _convert_json_to_excel(json_path: Path, excel_path: Path) -> None:
    if not json_path.exists():
        raise FileNotFoundError(f"Pytest JSON report not found: {json_path}")
    with json_path.open() as handle:
        payload = json.load(handle)

    cases = []
    for case in payload.get("tests", []):
        outcome = case["outcome"]
        expected = "Pass" if outcome == "passed" else "Pass"
        actual = "Pass" if outcome == "passed" else case.get("longrepr", "Fail")
        result = outcome.upper()

        cases.append(
            {
                "Test case name": case["nodeid"],
                "Expected": expected,
                "Actual": actual,
                "Result": result,
            }
        )

    dataframe = pd.DataFrame(
        cases, columns=["Test case name", "Expected", "Actual", "Result"]
    )
    dataframe.to_excel(excel_path, index=False)
    print("Excel report written to", excel_path)


def _should_run_pytest() -> bool:
    return os.getenv("RUN_PYTEST", "true").lower() not in ("false", "0", "no")


def main() -> int:
    paths = _prepare_directories()
    project_root = Path(CONFIG_ROOT)
    exit_code = 0

    if _should_run_pytest():
        exit_code = _run_pytest_with_reports(paths, project_root)
        if exit_code != 0:
            print("Pytest finished with failures; reports may still be usable.")
    else:
        if not paths["json"].exists():
            raise FileNotFoundError(f"Pytest JSON report not found: {paths['json']}")
        print("Skipping pytest execution because RUN_PYTEST=false")

    try:
        _render_html_report(paths["json"], paths["html"], paths["css"])
        _convert_json_to_excel(paths["json"], paths["excel"])
    except Exception as exc:  # pragma: no cover
        print("Failed to convert JSON report to Excel:", exc)
        if exit_code == 0:
            exit_code = 1
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
