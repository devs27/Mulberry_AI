from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

from app.api import health, auth, diagnose
from app.database.db import Base, engine
from app.models import user, diagnosis, disease_info, listing  # noqa: F401 - ensures models are registered before create_all

app = FastAPI(
    title="MulberryCare AI",
    description="AI-Powered Mulberry Health & Sericulture Support Platform",
    version="0.1.0",
)

# Open CORS for local prototype development. Restrict this before production.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Resolve absolute path to backend/static directory relative to main.py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(os.path.dirname(BASE_DIR), "static")
os.makedirs(os.path.join(STATIC_DIR, "uploads"), exist_ok=True)


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)
    
    from app.database.db import SessionLocal
    from app.models.disease_info import DiseaseInformation
    from app.database.seed_diseases import seed_disease_info
    db = SessionLocal()
    try:
        if db.query(DiseaseInformation).count() == 0:
            seed_disease_info(db)
    except Exception as e:
        print(f"Error seeding disease information: {e}")
    finally:
        db.close()


from app.api import health, auth, diagnose, weather, chat, listings
# ...
app.include_router(health.router)
app.include_router(auth.router)
app.include_router(diagnose.router)
app.include_router(weather.router)
app.include_router(chat.router)
app.include_router(listings.router)

from fastapi.responses import FileResponse
from fastapi import Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.models.user import User
from app.models.diagnosis import Diagnosis
from app.services.auth_service import decode_access_token

def get_current_user_for_image(request: Request, db: Session = Depends(get_db)) -> User:
    token = None
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.split(" ")[1]
    if not token:
        token = request.query_params.get("token")
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    payload = decode_access_token(token)
    if payload is None or "sub" not in payload:
        raise HTTPException(status_code=401, detail="Could not validate credentials")
    # User.id is a UUID string — query directly with str sub
    user_id = str(payload["sub"])
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=401, detail="Could not validate credentials")
    return user

@app.get("/static/uploads/{filename}")
def get_secure_upload(filename: str, current_user: User = Depends(get_current_user_for_image), db: Session = Depends(get_db)):
    # Verify that the filename belongs to a diagnosis created by the current user
    diag = db.query(Diagnosis).filter(
        Diagnosis.image_path.like(f"%/uploads/{filename}"),
        Diagnosis.user_id == current_user.id
    ).first()
    if not diag:
        raise HTTPException(status_code=403, detail="Access denied to this resource")
    file_path = os.path.join(STATIC_DIR, "uploads", filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(file_path)

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")