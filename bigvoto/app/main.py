from fastapi import FastAPI
from app.settings import settings

app = FastAPI()


@app.get("/")
async def home():
    return {"message": "this is the home page"}
