Development environment checklist

Database (database_postgres):
- Copy .env.example to .env
- SQLITE_DB=./app.db

Backend (backend_api):
- Copy .env.example to .env
- DB_URL=sqlite:///./app.db
- CORS_ORIGINS includes https://appetize.io
- SECRET_KEY length >= 32
- (Optional) EKYC_PROVIDER_API_KEY and EKYC_WEBHOOK_SECRET for webhook tests

Frontend (frontend_web):
- Copy .env.example to .env
- BACKEND_BASE_URL=https://vscode-internal-23122-beta.beta01.cloud.kavia.ai:3001

Validation:
- Access backend docs at preview URL
- Register/Login -> obtain token
- CRUD credentials with Bearer token
- Create share and access via /sharing/access/{token}
