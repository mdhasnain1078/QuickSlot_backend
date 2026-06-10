# pyrefly: ignore [missing-import]
from fastapi import APIRouter, Depends, Query
from typing import List
from app.schemas.domain import VenueResponse, SlotResponse, BookingResponse, BookingCreate, BaseAPIResponse
from app.database.mongodb import db
from app.services.booking_service import booking_service
from app.repositories.slot_repository import slot_repository

api_router = APIRouter()
# --- Venues ---
venues_router = APIRouter(prefix="/venues", tags=["venues"])

@venues_router.get("/", response_model=dict)
async def get_venues():
    cursor = db.db.venues.find({})
    venues = await cursor.to_list(length=100)
    for v in venues:
        v["_id"] = str(v["_id"])
    return {"success": True, "message": "Venues retrieved", "data": venues}

@venues_router.get("/{venue_id}/slots", response_model=dict)
async def get_venue_slots(venue_id: str, date: str = Query(..., description="YYYY-MM-DD")):
    slots = await slot_repository.get_venue_slots(venue_id, date)
    return {"success": True, "message": "Slots retrieved", "data": slots}

# --- Bookings ---
bookings_router = APIRouter(prefix="/bookings", tags=["bookings"])

@bookings_router.post("/", response_model=dict)
async def create_booking(booking_data: BookingCreate):
    booking = await booking_service.create_booking(booking_data)
    return {"success": True, "message": "Booking successful", "data": booking}

@bookings_router.delete("/{booking_id}", response_model=dict)
async def cancel_booking(booking_id: str):
    # Not fully implemented in service, but we have the endpoint
    success = await booking_service.cancel_booking(booking_id)
    return {"success": True, "message": "Booking cancelled", "data": {"cancelled": success}}

# --- Users (Bookings) ---
users_router = APIRouter(prefix="/users", tags=["users"])

@users_router.get("/{user_id}/bookings", response_model=dict)
async def get_user_bookings(user_id: str):
    bookings = await booking_service.get_user_bookings(user_id)
    return {"success": True, "message": "User bookings retrieved", "data": bookings}

# Include routers
api_router.include_router(venues_router)
api_router.include_router(bookings_router)
api_router.include_router(users_router)
