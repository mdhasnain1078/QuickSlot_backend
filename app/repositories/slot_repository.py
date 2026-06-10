from typing import List, Optional
from bson import ObjectId
from app.database.mongodb import db

class SlotRepository:
    
    async def get_venue_slots(self, venue_id: str, date: str) -> List[dict]:
        cursor = db.db.slots.find({"venue_id": venue_id, "date": date})
        slots = await cursor.to_list(length=100)
        for s in slots:
            s["_id"] = str(s["_id"])
        return slots

    async def get_slot(self, slot_id: str) -> Optional[dict]:
        slot = await db.db.slots.find_one({"_id": ObjectId(slot_id)})
        if slot:
            slot["_id"] = str(slot["_id"])
        return slot

    async def book_slot_atomic(self, slot_id: str) -> bool:
        """
        ATOMIC OPERATION to prevent double booking.
        Finds the slot only if it is 'available'.
        Updates it to 'booked'.
        If it was already 'booked', modified_count will be 0.
        """
        result = await db.db.slots.update_one(
            {"_id": ObjectId(slot_id), "status": "available"},
            {"$set": {"status": "booked"}}
        )
        return result.modified_count > 0

    async def release_slot(self, slot_id: str) -> bool:
        result = await db.db.slots.update_one(
            {"_id": ObjectId(slot_id)},
            {"$set": {"status": "available"}}
        )
        return result.modified_count > 0

slot_repository = SlotRepository()
