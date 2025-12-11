from fastapi import FastAPI
import sys
from routes.auth import router as auth_router
from utility.connectDb import init_db
app = FastAPI()
@app.on_event("startup")
async def app_init():
    await init_db()
    print("connect to db is successfully 😍 ")
app.include_router(auth_router) 

# /docs or /redoc