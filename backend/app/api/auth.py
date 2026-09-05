from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.database.db import get_db
from app.models.user import User
from app.schemas.user import UserSignup, UserLogin, UserOut, Token
from app.services.auth_service import hash_password, verify_password, create_access_token
from app.api.deps import get_current_user

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/signup", response_model=Token, status_code=status.HTTP_201_CREATED)
def signup(payload: UserSignup, db: Session = Depends(get_db)):
    if not payload.email and not payload.phone:
        raise HTTPException(status_code=400, detail="Provide an email or phone number")

    existing = None
    if payload.email:
        existing = db.query(User).filter(User.email == payload.email).first()
    if not existing and payload.phone:
        existing = db.query(User).filter(User.phone == payload.phone).first()
    if existing:
        raise HTTPException(status_code=409, detail="Account already exists")

    user = User(
        name=payload.name,
        email=payload.email,
        phone=payload.phone,
        password_hash=hash_password(payload.password),
        role=payload.role,
        preferred_language=payload.preferred_language,
        village=payload.village,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    # Seed 2 mock diagnoses for demonstration / testing purposes
    from datetime import datetime, timedelta
    from app.models.diagnosis import Diagnosis
    
    diag1 = Diagnosis(
        user_id=user.id,
        disease="Leaf Rust",
        confidence=0.91,
        variety="S36",
        timestamp=datetime.utcnow(),
        severity="moderate",
        is_uncertain=False,
        image_path="/images/demo_leaf_rust.jpg"
    )
    diag2 = Diagnosis(
        user_id=user.id,
        disease="Healthy",
        confidence=0.96,
        variety="M5",
        timestamp=datetime.utcnow() - timedelta(days=3),
        severity=None,
        is_uncertain=False,
        image_path="/images/demo_healthy.jpg"
    )
    db.add(diag1)
    db.add(diag2)
    db.commit()

    token = create_access_token(subject=str(user.id), extra_claims={"role": user.role.value})
    return Token(access_token=token, user=UserOut.model_validate(user))


@router.post("/login", response_model=Token)
def login(payload: UserLogin, db: Session = Depends(get_db)):
    user = (
        db.query(User)
        .filter(or_(User.email == payload.identifier, User.phone == payload.identifier))
        .first()
    )
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(subject=str(user.id), extra_claims={"role": user.role.value})
    return Token(access_token=token, user=UserOut.model_validate(user))


@router.get("/me", response_model=UserOut)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user