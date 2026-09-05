import re
from datetime import datetime
from typing import Optional, Dict
from pydantic import BaseModel, Field, field_validator


class ListingCreate(BaseModel):
    variety: str = Field(..., description="Cocoon variety (e.g. Bivoltine, Multivoltine, Crossbreed)")
    price_per_kg: float = Field(..., description="Price in Rs per kg")
    quantity_kg: float = Field(..., description="Quantity in kg")
    location: str = Field(..., description="Location of cocoons")
    contact_phone: str = Field(..., description="Seller phone number")
    description: Optional[str] = Field(None, description="Optional notes")

    @field_validator("variety")
    @classmethod
    def validate_variety(cls, value: str):
        if not value or not value.strip():
            raise ValueError("Variety cannot be empty")
        return value.strip()

    @field_validator("price_per_kg")
    @classmethod
    def validate_price(cls, value: float):
        if value <= 0:
            raise ValueError("Price per kg must be greater than zero")
        return value

    @field_validator("quantity_kg")
    @classmethod
    def validate_quantity(cls, value: float):
        if value <= 0:
            raise ValueError("Quantity in kg must be greater than zero")
        return value

    @field_validator("location")
    @classmethod
    def validate_location(cls, value: str):
        if not value or not value.strip():
            raise ValueError("Location is required")
        return value.strip()

    @field_validator("contact_phone")
    @classmethod
    def validate_phone(cls, value: str):
        if not value or not value.strip():
            raise ValueError("Contact phone is required")
        # Basic check: at least 8 digits
        clean_phone = re.sub(r"\D", "", value)
        if len(clean_phone) < 8:
            raise ValueError("Phone number must have at least 8 digits")
        return value.strip()


class ListingOut(BaseModel):
    id: str
    user_id: str
    variety: str
    price_per_kg: float
    quantity_kg: float
    location: str
    contact_phone: str
    status: str
    description: Optional[str]
    created_at: datetime
    
    # Bilingual disclaimers returned automatically with every listing
    quality_disclaimer: Dict[str, str] = {
        "en": "All listings are self-reported by farmers. Buyers must perform physical cocoon shell weight tests and check pupal condition before transaction.",
        "ta": "அனைத்து பதிவுகளும் விவசாயிகளால் சுய-அறிவிக்கப்பட்டவை. வாங்குபவர்கள் பரிவர்த்தனைக்கு முன் பட்டுக்கூடு ஓடு எடை சோதனைகளைச் செய்து கூட்டுப்புழு நிலையைச் சரிபார்க்க வேண்டும்."
    }
    
    price_disclaimer: Dict[str, str] = {
        "en": "Listed prices are farmer-provided and may change. MulberryCare does not guarantee the listed price or transaction.",
        "ta": "குறிப்பிடப்பட்ட விலைகள் விவசாயிகளால் வழங்கப்பட்டவை மற்றும் மாறக்கூடும். MulberryCare விலை அல்லது பரிவர்த்தனைக்கு உத்தரவாதம் அளிக்காது."
    }

    class Config:
        from_attributes = True
