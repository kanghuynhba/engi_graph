from sqlalchemy.orm import Session

from app.models.category import Category


DEFAULT_CATEGORIES = [
    {"name": "Uncategorized", "slug": "uncategorized", "description": "Fallback when classification is uncertain.", "created_by": "system"},
    {"name": "Distributed Systems", "slug": "distributed-systems", "description": "Architecture and techniques for systems across multiple machines or services.", "created_by": "system"},
    {"name": "Infrastructure", "slug": "infrastructure", "description": "Platform, compute, networking, and operational infrastructure.", "created_by": "system"},
    {"name": "Databases", "slug": "databases", "description": "Storage engines, query systems, and data consistency.", "created_by": "system"},
    {"name": "Data Engineering", "slug": "data-engineering", "description": "Pipelines, streaming, batch processing, and data platforms.", "created_by": "system"},
    {"name": "Machine Learning / AI", "slug": "machine-learning-ai", "description": "ML systems, model training, inference, and AI product engineering.", "created_by": "system"},
    {"name": "Observability", "slug": "observability", "description": "Monitoring, tracing, logging, and metrics.", "created_by": "system"},
    {"name": "Reliability / Resilience", "slug": "reliability-resilience", "description": "Fault tolerance, disaster recovery, SRE practices, and chaos engineering.", "created_by": "system"},
    {"name": "Performance Optimization", "slug": "performance-optimization", "description": "Latency reduction, throughput, caching, and efficiency improvements.", "created_by": "system"},
    {"name": "Security", "slug": "security", "description": "Application security, access control, cryptography, and threat modeling.", "created_by": "system"},
    {"name": "Developer Tools", "slug": "developer-tools", "description": "CI/CD, build systems, developer experience, and internal tooling.", "created_by": "system"},
    {"name": "Cloud / Platform Engineering", "slug": "cloud-platform-engineering", "description": "Cloud services, Kubernetes, multi-cloud, and platform abstractions.", "created_by": "system"},
    {"name": "Mobile Engineering", "slug": "mobile-engineering", "description": "iOS, Android, cross-platform mobile development.", "created_by": "system"},
    {"name": "Frontend / Web Engineering", "slug": "frontend-web-engineering", "description": "Web performance, UI frameworks, browser APIs, and frontend architecture.", "created_by": "system"},
    {"name": "Content Delivery / CDN", "slug": "content-delivery-cdn", "description": "CDN design, video delivery, caching infrastructure, and edge computing.", "created_by": "system"},
    {"name": "Messaging / Real-time Systems", "slug": "messaging-realtime-systems", "description": "Message queues, event streaming, WebSockets, and real-time communication.", "created_by": "system"},
]


class CategoryRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, data: dict) -> Category:
        category = Category(**data)
        self.db.add(category)
        self.db.commit()
        self.db.refresh(category)
        return category

    def get_by_id(self, id: int) -> Category | None:
        return self.db.get(Category, id)

    def get_by_slug(self, slug: str) -> Category | None:
        return self.db.query(Category).filter(Category.slug == slug).first()

    def get_by_name(self, name: str) -> Category | None:
        return self.db.query(Category).filter(Category.name == name).first()

    def list_all(self) -> list[Category]:
        return self.db.query(Category).order_by(Category.name).all()

    def update(self, id: int, data: dict) -> Category:
        category = self.get_by_id(id)
        if category is None:
            raise ValueError("Category not found")
        for key, value in data.items():
            setattr(category, key, value)
        self.db.commit()
        self.db.refresh(category)
        return category

    def delete(self, id: int) -> None:
        category = self.get_by_id(id)
        if category:
            self.db.delete(category)
            self.db.commit()

    def seed_defaults(self) -> None:
        if self.db.query(Category).count() > 0:
            return
        self.db.add_all(Category(**category) for category in DEFAULT_CATEGORIES)
        self.db.commit()
