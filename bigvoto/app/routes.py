from fastapi import APIRouter
from fastapi.responses import RedirectResponse
from app.controllers import user_controller, poll_controller


routes = APIRouter()

routes.include_router(user_controller.user_router, prefix='/api/users')
routes.include_router(poll_controller.poll_router, prefix='/api/polls')


@routes.get("/", response_class=RedirectResponse, include_in_schema=False)
async def home():
    return RedirectResponse(url="/docs", status_code=302)
