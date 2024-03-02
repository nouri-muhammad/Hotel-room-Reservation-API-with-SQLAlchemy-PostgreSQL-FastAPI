from fastapi import HTTPException, status

from db.models.hotels import (
    User, 
    UserInfo, 
    Address, 
    Country, 
    State, 
    City
)



def sign_up(
        user_name, 
        password, 
        first_name, 
        last_name, 
        social_security_num, 
        phone_num, 
        email, 
        country_name, 
        state_name, 
        city_name, 
        street, 
        unit_num, 
        address_line1, 
        address_line2,
        session_local
        ):
    session = session_local

    # check if the country, state and city exist in database 
    # (all the country names have already been passed in data_injection.py)
    # since it's not possible to include all states and cities in the world, 
    # there will be an "other" option to insert the name of the state and city and we check them up in database to add them if needed
    country = session.query(Country).filter_by(country_name = country_name).first()
    if not country:
        country = Country(country_name=country_name)
        session.add(country)
        session.flush()

    state = session.query(State).filter_by(state_name = state_name, country_id = country.id).first()
    if not state:
        state = State(state_name=state_name, country_id=country.id)
        session.add(state)
        session.flush()

    city = session.query(City).filter_by(city_name=city_name, state_id=state.id).first()
    if not city:
        city = City(state_id=state.id, city_name=city_name)
        session.add(city)
        session.flush()

    # create user record
    username_check = session.query(User).filter_by(user_name=user_name).first()
    if not username_check:
        user_record = User(user_name=user_name, password=password)
        session.add(user_record)
        session.flush()
    else:
        raise HTTPException(
            status_code=status.HTTP_226_IM_USED,
            detail="This username is already in use!"
        )

    # create user address record
    user_address = Address(
        country_id=country.id, 
        state_id=state.id, 
        city_id=city.id, 
        address_line1=address_line1, 
        address_line2=address_line2, 
        street=street, 
        unit_num=unit_num,
        user_id = user_record.id
    )    
    session.add(user_address)
    session.flush()

    # create user_info record
    email_check = session.query(UserInfo).filter_by(email=email).first()
    social_code_check = session.query(UserInfo).filter_by(social_security_num=social_security_num).first()
    if not email_check:
        if not social_code_check:
            user_info = UserInfo(
                first_name=first_name, 
                last_name=last_name, 
                user_id=user_record.id,
                social_security_num=social_security_num,
                phone_num=phone_num, 
                email=email
            )  
            session.add(user_info)
            session.flush()
        else:
            raise HTTPException(
                status_code=status.HTTP_226_IM_USED,
                detail="This security number is in use!"
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_226_IM_USED,
            detail="This email is used many times!"
        )


    # user_record.address = [user_address]
    # user_address.user = [user_record]
    session.flush()
    session.commit()
    session.close()
