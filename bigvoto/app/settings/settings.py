from functools import lru_cache
from pydantic import BaseSettings
from dotenv import load_dotenv
load_dotenv()


class AppSettings(BaseSettings):
    APP_NAME: str = ""
    TESTING: bool = False
    DEV_MODE: bool = False
    DEBUG: bool = False
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    DEFAULT_MAX_TIME_TO_POLL: int

    class config:
        env_file = ".env"


class DbSettings(BaseSettings):
    DEV_MODE: bool = False
    DATABASE_URL: str
    DATABASE_URL_DEV: str | bool = False

    class config:
        env_file = ".env"


class RabbitmqSettings(BaseSettings):
    RABBITMQ_USER: str
    RABBITMQ_PASSWORD: str
    RABBITMQ_HOST: str
    RABBITMQ_PORT: int

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


@lru_cache()
def get_rabbit_config() -> RabbitmqSettings:
    return RabbitmqSettings()


app_settings = get_app_config()
db_settings = get_db_config()
mail_settings = get_mail_config()
rabbitmb_settings = get_rabbit_config()
