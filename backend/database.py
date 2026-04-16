import os
from sqlalchemy import create_engine, event
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from dotenv import load_dotenv

# Load .env file for local development
load_dotenv()

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./app.db"
)

# SQLite requires check_same_thread=False, PostgreSQL doesn't need it
if "sqlite" in DATABASE_URL:
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False},
        # SQLite defaults to SERIALIZABLE isolation level
        # which provides good protection against race conditions
    )
    # Enable foreign key constraints for SQLite
    @event.listens_for(engine, "connect")
    def set_sqlite_pragma(dbapi_conn, connection_record):
        cursor = dbapi_conn.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()
else:
    # PostgreSQL connection pooling with better defaults for production
    engine = create_engine(
        DATABASE_URL,
        pool_size=5,
        max_overflow=10,
        pool_pre_ping=True,  # Test connections before using them
        # PostgreSQL uses READ COMMITTED by default
        # For critical operations, we use with_for_update() for explicit locking
    )

# Session factory with appropriate defaults
# autoflush=False: Prevents implicit flushes, giving explicit control
# expire_on_commit=True: Forces refresh after commit, ensuring fresh data
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    expire_on_commit=True
)


class Base(DeclarativeBase):
    pass
