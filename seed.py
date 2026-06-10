import asyncio
import datetime
from app.database.mongodb import db, connect_to_mongo, close_mongo_connection
# pyrefly: ignore [missing-import]
from bson import ObjectId

async def seed_data():
    # Check if venues already exist
    count = await db.db.venues.count_documents({})
    if count > 0:
        print("Database already seeded with venues!")
        return

    print("Seeding venues...")
    venues = [
        {
            "name": "Smashers Badminton Arena",
            "image": "https://images.unsplash.com/photo-1626224583764-f87db24ac4ea?auto=format&fit=crop&q=80&w=800",
            "sport_type": "Badminton",
            "location": "Downtown Sports Complex",
            "rating": 4.8
        },
        {
            "name": "Greenfield Football Turf",
            "image": "https://images.unsplash.com/photo-1459865264687-595d652de67e?auto=format&fit=crop&q=80&w=800",
            "sport_type": "Football",
            "location": "Northside Avenue",
            "rating": 4.5
        },
        {
            "name": "Strikers Cricket Nets",
            "image": "https://images.unsplash.com/photo-1531415074968-036ba1b575da?auto=format&fit=crop&q=80&w=800",
            "sport_type": "Cricket",
            "location": "East End Ground",
            "rating": 4.2
        }
    ]

    inserted_venues = await db.db.venues.insert_many(venues)
    venue_ids = inserted_venues.inserted_ids

    print("Seeding slots for the next 7 days...")
    slots = []
    
    today = datetime.date.today()
    
    for i in range(7):
        current_date = today + datetime.timedelta(days=i)
        date_str = current_date.strftime("%Y-%m-%d")
        
        for venue_id in venue_ids:
            # Create slots from 17:00 to 22:00
            for hour in range(17, 23):
                slots.append({
                    "venue_id": str(venue_id),
                    "date": date_str,
                    "time": f"{hour}:00",
                    "status": "available"
                })

    await db.db.slots.insert_many(slots)
    
    print("Seeding complete! Added venues and slots.")

if __name__ == "__main__":
    async def run_seed():
        await connect_to_mongo()
        await seed_data()
        await close_mongo_connection()
    asyncio.run(run_seed())
