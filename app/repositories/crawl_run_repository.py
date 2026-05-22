from datetime import datetime

from sqlalchemy.orm import Session

from app.models.crawl_run import CrawlRun


class CrawlRunRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, source_id: int) -> CrawlRun:
        run = CrawlRun(source_id=source_id, status="running")
        self.db.add(run)
        self.db.commit()
        self.db.refresh(run)
        return run

    def get_by_id(self, id: int) -> CrawlRun | None:
        return self.db.get(CrawlRun, id)

    def list_all(self) -> list[CrawlRun]:
        return self.db.query(CrawlRun).order_by(CrawlRun.id.desc()).all()

    def list_by_source(self, source_id: int) -> list[CrawlRun]:
        return self.db.query(CrawlRun).filter(CrawlRun.source_id == source_id).order_by(CrawlRun.id.desc()).all()

    def mark_success(self, id: int, stats: dict | None = None) -> None:
        run = self.get_by_id(id)
        if run:
            for key, value in (stats or {}).items():
                setattr(run, key, value)
            run.status = "success"
            run.finished_at = datetime.utcnow()
            self.db.commit()

    def mark_partial_success(self, id: int, stats: dict | None = None) -> None:
        run = self.get_by_id(id)
        if run:
            for key, value in (stats or {}).items():
                setattr(run, key, value)
            run.status = "partial_success"
            run.finished_at = datetime.utcnow()
            self.db.commit()

    def mark_failed(self, id: int, error_message: str) -> None:
        run = self.get_by_id(id)
        if run:
            run.status = "failed"
            run.error_message = error_message
            run.finished_at = datetime.utcnow()
            self.db.commit()

    def increment_stat(self, id: int, field: str, amount: int = 1) -> None:
        run = self.get_by_id(id)
        if run is None or not hasattr(run, field):
            return
        setattr(run, field, getattr(run, field) + amount)
        self.db.commit()

    def update_articles_found(self, id: int, count: int) -> None:
        run = self.get_by_id(id)
        if run:
            run.articles_found = count
            self.db.commit()
