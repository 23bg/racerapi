from typing import Any


def success_response(data: Any, message: str = "ok") -> dict[str, Any]:
    return {
        "status": "success",
        "message": message,
        "data": data,
    }
