import enum
import uuid
from datetime import datetime

from sqlalchemy import Column, String, DateTime, Enum as SAEnum
from sqlalchemy.orm import relationship
from app.database.db import Base


class UserRole(str, enum.Enum):
    farmer = "farmer"
    factory = "factory"


class Language(str, enum.Enum):
    en = "en"
    ta = "ta"


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=True)
    phone = Column(String, unique=True, index=True, nullable=True)
    password_hash = Column(String, nullable=False)
    role = Column(SAEnum(UserRole), nullable=False, default=UserRole.farmer)
    preferred_language = Column(SAEnum(Language), nullable=False, default=Language.en)
    village = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    diagnoses = relationship("Diagnosis", back_populates="user", cascade="all, delete-orphan")
    listings = relationship("CocoonListing", back_populates="user", cascade="all, delete-orphan")