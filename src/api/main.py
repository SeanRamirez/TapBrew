"""FastAPI application entry point."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.utils.config import get_settings

settings = get_settings()

app = FastAPI(
    title="TapFlow API",
    description="Real-time brewery analytics API",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "tapflow-api"}


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Welcome to TapFlow API",
        "docs": "/docs",
        "health": "/health",
    }
