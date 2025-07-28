from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_active_user
from app.db.base import get_db
from app.crud import crud_practice_session
from app.schemas.practice_session import (
    PracticeSessionCreate, 
    PracticeSessionResponse,
    PracticeSessionBulkResponse
)
from app.schemas.practice_session_detail import PracticeSessionDetailResponse
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
from app.db.models.practice_session import PracticeSession

@router.get("/user/{user_id}", response_model=List[PracticeSessionDetailResponse])
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
    try:
        # First check if user exists and get all related data in one query
        query = (
            select(PracticeSession)
            .join(User, PracticeSession.user_id == User.id)
            .join(Drill, PracticeSession.drill_id == Drill.id)
            .join(DrillGroup, PracticeSession.drill_group_id == DrillGroup.id)
            .where(PracticeSession.user_id == user_id)
            .order_by(PracticeSession.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        
        result = await db.execute(query)
        practice_sessions = result.scalars().all()
        
        if not practice_sessions:
            # Check if user exists to give appropriate error message
            user_query = await db.execute(select(User).where(User.id == user_id))
            user = user_query.scalars().first()
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"User with ID {user_id} not found"
                )
            # If user exists but has no sessions, return empty list
            return []
        
        detailed_responses = []
        for practice_session in practice_sessions:
            try:
                # Get all related data in a single query for drill group's drills
                drill_group_drills_query = await db.execute(
                    select(Drill)
                    .join(DrillGroup.drills)
                    .where(DrillGroup.id == practice_session.drill_group_id)
                )
                drill_group_drills = drill_group_drills_query.scalars().all()
                
                response = {
                    "id": practice_session.id,
                    "user_id": practice_session.user_id,
                    "drill_group_id": practice_session.drill_group_id,
                    "drill_id": practice_session.drill_id,
                    "created_at": practice_session.created_at,
                    "drill": {
                        "id": practice_session.drill.id,
                        "name": practice_session.drill.name,
                        "description": practice_session.drill.description,
                        "difficulty": str(practice_session.drill.difficulty),
                        "drill_type": practice_session.drill.drill_type,
                        "duration_minutes": practice_session.drill.duration_minutes,
                        "target_score": practice_session.drill.target_score,
                        "created_at": practice_session.drill.created_at
                    },
                    "drill_group": {
                        "id": practice_session.drill_group.id,
                        "name": practice_session.drill_group.name,
                        "description": practice_session.drill_group.description,
                        "is_public": practice_session.drill_group.is_public,
                        "difficulty": str(practice_session.drill_group.difficulty),
                        "tags": practice_session.drill_group.tags,
                        "created_at": practice_session.drill_group.created_at,
                        "updated_at": practice_session.drill_group.updated_at,
                        "drills": [
                            {
                                "id": d.id,
                                "name": d.name,
                                "description": d.description,
                                "difficulty": str(d.difficulty),
                                "drill_type": d.drill_type,
                                "duration_minutes": d.duration_minutes,
                                "target_score": d.target_score,
                                "created_at": d.created_at
                            } for d in drill_group_drills
                        ]
                    },
                    "user": {
                        "id": practice_session.user.id,
                        "email": practice_session.user.email,
                        "username": practice_session.user.username,
                        "full_name": practice_session.user.full_name,
                        "is_active": practice_session.user.is_active,
                        "is_admin": practice_session.user.is_admin,
                        "phone_verified": practice_session.user.phone_verified,
                        "email_verified": practice_session.user.email_verified,
                        "created_at": practice_session.user.created_at,
                        "updated_at": practice_session.user.updated_at,
                    }
                }
                
                detailed_responses.append(response)
                
            except AttributeError as e:
                # Log warning about missing related data
                print(f"Warning: Missing related data for practice session {practice_session.id}: {str(e)}")
                continue
            except Exception as e:
                # Log unexpected errors but continue
                print(f"Unexpected error processing practice session {practice_session.id}: {str(e)}")
                continue
        
        return detailed_responses
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while fetching practice sessions: {str(e)}"
        )