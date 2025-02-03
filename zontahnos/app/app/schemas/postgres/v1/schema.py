# app/schemas/v1/schema.py
from pydantic import BaseModel, Field
from typing import Optional

class ProbeCreate(BaseModel):
    name: str = Field(..., description="The reference name for the probe. Must be unique.")
    location: str = Field(..., description="The location of the probe.")
    secret_key: str = Field(..., description="The secret key for the probe.")

class Probe(BaseModel):
    id: int
    name: str
    location: str
    secret_key: str

    class Config:
        orm_mode = True