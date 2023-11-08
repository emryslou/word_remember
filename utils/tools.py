import importlib
import os
from glob import glob
from typing import Callable

from fastapi import APIRouter

from core.config import APP_ROOT_DIR
from core.constants import logger, limiter


def find_routers(dir_name='.', router_name='apiRouter') -> list[APIRouter]:
    _routers = []
    routers_prefix = dir_name.replace(APP_ROOT_DIR, '').strip('/').replace('/', '.')
    module_names = [
        '{}.{}'.format(routers_prefix, file.replace('.py', '').replace('/', '.'))
        for file in glob('**/*.py', root_dir=dir_name, recursive=True)
        if not file.endswith('__init__.py')
    ]
    
    logger.debug(f'module name list: {module_names}')
    for mn in module_names:
        module = importlib.import_module(mn)
        if router_name in module.__dir__():
            _routers.append(getattr(module, router_name))
        else:
            logger.warning(f'cannot found router【{router_name}】in【{module.__package__}:{mn}】')
    
    return _routers


def router_prefix(file_name: str):
    cfg_replace = {
        APP_ROOT_DIR: '',
        '/routers': '',
        '.py': '',
        '/index': '',
    }
    
    prefix = file_name
    for _s, _r in cfg_replace.items():
        prefix = prefix.replace(_s, _r)
        
    return prefix
