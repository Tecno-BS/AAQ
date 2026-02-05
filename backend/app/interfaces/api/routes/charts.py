from uuid import UUID

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.dto.schemas import ChartItem, ChartsUploadResponse
from app.application.use_cases import upload_charts
from app.infraestructure.files.storage import save_chart_file
from app.infraestructure.repositories import ChartRepositoryImpl, StudyRepositoryImpl
from app.interfaces.api.deps import get_session

router = APIRouter(prefix="/studies", tags=["charts"])

ALLOWED_MIME_TYPES = {
    "image/png",
    "image/jpeg",
    "image/jpg",
    "image/webp",
    "application/pdf",
}


@router.post("/{study_id}/charts", response_model=ChartsUploadResponse, status_code=201)
async def upload_charts_endpoint(
    study_id: UUID,
    files: list[UploadFile] = File(...),
    session: AsyncSession = Depends(get_session),
):
    """Sube gráficas para un estudio."""
    
    # Validar que hay al menos un archivo
    if not files:
        raise HTTPException(status_code=400, detail="At least one file is required")
    
    # Validar tipos MIME
    for f in files:
        if f.content_type not in ALLOWED_MIME_TYPES:
            raise HTTPException(
                status_code=400,
                detail=f"File type '{f.content_type}' not allowed. Allowed: {ALLOWED_MIME_TYPES}"
            )
    
    # Guardar archivos y preparar datos
    files_data = []
    for f in files:
        storage_path = await save_chart_file(study_id, f)
        files_data.append({
            "filename": f.filename or "unknown",
            "storage_path": storage_path,
            "mime_type": f.content_type or "application/octet-stream",
        })
    
    # Crear registros en BD
    study_repo = StudyRepositoryImpl(session)
    chart_repo = ChartRepositoryImpl(session)
    
    try:
        charts = await upload_charts(study_repo, chart_repo, study_id, files_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    return ChartsUploadResponse(
        study_id=study_id,
        charts=[
            ChartItem(
                id=c.id,
                original_filename=c.original_filename,
                mime_type=c.mime_type,
                created_at=c.created_at,
            )
            for c in charts
        ],
    )