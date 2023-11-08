"""样例
"""
from fastapi import APIRouter

import utils.response
from utils.tools import router_prefix
from fastapi import Request, Response
from core.constants import limiter

_router = APIRouter(prefix=router_prefix(__file__))


@_router.get('/limit')
@limiter.limit('1/second')
async def alimit(request: Request, response: Response, a):
    return utils.response.success(data={'a': a, 'headers': request.headers})


@_router.get('/limit1')
async def limit(request: Request):
    return {'headers': request.headers}


@_router.post('/csrf')
async def csrf():
    return {}
