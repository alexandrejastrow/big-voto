from fastapi import FastAPI
from app import __version__
from app.routes import routes
from app.settings.settings import app_settings

app = FastAPI(
    title=app_settings.APP_NAME,
    version=__version__,
    redoc_url=None
)

app.include_router(routes)
