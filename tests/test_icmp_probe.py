# tests/test_icmp_probe.py
import secrets
from app.schemas.v1 import schema_icmp_probe as schema
import logging

logger = logging.getLogger(__name__)

def test_create_icmp_probe(test_app, test_db, influx_manager):
    secret_key = secrets.token_hex(16)
    probe_data = schema.Create(name="test_probe", location="test_location", measurement="icmp_probes")
    response = test_app.post("/api/v1/icmp/create", json=probe_data.dict())
    logger.info(f"Create ICMP Probe Response: {response.json()}")
    assert response.status_code == 200
    assert response.json()["name"] == "test_probe"
    assert response.json()["location"] == "test_location"
    assert response.json()["measurement"] == "icmp_probes"
    assert "key" in response.json()

def test_list_icmp_probes(test_app, test_db, influx_manager):
    response = test_app.get("/api/v1/icmp/list")
    logger.info(f"List ICMP Probes Response: {response.json()}")
    assert response.status_code == 200
    assert "probes" in response.json()
    assert isinstance(response.json()["probes"], list)

def test_update_icmp_probe(test_app, test_db, influx_manager):
    # First, create a probe to update
    secret_key = secrets.token_hex(16)
    create_data = schema.Create(name="test_probe_update", location="test_location_update", measurement="icmp_probes")
    create_response = test_app.post("/api/v1/icmp/create", json=create_data.dict())
    assert create_response.status_code == 200

    # Update the probe
    update_data = schema.Update(
        location="updated_location",
        probe_name="test_probe_update",
        target_host="updated_host",
        latency=10.5,
        status=0,
        key=create_response.json()["key"]
    )
    update_response = test_app.post("/api/v1/icmp/update", json=update_data.dict())
    logger.info(f"Update ICMP Probe Response: {update_response.json()}")
    assert update_response.status_code == 200
    assert update_response.json()["message"] == "ICMP probe stored successfully"

def test_delete_icmp_probe(test_app, test_db, influx_manager):
    # First, create a probe to delete
    secret_key = secrets.token_hex(16)
    create_data = schema.Create(name="test_probe_delete", location="test_location_delete", measurement="icmp_probes")
    create_response = test_app.post("/api/v1/icmp/create", json=create_data.dict())
    assert create_response.status_code == 200

    # Delete the probe
    delete_data = schema.Delete(name="test_probe_delete")
    delete_response = test_app.post("/api/v1/icmp/delete", json=delete_data.dict())
    logger.info(f"Delete ICMP Probe Response: {delete_response.json()}")
    assert delete_response.status_code == 200
    assert delete_response.json()["message"] == "Probe test_probe_delete deleted successfully"