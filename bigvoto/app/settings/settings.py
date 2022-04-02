from functools import lru_cache
from pydantic import BaseSettings
from dotenv import load_dotenv
load_dotenv()


class AppSettings(BaseSettings):
    app_name: str = ""
    testing: bool = False
    dev_mode: bool = False
    debug: bool = False
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int = 120

    class config:
        env_file = ".env"


class DbSettings(BaseSettings):
    dev_mode: bool = False
    database_url: str
    database_url_dev: str | bool = False

    class config:
        env_file = ".env"


class MailSettings(BaseSettings):
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_PORT: int
    MAIL_SERVER: str
    MAIL_TLS: bool = True
    MAIL_SSL: bool = False
    MAIL_USE_CREDENTIALS: bool = True
    MAIL_VALIDATE_CERTS: bool = True
    MAIL_HOST_DEV: str
    MAIL_HOST_PROD: str

    class config:
        env_file = ".env"


@lru_cache()
def get_app_config() -> AppSettings:
    return AppSettings()


@lru_cache()
def get_db_config() -> DbSettings:
    return DbSettings()


@lru_cache()
def get_mail_config() -> MailSettings:
    return MailSettings()


app_settings = get_app_config()
db_settings = get_db_config()
mail_settings = get_mail_config()
