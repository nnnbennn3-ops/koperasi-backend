from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.middlewares.VerifiedToken import verify_token
from src.utils.AuthContext import AuthContext, get_auth_context
from src.controllers.master import SavingTypeController

app = FastAPI(
    title="Koperasi Karyawan Backend API",
    version="1.0.0",
    description="Backend Service untuk Koperasi Karyawan Clean Architecture",
    # dependencies=[Depends(verify_token)],
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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


# Contoh protected endpoint yang membaca user_id dari JWT
@app.get("/api/v1/profile")
def get_my_profile(auth: AuthContext = Depends(get_auth_context)):
    return {
        "message": "Token valid!",
        "user_id": auth.user_id,
        "company_id": auth.company_id,
        "payload": auth.payload,
    }
