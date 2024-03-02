from datetime import date

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db.db_setup import get_db
from api.utils.bookings import available_rooms, reserve_room


router = APIRouter()


@router.get("/booking/available_rooms")
async def read_available_rooms(
    city: str,
    checkin_date: date,
    checkout_date: date,
    hotel_name: str=None,
    db: Session=Depends(get_db)
):
    return available_rooms(
        city=city,
        checkin_date=checkin_date,
        checkout_date=checkout_date,
        name_of_hotel=hotel_name,
        session_local=db
    )


@router.post("/booking/reserve_room")
async def room_reservation(
    user_name: str,
    city: str,
    hotel_name: str,
    room_num: str,
    checkin_date: date,
    checkout_date: date,
    adult_num: int,
    child_num: int, 
    db: Session=Depends(get_db)
):
    return reserve_room(
        user_name=user_name,
        city=city,
        hotel_name=hotel_name,
        room_num=room_num,
        checkin_date=checkin_date,
        checkout_date=checkout_date,
        adult_num=adult_num,
        child_num=child_num,
        session_local=db
    )

