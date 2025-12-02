from fastapi import FastAPI
from .database import Base, engine
from .routers import users, doctors, patients, appointments, prescriptions

Base.metadata.create_all(bind=engine)

app = FastAPI(title="MediConnectPro API")

app.include_router(users.router)
app.include_router(doctors.router)
app.include_router(patients.router)
app.include_router(appointments.router)
app.include_router(prescriptions.router)
