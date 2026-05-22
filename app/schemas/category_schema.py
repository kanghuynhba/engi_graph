from datetime import datetime

from pydantic import BaseModel, ConfigDict


class CategoryCreate(BaseModel):
    name: str
    slug: str
    description: str | None = None
    created_by: str = "manual"


class CategoryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    slug: str
    description: str | None
    created_by: str
    created_at: datetime
