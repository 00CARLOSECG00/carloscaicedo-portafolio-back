"""Vercel serverless entry point for FastAPI."""

from app.main import app
from mangum import Mangum

handler = Mangum(app, lifespan="off")
