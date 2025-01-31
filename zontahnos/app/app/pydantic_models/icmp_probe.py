from pydantic import BaseModel, Field
from typing import Optional


class Create(BaseModel):
    name: str = Field(
        ..., description="The referrence name for the probe. Must be unique."
    )
    location: str = Field(..., description="The location of the probe.")
    measurement: str = Field("icmp_probes", description="The InfluxDB Measurement.")


class Delete(BaseModel):
    name: str = Field(
        ..., description="The referrence name for the probe. Must be unique."
    )


class Update(BaseModel):
    location: str
    probe_name: str
    target_host: str
    latency: Optional[float] = None
    status: int  # Boolean, 0 = Success, 1 = Failure
    key: str = Field(..., description="The secret key for the probe.")
