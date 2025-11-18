from __future__ import annotations

import logging
from typing import List
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware import Middleware

from src.config.settings import settings
from src.database.session import init_engine_and_session, close_engine
from src.routers import auth, ekyc, credentials, sharing, admin

# Initialize logging early based on settings
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO),
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
)
logger = logging.getLogger("api.main")


def _build_cors_origins(origins_str: str) -> List[str]:
    if not origins_str:
        return ["*"]
    items = [o.strip() for o in origins_str.split(",") if o.strip()]
    return items or ["*"]


# PUBLIC_INTERFACE
def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application.

    - Loads env-driven settings
    - Configures CORS
    - Initializes DB engine and session factory
    - Includes routers with OpenAPI tags
    - Exposes health (/) and readiness (/ready) endpoints

    Returns:
        FastAPI: Configured FastAPI application instance.
    """
    middleware = [
        Middleware(
            CORSMiddleware,
            allow_origins=_build_cors_origins(settings.CORS_ORIGINS),
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
    ]

    app = FastAPI(
        title="Secure Credential Wallet API",
        description=(
            "Secure digital credential wallet with auth, encrypted storage, eKYC mock, "
            "sharing, and admin features. Implements env-driven security and metrics toggles."
        ),
        version="0.1.0",
        openapi_tags=[
            {"name": "health", "description": "Service health and status."},
            {"name": "auth", "description": "Authentication and token management."},
            {"name": "ekyc", "description": "Mock eKYC provider flows and webhooks."},
            {"name": "credentials", "description": "Encrypted credential storage and retrieval."},
            {"name": "sharing", "description": "Secure credential sharing endpoints."},
            {"name": "admin", "description": "Admin management endpoints."},
        ],
        middleware=middleware,
    )

    # DB init
    init_engine_and_session()

    # Routers
    app.include_router(auth.router, prefix="/auth", tags=["auth"])
    app.include_router(ekyc.router, prefix="/ekyc", tags=["ekyc"])
    app.include_router(credentials.router, prefix="/credentials", tags=["credentials"])
    app.include_router(sharing.router, prefix="/sharing", tags=["sharing"])
    app.include_router(admin.router, prefix="/admin", tags=["admin"])

    @app.get(
        "/",
        tags=["health"],
        summary="Health Check",
        description="Returns API health status.",
        responses={200: {"description": "Service is healthy"}},
    )
    def health_check():
        return {"status": "ok", "version": app.version}

    @app.get(
        "/ready",
        tags=["health"],
        summary="Readiness Probe",
        description="Readiness probe to signal dependencies are initialized.",
        responses={200: {"description": "Service is ready"}},
    )
    def readiness_probe():
        # In future we can attempt a lightweight DB check here
        return {"ready": True}

    @app.on_event("shutdown")
    async def _on_shutdown() -> None:
        close_engine()

    return app


app = create_app()
