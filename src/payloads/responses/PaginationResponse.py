from typing import Any


def _pagination_list_payload(
    page: int, page_limit: int, npages: int, nrows: int, data: Any
) -> dict[str, Any]:
    return {
        "page_limit": page_limit,
        "page": page,
        "total_rows": nrows,
        "total_pages": npages,
        "data": data,
    }


def pagination_response(
    status_code: int,
    message: str,
    page: int,
    page_limit: int,
    npages: int,
    nrows: int,
    data: list[Any] | Any,
) -> dict[str, Any]:
    return {
        "status_code": status_code,
        "message": message,
        **_pagination_list_payload(page, page_limit, npages, nrows, data),
    }
