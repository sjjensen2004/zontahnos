# app/db/models.py
from sqlalchemy import Column, Integer, String
from app.core.database import Base
from core.logger import get_logger

logger = get_logger(__name__)

class IcmpProbe(Base):
    __tablename__ = "probes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    location = Column(String)
    measurement = Column(String)
    secret_key = Column(String)