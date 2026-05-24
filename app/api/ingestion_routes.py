from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Request

from app.api.dependencies import Services, get_services
from app.schemas.ingestion_schema import (
    CrawlRunResponse,
    CrawlSourceResponse,
    IngestUrlRequest,
    IngestUrlResponse,
)
from app.services.ingestion_jobs import run_crawl_background

router = APIRouter(prefix="/api/ingestion", tags=["ingestion"])


@router.post("/sources/{source_id}/crawl", response_model=CrawlSourceResponse)
def crawl_source(
    source_id: int,
    background_tasks: BackgroundTasks,
    request: Request,
    services: Services = Depends(get_services),
):
    try:
        source, run = services.ingestion.create_crawl_run(source_id)
    except ValueError:
        raise HTTPException(status_code=404, detail="Source not found")
    background_tasks.add_task(run_crawl_background, run.id, source.id, request.app)
    return CrawlSourceResponse(
        crawl_run_id=run.id,
        source_id=source_id,
        status="running",
        message="Crawl started",
    )


@router.post("/articles/ingest-url", response_model=IngestUrlResponse)
async def ingest_url(
    payload: IngestUrlRequest, services: Services = Depends(get_services)
):
    result = await services.ingestion.ingest_url(payload.source_id, payload.url)
    return IngestUrlResponse(**result.__dict__)


@router.post("/articles/{article_id}/reindex")
def reindex_article(article_id: int):
    return {"status": "not_implemented", "article_id": article_id}


@router.get("/crawl-runs", response_model=list[CrawlRunResponse])
def list_crawl_runs(services: Services = Depends(get_services)):
    return services.ingestion.crawl_run_repository.list_all()


@router.get("/crawl-runs/{crawl_run_id}", response_model=CrawlRunResponse)
def get_crawl_run(crawl_run_id: int, services: Services = Depends(get_services)):
    run = services.ingestion.crawl_run_repository.get_by_id(crawl_run_id)
    if run is None:
        raise HTTPException(status_code=404, detail="Crawl run not found")
    return run
