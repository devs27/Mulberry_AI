import uuid
from datetime import datetime
from sqlalchemy import Column, String, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.database.db import Base


class Diagnosis(Base):
    __tablename__ = "diagnoses"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), index=True, nullable=False)
    disease = Column(String, nullable=False)
    confidence = Column(Float, nullable=False)
    variety = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    severity = Column(String, nullable=True)
    is_uncertain = Column(Boolean, default=False, nullable=False)
    image_path = Column(String, nullable=True)

    # Relationship to user
    user = relationship("User", back_populates="diagnoses")
