# app/api/v1/routes/icmp_probe.py
import secrets
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.schemas.influx import icmp_probe
from app.utils.influx_db_manager import InfluxDBManager
from app.core.database import get_db
from app.services.v1 import service_icmp_probe
from app.schemas.postgres.v1 import schema
import logging

logger = logging.getLogger(__name__)

router = APIRouter()
db_manager = InfluxDBManager()


@router.post("/create", summary="Create an ICMP probe")
def create_icmp_probe(body: icmp_probe.Create, db: Session = Depends(get_db)):
    """
    Generate a key and database entry to collect ICMP probe metrics.
    """
    # Check if the probe name already exists in PostgreSQL
    if service_icmp_probe.get_probe_by_name(db, name=body.name):
        raise HTTPException(status_code=400, detail="Probe name already exists")

    secret_key = secrets.token_hex(16)  # Generate a 32-character hex key
    try:
        # Create the probe in PostgreSQL
        probe_data = schema.ProbeCreate(name=body.name, location=body.location, measurement=body.measurement, secret_key=secret_key)
        service_icmp_probe.create_probe(db=db, probe_data=probe_data)
        return {"name": body.name, "location": body.location, "measurement":body.measurement, "key": secret_key}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create probe: {str(e)}")


@router.post("/delete", summary="Delete an ICMP probe")
def delete_icmp_probe(body: icmp_probe.Delete, db: Session = Depends(get_db)):
    """
    Delete an ICMP probe by name.
    """
    # Check if the probe name exists in PostgreSQL
    db_probe = service_icmp_probe.get_probe_by_name(db, name=body.name)
    if not db_probe:
        raise HTTPException(status_code=404, detail="Probe not found")

    try:
        # Delete the probe in InfluxDB
        db_manager.delete_icmp_probe(body.name)
        # Delete the probe in PostgreSQL
        service_icmp_probe.delete_probe(db=db, probe_id=db_probe.id)
        return {"message": f"Probe {body.name} deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete probe: {str(e)}")


@router.post("/update", summary="Update probe metrics")
def update_icmp_record(body: icmp_probe.Update, db: Session = Depends(get_db)):
    """
    Update an existing ICMP agent record.
    """
    try:
        # Check if the secret key is valid in PostgreSQL
        db_probe = service_icmp_probe.get_probe_by_name(db, name=body.probe_name)
        if not db_probe or db_probe.secret_key != body.key:
            raise HTTPException(
                status_code=403, detail="Invalid secret key and/or probe name."
            )

        # Store the metrics in InfluxDB
        db_manager.write_icmp_probe(
            body.location, body.probe_name, body.target_host, body.latency, body.status
        )
        return {"message": "ICMP probe stored successfully"}

    except HTTPException as http_exc:  # Allow FastAPI to handle known errors
        raise http_exc

    except Exception as e:  # Catch unexpected errors and return a 500
        raise HTTPException(status_code=500, detail=f"Failed to store probe: {str(e)}")


@router.get("/list", summary="List all ICMP probes")
def list_icmp_probes(db: Session = Depends(get_db)):
    """
    List all existing ICMP probes with their name, location and measurement.
    """
    try:
        probes = service_icmp_probe.list_probes(db)
        return {"probes": probes}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list probes: {str(e)}")