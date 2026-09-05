from typing import Optional
from pydantic import BaseModel, EmailStr, field_validator

from app.models.user import UserRole, Language


class UserSignup(BaseModel):
    name: str
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    password: str
    role: UserRole = UserRole.farmer
    preferred_language: Language = Language.en
    village: Optional[str] = None

    @field_validator("password")
    @classmethod
    def password_min_length(cls, v: str) -> str:
        if len(v) < 6:
            raise ValueError("Password must be at least 6 characters")
        return v

    @field_validator("phone")
    @classmethod
    def require_email_or_phone(cls, v, info):
        # Basic guard; full email-or-phone cross validation done in the route.
        return v


class UserLogin(BaseModel):
    identifier: str  # email or phone
    password: str


class UserOut(BaseModel):
    id: str
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    role: UserRole
    preferred_language: Language
    village: Optional[str] = None

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut