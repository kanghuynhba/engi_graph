from app.core.database import SessionLocal
from app.services.factory import build_ingestion_service


async def run_crawl_background(crawl_run_id: int, source_id: int, app) -> None:
    db = SessionLocal()
    try:
        service = build_ingestion_service(db, app.state.http_client)
        await service.process_crawl_run_by_id(source_id, crawl_run_id)
    finally:
        db.close()
