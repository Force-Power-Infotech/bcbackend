from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Boolean, JSON, Index, sql as sa
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base import Base

class DrillGroupDrills(Base):
    __tablename__ = "drill_group_drills"
    drill_group_id = Column(UUID(as_uuid=True), ForeignKey("drill_groups.id", ondelete="CASCADE"), nullable=False, primary_key=True)
    drill_id = Column(UUID(as_uuid=True), ForeignKey("drills.id", ondelete="CASCADE"), nullable=False, primary_key=True)
    __table_args__ = (
        Index('idx_drill_group_drills_drill_id', 'drill_id'),
        Index('idx_drill_group_drills_group_id', 'drill_group_id'),
    )

class DrillGroup(Base):
    __tablename__ = "drill_groups"
    id = Column(UUID(as_uuid=True), primary_key=True, default=sa.text('gen_random_uuid()'))
    meta_drill_group_id = Column(UUID(as_uuid=True), ForeignKey('meta_drill_groups.id', ondelete='CASCADE'), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    is_public = Column(Boolean, nullable=False, server_default=sa.text('true'))
    difficulty = Column(Integer, nullable=True)
    tags = Column(JSON, nullable=True, server_default='[]')
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())
    image = Column(String(255), nullable=True)

    user = relationship("User", back_populates="drill_groups")
    drills = relationship("Drill", secondary="drill_group_drills", back_populates="drill_groups")

    @property
    def difficulty_str(self):
        return str(self.difficulty) if self.difficulty is not None else "1"
