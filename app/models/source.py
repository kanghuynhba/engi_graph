from datetime import datetime


from sqlalchemy import Boolean, DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Source(Base):
    __tablename__ = "sources"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    company: Mapped[str] = mapped_column(String, nullable=False, index=True)
    base_url: Mapped[str] = mapped_column(String, nullable=False)
    feed_url: Mapped[str | None] = mapped_column(String, nullable=True)
    sitemap_url: Mapped[str | None] = mapped_column(String, nullable=True)
    allowed_domains: Mapped[str] = mapped_column(String, nullable=False)
    crawl_mode: Mapped[str] = mapped_column(String, nullable=False)
    enabled: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    articles = relationship("Article", back_populates="source")
