from sqlalchemy import Column, Integer, DateTime, ForeignKey, Index
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4
from app.db.base import Base


class PracticeSession(Base):
    __tablename__ = "practice_sessions"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    drill_group_id = Column(UUID(as_uuid=True), ForeignKey("drill_groups.id", ondelete="CASCADE"), nullable=False)
    drill_id = Column(UUID(as_uuid=True), ForeignKey("drills.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="practice_sessions", lazy="joined")
    drill_group = relationship("DrillGroup", lazy="joined")
    drill = relationship("Drill", back_populates="practice_sessions", foreign_keys=[drill_id], lazy="joined")
    
    # Define indexes for better performance
    __table_args__ = (
        Index('idx_practice_sessions_user_id', 'user_id'),
        Index('idx_practice_sessions_drill_group_id', 'drill_group_id'),
        Index('idx_practice_sessions_drill_id', 'drill_id'),
    )
