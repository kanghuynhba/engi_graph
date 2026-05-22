from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class RAGResult(Base):
    __tablename__ = "rag_results"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    rag_query_id: Mapped[int] = mapped_column(ForeignKey("rag_queries.id"), nullable=False, index=True)
    article_id: Mapped[int] = mapped_column(ForeignKey("articles.id"), nullable=False, index=True)
    chunk_id: Mapped[int] = mapped_column(ForeignKey("article_chunks.id"), nullable=False, index=True)
    score: Mapped[float] = mapped_column(Float, nullable=False)
    rank: Mapped[int] = mapped_column(Integer, nullable=False)
    result_type: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
