# Product-Catalog

This project provides a small FastAPI product catalog with an optional MCP server layer.

Quick start (local):

1. Create and activate a virtual environment (Windows PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. Create a local Postgres database or run with Docker Compose (recommended).

3. Run the API locally (set DATABASE_URL if your DB isn't default):

```powershell
#$env:DATABASE_URL = "postgresql+psycopg2://postgres:password@localhost:5432/product_catalog"
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Docker (recommended):

```powershell
docker compose up --build
```

Notes:
- The app reads `DATABASE_URL` from environment. The docker-compose file provides a `db` service and sets `DATABASE_URL` for the `api` service.
- We use `psycopg2-binary` in `requirements.txt` to avoid building libpq locally. The `Dockerfile` still installs minimal system build tools to support other packages.
- If `fastmcp` isn't installed, `mcp_server.py` falls back to a simple CLI listing of products.
