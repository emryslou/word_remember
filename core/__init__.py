from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette_csrf import CSRFMiddleware
from routers import routers as app_routers
import core.config as config
from core.event_handle import app_event_handler
from core.database import DataBaseModel, engine, Session, get_db
from core.constants import logger


__all__ = [
    'EwmApp',
    'Session',
    'get_db',
    'templates',
]


class EwmApp(object):
    """
    global app
    """

    instance = None
    config = None

    def __init__(self) -> None:
        self.config = config
        self.instance = FastAPI()
        self.templates = None

    def start(self):
        """
        server init
        """
        self.app_init()
        self.mount_static()
        self.mount_routers()
        
        return self
    
    def app_init(self):
        DataBaseModel.metadata.create_all(bind=engine)
        if self.config.APP_CSRF['enable']:
            self.app_csrf()
        app_event_handler(self.instance)
    
    def app_csrf(self):
        logger.info('csrf starting ....')
        self.instance.add_middleware(
            CSRFMiddleware,
            **dict(
                secret=self.config.APP_CSRF['secret'],
                safe_methods={ "HEAD", "OPTIONS", "TRACE"},
                cookie_name='ewm-csrf-token',
            )
        )
        
    def mount_static(self):
        """mount_static"""
        staticConfig = self.config.APP_CONFIG.get("static")
        self.instance.mount(
            "/static", StaticFiles(directory=staticConfig), name="static"
        )

    def mount_routers(self):
        """mount_routers"""
        for router in app_routers:
            for rs in router.routes:
                logger.debug(f'end points: {rs.endpoint.__module__}:{rs.endpoint.__name__} '
                             f'[methods: {",".join(rs.methods)}; path: {rs.path}] mounted')
            self.instance.include_router(router)

    @property
    def app(self):
        """app"""
        return self.instance
