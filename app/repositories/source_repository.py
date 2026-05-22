from sqlalchemy.orm import Session

from app.models.source import Source


class SourceRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, data: dict) -> Source:
        source = Source(**data)
        self.db.add(source)
        self.db.commit()
        self.db.refresh(source)
        return source

    def get_by_id(self, id: int) -> Source | None:
        return self.db.get(Source, id)

    def list_all(self) -> list[Source]:
        return self.db.query(Source).order_by(Source.id).all()

    def list_enabled(self) -> list[Source]:
        return self.db.query(Source).filter(Source.enabled.is_(True)).order_by(Source.id).all()

    def update(self, id: int, data: dict) -> Source:
        source = self.get_by_id(id)
        if source is None:
            raise ValueError("Source not found")
        for key, value in data.items():
            setattr(source, key, value)
        self.db.commit()
        self.db.refresh(source)
        return source

    def delete(self, id: int) -> None:
        source = self.get_by_id(id)
        if source:
            self.db.delete(source)
            self.db.commit()
