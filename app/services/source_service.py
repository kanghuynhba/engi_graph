import json


class SourceService:
    def __init__(self, repository):
        self.repository = repository

    def create_source(self, data: dict):
        data = data.copy()
        data["allowed_domains"] = json.dumps(data.get("allowed_domains", []))
        return self.repository.create(data)

    def list_sources(self):
        return self.repository.list_all()

    def get_source(self, source_id: int):
        return self.repository.get_by_id(source_id)

    def update_source(self, source_id: int, data: dict):
        data = data.copy()
        if "allowed_domains" in data and isinstance(data["allowed_domains"], list):
            data["allowed_domains"] = json.dumps(data["allowed_domains"])
        return self.repository.update(source_id, data)

    def delete_source(self, source_id: int) -> None:
        self.repository.delete(source_id)

    def enable_source(self, source_id: int):
        return self.repository.update(source_id, {"enabled": True})

    def disable_source(self, source_id: int):
        return self.repository.update(source_id, {"enabled": False})
