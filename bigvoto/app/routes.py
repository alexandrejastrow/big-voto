from fastapi import APIRouter
from app.controllers import user_controller


routes = APIRouter()

routes.include_router(user_controller.router, prefix='/users')
