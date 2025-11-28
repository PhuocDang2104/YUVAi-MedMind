from sqlalchemy.orm import declarative_base

Base = declarative_base()

# Import models so Alembic can auto-detect metadata (keep at end to avoid circular imports).
from app import models  # noqa: E402,F401
