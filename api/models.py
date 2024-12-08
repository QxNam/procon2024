from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float, Boolean
from sqlalchemy.orm import relationship
from .database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    username = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)

    # Quan hệ với Submit
    submits = relationship("Submit", back_populates="user", cascade="all, delete-orphan")

class Submit(Base):
    __tablename__ = "submits"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    question_id = Column(Integer, nullable=False)
    max_score = Column(Integer, nullable=False)
    start_time = Column(DateTime, default=datetime.utcnow, nullable=False)
    end_time = Column(DateTime, nullable=True)
    step_count = Column(Integer)
    resubmission_count = Column(Integer, default=0)
    total_time = Column(Float, default=0.0)
    status = Column(Integer, default=0)
    score = Column(Float)

    # Quan hệ ngược với User
    user = relationship("User", back_populates="submits")