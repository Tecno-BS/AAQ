from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.infraestructure.db.session import engine
from app.interfaces.api.routes import health, studies, charts, analyze, reports


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle manager para startup y shutdown."""
    # Startup
    yield
    # Shutdown
    await engine.dispose()


app = FastAPI(
    title="AAQ API",
    description="Agente de Análisis Cuantitativo - Sistema de Producción de Conocimiento",
    version="0.1.0",
    lifespan=lifespan,
)

# Registrar routers
app.include_router(health.router)
app.include_router(studies.router)
app.include_router(charts.router)
app.include_router(analyze.router)
app.include_router(reports.router)