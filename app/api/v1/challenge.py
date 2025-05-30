from typing import Any, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta

from app.db.base import get_db
from app.schemas.user import User
from app.schemas.challenge import Challenge, ChallengeCreate, ChallengeUpdate, ChallengeWithUsers, ChallengeStatusEnum
from app.api import deps
from app.crud import crud_challenge, crud_user

router = APIRouter()


@router.post("/send", response_model=Challenge)
async def send_challenge(
    challenge_in: ChallengeCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Send a challenge to another user.
    """
    # Check if recipient exists
    recipient = await crud_user.get(db, user_id=challenge_in.recipient_id)
    if not recipient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recipient user not found",
        )
    
    # Create the challenge
    challenge = await crud_challenge.create(
        db, 
        obj_in=challenge_in, 
        sender_id=current_user.id
    )
    
    return challenge


@router.get("/", response_model=List[Challenge])
async def list_challenges(
    status: Optional[List[ChallengeStatusEnum]] = Query(None),
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    List all challenges for the current user (sent or received).
    """
    challenges = await crud_challenge.get_user_challenges(
        db, 
        user_id=current_user.id,
        status=status,
        skip=skip, 
        limit=limit
    )
    
    return challenges


@router.get("/{challenge_id}", response_model=ChallengeWithUsers)
async def get_challenge(
    challenge_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get a specific challenge by ID.
    """
    challenge = await crud_challenge.get_with_users(db, challenge_id=challenge_id)
    if not challenge:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Challenge not found",
        )
    
    # Check if the user is involved in this challenge
    if challenge["sender_id"] != current_user.id and challenge["recipient_id"] != current_user.id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    
    return challenge


@router.put("/{challenge_id}/accept", response_model=Challenge)
async def accept_challenge(
    challenge_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Accept a challenge.
    """
    challenge = await crud_challenge.get(db, challenge_id=challenge_id)
    if not challenge:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Challenge not found",
        )
    
    # Check if the user is the recipient of this challenge
    if challenge.recipient_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only the challenge recipient can accept it",
        )
    
    # Check if challenge can be accepted (is pending and not expired)
    if challenge.status != ChallengeStatusEnum.PENDING:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Challenge is not pending (current status: {challenge.status})",
        )
    
    if challenge.expires_at and challenge.expires_at < datetime.utcnow():
        await crud_challenge.update_status(db, challenge_id=challenge_id, status=ChallengeStatusEnum.EXPIRED)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Challenge has expired",
        )
    
    updated_challenge = await crud_challenge.update_status(
        db, 
        challenge_id=challenge_id, 
        status=ChallengeStatusEnum.ACCEPTED
    )
    
    return updated_challenge


@router.put("/{challenge_id}/decline", response_model=Challenge)
async def decline_challenge(
    challenge_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Decline a challenge.
    """
    challenge = await crud_challenge.get(db, challenge_id=challenge_id)
    if not challenge:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Challenge not found",
        )
    
    # Check if the user is the recipient of this challenge
    if challenge.recipient_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only the challenge recipient can decline it",
        )
    
    # Check if challenge can be declined (is pending)
    if challenge.status != ChallengeStatusEnum.PENDING:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Challenge is not pending (current status: {challenge.status})",
        )
    
    updated_challenge = await crud_challenge.update_status(
        db, 
        challenge_id=challenge_id, 
        status=ChallengeStatusEnum.DECLINED
    )
    
    return updated_challenge


@router.put("/{challenge_id}/complete", response_model=Challenge)
async def complete_challenge(
    challenge_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Mark a challenge as completed.
    """
    challenge = await crud_challenge.get(db, challenge_id=challenge_id)
    if not challenge:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Challenge not found",
        )
    
    # Check if the user is involved in this challenge
    if challenge.sender_id != current_user.id and challenge.recipient_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    
    # Check if challenge can be completed (is accepted)
    if challenge.status != ChallengeStatusEnum.ACCEPTED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Challenge must be accepted before it can be completed (current status: {challenge.status})",
        )
    
    updated_challenge = await crud_challenge.update_status(
        db, 
        challenge_id=challenge_id, 
        status=ChallengeStatusEnum.COMPLETED
    )
    
    return updated_challenge
