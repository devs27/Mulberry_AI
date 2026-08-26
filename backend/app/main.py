"""
MulberryCare AI - Backend entrypoint (Phase 1: architecture & health check).
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import health

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

app.include_router(health.router)
