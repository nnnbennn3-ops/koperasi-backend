import logging
import requests
from src.configs.config import settings

logger = logging.getLogger(__name__)
DEFAULT_TIMEOUT = 10.0


def _normalize_url(base_url: str, endpoint: str) -> str:
    """Build and normalize URL by collapsing duplicate slashes while preserving ://."""
    if not endpoint.startswith("v1/") and not endpoint.startswith("/v1/"):
        endpoint = f"v1/{endpoint.lstrip('/')}"
    raw = f"{base_url.rstrip('/')}/{endpoint.lstrip('/')}"
    return raw.replace("://", "TEMP").replace("//", "/").replace("TEMP", "://")


class APIEndpoint:
    def __init__(
        self,
        base_url: str,
        endpoint: str,
        debug: bool = False,
        timeout: float = DEFAULT_TIMEOUT,
    ):
        self.url = _normalize_url(base_url, endpoint)
        self.debug = debug
        self.timeout = timeout

    def __call__(
        self,
        fields: list[str] | None = None,
        headers: dict | str | None = None,
        params: dict | None = None,
    ):
        req_headers = {}
        if isinstance(headers, str):
            req_headers["Authorization"] = headers
        elif isinstance(headers, dict):
            req_headers.update(headers)

        try:
            response = requests.get(
                self.url, headers=req_headers, params=params, timeout=self.timeout
            )
            if response.status_code != 200:
                return {
                    "error": f"HTTP {response.status_code}",
                    "message": response.text,
                }

            payload = response.json()
            data = payload.get("data")
            if data is None:
                return {"error": "Empty data"}

            if fields and isinstance(data, dict):
                return {f: data.get(f) for f in fields}
            if fields and isinstance(data, list):
                return [
                    {f: item.get(f) for f in fields}
                    for item in data
                    if isinstance(item, dict)
                ]
            return data
        except Exception as err:
            return {"error": str(err)}


class _ServiceRef:
    def __init__(
        self, base_url: str, debug: bool = False, timeout: float = DEFAULT_TIMEOUT
    ):
        self._base_url = base_url
        self._debug = debug
        self._timeout = timeout

    def __getattr__(self, endpoint: str) -> APIEndpoint:
        if endpoint.startswith("_"):
            raise AttributeError(endpoint)
        return self[endpoint]

    def __getitem__(self, endpoint: str) -> APIEndpoint:
        return APIEndpoint(
            self._base_url, endpoint, debug=self._debug, timeout=self._timeout
        )


class ServiceClient:
    """Lookup service base URLs from settings (general, user, finance)."""

    _ALIAS_MAP = {
        "general": "general_service_url",
        "user": "user_service_url",
        "finance": "finance_service_url",
    }

    def __init__(self, debug: bool = False, timeout: float = DEFAULT_TIMEOUT):
        self.debug = debug
        self.timeout = timeout

    def __getattr__(self, name: str) -> _ServiceRef:
        if name.startswith("_"):
            raise AttributeError(name)
        attr_name = self._ALIAS_MAP.get(name, name)
        base_url = getattr(settings, attr_name, None)
        if not base_url:
            raise AttributeError(f"Service tidak ditemukan: {name}")
        return _ServiceRef(base_url, debug=self.debug, timeout=self.timeout)
