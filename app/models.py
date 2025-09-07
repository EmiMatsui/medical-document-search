from sqlalchemy import Column, Integer, BigInteger, String, Text, DateTime, func
from .db import Base

class FileRecord(Base):
    __tablename__ = "files"
    __table_args__ = {"sqlite_autoincrement": True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    original_name = Column(String(255), nullable=False)
    saved_path = Column(Text, nullable=False)
    mime_type = Column(String(100))
    size_bytes = Column(BigInteger)
    uploaded_at = Column(DateTime, nullable=False, server_default=func.now())
