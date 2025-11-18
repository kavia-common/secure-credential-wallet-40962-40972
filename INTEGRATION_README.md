# Integration Guide (Development)

This repo contains:
- backend_api (FastAPI)
- database_postgres (SQLite used for dev)
- frontend_web (Flutter)

Running containers (preview):
- Backend API (docs): https://vscode-internal-23122-beta.beta01.cloud.kavia.ai:3001/docs
- Backend API base URL: https://vscode-internal-23122-beta.beta01.cloud.kavia.ai:3001
- Database (SQLite): https://vscode-internal-23122-beta.beta01.cloud.kavia.ai:3020
- Frontend preview: https://appetize.io/embed/drulzdxyg5mu7fv3flhnvkdose

Environment setup

1) Database (development uses SQLite file)
- cd secure-credential-wallet-40962-40973/database_postgres
- cp .env.example .env
- Validate SQLITE_DB=./app.db (default)

2) Backend API
- cd secure-credential-wallet-40962-40972/backend_api
- If missing, create .env from example: cp .env.example .env
- Ensure DB_URL=sqlite:///./app.db (matches database SQLITE_DB: ./app.db)
- Ensure CORS_ORIGINS includes your frontend origin(s), e.g., https://appetize.io
- Run migrations: alembic upgrade head
- Start: python run.py (listens on 0.0.0.0:8000 locally; preview is on port 3001)
- Docs: http(s)://<host>:<port>/docs

3) Frontend
- cd secure-credential-wallet-40962-40974/frontend_web
- cp .env.example .env
- Ensure BACKEND_BASE_URL is set to: https://vscode-internal-23122-beta.beta01.cloud.kavia.ai:3001
- Start your Flutter app per the project tooling.

Validation checklist (dev)
- backend_api/.env: DB_URL=sqlite:///./app.db, CORS_ORIGINS includes https://appetize.io
- database_postgres/.env: SQLITE_DB=./app.db
- frontend_web/.env: BACKEND_BASE_URL=https://vscode-internal-23122-beta.beta01.cloud.kavia.ai:3001
- Access /docs at backend preview; register/login works; CRUD credentials works; sharing + webhook as per docs.

Notes
- Keep secrets out of VCS. Use .env locally.
- For production, replace SQLite with a managed Postgres and set DB_URL accordingly.
- Update CORS_ORIGINS to the deployed frontend origins before production.
