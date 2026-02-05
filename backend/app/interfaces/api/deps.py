from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from app.infraestructure.db.session import async_session_factory


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency que provee una sesión de base de datos.
    Hace commit si no hay excepción, rollback si la hay.
    """
    async with async_session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise