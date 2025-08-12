from sqlalchemy import Column, Integer, String, DateTime, Boolean, UniqueConstraint, Index
import datetime
from .db import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    hashed_password = Column(String(200), nullable=False)
    first_name = Column(String(100), nullable=True)
    last_name = Column(String(100), nullable=True)
    father_name = Column(String(100), nullable=True)
    national_id = Column(String(10), unique=True, index=True, nullable=True)
    card_number = Column(String(19), nullable=True)
    phone = Column(String(11), nullable=True)
    birth_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    last_login = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True)
    role = Column(String(50), default="کارمند")

    __table_args__ = (
        UniqueConstraint("username", name="uq_users_username"),
        UniqueConstraint("national_id", name="uq_users_national_id"),
        Index("ix_users_created_at", "created_at"),
    )

class LoginHistory(Base):
    __tablename__ = "login_history"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    username = Column(String(50), nullable=False)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow, index=True)
    ip = Column(String(45), nullable=True)
