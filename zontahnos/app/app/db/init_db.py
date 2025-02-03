# app/db/init_db.py
from sqlalchemy.orm import Session
from app.core.database import engine, Base, SessionLocal
from app.db import models

def init_db():
    # Create tables
    Base.metadata.create_all(bind=engine)

    # Seed initial data if necessary
    db: Session = SessionLocal()
    try:
        # Example: Create an initial probe if it doesn't exist
        if not db.query(models.IcmpProbe).first():
            initial_probe = models.IcmpProbe(name="initial_probe", location="initial_location", secret_key="initial_key")
            db.add(initial_probe)
            db.commit()
    finally:
        db.close()

if __name__ == "__main__":
    init_db()