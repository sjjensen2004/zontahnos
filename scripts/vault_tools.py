import hvac
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

VAULT_ADDR = "http://127.0.0.1:8200"  
VAULT_TOKEN = "root"

class VaultTool:
    def __init__(self, vault_url: str, vault_token: str):
        self.client = hvac.Client(url=vault_url, token=vault_token)
        if not self.client.is_authenticated():
            logger.error("Vault authentication failed")
        else:
            logger.info("Vault authentication successful")

    def mounted_secret_engines(self):
        try:
            response = self.client.sys.list_mounted_secrets_engines()
            return response["data"]
        except Exception as e:
            logger.error(f"Error listing mounted secret engines: {e}")
    
    def mount_custom_engine(self, name: str):
        try:
            self.client.sys.enable_secrets_engine(
                backend_type="kv",
                path=name,
                options={"version": 2}
            )
            logger.info(f"Successfully mounted secret engine at path: {name}")
        except Exception as e:
            logger.error(f"Error mounting secret engine at path {name}: {e}")

    def store_kv(self, mount_point, path, data):
        self.client.secrets.kv.v2.create_or_update_secret(
            mount_point=mount_point,
            path=path,
            secret=data
        )

            
if __name__ == "__main__":
    vt = VaultTool(VAULT_ADDR, VAULT_TOKEN)
    vt.mount_custom_engine("dev")
    logger.info(vt.mounted_secret_engines())