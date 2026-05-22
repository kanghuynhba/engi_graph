class CategoryService:
    def __init__(self, repository):
        self.repository = repository

    def create_category(self, data: dict):
        return self.repository.create(data)

    def list_categories(self):
        return self.repository.list_all()

    def get_category(self, category_id: int):
        return self.repository.get_by_id(category_id)

    def update_category(self, category_id: int, data: dict):
        return self.repository.update(category_id, data)

    def delete_category(self, category_id: int) -> None:
        self.repository.delete(category_id)

    def seed_defaults(self) -> None:
        self.repository.seed_defaults()
