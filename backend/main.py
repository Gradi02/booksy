import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import Base, engine
from routers import auth_router, devices_router, users_router
from seed_loader import initialize_data

app = FastAPI(title="Booksy Inventory API")

# Parse CORS origins from environment or use defaults
allowed_origins = os.getenv(
    "ALLOWED_ORIGINS",
    "http://localhost:5173,http://127.0.0.1:5173,http://localhost:3000,http://127.0.0.1:3000"
).split(",")

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# Include routers
app.include_router(auth_router)
app.include_router(devices_router)
app.include_router(users_router)


@app.on_event("startup")
def startup() -> None:
    """Initialize database and seed data on startup."""
    Base.metadata.create_all(bind=engine)
    from auth import get_db
    db = next(get_db())
    try:
        initialize_data(db)
    finally:
        db.close()


@app.get("/")
def root():
    """Health check endpoint."""
    return {"message": "Booksy Inventory API is running"}

