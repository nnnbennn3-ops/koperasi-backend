from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.controllers.master import SavingTypeController
from src.controllers.transaction import (
    DashboardController,
)

app = FastAPI(
    title="Koperasi Karyawan Backend API",
    version="1.0.0",
    description="Backend Service untuk Koperasi Karyawan Clean Architecture",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# REGISTER ROUTERS
app.include_router(DashboardController.router)
app.include_router(SavingTypeController.router)


@app.get("/")
def root():
    return {
        "status": "online",
        "service": "Koperasi Karyawan Backend",
        "version": "1.0.0",
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}
