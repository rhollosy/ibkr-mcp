import logging
import time
from functools import wraps
from typing import Any

from ibkr.exceptions import IBKRError

logger = logging.getLogger(__name__)


def warn_if_slow(threshold: float = 2.0):
    """Decorator to append a warning if the decorated function is slow."""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs) -> Any:
            start_time = time.perf_counter()
            result = await func(*args, **kwargs)
            duration = time.perf_counter() - start_time
            if duration > threshold:
                warning = (
                    f"\nWARNING: Request took {duration:.2f}s "
                    f"(target: < {threshold}s)"
                )
                if isinstance(result, str):
                    return result + warning
            return result
        return wrapper
    return decorator

def catch_errors():
    """T009b: Global error handling decorator for MCP tools."""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs) -> Any:
            try:
                return await func(*args, **kwargs)
            except IBKRError as e:
                logger.error("IBKRError in %s: %s", func.__name__, e)
                return f"Error: {e}"
            except Exception as e:
                logger.exception("Unexpected error in %s", func.__name__)
                return f"Unexpected Error: {e}"
        return wrapper
    return decorator
