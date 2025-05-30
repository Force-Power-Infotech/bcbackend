from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Text, Float
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid

from app.db.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    phone_number = Column(String(20), unique=True, index=True, nullable=False)
    phone_verified = Column(Boolean, default=False, nullable=False)
    email_verified = Column(Boolean, default=False, nullable=False)
    full_name = Column(String)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    otp = Column(String(6), nullable=True)  # Add OTP column to store the current OTP
    
    # Relationships
    sessions = relationship("Session", back_populates="user")
    sent_challenges = relationship("Challenge", back_populates="sender", foreign_keys="Challenge.sender_id")
    received_challenges = relationship("Challenge", back_populates="recipient", foreign_keys="Challenge.recipient_id")
