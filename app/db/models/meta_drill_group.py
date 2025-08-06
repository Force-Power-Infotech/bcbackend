from sqlalchemy import Column, String, Text, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import sqlalchemy as sa
import uuid
from app.db.base import Base

class MetaDrillGroup(Base):
    __tablename__ = "meta_drill_groups"
    id = Column(UUID(as_uuid=True), primary_key=True, default=sa.text('gen_random_uuid()'))
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
