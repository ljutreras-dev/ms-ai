from typing import Any, Dict, Optional
from src.context.shared.domain.base_error import BaseError


class ResourceNotFoundError(BaseError):
    """Raised when an entity or resource is not found."""

    def __init__(self, message: str = "Resource not found", info: Optional[Dict[str, Any]] = None):
        super().__init__(message=message, status_code=404, info=info or {"error": message})


class InvalidArgumentError(BaseError):
    """Raised when provided arguments or payloads fail domain validation."""

    def __init__(self, message: str = "Invalid argument provided", info: Optional[Dict[str, Any]] = None):
        super().__init__(message=message, status_code=422, info=info or {"error": message})


class DatabaseConnectionError(BaseError):
    """Raised when connection to persistence service (Mongo, Redis) fails."""

    def __init__(self, message: str = "Database connection error", info: Optional[Dict[str, Any]] = None):
        super().__init__(message=message, status_code=503, info=info or {"error": message})
