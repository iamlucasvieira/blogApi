"""Module for database connection and queries."""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Create a SQLAlchemy engine.
SQLALCHEMY_DATABASE_URL = "sqlite:///./app.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# Create a SQLAlchemy declarative model.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a base class for our models.
Base = declarative_base()
