# app/crud/v1/crud_icmp_probe.py
from sqlalchemy.orm import Session
from app.db.models import IcmpProbe
from app.schemas.v1 import schema_icmp_probe as schema
from core.logger import get_logger

logger = get_logger(__name__)

def create_probe(db: Session, probe: schema.ProbeCreate):
    db_probe = IcmpProbe(name=probe.name, location=probe.location, measurement=probe.measurement, secret_key=probe.secret_key)
    db.add(db_probe)
    db.commit()
    db.refresh(db_probe)
    return db_probe

def get_probe(db: Session, probe_id: int):
    return db.query(IcmpProbe).filter(IcmpProbe.id == probe_id).first()

def get_probe_by_name(db: Session, name: str):
    return db.query(IcmpProbe).filter(IcmpProbe.name == name).first()

def delete_probe(db: Session, probe_id: int):
    db.query(IcmpProbe).filter(IcmpProbe.id == probe_id).delete()
    db.commit()

def list_probes(db: Session):
    return db.query(IcmpProbe).all()