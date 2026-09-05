import uuid
from sqlalchemy import Column, String
from app.database.db import Base


class DiseaseInformation(Base):
    __tablename__ = "disease_information"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, unique=True, index=True, nullable=False)
    
    symptoms_en = Column(String, nullable=False)
    symptoms_ta = Column(String, nullable=False)
    
    causes_en = Column(String, nullable=False)
    causes_ta = Column(String, nullable=False)
    
    management_en = Column(String, nullable=False)
    management_ta = Column(String, nullable=False)
    
    prevention_en = Column(String, nullable=False)
    prevention_ta = Column(String, nullable=False)
    
    disclaimer_en = Column(String, nullable=False)
    disclaimer_ta = Column(String, nullable=False)
