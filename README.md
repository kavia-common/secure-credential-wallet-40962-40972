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