from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import health, auth
from app.database.db import Base, engine
from app.models import user  # noqa: F401 - ensures model is registered before create_all

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


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)


app.include_router(health.router)
app.include_router(auth.router)