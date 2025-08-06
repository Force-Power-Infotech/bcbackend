from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException as StarletteHTTPException
import logging.config

from app.core.config import settings
from app.core.logging_config import setup_logging

# Setup logging configuration
logging.config.dictConfig(setup_logging(level="INFO" if settings.ENV == "production" else "DEBUG"))
from app.api.v1 import auth, users, practice_session, dashboard, drill_group, drill, search, meta_drill_group, sub_drill

# Create FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url=f"{settings.API_V1_STR}/docs",
    redoc_url=f"{settings.API_V1_STR}/redoc",
)

# Database connection management
from app.db.base import engine

@app.on_event("shutdown")
async def shutdown():
    # Close all database connections
    await engine.dispose()

# Set up session middleware
from starlette.middleware.sessions import SessionMiddleware
app.add_middleware(
    SessionMiddleware,
    secret_key=settings.SECRET_KEY,  # Use secret key from settings
    session_cookie="bowlsace_session",
    same_site="lax",  # Protects against CSRF
    https_only=settings.ENV == "production",  # Only use HTTPS in production
    max_age=86400  # 24 hours
)

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Include API routers
app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["auth"])
app.include_router(users.router, prefix=f"{settings.API_V1_STR}/users", tags=["users"])
app.include_router(drill.router, prefix=f"{settings.API_V1_STR}/drill", tags=["drill"])
app.include_router(practice_session.router, prefix=f"{settings.API_V1_STR}/practice-sessions", tags=["practice_sessions"])
app.include_router(dashboard.router, prefix=f"{settings.API_V1_STR}/dashboard", tags=["dashboard"])
app.include_router(drill_group.router, prefix=f"{settings.API_V1_STR}/drill-groups", tags=["drill_groups"])
app.include_router(search.router, prefix=settings.API_V1_STR)
app.include_router(meta_drill_group.router, prefix=f"{settings.API_V1_STR}/meta-drill-groups", tags=["meta_drill_groups"])
app.include_router(sub_drill.router, prefix=f"{settings.API_V1_STR}/sub-drills", tags=["sub_drills"])


# Health check endpoint
@app.get("/health", tags=["health"])
async def health_check():
    return {"status": "ok"}


# Handle exceptions
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )


@app.get("/")
async def root():
    return {
        "message": "Welcome to BowlsAce API",
        "docs": f"{settings.API_V1_STR}/docs"
    }
