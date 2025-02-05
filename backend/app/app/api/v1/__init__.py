from fastapi import APIRouter
from app.api.v1.routes import icmp_probe

api_router = APIRouter()
api_router.include_router(icmp_probe.router, prefix="/icmp", tags=["ICMP Probe"])
