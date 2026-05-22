from sqlalchemy.orm import Session

from app.models.rag_query import RAGQuery


class RAGQueryRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, data: dict) -> RAGQuery:
        query = RAGQuery(**data)
        self.db.add(query)
        self.db.commit()
        self.db.refresh(query)
        return query

    def get_by_id(self, id: int) -> RAGQuery | None:
        return self.db.get(RAGQuery, id)

    def list_recent(self, limit: int = 20) -> list[RAGQuery]:
        return self.db.query(RAGQuery).order_by(RAGQuery.id.desc()).limit(limit).all()
