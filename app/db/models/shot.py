from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Text, Float, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum

from app.db.base_class import Base


class ShotType(str, enum.Enum):
    DRAW = "draw"
    DRIVE = "drive"
    WEIGHTED = "weighted"


class Shot(Base):
    __tablename__ = "shots"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("sessions.id", ondelete="CASCADE"), nullable=False, index=True)
    drill_id = Column(Integer, ForeignKey("drills.id", ondelete="SET NULL"), nullable=True, index=True)
    
    # Shot details
    shot_type = Column(Enum(ShotType, name="shottype"), nullable=False)
    distance_meters = Column(Float, nullable=True)
    accuracy_score = Column(Integer, nullable=True)  # 1-10 scale
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    
    # Relationships
    drill = relationship("Drill", back_populates="shots", uselist=False)
