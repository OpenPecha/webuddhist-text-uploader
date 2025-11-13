# WebBuddhist Text Uploader - FastAPI + Poetry

FastAPI scaffold managed by Poetry.

## Prerequisites
- Python 3.10 or newer
- Poetry installed (`pipx install poetry` or see `https://python-poetry.org/docs/#installation`)

## Setup
1. Install dependencies:
   ```bash
   poetry install
   ```
2. Activate the virtualenv (optional; you can also prefix commands with `poetry run`):
   ```bash
   poetry shell
   ```

## Run the API (dev)
```bash
poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

- Open `http://localhost:8000` for a basic status message.
- Open `http://localhost:8000/docs` for interactive Swagger docs.

## Project layout
```
app/
  __init__.py
  main.py          # FastAPI application entrypoint (ASGI: app.main:app)
pyproject.toml     # Poetry configuration and dependencies
.gitignore
README.md
```

## Useful commands
- Add a dependency:
  ```bash
  poetry add <package>
  ```
- Add a dev-only dependency:
  ```bash
  poetry add --group dev <package>
  ```
- Run a script inside the venv:
  ```bash
  poetry run <command>
  ```

## Health checks
- Root: `GET /` returns a simple status
- Health: `GET /health` returns `{"status": "healthy"}`

## Notes
- The ASGI app is `app.main:app`.
- For production, remove `--reload` and configure a process manager or container.