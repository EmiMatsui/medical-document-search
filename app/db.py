import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# 簡易：SQLite（必要なら MYSQL_URL=... を環境変数で渡す）
MYSQL_URL = os.getenv("MYSQL_URL")
DB_URL = MYSQL_URL if MYSQL_URL else "sqlite:///./uploads.db"

engine = create_engine(DB_URL, pool_pre_ping=True, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
