from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class CrawlRun(Base):
    __tablename__ = "crawl_runs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    source_id: Mapped[int] = mapped_column(ForeignKey("sources.id"), nullable=False, index=True)
    started_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    finished_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    status: Mapped[str] = mapped_column(String, nullable=False, default="running", index=True)
    articles_found: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    articles_created: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    articles_updated: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    articles_skipped: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    articles_failed: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
