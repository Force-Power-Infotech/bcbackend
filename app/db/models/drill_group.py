from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Boolean, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.db.base import Base


class DrillGroup(Base):
    __tablename__ = "drill_groups"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    is_public = Column(Boolean, default=True)
    difficulty = Column(Integer, default=1)
    tags = Column(JSON, default=list)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="drill_groups")
    drills = relationship("Drill", secondary="drill_group_drills", back_populates="drill_groups")
    
    class Config:
        from_attributes = True


class DrillGroupDrills(Base):
    __tablename__ = "drill_group_drills"
    
    id = Column(Integer, primary_key=True, index=True)
    drill_group_id = Column(Integer, ForeignKey("drill_groups.id", ondelete="CASCADE"), nullable=False)
    drill_id = Column(Integer, ForeignKey("drills.id", ondelete="CASCADE"), nullable=False)
