import logging
from typing import Any

logger = logging.getLogger(__name__)


def safe_fetch_field(
    caller: Any,
    endpoint: str,
    field: str,
    headers: dict | None = None,
    default: Any = "",
    log_context: str | None = None,
) -> Any:
    try:
        data = (
            caller[endpoint]([field], headers=headers)
            if headers
            else caller[endpoint]([field])
        )
        if data is None:
            return default

        if isinstance(data, dict):
            if "error" in data:
                logger.warning(
                    "Error response from '%s' while fetching field '%s'%s: %s",
                    endpoint,
                    field,
                    f" [{log_context}]" if log_context else "",
                    data.get("error") or data.get("message"),
                )
                return default
            val = data.get(field)
            return val if val is not None else default

        if isinstance(data, list) and data:
            first = data[0]
            if isinstance(first, dict):
                if "error" in first:
                    logger.warning(
                        "Error in list response from '%s' while fetching field '%s'%s: %s",
                        endpoint,
                        field,
                        f" [{log_context}]" if log_context else "",
                        first.get("error") or first.get("message"),
                    )
                    return default
                val = first.get(field)
                return val if val is not None else default

            return default
    except Exception as err:
        logger.warning(
            "Exception fetching field '%s' from endpoint: '%s'%s: %s",
            field,
            endpoint,
            f" [{log_context}]" if log_context else "",
            err,
        )
        return default


def safe_fetch_dict(
    caller: Any,
    endpoint: str,
    fields: list[str] | None = None,
    headers: dict | None = None,
    log_context: str | None = None,
) -> dict[str, Any] | None:
    try:
        data = (
            caller[endpoint](fields, headers=headers)
            if fields
            else (caller[endpoint](headers=headers) if headers else caller[endpoint]())
        )
        if data is None:
            return None

        if isinstance(data, dict):
            if "error" in data:
                logger.warning(
                    "Error response from endpoint '%s'%s: %s",
                    endpoint,
                    f" [{log_context}]" if log_context else "",
                    data.get("error") or data.get("message"),
                )
                return None
            return data

        if isinstance(data, list) and data:
            first = data[0]
            if isinstance(first, dict):
                if "error" in first:
                    logger.warning(
                        "Error in list response from endpoint: '%s'%s: %s",
                        endpoint,
                        f" [{log_context}]" if log_context else "",
                        first.get("error") or first.get("message"),
                    )
                    return None
                return first

            return None
    except Exception as err:
        logger.warning(
            "Exception fetching dict from endpoint: '%s'%s: %s",
            endpoint,
            f" [{log_context}]" if log_context else "",
            err,
        )
        return None


def safe_fetch_list(
    caller: Any,
    endpoint: str,
    fields: list[str] | None = None,
    headers: dict | None = None,
    log_context: str | None = None,
) -> list[dict[str, Any]]:
    try:
        data = (
            caller[endpoint](fields, headers=headers)
            if fields
            else (caller[endpoint](headers=headers) if headers else caller[endpoint]())
        )
        if data is None:
            return []

        if isinstance(data, dict):
            if "error" in data:
                logger.warning(
                    "Error response from endpoint '%s'%s: %s",
                    endpoint,
                    f" [{log_context}]" if log_context else "",
                    data.get("error") or data.get("message"),
                )
                return []
            return [data]

        if isinstance(data, list):
            if data and isinstance(data[0], dict) and "error" in data[0]:
                logger.warning(
                    "Error in list response from endpoint '%s'%s: %s",
                    endpoint,
                    f" [{log_context}]" if log_context else "",
                    data[0].get("error") or data[0].get("message"),
                )
                return []
            return [item for item in data if isinstance(item, dict)]

        return []
    except Exception as err:
        logger.warning(
            "Exception fetching list from endpoint '%s'%s: %s",
            endpoint,
            f" [{log_context}]" if log_context else "",
            err,
        )
        return []
