import secrets
from fastapi import APIRouter, HTTPException
from app.pydantic_models import icmp_probe
from app.utils.db_manager import InfluxDBManager
from app.core.config import settings
import logging 

logger = logging.getLogger(__name__)

router = APIRouter()
db_manager = InfluxDBManager()

@router.post("/create", summary="Create an ICMP probe")
def create_icmp_probe(body: icmp_probe.Create):
    """
    Generate a key and database entry to collect ICMP probe metrics.
    """
    # Check if the probe name already exists
    if db_manager.probe_exists(body.name):
        raise HTTPException(status_code=400, detail="Probe name already exists")

    secret_key = secrets.token_hex(16)  # Generate a 32-character hex key
    try:
        db_manager.create_icmp_probe(body.name, body.location, secret_key)
        return {"name": body.name, "location": body.location, "key": secret_key}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create probe: {str(e)}")

@router.post("/delete", summary="Delete an ICMP probe")
def delete_icmp_probe(body: icmp_probe.Delete):
    """
    Delete an ICMP probe by name.
    """
    # Check if the probe name exists
    if not db_manager.probe_exists(body.name):
        raise HTTPException(status_code=404, detail="Probe not found")

    try:
        db_manager.delete_icmp_probe(body.name)
        return {"message": f"Probe {body.name} deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete probe: {str(e)}")

@router.post("/update", summary="Update probe metrics")
def update_icmp_record(body: icmp_probe.Update):
    """
    Update an existing ICMP agent record.
    """
    try:
        if not db_manager.validate_probe_key(body.probe_name, body.key):
            raise HTTPException(status_code=403, detail="Invalid secret key and/or probe name.")
        
        db_manager.write_icmp_probe(
            body.location,
            body.probe_name,
            body.target_host,
            body.latency,
            body.status
        )
        return {"message": "ICMP probe stored successfully"}
    
    except HTTPException as http_exc:  # Allow FastAPI to handle known errors
        raise http_exc  
    
    except Exception as e:  # Catch unexpected errors and return a 500
        raise HTTPException(status_code=500, detail=f"Failed to store probe: {str(e)}")
    
@router.get("/list", summary="List all ICMP probes")
def list_icmp_probes():
    """
    List all existing ICMP probes with their name and location.
    """
    try:
        probes = db_manager.list_icmp_probes()
        return {"probes": probes}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list probes: {str(e)}")
    