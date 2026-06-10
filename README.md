# QuickSlot Backend

QuickSlot is a blazing-fast, modern backend service for a sports venue booking application. It provides robust REST APIs for managing venues, viewing available time slots, handling user bookings with atomic concurrency control, and securely interacting with a MongoDB database.

This backend is built using **FastAPI** for high performance, **Motor** (AsyncIO MongoDB driver) for non-blocking database operations, and **Pydantic v2** for strict data validation.

## 🚀 Live Demo
The backend is deployed and currently live on Render at:
**[https://quickslot-backend-g4ed.onrender.com](https://quickslot-backend-g4ed.onrender.com)**

You can view the interactive API documentation by visiting:
- **Swagger UI:** [https://quickslot-backend-g4ed.onrender.com/docs](https://quickslot-backend-g4ed.onrender.com/docs)
- **ReDoc:** [https://quickslot-backend-g4ed.onrender.com/redoc](https://quickslot-backend-g4ed.onrender.com/redoc)

## 🛠️ Technology Stack
- **Framework:** FastAPI (Python 3.10+)
- **Database:** MongoDB (Atlas Cloud)
- **Database Driver:** Motor (AsyncIO MongoDB)
- **Data Validation:** Pydantic v2
- **Deployment:** Render (Docker)

## 📂 Project Structure
```text
backend/
├── app/
│   ├── api/             # API Router definitions (Venues, Bookings, Users)
│   ├── core/            # Configuration and global exception handlers
│   ├── database/        # MongoDB connection management
│   ├── repositories/    # Database interaction logic (CRUD operations)
│   ├── schemas/         # Pydantic models for request/response validation
│   ├── services/        # Business logic and atomic operations
│   └── main.py          # FastAPI application entry point
├── Dockerfile           # Docker configuration for Render deployment
├── requirements.txt     # Python dependencies
├── seed.py              # Script to populate the database with initial venue data
└── .env                 # Environment variables configuration
```

## ✨ Key Features
- **Atomic Slot Booking:** Utilizes MongoDB's atomic `update_one` with strict status filtering to prevent double-booking race conditions natively.
- **Asynchronous Architecture:** Fully async from the API routes down to the database operations, ensuring maximum throughput.
- **Automatic Seeding:** The application checks and automatically populates initial venue dummy data on the first run.
- **Cross-Origin Resource Sharing (CORS):** Fully configured to accept requests from the Flutter frontend.
- **Friendly Root Route:** Custom health-check and root endpoints for easy monitoring.

## 💻 Local Development

### 1. Prerequisites
- Python 3.10 or higher
- A MongoDB cluster (Atlas or local)

### 2. Setup Environment
Clone the repository and create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

Install the dependencies:
```bash
pip install -r requirements.txt
```

### 3. Environment Variables
Create a `.env` file in the root `backend/` directory:
```env
PROJECT_NAME="QuickSlot API"
MONGO_URI="mongodb+srv://<your_user>:<your_password>@<your_cluster_url>/"
MONGO_DB="quickslot"
```

### 4. Run the Server
Start the FastAPI application using Uvicorn:
```bash
uvicorn app.main:app --reload
```
The server will start at `http://127.0.0.1:8000`. 
On startup, it will automatically connect to MongoDB and run the seed script to ensure initial venues exist.

## 📋 API Endpoints Summary

### Venues
- `GET /api/v1/venues/` - Retrieve a list of all available venues
- `GET /api/v1/venues/{venue_id}/slots?date=YYYY-MM-DD` - Retrieve available slots for a specific venue on a specific date

### Bookings
- `POST /api/v1/bookings/` - Book a slot (requires `user_id`, `venue_id`, `slot_id`, `date`)
- `DELETE /api/v1/bookings/{booking_id}` - Cancel a booking and release the slot back to the public

### Users
- `GET /api/v1/users/{user_id}/bookings` - Retrieve all active bookings for a specific user

---
*Built for the Swadesh AI Hackathon.*
