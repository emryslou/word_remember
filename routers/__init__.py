from utils.tools import find_routers
import os

__all__ = [
    'routers',
]

routers = find_routers(os.path.dirname(__file__), '_router')
