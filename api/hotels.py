from typing import Optional

from fastapi import APIRouter, Depends
from fastapi.params import Query
from sqlalchemy.orm import Session

from db.db_setup import get_db
from api.utils.hotels import hotel_registery, room_registery, hotel_search_by_location, room_search_by_hotel


router = APIRouter()


@router.post("/hotels/register")
async def hotel_register(
    country: str, 
    state: str, 
    city: str, 
    hotel_name: str, 
    web_address: str, 
    stars: int, 
    address: str, 
    description: str, 
    manager: str = None, 
    db: Session=Depends(get_db)
):
    return hotel_registery(
        country=country, 
        state=state, 
        city=city, 
        hotel_name=hotel_name, 
        web_address=web_address, 
        stars=stars, 
        address=address, 
        description=description, 
        manager=manager, 
        session_local=db
    )


@router.post("/hotels/rooms/register")
async def hotel_room_register(
    hotel_name: str, 
    floor_num: int, 
    room_num: str, 
    capacity: int, 
    bed_num:int, 
    price: float, 
    class_name: str = Query(description="standard, suite, deluxe"), 
    db: Session=Depends(get_db)
):
    return room_registery(
        hotel_name=hotel_name, 
        floor_num=floor_num, 
        class_name=class_name, 
        room_num=room_num, 
        capacity=capacity, 
        bed_num=bed_num, 
        price=price, 
        session_local=db
    )


@router.get("/hotels/search_by_city")
async def hotel_search(
    city: str,
    hotel_name: Optional[str]=None,
    stars: Optional[int]=None,
    db: Session=Depends(get_db)
):
    return hotel_search_by_location(
        city=city,
        hotel_name=hotel_name,
        stars=stars,
        session_local=db
    )


@router.get("/hotels/{city}/{hotel_name}/rooms")
async def hotel_rooms(
    city: str,
    hotel_name: str,
    db: Session=Depends(get_db)
):
    return room_search_by_hotel(
        city=city,
        hotel_name=hotel_name,
        session_local=db
    )


# TODO: add list of available rooms in a specific date after you're done with booking


