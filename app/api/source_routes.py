from fastapi import APIRouter, Depends, HTTPException

from app.api.dependencies import Services, get_services
from app.schemas.source_schema import SourceCreate, SourceResponse

router = APIRouter(prefix="/api/sources", tags=["sources"])


@router.get("", response_model=list[SourceResponse])
def list_sources(services: Services = Depends(get_services)):
    return services.sources.list_sources()


@router.get("/{source_id}", response_model=SourceResponse)
def get_source(source_id: int, services: Services = Depends(get_services)):
    source = services.sources.get_source(source_id)
    if source is None:
        raise HTTPException(status_code=404, detail="Source not found")
    return source


@router.post("", response_model=SourceResponse)
def create_source(payload: SourceCreate, services: Services = Depends(get_services)):
    return services.sources.create_source(payload.model_dump())


@router.put("/{source_id}", response_model=SourceResponse)
def update_source(source_id: int, payload: SourceCreate, services: Services = Depends(get_services)):
    return services.sources.update_source(source_id, payload.model_dump())


@router.delete("/{source_id}")
def delete_source(source_id: int, services: Services = Depends(get_services)):
    services.sources.delete_source(source_id)
    return {"status": "deleted"}
