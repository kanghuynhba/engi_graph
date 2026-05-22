from datetime import datetime

from pydantic import BaseModel, ConfigDict, field_validator


class ArticleResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    source_id: int
    category_id: int | None
    category_name: str | None = None
    company: str
    title: str | None
    url: str
    author_name: str | None
    published_at: datetime | None
    status: str
    created_at: datetime

    @field_validator("category_name", mode="before")
    @classmethod
    def category_name_from_relation(cls, value):
        return value

    @classmethod
    def from_article(cls, article):
        data = article.__dict__.copy()
        data["category_name"] = article.category.name if getattr(article, "category", None) else None
        return cls(**data)


class ArticleDetailResponse(ArticleResponse):
    clean_text: str
    summary: str | None


class ArticleChunkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    article_id: int
    chunk_index: int
    heading: str | None
    text: str
    token_count: int
