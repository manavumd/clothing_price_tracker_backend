from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

# Load environment variable for the database URL
DATABASE_URL = os.getenv("DATABASE_URL")

# Create the SQLAlchemy engine for MySQL
engine = create_engine(DATABASE_URL)

# SessionLocal will be used to interact with the database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for creating ORM models
Base = declarative_base()

def get_db():
    """
    Get a database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
