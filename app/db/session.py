from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import settings

engine: Engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,
)

SessionLocal: sessionmaker[Session] = sessionmaker(
    bind=engine,
    class_=Session,
    autoflush=False,
    expire_on_commit=False,
)
