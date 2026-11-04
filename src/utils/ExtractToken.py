import os
from fastapi import HTTPException, status
import jwt
from jwt.algorithms import RSAAlgorithm
import requests
from src.configs.config import settings

_cached_public_key = None
ALGORITHM = "RS256"


def get_public_key():
    global _cached_public_key
    if _cached_public_key is not None:
        return _cached_public_key

    try:
        if hasattr(settings, "user_service_url") and settings.user_service_url:
            user_url = settings.user_service_url.rstrip("/")
            if "/v1" in user_url:
                jwks_url = f"{user_url}/.well-known/jwks.json"
            else:
                jwks_url = f"{user_url}/v1/.well-known/jwks.json"

            response = requests.get(jwks_url, timeout=3)
            if response.status_code == 200:
                jwks_data = response.json()
                keys = jwks_data.get("keys", [])
                if keys:
                    rsa_key = next((k for k in keys if k.get("kty") == "RSA"), keys[0])
                    _cached_public_key = RSAAlgorithm.from_jwk(rsa_key)
                    return _cached_public_key
    except Exception:
        pass

    base_dir = os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    )
    pem_path = os.path.join(base_dir, "security", "public.pem")
    if os.path.exists(pem_path):
        with open(pem_path) as f:
            _cached_public_key = f.read()

    return _cached_public_key


def extract_token(api_key: str) -> dict:
    """Mengekstrak dan memverifikasi token RS256 dengan error handling rapi."""
    if not api_key:
        return {}
    if "Bearer" in api_key:
        api_key_split = api_key.split(" ")
        api_key_short = api_key_split[1]
    else:
        api_key_short = api_key

    key = get_public_key()
    try:
        payload = jwt.decode(
            api_key_short,
            key,
            algorithms=[ALGORITHM],
            leeway=2,
            options={"verify_aud": False},
        )
        return payload
    except jwt.ExpiredSignatureError:
        # Tangkap token expired secara sopan -> HTTP 401
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired, please log in again",
        )
    except jwt.InvalidTokenError:
        # Tangkap token palsu / signature salah -> HTTP 401
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token signature",
        )


def extract_user_id_from_token(api_key: str | None) -> int | None:
    if not api_key:
        return None
    try:
        payload = extract_token(api_key)
        if isinstance(payload, dict):
            val = (
                payload.get("user_id")
                or payload.get("user_employee_id")
                or payload.get("sub")
            )
            if val is not None:
                return int(val)
    except Exception:
        pass
    return None
