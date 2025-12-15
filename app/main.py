"""
FastAPI application entry point for MediConnectPro
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import Base, engine
from .core.config import settings
from .middleware.auth_middleware import AuthMiddleware
from .routers import (
    auth_router,
    users_router,
    doctors_router,
    patients_router,
    schedules_router,
    appointments_router,
    prescriptions_router
)

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Medical connectivity platform API"
)

# Add middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(AuthMiddleware)

# Include routers
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(doctors_router)
app.include_router(patients_router)
app.include_router(schedules_router)
app.include_router(appointments_router)
app.include_router(prescriptions_router)


# Health check endpoint
@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": settings.APP_NAME}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
