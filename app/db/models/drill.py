from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Text, Float
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Drill(Base):
    __tablename__ = "drills"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    difficulty = Column(Integer, nullable=False, server_default='1')
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())
    target_score = Column(Integer, nullable=True)
    drill_type = Column(String(50), nullable=False)
    duration_minutes = Column(Integer, nullable=True)

    # Relationships
    practice_sessions = relationship("PracticeSession", back_populates="drill", foreign_keys="PracticeSession.drill_id")
    drill_groups = relationship("DrillGroup", secondary="drill_group_drills", back_populates="drills")
    shots = relationship("Shot", back_populates="drill", cascade="all, delete-orphan")
