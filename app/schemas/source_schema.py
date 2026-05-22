import json
from datetime import datetime

from pydantic import BaseModel, ConfigDict, field_validator


class SourceCreate(BaseModel):
    name: str
    company: str
    base_url: str
    feed_url: str | None = None
    sitemap_url: str | None = None
    allowed_domains: list[str] = []
    crawl_mode: str = "feed"
    enabled: bool = True


class SourceResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    company: str
    base_url: str
    feed_url: str | None
    crawl_mode: str
    allowed_domains: list[str]
    enabled: bool
    created_at: datetime

    @field_validator("allowed_domains", mode="before")
    @classmethod
    def parse_allowed_domains(cls, value):
        if isinstance(value, str):
            return json.loads(value)
        return value
