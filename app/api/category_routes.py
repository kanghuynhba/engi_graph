from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.repositories.category_repository import CategoryRepository
from app.schemas.category_schema import CategoryCreate, CategoryResponse
from app.services.category_service import CategoryService

router = APIRouter(prefix="/api/categories", tags=["categories"])


def get_service(db: Session = Depends(get_db)) -> CategoryService:
    return CategoryService(CategoryRepository(db))


@router.get("", response_model=list[CategoryResponse])
def list_categories(service: CategoryService = Depends(get_service)):
    return service.list_categories()


@router.post("/seed-defaults")
def seed_defaults(service: CategoryService = Depends(get_service)):
    service.seed_defaults()
    return {"status": "seeded"}


@router.get("/{category_id}", response_model=CategoryResponse)
def get_category(category_id: int, service: CategoryService = Depends(get_service)):
    category = service.get_category(category_id)
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@router.post("", response_model=CategoryResponse)
def create_category(payload: CategoryCreate, service: CategoryService = Depends(get_service)):
    return service.create_category(payload.model_dump())


@router.put("/{category_id}", response_model=CategoryResponse)
def update_category(category_id: int, payload: CategoryCreate, service: CategoryService = Depends(get_service)):
    return service.update_category(category_id, payload.model_dump())


@router.delete("/{category_id}")
def delete_category(category_id: int, service: CategoryService = Depends(get_service)):
    service.delete_category(category_id)
    return {"status": "deleted"}

