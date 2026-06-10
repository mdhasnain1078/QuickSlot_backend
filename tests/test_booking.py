import asyncio
import pytest
from httpx import AsyncClient
from app.main import app
from app.database.mongodb import db

@pytest.fixture(autouse=True)
async def setup_db():
    await db.db.slots.insert_one({
        "_id": "slot1",
        "venue_id": "venue1",
        "date": "2023-12-01",
        "time": "18:00",
        "status": "available"
    })
    yield
    await db.db.slots.delete_many({})
    await db.db.bookings.delete_many({})

@pytest.mark.asyncio
async def test_concurrent_bookings():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        
        # Simulate 5 concurrent users trying to book the exact same slot
        async def try_book(user_id):
            return await ac.post("/api/v1/bookings/", json={
                "user_id": user_id,
                "venue_id": "venue1",
                "slot_id": "slot1",
                "date": "2023-12-01"
            })
            
        tasks = [try_book(f"user{i}") for i in range(5)]
        responses = await asyncio.gather(*tasks)
        
        success_count = sum(1 for r in responses if r.status_code == 200 and r.json()["success"])
        conflict_count = sum(1 for r in responses if r.status_code == 409)
        
        assert success_count == 1
        assert conflict_count == 4
