from datetime import date, timedelta
import pandas as pd

from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from db.models.hotels import (
    Hotel,
    Rooms,
    City,
    Booking,
    RoomStatus,
    User
)


def available_rooms(
        city: str,
        checkin_date: date, 
        checkout_date: date, 
        session_local: Session,
        name_of_hotel: str=None
):

    session = session_local

    cityname = session.query(City).filter_by(city_name=city).first()
    if not cityname:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No hotel from this city has registered!"
        )
    if name_of_hotel:
        hotelname = session.query(Hotel).filter_by(hotel_name=name_of_hotel, city_id=cityname.id).first()
        if not hotelname:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="no hotel with the mentioned has registered!"
            )

        # getting all the rooms in the mentioned hotel
        all_rooms = session.query(Rooms).filter_by(hotel_id=hotelname.id).all()

        # creating a date range using pandas
        date_range = pd.date_range(start=checkin_date, end=checkout_date)
    
        # search if any of the rooms is reserved in the mentioned time
        rooms = []
        for room in all_rooms:
            i=1
            status = session.query(RoomStatus).filter_by(room_id=room.id).all()
            if status:
                for st in status:
                    if date_range.isin(st.booked_date).any():
                        i=0
                if i==1:
                    rooms.append(st.room_id)
            else:
                rooms.append(room.id)
        
        query = session.query(Rooms)
        query = query.filter(Rooms.id.in_(rooms)).all()

        return query

    if not name_of_hotel:
        pass


def get_date_range(checkin_date, checkout_date):
    current_date = checkin_date
    while current_date <= checkout_date:
        yield current_date
        current_date += timedelta(days=1)


def get_reservation_day_num(checkin_date, checkout_date):
    dif = checkout_date - checkin_date
    num_nights = dif.days
    return num_nights


def reserve_room(
        user_name: str,
        city: str,
        hotel_name: str,
        room_num: str,
        checkin_date: date,
        checkout_date: date,
        adult_num: int,
        child_num: int,
        session_local: Session,
):
    session = session_local
    
    username = session.query(User).filter_by(user_name=user_name).first()
    if not username:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="There is no user with the specified username"
        ) 

    cityname = session.query(City).filter_by(city_name=city).first()
    if not cityname:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No hotel from this city has registered!"
        )
    
    hotelname = session.query(Hotel).filter_by(hotel_name=hotel_name, city_id=cityname.id).first()
    if not hotelname:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No hotel with this name has registered!"
        )

    roomcheck = session.query(Rooms).filter_by(room_number=room_num, hotel_id=hotelname.id).first()
    if not roomcheck:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No room with this room number, in the specified hotel has registered!"
        )

    roomstatus = session.query(RoomStatus).filter_by(room_id=roomcheck.id).all()
    if roomstatus:
        date_range = pd.date_range(start=checkin_date, end=checkout_date)

        for rmst in roomstatus:
            if date_range.isin(rmst.booked_date).any():
                raise HTTPException(
                    status_code=status.HTTP_226_IM_USED,
                    detail="This room is reserved in that period!"
                )
    
    dates = [checkin_date + timedelta(days=i) for i in range((checkout_date - checkin_date).days + 1)]
    roomstat = RoomStatus(
        room_id=roomcheck.id,
        booked_date=dates
    )            
    session.add(roomstat)
    session.flush()

    # add in booking table
    booking = Booking(
        user_id=username.id,
        booking_price=roomcheck.price * get_reservation_day_num(checkin_date=checkin_date, checkout_date=checkout_date),
        room_id=roomcheck.id,
        checkin_date=checkin_date,
        checkout_date=checkout_date,
        adult_num=adult_num,
        children_num=child_num,
        paid_status=True
    )
    session.add(booking)
    session.flush()

    session.commit()
            
    return {"msg": f"Room{room_num} is reserved for you from {checkin_date} to {checkout_date}"}








