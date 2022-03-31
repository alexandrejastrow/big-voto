from functools import lru_cache
from pydantic import BaseSettings
from dotenv import load_dotenv
load_dotenv()


class AppSettings(BaseSettings):
    app_name: str = ""
    testing: bool = False
    dev_mode: bool = False
    debug: bool = False
    database_url: str = ""
    database_url_dev: str | bool = False

    class config:
        env_file = ".env"


class DbSettings(BaseSettings):
    dev_mode: bool = False
    database_url: str
    database_url_dev: str | bool = False

    class config:
        env_file = ".env"


@lru_cache()
def get_app_config() -> AppSettings:
    return AppSettings()


@lru_cache()
def get_db_config() -> DbSettings:
    return DbSettings()


app_settings = get_app_config()
db_settings = get_db_config()
