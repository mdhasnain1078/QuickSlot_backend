from typing import List, Optional
from datetime import datetime
from bson import ObjectId
from app.database.mongodb import db
from app.schemas.domain import BookingCreate

class BookingRepository:
    
    async def create_booking(self, booking_data: BookingCreate) -> dict:
        doc = booking_data.model_dump()
        doc["created_at"] = datetime.utcnow()
        # Convert string IDs to ObjectId if needed, but since we are keeping it simple, 
        # we can store them as strings or ObjectIds. Let's store as strings to match PyObjectId mapping easily, 
        # or we just use strings directly for simplicity.
        result = await db.db.bookings.insert_one(doc)
        doc["_id"] = str(result.inserted_id)
        return doc
    
    async def get_user_bookings(self, user_id: str) -> List[dict]:
        cursor = db.db.bookings.find({"user_id": user_id})
        bookings = await cursor.to_list(length=100)
        for b in bookings:
            b["_id"] = str(b["_id"])
        return bookings

    async def delete_booking(self, booking_id: str) -> bool:
        result = await db.db.bookings.delete_one({"_id": ObjectId(booking_id)})
        return result.deleted_count > 0

booking_repository = BookingRepository()
