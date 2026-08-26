from fastapi import APIRouter

router = APIRouter(tags=["health"])


@router.get("/")
def root():
    return {"app": "MulberryCare AI", "status": "ok"}


@router.get("/api/health")
def health_check():
    return {"status": "ok", "service": "backend"}
