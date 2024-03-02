from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from db.models.hotels import (
    Hotel,
    Rooms,
    City,
    State,
    Country,
    ClassName,
    Floor
)


def hotel_registery(
        country:str, state: str, city: str, hotel_name: str, web_address: str, stars: int, 
        address: str, description: str, session_local: Session, manager: str = None
):
    session = session_local

    # check if the location is already exist in database or not! 

    countryname = session.query(Country).filter_by(country_name=country).first()
    if not countryname:
        country = Country(country_name=country)
        session.add(country)
        session.flush()
        state = State(state_name=state, country_id=country.id)
        session.add(state)
        session.flush()
        city = City(city_name=city, state_id=state.id)
        session.add(city)
        session.flush()
    else:
        country=countryname
        statename = session.query(State).filter_by(state_name=state).first()
        if not statename:
            state = State(state_name=state, country_id=country.id)
            session.add(state)
            session.flush()
            city = City(city_name=city, state_id=state.id)
            session.add(city)
            session.flush()
        else:
            state=statename
            cityname = session.query(City).filter_by(city_name=city).first()
            if not cityname:
                city = City(city_name=city, state_id=state.id)
                session.add(city)
                session.flush()
            else:
                city=cityname

    
    hotel = session.query(Hotel).filter_by(hotel_name=hotel_name, city_id=city.id).first()
    # by the logic that two hotels with same name in one city cannot exist
    if hotel:
        raise HTTPException(
            status_code=status.HTTP_226_IM_USED,
            detail="This hotel have already been registered!"
        )
    else:
        new_hotel = Hotel(
            city_id=city.id,
            hotel_name=hotel_name,
            web_address=web_address,
            stars=stars,
            address=address,
            description=description,
            manager=manager
        )
    session.add(new_hotel)
    session.flush()
    session.commit()
    session.close()
    return {"message": f"Hotel {hotel_name} Successfully added"}


def room_registery(
        hotel_name: str,
        floor_num: int,
        class_name: ClassName,
        room_num: str,
        capacity: int,
        bed_num: int,
        price: float,
        session_local: Session
):
    session = session_local

    # check the hotel
    hotel = session.query(Hotel).filter_by(hotel_name=hotel_name).first()
    if not hotel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Hotel not found"
        )

    # check if the class_name is valid
    if class_name not in ClassName.__members__:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid room class name"
        )
    
    floor = session.query(Floor).filter_by(floor_num=floor_num).first()
    if not floor:
        floor=Floor(floor_num=floor)
        session.add(floor)
        session.flush()

    room = Rooms(
        hotel_id=hotel.id,
        floor_id=floor.id,
        room_class_id=ClassName[class_name],
        room_number=room_num,
        capacity=capacity,
        bed_num=bed_num,
        price=price
    )
    session.add(room)
    session.flush()
    session.commit()
    return {"message": f"Room {room_num} Successfully added"}


def hotel_search_by_location(
        city: str,
        hotel_name: str, 
        stars: int, 
        session_local: Session
):
    session = session_local

    # check the city
    cityname = session.query(City).filter_by(city_name=city).first()
    if city:
        if not cityname:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No hotel from this city has registered!"
            )
    if hotel_name:
        hotelname = session.query(Hotel).filter_by(hotel_name=hotel_name)
        if not hotelname:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No hotel with the specified name has registered!"
            )
    if stars:
        star = session.query(Hotel).filter_by(stars=stars)
        if not star:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No hotel with the desired stars is available!"
            )
    
    # create queries if there is no error
    query = session.query(Hotel)
    
    query = query.filter(Hotel.city_id == cityname.id)
    if hotel_name:
        query = query.filter(Hotel.hotel_name == hotel_name)
    if stars:
        query = query.filter(Hotel.stars == stars)
    
    result = query.all()
    return result 


def room_search_by_hotel(
        city: str,
        hotel_name: str,
        session_local: Session
):
    session = session_local

    cityname = session.query(City).filter_by(city_name=city).first()
    if not cityname:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No hotel from this city has registered!"
            )

    hotelname = session.query(Hotel).filter_by(hotel_name=hotel_name).first()
    if not hotelname:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No hotel with the specified name has registered!"
        )

    query = session.query(Hotel)
    query = query.filter(Hotel.city_id == cityname.id, Hotel.hotel_name == hotel_name).first()

    roomquery = session.query(Rooms)
    roomquery = roomquery.filter(Rooms.hotel_id == hotelname.id).first()

    if not roomquery:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="This hotel have not registered any rooms"
        )

    result = roomquery

    return result 

