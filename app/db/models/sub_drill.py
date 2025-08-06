from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import sqlalchemy as sa
import uuid
from app.db.base import Base

class SubDrill(Base):
    __tablename__ = "sub_drills"
    id = Column(UUID(as_uuid=True), primary_key=True, default=sa.text('gen_random_uuid()'))
    drill_id = Column(UUID(as_uuid=True), ForeignKey('drills.id', ondelete='CASCADE'), nullable=False)
    title = Column(String(255), nullable=False)
    instruction = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
