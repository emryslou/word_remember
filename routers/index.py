from fastapi import APIRouter, Request
from core.templates import Templates
from utils.tools import router_prefix

_router = APIRouter(prefix=router_prefix(__file__), tags=['index'])


@_router.get("/", name='index')
@_router.get("/index", name='index')
async def index(request: Request):
    return Templates.TemplateResponse("index.html", context={"request": request})
