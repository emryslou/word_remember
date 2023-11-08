from fastapi.templating import Jinja2Templates
import core.config as config


Templates = Jinja2Templates(directory=config.APP_CONFIG.get("tpl"))
