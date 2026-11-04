from dataclasses import dataclass
from fastapi import HTTPException, Request, Security
from fastapi.security.api_key import APIKeyHeader
from src.utils.ExtractToken import extract_token

# Menandai ke Swagger bahwa endpoint butuh Header Authorization
api_key_header = APIKeyHeader(name="authorization", auto_error=False)


@dataclass
class AuthContext:
    authorization: str
    user_id: int
    company_id: int | None = None
    payload: dict | None = None


def get_auth_context(
    request: Request, api_key: str | None = Security(api_key_header)
) -> AuthContext:
    """Mengekstrak dan memvalidasi JWT token dari Header Authorization."""
    authorization = api_key or request.headers.get("authorization")
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing Authorization Header")

    payload = extract_token(authorization)
    if not isinstance(payload, dict):
        raise HTTPException(status_code=401, detail="Invalid token payload")

    user_id_raw = (
        payload.get("user_id") or payload.get("user_employee_id") or payload.get("sub")
    )
    if not user_id_raw:
        raise HTTPException(
            status_code=401, detail="user_id not found in authorization token"
        )

    try:
        user_id = int(user_id_raw)
    except (ValueError, TypeError):
        raise HTTPException(status_code=401, detail="Invalid user_id format in token")

    company_id_raw = payload.get("active_company_id") or payload.get("company_id")
    company_id = int(company_id_raw) if company_id_raw is not None else None

    return AuthContext(
        authorization=authorization,
        user_id=user_id,
        company_id=company_id,
        payload=payload,
    )
