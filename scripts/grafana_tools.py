import requests
from requests.auth import HTTPBasicAuth
import logging

"""
This generates a Grafana API key and stores it in hashicorp vault (path=grafana/api-key)
"""

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

class GrafanaTools:
    def __init__(self, grafana_url, grafana_username, grafana_password):
        self.grafana_url = grafana_url
        self.grafana_username = grafana_username
        self.grafana_password = grafana_password

    def create_service_account(self, service_account_name):
        try:
            response = requests.post(
                f"{self.grafana_url}/api/serviceaccounts",
                auth=HTTPBasicAuth(self.grafana_username, self.grafana_password),
                headers={"Content-Type": "application/json"},
                json={"name": service_account_name, "role": "Admin"}
            )
            response.raise_for_status()
            service_account_data = response.json()
            service_account_id = service_account_data["id"]
            logger.info(f"Created Service Account with ID: {service_account_id}")
            return service_account_id
        except requests.exceptions.RequestException as e:
            logger.error(f"Error creating service account: {e}")

    def generate_api_token(self, service_account_id, api_token_name):
        try:
            token_response = requests.post(
                f"{self.grafana_url}/api/serviceaccounts/{service_account_id}/tokens",
                auth=HTTPBasicAuth(self.grafana_username, self.grafana_password),
                headers={"Content-Type": "application/json"},
                json={"name": api_token_name}
            )
            token_response.raise_for_status()
            api_key = token_response.json()["key"]
            logging.info(f"Generated API Key: {api_key}")
            return api_key
        except requests.exceptions.RequestException as e:
            logger.error(f"Error generating token: {e}")


if __name__ == "__main__":
    pass
