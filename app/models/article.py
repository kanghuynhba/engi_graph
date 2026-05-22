from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Article(Base):
    __tablename__ = "articles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    source_id: Mapped[int] = mapped_column(ForeignKey("sources.id"), nullable=False, index=True)
    category_id: Mapped[int | None] = mapped_column(ForeignKey("categories.id"), nullable=True, index=True)
    company: Mapped[str] = mapped_column(String, nullable=False, index=True)
    title: Mapped[str | None] = mapped_column(String, nullable=True)
    url: Mapped[str] = mapped_column(String, nullable=False, index=True)
    canonical_url: Mapped[str] = mapped_column(String, nullable=False, index=True)
    author_name: Mapped[str | None] = mapped_column(String, nullable=True)
    published_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    updated_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    raw_html: Mapped[str | None] = mapped_column(Text, nullable=True)
    clean_text: Mapped[str] = mapped_column(Text, nullable=False)
    summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    content_hash: Mapped[str] = mapped_column(String, unique=True, nullable=False, index=True)
    status: Mapped[str] = mapped_column(String, nullable=False, default="pending", index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    source = relationship("Source", back_populates="articles")
    category = relationship("Category", back_populates="articles")
    chunks = relationship("ArticleChunk", back_populates="article", cascade="all, delete-orphan")
