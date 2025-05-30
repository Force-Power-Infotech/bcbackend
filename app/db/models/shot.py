from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Text, Float, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum

from app.db.base import Base


class ShotType(str, enum.Enum):
    DRAW = "draw"
    DRIVE = "drive"
    WEIGHTED = "weighted"


class Shot(Base):
    __tablename__ = "shots"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("sessions.id"), nullable=False)
    drill_id = Column(Integer, ForeignKey("drills.id"), nullable=True)
    
    # Shot details
    shot_type = Column(Enum(ShotType), nullable=False)
    distance_meters = Column(Float)
    accuracy_score = Column(Integer)  # 1-10 scale
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    session = relationship("Session", back_populates="shots")
    drill = relationship("Drill", back_populates="shots")
