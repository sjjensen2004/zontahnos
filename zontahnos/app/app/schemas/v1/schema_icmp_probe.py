from pydantic import BaseModel, Field
from typing import Optional
from app.core.logger import get_logger

logger = get_logger(__name__)

class Create(BaseModel):
    name: str = Field(..., description="The reference name for the probe. Must be unique.")
    location: str = Field(..., description="The location of the probe.")
    measurement: str = Field("icmp_probes", description="The InfluxDB Measurement.")

class ProbeCreate(BaseModel):
    name: str = Field(..., description="The reference name for the probe. Must be unique.")
    location: str = Field(..., description="The location of the probe.")
    measurement: str = Field(..., description="Influx Measurement Name")
    secret_key: str = Field(..., description="The secret key for the probe.")

class Probe(BaseModel):
    id: int
    name: str
    location: str
    measurement: str
    secret_key: str

    class Config:
        orm_mode = True

class Delete(BaseModel):
    name: str = Field(..., description="The reference name for the probe.")

class Update(BaseModel):
    location: str
    probe_name: str
    target_host: str
    latency: Optional[float] = None
    status: int  # Boolean, 0 = Success, 1 = Failure
    key: str = Field(..., description="The secret key for the probe.")