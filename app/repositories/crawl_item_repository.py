from datetime import datetime

from sqlalchemy.orm import Session

from app.models.crawl_item import CrawlItem


class CrawlItemRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, data: dict) -> CrawlItem:
        item = CrawlItem(**data)
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    def get_by_id(self, id: int) -> CrawlItem | None:
        return self.db.get(CrawlItem, id)

    def list_by_crawl_run(self, crawl_run_id: int) -> list[CrawlItem]:
        return self.db.query(CrawlItem).filter(CrawlItem.crawl_run_id == crawl_run_id).order_by(CrawlItem.id).all()

    def mark_processing(self, id: int) -> None:
        item = self.get_by_id(id)
        if item:
            item.status = "processing"
            self.db.commit()

    def mark_processed(self, id: int, article_id: int | None) -> None:
        item = self.get_by_id(id)
        if item:
            item.status = "processed"
            item.article_id = article_id
            self.db.commit()

    def mark_skipped_duplicate(self, id: int, article_id: int | None) -> None:
        item = self.get_by_id(id)
        if item:
            item.status = "skipped_duplicate"
            item.article_id = article_id
            self.db.commit()

    def mark_failed(self, id: int, error_message: str) -> None:
        item = self.get_by_id(id)
        if item:
            item.status = "failed"
            item.error_message = error_message
            item.last_error_at = datetime.utcnow()
            self.db.commit()

    def increment_retry(self, id: int, error_message: str) -> None:
        item = self.get_by_id(id)
        if item:
            item.retry_count += 1
            item.status = "retry_pending"
            item.error_message = error_message
            item.last_error_at = datetime.utcnow()
            self.db.commit()

    def list_retryable(self, crawl_run_id: int) -> list[CrawlItem]:
        return (
            self.db.query(CrawlItem)
            .filter(CrawlItem.crawl_run_id == crawl_run_id)
            .filter(CrawlItem.status.in_(["failed", "retry_pending"]))
            .filter(CrawlItem.retry_count < CrawlItem.max_retries)
            .order_by(CrawlItem.id)
            .all()
        )
