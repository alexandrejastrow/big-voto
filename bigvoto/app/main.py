from fastapi import FastAPI
from app.routes import routes
from app import __version__
from app.settings.settings import app_settings

app = FastAPI(
    title=app_settings.app_name,
    version=__version__,
    redoc_url=None
)

app.include_router(routes)
