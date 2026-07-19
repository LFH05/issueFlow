"""Shared FastAPI dependencies belong here."""

from collections.abc import Generator

from sqlalchemy.orm import Session

from app.db.session import SessionLocal


# 为一次 FastAPI 请求创建一份数据库 Session；请求结束后关闭 Session 并归还连接。
def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
