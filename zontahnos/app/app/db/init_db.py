# app/db/init_db.py
from sqlalchemy.orm import Session
from app.core.database import engine, Base, SessionLocal
from app.db.models import IcmpProbe

def init_db():
    # Create tables
    Base.metadata.create_all(bind=engine)

    # Seed initial data if necessary
    db: Session = SessionLocal()
    try:
        # Example: Create an initial probe if it doesn't exist
        if not db.query(IcmpProbe).first():
            initial_probe = IcmpProbe(name="initial_probe", location="initial_location", secret_key="initial_key")
            db.add(initial_probe)
            db.commit()
    finally:
        db.close()

if __name__ == "__main__":
    init_db()