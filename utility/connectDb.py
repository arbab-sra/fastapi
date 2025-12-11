import motor.motor_asyncio
from beanie import init_beanie
from model.usermodle import User
import sys ,os
from dotenv import load_dotenv
load_dotenv()

DATABASE_URL = os.getenv("DB_URL") or os.environ["DB_URL"] or "mongodb://root:example@localhost:27017/" # Replace with your connection string
client = motor.motor_asyncio.AsyncIOMotorClient(DATABASE_URL)

async def init_db():
    try:
        connt = await init_beanie(database=client["arbabsra"], document_models=[User])
        if connt:
            print("Database initialized")
        else:
            print("Database not initialized")
            
    except Exception as e:
        print(f"Error to connect to db: {e}")
       