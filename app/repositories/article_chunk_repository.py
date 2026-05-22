from sqlalchemy.orm import Session

from app.models.article_chunk import ArticleChunk


class ArticleChunkRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, data: dict) -> ArticleChunk:
        chunk = ArticleChunk(**data)
        self.db.add(chunk)
        self.db.commit()
        self.db.refresh(chunk)
        return chunk

    def bulk_create(self, chunks: list[dict]) -> list[ArticleChunk]:
        objects = [ArticleChunk(**chunk) for chunk in chunks]
        self.db.add_all(objects)
        self.db.commit()
        for obj in objects:
            self.db.refresh(obj)
        return objects

    def get_by_id(self, id: int) -> ArticleChunk | None:
        return self.db.get(ArticleChunk, id)

    def list_by_article(self, article_id: int) -> list[ArticleChunk]:
        return self.db.query(ArticleChunk).filter(ArticleChunk.article_id == article_id).order_by(ArticleChunk.chunk_index).all()

    def list_by_ids(self, ids: list[int]) -> list[ArticleChunk]:
        return self.db.query(ArticleChunk).filter(ArticleChunk.id.in_(ids)).all() if ids else []

    def update_vector_id(self, chunk_id: int, vector_id: str) -> None:
        chunk = self.get_by_id(chunk_id)
        if chunk:
            chunk.vector_id = vector_id
            self.db.commit()

    def delete_by_article(self, article_id: int) -> None:
        self.db.query(ArticleChunk).filter(ArticleChunk.article_id == article_id).delete()
        self.db.commit()
