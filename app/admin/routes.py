from typing import Optional
from datetime import datetime, timedelta
from fastapi import APIRouter, Request, Form, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, and_
from starlette.status import HTTP_401_UNAUTHORIZED

from app.db.base import get_db
from app.crud import crud_user, crud_practice, crud_challenge
from app.schemas.user import User
from app.api import deps

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")
security = HTTPBasic()

# Admin credentials - in production, these should be in environment variables
ADMIN_CREDENTIALS = {
    "username": "admin",
    "password": "1234"
}

# --- Auth Middleware and Dependencies ---

def require_admin_auth(request: Request):
    """Check if admin is authenticated"""
    if request.cookies.get("admin_logged_in") != "true":
        return RedirectResponse(url="/admin/login", status_code=302)

def get_admin_context(request: Request):
    """Get common admin template context"""
    return {
        "request": request,
        "current_admin": {
            "username": request.cookies.get("admin_username", ADMIN_CREDENTIALS["username"])
        }
    }

# --- Authentication Routes ---

@router.get("/login", response_class=HTMLResponse, name="admin_login_get")
def login_get(request: Request):
    # Redirect to dashboard if already logged in
    if request.cookies.get("admin_logged_in") == "true":
        return RedirectResponse(url="/admin", status_code=302)
    return templates.TemplateResponse("admin/login.html", {"request": request})

@router.post("/login", response_class=HTMLResponse, name="admin_login")
def login_post(request: Request, username: str = Form(...), password: str = Form(...)):
    if username == ADMIN_CREDENTIALS["username"] and password == ADMIN_CREDENTIALS["password"]:
        response = RedirectResponse(url="/admin", status_code=302)
        response.set_cookie(key="admin_logged_in", value="true", httponly=True)
        response.set_cookie(key="admin_username", value=username, httponly=True)
        return response
    
    return templates.TemplateResponse(
        "admin/login.html",
        {"request": request, "error": "Invalid username or password"},
        status_code=401
    )

@router.get("/logout", name="admin_logout")
def logout():
    response = RedirectResponse(url="/admin/login", status_code=302)
    response.delete_cookie(key="admin_logged_in")
    response.delete_cookie(key="admin_username")
    return response

# --- Dashboard Routes ---

@router.get("/", response_class=HTMLResponse, name="admin_dashboard")
async def admin_dashboard(
    request: Request, 
    auth=Depends(require_admin_auth),
    db: AsyncSession = Depends(get_db)
):
    if isinstance(auth, RedirectResponse):
        return auth
    
    # Get live statistics
    today = datetime.now()
    today_start = datetime(today.year, today.month, today.day)

    # User statistics
    total_users = await crud_user.get_count(db)
    new_users_today = await crud_user.get_count(
        db, 
        created_at_after=today_start
    )

    # Session statistics
    total_sessions = await crud_practice.get_session_count(db)
    new_sessions_today = await crud_practice.get_session_count(
        db,
        created_at_after=today_start
    )

    # Shot statistics
    total_shots = await crud_practice.get_shot_count(db)
    new_shots_today = await crud_practice.get_shot_count(
        db,
        created_at_after=today_start
    )

    # Challenge statistics
    active_challenges = await crud_challenge.get_count(
        db,
        status="active"
    )
    completed_challenges_today = await crud_challenge.get_count(
        db,
        status="completed",
        completed_at_after=today_start
    )

    # User growth chart data (last 6 months)
    months = []
    user_counts = []
    for i in range(5, -1, -1):
        month_date = today - timedelta(days=i*30)
        months.append(month_date.strftime("%b"))
        count = await crud_user.get_count(
            db,
            created_at_before=month_date
        )
        user_counts.append(count)

    # Shot performance chart data
    shot_types = ["Draw", "Drive", "Weight"]
    accuracies = []
    for shot_type in shot_types:
        accuracy = await crud_practice.get_average_accuracy(
            db,
            shot_type=shot_type
        )
        accuracies.append(accuracy or 0)

    # Recent activities
    recent_activities = await crud_practice.get_recent_activities(db, limit=5)
    
    stats = {
        "total_users": total_users,
        "new_users_today": new_users_today,
        "total_sessions": total_sessions,
        "new_sessions_today": new_sessions_today,
        "total_shots": total_shots,
        "new_shots_today": new_shots_today,
        "active_challenges": active_challenges,
        "completed_challenges_today": completed_challenges_today
    }
    
    chart_data = {
        "user_growth": {
            "labels": months,
            "data": user_counts
        },
        "shot_performance": {
            "labels": shot_types,
            "data": accuracies
        }
    }
    
    context = get_admin_context(request)
    context["stats"] = stats
    context["chart_data"] = chart_data
    context["recent_activities"] = recent_activities
    return templates.TemplateResponse("admin/dashboard.html", context)

# --- User Management Routes ---

@router.get("/users", response_class=HTMLResponse, name="admin_users")
async def admin_users(
    request: Request, 
    auth=Depends(require_admin_auth),
    db: AsyncSession = Depends(get_db),
    page: int = 1,
    search: Optional[str] = None
):
    if isinstance(auth, RedirectResponse):
        return auth
    
    per_page = 20
    skip = (page - 1) * per_page
    
    users = await crud_user.get_multi(
        db,
        skip=skip,
        limit=per_page,
        search=search
    )
    total = await crud_user.get_count(db, search=search)
    
    context = get_admin_context(request)
    context.update({
        "users": users,
        "total": total,
        "page": page,
        "pages": (total + per_page - 1) // per_page,
        "search": search
    })
    return templates.TemplateResponse("admin/users.html", context)

# --- Session Management Routes ---

@router.get("/sessions", response_class=HTMLResponse, name="admin_sessions")
async def admin_sessions(
    request: Request, 
    auth=Depends(require_admin_auth),
    db: AsyncSession = Depends(get_db),
    page: int = 1,
    user_id: Optional[int] = None
):
    if isinstance(auth, RedirectResponse):
        return auth
    
    per_page = 20
    skip = (page - 1) * per_page
    
    sessions = await crud_practice.get_sessions(
        db,
        skip=skip,
        limit=per_page,
        user_id=user_id
    )
    total = await crud_practice.get_session_count(db, user_id=user_id)
    
    context = get_admin_context(request)
    context.update({
        "sessions": sessions,
        "total": total,
        "page": page,
        "pages": (total + per_page - 1) // per_page,
        "user_id": user_id
    })
    return templates.TemplateResponse("admin/sessions.html", context)

# --- Shot Analytics Routes ---

@router.get("/shots", response_class=HTMLResponse, name="admin_shots")
async def admin_shots(
    request: Request, 
    auth=Depends(require_admin_auth),
    db: AsyncSession = Depends(get_db),
    page: int = 1,
    session_id: Optional[int] = None
):
    if isinstance(auth, RedirectResponse):
        return auth
    
    per_page = 50
    skip = (page - 1) * per_page
    
    shots = await crud_practice.get_shots(
        db,
        skip=skip,
        limit=per_page,
        session_id=session_id
    )
    total = await crud_practice.get_shot_count(db, session_id=session_id)
    
    # Get analytics
    shot_analytics = await crud_practice.get_shot_analytics(db)
    
    context = get_admin_context(request)
    context.update({
        "shots": shots,
        "total": total,
        "page": page,
        "pages": (total + per_page - 1) // per_page,
        "session_id": session_id,
        "shot_analytics": shot_analytics
    })
    return templates.TemplateResponse("admin/shots.html", context)

# --- Drill Management Routes ---

@router.get("/drills", response_class=HTMLResponse, name="admin_drills")
async def admin_drills(
    request: Request, 
    auth=Depends(require_admin_auth),
    db: AsyncSession = Depends(get_db),
    page: int = 1
):
    if isinstance(auth, RedirectResponse):
        return auth
    
    per_page = 20
    skip = (page - 1) * per_page
    
    drills = await crud_practice.get_drills(
        db,
        skip=skip,
        limit=per_page
    )
    total = await crud_practice.get_drill_count(db)
    
    context = get_admin_context(request)
    context.update({
        "drills": drills,
        "total": total,
        "page": page,
        "pages": (total + per_page - 1) // per_page
    })
    return templates.TemplateResponse("admin/drills.html", context)

# --- Challenge Management Routes ---

@router.get("/challenges", response_class=HTMLResponse, name="admin_challenges")
async def admin_challenges(
    request: Request, 
    auth=Depends(require_admin_auth),
    db: AsyncSession = Depends(get_db),
    page: int = 1,
    status: Optional[str] = None
):
    if isinstance(auth, RedirectResponse):
        return auth
    
    per_page = 20
    skip = (page - 1) * per_page
    
    challenges = await crud_challenge.get_multi(
        db,
        skip=skip,
        limit=per_page,
        status=status
    )
    total = await crud_challenge.get_count(db, status=status)
    
    context = get_admin_context(request)
    context.update({
        "challenges": challenges,
        "total": total,
        "page": page,
        "pages": (total + per_page - 1) // per_page,
        "status": status
    })
    return templates.TemplateResponse("admin/challenges.html", context)

# --- Metrics Routes ---

@router.get("/metrics", response_class=HTMLResponse, name="admin_metrics")
async def admin_metrics(
    request: Request, 
    auth=Depends(require_admin_auth),
    db: AsyncSession = Depends(get_db)
):
    if isinstance(auth, RedirectResponse):
        return auth

    # Get various metrics for different time periods
    today = datetime.now()
    week_ago = today - timedelta(days=7)
    month_ago = today - timedelta(days=30)
    
    metrics = {
        "users": {
            "total": await crud_user.get_count(db),
            "week": await crud_user.get_count(db, created_at_after=week_ago),
            "month": await crud_user.get_count(db, created_at_after=month_ago)
        },
        "sessions": {
            "total": await crud_practice.get_session_count(db),
            "week": await crud_practice.get_session_count(db, created_at_after=week_ago),
            "month": await crud_practice.get_session_count(db, created_at_after=month_ago)
        },
        "shots": {
            "total": await crud_practice.get_shot_count(db),
            "week": await crud_practice.get_shot_count(db, created_at_after=week_ago),
            "month": await crud_practice.get_shot_count(db, created_at_after=month_ago)
        },
        "challenges": {
            "total": await crud_challenge.get_count(db),
            "completed": await crud_challenge.get_count(db, status="completed"),
            "completion_rate": await crud_challenge.get_completion_rate(db)
        }
    }
    
    context = get_admin_context(request)
    context["metrics"] = metrics
    return templates.TemplateResponse("admin/metrics.html", context)
