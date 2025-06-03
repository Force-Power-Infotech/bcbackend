from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.core.config import settings
from app.api.v1 import auth, user, practice, challenge, dashboard, advisor, admin, drill_group, drill
from app.admin import routes as admin_routes

# Create FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url=f"{settings.API_V1_STR}/docs",
    redoc_url=f"{settings.API_V1_STR}/redoc",
)

# Set up session middleware
from starlette.middleware.sessions import SessionMiddleware
app.add_middleware(
    SessionMiddleware,
    secret_key="your-secret-key-here",  # Replace with a secure secret key
    session_cookie="bowlsace_session",
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
app.include_router(user.router, prefix=f"{settings.API_V1_STR}/users", tags=["users"])
app.include_router(drill.router, prefix=f"{settings.API_V1_STR}/drill", tags=["drill"])
app.include_router(practice.router, prefix=f"{settings.API_V1_STR}/practice", tags=["practice"])
app.include_router(challenge.router, prefix=f"{settings.API_V1_STR}/challenge", tags=["challenge"])
app.include_router(dashboard.router, prefix=f"{settings.API_V1_STR}/dashboard", tags=["dashboard"])
app.include_router(advisor.router, prefix=f"{settings.API_V1_STR}/advisor", tags=["advisor"])
app.include_router(admin.router, prefix=f"{settings.API_V1_STR}/admin", tags=["admin"])
app.include_router(drill_group.router, prefix=f"{settings.API_V1_STR}/drill-groups", tags=["drill_groups"])

# Include Admin UI routes
app.include_router(admin_routes.router, prefix="/admin", tags=["admin_ui"])


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
