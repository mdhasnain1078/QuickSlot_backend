from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime

class PyObjectId(str):
    @classmethod
    def __get_pydantic_core_schema__(cls, _source_type, _handler):
        from pydantic_core import core_schema
        return core_schema.str_schema()

# --- User ---
class UserBase(BaseModel):
    name: str

class UserCreate(UserBase):
    pass

class UserResponse(UserBase):
    id: PyObjectId = Field(alias="_id")
    model_config = ConfigDict(populate_by_name=True)

# --- Venue ---
class VenueBase(BaseModel):
    name: str
    image: str
    sport_type: str
    location: str
    rating: float

class VenueResponse(VenueBase):
    id: PyObjectId = Field(alias="_id")
    model_config = ConfigDict(populate_by_name=True)

# --- Slot ---
class SlotBase(BaseModel):
    venue_id: PyObjectId
    date: str # YYYY-MM-DD
    time: str # HH:MM
    status: str = "available" # 'available', 'booked'

class SlotCreate(SlotBase):
    pass

class SlotResponse(SlotBase):
    id: PyObjectId = Field(alias="_id")
    model_config = ConfigDict(populate_by_name=True)

# --- Booking ---
class BookingBase(BaseModel):
    user_id: PyObjectId
    venue_id: PyObjectId
    slot_id: PyObjectId
    date: str # YYYY-MM-DD

class BookingCreate(BookingBase):
    pass

class BookingResponse(BookingBase):
    id: PyObjectId = Field(alias="_id")
    created_at: datetime
    model_config = ConfigDict(populate_by_name=True)

# --- Common Responses ---
class BaseAPIResponse(BaseModel):
    success: bool
    message: str
    errors: list = []
