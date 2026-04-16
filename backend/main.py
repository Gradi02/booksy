import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import Base, engine
from routers import auth_router, devices_router, users_router, ai_router
from seed_loader import initialize_data


def startup() -> None:
    """Initialize database and seed data on startup."""
    Base.metadata.create_all(bind=engine)
    from auth import get_db
    db = next(get_db())
    try:
        initialize_data(db)
    finally:
        db.close()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan context manager."""
    # Startup
    startup()
    yield
    # Shutdown (add cleanup logic here if needed)


app = FastAPI(
    title="Booksy Inventory API",
    lifespan=lifespan,
) 

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router)
app.include_router(devices_router)
app.include_router(users_router)
app.include_router(ai_router)


@app.get("/")
def root():
    """Health check endpoint."""
    return {"message": "Booksy Inventory API is running"}

