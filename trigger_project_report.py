import argparse
import json
import sys
import urllib.request


def parse_args():
    parser = argparse.ArgumentParser(
        description="Trigger the GitHub Actions reporting workflow via repository_dispatch."
    )
    parser.add_argument("--owner", required=True, help="GitHub repository owner")
    parser.add_argument("--repo", required=True, help="GitHub repository name")
    parser.add_argument("--token", required=True, help="GitHub token with repo access")
    parser.add_argument("--project", help="Single project name, e.g. lct")
    parser.add_argument(
        "--projects", help="Comma-separated list of projects, e.g. atcu,lct"
    )
    parser.add_argument("--marker", help="Pytest marker expression, e.g. api or smoke")
    parser.add_argument(
        "--report-dir",
        default="reports",
        help="Optional report output directory",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    if args.project and args.projects:
        print("Error: --project and --projects are mutually exclusive.")
        sys.exit(1)

    url = f"https://api.github.com/repos/{args.owner}/{args.repo}/dispatches"
    payload = {
        "event_type": "run-project-report",
        "client_payload": {
            "report_dir": args.report_dir,
        },
    }

    if args.project:
        payload["client_payload"]["project"] = args.project
    if args.projects:
        payload["client_payload"]["projects"] = args.projects
    if args.marker:
        payload["client_payload"]["marker"] = args.marker

    data = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(url, data=data)
    request.add_header("Accept", "application/vnd.github+json")
    request.add_header("Authorization", f"token {args.token}")
    request.add_header("Content-Type", "application/json")

    try:
        with urllib.request.urlopen(request) as response:
            print("Dispatch request sent successfully.")
            print("Response status:", response.status)
            print(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        print("Failed to send dispatch request.")
        print(exc.code, exc.reason)
        print(exc.read().decode("utf-8"))
        sys.exit(1)


if __name__ == "__main__":
    main()
