from datetime import datetime

from sqlalchemy import DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class RAGQuery(Base):
    __tablename__ = "rag_queries"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    original_query: Mapped[str] = mapped_column(Text, nullable=False)
    rewritten_query: Mapped[str | None] = mapped_column(Text, nullable=True)
    intent: Mapped[str | None] = mapped_column(String, nullable=True)
    return_type: Mapped[str | None] = mapped_column(String, nullable=True)
    filters_json: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
