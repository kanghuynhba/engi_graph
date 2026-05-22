from sqlalchemy.orm import Session

from app.models.rag_result import RAGResult


class RAGResultRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, data: dict) -> RAGResult:
        result = RAGResult(**data)
        self.db.add(result)
        self.db.commit()
        self.db.refresh(result)
        return result

    def bulk_create(self, results: list[dict]) -> list[RAGResult]:
        objects = [RAGResult(**result) for result in results]
        self.db.add_all(objects)
        self.db.commit()
        for obj in objects:
            self.db.refresh(obj)
        return objects

    def list_by_query(self, rag_query_id: int) -> list[RAGResult]:
        return self.db.query(RAGResult).filter(RAGResult.rag_query_id == rag_query_id).order_by(RAGResult.rank).all()
