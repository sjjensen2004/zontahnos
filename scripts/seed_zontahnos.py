from dotenv import load_dotenv
import os
from vault_tools import VaultTool
from grafana_tools import GrafanaTools
from attach_grafana_influx import attach_grafana_influx
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

load_dotenv()

GRAFANA_URL = "http://127.0.0.1:3000"
GRAFANA_SERVICE_ACCOUNT = "zontahnos"
GRAFANA_API_TOKEN_NAME = "zontahnos"
INFLUX_URL = "http://127.0.0.1:8086"
INFLUX_USERNAME = os.getenv("INFLUXDB_USERNAME")
INFLUXDB_PASSWORD = os.getenv("INFLUXDB_PASSWORD")
INFLUXDB_TOKEN = os.getenv("INFLUXDB_TOKEN")
INFLUXDB_INIT_ORG = os.getenv("INFLUXDB_INIT_ORG")
INFLUXDB_INIT_BUCKET = os.getenv("INFLUXDB_INIT_BUCKET")
GF_SECURITY_ADMIN_USER = os.getenv("GF_SECURITY_ADMIN_USER")
GF_SECURITY_ADMIN_PASSWORD = os.getenv("GF_SECURITY_ADMIN_PASSWORD")


if __name__ == "__main__":
    # Seed Vault Schema for dev and prod envs
    influxpath = "dev/zontahnos/influxdb"
    grafanapath = "dev/zontahnos/grafana"

    # Create Vault Tools object
    vt = VaultTool(
        vault_url=os.getenv("VAULT_ADDR"),
        vault_token=os.getenv("VAULT_DEV_ROOT_TOKEN_ID"),
    )
    vt.mount_custom_engine("dev")
    vt.mount_custom_engine("prod")

    # Store env KV in Vault
    vt.store_kv(influxpath, {"username": INFLUX_USERNAME})
    vt.store_kv(influxpath, {"password": INFLUXDB_PASSWORD})
    vt.store_kv(influxpath, {"api_token": INFLUXDB_TOKEN})
    vt.store_kv(influxpath, {"init_org": INFLUXDB_INIT_ORG})
    vt.store_kv(influxpath, {"init_bucket": INFLUXDB_INIT_BUCKET})
    vt.store_kv(grafanapath, {"username": GF_SECURITY_ADMIN_USER})
    vt.store_kv(grafanapath, {"password": GF_SECURITY_ADMIN_PASSWORD})

    # Create Grafana Tools object
    gt = GrafanaTools(
        grafana_url=GRAFANA_URL,
        grafana_username=GF_SECURITY_ADMIN_USER,
        grafana_password=GF_SECURITY_ADMIN_PASSWORD,
    )

    # Create a Grafana service account
    gsa = gt.create_service_account(service_account_name=GRAFANA_SERVICE_ACCOUNT)

    # Generate a Grafana API token
    gat = gt.generate_api_token(
        service_account_id=gsa, api_token_name=GRAFANA_API_TOKEN_NAME
    )

    # Store the Grafana API token in Vault
    vt.store_kv(grafanapath, {"api_key": gat})

    # Attach InfluxDB to Grafana
    attach_grafana_influx(
        grafana_url=GRAFANA_URL,
        grafana_api_key=gat,
        influx_url=INFLUX_URL,
        influx_api_token=INFLUXDB_TOKEN,
        influx_bucket=INFLUXDB_INIT_BUCKET,
        influx_org=INFLUXDB_INIT_ORG,
    )
