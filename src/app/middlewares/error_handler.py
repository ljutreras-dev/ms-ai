import traceback
from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from src.context.shared.domain.base_error import BaseError
from src.context.shared.infrastructure.logger.app_logger import AppLogger

logger = AppLogger()


async def base_error_handler(request: Request, exc: BaseError) -> JSONResponse:
    """Handles domain and application layer BaseError exceptions."""
    logger.warning(
        f"Domain Error on {request.method} {request.url.path} - "
        f"Status: {exc.status_code} - Info: {exc.info}"
    )
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.info,
    )


async def validation_error_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """Handles Pydantic input validation failures with 422 Unprocessable Entity."""
    errors = []
    for err in exc.errors():
        field_path = " -> ".join(str(loc) for loc in err.get("loc", []))
        errors.append({
            "field": field_path,
            "message": err.get("msg"),
            "type": err.get("type"),
        })

    logger.warning(f"Validation failure on {request.method} {request.url.path}: {errors}")
    return JSONResponse(
        status_code=422,
        content={"message": "Validation Error", "errors": errors},
    )


async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Catches unhandled server errors, logs complete stack trace and returns 500."""
    stack = traceback.format_exc()
    logger.error(
        f"--------- [REQUEST FAIL]: {request.method} {request.url}\n"
        f"--------- [HEADERS]: {dict(request.headers)}\n"
        f"--------- [ERROR TYPE]: {type(exc).__name__}\n"
        f"--------- [ERROR MESSAGE]: {str(exc)}\n"
        f"--------- [ERROR STACK]:\n{stack}"
    )
    return JSONResponse(
        status_code=500,
        content={"error": "Internal Server Error", "message": "An unexpected error occurred."},
    )
