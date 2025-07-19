from typing import Any, Dict, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import get_db
from app.db.models.practice_session import PracticeSession
from app.db.models.shot import Shot, ShotType
from app.schemas.user import User
from app.api import deps
from app.crud import crud_user

router = APIRouter()


@router.get("/recommendation/{user_id}", response_model=Dict[str, Any])
async def get_advice_recommendations(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get personalized advice recommendations based on practice history.
    """
    # Check if user exists
    user = await crud_user.get(db, user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    
    # Check permissions (only the user or an admin can get recommendations)
    if user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    
    # Get shot type performance
    shot_type_performance = await db.execute(
        select(
            Shot.shot_type,
            func.avg(Shot.accuracy_score).label("avg_accuracy"),
            func.count(Shot.id).label("count")
        )
        .join(PracticeSession, Shot.session_id == PracticeSession.id)
        .where(PracticeSession.user_id == user_id)
        .group_by(Shot.shot_type)
    )
    
    shot_type_results = {}
    worst_shot_type = None
    worst_accuracy = float('inf')
    total_shots = 0
    
    for row in shot_type_performance:
        accuracy = float(row.avg_accuracy) if row.avg_accuracy else 0.0
        shot_type_results[row.shot_type] = {
            "accuracy": accuracy,
            "count": row.count
        }
        total_shots += row.count
        
        # Track worst performing shot type
        if accuracy < worst_accuracy and row.count >= 5:  # Minimum sample size
            worst_accuracy = accuracy
            worst_shot_type = row.shot_type
    
    # Generate recommendations based on analysis
    recommendations = []
    focus_areas = []
    
    if not shot_type_results:
        recommendations.append("Start logging your practice sessions to receive personalized advice.")
        focus_areas = ["Log at least 5 shots of each type: draw, drive, and weighted."]
    else:
        # Identify lacking areas
        for shot_type in [st.value for st in ShotType]:
            if shot_type not in shot_type_results or shot_type_results[shot_type]["count"] < 5:
                recommendations.append(f"Practice more {shot_type} shots to get better insights.")
                focus_areas.append(f"Log at least 5 {shot_type} shots.")
        
        # Advice for worst performing shot type
        if worst_shot_type:
            recommendations.append(f"Your {worst_shot_type} shots need the most improvement with an average accuracy of {worst_accuracy:.1f}/10.")
            
            # Specific drills based on shot type
            if worst_shot_type == "draw":
                focus_areas.append("Practice draw shots at varying distances to improve touch.")
                focus_areas.append("Try the 'ladder drill' - place markers at 1m intervals and aim to land between them.")
            elif worst_shot_type == "drive":
                focus_areas.append("Work on drive shot consistency with the 'clearing drill'.")
                focus_areas.append("Practice driving with different weights to improve control.")
            elif worst_shot_type == "weighted":
                focus_areas.append("Focus on weighted shot accuracy with the 'narrow gap drill'.")
                focus_areas.append("Practice weighted shots with varying backswing lengths.")
    
    return {
        "username": user.username,
        "total_shots": total_shots,
        "shot_type_performance": shot_type_results,
        "recommendations": recommendations,
        "focus_areas": focus_areas,
        "suggested_practice_time": 30 if total_shots > 100 else 20  # minutes
    }
