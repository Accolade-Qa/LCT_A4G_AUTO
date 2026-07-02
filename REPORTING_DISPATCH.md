# GitHub Actions Reporting Dispatch

This repository supports triggering the `Test and Report Workflow` from:

- `push` events on `main`, `master`, and `atcu`
- manual `workflow_dispatch`
- remote `repository_dispatch` events

## What it does

The workflow runs:

- project-specific pytest execution via `utils/generate_reports.py`
- report generation in JSON, HTML, and Excel formats
- artifact upload
- email notification with report attachments

## Supported inputs

### `workflow_dispatch`

- `project` — run one project, e.g. `lct`
- `projects` — run multiple projects, e.g. `atcu,lct`
- `marker` — pytest marker expression, e.g. `smoke`, `api`, `regression and not slow`
- `report_dir` — base report directory, default `reports`

### `repository_dispatch`

Use `client_payload` with the same field names:

- `project`
- `projects`
- `marker`
- `report_dir`

## How to trigger a project-specific run

### Run a single project + marker

This will run `lct` project tests filtered by the `api` marker:

```bash
curl -X POST \
  -H "Authorization: token $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github+json" \
  https://api.github.com/repos/OWNER/REPO/dispatches \
  -d '{
    "event_type": "run-project-report",
    "client_payload": {
      "project": "lct",
      "marker": "api"
    }
  }'
```

### Run multiple projects in one dispatch

This will run `atcu` and `lct` with the `smoke` marker:

```bash
curl -X POST \
  -H "Authorization: token $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github+json" \
  https://api.github.com/repos/OWNER/REPO/dispatches \
  -d '{
    "event_type": "run-project-report",
    "client_payload": {
      "projects": "atcu,lct",
      "marker": "smoke"
    }
  }'
```

### Run full regression for all projects

This will run the full regression marker for all configured projects if your code supports running all-projects in one invocation:

```bash
curl -X POST \
  -H "Authorization: token $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github+json" \
  https://api.github.com/repos/OWNER/REPO/dispatches \
  -d '{
    "event_type": "run-project-report",
    "client_payload": {
      "marker": "regression"
    }
  }'
```

> Use `projects` when you want multiple projects in one request. `project` and `projects` are mutually exclusive in the workflow logic.

## Example marker values

- `smoke` — fast critical path
- `regression` — full suite
- `api` — API tests only
- `regression and not slow` — full regression without slow tests
- `smoke and critical` — critical smoke tests

## workflow_dispatch example

If you open the workflow in GitHub and click **Run workflow**, fill in:

- `project`: `lct`
- `marker`: `api`
- `report_dir`: `reports`

## Dummy Python trigger script

Use the helper script at `scripts/trigger_project_report.py` to send a repository dispatch from Python.

Example usage for `lct` + `api`:

```bash
python scripts/trigger_project_report.py \
  --owner OWNER \
  --repo REPO \
  --token "$GITHUB_TOKEN" \
  --project lct \
  --marker api
```

Example usage for `atcu,lct` + `smoke`:

```bash
python scripts/trigger_project_report.py \
  --owner OWNER \
  --repo REPO \
  --token "$GITHUB_TOKEN" \
  --projects atcu,lct \
  --marker smoke
```
