from app.core.database import Base, SessionLocal, engine
from data.seeds import seed_categories_and_sources


def initialize_database_if_needed() -> None:
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed_categories_and_sources(db)
    finally:
        db.close()
