from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db.db_setup import get_db
from api.utils.signup import sign_up
from api.utils.signin import sign_in
from api.utils.users import users_list, user_detail


router = APIRouter()

@router.get("/users/user/{user_name}")
async def read_user(user_name: str, db: Session = Depends(get_db)):
    return user_detail(username=user_name, session_local=db)


@router.get("/users/users_list")
async def get_users(db: Session = Depends(get_db)):
    return users_list(db)


@router.get("/users/signin")
async def user_sign_in(
    user_name: str, 
    password: str, 
    db: Session = Depends(get_db)
):
    return sign_in(
        user_name, 
        password, db
    )


@router.post("/users/signup")
async def create_user(
    user_name: str,
    password: str,
    first_name: str,
    last_name: str,
    social_security_num: str,
    phone_num: str,
    email: str,
    country_name: str,
    state_name: str,
    city_name: str,
    street: str,
    unit_num: str,
    address_line1: str,
    address_line2: Optional[str] = None,
    db: Session = Depends(get_db)
):
    sign_up(
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
        db
    )
