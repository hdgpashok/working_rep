from functools import wraps
from typing import Callable

from src.utils.logger import get_logger
from src.utils.timeout import timeout_with_jitter
from src.exceptions.timeout_error import ServerTimeoutError

from config.config import settings

from starlette.status import (
    HTTP_500_INTERNAL_SERVER_ERROR,
    HTTP_502_BAD_GATEWAY,
    HTTP_503_SERVICE_UNAVAILABLE,
    HTTP_504_GATEWAY_TIMEOUT,
    HTTP_429_TOO_MANY_REQUESTS
)


logger = get_logger('retry_logger')


RETRY_STATUSES = [
    HTTP_500_INTERNAL_SERVER_ERROR,
    HTTP_502_BAD_GATEWAY,
    HTTP_503_SERVICE_UNAVAILABLE,
    HTTP_504_GATEWAY_TIMEOUT,
    HTTP_429_TOO_MANY_REQUESTS
]


def retry(max_retries: int = settings.MAX_RETIES):

    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return await func(*args, **kwargs)

                except Exception as exc:
                    logger.warning(
                        f"[RETRY] Attempt {attempt + 1}/{max_retries} failed "
                        f"with {type(exc).__name__}. Retrying..."
                        f"{exc}"
                    )
                    if attempt == max_retries - 1:
                        break
                    await timeout_with_jitter(attempt)

            logger.error(f"[RETRY] All {max_retries} attempts failed")
            raise ServerTimeoutError(message='server timeout')

        return wrapper

    return decorator