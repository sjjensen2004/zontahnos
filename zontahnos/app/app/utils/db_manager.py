from influxdb_client import InfluxDBClient, Point, WritePrecision
from datetime import datetime
import logging
from app.core.config import settings

logger = logging.getLogger(__name__)

INFLUXDB_TOKEN = settings.INFLUXDB_TOKEN
INFLUXDB_URL = settings.INFLUXDB_URL
ORG = settings.ORG
BUCKET = settings.BUCKET   

class InfluxDBManager:
    def __init__(self):
        """Initialize InfluxDB client and APIs."""
        self.client = InfluxDBClient(
            url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=ORG
        )
        self.write_api = self.client.write_api()
        self.query_api = self.client.query_api()

    def create_icmp_probe(self, name: str, location: str, secret_key: str):
        """Create a new ICMP probe entry with a secret key."""
        logger.info(f"LOG: {INFLUXDB_TOKEN}")
        point = (
            Point("icmp_probes")  # Measurement
            .tag("name", name)  # Probe Name
            .tag("location", location)  # Probe Location
            .field("key", secret_key)  # Secret Key
            .time(datetime.utcnow(), WritePrecision.NS)  # Timestamp
        )
        self.write_api.write(bucket=BUCKET, org=ORG, record=point)
        logger.info(f"✅ ICMP Probe {name} created with key {secret_key}.")

    def write_icmp_probe(
        self,
        location: str,
        probe_name: str,
        target_host: str,
        latency: float,
        status: int,
    ):
        """Write ICMP probe data to InfluxDB."""
        point = (
            Point("icmp_latency")  # Measurement
            .tag("location", location)  # Probe Location
            .tag("probe", probe_name)  # Unique Probe Name
            .tag("host", target_host)  # Target Host
            .field("latency", latency)  # ICMP Latency
            .field("status", int(status))  # Success/Failure
            .time(datetime.utcnow(), WritePrecision.NS)  # Timestamp
        )

        self.write_api.write(bucket=BUCKET, org=ORG, record=point)
        logger.info(f"✅ ICMP Probe from {location} ({target_host}) stored.")

    def validate_probe_key(self, probe_name: str, key: str) -> bool:
        """Validate the secret key for a given probe."""
        query = f'from(bucket: "{BUCKET}") |> range(start: -1d) |> filter(fn: (r) => r._measurement == "icmp_probes" and r.name == "{probe_name}" and r._field == "key" and r._value == "{key}")'
        result = self.query_api.query(org=ORG, query=query)
        return len(result) > 0

    def probe_exists(self, probe_name: str) -> bool:
        """Check if a probe with the given name already exists."""
        query = f'from(bucket: "{BUCKET}") |> range(start: -1d) |> filter(fn: (r) => r._measurement == "icmp_probes" and r.name == "{probe_name}")'
        result = self.query_api.query(org=ORG, query=query)
        return len(result) > 0
    
    def list_icmp_probes(self):
        """List all ICMP probes with their name and location."""
        query = f'from(bucket: "{BUCKET}") |> range(start: -1d) |> filter(fn: (r) => r._measurement == "icmp_probes") |> keep(columns: ["name", "location"])'
        result = self.query_api.query(org=ORG, query=query)
        probes = []
        for table in result:
            for record in table.records:
                probes.append({"name": record["name"], "location": record["location"]})
        return probes

    def close(self):
        """Close InfluxDB connection."""
        self.client.close()
