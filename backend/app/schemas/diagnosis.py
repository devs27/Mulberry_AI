from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class DiagnosisOut(BaseModel):
    id: str
    user_id: str
    disease: str
    confidence: float
    variety: str
    timestamp: datetime
    severity: Optional[str] = None
    is_uncertain: bool
    image_path: Optional[str] = None

    class Config:
        from_attributes = True
