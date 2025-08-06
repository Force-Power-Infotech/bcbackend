from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from app.api.deps import get_current_active_user
from app.db.base import get_db
from app.crud import crud_practice_session
from app.schemas.practice_session import (
    PracticeSessionCreate, 
    PracticeSessionResponse,
    PracticeSessionBulkResponse,
    PracticeSessionDetailResponse
)
from app.db.models.user import User
from sqlalchemy import select, cast
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import selectinload
from app.db.models.drill import Drill
from app.db.models.drill_group import DrillGroup
from app.db.models.practice_session import PracticeSession

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


@router.get("/user/{user_id}", response_model=List[PracticeSessionDetailResponse])
async def get_user_practice_sessions(
    user_id: UUID,  # ✅ Corrected
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
        # First check if user exists
        user_query = await db.execute(select(User).where(User.id == user_id))
        user = user_query.scalar_one_or_none()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with ID {user_id} not found"
            )
        
        # Get practice sessions for the user with all related data in a single query
        # First, check if there are any practice sessions for this user
        ps_count_query = (
            select(PracticeSession)
            .where(PracticeSession.user_id == user_id)
        )
        result = await db.execute(ps_count_query)
        practice_sessions_exist = result.first() is not None

        if not practice_sessions_exist:
            return []

        # If practice sessions exist, load them with their relationships
        ps_query = (
            select(PracticeSession)
            .options(
                selectinload(PracticeSession.user),
                selectinload(PracticeSession.drill_group),
                selectinload(PracticeSession.drill)
            )
            .where(PracticeSession.user_id == user_id)
            .order_by(PracticeSession.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        
        try:
            print("Executing query:", str(ps_query.compile(compile_kwargs={"literal_binds": True})))
            result = await db.execute(ps_query)
            practice_sessions = result.unique().scalars().all()
            print("Query result count:", len(practice_sessions) if practice_sessions else 0)
            
            if not practice_sessions:
                return []

            # Log UUIDs for verification
            print("First session UUID values:", {
                "drill_group_id": str(practice_sessions[0].drill_group_id) if practice_sessions else None,
                "drill_id": str(practice_sessions[0].drill_id) if practice_sessions else None
            })
        except Exception as e:
            import traceback
            print(f"Database query error: {str(e)}")
            print("Full traceback:", traceback.format_exc())
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error executing database query: {str(e)}\nTraceback: {traceback.format_exc()}"
            )
        
        detailed_responses = []
        for ps in practice_sessions:
            try:
                drill = ps.drill
                drill_group = ps.drill_group
                
                if not drill:
                    print(f"Warning: Drill {ps.drill_id} not found for practice session {ps.id}")
                    continue
                
                if not drill_group:
                    print(f"Warning: Drill group {ps.drill_group_id} not found for practice session {ps.id}")
                    continue
                
                # Get drill group's drills from the relationship
                drill_group_drills = drill_group.drills
                
                response = PracticeSessionDetailResponse(
                    id=ps.id,
                    user_id=ps.user_id,
                    drill_group_id=ps.drill_group_id,
                    drill_id=ps.drill_id,
                    created_at=ps.created_at,
                    drill={
                        "id": drill.id,
                        "name": drill.name,
                        "description": drill.description,
                        "difficulty": str(drill.difficulty),
                        "drill_type": drill.drill_type,
                        "duration_minutes": drill.duration_minutes,
                        "target_score": drill.target_score,
                        "created_at": drill.created_at
                    },
                    drill_group={
                        "id": drill_group.id,
                        "name": drill_group.name,
                        "description": drill_group.description,
                        "is_public": drill_group.is_public,
                        "difficulty": str(drill_group.difficulty),
                        "tags": drill_group.tags,
                        "created_at": drill_group.created_at,
                        "updated_at": drill_group.updated_at,
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
                    user={
                        "id": user.id,
                        "email": user.email,
                        "username": user.username,
                        "full_name": user.full_name,
                        "is_active": user.is_active,
                        "is_admin": user.is_admin,
                        "phone_verified": user.phone_verified,
                        "email_verified": user.email_verified,
                        "created_at": user.created_at,
                        "updated_at": user.updated_at
                    }
                )
                
                detailed_responses.append(response)
                
            except AttributeError as e:
                print(f"Warning: Missing related data for practice session {ps.id}: {str(e)}")
                continue
            except Exception as e:
                print(f"Unexpected error processing practice session {ps.id}: {str(e)}")
                continue
        
        return detailed_responses
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while fetching practice sessions: {str(e)}"
        )
