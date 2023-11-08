import enum
import logging
from slowapi import Limiter
from slowapi.util import get_ipaddr

logger = logging.getLogger('uvicorn.error')

limiter = Limiter(key_func=get_ipaddr, default_limits=['10/second'], headers_enabled=True)


class ApiResponseCode(enum.Enum):
    SUCCESS = 0  # success
    SYSTEM_ERROR = 1
    DB_ERROR = 100
    APP_ERROR = 200
    