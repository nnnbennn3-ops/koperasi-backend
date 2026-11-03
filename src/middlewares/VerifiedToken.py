import logging
from datetime import UTC, datetime
import jwt
from fastapi import HTTPException, Request, Security, status
from fastapi.security.api_key import APIKeyHeader

from src.utils.ExtractToken import get_public_key

logger = logging.getLogger("uvicorn.error")
ALGORITHM = "RS256"

api_key_header = APIKeyHeader(name="authorization", auto_error=False)

_EXCLUDED_DOC_PATHS = (
    "/docs",
    "/redoc",
    "/openapi.json",
    "/docs/oauth2-redirect",
    "/health",
    "/",
)


def _is_excluded_path(path: str) -> bool:
    normalized = path.rstrip("/") or "/"
    return normalized in _EXCLUDED_DOC_PATHS


def verify_token(request: Request, api_key: str = Security(api_key_header)):
    """Validasi Bearer token RS256 untuk setiap route."""
    if _is_excluded_path(request.url.path):
        return None

    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="missing or invalid token",
        )

    try:
        if "Bearer " in api_key:
            api_key_short = api_key.split(" ")[1]
        else:
            api_key_short = api_key

        payload = jwt.decode(
            api_key_short,
            get_public_key(),
            algorithms=[ALGORITHM],
            leeway=2,
            options={"verify_aud": False},
        )

        if not payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="token not valid",
            )
        return payload

    except jwt.ExpiredSignatureError as e:
        logger.info(f"Token expired: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
        )
    except jwt.InvalidTokenError as e:
        logger.info(f"Invalid token: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token signature",
        )
