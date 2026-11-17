from typing import Any, Dict, Optional


class BaseError(Exception):
    """
    Base domain error for application and domain layer exceptions.
    Mirrors the BaseError pattern from the Node.js Clean Architecture template.
    """

    def __init__(
        self,
        message: str,
        status_code: int = 400,
        info: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.info = info or {"error": message}

    def to_dict(self) -> Dict[str, Any]:
        return {
            "status_code": self.status_code,
            "message": self.message,
            "info": self.info,
        }
