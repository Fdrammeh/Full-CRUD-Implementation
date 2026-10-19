from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, DeclarativeBase
from typing import Generator

DATABASE_URL ="sqlite:///./student.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass

# Provide a database session per request
def get_db() -> Generator[Session, None, None]:
    """Provides a database session per request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()