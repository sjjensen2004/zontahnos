from fastapi import APIRouter
from app.api.api_v1.endpoints import icmp_probe

api_router = APIRouter()
api_router.include_router(icmp_probe.router, prefix="/icmp", tags=['ICMP Probe'])