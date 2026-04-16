"""Pytest configuration and fixtures for backend tests."""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

import pytest

# Must import models and base before creating test database
from database import Base
from main import app
from auth import get_db
import models


@pytest.fixture(scope="session")
def test_db_engine():
    """Create test database engine using SQLite in-memory."""
    # Use in-memory SQLite for fast tests
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
    )
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db_session(test_db_engine):
    """Create a new database session for each test."""
    connection = test_db_engine.connect()
    transaction = connection.begin()
    session = sessionmaker(autocommit=False, autoflush=False, bind=connection)()
    
    yield session
    
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def client(db_session):
    """Create a test client with mocked database dependency."""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as test_client:
        yield test_client
    
    app.dependency_overrides.clear()


@pytest.fixture
def admin_user(db_session):
    """Create an admin user in test database."""
    from auth import get_password_hash
    
    admin = models.User(
        username="admin@booksy.com",
        hashed_password=get_password_hash("admin123"),
        is_admin=True,
    )
    db_session.add(admin)
    db_session.commit()
    db_session.refresh(admin)
    return admin


@pytest.fixture
def regular_user(db_session):
    """Create a regular (non-admin) user in test database."""
    from auth import get_password_hash
    
    user = models.User(
        username="user@booksy.com",
        hashed_password=get_password_hash("password123"),
        is_admin=False,
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def admin_token(client, admin_user):
    """Get JWT token for admin user."""
    response = client.post(
        "/auth/token",
        data={"username": "admin@booksy.com", "password": "admin123"},
    )
    return response.json()["access_token"]


@pytest.fixture
def regular_user_token(client, regular_user):
    """Get JWT token for regular user."""
    response = client.post(
        "/auth/token",
        data={"username": "user@booksy.com", "password": "password123"},
    )
    return response.json()["access_token"]


@pytest.fixture
def available_device(db_session):
    """Create an available device in test database."""
    device = models.Device(
        name="Test Laptop",
        brand="Dell",
        status=models.DeviceStatus.AVAILABLE,
        notes="Test device",
    )
    db_session.add(device)
    db_session.commit()
    db_session.refresh(device)
    return device


@pytest.fixture
def in_use_device(db_session):
    """Create an in-use device in test database."""
    device = models.Device(
        name="Test iPad",
        brand="Apple",
        status=models.DeviceStatus.IN_USE,
        assigned_to="admin@booksy.com",
        notes="Already rented",
    )
    db_session.add(device)
    db_session.commit()
    db_session.refresh(device)
    return device


@pytest.fixture
def repair_device(db_session):
    """Create a device in repair status in test database."""
    device = models.Device(
        name="Test Phone",
        brand="Samsung",
        status=models.DeviceStatus.REPAIR,
        notes="In repair",
    )
    db_session.add(device)
    db_session.commit()
    db_session.refresh(device)
    return device
