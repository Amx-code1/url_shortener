from sqlalchemy import Column, Integer, String
from app.db.base import Base
from sqlalchemy import DateTime
from datetime import datetime
from sqlalchemy import Integer


class URL(Base):
    __tablename__ = "urls"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    short_code = Column(String, unique=True, index=True)
    long_url = Column(String)
    expires_at = Column(DateTime, nullable=True)