from fastapi import FastAPI

from api import users, hotels, bookings


app = FastAPI(
    title="Hotel Room Reservation Fast API",
    description="A Website For Managing Hotel Room Reservations.",
    version="0.0.1",
    contact={
        "name": "Nouri Muhammad",
        "email": "nouri.muhammad1991@gmail.com",
    }
)


app.include_router(users.router)
app.include_router(hotels.router)
app.include_router(bookings.router)

@app.get("/")
async def root():
    return {"msg": "We provide you with a hotel room for your trip."}
