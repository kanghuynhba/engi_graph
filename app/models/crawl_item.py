from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class CrawlItem(Base):
    __tablename__ = "crawl_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    crawl_run_id: Mapped[int] = mapped_column(ForeignKey("crawl_runs.id"), nullable=False, index=True)
    source_id: Mapped[int] = mapped_column(ForeignKey("sources.id"), nullable=False, index=True)
    url: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[str] = mapped_column(String, nullable=False, default="discovered", index=True)
    article_id: Mapped[int | None] = mapped_column(ForeignKey("articles.id"), nullable=True, index=True)
    retry_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    max_retries: Mapped[int] = mapped_column(Integer, default=3, nullable=False)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    last_error_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
