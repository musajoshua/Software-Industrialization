# Docker Notes

## Docker Network are

- Bridge
- None
- Host
- Overlay

**Note**
Custom Bridge (a custom network) allows us to target each service in the container with their dns name

Docker compose gives us a network when we use it.

## CI/CD Notes

When building your yaml file, give it a name `name: `

`on:` is used to specify the event triggers.

### GitHub Actions CI/CD

- Workflow file path: `.github/workflows/<name>.yml`
- Use `name:` for the workflow title.
- `on:` defines trigger events:
  - `push:` run on push to branches
  - `pull_request:` run on PRs
  - `schedule:` run on cron
  - `workflow_dispatch:` manual trigger
- `jobs:` defines one or more jobs.
- Each job can run on a runner like `ubuntu-latest`.
- Use `steps:` inside a job.
- Typical steps:
  - `uses: actions/checkout@v4`
  - `uses: actions/setup-python@v5` or `actions/setup-node@v5`
  - `run: pip install -r requirements.txt`
  - `run: pytest`
- Use `needs:` to make one job wait for another.
- Use `env:` for environment variables.
- Use `with:` to pass inputs to action steps.

**Note**
GitHub Actions workflows are YAML and must be valid syntax. Use the `push` and `pull_request` triggers for CI and `workflow_dispatch` for manual runs.

