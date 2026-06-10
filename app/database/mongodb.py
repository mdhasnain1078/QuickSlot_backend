# pyrefly: ignore [missing-import]
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from app.core.config import settings
# pyrefly: ignore [missing-import]
import certifi

class MongoDB:
    client: AsyncIOMotorClient = None
    db: AsyncIOMotorDatabase = None

db = MongoDB()

async def connect_to_mongo():
    db.client = AsyncIOMotorClient(settings.MONGO_URI, tlsCAFile=certifi.where())
    db.db = db.client[settings.MONGO_DB]
    print("Connected to MongoDB")
    
    # Ensure indexes
    await db.db.slots.create_index([("date", 1), ("venue_id", 1)])
    await db.db.bookings.create_index([("user_id", 1)])

async def close_mongo_connection():
    if db.client:
        db.client.close()
        print("Closed MongoDB connection")
