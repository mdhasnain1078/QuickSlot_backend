import asyncio
from app.database.mongodb import connect_to_mongo, db, close_mongo_connection
from app.core.config import settings

async def main():
    await connect_to_mongo()
    bookings = await db.db.bookings.find().to_list(100)
    print("ALL BOOKINGS:")
    for b in bookings:
        print(b)
    await close_mongo_connection()
    
asyncio.run(main())
