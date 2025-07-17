from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_active_user
from app.db.base import get_db
from app.crud import crud_practice_session
from app.schemas.practice_session import (
    PracticeSessionCreate, 
    PracticeSessionResponse,
    PracticeSessionDetailResponse,
    PracticeSessionBulkResponse
)
from app.db.models.user import User

router = APIRouter()


@router.post("/", response_model=PracticeSessionBulkResponse)
async def create_practice_sessions(
    *,
    db: AsyncSession = Depends(get_db),
    practice_data: PracticeSessionCreate
):
    """
    Create multiple practice session entries for a user.
    """
    try:
        practice_sessions = await crud_practice_session.create_practice_sessions(
            db=db,
            user_id=practice_data.user_id,
            drill_group_id=practice_data.drill_group_id,
            drill_ids=practice_data.drill_ids
        )
        
        # Convert to response model
        practice_session_responses = [
            PracticeSessionResponse(
                id=session.id,
                user_id=session.user_id,
                drill_group_id=session.drill_group_id,
                drill_id=session.drill_id,
                created_at=session.created_at
            ) for session in practice_sessions
        ]
        
        # Return bulk response
        return PracticeSessionBulkResponse(
            practice_sessions=practice_session_responses,
            message=f"Successfully created {len(practice_sessions)} practice sessions."
        )
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred: {str(e)}"
        )


from sqlalchemy import select
from app.db.models.drill import Drill
from app.db.models.drill_group import DrillGroup
from app.db.models.user import User

@router.get("/user/{user_id}")
async def get_user_practice_sessions(
    user_id: int,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
):
    """
    Get all practice sessions for a user with detailed information about drills and drill groups.
    
    Returns:
    - Detailed information about each practice session
    - Information about the associated drill and drill group
    """
    # For testing purposes: No authentication required
    # In production, you would add back the authentication check
        
    practice_sessions = await crud_practice_session.get_user_practice_sessions(
        db=db, user_id=user_id, skip=skip, limit=limit
    )
    
    # Create a detailed response manually
    detailed_responses = []
    for ps in practice_sessions:
        # Get drill information
        drill_query = await db.execute(select(Drill).where(Drill.id == ps.drill_id))
        drill = drill_query.scalars().first()
        
        # Get drill group information
        drill_group_query = await db.execute(select(DrillGroup).where(DrillGroup.id == ps.drill_group_id))
        drill_group = drill_group_query.scalars().first()
        
        # Get user information
        user_query = await db.execute(select(User).where(User.id == ps.user_id))
        user = user_query.scalars().first()
        
        # Get drills for drill group
        drill_group_drills_query = await db.execute(
            select(Drill)
            .join(DrillGroup.drills)
            .where(DrillGroup.id == ps.drill_group_id)
        )
        drill_group_drills = drill_group_drills_query.scalars().all()
        
        response = {
            "id": ps.id,
            "user_id": ps.user_id,
            "drill_group_id": ps.drill_group_id,
            "drill_id": ps.drill_id,
            "created_at": ps.created_at,
            "drill": {
                "id": drill.id,
                "name": drill.name,
                "description": drill.description,
                "difficulty": drill.difficulty,
                "drill_type": drill.drill_type,
                "duration_minutes": drill.duration_minutes,
                "target_score": drill.target_score,
                "created_at": drill.created_at
            },
            "drill_group": {
                "id": drill_group.id,
                "name": drill_group.name,
                "description": drill_group.description,
                "is_public": drill_group.is_public,
                "difficulty": drill_group.difficulty,
                "tags": drill_group.tags,
                "created_at": drill_group.created_at,
                "updated_at": drill_group.updated_at,
                "drills": [
                    {
                        "id": d.id,
                        "name": d.name,
                        "description": d.description,
                        "difficulty": d.difficulty,
                        "drill_type": d.drill_type,
                        "duration_minutes": d.duration_minutes,
                        "target_score": d.target_score,
                        "created_at": d.created_at
                    } for d in drill_group_drills
                ]
            },
            "user": {
                "id": user.id,
                "email": user.email,
                "username": user.username,
                "full_name": user.full_name,
                "is_active": user.is_active,
                "is_admin": user.is_admin,
                "phone_verified": user.phone_verified,
                "email_verified": user.email_verified,
                "created_at": user.created_at,
                "updated_at": user.updated_at,
            }
        }
        
        detailed_responses.append(response)
    
    return detailed_responses
