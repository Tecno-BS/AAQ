from fastapi import APIRouter

from app.core.constants import STUDY_TYPES

router = APIRouter(prefix="/study-types", tags=["study-types"])

@router.get("")
async def list_study_types():
    #Devuelve la lista oficial de tipos de estudio (BS)

    return {"study_types" : list(STUDY_TYPES)}

