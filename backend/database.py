import os
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

# Load .env file for local development
from dotenv import load_dotenv
load_dotenv()

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./app.db"
)

# SQLite requires check_same_thread=False, PostgreSQL doesn't need it
if "sqlite" in DATABASE_URL:
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
    engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass
