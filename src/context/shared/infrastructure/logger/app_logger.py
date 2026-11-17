import sys
from typing import Any
from src.context.shared.domain.logger_contract import LoggerContract

try:
    from loguru import logger as _loguru_logger

    class AppLogger(LoggerContract):
        def __init__(self) -> None:
            _loguru_logger.remove()
            _loguru_logger.add(
                sys.stdout,
                colorize=True,
                format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
                level="INFO",
            )
            self._logger = _loguru_logger

        def info(self, message: str, *args: Any, **kwargs: Any) -> None:
            self._logger.info(message, *args, **kwargs)

        def debug(self, message: str, *args: Any, **kwargs: Any) -> None:
            self._logger.debug(message, *args, **kwargs)

        def warning(self, message: str, *args: Any, **kwargs: Any) -> None:
            self._logger.warning(message, *args, **kwargs)

        def error(self, message: str, *args: Any, **kwargs: Any) -> None:
            self._logger.error(message, *args, **kwargs)

        def critical(self, message: str, *args: Any, **kwargs: Any) -> None:
            self._logger.critical(message, *args, **kwargs)

except ImportError:
    import logging

    class AppLogger(LoggerContract):  # type: ignore[no-redef]
        def __init__(self) -> None:
            logging.basicConfig(
                level=logging.INFO,
                format="%(asctime)s | %(levelname)-8s | %(name)s:%(lineno)d - %(message)s",
                handlers=[logging.StreamHandler(sys.stdout)],
            )
            self._logger = logging.getLogger("backend_template")

        def info(self, message: str, *args: Any, **kwargs: Any) -> None:
            self._logger.info(message, *args, **kwargs)

        def debug(self, message: str, *args: Any, **kwargs: Any) -> None:
            self._logger.debug(message, *args, **kwargs)

        def warning(self, message: str, *args: Any, **kwargs: Any) -> None:
            self._logger.warning(message, *args, **kwargs)

        def error(self, message: str, *args: Any, **kwargs: Any) -> None:
            self._logger.error(message, *args, **kwargs)

        def critical(self, message: str, *args: Any, **kwargs: Any) -> None:
            self._logger.critical(message, *args, **kwargs)
