import os

APP_ROOT_DIR = os.getcwd()

APP_DEBUG = True

APP_VERSION = "0.0.1"

APP_CONFIG = {
    "static": f"{APP_ROOT_DIR}/assets/static",
    "tpl": f"{APP_ROOT_DIR}/assets/templates",
}

APP_CSRF = {
    'enable': True,
    'secret': 'ewm_20230418',
}

DB_CONFIG = {
    "uri": f"sqlite:///{APP_ROOT_DIR}/storage/db/eng_words.db",
}
