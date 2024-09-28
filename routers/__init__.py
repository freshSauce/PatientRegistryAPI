from .patients import router as patients_router
from .doctors import router as doctors_router
from .auth import router as auth_router

__all__ = ["patients_router", "doctors_router", "auth_router"]