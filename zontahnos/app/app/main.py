from fastapi import FastAPI
from app.api.v1 import api_router
from app.api.pages_router.route_home import home_router
from app.core.config import settings
from app.db.init_db import init_db
from app.core.logger import get_logger

def include_routers(app: FastAPI):
    """Include routers in the FastAPI application."""
    app.include_router(api_router, prefix=settings.API_V1)
    app.include_router(home_router)


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(title="Zontahnos", openapi_url=f"/api/v1")
    logger = get_logger(__name__) 
    logger.info("tes")
    include_routers(app)

    @app.on_event("startup")
    async def startup_event():
        init_db()

    return app


app = create_app()