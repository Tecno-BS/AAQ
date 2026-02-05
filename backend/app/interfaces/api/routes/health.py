from fastapi import APIRouter
from sqlalchemy import text

from app.infraestructure.db.session import engine

router = APIRouter(tags=["health"])


@router.get("/health")
async def health():
    """Health check básico."""
    return {"status": "ok"}


@router.get("/health/db")
async def health_db():
    """Health check con verificación de base de datos."""
    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        return {"status": "ok", "db": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "db": "error", "detail": str(e)}