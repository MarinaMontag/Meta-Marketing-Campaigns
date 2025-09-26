from contextlib import contextmanager
from functools import lru_cache

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from settings import settings


@lru_cache()
def get_engine():
    return create_engine(
        settings.DATABASE_URL,
        pool_pre_ping=True,
        future=True
    )

SessionLocal = sessionmaker(bind=get_engine(), autoflush=False, autocommit=False)

@contextmanager
def session_scope():
    session = SessionLocal()

    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
