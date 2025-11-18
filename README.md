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
- Generate: python -m src.api.generate_openAPI
- File: backend_api/interfaces/openapi.json

Preview URLs
- Backend base URL: https://vscode-internal-23122-beta.beta01.cloud.kavia.ai:3001
- Docs: https://vscode-internal-23122-beta.beta01.cloud.kavia.ai:3001/docs
- Frontend preview: https://appetize.io/embed/drulzdxyg5mu7fv3flhnvkdose

End-to-end (dev) setup
1) Database (SQLite for dev):
   - cd secure-credential-wallet-40962-40973/database_postgres
   - cp .env.example .env
   - Ensure SQLITE_DB is ./app.db (default). This file will be created as needed.

2) Backend API:
   - cd secure-credential-wallet-40962-40972/backend_api
   - Ensure a real .env exists (if missing, copy from .env.example).
   - Ensure DB_URL matches the database SQLITE_DB path (default sqlite:///./app.db).
   - CORS:
     - Include the frontend preview origin: CORS_ORIGINS=https://appetize.io
     - To add more, provide CSV (e.g., https://appetize.io,http://localhost:3000).
   - Run DB migrations: alembic upgrade head
   - Start API: python run.py
   - Docs: http://localhost:8000/docs (local), preview docs as above.

3) Frontend:
   - cd secure-credential-wallet-40962-40974/frontend_web
   - cp .env.example .env
   - Set BACKEND_BASE_URL to the backend preview URL:
     BACKEND_BASE_URL=https://vscode-internal-23122-beta.beta01.cloud.kavia.ai:3001
   - Start the Flutter/Web/Platform app per that project's instructions.

Notes:
- Do not commit real secrets. These examples are for local dev only.
- When switching to Postgres, set backend_api/.env DB_URL accordingly and run migrations.