from typing import List
from app.schemas.domain import BookingCreate
from app.repositories.slot_repository import slot_repository
from app.repositories.booking_repository import booking_repository
from app.core.exceptions import ConflictException, NotFoundException

class BookingService:
    async def get_user_bookings(self, user_id: str) -> List[dict]:
        return await booking_repository.get_user_bookings(user_id)

    async def create_booking(self, booking_data: BookingCreate) -> dict:
        # Check if slot exists
        slot = await slot_repository.get_slot(booking_data.slot_id)
        if not slot:
            raise NotFoundException("Slot not found")
        
        if slot["venue_id"] != booking_data.venue_id or slot["date"] != booking_data.date:
            raise ConflictException("Slot mismatch with venue or date")
            
        if slot["status"] != "available":
            raise ConflictException("Slot already booked")

        # ATOMIC OPERATION
        # Try to update the slot status from 'available' to 'booked'
        # If another request successfully booked this slot a millisecond ago,
        # the status would now be 'booked', and this update will modify 0 documents.
        is_booked = await slot_repository.book_slot_atomic(booking_data.slot_id)
        
        if not is_booked:
            raise ConflictException("Slot already booked")
            
        # If we successfully locked the slot, create the booking record
        try:
            booking = await booking_repository.create_booking(booking_data)
            return booking
        except Exception as e:
            # Compensating transaction if booking creation fails for some reason
            await slot_repository.release_slot(booking_data.slot_id)
            raise e

    async def cancel_booking(self, booking_id: str) -> bool:
        from bson import ObjectId
        from app.database.mongodb import db
        booking = await db.db.bookings.find_one({"_id": ObjectId(booking_id)})
        if not booking:
            return False
        await slot_repository.release_slot(booking["slot_id"])
        return await booking_repository.delete_booking(booking_id)

booking_service = BookingService()
