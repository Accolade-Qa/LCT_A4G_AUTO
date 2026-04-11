import json
import os
import subprocess
import sys
from pathlib import Path
from config.global_var import REPORT_PATH, ROOT_DIR as CONFIG_ROOT
import pandas as pd

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

def _prepare_directories() -> dict[str, Path]:
    reports_root = Path(REPORT_PATH)
    paths = {
        "html": reports_root / "pytests" / "report.html",
        "json": reports_root / "json" / "report.json",
        "excel": reports_root / "excel" / "pytest-results.xlsx",
    }
    for path in paths.values():
        path.parent.mkdir(parents=True, exist_ok=True)
    return paths


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

    dataframe = pd.DataFrame(cases, columns=["Test case name", "Expected", "Actual", "Result"])
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
        _convert_json_to_excel(paths["json"], paths["excel"])
    except Exception as exc:  # pragma: no cover
        print("Failed to convert JSON report to Excel:", exc)
        if exit_code == 0:
            exit_code = 1
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
