from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from app.routes.user_router import router as user_routes
from app import __version__
from app.settings.settings import app_settings

app = FastAPI(
    title=app_settings.app_name,
    version=__version__,
    redoc_url=None
)

app.include_router(user_routes, prefix="/api")


@app.get("/", response_class=RedirectResponse, include_in_schema=False)
async def home():
    return RedirectResponse(url="/docs", status_code=302)