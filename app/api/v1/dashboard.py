from typing import Any, Dict

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func, select, Integer
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import get_db
from app.db.models.session import Session
from app.db.models.shot import Shot
from app.db.models.drill import Drill
from app.db.models.challenge import Challenge, ChallengeStatus
from app.schemas.user import User
from app.api import deps
from app.crud import crud_user

router = APIRouter()


@router.get("/{user_id}", response_model=Dict[str, Any])
async def get_dashboard_metrics(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get dashboard metrics for a user.
    """
    # Check if user exists
    user = await crud_user.get(db, user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    
    # Check permissions (only the user or an admin can see their own dashboard)
    if user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    
    # Get session count
    session_count = await db.execute(
        select(func.count(Session.id)).where(Session.user_id == user_id)
    )
    
    # Get shot metrics
    shot_metrics = await db.execute(
        select(
            func.count(Shot.id).label("total_shots"),
            func.avg(Shot.accuracy_score).label("average_accuracy")
        )
        .join(Session, Shot.session_id == Session.id)
        .where(Session.user_id == user_id)
    )
    
    shot_result = shot_metrics.first()
    
    # Get challenge metrics
    challenge_metrics = await db.execute(
        select(
            func.count(Challenge.id).label("total_challenges"),
            func.sum(
                (Challenge.status == ChallengeStatus.COMPLETED).cast(Integer)
            ).label("completed_challenges")
        )
        .where(
            (Challenge.sender_id == user_id) | (Challenge.recipient_id == user_id)
        )
    )
    
    challenge_result = challenge_metrics.first()
    
    # Get recent improvement trend (compare last 10 sessions)
    recent_shots = await db.execute(
        select(
            Session.id,
            func.avg(Shot.accuracy_score).label("avg_accuracy")
        )
        .join(Shot, Session.id == Shot.session_id)
        .where(Session.user_id == user_id)
        .group_by(Session.id)
        .order_by(Session.created_at.desc())
        .limit(10)
    )
    
    recent_scores = [row.avg_accuracy for row in recent_shots if row.avg_accuracy is not None]
    improvement_trend = None
    if len(recent_scores) >= 2:
        # Simple trend calculation
        first_half = sum(recent_scores[len(recent_scores)//2:]) / (len(recent_scores) - len(recent_scores)//2)
        second_half = sum(recent_scores[:len(recent_scores)//2]) / (len(recent_scores)//2)
        improvement_trend = second_half - first_half
    
    return {
        "username": user.username,
        "total_sessions": session_count.scalar() or 0,
        "total_shots": shot_result.total_shots if shot_result else 0,
        "average_accuracy": float(shot_result.average_accuracy) if shot_result and shot_result.average_accuracy else 0.0,
        "total_challenges": challenge_result.total_challenges if challenge_result else 0,
        "completed_challenges": challenge_result.completed_challenges if challenge_result and challenge_result.completed_challenges else 0,
        "improvement_trend": float(improvement_trend) if improvement_trend is not None else 0.0
    }
