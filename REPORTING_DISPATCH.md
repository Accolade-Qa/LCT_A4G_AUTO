# GitHub Actions Reporting Dispatch Guide

This document captures the complete trigger flow for the reporting workflow, including:

- workflow trigger types
- project and marker selection
- external invocation from Bitbucket or other CI
- token requirements and security considerations

## Supported trigger methods

The reporting workflow can be started by:

1. `push` events on selected branches:
   - `main`
   - `master`
   - `atcu`
2. Manual `workflow_dispatch`
3. External `repository_dispatch`

## What the workflow does

When triggered, the workflow:

- checks out the repository
- installs Python and Playwright dependencies
- runs tests using `python utils/generate_reports.py`
- generates JSON, HTML, and Excel reports
- verifies report files
- uploads artifacts
- sends an email notification with attached reports

## Supported trigger inputs

### `workflow_dispatch`

Inputs available when run manually from GitHub:

- `project`: single project name, e.g. `lct`
- `projects`: comma-separated projects, e.g. `atcu,lct`
- `marker`: pytest marker expression, e.g. `smoke`, `api`, `regression and not slow`
- `report_dir`: destination directory for reports, default `reports`

### `repository_dispatch`

External systems must send payload values via `client_payload`:

- `project`
- `projects`
- `marker`
- `report_dir`

The workflow uses the payload values in this order:
- `projects` if present
- otherwise `project`
- then `marker`
- then `report_dir`

### Important compatibility note

- `project` and `projects` are mutually exclusive.
- If `projects` is provided, `project` is ignored.
- `repository_dispatch` triggers the workflow definition on the default branch (`master`).
- `workflow_dispatch` can target a branch via `ref`.

## Branch behavior

### When to use `repository_dispatch`

- Use it for external triggers from another CI system or script.
- It runs the workflow defined on the repository default branch.
- In this repo, the default branch is `master`.
- Therefore the workflow file must exist on `master` for `repository_dispatch` to work.

### When to use `workflow_dispatch`

- Use it when you need to trigger the workflow from a specific branch.
- It can run the workflow file from `atcu`, `master`, or any branch where the file exists.
- This is the best choice if your trigger source needs branch-specific behavior.

## Use cases

### 1. Trigger from another CI after deploy

Scenario:
- developer pushes code to Bitbucket
- deploy succeeds in Bitbucket pipeline
- the pipeline sends a GitHub API request to trigger the reporting workflow

Result:
- GitHub runs the reporting workflow independently
- no repo clone or GitHub checkout is required on the developer machine

### 2. External curl trigger from a shell or script

You can trigger the workflow from any system that has network access to GitHub and a valid GitHub token.

### 3. Developer local trigger

If a developer wants to trigger the workflow manually, they can use:
- a `curl` command, or
- the helper script `trigger_project_report.py`

They do not need the full repository cloned just for triggering.

## Token requirements

### Which token is needed?

Developers need a **GitHub token**, not a Bitbucket token.

The trigger request authenticates against GitHub, so the API token must be issued by GitHub.

### Best practice

- each developer should use their own GitHub token, or
- your team should use a shared service account / machine user token stored securely
- never hardcode a token in source code
- store the token in Bitbucket secret variables or GitHub secrets
- rotate or revoke exposed tokens immediately

### Required GitHub PAT scopes

- `repo` (for private repositories)
- `workflow`

## Example trigger commands

### Repository dispatch for a single project

Run `lct` smoke tests:

```bash
curl -X POST \
  -H "Authorization: token $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github+json" \
  https://api.github.com/repos/Accolade-Qa/LCT_A4G_AUTO/dispatches \
  -d '{
    "event_type": "run-project-report",
    "client_payload": {
      "project": "lct",
 "marker": "smoke",
      "report_dir": "reports"
    }
  }'
```

### Repository dispatch for multiple projects

Run `atcu` and `lct` smoke tests:

```bash
curl -X POST \
  -H "Authorization: token $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github+json" \
  https://api.github.com/repos/Accolade-Qa/LCT_A4G_AUTO/dispatches \
  -d '{
    "event_type": "run-project-report",
    "client_payload": {
      "projects": "atcu,lct",
      "marker": "smoke",
      "report_dir": "reports"
    }
  }'
```

### Repository dispatch for full regression

Run regression across all configured projects:

```bash
curl -X POST \
  -H "Authorization: token $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github+json" \
  https://api.github.com/repos/Accolade-Qa/LCT_A4G_AUTO/dispatches \
  -d '{
    "event_type": "run-project-report",
    "client_payload": {
      "marker": "regression",
      "report_dir": "reports"
    }
  }'
```

### workflow_dispatch with a branch ref

If the workflow file exists on `atcu`, target that branch explicitly:

```bash
curl -X POST \
  -H "Authorization: token $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github+json" \
  https://api.github.com/repos/Accolade-Qa/LCT_A4G_AUTO/actions/workflows/reporting.yml/dispatches \
  -d '{
    "ref": "atcu",
    "inputs": {
      "project": "lct",
      "marker": "smoke",
      "report_dir": "reports"
    }
  }'
```

## Helper script

Use the helper script `trigger_project_report.py` to simplify GitHub dispatch calls.

Example for `lct` smoke tests using repository_dispatch:

```bash
python trigger_project_report.py \
  --owner Accolade-Qa \
  --repo LCT_A4G_AUTO \
  --token "$GITHUB_TOKEN" \
  --project lct \
  --marker smoke
```

Example for `atcu,lct` smoke tests using repository_dispatch:

```bash
python trigger_project_report.py \
  --owner Accolade-Qa \
  --repo LCT_A4G_AUTO \
  --token "$GITHUB_TOKEN" \
  --projects atcu,lct \
  --marker smoke
```

Example for `atcu` branch-specific workflow_dispatch (recommended when testing on `atcu` branch):

```bash
python trigger_project_report.py \
  --owner Accolade-Qa \
  --repo LCT_A4G_AUTO \
  --token "$GITHUB_TOKEN" \
  --project atcu \
  --marker smoke \
  --ref atcu
```

## Common pitfalls

- `repository_dispatch` only triggers workflows on the default branch.
- `workflow_dispatch` can target a branch using `ref`.
- `project` and `projects` cannot be used together.
- The GitHub token must be valid and have the correct scopes.
- Do not share your personal token; use individual tokens or a secure service account.

## Summary

- The trigger source can be Bitbucket, a local shell, or another CI.
- The important token is a GitHub PAT, never a Bitbucket token.
- The workflow file must exist on the branch being dispatched.
- Developers do not need the whole repo cloned just to send the trigger.
- Store tokens securely in CI variables or secrets.
