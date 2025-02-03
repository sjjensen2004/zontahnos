from influxdb_client import InfluxDBClient, Point, WritePrecision
from datetime import datetime
from app.core.config import settings
from core.logger import get_logger

logger = get_logger(__name__)

INFLUXDB_TOKEN = settings.INFLUXDB_TOKEN
INFLUXDB_URL = settings.INFLUXDB_URL
ORG = settings.ORG
BUCKET = settings.BUCKET


class InfluxDBManager:
    def __init__(self):
        """Initialize InfluxDB client and APIs."""
        self.client = InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=ORG)
        self.write_api = self.client.write_api()
        self.query_api = self.client.query_api()
        self.delete_api = self.client.delete_api()

    # def create_icmp_probe(self, name: str, location: str, secret_key: str):
    #     """Create a new ICMP probe entry with a secret key."""
    #     point = (
    #         Point("icmp_probes")  # Measurement
    #         .tag("name", name)  # Probe Name
    #         .tag("location", location)  # Probe Location
    #         .field("key", secret_key)  # Secret Key
    #         .field("active", True)  # Status
    #         .time(datetime.utcnow(), WritePrecision.NS)  # Timestamp
    #     )
    #     self.write_api.write(bucket=BUCKET, org=ORG, record=point)
    #     logger.info(f"ICMP Probe {name} created with key {secret_key}.")

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
            Point("icmp_probes")  # Measurement
            .tag("location", location)  # Probe Location
            .tag("name", probe_name)  # Unique Probe Name
            .tag("host", target_host)  # Target Host
            .field("latency", latency)  # ICMP Latency
            .field("status", int(status))  # Success/Failure
            .time(datetime.utcnow(), WritePrecision.NS)  # Timestamp
        )

        self.write_api.write(bucket=BUCKET, org=ORG, record=point)
        logger.info(f"ICMP Probe from {location} ({target_host}) stored.")

    # def validate_probe_key(self, probe_name: str, key: str) -> bool:
    #     """Validate the secret key for a given probe."""
    #     query = f'from(bucket: "{BUCKET}") |> range(start: 0) |> filter(fn: (r) => r._measurement == "icmp_probes" and r.name == "{probe_name}" and r._field == "key" and r._value == "{key}")'
    #     result = self.query_api.query(org=ORG, query=query)
    #     return len(result) > 0

    # def probe_exists(self, probe_name: str) -> bool:
    #     """Check if a probe with the given name already exists."""
    #     query = f'from(bucket: "{BUCKET}") |> range(start: 0) |> filter(fn: (r) => r._measurement == "icmp_probes" and r.name == "{probe_name}")'
    #     result = self.query_api.query(org=ORG, query=query)
    #     return len(result) > 0

    # def list_icmp_probes(self):
    #     """List all active ICMP probes with their name and location."""
    #     query = f'''
    #     from(bucket: "{BUCKET}")
    #       |> range(start: 0)  // Include all data
    #       |> filter(fn: (r) => r._measurement == "icmp_probes")
    #       |> filter(fn: (r) => r._field == "active" and r._value == true)
    #       |> group(columns: ["name", "location"])
    #       |> distinct(column: "name")
    #     '''
    #     result = self.query_api.query(org=ORG, query=query)
    #     probes = []
    #     for table in result:
    #         for record in table.records:
    #             probes.append({"name": record["name"], "location": record["location"]})
    #     return probes

    # def delete_icmp_probe(self, probe_name: str):
    #     """Set the ICMP probe as inactive and then delete it by its name."""
    #     # Set the probe as inactive
    #     point = (
    #         Point("icmp_probes")
    #         .tag("name", probe_name)
    #         .field("active", False)
    #         .time(datetime.utcnow(), WritePrecision.NS)
    #     )
    #     self.write_api.write(bucket=BUCKET, org=ORG, record=point)
    #     logger.info(f"ICMP Probe '{probe_name}' set to inactive.")

    #     # Proceed to delete the probe
    #     start_time = "1970-01-01T00:00:00Z"
    #     end_time = datetime.utcnow().isoformat() + "Z"
    #     safe_probe_name = probe_name.replace('"', '\\"')
    #     predicate = f'_measurement="icmp_probes" AND "name"=\'{safe_probe_name}\''

    #     try:
    #         self.delete_api.delete(
    #             start=start_time,
    #             stop=end_time,
    #             predicate=predicate,
    #             bucket=BUCKET,
    #             org=ORG,
    #         )
    #         logger.info(f"ICMP Probe '{probe_name}' deleted successfully.")
    #     except Exception as e:
    #         logger.error(f"Failed to delete probe '{probe_name}': {e}")