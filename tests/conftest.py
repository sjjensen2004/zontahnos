# tests/conftest.py
import pytest
import logging
import time
from fastapi.testclient import TestClient
from app.main import create_app
from app.core.database import Base, engine, SessionLocal
from app.utils.influx_db_manager import InfluxDBManager

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

@pytest.fixture(scope="module")
def test_app():
    app = create_app()
    client = TestClient(app)
    yield client

@pytest.fixture(scope="module")
def test_db():
    # Create the database and tables
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    yield db
    db.close()
    # Drop the database and tables
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="module")
def influx_manager():
    # Initialize InfluxDBManager
    manager = InfluxDBManager()
    yield manager
    # Optionally, clean up InfluxDB data here if needed

@pytest.fixture(scope="session", autouse=True)
def delay_shutdown():
    yield
    # Delay shutdown for 10 seconds
    time.sleep(10)