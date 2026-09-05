import uuid
from datetime import datetime
from sqlalchemy import Column, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database.db import Base


class CocoonListing(Base):
    __tablename__ = "cocoon_listings"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), index=True, nullable=False)
    variety = Column(String, nullable=False)
    price_per_kg = Column(Float, nullable=False)
    quantity_kg = Column(Float, nullable=False)
    location = Column(String, nullable=False)
    contact_phone = Column(String, nullable=False)
    status = Column(String, default="active", nullable=False) # "active" or "sold"
    description = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationship to user
    user = relationship("User", back_populates="listings")
