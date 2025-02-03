# app/crud/v1/crud_icmp_probe.py
from sqlalchemy.orm import Session
from app.db import models
from app.schemas.postgres.v1 import schema

def create_probe(db: Session, probe: schema.ProbeCreate):
    db_probe = models.IcmpProbe(name=probe.name, location=probe.location, secret_key=probe.secret_key)
    db.add(db_probe)
    db.commit()
    db.refresh(db_probe)
    return db_probe

def get_probe(db: Session, probe_id: int):
    return db.query(models.IcmpProbe).filter(models.IcmpProbe.id == probe_id).first()

def get_probe_by_name(db: Session, name: str):
    return db.query(models.IcmpProbe).filter(models.IcmpProbe.name == name).first()

def delete_probe(db: Session, probe_id: int):
    db.query(models.IcmpProbe).filter(models.IcmpProbe.id == probe_id).delete()
    db.commit()

def list_probes(db: Session):
    return db.query(models.IcmpProbe).all()