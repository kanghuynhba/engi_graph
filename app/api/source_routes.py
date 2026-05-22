from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.repositories.source_repository import SourceRepository
from app.schemas.source_schema import SourceCreate, SourceResponse
from app.services.source_service import SourceService

router = APIRouter(prefix="/api/sources", tags=["sources"])


def get_service(db: Session = Depends(get_db)) -> SourceService:
    return SourceService(SourceRepository(db))


@router.get("", response_model=list[SourceResponse])
def list_sources(service: SourceService = Depends(get_service)):
    return service.list_sources()


@router.get("/{source_id}", response_model=SourceResponse)
def get_source(source_id: int, service: SourceService = Depends(get_service)):
    source = service.get_source(source_id)
    if source is None:
        raise HTTPException(status_code=404, detail="Source not found")
    return source


@router.post("", response_model=SourceResponse)
def create_source(payload: SourceCreate, service: SourceService = Depends(get_service)):
    return service.create_source(payload.model_dump())


@router.put("/{source_id}", response_model=SourceResponse)
def update_source(source_id: int, payload: SourceCreate, service: SourceService = Depends(get_service)):
    return service.update_source(source_id, payload.model_dump())


@router.delete("/{source_id}")
def delete_source(source_id: int, service: SourceService = Depends(get_service)):
    service.delete_source(source_id)
    return {"status": "deleted"}
