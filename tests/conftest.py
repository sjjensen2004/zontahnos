# tests/conftest.py
import pytest
from fastapi.testclient import TestClient
from app.main import create_app
from app.core.database import Base, engine, SessionLocal

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