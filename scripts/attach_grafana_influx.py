import requests
import logging

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)


def attach_grafana_influx(grafana_api_key, grafana_url, influx_url, influx_org, influx_bucket, influx_api_token):
    headers = {
        "Authorization": f"Bearer {grafana_api_key}",
        "Content-Type": "application/json"
    }

    data = {
        "name": "InfluxDB",
        "type": "influxdb",
        "url": influx_url,
        "access": "proxy",
        "basicAuth": False,
        "jsonData": {
            "version": "Flux",
            "organization": influx_org,
            "defaultBucket": influx_bucket,
            "httpMode": "POST"
        },
        "secureJsonData": {
            "token": influx_api_token
        }
    }

    try:
        response = requests.post(f"{grafana_url}/api/datasources", json=data, headers=headers)
        response.raise_for_status()
        return "InfluxDB successfully added to Grafana!"
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to add InfluxDB to Grafana: {e}")
        raise

if __name__ == "__main__":
    pass