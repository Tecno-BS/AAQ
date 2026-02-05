from pathlib import Path
from uuid import UUID, uuid4

from fastapi import UploadFile

from app.config import settings


def ensure_storage_dir(study_id: UUID) -> Path:
    """Crea el directorio de almacenamiento si no existe."""
    base = Path(settings.FILES_STORAGE_PATH)
    study_dir = base / str(study_id) / "charts"
    study_dir.mkdir(parents=True, exist_ok=True)
    return study_dir


async def save_chart_file(study_id: UUID, file: UploadFile) -> str:
    """
    Guarda un archivo de gráfica en el filesystem.
    
    Args:
        study_id: ID del estudio
        file: Archivo subido
    
    Returns:
        Path relativo al archivo guardado (relativo a FILES_STORAGE_PATH)
    """
    dir_path = ensure_storage_dir(study_id)
    
    # Obtener extensión del archivo original
    original_name = file.filename or "file.bin"
    ext = Path(original_name).suffix or ".bin"
    
    # Generar nombre único
    filename = f"{uuid4()}{ext}"
    file_path = dir_path / filename
    
    # Leer y guardar contenido
    content = await file.read()
    file_path.write_bytes(content)
    
    # Retornar path relativo
    base = Path(settings.FILES_STORAGE_PATH)
    return str(file_path.relative_to(base))


def get_file_path(relative_path: str) -> Path:
    """Obtiene el path absoluto de un archivo dado su path relativo."""
    base = Path(settings.FILES_STORAGE_PATH)
    return base / relative_path