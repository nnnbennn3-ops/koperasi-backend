from typing import Any


def payload_response(status_code: int, message: str, data: Any = None) -> dict:
    return {"status_code": status_code, "message": message, "data": data}
