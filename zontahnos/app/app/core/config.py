from pydantic import BaseSettings
import hvac

class Settings(BaseSettings):
    API_V1: str = "/api/v1"
    INFLUXDB_URL: str
    INFLUXDB_TOKEN: str
    ORG: str
    BUCKET: str
    GRAFANA_TOKEN: str = None

    class Config:
        env_file = ".env"

settings = Settings()
