from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Text, Float
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.db.base import Base


class Drill(Base):
    __tablename__ = "drills"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("sessions.id"), nullable=True)  # Made nullable for template drills
    name = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    target_score = Column(Integer)  # Expected performance threshold
    difficulty = Column(Integer)  # 1-10 scale
    drill_type = Column(String, nullable=False)  # Type of drill (DRAW, DRIVE, etc.)
    duration_minutes = Column(Integer, nullable=False)  # Duration in minutes
    created_at = Column(DateTime(timezone=True), server_default=func.now())
      # Relationships
    session = relationship("Session", back_populates="drills")
    shots = relationship("Shot", back_populates="drill")
    drill_groups = relationship("DrillGroup", secondary="drill_group_drills", back_populates="drills")
