from datetime import datetime

from pydantic import BaseModel, ConfigDict


class CrawlSourceResponse(BaseModel):
    crawl_run_id: int
    source_id: int
    status: str
    message: str


class IngestUrlRequest(BaseModel):
    source_id: int
    url: str


class IngestUrlResponse(BaseModel):
    status: str
    article_id: int | None
    url: str
    error_message: str | None = None


class CrawlRunResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    source_id: int
    started_at: datetime
    finished_at: datetime | None
    status: str
    articles_found: int
    articles_created: int
    articles_updated: int
    articles_skipped: int
    articles_failed: int
    error_message: str | None
