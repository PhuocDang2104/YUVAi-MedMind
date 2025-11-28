from sqlalchemy import create_engine

from app.core.config import settings
from app.db.base import Base  # noqa: F401 - imports models for metadata


def init_db() -> None:
    engine = create_engine(settings.database_url, pool_pre_ping=True)
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    init_db()
