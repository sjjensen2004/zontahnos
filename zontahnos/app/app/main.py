from fastapi import FastAPI
from app.api.v1 import api_router
from app.api.pages_router.route_home import home_router
from app.core.config import settings
from app.db.init_db import init_db
import logging


def configure_logging():
    """Configure logging for the application."""
    logging.basicConfig(
        filename="logs/main.txt",
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=logging.DEBUG,
    )
    logger = logging.getLogger(__name__)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(
        logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    )
    logger.addHandler(console_handler)


def include_routers(app: FastAPI):
    """Include routers in the FastAPI application."""
    app.include_router(api_router, prefix=settings.API_V1)
    app.include_router(home_router)


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    configure_logging()
    app = FastAPI(title="Zontahnos", openapi_url=f"/api/v1")
    include_routers(app)

    @app.on_event("startup")
    async def startup_event():
        init_db()

    return app


app = create_app()