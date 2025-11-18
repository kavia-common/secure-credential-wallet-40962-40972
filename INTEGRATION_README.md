# Integration Guide (Development)

This repo contains:
- backend_api (FastAPI)
- database_postgres (SQLite used for dev)
- frontend_web (Flutter)

Environment setup

1) Database (development uses SQLite file)
- cd secure-credential-wallet-40962-40973/database_postgres
- cp .env.example .env
- Validate SQLITE_DB=./app.db (default)

2) Backend API
- cd secure-credential-wallet-40962-40972/backend_api
- cp .env.example .env
- Ensure DB_URL=sqlite:///./app.db (matches database SQLITE_DB)
- Optional: set CORS_ORIGINS to your frontend origin(s), e.g., http://localhost:3000
- Run migrations: alembic upgrade head
- Start: python run.py (listens on 0.0.0.0:8000)
- Docs: http://localhost:8000/docs

3) Frontend
- cd secure-credential-wallet-40962-40974/frontend_web
- cp .env.example .env
- Set BACKEND_BASE_URL to your backend URL (http://localhost:8000)
- Start your Flutter app per the project tooling.

Notes
- Keep secrets out of VCS. Use .env locally.
- For production, replace SQLite with a managed Postgres and set DB_URL accordingly.
- Update CORS_ORIGINS to the deployed frontend origins before production.
