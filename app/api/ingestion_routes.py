from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app.core.database import SessionLocal, get_db
from app.ingestion.crawler import Crawler
from app.repositories.crawl_run_repository import CrawlRunRepository
from app.repositories.source_repository import SourceRepository
from app.schemas.ingestion_schema import CrawlRunResponse, CrawlSourceResponse, IngestUrlRequest, IngestUrlResponse
from app.services.factory import build_indexing_pipeline, build_orchestrator
from app.services.ingestion_service import IngestionService

router = APIRouter(prefix="/api/ingestion", tags=["ingestion"])


def get_service(request: Request, db: Session = Depends(get_db)) -> IngestionService:
    client = request.app.state.http_client
    return IngestionService(SourceRepository(db), CrawlRunRepository(db), Crawler(client), build_orchestrator(db, client), build_indexing_pipeline(db, client))


@router.post("/sources/{source_id}/crawl", response_model=CrawlSourceResponse)
def crawl_source(source_id: int, background_tasks: BackgroundTasks, request: Request, db: Session = Depends(get_db)):
    source = SourceRepository(db).get_by_id(source_id)
    if source is None:
        raise HTTPException(status_code=404, detail="Source not found")
    run = CrawlRunRepository(db).create(source_id)
    background_tasks.add_task(run_crawl_background_existing, run.id, source_id, request.app)
    return CrawlSourceResponse(crawl_run_id=run.id, source_id=source_id, status="running", message="Crawl started")


async def run_crawl_background_existing(crawl_run_id: int, source_id: int, app) -> None:
    db = SessionLocal()
    try:
        client = app.state.http_client
        run_repo = CrawlRunRepository(db)
        service = IngestionService(SourceRepository(db), run_repo, Crawler(client), build_orchestrator(db, client), build_indexing_pipeline(db, client))
        await service.process_crawl_run(service.source_repository.get_by_id(source_id), run_repo.get_by_id(crawl_run_id))
    finally:
        db.close()


@router.post("/articles/ingest-url", response_model=IngestUrlResponse)
async def ingest_url(payload: IngestUrlRequest, service: IngestionService = Depends(get_service)):
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
