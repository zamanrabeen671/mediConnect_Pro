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
    prescriptions_router,
    blood_group_router,
    medicines_router,
    admin_router,
    specializations_router,
    institutes_router,
    qualifications_router,
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
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
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
app.include_router(blood_group_router)
app.include_router(medicines_router)
app.include_router(admin_router)
app.include_router(specializations_router)
app.include_router(institutes_router)
app.include_router(qualifications_router)


# Health check endpoint
@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": settings.APP_NAME}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
