from sqlalchemy.orm import Session, joinedload

from app.models.article import Article


class ArticleRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, data: dict) -> Article:
        article = Article(**data)
        self.db.add(article)
        self.db.commit()
        self.db.refresh(article)
        return article

    def get_by_id(self, id: int) -> Article | None:
        return self.db.query(Article).options(joinedload(Article.category)).filter(Article.id == id).first()

    def get_by_url(self, url: str) -> Article | None:
        return self.db.query(Article).filter(Article.url == url).first()

    def get_by_canonical_url(self, canonical_url: str) -> Article | None:
        return self.db.query(Article).filter(Article.canonical_url == canonical_url).first()

    def get_by_content_hash(self, content_hash: str) -> Article | None:
        return self.db.query(Article).filter(Article.content_hash == content_hash).first()

    def list_all(self, limit: int = 100, offset: int = 0) -> list[Article]:
        return self.db.query(Article).options(joinedload(Article.category)).order_by(Article.id.desc()).offset(offset).limit(limit).all()

    def list_by_source(self, source_id: int) -> list[Article]:
        return self.db.query(Article).filter(Article.source_id == source_id).order_by(Article.id.desc()).all()

    def list_by_category(self, category_id: int) -> list[Article]:
        return self.db.query(Article).filter(Article.category_id == category_id).order_by(Article.id.desc()).all()

    def list_by_ids(self, ids: list[int]) -> list[Article]:
        return self.db.query(Article).filter(Article.id.in_(ids)).all() if ids else []

    def update_status(self, article_id: int, status: str) -> None:
        article = self.get_by_id(article_id)
        if article:
            article.status = status
            self.db.commit()

    def delete(self, article_id: int) -> None:
        article = self.get_by_id(article_id)
        if article:
            self.db.delete(article)
            self.db.commit()
