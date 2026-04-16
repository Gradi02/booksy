"""API routers for different feature domains."""
from .auth import router as auth_router
from .devices import router as devices_router
from .users import router as users_router
from .ai import router as ai_router

__all__ = ["auth_router", "devices_router", "users_router", "ai_router"]
