import argparse
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path

# Add project root to path
ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT))

def load_yaml_config(project):
    """Load configuration from config/<project>.yaml."""
    yaml_path = ROOT / "config" / f"{project}.yaml"
    if not yaml_path.exists():
        return {}
    try:
        import yaml
        with open(yaml_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    except Exception as e:
        print(f"Error reading YAML for {project}: {e}")
        return {}

def get_live_app_version(base_url):
    """Attempt to retrieve the live build version from the login page footer using Playwright."""
    if not base_url or base_url == "N/A":
        return "Unknown"
    
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("Playwright is not installed in the python environment. Skipping live version fetch.")
        return "Unknown (Playwright not installed)"
        
    try:
        print(f"Fetching live version from {base_url}...")
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            # Use a quick timeout to prevent hanging the pipeline
            context = browser.new_context(ignore_https_errors=True)
            page = context.new_page()
            page.goto(base_url, timeout=12000, wait_until="domcontentloaded")
            
            # Selector for the version footer
            locator = page.locator("body app-root app-footer span:nth-child(1)")
            locator.wait_for(state="attached", timeout=3000)
            version_text = locator.inner_text().strip()
            browser.close()
            
            if version_text:
                print(f"Found version: {version_text}")
                return version_text
            return "Unknown"
    except Exception as e:
        print(f"Failed to fetch live version from {base_url}: {e}")
        return "Unknown (Unavailable)"

def determine_environment(base_url):
    """Determine the environment name based on the base URL."""
    if not base_url or base_url == "N/A":
        return "Unknown"
    url_lower = base_url.lower()
    if "prod" in url_lower:
        return "Production"
    elif "staging" in url_lower:
        return "Staging"
    elif "qa" in url_lower:
        return "QA"
    else:
        return "QA/Staging"

def parse_report_json(json_path):
    """Parse report.json to extract test results."""
    results = {
        "passed": 0,
        "failed": 0,
        "skipped": 0,
        "total": 0,
        "duration": 0.0,
        "failures": []
    }
    
    if not json_path.exists():
        return results
        
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        summary = data.get("summary", {})
        results["passed"] = summary.get("passed", 0)
        results["failed"] = summary.get("failed", 0)
        results["skipped"] = summary.get("skipped", 0)
        results["total"] = results["passed"] + results["failed"] + results["skipped"]
        results["duration"] = round(data.get("duration", 0.0), 2)
        
        # Extract failures details
        for test in data.get("tests", []):
            if test.get("outcome") == "failed":
                name = test.get("nodeid", "Unknown Test")
                # Clean name a bit
                name_clean = name.split("::")[-1] if "::" in name else name
                message = "No failure message available"
                call = test.get("call", {})
                if call and call.get("longrepr"):
                    message = str(call.get("longrepr")).split("\n")[-1]
                results["failures"].append({"name": name_clean, "message": message})
                
    except Exception as e:
        print(f"Error parsing JSON report {json_path}: {e}")
        
    return results

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--report-dir", default="reports", help="Directory where reports are located.")
    parser.add_argument("--actor", default="github-actions", help="The user who triggered the run.")
    parser.add_argument("--run-number", default="N/A", help="Workflow run number.")
    parser.add_argument("--ref", default="master", help="Git branch/ref name.")
    parser.add_argument("--sha", default="N/A", help="Git commit SHA.")
    args = parser.parse_args()
    
    report_dir = Path(args.report_dir)
    print(f"Scanning for report.json files in: {report_dir.resolve()}")
    
    # Locate all subdirectories containing report.json
    project_reports = {}
    
    # 1. Scan subdirectories (project specific)
    if report_dir.exists():
        for sub in report_dir.iterdir():
            if sub.is_dir():
                json_path = sub / "report.json"
                if json_path.exists():
                    project_reports[sub.name] = json_path
                    
    # 2. Check fallback/top-level if no subdirs found
    if not project_reports and (report_dir / "report.json").exists():
        # Fallback project name from environment or config default
        project_name = os.getenv("PROJECT") or "lct"
        project_reports[project_name] = report_dir / "report.json"
        
    print(f"Found project reports: {list(project_reports.keys())}")
    
    project_details = []
    overall_status = "PASS"
    total_passed = 0
    total_failed = 0
    total_skipped = 0
    total_duration = 0.0
    
    for proj_name, json_path in project_reports.items():
        # Load project config
        config = load_yaml_config(proj_name)
        base_url = config.get("base_url", "N/A")
        
        # Get dynamic metadata
        env_name = determine_environment(base_url)
        app_version = get_live_app_version(base_url)
        
        # Parse test metrics
        stats = parse_report_json(json_path)
        
        total_passed += stats["passed"]
        total_failed += stats["failed"]
        total_skipped += stats["skipped"]
        total_duration += stats["duration"]
        
        if stats["failed"] > 0:
            overall_status = "FAIL"
            
        pass_rate = 0.0
        total_runs = stats["passed"] + stats["failed"]
        if total_runs > 0:
            pass_rate = round((stats["passed"] / total_runs) * 100, 1)
            
        project_details.append({
            "name": proj_name.upper(),
            "url": base_url,
            "env": env_name,
            "version": app_version,
            "passed": stats["passed"],
            "failed": stats["failed"],
            "skipped": stats["skipped"],
            "total": stats["total"],
            "duration": stats["duration"],
            "pass_rate": pass_rate,
            "failures": stats["failures"]
        })
        
    # Build HTML email
    build_html_email(
        project_details,
        overall_status,
        args.actor,
        args.run_number,
        args.ref,
        args.sha,
        total_passed,
        total_failed,
        total_skipped,
        round(total_duration, 2)
    )

def build_html_email(projects, status, actor, run_number, ref, sha, passed, failed, skipped, duration):
    """Generate a highly aesthetic, responsive HTML email body."""
    status_color = "#10b981" if status == "PASS" else "#ef4444"
    status_bg = "#d1fae5" if status == "PASS" else "#fee2e2"
    status_text = "PASSED" if status == "PASS" else "FAILED"
    
    html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
    body {{
        font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
        background-color: #f8fafc;
        margin: 0;
        padding: 0;
        color: #334155;
    }}
    .email-container {{
        max-width: 680px;
        margin: 20px auto;
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.05);
    }}
    .header {{
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        color: #ffffff;
        padding: 30px 24px;
        position: relative;
    }}
    .header h1 {{
        margin: 0;
        font-size: 22px;
        font-weight: 700;
        letter-spacing: -0.5px;
    }}
    .header .meta {{
        font-size: 13px;
        color: #94a3b8;
        margin-top: 8px;
    }}
    .status-badge {{
        display: inline-block;
        padding: 6px 12px;
        font-weight: 700;
        font-size: 12px;
        border-radius: 20px;
        text-transform: uppercase;
        margin-top: 12px;
        color: {status_color};
        background-color: {status_bg};
    }}
    .content {{
        padding: 24px;
    }}
    .summary-grid {{
        display: flex;
        justify-content: space-between;
        gap: 12px;
        margin-bottom: 24px;
    }}
    .summary-card {{
        flex: 1;
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 12px;
        text-align: center;
    }}
    .summary-card .value {{
        font-size: 20px;
        font-weight: 700;
        color: #0f172a;
    }}
    .summary-card .label {{
        font-size: 11px;
        color: #64748b;
        text-transform: uppercase;
        margin-top: 4px;
        letter-spacing: 0.5px;
    }}
    .project-section {{
        margin-top: 24px;
    }}
    .project-card {{
        border: 1px solid #e2e8f0;
        border-left: 4px solid #64748b;
        border-radius: 8px;
        padding: 16px;
        margin-bottom: 16px;
        background: #ffffff;
    }}
    .project-card.pass {{
        border-left-color: #10b981;
    }}
    .project-card.fail {{
        border-left-color: #ef4444;
    }}
    .project-header {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-bottom: 1px solid #f1f5f9;
        padding-bottom: 10px;
        margin-bottom: 12px;
    }}
    .project-title {{
        font-size: 16px;
        font-weight: 700;
        color: #0f172a;
    }}
    .project-env-badge {{
        font-size: 11px;
        background: #f1f5f9;
        color: #475569;
        padding: 3px 8px;
        border-radius: 4px;
        font-weight: 600;
    }}
    .project-meta-table {{
        width: 100%;
        font-size: 13px;
        margin-bottom: 12px;
        border-collapse: collapse;
    }}
    .project-meta-table td {{
        padding: 4px 0;
    }}
    .project-meta-table td.lbl {{
        color: #64748b;
        width: 120px;
    }}
    .project-meta-table td.val {{
        font-weight: 500;
        color: #334155;
    }}
    .stats-row {{
        display: flex;
        gap: 16px;
        font-size: 12px;
        background: #f8fafc;
        padding: 8px 12px;
        border-radius: 6px;
    }}
    .stats-item {{
        display: flex;
        gap: 6px;
    }}
    .stats-item .lbl {{
        color: #64748b;
    }}
    .stats-item .val {{
        font-weight: 700;
    }}
    .failures-list {{
        margin-top: 12px;
        background: #fef2f2;
        border: 1px solid #fee2e2;
        border-radius: 6px;
        padding: 12px;
    }}
    .failures-header {{
        font-size: 13px;
        font-weight: 700;
        color: #991b1b;
        margin-bottom: 8px;
    }}
    .failure-item {{
        font-size: 12px;
        color: #b91c1c;
        margin-bottom: 6px;
        padding-left: 12px;
        border-left: 2px solid #f87171;
    }}
    .failure-item:last-child {{
        margin-bottom: 0;
    }}
    .footer {{
        background: #f1f5f9;
        padding: 20px;
        text-align: center;
        font-size: 12px;
        color: #64748b;
        border-top: 1px solid #e2e8f0;
    }}
    .footer a {{
        color: #2563eb;
        text-decoration: none;
    }}
</style>
</head>
<body>
<div class="email-container">
    <div class="header">
        <h1>Automation Test Execution Report</h1>
        <div class="meta">
            Branch: <b>{ref}</b> &nbsp;|&nbsp; Commit: <b>{sha[:8]}</b> &nbsp;|&nbsp; Triggered by: <b>{actor}</b>
        </div>
        <div class="status-badge">{status_text}</div>
    </div>
    
    <div class="content">
        <div class="summary-grid">
            <div class="summary-card">
                <div class="value" style="color: #10b981;">{passed}</div>
                <div class="label">Passed</div>
            </div>
            <div class="summary-card">
                <div class="value" style="color: #ef4444;">{failed}</div>
                <div class="label">Failed</div>
            </div>
            <div class="summary-card">
                <div class="value" style="color: #d97706;">{skipped}</div>
                <div class="label">Skipped</div>
            </div>
            <div class="summary-card">
                <div class="value">{duration}s</div>
                <div class="label">Duration</div>
            </div>
        </div>
        
        <div class="project-section">
            <h3 style="margin-top: 0; color: #0f172a; font-size: 16px; border-bottom: 2px solid #e2e8f0; padding-bottom: 8px;">Executed Projects Summary</h3>
    """
    
    for proj in projects:
        card_class = "pass" if proj["failed"] == 0 else "fail"
        html += f"""
            <div class="project-card {card_class}">
                <div class="project-header" style="display: flex; justify-content: space-between;">
                    <span class="project-title">{proj["name"]}</span>
                    <span class="project-env-badge">{proj["env"]}</span>
                </div>
                <table class="project-meta-table">
                    <tr>
                        <td class="lbl">Target URL:</td>
                        <td class="val"><a href="{proj["url"]}" style="color: #2563eb; text-decoration: none;">{proj["url"]}</a></td>
                    </tr>
                    <tr>
                        <td class="lbl">App Version:</td>
                        <td class="val"><code>{proj["version"]}</code></td>
                    </tr>
                </table>
                <div class="stats-row" style="display: flex;">
                    <div class="stats-item" style="margin-right: 15px;">
                        <span class="lbl">Total:</span>
                        <span class="val">{proj["total"]}</span>
                    </div>
                    <div class="stats-item" style="margin-right: 15px;">
                        <span class="lbl" style="color: #10b981;">Passed:</span>
                        <span class="val" style="color: #10b981;">{proj["passed"]}</span>
                    </div>
                    <div class="stats-item" style="margin-right: 15px;">
                        <span class="lbl" style="color: #ef4444;">Failed:</span>
                        <span class="val" style="color: #ef4444;">{proj["failed"]}</span>
                    </div>
                    <div class="stats-item" style="margin-right: 15px;">
                        <span class="lbl" style="color: #d97706;">Skipped:</span>
                        <span class="val" style="color: #d97706;">{proj["skipped"]}</span>
                    </div>
                    <div class="stats-item" style="margin-left: auto;">
                        <span class="lbl">Pass Rate:</span>
                        <span class="val" style="color: {'#10b981' if proj['pass_rate'] == 100.0 else '#d97706' if proj['pass_rate'] >= 80.0 else '#ef4444'}">{proj["pass_rate"]}%</span>
                    </div>
                </div>
        """
        
        if proj["failures"]:
            html += f"""
                <div class="failures-list">
                    <div class="failures-header">Failed Tests ({len(proj["failures"])}):</div>
            """
            for failure in proj["failures"]:
                html += f"""
                    <div class="failure-item">
                        <b>{failure["name"]}</b>: {failure["message"]}
                    </div>
                """
            html += "</div>"
            
        html += "</div>"
        
    html += f"""
        </div>
    </div>
    
    <div class="footer">
        <p>This is an automated notification from the Continuous Integration system.</p>
        <p>Workflow Run: <a href="https://github.com/{os.getenv('GITHUB_REPOSITORY', 'Accolade-Qa/LCT_A4G_AUTO')}/actions/runs/{run_number}">#{run_number}</a></p>
    </div>
</div>
</body>
</html>
"""
    
    output_path = ROOT / "email_body.html"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Successfully generated HTML email body at: {output_path.resolve()}")

if __name__ == "__main__":
    main()
