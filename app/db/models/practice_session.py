from sqlalchemy import Column, Integer, DateTime, ForeignKey, Index
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.db.base import Base


class PracticeSession(Base):
    __tablename__ = "practice_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    drill_group_id = Column(Integer, ForeignKey("drill_groups.id", ondelete="CASCADE"), nullable=False)
    drill_id = Column(Integer, ForeignKey("drills.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="practice_sessions")
    drill_group = relationship("DrillGroup")
    drill = relationship("Drill")
    
    # Define indexes for better performance
    __table_args__ = (
        Index('idx_practice_sessions_user_id', 'user_id'),
        Index('idx_practice_sessions_drill_group_id', 'drill_group_id'),
        Index('idx_practice_sessions_drill_id', 'drill_id'),
    )
