import os
import smtplib
import glob
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

USERNAME = os.getenv("MAIL_USERNAME")
PASSWORD = os.getenv("MAIL_PASSWORD")
TO_EMAIL = os.getenv("MAIL_TO")
FROM_EMAIL = os.getenv("MAIL_FROM")

status = os.getenv("STATUS")
color = os.getenv("STATUS_COLOR")

passed = int(os.getenv("TESTS_PASSED", 0))
failed = int(os.getenv("TESTS_FAILED", 0))
skipped = int(os.getenv("TESTS_SKIPPED", 0))
total = int(os.getenv("TESTS_TOTAL", 0))

trend = os.getenv("TREND")
failed_tests = os.getenv("FAILED_TESTS")

repo = os.getenv("GITHUB_REPOSITORY")
run_id = os.getenv("GITHUB_RUN_ID")
run_number = os.getenv("GITHUB_RUN_NUMBER")

report_url = os.getenv("REPORT_URL")

percent = int((passed / total) * 100) if total else 0

subject = f"{status} | {percent}% Passed | Run #{run_number}"

html = f"""
<div style="font-family: Arial; max-width:800px; margin:auto;">
  <div style="background:{color}; color:white; padding:15px; text-align:center;">
    {status} • {percent}% Passed
  </div>

  <br>

  <div style="background:#eee;">
    <div style="width:{percent}%; background:#2ECC71; padding:8px;"></div>
  </div>

  <br>

  <table style="width:100%; text-align:center;">
    <tr>
      <td style="background:#2ECC71;color:white;">Passed<br>{passed}</td>
      <td style="background:#E74C3C;color:white;">Failed<br>{failed}</td>
      <td style="background:#F1C40F;">Skipped<br>{skipped}</td>
      <td style="background:#3498DB;color:white;">Total<br>{total}</td>
    </tr>
  </table>

  <h3>📉 Trend</h3>
  <p>{trend}</p>

  <h3>❌ Failed Tests</h3>
  <pre>{failed_tests}</pre>

  <p>
    <a href="https://github.com/{repo}/actions/runs/{run_id}">View Run</a><br>
    <a href="{report_url}">View HTML Report</a>
  </p>

  <p>Reports & screenshots attached.</p>
</div>
"""

msg = MIMEMultipart()
msg["From"] = FROM_EMAIL
msg["To"] = TO_EMAIL
msg["Subject"] = subject

msg.attach(MIMEText(html, "html"))

files = [
    os.getenv("REPORT_HTML"),
    os.getenv("REPORT_EXCEL"),
]

files += glob.glob("**/*.png", recursive=True)

for file in files:
    if file and os.path.exists(file):
        with open(file, "rb") as f:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(f.read())
            encoders.encode_base64(part)
            part.add_header("Content-Disposition", f"attachment; filename={os.path.basename(file)}")
            msg.attach(part)

with smtplib.SMTP("smtp.gmail.com", 587) as server:
    server.starttls()
    server.login(USERNAME, PASSWORD)
    server.send_message(msg)

print("✅ Email sent")