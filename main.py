from fastapi import FastAPI

from db.db_setup import engine, session_local


app = FastAPI(
    title="Hotel Room Reservation Fast API",
    description="A Website For Managing Hotel Room Reservations.",
    version="0.0.1",
    contact={
        "name": "Nouri Muhammad",
        "email": "nouri.muhammad1991@gmail.com",
    },
    license_info={
        "name": "MIT",
    },
)


@app.get("/")
async def root():
    return {"msg": "Let's Explore Allah's Creation! We provide you with a place to stay."}
