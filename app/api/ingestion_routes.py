from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app.api.dependencies import Services, get_services
from app.core.database import get_db
from app.schemas.ingestion_schema import (
    CrawlRunResponse,
    CrawlSourceResponse,
    IngestUrlRequest,
    IngestUrlResponse,
)
from app.services.factory import build_ingestion_service
from app.services.ingestion_jobs import run_crawl_background
from app.services.ingestion_service import IngestionService

router = APIRouter(prefix="/api/ingestion", tags=["ingestion"])


def get_service(request: Request, db: Session = Depends(get_db)) -> IngestionService:
    return build_ingestion_service(db, request.app.state.http_client)


@router.post("/sources/{source_id}/crawl", response_model=CrawlSourceResponse)
def crawl_source(
    source_id: int,
    background_tasks: BackgroundTasks,
    request: Request,
    service: IngestionService = Depends(get_service),
):
    try:
        source, run = service.create_crawl_run(source_id)
    except ValueError:
        raise HTTPException(status_code=404, detail="Source not found")
    background_tasks.add_task(
        run_crawl_background, run.id, source.id, request.app
    )
    return CrawlSourceResponse(
        crawl_run_id=run.id,
        source_id=source_id,
        status="running",
        message="Crawl started",
    )


@router.post("/articles/ingest-url", response_model=IngestUrlResponse)
async def ingest_url(
    payload: IngestUrlRequest, service: IngestionService = Depends(get_service)
):
    result = await service.ingest_url(payload.source_id, payload.url)
    return IngestUrlResponse(**result.__dict__)


@router.post("/articles/{article_id}/reindex")
def reindex_article(article_id: int):
    return {"status": "not_implemented", "article_id": article_id}


@router.get("/crawl-runs", response_model=list[CrawlRunResponse])
def list_crawl_runs(db: Session = Depends(get_db)):
    return CrawlRunRepository(db).list_all()


@router.get("/crawl-runs/{crawl_run_id}", response_model=CrawlRunResponse)
def get_crawl_run(crawl_run_id: int, db: Session = Depends(get_db)):
    run = CrawlRunRepository(db).get_by_id(crawl_run_id)
    if run is None:
        raise HTTPException(status_code=404, detail="Crawl run not found")
    return run
