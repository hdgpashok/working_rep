import asyncio

from sqlalchemy.exc import IntegrityError, DataError, OperationalError
from sqlalchemy.exc import TimeoutError as SATimeoutError
from aiokafka.errors import KafkaConnectionError, KafkaTimeoutError, RequestTimedOutError


TRANSIENT_ERRORS = (
    OperationalError,
    SATimeoutError,
    asyncio.TimeoutError,
    KafkaConnectionError,
    KafkaTimeoutError,
    RequestTimedOutError,
)

NON_RETRYABLE_ERRORS = (
    ValueError,
    KeyError,
    IntegrityError,
    DataError,
)