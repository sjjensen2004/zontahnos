# app/services/v1/service_icmp_probe.py
from sqlalchemy.orm import Session
import app.db.crud.v1.crud_icmp_probe as cp
from app.db.models import IcmpProbe  
from app.schemas.v1 import schema_icmp_probe as schema
from app.core.logger import get_logger

logger = get_logger(__name__)

def create_probe(db: Session, probe_data: schema.ProbeCreate):
    return cp.create_probe(db, probe_data)

def get_probe(db: Session, probe_id: int):
    return cp.get_probe(db, probe_id)

def get_probe_by_name(db: Session, name: str):
    return cp.get_probe_by_name(db, name)

def delete_probe(db: Session, probe_id: int):
    return cp.delete_probe(db, probe_id)

def list_probes(db: Session):
    return db.query(IcmpProbe).all()  