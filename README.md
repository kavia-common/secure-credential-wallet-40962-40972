# secure-credential-wallet-40962-40972

Backend API
- FastAPI app with auth, eKYC mock, encrypted credentials, sharing, and admin routes.
- Env-driven settings (.env). Copy .env.example -> .env and adjust values.
- Health: GET /
- Readiness: GET /ready
- Run Alembic migrations:
  - cd backend_api
  - alembic upgrade head
- Local dev:
  - cd backend_api
  - python run.py

OpenAPI
- Generate: python -m src.api.generate_openapi
- File: backend_api/interfaces/openapi.json

End-to-end (dev) setup
1) Database (SQLite for dev):
   - cd secure-credential-wallet-40962-40973/database_postgres
   - cp .env.example .env
   - Ensure SQLITE_DB is ./app.db (default). This file will be created as needed.

2) Backend API:
   - cd secure-credential-wallet-40962-40972/backend_api
   - cp .env.example .env
   - Ensure DB_URL matches the database SQLITE_DB path (default sqlite:///./app.db).
   - CORS:
     - For local development, you can leave CORS_ORIGINS=*.
     - To restrict, set CORS_ORIGINS to a CSV of exact origins (e.g., http://localhost:3000,http://127.0.0.1:3000).
   - Run DB migrations: alembic upgrade head
   - Start API: python run.py
   - Docs: http://localhost:8000/docs

3) Frontend:
   - cd secure-credential-wallet-40962-40974/frontend_web
   - cp .env.example .env
   - Set BACKEND_BASE_URL to your backend (e.g., http://localhost:8000).
   - Start the Flutter/Web/Platform app per that project's instructions.

Notes:
- Do not commit real secrets. These examples are for local dev only.
- When switching to Postgres, set backend_api/.env DB_URL accordingly and run migrations.