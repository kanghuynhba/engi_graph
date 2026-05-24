from fastapi import APIRouter, Depends, HTTPException

from app.api.dependencies import Services, get_services
from app.schemas.category_schema import CategoryCreate, CategoryResponse

router = APIRouter(prefix="/api/categories", tags=["categories"])


@router.get("", response_model=list[CategoryResponse])
def list_categories(services: Services = Depends(get_services)):
    return services.categories.list_categories()


@router.post("/seed-defaults")
def seed_defaults(services: Services = Depends(get_services)):
    services.categories.seed_defaults()
    return {"status": "seeded"}


@router.get("/{category_id}", response_model=CategoryResponse)
def get_category(category_id: int, services: Services = Depends(get_services)):
    category = services.categories.get_category(category_id)
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@router.post("", response_model=CategoryResponse)
def create_category(payload: CategoryCreate, services: Services = Depends(get_services)):
    return services.categories.create_category(payload.model_dump())


@router.put("/{category_id}", response_model=CategoryResponse)
def update_category(category_id: int, payload: CategoryCreate, services: Services = Depends(get_services)):
    return services.categories.update_category(category_id, payload.model_dump())


@router.delete("/{category_id}")
def delete_category(category_id: int, services: Services = Depends(get_services)):
    services.categories.delete_category(category_id)
    return {"status": "deleted"}
