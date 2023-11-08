import utils
from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException, RequestValidationError, StarletteHTTPException
from fastapi import FastAPI
from core.constants import logger
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_ipaddr


def app_event_handler(app: FastAPI):
    logger.info('app event handler ...')
    
    @app.on_event('startup')
    async def start_up():
        logger.debug('ewm start ....')
    
    @app.on_event('shutdown')
    async def shutdown():
        logger.debug('ewm stopped ...')
    
    @app.exception_handler(HTTPException)
    async def exception_he_handler(req: Request, exc: HTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content=utils.response.fail(exc.status_code, f"Oops! some error happend")
        )
    
    @app.exception_handler(RequestValidationError)
    async def exception_rve_handler(req: Request, exc: RequestValidationError):
        return JSONResponse(
            status_code=499,
            content=utils.response.response(499, exc.errors())
        )

    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request, exc: StarletteHTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content=utils.response.fail(exc.status_code, exc.detail)
        )
    
    app.state.limiter = Limiter(key_func=get_ipaddr, default_limits=['10/second'])
    
    @app.exception_handler(RateLimitExceeded)
    async def rate_limit_handler(req, exc: RateLimitExceeded):
        logger.debug('rate limit handler ...')
        return _rate_limit_exceeded_handler(req, exc)
