from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from contextlib import asynccontextmanager
from beanie import init_beanie
import os

from simplecrudapi.routers import profile, user
from simplecrudapi.odm_schemas import Profile

@asynccontextmanager
async def db_lifespan(app: FastAPI):
    mongodb_url = os.getenv("MONGODB_URL")
    app.mongodb_client = AsyncIOMotorClient(mongodb_url)
    app.db = app.mongodb_client.get_database("college")
    ping_response = await app.db.command("ping")
    if int(ping_response["ok"]) != 1:
        raise Exception("Problem while connecting to database")
    print("Connected MongoDB")
    await init_beanie(database=app.db, document_models=[Profile])
    yield
    
    # when application shutting down
    app.mongodb_client.close()
    print("Disconnected MongoDB")

app = FastAPI(lifespan=db_lifespan)
@app.get("/")
def root():
    return {"message": "Simple CRUD with mongoDB"}

app.include_router(user.router)
app.include_router(profile.router)