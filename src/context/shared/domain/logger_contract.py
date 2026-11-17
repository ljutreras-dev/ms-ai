from abc import ABC, abstractmethod
from typing import Any


class LoggerContract(ABC):
    """Abstract interface defining the logging contract across bounded contexts."""

    @abstractmethod
    def info(self, message: str, *args: Any, **kwargs: Any) -> None:
        pass

    @abstractmethod
    def debug(self, message: str, *args: Any, **kwargs: Any) -> None:
        pass

    @abstractmethod
    def warning(self, message: str, *args: Any, **kwargs: Any) -> None:
        pass

    @abstractmethod
    def error(self, message: str, *args: Any, **kwargs: Any) -> None:
        pass

    @abstractmethod
    def critical(self, message: str, *args: Any, **kwargs: Any) -> None:
        pass
